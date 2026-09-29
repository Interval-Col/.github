#!/usr/bin/env python3
"""Validate `corpus-registry.yml` and answer "who consumes this KB, and how".

Task 1.1 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`. The registry
replaces every hardcoded dispatch list in the KB repos; this is how a workflow
reads it without PyYAML.

    python3 scripts/corpus_registry.py validate
    python3 scripts/corpus_registry.py consumers --kb biuman-kb             # JSON rows
    python3 scripts/corpus_registry.py consumers --kb biuman-kb --mode wait --field repo
    python3 scripts/corpus_registry.py grants --app admission-patient       # audiences per KB
    python3 scripts/corpus_registry.py corpus --app admission-patient       # the embed's KB_CORPUS
    python3 scripts/corpus_registry.py table                                # Markdown, for humans

Exit codes: 0 ok · 1 the registry is invalid (every problem listed) · 2 usage.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_lib import MODES, RegistryError, consumers_of, load_registry  # noqa: E402

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "corpus-registry.yml"


def live_edges(reg: dict, app: str, environment: str | None = None) -> list[dict]:
    """`app`'s non-planned edges; with `environment`, only the ones the registry
    lists for it. Without the filter a prod deploy inherits dev-only grants and the
    `environments` column is decoration (Fable review, 2026-09-28)."""
    return [c for c in reg["consumers"]
            if c["app"] == app and c["mode"] != "planned"
            and (environment is None or environment in c["environments"])]


def corpus_for(reg: dict, app: str, environment: str | None = None) -> dict:
    """What the shared embedder (registry/corpus/kb_embedder.py) loads for `app`:
    {kb: {"url", "audiences"}} for its LIVE edges only — a `planned` edge is not
    embedded, so corpus-verify never sees chunks the registry does not grant yet.
    The URL is the KB's sidecar on the app's own network: `http://<image>`, the
    compose service name every consumer already uses (biuman-kb-site, …)."""
    return {
        c["kb"]: {"url": f"http://{reg['kbs'][c['kb']]['image']}",
                  "audiences": sorted(c["audiences"])}
        for c in live_edges(reg, app, environment)
    }


def table(reg: dict) -> str:
    rows = ["| KB | App | Repo | Serves | Environments | Mode |", "|---|---|---|---|---|---|"]
    for c in reg["consumers"]:
        rows.append(
            f"| `{c['kb']}` | {c['app']} | `{c['repo']}` | {', '.join(c['audiences'])} "
            f"| {', '.join(c['environments'])} | {c['mode']} |"
        )
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("table")
    c = sub.add_parser("consumers")
    c.add_argument("--kb", required=True)
    c.add_argument("--mode", action="append", choices=MODES,
                   help="repeatable; default: wait + notify (the ones a publisher dispatches)")
    c.add_argument("--field", help="print one field per line instead of JSON")
    g = sub.add_parser("grants")
    g.add_argument("--app", required=True)
    g.add_argument("--environment", help="only the edges the registry lists for it")
    k = sub.add_parser("corpus", help="KB_CORPUS JSON for the shared embedder (live edges only)")
    k.add_argument("--app", required=True)
    k.add_argument("--environment", help="only the edges the registry lists for it; "
                   "an environment with none gets `{}` — Nerea serves nothing")
    args = ap.parse_args()

    try:
        reg = load_registry(Path(args.registry).read_text(encoding="utf-8"), args.registry)
    except OSError as exc:
        print(f"::error::cannot read {args.registry}: {exc}", file=sys.stderr)
        return 2
    except RegistryError as exc:
        print(f"::error::{args.registry} is invalid:\n{exc}", file=sys.stderr)
        return 1

    if args.cmd == "validate":
        n = {m: sum(1 for x in reg["consumers"] if x["mode"] == m) for m in MODES}
        print(f"{args.registry}: valid — {len(reg['kbs'])} KBs, {len(reg['consumers'])} "
              f"consumers ({', '.join(f'{k}: {v}' for k, v in n.items())})")
    elif args.cmd == "table":
        print(table(reg))
    elif args.cmd == "consumers":
        if args.kb not in reg["kbs"]:
            print(f"::error::kb `{args.kb}` is not in the registry", file=sys.stderr)
            return 2
        rows = consumers_of(reg, args.kb, tuple(args.mode or ("wait", "notify")))
        if args.field:
            print("\n".join(str(r.get(args.field, "")) for r in rows))
        else:
            print(json.dumps(rows, ensure_ascii=False))
    elif args.cmd == "corpus":
        print(json.dumps(corpus_for(reg, args.app, args.environment), ensure_ascii=False,
                         sort_keys=True))
    elif args.cmd == "grants":
        rows = [x for x in reg["consumers"] if x["app"] == args.app
                and (args.environment is None or args.environment in x["environments"])]
        if not rows:
            print(f"::error::app `{args.app}` consumes no KB in the registry", file=sys.stderr)
            return 2
        print(json.dumps({x["kb"]: {"audiences": x["audiences"], "mode": x["mode"]}
                          for x in rows}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
