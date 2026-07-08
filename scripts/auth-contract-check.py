#!/usr/bin/env python3
"""auth-contract-check — Pháros auth contract conformance gate (RFC 0016 Phase 1).

Asserts the *mechanical subset* of the auth contract (auth-contract.md) against an
app, driven by the app's own `.auth-contract.yml` manifest:

  A1  manifest valid (profile known, referenced paths exist)
  A2  the 7 /auth/admin/* endpoints present in the admin router (at least these)
  A3  require_capability guards unknown capability ids (KeyError at import)
  A4  no seeding / upgrade / create_all on app startup (allowlist = file + reason)
  A5  every FE capability reference is a subset of the backend catalog
  A6  auth tables present; role column width >= the standard minimum
  A7  runtime role registry (create/rename/delete-role) present (info/warn)
  A8  require_role used as a gate is an allowlisted documented shim (info/warn)

Deliberately stdlib-only (same rule as db-tenant-check.py): a future *required*
check must not depend on PyPI on the merge path. The manifest parser therefore
accepts a strict, documented subset of YAML and fails loudly on anything it does
not understand — misparse must never pass silently.

Usage:
  auth-contract-check.py --manifest .auth-contract.yml [--enforce] [--json out.json]

Exit code: 0 unless --enforce is set and at least one check FAILs.
Do NOT edit per-repo copies — this script lives in Interval-Col/.github and is
executed from there by the reusable workflow auth-contract-check.yml.
"""

import argparse
import json
import os
import re
import sys

PROFILES = ("app", "greenfield")

# A2 — the seven contract admin endpoints (router-relative; path-param names are
# matched leniently so {username}/{user} etc. do not matter). At-least-these:
# finance-lch also carries POST/PATCH/DELETE /roles (the role registry, A7).
ADMIN_ENDPOINTS = [
    ("GET /users",                    r'@\w+\.get\(\s*["\']/users["\']'),
    ("POST /users",                   r'@\w+\.post\(\s*["\']/users["\']'),
    ("PATCH /users/{username}",       r'@\w+\.patch\(\s*["\']/users/\{[^}]+\}["\']'),
    ("DELETE /users/{username}",      r'@\w+\.delete\(\s*["\']/users/\{[^}]+\}["\']'),
    ("GET /capabilities",            r'@\w+\.get\(\s*["\']/capabilities["\']'),
    ("GET /roles",                    r'@\w+\.get\(\s*["\']/roles["\']'),
    ("PUT /roles/{role}/capabilities", r'@\w+\.put\(\s*["\']/roles/\{[^}]+\}/capabilities["\']'),
]

# A7 — the runtime role-registry endpoints (create / rename / delete a role).
REGISTRY_POST   = r'@\w+\.post\(\s*["\']/roles["\']'
REGISTRY_MUTATE = r'@\w+\.(patch|delete)\(\s*["\']/roles/\{[^}]+\}["\']'   # not .../capabilities

# A4 — seeding / DDL patterns that must not run on app startup (only in a
# deploy-step one-shot / seeds module). Prose in comments is ignored.
STARTUP_SEED = [
    r"\bensure_bootstrap_admin\s*\(",
    r"\bensure_role_capabilities_seed\s*\(",
    r"\bensure_roles_seed\s*\(",
    r"\binit_db\s*\(",
    r"\bcommand\.upgrade\s*\(",
    r"\.create_all\s*\(",
]

CAP_KEY = re.compile(r'["\']([A-Za-z][\w]*(?:\.[\w]+)+)["\']\s*:')   # dotted dict key
FE_REQ  = re.compile(r'requiresCap:\s*["\']([\w.]+)["\']')
FE_CAN  = re.compile(r'\bcan\(\s*["\']([\w.]+)["\']')
ROLE_W  = re.compile(r'\brole\b[^\n]*String\((\d+)\)')
TABLE   = re.compile(r'__tablename__\s*=\s*["\'](\w+)["\']')

PASS, FAIL, WARN, INFO, SKIP = "PASS", "FAIL", "WARN", "INFO", "SKIP"
ICON = {PASS: "✅", FAIL: "❌", WARN: "⚠️", INFO: "ℹ️", SKIP: "⏭️"}


class ManifestError(Exception):
    pass


# --------------------------------------------------------------------------
# Strict mini-YAML parser (manifest subset only — see auth-contract.md).
# Shared verbatim with db-tenant-check.py: comments, `key: scalar`,
# `key: [a, b]`, one-level nested maps, block lists of scalars / flat maps.
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
            if m:
                current = {m.group(1): _scalar(m.group(2))}
                items.append(current)
            else:
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
# Helpers
# --------------------------------------------------------------------------

