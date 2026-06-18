# Pháros FE-spec rollout v2 — registry adoption across the 3 remaining apps

> ⛔ **Supersedes** [`plans/archive/pharos-fe-spec-rollout.md`](archive/pharos-fe-spec-rollout.md) (v1, 2026-06-17).
> **Execution plan for [RFC 0008](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) (ACCEPTED 2026-06-17), Phases 1–3 — the FE rollout.**
> v1 predated `spec(3)` + the pixel-spec reproducibility work and carried two stale sub-brand values.
> This v2 bakes the corrected spec, records **pharos-lis as the DONE reference**, resolves the open
> decisions (German, 2026-06-18), and adapts each track to the **real, current FE** of each app
> (surveyed 2026-06-18).
>
> **Written to be executed by a Sonnet-class agent under Opus review.** Steps are file-anchored +
> imperative; each track has a **VERIFY** block. Judgment steps are tagged **🟠 ESCALATE**
> (owner/architect decides — do **not** guess); everything else is **🔵 mechanical**. All repos
> branch off **`develop`** (confirm PR base at open — `origin/HEAD→main` on finance/commercial is
> just the GitHub default).

## Status

- **Step 0 · pharos-lis «Laboratorio» — ✅ DONE (reference).** `lab-qc/frontend` on `develop @ 3b17aa8`:
  canonical shell, 6 fidelity fixes, reproducible spec (family `092fa725`, lis-clinico `52802ac5`),
  `shell-contract` CI gate green. **This is the pattern every track copies.**
- **Track A · admission-patient «Pacientes» — ⬜ CANARY (next).**
- **Track B · finance-lch «Números» — ⬜.**
- **Track C · commercial-lch «Clientes» — ⬜.**
- **biuman-lis «Deportivo» — DEFERRED** (out of scope; RFC 0008 Phase 3, separate plan).

## Owners & order (sequencing locked 2026-06-18 — hardest-first canary)

| # | Track | App | FE dir | Owner | Effort | Risk |
|---|---|---|---|---|---|---|
| **A** | Pacientes | admission-patient | repo root (no `frontend/`) | **skuger** | L | **High** — srcDir migration + pastel + 2 layouts |
| **B** | Números | finance-lch | `frontend/` | **egomez** | M | Med — replace a rich shell, retire cobol, chart tokens |
| **C** | Clientes | commercial-lch | `frontend/` | **crincon04** | S | Low — near-blank slate |

Track A is the canary on purpose: it proves the srcDir migration + the pastel split + the full
sync→verify loop end-to-end before B/C start. B and C may overlap once A's pattern is confirmed
(both are `app/`-native and low-risk), owner schedules permitting.

## Decisions locked (German, 2026-06-18)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Pastel contrast (Pacientes `#FFE0E6` / Clientes `#FFB86B`) | **SPLIT** — pastel kept as a decorative wash; functional `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds) = **`#ff3d63`** (rosa) / **`#e37600`** (ámbar), AA-compliant. Fixed in `registry/tokens.css` **and** `buildSpec`; regen `admisiones.md`+`crm.md`; bump ledger. |
| 2 | admission-patient flat-root vs `app/` srcDir | **Migrate to `app/` srcDir** — `git mv` the Nuxt dirs into `app/`; `server/` + `nuxt.config.ts` stay at root → Minio Nitro routes untouched. **No sync fork.** |
| 3 | Backend data scope for first adoption | **Mock-first** through Stages 1–3; real backend wired + validated only at Stage 5 owner sign-off. |
| 4 | finance-lch 3rd "cobol" theme | **Retire** — `.dark`-only per RFC 0008 ("no cobol"). |

## Corrected spec values — live `registry/spec/*` (supersedes the v1 table)

