---
status: active
owner: gczuluaga
created: 2026-06-01
updated: 2026-06-02
home: Interval-Col/.github (org-level — this automation spans every repo's trackers, so it lives here, not in any single app repo)
related:
  - Interval-Col/rfcs#4 (digest thread where the tracker convention was announced)
  - trackers it operates on: Interval-Col/finance-lch#1, Interval-Col/nucleus-db#1,
    Interval-Col/nucleus-db#2, Interval-Col/rfcs#3, Interval-Col/admission-patient#4,
    Interval-Col/admission-patient#5, Interval-Col/commercial-lch#1, Interval-Col/commercial-lch#2
note: >
  End-of-day automation to keep the org's GitHub issue trackers current.
  v1 (central, propose-only) chosen 2026-06-01 as the starting shape;
  v2 (per-dev) and v3 (auto-apply high-confidence) are PARKED here so we
  don't forget them — they are the graduation path, not day-one scope.
---

# EOD tracker-hygiene automation

Keep the cross-repo trackers honest **automatically**, instead of by the
manual pass we ran 2026-06-01. A scheduled Claude Code routine wakes at the
end of the working day, reads the day's merged work, and reconciles it
against the trackers' checklists.

This is an **org-level** concern — it touches trackers in every app repo —
so the plan lives in `Interval-Col/.github`, not in any single app's `plans/`.

## The convention it enforces (already agreed)

Announced in the digest thread (Interval-Col/rfcs#4):
1. **Native task-list checkboxes** (`- [ ]` / `- [x]`) are the single source
   of progress truth — `✅`-in-prose does NOT roll up and is decoration only.
2. A visible **`Blocked by: #N`** line where a real dependency exists.

## Why this is hard (the reason v1 is propose-only)

Mapping a day's commits/PRs to checklist items is a **guess**. A commit
"fix payer modal" does not cleanly map to "Phase 4 — Payers · done." A
*wrong* tick is worse than no tick: it tells the **gate-keeper** something
is finished when it isn't. We tripped the write-action safety rails twice
doing this by hand with a human watching — an unattended nightly cron
multiplies that risk. So trust is earned in phases.

## Phases

### v1 — Central, propose-only  ✅ LIVE 2026-06-02
- **Routine:** `trig_01WTXhtzpJfFzRgZSqnCxdQC` (manage at claude.ai/code/routines),
  owner @gczuluaga, cron `0 0 * * 2-6` = weekdays 19:00 Bogotá, model sonnet-4-6,
  tools Bash/Read/Grep, env **"Interval-Col GH"**. Manual test run 2026-06-02
  returned 200 (GitHub access OK).
- **Watches the 4 active execution-trackers** (the `eodWatch` set from the
  2026-06-02 portfolio triage): commercial-lch#1, admission-patient#4,
  admission-patient#5, nucleus-db#5. (finance-lch#1 + nucleus-db#2 were closed
  in that triage; the others are co-creation/parked, not week-to-week movers.)
- Reads the day's merged PRs across the active repos (by author, from git).
- Posts **one "tracker check-in" comment** per active tracker:
  *"Looks done today: suggest ticking 1.4, 1.5 on #4 — confirm?"* and
  @-mentions the owner.
- **No auto-edits.** The human ticks the box. Zero mismark risk.
- Run it ~1 week; tune which signals it trusts before graduating.

### v2 — Per-dev routines  ⏸ PARKED (graduation)
- Each dev runs their **own** EOD routine, under their **own identity**, so
  it knows their actual day's work and attribution is correct.
- **Prerequisite:** every dev is on Claude Code and creates their routine.
  Until then, v1's central model is the only option.
- Better accuracy + correct authorship than central; more setup per person.

### v3 — Auto-apply high-confidence  ⏸ PARKED (graduation)
- Routine **auto-ticks only** boxes whose PR explicitly names the issue +
  item (e.g. branch/title `…#4 1.5`); everything fuzzy stays a *suggestion*.
- Only after v1 has shown the suggestions are reliably right.
- Note: this is the point where the routine starts **writing** to trackers
  unattended — it needs scoped write permission and will surface the same
  write-action guardrails we hit manually.

## Setup — how to connect GitHub (learned the hard way, 2026-06-02)

A routine's GitHub access does NOT come from the org GitHub App alone. The
routine runs as a cloud agent that needs **your claude.ai account's GitHub
token**, and getting it there has two non-obvious requirements:

1. **Run `/web-setup` in the TERMINAL CLI** — the **VS Code extension does not
   expose `/web-setup`**. Install the standalone CLI first
   (`npm install -g @anthropic-ai/claude-code`), run `claude` in a terminal
   (sign in as the **same account** that owns the routine), then `/web-setup`
   and authorize GitHub. This syncs the `gh` token the routine uses.
2. **Use a GitHub-connected environment** — after `/web-setup`, `/schedule`
   offers an env named **"Interval-Col GH"**. The old generic "Default" env
   fails with `github_repo_access_denied`.

**Red herrings that cost ~1 hour on 2026-06-02 (don't repeat):**
- Installing the org **GitHub App** (repos=all) — needed for interactive
  sessions, NOT sufficient for routines.
- The org's **"Access restricted" OAuth third-party policy** — irrelevant; the
  Claude integration is a **GitHub App**, not an OAuth App. Do NOT click
  "Remove restrictions"; it wouldn't help and weakens the org.
- Recreating the routine / waiting for propagation — neither fixed it.

**Failure signature:** routine run → HTTP 400 `github_repo_access_denied`
("re-authorize GitHub in settings"); a scheduled run auto-disables with
`ended_reason: auto_disabled_repo_access`.

## Open questions before building v1
- Schedule: one fixed time (e.g. 19:00 America/Bogotá) vs per-dev EOD.
- Scope: which repos/trackers are "active" enough to be worth a nightly check.
- Cost: cloud-agent tokens × repos × weekdays — confirm acceptable.
- Permission: the routine needs issue-comment rights; an auto-apply (v3)
  routine needs issue-edit rights.

## Decision log
- **2026-06-01** — Chose **v1 (central, propose-only)** as the starting
  shape. Parked v2 (per-dev) + v3 (auto-apply) as the graduation path so
  they are not forgotten. (gczuluaga)
- **2026-06-01** — Relocated this plan from `finance-lch/plans/` to
  `Interval-Col/.github/plans/` — it's org-level, not finance-specific. (gczuluaga)
- **2026-06-02** — v1 **stood up and verified** (`trig_01WTXhtzpJfFzRgZSqnCxdQC`,
  env "Interval-Col GH"); manual run returned 200. Scoped to the 4 `eodWatch`
  trackers from that day's portfolio triage. (gczuluaga)
- **2026-06-02** — Recorded the GitHub-connection requirement (`/web-setup` in
  the terminal CLI + a GitHub-connected env) after an hour of dead ends — see
  the **Setup** section. (gczuluaga)
