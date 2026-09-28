#!/usr/bin/env python3
"""Verify that a Nerea learned what its KBs say — and nothing it shouldn't serve.

Task 1.4 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`. It runs after
every embed, INSIDE the consumer's backend container (which already holds the DB
connection, the CA and the network path to its KB sidecars), piped in by
`corpus-verify.yml`:

    docker exec -i -e CORPUS_VERIFY_CONFIG=<base64 json> <backend> python - < corpus_verify.py

So it is self-contained: stdlib plus whichever DB driver the app already ships
(SQLAlchemy, psycopg2 or psycopg 3). It reads aggregates only — slugs, hashes and
counts — never a chunk's text, and opens a READ ONLY transaction it rolls back.

For each KB the app is granted (corpus-registry.yml), against that KB's v5 index:

- **V1 floor** — the KB has chunks at all, at least `floor` of them.
- **V2 fresh** — every `vigente` article the app may serve is stored with **its
  current `content_hash`**. An edited article keeps its slug, so a slug check
  passes on stale chunks; the hash doesn't.
- **V3 absent** — anything stored that the app may NOT serve has **zero** chunks:
  an article removed from the KB, no longer `vigente`, or outside the grant. A
  broken prune otherwise keeps obsolete guidance retrievable while V1/V2 stay green.
  Chunks with no `metadata.kb` fail too: they cannot be attributed, so they
  cannot be pruned.
- **V4 answers** — each article's `verificacion` questions go to the app's own
  chat service through its ask module (`python -m <ask_module> --question …
  --audiences …`, which prints `{"reply": …, "sources": [...]}`). The answer must
  cite `debe_citar` and contain `debe_decir` (accent- and case-insensitive). It
  asserts citation and key facts, never wording, and retries once: a flaky check
  that gets muted is worse than none.

The embedder's side of the contract: every row carries `metadata.kb` (the KB id)
and `metadata.content_hash` (the index's hash of the article it came from), and
`source` is the article slug.

Exit codes: 0 verified · 1 a check failed · 2 configuration.
"""

from __future__ import annotations

import base64
import importlib
import json
import os
import subprocess
import sys
import unicodedata
import urllib.request

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"
ICON = {PASS: "✅", FAIL: "❌", SKIP: "⏭️"}

SQL = (
    "SELECT metadata->>'kb' AS kb, source, metadata->>'content_hash' AS content_hash, "
    "count(*) AS chunks FROM {table} GROUP BY 1, 2, 3"
)


# ── Pure checks (unit-tested) ─────────────────────────────────────────


def servable(index: dict, audiences: list[str]) -> dict[str, dict]:
    """{slug: article} the app may serve from this index: vigente and granted."""
    return {
        a["slug"]: a
        for a in index.get("articles", [])
        if a.get("status") == "vigente" and a.get("audience") in audiences
    }


def evaluate_kb(kb: str, index: dict, audiences: list[str], stored: list[tuple],
                floor: int) -> list[tuple[str, str, str]]:
    """V1–V3 for one KB. `stored` = [(source, content_hash, chunks)] for this KB."""
    results = []
    if index.get("version", 0) < 5:
        return [("V2", FAIL, f"{kb}: index is v{index.get('version')} — V2/V3 need v5 "
                             "(content_hash); publish the KB through kb-publish")]
    want = servable(index, audiences)
    total = sum(n for _, _, n in stored)
    # Nothing servable ⇒ the floor is 0: any chunk would be a V3 failure anyway.
    need = max(floor, 1) if want else 0
    if total >= need:
        results.append(("V1", PASS, f"{kb}: {total} chunks (floor {need})"))
    else:
        results.append(("V1", FAIL, f"{kb}: {total} chunks, floor is {need} — "
                                    "the embed did not load this KB"))

    hashes: dict[str, set] = {}
    for source, h, _ in stored:
        hashes.setdefault(source, set()).add(h)
    missing = sorted(s for s in want if s not in hashes)
    stale = sorted(s for s in want if s in hashes and hashes[s] != {want[s]["content_hash"]})
    if missing or stale:
        parts = []
        if missing:
            parts.append(f"missing {len(missing)}: {', '.join(missing[:5])}")
        if stale:
            parts.append(f"stale {len(stale)}: {', '.join(stale[:5])}")
        results.append(("V2", FAIL, f"{kb}: " + "; ".join(parts)))
    else:
        results.append(("V2", PASS, f"{kb}: {len(want)} servable articles, all at their "
                                    "current content_hash"))

    extra = sorted(s for s in hashes if s not in want)
    if extra:
        results.append(("V3", FAIL, f"{kb}: {len(extra)} article(s) stored that this app may "
                                    f"not serve (removed, not vigente, or outside "
                                    f"{audiences}): {', '.join(extra[:5])}"))
    else:
        results.append(("V3", PASS, f"{kb}: nothing stored outside the servable set"))
    return results


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def cites(sources: list, slug: str) -> bool:
    for s in sources or []:
        s = str(s)
        if s == slug or s.endswith(":" + slug):
            return True
    return False


def check_answer(item: dict, reply: str, sources: list) -> tuple[bool, str]:
    problems = []
    if not cites(sources, item["debe_citar"]):
        problems.append(f"did not cite `{item['debe_citar']}` (cited: {sources or 'nothing'})")
    if item.get("debe_decir") and _norm(item["debe_decir"]) not in _norm(reply):
        problems.append(f"did not say «{item['debe_decir']}»")
    return (not problems), "; ".join(problems) or "cited and said it"


# ── Container side ────────────────────────────────────────────────────