| Sub-brand | spec-ver (target) | theme class | `--primary` (light / dark) | glyph | subLabel | sub-name | Intensidad | browser tab |
|---|---|---|---|---|---|---|---|---|
| **Números** (erp) | `5c38266d` | `theme-numeros` | `#7A5D00` / `#E6C34D` | `ShipWheel` | `ERP · Finanzas y operaciones` | Números | **Sutil** | `Pháros — Números` |
| **Clientes** (crm) | `b4e4f78a` | `theme-clientes` | wash `#FFB86B` → fn `#e37600` | `Telescope` | `CRM · Relaciones comerciales` | Clientes | **Neutro** *(v1 said Sutil — stale)* | `Pháros — Clientes` |
| **Pacientes** (admisiones) | `cb47c317` | `theme-recepcion` | wash `#FFE0E6` → fn `#ff3d63` | `Anchor` | `Admisiones · Recepción` | **Pacientes** *(v1 said Recepción — stale)* | `Pháros — Pacientes` |

Family `092fa725` + lis-clinico `52802ac5` are already current in
`registry/spec/.implemented.json`. Each track bumps its own ledger entry on Stage-5 sign-off:
`admisiones 091d6523 → cb47c317` · `erp 8be5e785 → 5c38266d` · `crm 8a032836 → b4e4f78a`.

## The model — 5-stage deployable track

Each app is an independent track. A Sonnet agent carries stages **1–3**; the owner/architect carries
**4–5**.

| Stage | Name | Gate / DoD |
|---|---|---|
| 1 | **Adopt** | Shell synced + 5 knobs set; app builds; renders light + dark |
| 2 | **Gate** | Layer A (pre-commit) + Layer B (`pharos-lint-check.yml` required check) + Layer D (`check-token-drift`/`check-contrast`/`check-font-allowlist`) green |
| 3 | **Validate** | App's own `e2e/shell-contract.spec.ts` (6 assertions) + `test-contract` CI job green; **verified by running** (screenshots L+D, nav group expanded to an active leaf) |
| 4 | **Deploy** | `ci-cd.yml` (owner-gated) |
| 5 | **Sign-off** | Owner validates against **real backend**; bump `.implemented.json` |

**"Migrated" = the synced shell (`app/layouts/default.vue`) + the 5 knobs + a green shell-contract.**
**No pixel baselines** (vetoed as excessive — the shell-contract spec is the durable guard).
**Never hand-edit registry-owned files** (`tokens.css`, anything under `registry/app/**`, the gate
scripts, the lint workflow) — fix the registry → re-sync.

**The five per-app knobs** (everything else is sync-owned):

