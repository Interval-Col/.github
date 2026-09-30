"""kb_embedder — the ONE embedder every Pháros Nerea uses to learn its KBs.

Task 3.1 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`. Synced
byte-for-byte into each app's chat dir by `scripts/sync-pharos-registry.sh
--embedder-dir <dir>` (like `prompts/nerea_persona.py`); do NOT edit a copy — edit
this file and re-sync. Each app keeps only a thin wrapper that supplies how to
write ITS table and how to call ITS proxy client.

What it guarantees, the same in every app:

- **What it serves comes from the registry, per deploy.** The deploy passes
  `KB_CORPUS` — `{"<kb>": {"url": "...", "audiences": [...]}}` from
  `corpus_registry.py corpus --app <app>` — so no app keeps its own copy of the
  grants (German, 2026-09-28). No corpus ⇒ nothing is embedded: fail closed.
- **Only `vigente`, only granted audiences.** A draft is text nobody approved. An
  audience the app is not granted is never sent to the proxy, and one this module
  does not know is skipped, never downgraded to `staff`.
- **Emails never leave the app** — the proxy's corpus gate rejects them, rightly.
- **Transient upstream errors are retried** (a 502 from the provider reddened
  Admisiones' first lch-admin-kb refresh on 2026-09-28), with backoff.
- **Every row is attributable:** `kb` and `content_hash` (the index's own hash of
  the article), the contract Interval-Col/.github corpus-verify checks.
- **Prune KB by KB,** and drop rows with no or an unknown `kb` only when every
  source AND every article refreshed — a failed one keeps its old rows.
- **Loud:** `[done]` only when everything refreshed; otherwise `[partial]`, exit 1.

Stdlib only: the apps differ in DB driver (SQLAlchemy, psycopg) and HTTP client.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol

#: D1 — the only audience vocabulary (corpus-registry.yml).
AUDIENCES = frozenset({"publico", "staff", "servicio-al-cliente", "ti", "liderazgo"})
#: Areas that default to leadership when an old index carries no audience at all.
LIDERAZGO_AREAS = frozenset({"comercial", "politicas"})

TARGET_CHARS = 2000
OVERLAP_CHARS = 200

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SIN_CORREO = "[correo no disponible por este canal]"


class Transient(Exception):
    """An embed failure worth retrying: an upstream 5xx, a timeout."""


class Blocked(Exception):
    """An embed failure retrying cannot fix: a gate refusal, a 4xx."""


@dataclass
class Article:
    kb: str
    slug: str
    area: str
    audience: str
    content_hash: str
    body: str


@dataclass
class Selection:
    articles: list[Article] = field(default_factory=list)
    total: int = 0
    skipped_status: int = 0
    skipped_audience: int = 0


class Store(Protocol):
    """How an app writes ITS embeddings table. `metadata()` below builds the row
    metadata so every app stores the same shape."""

    def replace(self, article: Article, chunks: list[str], vectors: list[list[float]]) -> None:
        """Delete this article's rows for this kb (and legacy rows with no kb) and
        insert the fresh chunks, in one transaction."""

    def prune(self, kb: str, keep: list[str]) -> int:
        """Delete rows of `kb` whose source is not in `keep`; return the count."""

    def prune_foreign(self, kbs: list[str]) -> int:
        """Delete rows with no `kb` or a kb not in `kbs`; return the count."""


EmbedFn = Callable[[list[str]], "tuple[list[list[float]], int | None]"]


# ── Pure pieces ───────────────────────────────────────────────────────


def parse_corpus(raw: str) -> dict[str, dict]:
    """`KB_CORPUS` JSON → {kb: {"url", "audiences"}}. Raises ValueError on a bad shape."""
    if not (raw or "").strip():
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("KB_CORPUS must be a JSON object {kb: {url, audiences}}")
    out = {}
    for kb, spec in data.items():
        if not isinstance(spec, dict) or not spec.get("url"):
            raise ValueError(f"KB_CORPUS[{kb!r}] needs a `url`")
        auds = spec.get("audiences") or []
        bad = [a for a in auds if a not in AUDIENCES]
        if bad:
            raise ValueError(f"KB_CORPUS[{kb!r}] has audiences outside D1: {bad}")
        out[kb] = {"url": spec["url"], "audiences": sorted(set(auds))}
    return out


def sin_correos(text: str) -> str:
    return _EMAIL.sub(SIN_CORREO, text)


def content_hash(body_md: str) -> str:
    return "sha256:" + hashlib.sha256(body_md.strip().encode("utf-8")).hexdigest()


def select(index: dict, kb: str, audiences: list[str]) -> Selection:
    """Keep what this app may serve from one index: vigente + a granted audience."""
    grant = set(audiences)
    sel = Selection()
    raw = index.get("articles", []) or []
    sel.total = len(raw)
    for a in raw:
        if (a.get("status") or "vigente").strip().lower() != "vigente":
            sel.skipped_status += 1
            continue
        area = a.get("area", "") or ""
        audience = (a.get("audience") or "").strip().lower()
        if not audience:
            audience = "liderazgo" if area in LIDERAZGO_AREAS else "staff"
        elif audience not in AUDIENCES:
            sel.skipped_audience += 1  # unknown: not ours to serve
            continue
        if audience not in grant:
            sel.skipped_audience += 1
            continue
        original = a.get("body_md") or ""
        if not original.strip():
            continue
        sel.articles.append(
            Article(
                kb=kb,
                slug=a["slug"],
                area=area,
                audience=audience,
                content_hash=a.get("content_hash") or content_hash(original),
                body=sin_correos(original),
            )
        )
    return sel


_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


def sections(text: str) -> list[tuple[list[str], str]]:
    """Split markdown at its headings: `[(breadcrumb, body)]`, body INCLUDING its own
    heading line. `#` lines inside code fences are not headings. A heading whose
    section has no text of its own (a parent immediately followed by a child) yields
    no section — it survives in its children's breadcrumb. Text before the first
    heading is a section with an empty breadcrumb."""
    out: list[tuple[list[str], str]] = []
    stack: list[tuple[int, str]] = []
    crumb: list[str] = []
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        body = "\n".join(buf).strip()
        # A section that is only its heading line carries nothing to embed.
        lines = [ln for ln in body.splitlines() if ln.strip()]
        if lines and not (len(lines) == 1 and _HEADING.match(lines[0])):
            out.append((list(crumb), body))

    for line in text.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
        m = None if in_fence else _HEADING.match(line)
        if m:
            flush()
            buf = []
            level, title = len(m.group(1)), m.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            crumb = [t for _, t in stack]
        buf.append(line)
    flush()
    return out


def _greedy(text: str, max_chars: int, overlap: int) -> list[str]:
    """Largest prefix ≤ max_chars ending at a paragraph break, then a sentence, then
    a space; each chunk starts `overlap` chars before the last end."""
    if len(text) <= max_chars:
        return [text.strip()] if text.strip() else []
    chunks, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            for sep in ("\n\n", ". ", " "):
                hit = text.rfind(sep, start, end)
                if hit > start + max_chars // 2:
                    end = hit + len(sep)
                    break
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def chunk(text: str, max_chars: int = TARGET_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """Chunk markdown SECTION BY SECTION: a chunk never crosses a heading, and every
    chunk of a titled section starts with its breadcrumb («§ Manual › 1.5.2
    Coagulación»), so the model knows which section a passage belongs to.

    Why (measured 2026-09-30, lab-qc in production): one character-window chunk held
    the end of §1.5.1 (EDTA tubes: process «idealmente antes de 1 hora») and the
    start of §1.5.2 (Coagulación: citrate 3.2%). Asked a vague question, Nerea
    fused them into «coagulación con EDTA, antes de 1 hora» — a clinical statement
    that is in no document — and cited the manual for it. Overlap never crosses a
    section either. Text with no headings chunks exactly as before."""
    out: list[str] = []
    for crumb, body in sections(text):
        pieces = _greedy(body, max_chars, overlap)
        if not crumb:
            out.extend(pieces)
            continue
        label = "§ " + " › ".join(crumb)
        out.extend(p if p.startswith(label) else f"{label}\n\n{p}" for p in pieces)
    return out


def metadata(article: Article, chunk_index: int, tenant: str = "") -> dict:
    """The row metadata every app stores. `audience` is what retrieval filters on."""
    meta = {
        "chunk_index": chunk_index,
        "area": article.area,
        "audience": article.audience,
        "kb": article.kb,
        "content_hash": article.content_hash,
    }
    if tenant:
        meta["tenant"] = tenant
    return meta


def embed_with_retry(
    embed: EmbedFn, texts: list[str], attempts: int = 3, sleep: Callable[[float], None] = time.sleep
):
    """Retry `Transient` with 2 s, 4 s … backoff; `Blocked` is raised at once."""
    for n in range(1, attempts + 1):
        try:
            return embed(texts)
        except Transient:
            if n == attempts:
                raise
            sleep(2.0 * n)
    raise AssertionError("unreachable")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """A KB sidecar never redirects. Following one could leave http(s) — the
    default handler accepts ftp:// — so a 3xx is an error (Codex on #252)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect)


