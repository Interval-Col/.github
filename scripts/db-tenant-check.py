#!/usr/bin/env python3
"""db-tenant-check — shared-DB tenant contract conformance gate (RFC 0015 Phase 1).

Asserts the *mechanical subset* of the tenant contract (db-tenant-contract.md)
against a repo, driven by the repo's own `.db-tenant.yml` manifest:

  T1  manifest valid (profile known, referenced paths exist)
  T2  migrate one-shot chain wired in the deploy compose file
      (each link depends_on the previous with service_completed_successfully;
       no link parked behind `profiles:`)
  T3  no DDL on app startup (command.upgrade / init_db / create_all /
      CREATE SCHEMA outside alembic roots must be allowlisted with a reason)
  T4  TLS wiring present (sslmode + CA cert in deploy compose or backend config;
      or an opaque-secret DSN documented in the manifest)
  T5  DSN password never interpolated into a raw f-string (URL.create() or
      opaque secret; exceptions allowlisted with a reason)
  T6  /health-style liveness + /ready-style readiness (with a DB probe) present
  T7  (info only) CREATE SCHEMA in alembic env.py — moves to the nucleus-db
      steward under C-lite (RFC 0015 Phase 2); never fails

Deliberately stdlib-only (same rule as plan_lint.py): a future *required* check
must not depend on PyPI availability on the merge path. The manifest and compose
parsers therefore accept a strict, documented subset of YAML and fail loudly on
anything they do not understand — misparse must never pass silently.

Usage:
  db-tenant-check.py --manifest .db-tenant.yml [--enforce] [--json out.json]

Exit code: 0 unless --enforce is set and at least one check FAILs.
Do NOT edit per-repo copies — this script lives in Interval-Col/.github and is
executed from there by the reusable workflow db-tenant-check.yml.
"""

import argparse
import json
import os
import re
import sys

PROFILES = ("alembic-app", "dml-only", "pre-onboarding")

# T3 patterns: the RFC-named startup-DDL subset for alembic apps; dml-only
# repos own zero DDL, so any DDL statement text in code is suspect there.
DDL_COMMON = [
    r"\bcommand\.upgrade\s*\(",
    r"\binit_db\s*\(",
    r"\.create_all\s*\(",
    r"\bCREATE\s+SCHEMA\b",
]
DDL_DML_ONLY_EXTRA = [
    r"\bCREATE\s+TABLE\b",
    r"\bALTER\s+TABLE\b",
    r"\bDROP\s+TABLE\b",
]

PASS, FAIL, WARN, INFO, SKIP = "PASS", "FAIL", "WARN", "INFO", "SKIP"
ICON = {PASS: "✅", FAIL: "❌", WARN: "⚠️", INFO: "ℹ️", SKIP: "⏭️"}


class ManifestError(Exception):
    pass


# --------------------------------------------------------------------------
# Strict mini-YAML parser (manifest subset only — see db-tenant-contract.md)
# Supports: comments, `key: scalar`, `key: [a, b]`, one-level nested maps,
# block lists of scalars, and block lists of flat maps. Anything else errors.
# --------------------------------------------------------------------------

def _scalar(tok):
    tok = tok.strip()
    if tok in ("null", "~", ""):
        return None
    if tok in ("true", "True"):
        return True
    if tok in ("false", "False"):
        return False
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    return tok


def _strip_comment(line):
    # Remove a trailing comment (a # preceded by whitespace), respecting quotes.
    out, in_q = [], None
    for i, ch in enumerate(line):
        if in_q:
            if ch == in_q:
                in_q = None
        elif ch in "\"'":
            in_q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def parse_manifest(text, path):
    lines = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw)
        if line.strip():
            lines.append((n, line))

    root, i = {}, 0
    while i < len(lines):
        n, line = lines[i]
        if line.startswith(" "):
            raise ManifestError(f"{path}:{n}: unexpected indentation")
        m = re.match(r"^([A-Za-z0-9_]+):(.*)$", line)
        if not m:
            raise ManifestError(f"{path}:{n}: expected `key: value`")
        key, rest = m.group(1), m.group(2).strip()
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            root[key] = [_scalar(t) for t in inner.split(",")] if inner else []
            i += 1
        elif rest:
            root[key] = _scalar(rest)
            i += 1
        else:
            # Block value: nested map, list of scalars, or list of flat maps.
            i += 1
            block = []
            while i < len(lines) and lines[i][1].startswith("  "):
                block.append(lines[i])
                i += 1
            if not block:
                root[key] = None
            elif block[0][1].lstrip().startswith("- "):
                root[key] = _parse_block_list(block, path)
            else:
                root[key] = _parse_flat_map(block, path)
    return root