def _read(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def walk_fe(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       ("node_modules", ".git", ".nuxt", ".output", "dist", "__pycache__")]
        for f in filenames:
            if f.endswith((".vue", ".ts", ".js", ".mjs")):
                yield os.path.join(dirpath, f)


def _strip_web_comments(text):
    """Drop /* */, <!-- -->, and // line comments so doc examples like
    `// can('cap.id')` are not mistaken for real capability references."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    for line in text.splitlines():
        m = re.search(r"(?<!:)//", line)   # a // that isn't part of a :// URL
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def _grep_code(text, rx):
    """True if rx matches any line with its Python/JS line-comment stripped."""
    for line in text.splitlines():
        code = re.split(r"#|//", line, maxsplit=1)[0]
        if rx.search(code):
            return True
    return False


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check(manifest, results):
    profile = manifest.get("profile")
    app = manifest.get("app", "?")

    # A1 — manifest validity
    problems = []
    if profile not in PROFILES:
        problems.append(f"unknown profile {profile!r} (expected one of {PROFILES})")
    if profile == "greenfield":
        if problems:
            results.append(("A1", FAIL, "; ".join(problems)))
        else:
            results.append(("A1", PASS, f"manifest valid for {app}"))
            results.append(("A2", INFO,
                            "greenfield: no auth module yet — the full contract applies "
                            "when this app adopts the shared auth (RFC 0016 Phase 4)"))
        return

    auth_dir   = manifest.get("auth_dir")
    admin_rt   = manifest.get("admin_router")
    deps       = manifest.get("deps")
    caps       = manifest.get("capabilities")
    models     = manifest.get("models") or (auth_dir and os.path.join(auth_dir, "models.py"))
    frontend   = manifest.get("frontend_dir")
    for label, p in (("auth_dir", auth_dir), ("admin_router", admin_rt),
                     ("deps", deps), ("capabilities", caps), ("models", models),
                     ("frontend_dir", frontend)):
        if not p or not os.path.exists(p):
            problems.append(f"{label} missing or not found: {p!r}")
    if problems:
        results.append(("A1", FAIL, "; ".join(problems)))
        return
    results.append(("A1", PASS, f"manifest valid for {app} (profile: {profile})"))

    admin_text = _read(admin_rt) or ""
    deps_text  = _read(deps) or ""

    # A2 — the 7 admin endpoints (at least these)
    missing = [name for name, pat in ADMIN_ENDPOINTS if not re.search(pat, admin_text)]
    if missing:
        results.append(("A2", FAIL, f"missing admin endpoint(s) in {admin_rt}: " + ", ".join(missing)))
    else:
        results.append(("A2", PASS, f"all 7 /auth/admin/* endpoints present in {admin_rt}"))

    # A3 — require_capability rejects unknown ids
    if re.search(r"if\s+capability\s+not\s+in\s+CAPABILITIES", deps_text):
        results.append(("A3", PASS, f"require_capability guards unknown ids in {deps}"))
    else:
        results.append(("A3", FAIL,
                        f"no `if capability not in CAPABILITIES` guard in {deps} "
                        "— an unknown capability must raise at import, not pass silently"))

    # A4 — no seeding/DDL on app startup
    rx = re.compile("|".join(STARTUP_SEED))
    allow = {a["file"]: a.get("reason", "") for a in (manifest.get("startup_seed_allow") or [])}
    startup_files = manifest.get("startup_files") or ["backend/app/main.py"]
    hits, allowed = [], []
    for f in startup_files:
        body = _read(f)
        if body is None:
            continue
        norm = f.replace(os.sep, "/")
        for i, line in enumerate(body.splitlines(), 1):
            if rx.search(line.split("#", 1)[0]):
                if norm in allow:
                    allowed.append(f"{norm} (reason: {allow[norm]})")
                    break
                hits.append(f"{norm}:{i}: {line.strip()[:80]}")
    if hits:
        results.append(("A4", FAIL, "seeding/DDL on app startup (move to a deploy-step one-shot, "
                        "or allowlist with a reason): " + "; ".join(hits[:6])))
    else:
        detail = "no unallowlisted startup seeding/DDL"
        if allowed:
            detail += " — allowlisted: " + "; ".join(sorted(set(allowed)))
        results.append(("A4", PASS, detail))

    # A5 — FE capability refs subset of the backend catalog
    caps_text = _read(caps) or ""
    catalog = set(CAP_KEY.findall(caps_text))
    if not catalog:
        results.append(("A5", WARN, f"could not extract a capability catalog from {caps}"))
    elif not frontend or not os.path.isdir(frontend):
        results.append(("A5", SKIP, f"no frontend_dir to scan ({frontend!r})"))
    else:
        fe_refs = {}
        for f in walk_fe(frontend):
            body = _strip_web_comments(_read(f) or "")
            for cap in FE_REQ.findall(body) + FE_CAN.findall(body):
                fe_refs.setdefault(cap, f)
        unknown = {c: p for c, p in fe_refs.items() if c not in catalog}
        if unknown:
            detail = "; ".join(f"{c} ({os.path.relpath(p)})" for c, p in list(unknown.items())[:6])
            results.append(("A5", FAIL, f"FE references capabilities not in the backend catalog: {detail}"))
        else:
            results.append(("A5", PASS,
                            f"{len(fe_refs)} FE capability ref(s) all in the {len(catalog)}-key catalog"))

    # A6 — auth tables present; role column width >= standard
    models_text = _read(models) or ""
    tables = set(TABLE.findall(models_text))
    want_tables = manifest.get("auth_tables") or []
    missing_t = [t for t in want_tables if t not in tables]
    widths = [int(w) for w in ROLE_W.findall(models_text)]
    role_min = manifest.get("role_col_min") or 32
    if missing_t:
        results.append(("A6", FAIL, f"auth table(s) not found in {models}: " + ", ".join(missing_t)))
    elif not widths:
        results.append(("A6", WARN, f"could not read a role column width from {models}"))
    elif min(widths) < int(role_min):
        results.append(("A6", WARN, f"role column width {min(widths)} < standard minimum {role_min} "
                        "(widen — `String(20)` is one char from the wall, RFC 0016 §2c)"))
    else:
        results.append(("A6", PASS, f"auth tables present; role width {min(widths)} >= {role_min}"))

    # A7 — runtime role registry (create/rename/delete role)
    has_post = bool(re.search(REGISTRY_POST, admin_text))
    has_mutate = bool(re.search(REGISTRY_MUTATE, admin_text))
    custom = str(manifest.get("custom_roles", "on")).lower()
    if has_post and has_mutate:
        results.append(("A7", PASS, "runtime role registry present (POST/PATCH/DELETE /roles)"))
    elif custom == "off":
        results.append(("A7", INFO, "no role registry yet; manifest declares `custom_roles: off` "
                        "(closed vocabulary until D4 lands — RFC 0016 Phase 2)"))
    else:
        results.append(("A7", WARN, "manifest declares `custom_roles: on` but no create/rename/delete-role "
                        "endpoints found — add the role registry (RFC 0016 D4)"))

    # A8 — require_role used as a gate must be an allowlisted documented shim
    allow8 = {a["file"]: a.get("reason", "") for a in (manifest.get("require_role_allow") or [])}
    gate_rx = re.compile(r"Depends\(\s*require_role\s*\(")
    scan_root = manifest.get("backend_dir") or auth_dir
    used, waived = [], []
    for dirpath, dirnames, filenames in os.walk(scan_root):
        dirnames[:] = [d for d in dirnames if d not in
                       ("node_modules", ".git", "__pycache__", ".venv", "venv", "tests")]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            body = _read(p) or ""
            if _grep_code(body, gate_rx):
                norm = os.path.relpath(p).replace(os.sep, "/")
                (waived if norm in allow8 else used).append(
                    norm + (f" (reason: {allow8[norm]})" if norm in allow8 else ""))
    if used:
        results.append(("A8", WARN, "require_role used as a gate (should be capability-only, or an "
                        "allowlisted documented shim): " + "; ".join(sorted(set(used))[:6])))
    else:
        detail = "no require_role gates (capability-only)"
        if waived:
            detail += " — allowlisted shim: " + "; ".join(sorted(set(waived)))
        results.append(("A8", PASS, detail))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", default=".auth-contract.yml")
    ap.add_argument("--enforce", action="store_true",
                    help="exit non-zero on FAIL (required-check mode; default is advisory)")
    ap.add_argument("--json", help="also write machine-readable results to this path")
    args = ap.parse_args()

    # Resolve all manifest-relative paths from the manifest's own directory, so
    # the check runs from anywhere. In CI (CWD = caller repo root, manifest at
    # root) this is a no-op — identical to db-tenant-check.
    results = []
    mpath = os.path.abspath(args.manifest)
    try:
        text = open(mpath, encoding="utf-8").read()
        os.chdir(os.path.dirname(mpath))
        args.manifest = os.path.basename(mpath)
        manifest = parse_manifest(text, args.manifest)
    except (OSError, ManifestError) as e:
        manifest = {}
        results.append(("A1", FAIL, f"cannot load manifest: {e}"))
    if manifest:
        check(manifest, results)

    app = manifest.get("app", os.path.basename(os.getcwd()))
    profile = manifest.get("profile", "?")
    mode = "enforce" if args.enforce else "advisory"
    failed = [r for r in results if r[1] == FAIL]

    lines = [f"## auth-contract-check — {app} (profile: {profile}, mode: {mode})", "",
             "| check | status | detail |", "|---|---|---|"]
    for cid, status, detail in results:
        lines.append(f"| {cid} | {ICON[status]} {status} | {detail} |")
    lines.append("")
    verdict = ("**DRIFT** — see contract: Interval-Col/.github/auth-contract.md"
               if failed else "**conformant**")
    if failed and not args.enforce:
        verdict += " _(advisory mode: not blocking — flips to required per RFC 0016 Phase 1)_"
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
            print(f"::{kind}::auth-contract-check {cid}: {detail}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"app": app, "profile": profile, "mode": mode,
                       "conformant": not failed,
                       "results": [{"check": c, "status": s, "detail": d}
                                   for c, s, d in results]}, fh, indent=2)

    sys.exit(1 if (failed and args.enforce) else 0)


if __name__ == "__main__":
    main()