def fetch_index(url: str, timeout: float = 30.0) -> dict:
    """GET <url>/kb-index.json from a KB sidecar. Only http(s), and no redirects:
    the URL comes from the registry (`http://<image>`), and nothing else is a KB site."""
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"KB site URL must be http(s): {url!r}")
    with _OPENER.open(url.rstrip("/") + "/kb-index.json", timeout=timeout) as r:
        return json.load(r)


# ── The run ───────────────────────────────────────────────────────────


def run(
    corpus: dict[str, dict],
    store: Store,
    embed: EmbedFn,
    *,
    only_slug: str | None = None,
    dry_run: bool = False,
    log: Callable[[str], None] = print,
    err: Callable[[str], None] = print,
    fetch: Callable[[str], dict] = fetch_index,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Refresh every KB in `corpus`. Returns the process exit code: 0 all refreshed
    (`[done]`), 1 something did not (`[partial]`), 2 configuration."""
    if not corpus:
        err(
            "ERROR: no KB corpus configured (KB_CORPUS is empty) — nothing is embedded. "
            "The deploy passes it from corpus-registry.yml."
        )
        return 2

    selections: dict[str, Selection] = {}
    failed_sources: list[str] = []
    for kb, spec in corpus.items():
        try:
            index = fetch(spec["url"])
        except (urllib.error.URLError, OSError, ValueError) as exc:
            err(f"[fail] {kb}: cannot read {spec['url']}/kb-index.json: {exc}")
            failed_sources.append(kb)
            continue
        sel = select(index, kb, spec["audiences"])
        if sel.total == 0:
            err(f"[fail] {kb}: the index at {spec['url']} has zero articles")
            failed_sources.append(kb)
            continue
        log(
            f"[source] {kb}: {len(sel.articles)} of {sel.total} articles served (skipped "
            f"{sel.skipped_status} not vigente, {sel.skipped_audience} outside the grant "
            f"{spec['audiences']})"
        )
        selections[kb] = sel

    articles = [a for s in selections.values() for a in s.articles]
    if only_slug is not None:
        articles = [a for a in articles if a.slug == only_slug]
        if not articles:
            err(f"--source {only_slug!r} is not served from any KB")
            return 2

    planned = [(a, chunk(a.body)) for a in articles]
    chars = sum(len(c) for _, cs in planned for c in cs)
    log(
        f"[embed_kb] articles={len(articles)} chunks={sum(len(cs) for _, cs in planned)} "
        f"chars={chars} ~tokens={chars // 4}"
    )
    if dry_run:
        for a, cs in planned:
            log(f"  [{a.kb}:{a.slug}] audience={a.audience} chunks={len(cs)}")
        return 1 if failed_sources else 0

    failed: list[str] = []
    tokens = 0
    for a, cs in planned:
        if not cs:
            log(f"[skip] {a.kb}:{a.slug}: no chunks")
            continue
        try:
            vectors, tokens_in = embed_with_retry(embed, cs, sleep=sleep)
        except (Transient, Blocked) as exc:
            err(f"[fail] {a.kb}:{a.slug}: {exc}")
            failed.append(f"{a.kb}:{a.slug}")
            continue
        if len(vectors) != len(cs):
            err(f"[fail] {a.kb}:{a.slug}: {len(vectors)} vectors for {len(cs)} chunks")
            failed.append(f"{a.kb}:{a.slug}")
            continue
        store.replace(a, cs, vectors)
        tokens += tokens_in or 0
        log(f"[ok] {a.kb}:{a.slug}: {len(cs)} chunks (audience={a.audience})")

    if only_slug is None:
        for kb, sel in selections.items():
            n = store.prune(kb, [a.slug for a in sel.articles])
            if n:
                log(f"[prune] {kb}: removed {n} chunk(s) no longer served")
        if not failed_sources and not failed:
            n = store.prune_foreign(list(corpus))
            if n:
                log(f"[prune] removed {n} chunk(s) with no or an unknown kb")

    bad = failed_sources + failed
    if bad:
        err(f"[partial] {len(bad)} source(s)/article(s) NOT refreshed: " + ", ".join(bad))
        return 1
    log(f"[done] total tokens_in={tokens}")
    return 0