def _parse_flat_map(block, path):
    out = {}
    for n, line in block:
        m = re.match(r"^  ([A-Za-z0-9_]+):(.*)$", line)
        if not m:
            raise ManifestError(f"{path}:{n}: expected `  key: value` in nested map")
        out[m.group(1)] = _scalar(m.group(2))
    return out


def _parse_block_list(block, path):
    items, current = [], None
    for n, line in block:
        stripped = line.strip()
        if stripped.startswith("- "):
            body = stripped[2:]
            m = re.match(r"^([A-Za-z0-9_]+):(.*)$", body)
            if m:  # list of maps
                current = {m.group(1): _scalar(m.group(2))}
                items.append(current)
            else:  # list of scalars
                current = None
                items.append(_scalar(body))
        elif current is not None:
            m = re.match(r"^([A-Za-z0-9_]+):(.*)$", stripped)
            if not m:
                raise ManifestError(f"{path}:{n}: expected `key: value` in list item")
            current[m.group(1)] = _scalar(m.group(2))
        else:
            raise ManifestError(f"{path}:{n}: continuation line outside a map item")
    return items


# --------------------------------------------------------------------------
# Compose scanner — extracts, per service: profiles present?, depends_on map.
# Indentation-scoped line scan (2-space convention org-wide); strict enough
# that an unrecognized layout surfaces as a missing service (FAIL), never a
# silent pass.
# --------------------------------------------------------------------------

def parse_compose_services(text):
    services, current, dep_target = {}, None, None
    in_services, in_depends = False, False
    for raw in text.splitlines():
        line = _strip_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            in_services = stripped == "services:"
            current = None
            continue
        if not in_services:
            continue
        if indent == 2 and stripped.endswith(":") and not stripped.startswith("-"):
            current = stripped[:-1]
            services[current] = {"profiles": False, "depends_on": {}}
            in_depends = False
            continue
        if current is None:
            continue
        if indent == 4:
            in_depends = stripped.startswith("depends_on")
            if stripped.startswith("profiles"):
                services[current]["profiles"] = True
            dep_target = None
            continue
        if in_depends and indent == 6:
            if stripped.startswith("- "):
                services[current]["depends_on"][stripped[2:].strip()] = None
            elif stripped.endswith(":"):
                dep_target = stripped[:-1]
                services[current]["depends_on"][dep_target] = None
            continue
        if in_depends and indent == 8 and dep_target:
            m = re.match(r"^condition:\s*(\S+)$", stripped)
            if m:
                services[current]["depends_on"][dep_target] = m.group(1)
    return services


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def walk_py(root, exclude_dirs):
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, ".")
        dirnames[:] = [
            d for d in dirnames
            if d not in ("node_modules", ".git", "__pycache__", ".venv", "venv")
            and not any(
                os.path.join(rel_dir, d).startswith(ex.rstrip("/")) or d == "tests"
                for ex in exclude_dirs
            )
        ]
        for f in filenames:
            if f.endswith(".py"):
                yield os.path.join(rel_dir, f)