| Knob | Where | Notes |
|---|---|---|
| theme class | `nuxt.config.ts` → `app.head.htmlAttrs.class` | e.g. `theme-recepcion` |
| browser tab | `nuxt.config.ts` → `title` (`titleTemplate: 'Pháros — %s'` is inherited) + favicon `link` + `public/favicon.svg` | e.g. `title: 'Pacientes'` → `Pháros — Pacientes` |
| glyph + sub-name + subLabel | `app/app.vue` → `<NuxtLayout glyph="…" sub-name="…" sub-label="…">` | Lucide-by-name |
| nav | `app/navigation/menu.ts` | es-CO; group → sub-group → leaf |
| user / topbar slots | `app/app.vue` → `#user` (`<SidebarUser>` wired to the app's auth store) + `#topbar-end` | app-owned content |

## Execution protocol (per track — for the implementing agent)

1. `git -C <repo> checkout develop && git -C <repo> pull && git -C <repo> checkout -b feat/pharos-fe-spec`.
2. Do the 🔵 steps in order. For every 🟠 step: **stop and ask the owner/architect** — do not improvise.
3. **Gate after every step**: `pnpm lint-check` stays green (or gets greener); run the app and eyeball the changed surface in **both light and dark**.
4. **Commit per step**, scoped to touched files (Conventional Commits + `Co-Authored-By`). **Never `git add -A`/`.`**; **never push** unless the owner asks.
5. Track is **done** when its **VERIFY** block passes. Then the owner opens the PR (**owners merge their own**).

**Copy, don't reinvent.** The shell, tokens, gate scripts, eslint template, and lint workflow all
come from the registry via `sync-pharos-registry.sh`. Lucide glyphs: `Anchor`, `ShipWheel`,
`Telescope` from `lucide-vue-next`.

## Stage 0 (rollout-wide pre-req) — the pastel SPLIT, done once · 🟠 architect-reviewed

Blocks Track A's accent (the canary is rosa). Dogfood discipline — **fix render + registry + spec +
generator together** (the "did you fix the generator too?" rule):

1. 🔵 **`Interval-Col/.github → registry/tokens.css`**: in `.theme-recepcion`, keep `#FFE0E6` as the
   decorative wash token(s); set functional `--primary` / `--ring` / `--sidebar-primary` (+ foregrounds)
   to `#ff3d63`. Same split for `.theme-clientes`: wash `#FFB86B`, functional `#e37600`.
2. 🟠 **`design-studio → buildSpec`**: serialize the wash-vs-functional split so a fresh
   `Exportar spec` is reproducible. **German merges his own design-studio PR.**
3. 🔵 **Regenerate** `registry/spec/admisiones.md` + `crm.md`; reconcile the spec-version + ledger
   targets (re-stamp if the split changes the hash).
4. 🔵 **Re-sync pharos-lis** + run its `shell-contract` → confirm zero regression (teal «Laboratorio»
   is not pastel, must be unaffected).
5. 🔵 `check-contrast` over the new functional values → must pass AA.

## Track A — admission-patient «Pacientes» (CANARY) · owner skuger

Repo root *is* the Nuxt app (no `frontend/`). Open the track with a **Sonnet deep-adaptation dig**
(file-level diff) reviewed by Opus; the steps below are its spec.

**Stage 1 · Adopt**
- 🔵 **srcDir migration:** create `app/`; `git mv` the Nuxt source dirs
  (`pages components layouts composables middleware plugins stores utils interfaces schemas services
  assets app.vue`) into `app/`. **Leave at root:** `server/` (14 Nitro routes incl. Minio
  `accounting/**`), `nuxt.config.ts`, `e2e/`, `playwright.config.ts`, `public/`. Verify `~`/`@`
  resolve to `app/` (Nuxt 4 default); fix any relative imports the move breaks. **Confirm `pnpm build`
  + the existing `e2e/smoke.spec.ts` pass BEFORE touching the shell** (isolates migration risk from
  shell risk).
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh .` from the repo root (single-app: fe-dir
  contains `app/`; `FE_REL` resolves to `.`).
- 🔵 **Manual follow-ups** (per sync output): `@import` tokens + components CSS in
  `app/assets/css/main.css`; `@nuxt/fonts` (Fraunces · DM Sans · IBM Plex Mono · JetBrains Mono);
  `lint-check` script in `package.json`; `@nuxt/eslint` + `nuxt prepare` postinstall; merge
  `registry/pre-commit.snippet.yaml` into `.pre-commit-config.yaml`.
- 🔵 **Knobs:** `nuxt.config.ts` → `htmlAttrs.class: 'theme-recepcion'`, `title: 'Pacientes'`,
  favicon link + `public/favicon.svg`. `app/app.vue` → `<NuxtLayout glyph="Anchor" sub-name="Pacientes"
  sub-label="Admisiones · Recepción">`. `#user` → `<SidebarUser>` wired to admission's SSO store;
  `AppHeader` apps-switcher → `#topbar-end`.
- 🟠 **nav mapping:** map the 8 `AdmisionSidebar` sections → `app/navigation/menu.ts` (Iconify class
  strings → Lucide component names; es-CO labels; real routes) — escalate any ambiguous section.
- 🔵 **2nd layout:** keep the header-only `deliveriesView` as an app-owned secondary layout (or route
  its pages through the shell sans-sidebar) — decide in the dig; not a registry concern.

**Stages 2–5:** Layer A/B/D synced + green → own `e2e/shell-contract.spec.ts` (active leaf + parent
group, glyph == `--primary`, bell, "Instrumento" ruler, tab `Pháros — Pacientes`) + `test-contract`
job → **VERIFY** → owner deploy → sign-off (mock→real) + bump `admisiones.md → cb47c317`.

**VERIFY (A):** `pnpm lint-check` green · `pnpm build` ok · screenshots light+dark · **expand a nav
group to an active leaf** (rosa beam + parent-group beam render; `Anchor` glyph is `#ff3d63`, not
gray) · `pnpm test:contract` green · Minio `server/api/accounting/**` routes still respond.

## Track B — finance-lch «Números» · owner egomez

Nuxt 4, clean `app/` srcDir ✓ — no migration. FE at `finance-lch/frontend`.

**Stage 1 · Adopt**
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh frontend .` from the repo root (monorepo:
  fe-dir=`frontend`, repo-root=`.`; `FE_REL` resolves to `frontend`).
- 🔵 **Replace** the ~650-line `app/layouts/default.vue` with the synced shell.
- 🔵 **Retire cobol:** drop the `data-theme` 3rd mode; `.dark`-only.
- 🟠 **RBAC nav:** map the capability-gated nav (`requiresCap` / `ship`) → `app/navigation/menu.ts`,
  preserving the gating by filtering the nav model in the app layer — escalate ambiguous palette/role
  mappings.
- 🔵 **Knobs:** `theme-numeros`, glyph `ShipWheel`, subLabel `ERP · Finanzas y operaciones`,
  `title: 'Números'`, Intensidad **Sutil**. Currency-scale toggle → `#topbar-end` (app-owned).
  `#user` → finance auth store.
- 🟠 **Charts (your call — FE only plots, backend owns stats):** keep **chart.js** for now; the synced
  `tokens.css` defines `--chart-1..5` (finance's were dead aliases). Optionally point charts at
  `--chart-1..5`. **`@unovis` migration is OUT of shell-adoption scope** — a separate, optional
  follow-up. **No stats rewrite.**

**Stages 2–5** as Track A (own shell-contract against finance routes; tab `Pháros — Números`; bump
`erp.md → 5c38266d`).

**VERIFY (B):** lint-check green · build ok · screenshots light+dark · expand nav to active leaf
(ámbar `#E6C34D` dark / `#7A5D00` light beam) · cobol theme gone · charts still render with their
tokens · `pnpm test:contract` green.

## Track C — commercial-lch «Clientes» · owner crincon04

Nuxt 4, `app/` srcDir ✓, FE at `commercial-lch/frontend`, near-blank slate (`app.vue` = `<NuxtPage/>`).

**Stage 1 · Adopt**
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh frontend .` — the sync **brings the shadcn
  `ui/` primitives + the shell** (the blank slate is a feature; nothing to tear out).
- 🔵 **`app/app.vue`:** wrap `<NuxtPage/>` in `<NuxtLayout glyph="Telescope" sub-name="Clientes"
  sub-label="CRM · Relaciones comerciales">`.
- 🔵 **nav:** build `app/navigation/menu.ts` from the 4 pages (index + quotes CRUD).
- 🔵 **Knobs:** `theme-clientes` (functional `#e37600` via the Stage-0 split), `title: 'Clientes'`,
  Intensidad **Neutro**. `#user` → commercial auth store.
- 🔵 **Apax font** coexists with the 4 Pháros fonts (no clash). Preserve the single Nitro route
  `server/api/pdf-render.post.ts`.

**Stages 2–5:** e2e is greenfield — add Playwright + `playwright.config.ts` + own
`shell-contract.spec.ts` + `test-contract` job; tab `Pháros — Clientes`; bump `crm.md → b4e4f78a`.

**VERIFY (C):** lint-check green · build ok · screenshots light+dark · expand nav to active leaf
(`#e37600` beam) · `pdf-render` route intact · `pnpm test:contract` green.

## RFC 0008 amendment (durable decisions — German merges)

A small `Decisions · 2026-06-18` amendment records: (1) the **pastel-split encoding rule** (wash vs
AA functional `#ff3d63`/`#e37600`); (2) the **canonical spec-name corrections** (Clientes Intensidad
`Neutro`; admisiones sub-name «Pacientes»); (3) the explicit **biuman-lis deferral**. Prepared on a
branch in `rfcs`; **German reviews + merges his own RFC PR**.

## Opus vs Sonnet — division of labor

- **Opus:** the locked decisions (done); review of the pastel-split values + the `buildSpec` change;
  review of each Sonnet adaptation dig + diff; the RFC amendment prose; Stage-5 gating.
- **Sonnet (under Opus review):** the per-app deep-adaptation digs, the srcDir `git mv`, knob-setting,
  `menu.ts` authoring, each `shell-contract.spec.ts`, the CI jobs.

🛑 chart statistical parity (finance) stays the architect's call; 🟠 pastel contrast was resolved
2026-06-18. Doc prose English; UI literals es-CO; code/DB English.
