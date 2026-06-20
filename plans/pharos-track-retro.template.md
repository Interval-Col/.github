# Pháros track retro — `<track-letter>` `<app>` · owner `<handle>`

> Fill on **Stage 5 → handoff**. This is the **Retro Gate** (mandatory). Open as a PR against
> `.github` labeled **`retro-gate`**; this doc + the downstream plan-section edits + the ledger bump
> ride **one** merge-commit. The `retro-gate` CI check enforces the rules below.
> See `plans/pharos-fe-spec-rollout-v2.md` → §Retro Gate.

- **Track / app / FE dir:** `<A|B|C>` · `<repo>` · `<fe-dir>`
- **Owner:** `<handle>`  **Date:** `<YYYY-MM-DD>`  **Handed off from commit:** `<sha>`
- **Next track unblocked:** `<B|C|none>` · tracking issue `#<47|48|—>`

## 1. Plan-vs-reality deltas (file-anchored — platitudes fail the gate)

> One row per real surprise. **No row may be prose-only** — each cites the plan line it
> contradicts/extends AND the downstream edit it produced. **Canary (A): reconcile EVERY
> §De-risk punch-list item here** (resolved or explicitly carried — none silently dropped).

| # | Symptom observed (concrete) | Plan line it contradicts/extends (file:anchor) | Downstream edit produced (section + PR line) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

## 2. Back-propagation into not-yet-started tracks

> The `retro-gate` check **fails** unless this PR's diff shows a **non-empty** change in each
> downstream track section of `pharos-fe-spec-rollout-v2.md`. If a track genuinely needs nothing,
> state it explicitly on its own line — the check greps for this exact form:

- **→ Track B (finance-lch):** `<summary of edits made>`  _or_  `> Back-propagation: NONE — <why>`
- **→ Track C (commercial-lch):** `<summary of edits made>`  _or_  `> Back-propagation: NONE — <why>`

Sweep these categories: **deps deltas** · **config gotchas** · **gate-fit** (font allowlist / raw-HTML) ·
**recipe refinements** (srcDir, knobs, menu, color-mode) · **gate-behavior surprises**.

## 3. STANDARD conformance (dictatorial — paste evidence, do not summarize)

- [ ] **shell-contract** green — `<cmd>` → `<result/link>`
- [ ] **`test-contract` CI job** green — `<run link>`
- [ ] **7-gate `Pháros — lint-check`** green — `<run link>`
- [ ] **Drift ledger bumped** in `registry/spec/.implemented.json`: `<file> <old> → <new>`
      **AND** `check-spec-drift` green — `<result>`
- [ ] **ZERO registry-owned hand-edits** — paste `sync-pharos-registry.sh --dry-run <fe-dir> <root>`:
      ```
      <output — must show "nothing to copy" / no diffs>
      ```
- [ ] **Next repo armed** — `<next-repo>` has `Pháros — lint-check` registered **required on
      `develop` AND `main`**: `<gh api branch-protection excerpt>`

## 4. Handoff (German only)

- [ ] Retro PR merged (merge-commit) — `<PR link>`
- [ ] `blocked:retro-gate` removed from `#<next>` + native blocked-by cleared → next track unblocked
- [ ] Ritual confirmed: retro-gate CI green · downstream sections diffed · **not** an `--admin`
      override of a red `retro-gate` check
