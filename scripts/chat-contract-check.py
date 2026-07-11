#!/usr/bin/env python3
"""chat-contract-check — Pháros chat contract conformance gate (RFC 0017 Phase 3).

Asserts the *mechanical subset* of the chat contract (chat-contract.md) against an
app's in-app AI chat feature, driven by the app's own `.chat-contract.yml` manifest:

  H1  manifest valid (profile known, referenced paths exist)
  H2  no provider SDK imported in the chat feature (google-genai / openai / …) —
      every provider call goes through pharos-llm-proxy (allowlist = file + reason)
  H3  the proxy client speaks the proxy contract (X-LLM-Proxy-Secret + URL env + a /v1 route)
  H4  no plaintext prompt/reply persistence — chat tables store usage/metadata only (info/warn)
  H5  a per-user rate limit exists and the router gates on it before the upstream call
  H6  graceful degradation — the router maps a proxy outage to 503, not a 500 (info/warn)
  H7  sources cited — a corpus-backed (rag) chat returns a `sources` field (info if rag off)
  H8  FE widget is the registry PharosHelpChat, not a hand-rolled one (info until adopted)

Deliberately stdlib-only (same rule as auth-contract-check.py / db-tenant-check.py):
a future *required* check must not depend on PyPI on the merge path. The manifest
parser therefore accepts a strict, documented subset of YAML and fails loudly on
anything it does not understand — misparse must never pass silently.

Usage:
  chat-contract-check.py --manifest .chat-contract.yml [--enforce] [--json out.json]

Exit code: 0 unless --enforce is set and at least one check FAILs.
Do NOT edit per-repo copies — this script lives in Interval-Col/.github and is
executed from there by the reusable workflow chat-contract-check.yml.
"""

import argparse
import json
import os
import re
import sys

PROFILES = ("chat", "planned")

# H2 — provider SDK imports that must NOT appear in a chat feature. The only
# outbound path to a model is pharos-llm-proxy (chat-contract.md CH1); the proxy
# is the sole holder of provider SDKs/keys. Prose in comments is ignored.
PROVIDER_SDK = [
    (r"from\s+google\s+import\s+genai\b",        "google-genai"),
    (r"import\s+google\.genai\b",                "google-genai"),
    (r"from\s+google\.genai\b",                  "google-genai"),
    (r"import\s+google\.generativeai\b",         "google-generativeai"),
    (r"from\s+google\.generativeai\b",           "google-generativeai"),
    (r"(^|\s)import\s+openai\b",                  "openai"),
    (r"from\s+openai\b",                          "openai"),
    (r"(^|\s)import\s+anthropic\b",               "anthropic"),
    (r"from\s+anthropic\b",                       "anthropic"),
    (r"(^|\s)import\s+vertexai\b",                "vertexai"),
    (r"from\s+vertexai\b",                        "vertexai"),
]

# H3 — the proxy client must speak the proxy contract: the shared-secret header,
# a URL env, and at least one /v1 route (chat or embed).
PROXY_SECRET_HEADER = re.compile(r"X-LLM-Proxy-Secret", re.I)
PROXY_URL_ENV       = re.compile(r"\bLLM_PROXY_URL\b")
PROXY_ROUTE         = re.compile(r"/v1/(chat|embed)\b")

# H4 — column NAMES that would hold a prompt/reply body if persisted. A chat
# usage table should carry username / token counts / timestamps only (CH2).
PLAINTEXT_COL = re.compile(
    r'\b(message|messages|prompt|prompts|reply|replies|content|question|answer|'
    r'body|conversation|transcript|chat_text|user_text)\b\s*=\s*Column\('
    r'[^)]*\b(String|Text|Unicode|VARCHAR|TEXT)\b',
    re.I,
)
# Same idea for a `Mapped[...]` declaration — incl. the SQLAlchemy 2.0 nullable
# idioms `Mapped[str | None]` / `Mapped[Optional[str]]` (body columns are usually
# nullable), so `[^\]]*\bstr\b[^\]]*` matches any bracket contents mentioning str.
PLAINTEXT_COL_MAPPED = re.compile(
    r'\b(message|prompt|reply|content|question|answer|body|conversation|transcript)\b'
    r'\s*:\s*Mapped\[[^\]]*\bstr\b[^\]]*\]',
    re.I,
)

