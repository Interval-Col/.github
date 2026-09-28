#!/usr/bin/env python3
"""Does this change carry code, or only documentation?

Read by the reusable `changes.yml`: every repo's heavy jobs (tests, builds,
deploys) run only when a change carries code. A PR that only edits a plan must
not spend ten minutes building a frontend and then deploy it to dev.

Documentation, org-wide — ONE list, so no repo drifts from another:
  - any `*.md` file, anywhere (README, CLAUDE.md, plans, guides, ADRs);
  - anything under `docs/` or `plans/` at any depth;
  - `LICENSE`.

Measured before choosing it (2026-09-28): no code in admission-patient,
pharos-llm-proxy or pharos-lis reads a `.md` file at runtime. A repo where some
`.md` IS an input to code passes `--code-regex` to claim those paths back.

    git diff --name-only A B | python3 changes_classify.py [--code-regex RE]

Prints `code=true|false` and `files=<n>` (GITHUB_OUTPUT format).
🔑 Fails OPEN: an empty or unreadable file list is `code=true`. Skipping the
tests because we could not tell is the one mistake this must never make.
"""

from __future__ import annotations

import argparse
import re
import sys

DOCS = re.compile(r"(\.md$|(^|/)(docs|plans)/|(^|/)LICENSE$)")


def is_docs(path: str, code_re: re.Pattern | None = None) -> bool:
    if code_re and code_re.search(path):
        return False
    return bool(DOCS.search(path))


def classify(paths: list[str], code_re: re.Pattern | None = None) -> bool:
    """True when the change carries code (or when we cannot tell)."""
    paths = [p.strip() for p in paths if p.strip()]
    if not paths:
        return True
    return not all(is_docs(p, code_re) for p in paths)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--code-regex", default="", help="paths that count as code even if docs")
    args = ap.parse_args()
    code_re = re.compile(args.code_regex) if args.code_regex else None
    paths = sys.stdin.read().splitlines()
    code = classify(paths, code_re)
    print(f"code={'true' if code else 'false'}")
    print(f"files={len([p for p in paths if p.strip()])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
