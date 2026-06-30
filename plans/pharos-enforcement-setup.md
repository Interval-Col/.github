---
status: in-progress
owner: gczuluaga
created: 2026-06-18
updated: 2026-06-29
issue: none — admin runbook; related open tracking issues Interval-Col/.github#43 and #73
start: TBD
target: TBD
implementation: gczuluaga
effort: S
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# Pháros Enforcement Setup — Branch-Protection & Retro-Gate Admin Runbook · Configuración de controles Pháros — runbook de branch-protection y Retro Gate

# Pháros rollout — enforcement setup (admin runbook · @gczuluaga only)

> ⚠️ These change **branch-protection / repo settings** — run by the org admin (German), not by an
> agent. They arm the "dictatorial standard" the v2 plan + Retro Gate assume. The recon found
> `pharos-lint-check` is **not** a required check in any target repo today, so the design-system gate
> is currently unenforced at CI. **Confirm exact context strings + `gh api` syntax against a first run
> before relying on them** (they're written indicatively; not agent-tested).

## A. Now — one-time, before Track A

1. **Merge** the v2 plan PR (includes `retro-gate.yml`) + the RFC PR.
2. **Create labels:**
   ```sh
   gh label create retro-gate -R Interval-Col/.github -c 5319e7 -d 'Pháros track handoff (Retro Gate) PR'
   for r in admission-patient finance-lch commercial-lch; do
     gh label create blocked:retro-gate -R "Interval-Col/$r" -c b60205 -d 'Blocked: awaiting prior track Retro Gate'
   done
   ```
3. **Register `retro-gate` as a required check on `.github` `main`** — after the workflow has run once
   on a `retro-gate`-labeled PR (so the context name is registered). Confirm the exact context name
   (`Pháros — retro-gate` / `retro-gate`) from that run, then add it to the existing required checks
   on `Interval-Col/.github` `main` (keep `gitleaks`).
4. **Parity fixes:**
   - `commercial-lch` `main`: enable `dismiss_stale_reviews` (the other two repos have it).
   - `admission-patient` `CODEOWNERS`: add `@SKuger01` for the frontend path(s) (a PR, not a setting) —
     matches finance-lch/commercial-lch granularity.

## B. Per-track — during each track's Stage 1–2 (once sync lands `pharos-lint-check.yml`)

For the track's repo `<repo>`, after the workflow is synced + has reported once on `develop`:
- Add the design-system context (confirm exact name, e.g. `Pháros — lint-check`) to the **required
  status checks on BOTH `develop` and `main`** — **alongside** the existing required contexts
  (`gitleaks` + the repo's lint/test/contract jobs); do not remove them.
- Required checks on `develop` block **even direct pushes** (per `BRANCHING-AND-DEPLOY.md`) — this is
  the load-bearing lever that makes the standard non-negotiable.
- The Retro Gate's STANDARD-conformance step verifies the **next** repo is armed before handoff, so
  this closes Gap 1 track-by-track.

## C. Deferred (escalation)

- Leave `enforce_admins` **OFF** for now — it preserves the documented solo-merge flow
  (`gh pr merge --admin`). Once a real second code-owner exists, turn it ON for `Interval-Col/.github`
  so even an admin cannot merge a red `retro-gate` check.