def _connect(db: str):
    """A DB-API-ish runner for `db`: `env:VAR`, or `attr:module:dotted.path` that
    resolves to a URL string, an Engine, or a callable returning either."""
    if db.startswith("env:"):
        target = os.environ[db[4:]]
    elif db.startswith("attr:"):
        _, mod, path = db.split(":", 2)
        target = importlib.import_module(mod)
        for part in path.split("."):
            target = getattr(target, part)
        if callable(target):
            target = target()
    else:
        raise ValueError(f"db must be `env:VAR` or `attr:module:path`, got {db!r}")

    if hasattr(target, "connect") and not isinstance(target, str):  # SQLAlchemy Engine
        return _connect_engine(target)

    url = str(target)
    try:
        import psycopg  # psycopg 3

        def run(sql):
            with psycopg.connect(url) as c:
                c.execute("SET TRANSACTION READ ONLY")
                rows = [tuple(r) for r in c.execute(sql).fetchall()]
                c.rollback()
            return rows
        return run
    except ImportError:
        from sqlalchemy import create_engine

        return _connect_engine(create_engine(url))


def _connect_engine(engine):
    from sqlalchemy import text

    def run(sql):
        with engine.connect() as c:
            c.execute(text("SET TRANSACTION READ ONLY"))
            rows = [tuple(r) for r in c.execute(text(sql)).all()]
            c.rollback()
        return rows
    return run


def _fetch_index(url: str) -> dict:
    with urllib.request.urlopen(url.rstrip("/") + "/kb-index.json", timeout=30) as r:
        return json.load(r)


def _ask(module: str, question: str, audiences: list[str]) -> tuple[str, list]:
    p = subprocess.run(
        [sys.executable, "-m", module, "--question", question, "--audiences", ",".join(audiences)],
        capture_output=True, text=True, timeout=120, check=False,
    )
    line = next((ln for ln in reversed(p.stdout.splitlines()) if ln.startswith("{")), None)
    if p.returncode != 0 or line is None:
        raise RuntimeError(f"ask module exited {p.returncode}: {(p.stderr or '').strip()[:160]}")
    out = json.loads(line)
    return out.get("reply", ""), out.get("sources", [])


def verify(cfg: dict) -> list[tuple[str, str, str]]:
    results: list[tuple[str, str, str]] = []
    run = _connect(cfg["db"])
    rows = run(SQL.format(table=cfg["table"]))
    by_kb: dict[str | None, list] = {}
    for kb, source, h, n in rows:
        by_kb.setdefault(kb, []).append((source, h, int(n)))

    if None in by_kb:
        n = sum(x[2] for x in by_kb.pop(None))
        results.append(("V3", FAIL, f"{n} chunk(s) carry no `metadata.kb` — they cannot be "
                                    "attributed to a KB, so no prune can reach them"))
    granted = cfg["grants"]
    for kb in sorted(set(by_kb) - set(granted)):
        n = sum(x[2] for x in by_kb[kb])
        results.append(("V3", FAIL, f"{n} chunk(s) from `{kb}`, which this app is not "
                                    "granted in corpus-registry.yml"))

    union = sorted({a for auds in granted.values() for a in auds})
    questions = []
    for kb, audiences in sorted(granted.items()):
        url = cfg["sources"].get(kb)
        if not url:
            results.append(("V1", FAIL, f"{kb}: no source URL configured for a granted KB"))
            continue
        try:
            index = _fetch_index(url)
        except Exception as exc:  # noqa: BLE001 — report, don't crash
            results.append(("V1", FAIL, f"{kb}: cannot read {url}/kb-index.json ({exc})"))
            continue
        results += evaluate_kb(kb, index, audiences, by_kb.get(kb, []), cfg.get("floor", 1))
        for art in servable(index, audiences).values():
            questions += [(kb, art["slug"], q) for q in art.get("verificacion", [])]

    if not questions:
        results.append(("V4", SKIP, "no `verificacion` questions in the servable articles"))
    elif not cfg.get("ask_module"):
        results.append(("V4", FAIL, f"{len(questions)} question(s) to ask but no `ask_module` "
                                    "— the app must expose one (chat-contract H11)"))
    else:
        for kb, slug, q in questions:
            ok, detail = False, ""
            for _ in range(1 + int(cfg.get("retries", 1))):
                try:
                    reply, sources = _ask(cfg["ask_module"], q["pregunta"], union)
                    ok, detail = check_answer(q, reply, sources)
                except Exception as exc:  # noqa: BLE001
                    ok, detail = False, str(exc)
                if ok:
                    break
            results.append(("V4", PASS if ok else FAIL, f"«{q['pregunta']}» ({kb}:{slug}): "
                                                         f"{detail}"))
    return results


def report(app: str, results: list[tuple[str, str, str]]) -> str:
    lines = [f"## corpus-verify · {app}", "", "| check | status | detail |", "|---|---|---|"]
    lines += [f"| {c} | {ICON[s]} {s} | {d} |" for c, s, d in results]
    return "\n".join(lines)


def main() -> int:
    raw = os.environ.get("CORPUS_VERIFY_CONFIG", "")
    if not raw:
        print("CORPUS_VERIFY_CONFIG is empty", file=sys.stderr)
        return 2
    cfg = json.loads(base64.b64decode(raw))
    try:
        results = verify(cfg)
    except Exception as exc:  # noqa: BLE001 — a crash is a failed verification, said plainly
        results = [("V0", FAIL, f"{type(exc).__name__}: {str(exc).splitlines()[0][:200]}")]
    failed = [r for r in results if r[1] == FAIL]
    print(report(cfg.get("app", "?"), results))
    print("CORPUS-VERIFY " + json.dumps({"app": cfg.get("app"), "ok": not failed,
                                         "failed": len(failed), "checks": len(results)}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