# H5 — a per-user rate-limit surface (module symbols) + the router gating on it.
RATE_LIMIT_SYMBOL = re.compile(r"\b(check_user_quota|PER_USER_[A-Z_]*LIMIT|check_rate_limit)\b")
RATE_LIMIT_IN_ROUTER = re.compile(r"\b(rate_limit|check_user_quota|check_rate_limit)\b")
ROUTER_429 = re.compile(r"\b(429|TOO_MANY_REQUESTS)\b")

# H6 — graceful degradation: the router turns a proxy outage into a 503.
ROUTER_503 = re.compile(r"\b(503|SERVICE_UNAVAILABLE)\b")
ROUTER_UNAVAILABLE = re.compile(r"\bProxy(Unavailable|Error)\b|\bUnavailable\b")

# H7 — a `sources` field on the chat response (corpus citation, CH5).
SOURCES_FIELD = re.compile(r"\bsources\b\s*:")

# H8 — the registry chat widget vs a hand-rolled one (mirrors auth A9). Match real
# USAGE (a <PharosHelpChat> tag, an import, or a direct .vue reference) — not a bare
# mention in a comment/string, which a stray TODO could otherwise satisfy.
FE_PHAROS_WIDGET = re.compile(r"<PharosHelpChat\b|import\s+PharosHelpChat\b|PharosHelpChat\.vue\b")

PASS, FAIL, WARN, INFO, SKIP = "PASS", "FAIL", "WARN", "INFO", "SKIP"
ICON = {PASS: "✅", FAIL: "❌", WARN: "⚠️", INFO: "ℹ️", SKIP: "⏭️"}


class ManifestError(Exception):
    pass


# --------------------------------------------------------------------------
# Strict mini-YAML parser (manifest subset only — see chat-contract.md).
# Shared VERBATIM with auth-contract-check.py / db-tenant-check.py: comments,
# `key: scalar`, `key: [a, b]`, one-level nested maps, block lists of
# scalars / flat maps. A future required check must not pull in PyYAML.
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


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _iter_py(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       ("node_modules", ".git", "__pycache__", ".venv", "venv", ".mypy_cache")]
        for f in filenames:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)


def walk_fe(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       ("node_modules", ".git", ".nuxt", ".output", "dist", "__pycache__")]
        for f in filenames:
            if f.endswith((".vue", ".ts", ".js", ".mjs")):
                yield os.path.join(dirpath, f)


def _code_lines(text):
    """Yield (lineno, code) with the Python line-comment stripped, so prose in a
    `# import openai to ...` comment is never mistaken for a real import."""
    for i, line in enumerate(text.splitlines(), 1):
        yield i, line.split("#", 1)[0]


def _py_code(text):
    """The text with Python line-comments stripped and rejoined, so a comment like
    `# ... 503 SERVICE_UNAVAILABLE ...` is not read as a real 503 path. H5/H6/H7
    scan behaviour, not prose — same discipline H2/H4 already apply per-line."""
    return "\n".join(code for _, code in _code_lines(text or ""))


