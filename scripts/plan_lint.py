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

# A plan may declare a deliberate divergence with `standard-exception: <reason>`.
#
# It covers PROSE ONLY — the bilingual title and the Spanish Resumen — because that
# is where a divergence can be legitimate (a framing doc written wholly in Spanish
# gains nothing from a bilingual title). It NEVER covers frontmatter: required keys,
# the status enum and retired keys are what machines read, and an exception there is
# a hole, not a decision. The first cut of this key exempted the whole file, which
# let four repos report zero findings while still missing dates (2026-08-06).
#
# The reason is MANDATORY: a bare key is itself a violation, so an exception can
# never be a silent opt-out — it is readable in the frontmatter and echoed in the log.
EXCEPTION_KEY = "standard-exception"
EXEMPTIBLE = "prose"   # marker for findings a declared exception may waive

# `start` / `target` feed planning, and `TBD` in them is worthless. A real date is
# the norm; the ONE sanctioned alternative is `none — <reason>`, for a plan whose
# exit is gated on an event rather than a calendar ("none — gated on the 20-report
# validation"). Ratified 2026-08-06. Anything else — TBD, none without a reason,
# a half-written placeholder — is a violation.
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NONE_RE = re.compile(r"^none\s+[—–-]\s+\S.*$", re.IGNORECASE)


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
    """Lint one plan.

    Returns (hard, prose, exception_reason).
      hard  — frontmatter violations. NEVER waivable; a declared exception does
              not touch them, because this is what the board and the tooling read.
      prose — bilingual title / Spanish Resumen. Waivable by a declared exception.
    """
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        annotate("warning", path, f"could not read: {e}")
        return 1, 0, None
    fm = parse_frontmatter(text)
    hard = prose = 0
    if fm is None:
        annotate("warning", path, "plan has no frontmatter block — add the schema v2.1 header (see plan-template.md)")
        return 1, 0, None

    # An exception is only honoured when it carries a reason.
    exception = fm.get(EXCEPTION_KEY) or None
    if EXCEPTION_KEY in fm and not exception:
        annotate("warning", path, f"`{EXCEPTION_KEY}:` declared with no reason — state why this plan "
                 f"diverges, in one line, or remove the key. An exception is never silent.")
        hard += 1

    missing = [k for k in REQUIRED_V21 if not fm.get(k)]
    if missing:
        annotate("warning", path, f"missing required v2.1 frontmatter keys: {', '.join(missing)} "
                 f"(`issue:` and `target:` accept `none — <reason>`)")
        hard += 1
    st = norm_status(fm.get("status", ""))
    if st and st not in STATUS_ENUM:
        annotate("warning", path, f"status '{fm.get('status')}' is not in the controlled enum "
                 f"({' | '.join(sorted(STATUS_ENUM))})")
        hard += 1
    retired = [k for k in fm if k in RETIRED_KEYS]
    if retired:
        annotate("warning", path, f"retired frontmatter key(s) {retired} — use `status: done`+`updated:` "
                 f"and `issue:` instead")
        hard += 1
    # A planning date is a date, or the sanctioned `none — <reason>`. `TBD` is neither:
    # it looks filled-in while carrying no information, so it passed the presence check
    # and wrote nothing useful anywhere (19 plans were sitting on it).
    for key in ("start", "target"):
        val = fm.get(key)
        if val and not DATE_RE.match(val) and not NONE_RE.match(val):
            annotate("warning", path, f"`{key}: {val}` is neither a YYYY-MM-DD date nor the "
                     f"sanctioned `none — <reason>` (for a plan gated on an event, not a calendar)")
            hard += 1
    # Prose — the only findings a declared exception may waive.
    lvl = "notice" if exception else "warning"
    if not re.search(r"^#\s+.+·.+", text, re.M):
        annotate(lvl, path, "no bilingual title `# English · Español` found")
        prose += 1
    if not re.search(r">\s*\*\*Resumen", text):
        annotate(lvl, path, "no top-level `> **Resumen (ES).**` blockquote found")
        prose += 1
    return hard, prose, exception


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    files = [a for a in args if a != "--strict"]
    files = [f for f in files if is_lintable(f)]
    if not files:
        print("plan-lint: no lintable plan files in the change set — OK")
        return 0
    total = 0         # findings that count against strict mode
    exempt_total = 0  # prose findings waived by a declared exception
    exceptions = []
    for f in files:
        hard, prose, exception = lint_file(f)
        total += hard              # frontmatter is never waivable
        if exception:
            exempt_total += prose
            exceptions.append((f, exception, hard))
        else:
            total += prose
    print(f"\nplan-lint: {len(files)} plan file(s) checked, {total} finding(s).")
    if exceptions:
        print(f"\n{len(exceptions)} plan(s) carry a declared `{EXCEPTION_KEY}` "
              f"({exempt_total} prose finding(s) waived):")
        for f, reason, hard in exceptions:
            flag = f"  ⚠️ still {hard} frontmatter finding(s) — NOT waived" if hard else ""
            print(f"  · {f} — {reason}{flag}")
        print("  An exception waives prose only (bilingual title, Resumen). Frontmatter is")
        print("  what the tooling reads, so it is never waivable. Exceptions are deliberate")
        print("  and reviewable, not silence — re-read them when the plan's phase ends.")
    if strict:
        print("mode: STRICT — findings fail the check.")
        return 1 if total else 0
    print(f"mode: ADVISORY — findings annotate only, they do NOT fail this check.")
    print(f"      Promote to `--strict` (required) once {PROMOTE_GATE} ratifies the status vocab "
          f"and the pilot repos are green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
