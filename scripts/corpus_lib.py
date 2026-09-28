"""Shared by the corpus scripts: the registry loader and a strict mini-YAML parser.

The corpus chain (RFC 0017 · plan `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`)
is three scripts that must agree on one file, `corpus-registry.yml`:

- `kb_index.py` builds a KB's v5 index with the KB's layout and audiences;
- `corpus_registry.py` answers "who consumes this KB, and how" for `kb-publish.yml`;
- `corpus_verify.py` checks a consumer's corpus against the index and its grants.

Stdlib only, like every check in this repo: no PyPI on the merge path.

⚠️ **The parser is the one in `chat-contract-check.py`, plus two things**, so it is
NOT shared verbatim with the contract checks:
  1. inline lists (`key: [a, b]`) are accepted inside list items and nested maps,
     not only at the top level — a registry row needs `audiences: [staff, ti]`;
  2. keys may contain `-` (`vigente-desde`, `debe-citar`), because KB frontmatter
     already uses them.
Everything else — comments, one level of nesting, block lists of flat maps — is
identical, and anything deeper is a parse error rather than a guess.
"""

from __future__ import annotations

import re

#: D1 (German, 2026-09-27): the ONE audience vocabulary for every KB and every
#: Nerea. `corpus-registry.yml` repeats it and the loader asserts they match, so
#: neither can drift alone.
AUDIENCES = ("publico", "staff", "servicio-al-cliente", "ti", "liderazgo")

#: How a publisher treats a consumer (see corpus-registry.yml § modes).
MODES = ("wait", "notify", "planned")

_KEY = r"[A-Za-z0-9_][A-Za-z0-9_-]*"


class ParseError(Exception):
    pass


class RegistryError(Exception):
    pass


# ── Mini-YAML ─────────────────────────────────────────────────────────


def _scalar(tok: str):
    tok = tok.strip()
    if tok in ("null", "~", ""):
        return None
    if tok in ("true", "True"):
        return True
    if tok in ("false", "False"):
        return False
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    if tok.startswith("[") and tok.endswith("]"):
        inner = tok[1:-1].strip()
        return [_scalar(t) for t in inner.split(",")] if inner else []
    return tok


def _strip_comment(line: str) -> str:
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


def parse_yaml(text: str, path: str = "<yaml>") -> dict:
    lines = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw)
        if line.strip():
            lines.append((n, line))

    root: dict = {}
    i = 0
    while i < len(lines):
        n, line = lines[i]
        if line.startswith(" "):
            raise ParseError(f"{path}:{n}: unexpected indentation")
        m = re.match(rf"^({_KEY}):(.*)$", line)
        if not m:
            raise ParseError(f"{path}:{n}: expected `key: value`")
        key, rest = m.group(1), m.group(2).strip()
        i += 1
        if rest:
            root[key] = _scalar(rest)
            continue
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


def _parse_flat_map(block, path) -> dict:
    out = {}
    for n, line in block:
        m = re.match(rf"^  ({_KEY}):(.*)$", line)
        if not m:
            raise ParseError(f"{path}:{n}: expected `  key: value` in nested map")
        out[m.group(1)] = _scalar(m.group(2))
    return out


def _parse_block_list(block, path) -> list:
    items: list = []
    current = None
    for n, line in block:
        stripped = line.strip()
        if stripped.startswith("- "):
            body = stripped[2:]
            m = re.match(rf"^({_KEY}):(.*)$", body)
            if m:
                current = {m.group(1): _scalar(m.group(2))}
                items.append(current)
            else:
                current = None
                items.append(_scalar(body))
        elif current is not None:
            m = re.match(rf"^({_KEY}):(.*)$", stripped)
            if not m:
                raise ParseError(f"{path}:{n}: expected `key: value` in list item")
            current[m.group(1)] = _scalar(m.group(2))
        else:
            raise ParseError(f"{path}:{n}: continuation line outside a map item")
    return items


# ── Registry ──────────────────────────────────────────────────────────


def _as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_registry(text: str, path: str = "corpus-registry.yml") -> dict:
    """Parse and validate the registry. Raises RegistryError listing EVERY problem."""
    try:
        reg = parse_yaml(text, path)
    except ParseError as exc:
        raise RegistryError(str(exc)) from exc

    problems: list[str] = []
    if reg.get("version") not in (1, "1"):
        problems.append("`version: 1` is required")

    vocab = _as_list(reg.get("audiences"))
    if tuple(vocab) != AUDIENCES:
        problems.append(
            f"`audiences` must be exactly {list(AUDIENCES)} (D1) — found {vocab}. Changing "
            "the vocabulary is a decision, and it changes corpus_lib.AUDIENCES too."
        )

    kbs = {}
    for kb in _as_list(reg.get("kbs")):
        if not isinstance(kb, dict) or not kb.get("id"):
            problems.append(f"kb entry without `id`: {kb!r}")
            continue
        kid = kb["id"]
        if kid in kbs:
            problems.append(f"kb `{kid}` declared twice")
        for req in ("repo", "image", "roots", "url", "default_status"):
            if not kb.get(req):
                problems.append(f"kb `{kid}`: `{req}` is required")
        if kb.get("url") not in (None, "site", "github"):
            problems.append(f"kb `{kid}`: `url` must be `site` or `github`")
        for field in ("roots", "skip", "liderazgo_areas", "audiences"):
            kb[field] = _as_list(kb.get(field))
        bad = [a for a in kb["audiences"] if a not in AUDIENCES]
        if bad:
            problems.append(f"kb `{kid}`: audiences outside D1: {bad}")
        if not kb["audiences"]:
            problems.append(f"kb `{kid}`: `audiences` (what it may declare) is required")
        kbs[kid] = kb

    consumers = []
    seen = set()
    for c in _as_list(reg.get("consumers")):
        if not isinstance(c, dict):
            problems.append(f"consumer entry is not a map: {c!r}")
            continue
        label = f"consumer {c.get('kb')}→{c.get('app')}"
        for req in ("kb", "app", "repo", "mode", "audiences", "environments"):
            if not c.get(req):
                problems.append(f"{label}: `{req}` is required")
        if (c.get("kb"), c.get("app")) in seen:
            problems.append(f"{label}: declared twice")
        seen.add((c.get("kb"), c.get("app")))
        if c.get("kb") and c["kb"] not in kbs:
            problems.append(f"{label}: unknown kb `{c['kb']}`")
        if c.get("mode") and c["mode"] not in MODES:
            problems.append(f"{label}: mode must be one of {list(MODES)}")
        c["audiences"] = _as_list(c.get("audiences"))
        c["environments"] = _as_list(c.get("environments"))
        bad = [a for a in c["audiences"] if a not in AUDIENCES]
        if bad:
            problems.append(f"{label}: audiences outside D1: {bad}")
        # 🔴 The grant is what a Nerea SERVES. Serving `publico` next to an internal
        # tier on the same assistant would mix internet and staff answers, so a
        # public consumer is granted `publico` alone.
        if "publico" in c["audiences"] and len(c["audiences"]) > 1:
            problems.append(f"{label}: `publico` cannot share a grant with internal tiers")
        consumers.append(c)

    if problems:
        raise RegistryError("\n".join(f"- {p}" for p in problems))
    reg["kbs"] = kbs
    reg["consumers"] = consumers
    return reg


def consumers_of(reg: dict, kb: str, modes: tuple[str, ...] = MODES) -> list[dict]:
    return [c for c in reg["consumers"] if c["kb"] == kb and c["mode"] in modes]