def _strip_web_comments(text):
    """Drop /* */, <!-- -->, and // line comments (shared with auth-contract-check)
    so an FE doc/TODO mention of PharosHelpChat is not read as real widget usage."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    for line in text.splitlines():
        m = re.search(r"(?<!:)//", line)   # a // that isn't part of a :// URL
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check(manifest, results):
    profile = manifest.get("profile")
    app = manifest.get("app", "?")

    # H1 — manifest validity
    problems = []
    if profile not in PROFILES:
        problems.append(f"unknown profile {profile!r} (expected one of {PROFILES})")
    if profile == "planned":
        if problems:
            results.append(("H1", FAIL, "; ".join(problems)))
        else:
            results.append(("H1", PASS, f"manifest valid for {app}"))
            results.append(("H2", INFO,
                            "planned: no chat feature yet — the full contract applies "
                            "when this app builds its chat (RFC 0017 Phase 5); new apps "
                            "adopt with enforce=true from day one"))
        return

    chat_dirs    = _as_list(manifest.get("chat_dirs"))
    proxy_client = manifest.get("proxy_client")
    router       = manifest.get("router")
    rate_limit   = manifest.get("rate_limit")
    models       = _as_list(manifest.get("models"))
    frontend     = manifest.get("frontend_dir")
    response_src = manifest.get("response_model") or router  # sources field lives here

    if not chat_dirs:
        problems.append("chat_dirs is required for profile: chat")
    for d in chat_dirs:
        if not d or not os.path.isdir(d):
            problems.append(f"chat_dir missing or not a directory: {d!r}")
    for label, p in (("proxy_client", proxy_client), ("router", router)):
        if not p or not os.path.exists(p):
            problems.append(f"{label} missing or not found: {p!r}")
    if frontend and not os.path.isdir(frontend):
        problems.append(f"frontend_dir not found: {frontend!r}")
    for a in (manifest.get("provider_sdk_allow") or []):
        if not isinstance(a, dict) or "file" not in a:
            problems.append(f"provider_sdk_allow entry missing a `file:` key: {a!r}")
    if problems:
        results.append(("H1", FAIL, "; ".join(problems)))
        return
    results.append(("H1", PASS, f"manifest valid for {app} (profile: {profile})"))

    # H2 — no provider SDK in the chat feature
    allow = {a["file"]: a.get("reason", "") for a in (manifest.get("provider_sdk_allow") or [])}
    hits, waived = [], []
    for d in chat_dirs:
        for f in _iter_py(d):
            norm = os.path.relpath(f).replace(os.sep, "/")
            body = _read(f) or ""
            for lineno, code in _code_lines(body):
                for pat, sdk in PROVIDER_SDK:
                    if re.search(pat, code):
                        if norm in allow:
                            waived.append(f"{norm} ({sdk}; reason: {allow[norm]})")
                        else:
                            hits.append(f"{norm}:{lineno}: {sdk}")
                        break
    if hits:
        results.append(("H2", FAIL,
                        "provider SDK imported in the chat feature — all provider calls "
                        "must go through pharos-llm-proxy (or allowlist with a reason): "
                        + "; ".join(sorted(set(hits))[:6])))
    else:
        detail = "no direct provider SDK in the chat feature (proxy is the only path)"
        if waived:
            detail += " — allowlisted: " + "; ".join(sorted(set(waived)))
        results.append(("H2", PASS, detail))

    # H3 — proxy client speaks the proxy contract
    pc = _read(proxy_client) or ""
    have = [bool(PROXY_SECRET_HEADER.search(pc)),
            bool(PROXY_URL_ENV.search(pc)),
            bool(PROXY_ROUTE.search(pc))]
    if all(have):
        results.append(("H3", PASS,
                        f"{os.path.relpath(proxy_client)} calls the proxy with X-LLM-Proxy-Secret "
                        "+ LLM_PROXY_URL + a /v1 route"))
    else:
        missing = [n for n, ok in zip(("X-LLM-Proxy-Secret header", "LLM_PROXY_URL env",
                                       "/v1/{chat,embed} route"), have) if not ok]
        results.append(("H3", FAIL,
                        f"{os.path.relpath(proxy_client)} does not speak the full proxy contract "
                        f"(missing: {', '.join(missing)}) — CH1"))

    # H4 — no plaintext prompt/reply persistence (heuristic → warn)
    persisted = []
    for m in models:
        body = _read(m)
        if body is None:
            continue
        for lineno, code in _code_lines(body):
            if PLAINTEXT_COL.search(code) or PLAINTEXT_COL_MAPPED.search(code):
                persisted.append(f"{os.path.relpath(m)}:{lineno}: {code.strip()[:70]}")
    if not models:
        results.append(("H4", INFO, "no `models` declared — nothing to scan for plaintext persistence"))
    elif persisted:
        results.append(("H4", WARN,
                        "a chat table looks like it persists prompt/reply text — store "
                        "usage/metadata only; content audit is hash-only in the proxy (CH2): "
                        + "; ".join(persisted[:4])))
    else:
        results.append(("H4", PASS,
                        f"chat model(s) carry usage/metadata only — no plaintext prompt/reply column "
                        f"({', '.join(os.path.relpath(m) for m in models)})"))

    # H5 — per-user rate limit, gated in the router before the upstream call.
    # Comment-stripped (like H2/H4): a `# check_user_quota / 429 ...` comment must
    # not satisfy a gate that CH3/CH4/CH5 require to be real code.
    rl = _py_code(_read(rate_limit)) if rate_limit else None
    router_text = _py_code(_read(router))
    has_limit_module = bool(rl and RATE_LIMIT_SYMBOL.search(rl))
    router_gates = bool(RATE_LIMIT_IN_ROUTER.search(router_text) and ROUTER_429.search(router_text))
    if router_gates and has_limit_module:
        results.append(("H5", PASS, "per-user rate limit present and gated in the router (429 before upstream)"))
    elif router_gates:
        results.append(("H5", WARN,
                        "the router gates on a rate limit but no per-user quota symbol found in "
                        f"{rate_limit!r} (check_user_quota / PER_USER_*_LIMIT) — CH3"))
    else:
        results.append(("H5", FAIL,
                        f"no per-user rate-limit gate in {os.path.relpath(router)} "
                        "(expected a rate_limit call + a 429 path before the proxy call) — CH3"))

    # H6 — graceful degradation: proxy outage → 503 (heuristic → warn)
    has_503 = bool(ROUTER_503.search(router_text))
    has_unavail = bool(ROUTER_UNAVAILABLE.search(router_text))
    if has_503 and has_unavail:
        results.append(("H6", PASS, "router maps a proxy outage to 503 (graceful degradation, CH4)"))
    else:
        miss = []
        if not has_503:
            miss.append("no 503/SERVICE_UNAVAILABLE path")
        if not has_unavail:
            miss.append("no proxy-unavailable handler")
        results.append(("H6", WARN,
                        f"could not confirm graceful degradation in {os.path.relpath(router)} "
                        f"({'; '.join(miss)}) — a proxy outage must be a 503, not a 500 (CH4)"))

    # H7 — sources cited for a corpus-backed (rag) chat
    rag = str(manifest.get("rag", "off")).lower() in ("on", "true", "yes")
    if not rag:
        results.append(("H7", INFO, "manifest declares `rag: off` (context-stuffing / no corpus) — "
                        "sources not required (CH5 applies to corpus answers)"))
    else:
        resp = _py_code(_read(response_src))
        if SOURCES_FIELD.search(resp):
            results.append(("H7", PASS, f"corpus chat exposes a `sources` field in {os.path.relpath(response_src)} (CH5)"))
        else:
            results.append(("H7", FAIL,
                            f"`rag: on` but no `sources` field found in {os.path.relpath(response_src)} "
                            "— a corpus answer must cite its sources (CH5)"))

    # H8 — FE widget is the registry PharosHelpChat (mirrors auth A9).
    fe_widget = str(manifest.get("fe_registry_widget", "off")).lower() in ("on", "true", "yes")
    if not fe_widget:
        results.append(("H8", INFO, "FE not on the registry chat widget yet; H8 applies once "
                        "`fe_registry_widget: on` (RFC 0017 Phase 4 — PharosHelpChat)"))
    elif not frontend or not os.path.isdir(frontend):
        results.append(("H8", SKIP, f"no frontend_dir to scan ({frontend!r})"))
    else:
        uses_pharos, handrolled = False, []
        for f in walk_fe(frontend):
            # A hand-rolled *HelpChat.vue (but NOT the registry PharosHelpChat.vue,
            # whose filename also ends in HelpChat.vue).
            if f.endswith("HelpChat.vue") and not f.endswith("PharosHelpChat.vue"):
                handrolled.append(os.path.relpath(f))
            if FE_PHAROS_WIDGET.search(_strip_web_comments(_read(f) or "")):
                uses_pharos = True
        if uses_pharos:
            results.append(("H8", PASS, "FE mounts the registry PharosHelpChat widget"))
        elif handrolled:
            results.append(("H8", FAIL,
                            "`fe_registry_widget: on` but a hand-rolled HelpChat remains and "
                            "PharosHelpChat is not mounted (adopt it via sync-pharos-registry.sh "
                            "--add components/PharosHelpChat.vue): "
                            + "; ".join(sorted(set(handrolled))[:4])))
        else:
            results.append(("H8", WARN,
                            "`fe_registry_widget: on` but no PharosHelpChat usage found under "
                            f"{frontend}"))


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", default=".chat-contract.yml")
    ap.add_argument("--enforce", action="store_true",
                    help="exit non-zero on FAIL (required-check mode; default is advisory)")
    ap.add_argument("--json", help="also write machine-readable results to this path")
    args = ap.parse_args()

    # Resolve all manifest-relative paths from the manifest's own directory, so the
    # check runs from anywhere. In CI (CWD = caller repo root, manifest at root)
    # this is a no-op — identical to auth-contract-check / db-tenant-check.
    results = []
    mpath = os.path.abspath(args.manifest)
    try:
        text = open(mpath, encoding="utf-8").read()
        os.chdir(os.path.dirname(mpath))
        args.manifest = os.path.basename(mpath)
        manifest = parse_manifest(text, args.manifest)
    except (OSError, ManifestError) as e:
        manifest = {}
        results.append(("H1", FAIL, f"cannot load manifest: {e}"))
    if manifest:
        check(manifest, results)
    elif not results:
        # Parsed cleanly but the file is empty / comments-only — an empty dict is
        # falsy, so `check()` would silently skip and report "conformant". A blank
        # or truncated manifest must FAIL H1, not sail the required gate.
        results.append(("H1", FAIL, "manifest is empty (no keys) — declare at least `app` and `profile`"))

    app = manifest.get("app", os.path.basename(os.getcwd()))
    profile = manifest.get("profile", "?")
    mode = "enforce" if args.enforce else "advisory"
    failed = [r for r in results if r[1] == FAIL]

    lines = [f"## chat-contract-check — {app} (profile: {profile}, mode: {mode})", "",
             "| check | status | detail |", "|---|---|---|"]
    for cid, status, detail in results:
        lines.append(f"| {cid} | {ICON[status]} {status} | {detail} |")
    lines.append("")
    verdict = ("**DRIFT** — see contract: Interval-Col/.github/chat-contract.md"
               if failed else "**conformant**")
    if failed and not args.enforce:
        verdict += " _(advisory mode: not blocking — flips to required per RFC 0017 Phase 3)_"
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
            print(f"::{kind}::chat-contract-check {cid}: {detail}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"app": app, "profile": profile, "mode": mode,
                       "conformant": not failed,
                       "results": [{"check": c, "status": s, "detail": d}
                                   for c, s, d in results]}, fh, indent=2)

    sys.exit(1 if (failed and args.enforce) else 0)


if __name__ == "__main__":
    main()
