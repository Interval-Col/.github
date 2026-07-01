#!/usr/bin/env python3
"""Plan-standards linter (advisory) — deterministic, zero-dependency.

Lints the plan `.md` files given as arguments against the org plan standard
(schema v2.1 + plan-craft): required frontmatter keys, the controlled `status`
enum, retired keys, bilingual title, top Resumen. Emits GitHub Actions
annotations (`::warning ...`) so violations surface inline on the PR.

ADVISORY by default (exit 0) — it annotates, it does not fail the check. This is
deliberate until the status-enum ↔ board-column reconciliation is ratified
(Interval-Col/operations#38). Pass `--strict` to fail on violations (the
"promote to required" mode) once #38 lands and the pilot repos are green.

Usage:
  python3 plan_lint.py [--strict] <plans/foo.md> [<plans/bar.md> ...]
"""
import sys, re, os

REQUIRED_V21 = ["status", "owner", "created", "updated",
                "issue", "start", "target", "implementation"]
STATUS_ENUM = {"proposed", "active", "in-progress", "blocked", "done",
               "superseded", "abandoned"}
RETIRED_KEYS = {"completed", "tracking-issue", "tracking-issues"}
PROMOTE_GATE = "Interval-Col/operations#38"


def parse_frontmatter(text):
    lines = text.split("\n")
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    # skip a leading HTML comment (templates)
    if i < len(lines) and lines[i].lstrip().startswith("<!--"):
        while i < len(lines) and "-->" not in lines[i]:
            i += 1
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return None
    vals = {}
    j = i + 1
    while j < len(lines) and lines[j].strip() != "---":
        m = re.match(r"^([A-Za-z][\w\-]*):(.*)$", lines[j])
        if m:
            vals.setdefault(m.group(1), m.group(2).strip())
        j += 1
    if j >= len(lines):
        return None
    return vals


def norm_status(val):
    if not val:
        return ""
    head = re.split(r"\s+[—–-]\s+|\s*\(|\s*:\s*", val.strip(), maxsplit=1)[0].strip().lower()
    return head.split()[0] if head.split() else head


def is_lintable(path):
    p = path.replace("\\", "/")
    base = os.path.basename(p)
    return ("/plans/" in p or p.startswith("plans/")) and "/archive/" not in p \
        and "template" not in base and base != "README.md" and p.endswith(".md")


def annotate(level, path, msg):
    print(f"::{level} file={path},line=1::{msg}")


def lint_file(path):
    """Return the number of violations (advisory annotations emitted)."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        annotate("warning", path, f"could not read: {e}")
        return 1
    fm = parse_frontmatter(text)
    n = 0
    if fm is None:
        annotate("warning", path, "plan has no frontmatter block — add the schema v2.1 header (see plan-template.md)")
        return 1
    missing = [k for k in REQUIRED_V21 if not fm.get(k)]
    if missing:
        annotate("warning", path, f"missing required v2.1 frontmatter keys: {', '.join(missing)} "
                 f"(use `issue: none — <reason>` to opt out)")
        n += 1
    st = norm_status(fm.get("status", ""))
    if st and st not in STATUS_ENUM:
        annotate("warning", path, f"status '{fm.get('status')}' is not in the controlled enum "
                 f"({' | '.join(sorted(STATUS_ENUM))})")
        n += 1
    retired = [k for k in fm if k in RETIRED_KEYS]
    if retired:
        annotate("warning", path, f"retired frontmatter key(s) {retired} — use `status: done`+`updated:` "
                 f"and `issue:` instead")
        n += 1
    if not re.search(r"^#\s+.+·.+", text, re.M):
        annotate("notice", path, "no bilingual title `# English · Español` found")
        n += 1
    if not re.search(r">\s*\*\*Resumen", text):
        annotate("notice", path, "no top-level `> **Resumen (ES).**` blockquote found")
        n += 1
    return n


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    files = [a for a in args if a != "--strict"]
    files = [f for f in files if is_lintable(f)]
    if not files:
        print("plan-lint: no lintable plan files in the change set — OK")
        return 0
    total = 0
    for f in files:
        total += lint_file(f)
    print(f"\nplan-lint: {len(files)} plan file(s) checked, {total} finding(s).")
    if strict:
        print("mode: STRICT — findings fail the check.")
        return 1 if total else 0
    print(f"mode: ADVISORY — findings annotate only, they do NOT fail this check.")
    print(f"      Promote to `--strict` (required) once {PROMOTE_GATE} ratifies the status vocab "
          f"and the pilot repos are green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
