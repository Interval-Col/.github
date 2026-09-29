#!/usr/bin/env python3
"""Tell the consumers a corpus-registry.yml change affects — then wait for their verdict.

Task 1.6 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`, run by
`corpus-registry-changed.yml` on every push to `main` that touches the registry.

Why: until now only a KB publish dispatched `kb-updated`. A registry change —
widening a grant (lab-qc + `liderazgo`), narrowing one, adding or dropping a KB
edge, moving an edge to another environment — loaded nothing until some
unrelated publish came along, and a narrowed grant left chunks that corpus-verify
V3 rejects. Each consumer reads its grants from the registry on every deploy, so
all a change needs is to trigger that deploy — for the consumers it touched,
and no one else.

What counts as touched: a repo whose LIVE edges (`wait`/`notify`) differ before
and after, compared on (app, kb, audiences, environments, the KB's image). Mode
is `wait` if any of its live edges waits, else `notify`.

Two cases this does NOT fix, said out loud (Fable review of 1.6, 2026-09-29):

- A repo that lost its LAST live edge is told as `notify`, but its rows stay:
  the app redeploys with `KB_CORPUS={}`, and the shared embedder refuses an
  empty corpus before it prunes. They are never SERVED — retrieval grants are
  `{}` too, so nothing matches — but cleaning them means unwiring the app.
- The `kbs:` block (`roots`, `skip`, `default_status`, `liderazgo_areas`, a KB's
  own `audiences`, …) is read when the KB BUILDS its index, in the KB's repo.
  Changing it tells no consumer and rebuilds nothing: `changed_kbs()` names
  them, and the workflow fails until someone republishes those KBs.

The dispatch and the wait are kb_dispatch.publish(): the same correlation id in
the consumer's `run-name`, the same demand for a green `corpus-verify…` job, the
same timeout. The payload says `source: registry`.

    python3 scripts/registry_dispatch.py plan --before old.yml --after corpus-registry.yml
    GH_TOKEN=… python3 scripts/registry_dispatch.py run --before old.yml --sha <sha>

`plan` prints the touched repos, comma-separated (the bot token is minted for
exactly those). An unreadable or invalid `--before` — a first push, a registry
that did not parse — counts as "everything changed": every live consumer is
touched. It errs toward refreshing, never toward silence.

Exit codes: 0 every touched consumer answered green (or none was touched) ·
1 a consumer failed, timed out or refused the dispatch · 2 usage / registry.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kb_dispatch  # noqa: E402
from corpus_lib import RegistryError, load_registry  # noqa: E402

DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "corpus-registry.yml"
LIVE = ("wait", "notify")
SOURCE = "registry"


def live_edges(reg: dict | None) -> dict[str, set[tuple]]:
    """{repo: {(app, kb, audiences, environments, image)}} over the live edges."""
    out: dict[str, set[tuple]] = {}
    if reg is None:
        return out
    for c in reg["consumers"]:
        if c["mode"] not in LIVE:
            continue
        image = reg["kbs"].get(c["kb"], {}).get("image", "")
        out.setdefault(c["repo"], set()).add((
            c["app"], c["kb"], tuple(sorted(c["audiences"])),
            tuple(sorted(c["environments"])), image,
        ))
    return out


KB_FIELDS_AT_BUILD = ("roots", "skip", "recursive", "url", "default_status",
                      "liderazgo_areas", "audiences", "repo")


def changed_kbs(before: dict | None, after: dict) -> list[str]:
    """KBs whose build-time fields changed: their index is stale until they
    republish. (`image` is not here — touched() handles it on the consumer side.)"""
    if before is None:
        return []
    old, new = before["kbs"], after["kbs"]
    return sorted(k for k in new if k in old and any(
        old[k].get(f) != new[k].get(f) for f in KB_FIELDS_AT_BUILD))


def touched(before: dict | None, after: dict) -> list[dict]:
    """The consumers to dispatch, as kb_dispatch.publish() takes them:
    [{"repo", "app", "mode"}], sorted by repo. `before=None` = everything changed."""
    old, new = live_edges(before), live_edges(after)
    if before is None:
        repos = set(new)
    else:
        repos = {r for r in set(old) | set(new) if old.get(r, set()) != new.get(r, set())}
    out = []
    for repo in sorted(repos):
        modes = {c["mode"] for c in after["consumers"]
                 if c["repo"] == repo and c["mode"] in LIVE}
        apps = sorted({e[0] for e in new.get(repo, set())}
                      or {e[0] for e in old.get(repo, set())})
        out.append({"repo": repo, "app": ", ".join(apps),
                    "mode": "wait" if "wait" in modes else "notify"})
    return out


def _load(path: str | None) -> dict | None:
    """The registry at `path`, or None when it cannot be read or does not parse."""
    if not path:
        return None
    try:
        return load_registry(Path(path).read_text(encoding="utf-8"), path)
    except (OSError, RegistryError) as exc:
        print(f"::warning::the previous registry ({path}) is unusable — treating every live "
              f"consumer as touched: {str(exc).splitlines()[0]}", file=sys.stderr)
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("cmd", choices=("plan", "run"))
    ap.add_argument("--before", help="the registry before the push; absent = everything changed")
    ap.add_argument("--after", default=str(DEFAULT_REGISTRY))
    ap.add_argument("--sha", help="the registry commit (run only)")
    ap.add_argument("--owner", default="Interval-Col")
    ap.add_argument("--timeout-minutes", type=float, default=45)
    ap.add_argument("--poll-seconds", type=float, default=30)
    args = ap.parse_args()

    try:
        after = load_registry(Path(args.after).read_text(encoding="utf-8"), args.after)
    except (OSError, RegistryError) as exc:
        print(f"::error::{args.after} is invalid:\n{exc}", file=sys.stderr)
        return 2
    before = _load(args.before)
    consumers = touched(before, after)
    stale_kbs = changed_kbs(before, after)

    if args.cmd == "plan":
        print(",".join(c["repo"] for c in consumers))
        return 0

    if not args.sha:
        print("::error::run needs --sha", file=sys.stderr)
        return 2
    stale = [
        f"{kb}: a build-time field changed (roots, default_status, audiences, …) — its index "
        "is stale until it republishes; merge any change to that KB's repo, or run its "
        "build-site workflow by hand"
        for kb in stale_kbs
    ]
    for line in stale:
        print(f"::error::{line}")
    if not consumers:
        print("::notice::this registry change touches no live consumer — nothing to tell")
        return 1 if stale else 0
    token = os.environ.get("GH_TOKEN", "")
    if not token:
        print("::error::GH_TOKEN is empty — the org bot token was not minted", file=sys.stderr)
        return 2

    outcomes = kb_dispatch.publish(kb_dispatch.Http(token), args.owner, SOURCE, args.sha,
                                   consumers, args.timeout_minutes * 60, args.poll_seconds)
    text = kb_dispatch.report(SOURCE, args.sha, outcomes, title="corpus-registry-changed")
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
    for o in outcomes:
        for w in o.warnings:
            print(f"::warning::{w}")
        if not o.ok:
            print(f"::error::{o.repo} ({o.mode}): {o.detail}")
    return 0 if all(o.ok for o in outcomes) and not stale else 1


if __name__ == "__main__":
    sys.exit(main())
