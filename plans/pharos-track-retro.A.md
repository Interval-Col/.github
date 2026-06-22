# Pháros track retro — `A` admission-patient «Pacientes» · owner `skuger`

> Fill on **Stage 5 → handoff**. This is the **Retro Gate** (mandatory). Open as a PR against
> `.github` labeled **`retro-gate`**; this doc + the downstream plan-section edits ride **one**
> merge-commit. See `plans/pharos-fe-spec-rollout-v2.md` → §Retro Gate.

- **Track / app / FE dir:** `A` · `admission-patient` · `.` (root `app/` srcDir)
- **Owner:** `skuger`  **Date:** `2026-06-22`  **Handed off from commit:** `3b0a304` (`develop` merge of #27)
- **Next track(s) unblocked:** `B` **and** `C` — **parallel handoff** (lead's call; both sections were back-propagated, so C does not wait on B) · tracking issues `#47`, `#48`

> ⚠️ **Honesty note (read first):** the FE rollout (Stages 1–3) is **done and merged to `develop`**.
> Three §3 conformance items are **still pending external/infra unblocks** and are documented as such
> below (not silently passed): `test-contract` headless auth, the `required`-check flip, and the
> (inert) deploy pipeline. Per the owner's call, this retro lands the **lessons + back-propagation now**
> (the non-blocked, decaying-fast value); §3 evidence is updated when those clear.

## 1. Plan-vs-reality deltas (file-anchored)

> Canary (A): every §De-risk punch-list item reconciled — none silently dropped.

| # | Symptom observed (concrete) | Plan line it contradicts/extends | Downstream edit produced |
|---|---|---|---|
| 1 | **§De-risk #1 (deps-delta + lockfile) — RESOLVED for A:** A's deps were already in (the Track-2 shadcn migration), so no `pnpm add` was needed. BUT the lockfile/frozen path still bit: `pnpm/action-setup@v4` failed CI with *"Multiple versions of pnpm specified"* — the registry `pharos-lint-check.yml` pins `version: 10.x` while `package.json` had `packageManager: pnpm@10.15.1`. | §De-risk item 1 (`pharos-fe-spec-rollout-v2.md` L57–59) | B & C recipes: **drop `packageManager`** (or pin it to match the workflow exactly) when wiring the sync workflow. |
| 2 | **§De-risk #2 (gate-fit) — RESOLVED + EXTENDED:** fonts + the `@import`s were already clean in A; the **real** gate-fit cost was `no-raw-html` + colours. Surprise: the **colour gates scan ALL of `app/` (components too)**, while `no-raw-html` scans only `pages/`+`layouts/`. So per-page conformance = **page + its child components** (for colours). | §De-risk item 2 (L60–63) | B & C: "gate-fit = page **+ its components** for colours" note added to both recipes. |
| 3 | **Dead/legacy code is a hidden gate-fit cost.** The colour gates flagged ~20 dead files (superseded `calendar/` cluster, old chrome `AdmisionSidebar`/`AppHeader`, orphans). Purging them (verified 0 refs repo-wide + build-green) cleared ~158 palette/hex hits **without conforming code that should be deleted**. | (no plan line — new) | B & C: "purge dead/legacy first (0-refs + build-green) before tokenizing." |
| 4 | **The `ui/` set lacked `Table`/`Textarea`** (also no Checkbox/Switch). Closing `no-raw-html` for data tables/textareas needed **vendoring thin pass-through primitives** (`ui/table/*`, `ui/textarea/`). | C quotes-rewrite (L269–271 already names Table/Textarea) | C: confirm the rewrite **vendors** the primitives, doesn't just rename. B: same for finance tables. |
| 5 | **shadcn `<Input>` silently drops the `v-model.number` modifier** → number inputs return **strings**, breaking `money()`/arithmetic. Fix: `:model-value` + `@update:model-value` with explicit `Number()` coercion (a `toNum` helper). | (no plan line — new) | **B (number-heavy / finance)** + C (quote amounts): mandatory note. |
| 6 | **White-on-accent token trap:** forcing `--primary-foreground: #FFFFFF` (owner wanted white button text on the rosa accent) **failed the contrast gate** (white on `#ff3d63` ≈ 3.6:1 < AA 4.5) **and** drifted the registry-owned `tokens.css` (token-drift gate). Reverted to the registry default `#2A0A12` (≈4.6:1) to green both. | Decision 1 pastel SPLIT (L44) · Stage 0 / `theme-clientes #e37600` (L275–277) | **C: `#e37600` (ámbar) hits the EXACT same trap** — flag "white-on-ámbar fails AA; keep the registry foreground; never hand-edit `tokens.css`." |
| 7 | **e2e auth blocker (the big one):** the global `isAuthorized` middleware authorizes **server-side** (`$fetch` to the SSO). In CI there's no SSO → it throws → logout → the shell never renders → `shell-contract` can't auth headlessly. Playwright can't mock a **server-side** fetch; the pharos-lis reference mocks auth **client-side** (localStorage), which doesn't apply. | Stages 2–5 (B L251/254 · C L280/284) "`test:contract` green" | B & C: **plan a test/dev auth path up front** — an `import.meta.dev`-guarded middleware bypass, or a mock-SSO — else `test-contract` is non-blocking-red. |
| 8 | **Tooling gotchas that cost real time:** (a) `nuxt.config.devServer.port` must be set so `pnpm dev` binds the port the Playwright webServer waits on (else the CI job hangs). (b) After `app/` srcDir, **vitest's `~`/`@` alias points at repo root** (unit imports fail) and vitest tries to run the Playwright specs → fix alias→`app/` + `exclude: e2e`. (c) eslint 10 crashes on **Node ≤20** (`Object.groupBy`) — CI uses 22/24. | Stages 2–5 e2e/test recipes (B L251 · C L280) | B & C: carry the 3 fixes into the e2e/test setup steps. |
| 9 | **Visual cohesion ≠ green gates (the hands-on lessons).** Passing the gates left pages looking like a patchwork; the real work was **reforming each surface holistically** — no stray/half-tokenized styles, **no double-sidebar/double-chrome** (side panels must be an in-flow `<aside>` at page level via full-bleed `-m-6 h-[calc(100%+3rem)]`, never covering the shell nav), **dark mode re-checked end-to-end** (alternating table-row bg muddies dark → divider rows + single surface), no stray vertical scroll (excess top padding), **breadcrumb-as-title** (no duplicated `<h1>`), status→**badges**, drop gratuitous shadows, align popovers (`align="end"`). | The plan's per-track recipes cover **mechanics** (knobs/menu/srcDir), not **visual cohesion** | B & C: a **"Visual cohesion (conform, don't patch)"** checklist added to both recipes' Stage 2. |
| 10 | **Enforcement + deploy are unarmed.** `pharos-lint-check` is **not a required check in any repo** (404 — the standard is unenforced at CI today), and `ci-cd.yml` is an **inert scaffold** (merging to `develop` deploys nothing) — Stages 4–5 are blocked on porting the deploy pipeline (separate infra track, admission-patient#21). | §Enforcement setup (L121–130) · the inert `ci-cd.yml` | Carried (not new to the plan, but proven live): B & C will hit the same un-armed enforcement + inert deploy. |

## 2. Back-propagation into not-yet-started tracks

- **→ Track B (finance-lch):** added a **"Carried from Track A's retro"** block to the Track B section — colour-gates-scan-components + dead-code-purge-first (#2/#3), **the shadcn `.number` trap (critical, finance is number-heavy)** (#5), the SSR-auth e2e blocker + test-auth path (#7), the `pnpm packageManager` conflict (#1), the devServer.port / vitest-alias / Node-22 fixes (#8), and a **Visual-cohesion checklist** (#9: no double-sidebar, dark-mode, no stray styles, breadcrumb-as-title, badges/shadows/popovers).
- **→ Track C (commercial-lch):** added the same block to the Track C section, with extra emphasis where C differs — **the `#e37600` ámbar white-on-accent contrast trap** (#6), **vendoring `Table`/`Textarea` primitives for the quotes-page rewrite** (#4, the bulk of C's work), the `.number` trap on quote amounts (#5), plus the shared e2e/tooling/visual-cohesion items.

## 3. STANDARD conformance (evidence — honest current state)

- [x] **7-gate `Pháros — lint-check`** green — `pnpm lint-check` (Node 22) → eslint 0 warnings + all 7 gates OK; confirmed in CI on PR #27 (`ESLint + design gates` ✅, `lint-and-build` ✅).
- [x] **shell-contract** authored + green where the env allows — `pnpm test:contract` → **5/6 pass**; the active-leaf assertion **skips** locally on a Vite-dev hydration flake (concurrent client / optimize-deps 504), exercised in CI when isolated.
- [ ] **`test-contract` CI job green** — ⏳ **PENDING:** job is wired but **non-blocking** (`continue-on-error`); the SSR `isAuthorized` middleware can't reach SSO in CI → shell won't render headlessly. Needs a test/dev auth path (delta #7). Update on fix.
- [ ] **Drift ledger bumped** in `registry/spec/.implemented.json` + `check-spec-drift` green — ⏳ to run at handoff (no registry-owned spec change in this track).
- [ ] **ZERO registry-owned hand-edits** — the one hand-edit that did happen (`tokens.css` white override) was **reverted** (commit `5789936`); `token-drift` gate is **green**. `sync-pharos-registry.sh --dry-run` output to be pasted at handoff.
- [ ] **Next repo (finance-lch) armed** — ⏳ **PENDING:** `Pháros — lint-check` is **not** a required check in any repo (404). Arming finance's `develop`+`main` is the admin step before B's handoff (delta #10).

## 4. Handoff (German / @gczuluaga only)

- [ ] Retro PR merged (merge-commit) — `<PR link>`
- [ ] `blocked:retro-gate` removed from **#47 AND #48** + blocked-by cleared → **Tracks B & C unblocked (parallel)**
- [ ] Ritual confirmed: retro-gate CI green · downstream sections diffed · **not** an `--admin` override
