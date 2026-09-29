#!/usr/bin/env python3
"""Build a KB's kb-index.json, v5 — the one index schema every KB publishes.

Task 1.2 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`. It replaces
the two builders that grew apart: `biuman-kb/site/build_docs.py` (v2) and
`lch-kb/site/build_index.py` (v4). One index is read by two kinds of consumer:
every Nerea's embedder and every «Conocimiento» view. One source, two readers.

What v5 adds, and why each piece exists:

- **`audience` is validated against D1, and an unknown value FAILS the build.**
  v2 and v4 coerced it to `liderazgo`, the most closed tier. That fails safe for
  a typo, but it fails *silent*: `servicio-al-cliente` and `ti` did not exist, so
  the customer-service and IT guides became `liderazgo` and no Nerea could serve
  them. A build that stops and says so is the fix.
- **`publico` is never inferred, and needs `vigente`** (the lch-kb rule): a draft
  marked `publico` drops to `staff`, with a warning, until Quality approves it.
- **`content_hash`** per article (sha256 of `body_md`). `corpus_verify.py`
  compares it with the hash the embedder stored: an edited article keeps its
  slug, so a slug check passes on stale chunks.
- **`verificacion`**: optional questions with a known answer, from frontmatter:

      verificacion:
        - pregunta: "¿Cuánto dura el bloqueo del SSO?"
          debe-decir: "5 minutos"
        - pregunta: "¿Cómo entra un médico al portal?"
          debe-citar: servicio-al-cliente/portal-de-resultados/ingreso-pacientes-y-medicos

  `debe-citar` defaults to the article itself.

Layout and allowed audiences come from `corpus-registry.yml`, not from here, so
a KB never carries its own copy of the rules.

Usage:
    python3 scripts/kb_index.py --kb biuman-kb --root ../biuman-kb --out kb-index.json
    python3 scripts/kb_index.py --kb biuman-kb --root ../biuman-kb --compare old-index.json

Exit codes: 0 built · 1 the KB is invalid (every problem is listed) · 2 usage.
Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_lib import AUDIENCES, ParseError, RegistryError, load_registry, parse_yaml  # noqa: E402

VERSION = 5
STATUS_PUBLICABLE = "vigente"
DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "corpus-registry.yml"

_FM = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)$", re.S)
_LINK = re.compile(r"(\[[^\]]*\]\()([^)\s#]+)(#[^)]*)?(\))")
_HEADING = re.compile(r"^#{1,3} +(.+)$", re.M)
_MD_STRIP = re.compile(r"[#>*`_\[\]()|]|!\[|--+")


class KbError(Exception):
    pass


# ── Parsing ───────────────────────────────────────────────────────────


def split_frontmatter(text: str, path: str) -> tuple[dict, str]:
    """(meta, body). Flat `key: value` plus block lists (`verificacion:`).
    A leading BOM (Notepad's UTF-8) is dropped first: with it `^---` did not match,
    the frontmatter was silently ignored, and a draft fell back to the KB's default
    status — `vigente` for biuman-kb, which non-technical staff edit. (CRLF is
    already folded by `read_text`; the replace covers callers passing raw text.)"""
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    m = _FM.match(text)
    if not m:
        return {}, text
    try:
        meta = parse_yaml(m.group(1), path)
    except ParseError as exc:
        raise KbError(f"frontmatter: {exc}") from exc
    return meta, m.group(2)


def _text(v) -> str:
    return "" if v is None else str(v).strip()


def plain(body: str, words: int) -> str:
    txt = _MD_STRIP.sub(" ", body)
    return " ".join(re.sub(r"\s+", " ", txt).split()[:words])


def first_h1(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def content_hash(body_md: str) -> str:
    return "sha256:" + hashlib.sha256(body_md.encode("utf-8")).hexdigest()


def rewrite_links(body: str, src_rel: str, indexed: set[str], blob: str) -> str:
    """Links to another indexed article stay; any other relative link becomes an
    absolute GitHub URL, so it works wherever the index is rendered."""

    def repl(m: re.Match[str]) -> str:
        target = m.group(2)
        if re.match(r"^[a-z]+://|^mailto:", target):
            return m.group(0)
        resolved = os.path.normpath(os.path.join(os.path.dirname(src_rel), target))
        if resolved in indexed:
            return m.group(0)
        return f"{m.group(1)}{blob}/{resolved}{m.group(3) or ''}{m.group(4)}"

    return _LINK.sub(repl, body)


# ── Audience ──────────────────────────────────────────────────────────


def audience_of(meta: dict, area: str, kb: dict, status: str, slug: str, warn) -> str:
    declared = _text(meta.get("audience")).lower()
    if declared:
        if declared not in AUDIENCES:
            raise KbError(f"audience «{declared}» is not in D1 {list(AUDIENCES)}")
        if declared not in kb["audiences"]:
            raise KbError(
                f"audience «{declared}» is not allowed in {kb['id']} "
                f"(corpus-registry.yml allows {kb['audiences']})"
            )
        if declared == "publico" and status != STATUS_PUBLICABLE:
            warn(f"{slug}: «audience: publico» on a «{status}» article — served as `staff` "
                 f"until it is {STATUS_PUBLICABLE}.")
            return "staff"
        return declared
    return "liderazgo" if area in kb["liderazgo_areas"] else "staff"


def verificacion_of(meta: dict, slug: str) -> list[dict]:
    raw = meta.get("verificacion")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise KbError("`verificacion` must be a list of `- pregunta: …` items")
    out = []
    for i, item in enumerate(raw, 1):
        if not isinstance(item, dict) or not _text(item.get("pregunta")):
            raise KbError(f"verificacion #{i}: `pregunta` is required")
        unknown = set(item) - {"pregunta", "debe-citar", "debe-decir"}
        if unknown:
            raise KbError(f"verificacion #{i}: unknown key(s) {sorted(unknown)}")
        out.append({
            "pregunta": _text(item["pregunta"]),
            "debe_citar": _text(item.get("debe-citar")) or slug,
            "debe_decir": _text(item.get("debe-decir")),
        })
    return out


# ── Build ─────────────────────────────────────────────────────────────


def discover(root: Path, kb: dict) -> list[str]:
    """Root-relative paths (with `.md`) of every article, sorted by name."""
    skip = set(kb["skip"])
    found = []
    for area in kb["roots"]:
        base = root / area
        if not base.is_dir():
            raise KbError(f"root `{area}/` does not exist in {root}")
        pattern = "**/*.md" if kb.get("recursive") else "*.md"
        for f in base.glob(pattern):
            rel = f.relative_to(root).as_posix()
            if f.name == "README.md" or f.stem in skip or rel[:-3] in skip:
                continue
            found.append(rel)
    # By-name sort: deterministic across OSes.
    return sorted(found)


def build(root: Path, kb: dict, source_commit: str = "local", warn=print) -> dict:
    blob = f"https://github.com/Interval-Col/{kb['repo']}/blob/main"
    rels = discover(root, kb)
    indexed = set(rels)
    problems: list[str] = []
    articles = []
    for rel in rels:
        slug = rel[:-3]
        try:
            meta, body = split_frontmatter((root / rel).read_text(encoding="utf-8"), rel)
            # The declared area wins (lch-kb files live in `fase-0/` but belong to real
            # areas); the folder is the fallback, which is biuman-kb's layout.
            area = _text(meta.get("area")) or rel.split("/", 1)[0]
            status = (_text(meta.get("status")) or kb["default_status"]).lower()
            body_md = rewrite_links(body, rel, indexed, blob).strip()
            article = {
                "slug": slug,
                "area": area,
                "title": _text(meta.get("title")) or first_h1(body) or Path(rel).stem,
                "status": status,
                "audience": audience_of(meta, area, kb, status, slug, warn),
                "content_hash": content_hash(body_md),
                "created": _text(meta.get("created")),
                "updated": _text(meta.get("updated")),
                "owner": _text(meta.get("owner")) or _text(meta.get("elaborado_por")),
                "fuente": _text(meta.get("fuente")),
                "url": f"/{slug}/" if kb["url"] == "site" else f"{blob}/{rel}",
                "excerpt": plain(body_md, 40),
                "text": plain(body_md, 5000),
                "body_md": body_md,
                "headings": _HEADING.findall(body_md),
                "verificacion": verificacion_of(meta, slug),
            }
            # Controlled-document fields (lch-kb, ISO 15189): kept when present.
            for key in ("tipo", "codigo", "version"):
                if _text(meta.get(key)):
                    article[key] = _text(meta[key])
            control = {
                k: _text(meta.get(k))
                for k in ("elaborado_por", "revisado_por", "conformidad_calidad",
                          "aprobado_por", "ciclo_revision", "proxima_revision")
                if _text(meta.get(k))
            }
            if control:
                article["control"] = control
            articles.append(article)
        except KbError as exc:
            problems.append(f"{rel}: {exc}")
    if problems:
        raise KbError("\n".join(f"- {p}" for p in problems))
    if not articles:
        raise KbError(f"{kb['id']}: zero articles under {kb['roots']} — an empty index is a "
                      "failed build, not a quiet one")
    return {
        "version": VERSION,
        "kb": kb["id"],
        "source_commit": source_commit,
        "audiences": list(AUDIENCES),
        "article_count": len(articles),
        "articles": articles,
    }


# ── Parity check (Done-when of Phase 1) ───────────────────────────────

#: What "identical in content" means across versions. Derived fields (excerpt,
#: text, headings) and new ones (content_hash, verificacion) are left out.
CONTENT_FIELDS = ("area", "title", "status", "audience", "body_md", "url")


def compare(new: dict, old: dict) -> list[str]:
    a = {x["slug"]: x for x in new["articles"]}
    b = {x["slug"]: x for x in old["articles"]}
    diffs = [f"only in v{new['version']}: {s}" for s in sorted(a.keys() - b.keys())]
    diffs += [f"only in v{old.get('version')}: {s}" for s in sorted(b.keys() - a.keys())]
    for slug in sorted(a.keys() & b.keys()):
        for f in CONTENT_FIELDS:
            # v5 strips `body_md`; v2 kept the leading/trailing newlines. Content is
            # the text, not its padding.
            x, y = a[slug].get(f), b[slug].get(f)
            if f == "body_md" and isinstance(x, str) and isinstance(y, str):
                x, y = x.strip(), y.strip()
            if x != y:
                diffs.append(f"{slug}: `{f}` differs")
    return diffs


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--kb", required=True, help="the KB id in corpus-registry.yml")
    ap.add_argument("--root", required=True, help="checkout of the KB repo")
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    ap.add_argument("--out", help="write the index here")
    ap.add_argument("--compare", help="an older kb-index.json to diff content against")
    args = ap.parse_args()

    try:
        reg = load_registry(Path(args.registry).read_text(encoding="utf-8"), args.registry)
    except (OSError, RegistryError) as exc:
        print(f"::error::corpus-registry.yml is invalid:\n{exc}", file=sys.stderr)
        return 2
    kb = reg["kbs"].get(args.kb)
    if kb is None:
        print(f"::error::kb `{args.kb}` is not in {args.registry}", file=sys.stderr)
        return 2

    try:
        index = build(Path(args.root), kb, os.environ.get("GIT_SHA", "local"),
                      warn=lambda m: print(f"::warning::{m}"))
    except KbError as exc:
        print(f"::error::{args.kb}: the index cannot be built:\n{exc}", file=sys.stderr)
        return 1

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
    by_aud: dict[str, int] = {}
    for a in index["articles"]:
        key = f"{a['audience']}/{a['status']}"
        by_aud[key] = by_aud.get(key, 0) + 1
    print(f"{args.kb}: v{VERSION}, {index['article_count']} articles — "
          + ", ".join(f"{k}: {n}" for k, n in sorted(by_aud.items())))

    if args.compare:
        old = json.loads(Path(args.compare).read_text(encoding="utf-8"))
        diffs = compare(index, old)
        if diffs:
            print(f"content differs from v{old.get('version')}:")
            print("\n".join(f"  - {d}" for d in diffs))
            return 1
        print(f"content identical to v{old.get('version')} "
              f"({len(old['articles'])} articles, fields: {', '.join(CONTENT_FIELDS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