def check(manifest, results):
    profile = manifest.get("profile")
    app = manifest.get("app", "?")

    # T1 — manifest validity
    problems = []
    if profile not in PROFILES:
        problems.append(f"unknown profile {profile!r} (expected one of {PROFILES})")
    if profile == "pre-onboarding":
        if problems:
            results.append(("T1", FAIL, "; ".join(problems)))
        else:
            results.append(("T1", PASS, f"manifest valid for {app}"))
            results.append(("T2", INFO,
                            "pre-onboarding: not yet a nucleus-db tenant — full contract "
                            "applies at onboarding under C-lite (RFC 0015 Phase 2)"))
        return

    backend = manifest.get("backend_dir")
    compose = manifest.get("deploy_compose")
    for label, p in (("backend_dir", backend), ("deploy_compose", compose)):
        if not p or not os.path.exists(p):
            problems.append(f"{label} missing or not found: {p!r}")
    for r in manifest.get("alembic_roots") or []:
        if not os.path.isdir(r):
            problems.append(f"alembic root not found: {r!r}")
    if problems:
        results.append(("T1", FAIL, "; ".join(problems)))
        return
    results.append(("T1", PASS, f"manifest valid for {app} (profile: {profile})"))

    compose_text = open(compose, encoding="utf-8").read()
    services = parse_compose_services(compose_text)

    # T2 — migrate one-shot chain
    chain = manifest.get("deploy_chain") or []
    if profile == "dml-only" and not chain:
        results.append(("T2", INFO, "dml-only: owns zero DDL, no migrate one-shot by design"))
    elif len(chain) < 2:
        results.append(("T2", FAIL, "deploy_chain must list migrate → … → app services"))
    else:
        errs = []
        for svc in chain:
            if svc not in services:
                errs.append(f"service {svc!r} not defined in {compose}")
        for svc in chain[:-1]:
            if svc in services and services[svc]["profiles"]:
                errs.append(f"one-shot {svc!r} is parked behind `profiles:` — deploy never runs it")
        for prev, nxt in zip(chain, chain[1:]):
            cond = services.get(nxt, {}).get("depends_on", {}).get(prev)
            if cond != "service_completed_successfully":
                errs.append(
                    f"{nxt!r} must depends_on {prev!r} with "
                    f"condition service_completed_successfully (found: {cond!r})")
        if errs:
            results.append(("T2", FAIL, "; ".join(errs)))
        else:
            results.append(("T2", PASS, " → ".join(chain) + " wired with service_completed_successfully"))

    # T3 — no DDL on app startup
    patterns = list(DDL_COMMON) + (DDL_DML_ONLY_EXTRA if profile == "dml-only" else [])
    rx = re.compile("|".join(patterns))
    allow = {a["file"]: a.get("reason", "") for a in (manifest.get("startup_ddl_allow") or [])}
    exclude = list(manifest.get("alembic_roots") or [])
    hits, allowed = [], []
    for path in walk_py(backend, exclude):
        norm = path.replace(os.sep, "/")
        try:
            body = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for i, line in enumerate(body.splitlines(), 1):
            # Ignore Python line comments — prose mentioning create_all() etc.
            # must not trip the gate; only executable text counts.
            if rx.search(line.split("#", 1)[0]):
                if norm in allow:
                    allowed.append(f"{norm} (reason: {allow[norm]})")
                    break
                hits.append(f"{norm}:{i}: {line.strip()[:80]}")
    if hits:
        results.append(("T3", FAIL, "startup-DDL pattern outside alembic roots, not allowlisted: "
                        + "; ".join(hits[:5])))
    else:
        detail = "no unallowlisted startup-DDL patterns"
        if allowed:
            detail += " — allowlisted: " + "; ".join(sorted(set(allowed)))
        results.append(("T3", PASS, detail))

    # T4 — TLS wiring
    if manifest.get("dsn_style") == "opaque-secret":
        env = manifest.get("dsn_env") or "?"
        if env in compose_text:
            results.append(("T4", PASS,
                            f"opaque-secret DSN ({env}) referenced in {compose}; "
                            "secret must carry sslmode=verify-full (contract §TLS)"))
        else:
            results.append(("T4", FAIL, f"dsn_env {env!r} not referenced in {compose}"))
    else:
        config_text = ""
        for path in walk_py(backend, list(manifest.get("alembic_roots") or [])):
            if re.search(r"(config|database|db)\.py$", path):
                config_text += open(path, encoding="utf-8", errors="replace").read()
        has_sslmode = "sslmode" in compose_text or "sslmode" in config_text
        has_ca = bool(re.search(r"sslrootcert|ca[_.-]?cert|\.crt", compose_text + config_text, re.I))
        if has_sslmode and has_ca:
            results.append(("T4", PASS, "sslmode + CA cert wiring found in deploy compose / backend config"))
        else:
            results.append(("T4", FAIL,
                            f"TLS wiring incomplete (sslmode found: {has_sslmode}, CA cert found: {has_ca}) "
                            "— contract requires verify-full in prod"))

    # T5 — DSN password interpolation
    if manifest.get("dsn_style") == "opaque-secret":
        results.append(("T5", PASS, "DSN is an opaque secret; no in-code assembly"))
    else:
        # Match password interpolation even when the f-string is split across
        # lines (implicit concatenation: `…{password}"` / `f"@{host}…`).
        dsn_rx = re.compile(
            r"postgresql(\+[a-z0-9]+)?://\{[^}]+\}:\{[^}]+\}[\"']?\s*f?[\"']?@")
        allow5 = {a["file"]: a.get("reason", "") for a in (manifest.get("dsn_allow") or [])}
        bad, waived = [], []
        url_create = False
        for path in walk_py(backend, list(manifest.get("alembic_roots") or [])):
            norm = path.replace(os.sep, "/")
            body = open(path, encoding="utf-8", errors="replace").read()
            if "URL.create(" in body:
                url_create = True
            if dsn_rx.search(body):
                (waived if norm in allow5 else bad).append(
                    norm + (f" (reason: {allow5[norm]})" if norm in allow5 else ""))
        if bad:
            results.append(("T5", FAIL,
                            "raw f-string DSN with interpolated password (not URL-encoded): "
                            + "; ".join(bad)))
        else:
            detail = "no unallowlisted raw-DSN assembly"
            if url_create:
                detail += "; URL.create() present (encodes password)"
            if waived:
                detail += " — allowlisted: " + "; ".join(waived)
            results.append(("T5", PASS, detail))

    # T6 — health endpoints
    health = manifest.get("health") or {}
    live, ready = health.get("liveness"), health.get("readiness")
    if not ready:
        results.append(("T6", FAIL,
                        "no readiness endpoint declared — contract requires a /ready-style "
                        "endpoint with a DB probe (SELECT 1)"))
    else:
        found_live, found_ready, ready_has_probe = not live, False, False
        for path in walk_py(backend, list(manifest.get("alembic_roots") or [])):
            body = open(path, encoding="utf-8", errors="replace").read()
            if live and re.search(r"""(get|route|api_route)\(\s*["']""" + re.escape(live) + r"""["']""", body):
                found_live = True
            if re.search(r"""(get|route|api_route)\(\s*["']""" + re.escape(ready) + r"""["']""", body):
                found_ready = True
                if re.search(r"SELECT\s+1", body, re.I):
                    ready_has_probe = True
        if not found_ready:
            results.append(("T6", FAIL, f"readiness route {ready!r} not found in {backend}"))
        elif not ready_has_probe:
            results.append(("T6", WARN, f"readiness route {ready!r} found but no `SELECT 1` DB probe in the same file"))
        elif live and not found_live:
            results.append(("T6", WARN, f"liveness route {live!r} not found (readiness OK)"))
        else:
            results.append(("T6", PASS, f"liveness {live!r} + readiness {ready!r} with DB probe"))

    # T7 — schema shell in env.py (informational; C-lite / Phase 2 target)
    shells = []
    for root in manifest.get("alembic_roots") or []:
        env_py = os.path.join(root, "env.py")
        if os.path.exists(env_py):
            body = open(env_py, encoding="utf-8", errors="replace").read()
            if re.search(r"CREATE\s+SCHEMA", body, re.I):
                shells.append(env_py)
    if shells:
        results.append(("T7", INFO,
                        "CREATE SCHEMA in " + ", ".join(shells)
                        + " — moves to the nucleus-db steward under C-lite (RFC 0015 Phase 2)"))
    else:
        results.append(("T7", INFO, "no CREATE SCHEMA in alembic env.py"))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", default=".db-tenant.yml")
    ap.add_argument("--enforce", action="store_true",
                    help="exit non-zero on FAIL (required-check mode; default is advisory)")
    ap.add_argument("--json", help="also write machine-readable results to this path")
    args = ap.parse_args()

    results = []
    try:
        manifest = parse_manifest(open(args.manifest, encoding="utf-8").read(), args.manifest)
    except (OSError, ManifestError) as e:
        manifest = {}
        results.append(("T1", FAIL, f"cannot load manifest: {e}"))
    if manifest:
        check(manifest, results)

    app = manifest.get("app", os.path.basename(os.getcwd()))
    profile = manifest.get("profile", "?")
    mode = "enforce" if args.enforce else "advisory"
    failed = [r for r in results if r[1] == FAIL]

    lines = [f"## db-tenant-check — {app} (profile: {profile}, mode: {mode})", "",
             "| check | status | detail |", "|---|---|---|"]
    for cid, status, detail in results:
        lines.append(f"| {cid} | {ICON[status]} {status} | {detail} |")
    lines.append("")
    verdict = ("**DRIFT** — see contract: Interval-Col/.github/db-tenant-contract.md"
               if failed else "**conformant**")
    if failed and not args.enforce:
        verdict += " _(advisory mode: not blocking — flips to required per RFC 0015 OQ4)_"
    lines.append(verdict)
    report = "\n".join(lines)

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(report + "\n")
    for cid, status, detail in results:
        if status == FAIL:
            kind = "error" if args.enforce else "warning"
            print(f"::{kind}::db-tenant-check {cid}: {detail}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"app": app, "profile": profile, "mode": mode,
                       "conformant": not failed,
                       "results": [{"check": c, "status": s, "detail": d}
                                   for c, s, d in results]}, fh, indent=2)

    sys.exit(1 if (failed and args.enforce) else 0)


if __name__ == "__main__":
    main()
