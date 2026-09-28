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


def chunk(text: str, max_chars: int = TARGET_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """Greedy chunker: largest prefix ≤ max_chars ending at a paragraph break, then a
    sentence, then a space; each chunk starts `overlap` chars before the last end."""
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


def fetch_index(url: str, timeout: float = 30.0) -> dict:
    """GET <url>/kb-index.json from a KB sidecar. Only http(s): the URL comes from
    the registry (`http://<image>`), and nothing else is a KB site."""
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"KB site URL must be http(s): {url!r}")
    target = url.rstrip("/") + "/kb-index.json"
    with urllib.request.urlopen(target, timeout=timeout) as r:  # noqa: S310 — scheme checked above
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
