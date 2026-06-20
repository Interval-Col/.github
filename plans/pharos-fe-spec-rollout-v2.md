# Pháros FE-spec rollout v2 — registry adoption across the 3 remaining apps

> ⛔ **Supersedes** [`plans/archive/pharos-fe-spec-rollout.md`](archive/pharos-fe-spec-rollout.md) (v1, 2026-06-17).
> **Execution plan for [RFC 0008](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) (ACCEPTED 2026-06-17), Phases 1–3 — the FE rollout.**
> v1 predated `spec(3)` + the pixel-spec reproducibility work and carried two stale sub-brand values.
> This v2 bakes the corrected spec, records **pharos-lis as the DONE reference**, resolves the open
> decisions (German, 2026-06-18), and adapts each track to the **real, current FE** of each app —
> **hardened by an adversarial de-risk pass (2026-06-18): 4 Opus auditors + an empirical lead-track build**
> (see the §De-risk corrections callout).
>
> **Written to be executed by a Sonnet-class agent under Opus review.** Steps are file-anchored +
> imperative; each track has a **VERIFY** block. Judgment steps are tagged **🟠 ESCALATE**
> (owner/architect decides — do **not** guess); everything else is **🔵 mechanical**. All repos
> branch off **`develop`** (confirm PR base at open — `origin/HEAD→main` on finance/commercial is the
> GitHub default).

## Status

- **Step 0 · pharos-lis «Laboratorio» — ✅ DONE (reference).** `lab-qc/frontend` on `develop @ 3b17aa8`:
  canonical shell, 6 fidelity fixes, reproducible spec (family `092fa725`, lis-clinico `52802ac5`),
  `shell-contract` CI gate green. **This is the pattern every track copies.**
- **Track A · admission-patient «Pacientes» — 🟡 IN PROGRESS · XL. Stage 1 Adopt DONE** (shell wired: nav/knobs/apps-switcher/bell; renders rosa light+dark; `pnpm build` green). **Stage 2 gate-fit IN PROGRESS — 9/14**: Pre-recepción · Inicio · Gestión médicos/pacientes · Estado de atención · Consultorios · Equipos · Plantillas de notificación · **Recepción** (whole intake flow: page + `PatientForm`/`ConfirmationPatientData`/`OrderCreation`/`OrderDemografic`/`CameraCapture` + the order sub-route, all 7 gates light+dark). **Scope learning: the colour gates scan components too → per-page conformance = page + its child components.** Styles only — functional fixes surfaced during the pass (patient-save 422 `null→""`, WS http-scheme for REST `$fetch`, dev caja bypass `import.meta.dev`-guarded) kept out of the style commits, tracked separately. On `feat/pharos-design-system`. Next: Agenda, Domicilios, Cajas, Horarios médicos, Toma de imágenes.
- **Track B · finance-lch «Números» — ⬜.**
- **Track C · commercial-lch «Clientes» — ⬜. Re-scoped S→M/High (raw-HTML rewrite + all deps missing).**
- **biuman-lis «Deportivo» — DEFERRED** (out of scope; RFC 0008 Phase 3, separate plan).

## Owners & order (sequencing locked 2026-06-18 — hardest-first)

> Terminology: **pharos-lis «Laboratorio» is the foundation/reference** (Step 0 — the proven first instance, done). The three apps below are the **rollout tracks**; admission-patient is the **lead track** (first + hardest), not a second proof.

| # | Track | App | FE dir | Owner | Effort | Risk |
|---|---|---|---|---|---|---|
| **A** | Pacientes | admission-patient | repo root (no `frontend/`) | **skuger** | **XL** | **High** — srcDir migration + missing deps + pastel + color-mode + 2 layouts |
| **B** | Números | finance-lch | `frontend/` | **egomez-lch** | M | Med — replace rich shell, cobol→.dark reconciliation, RBAC |
| **C** | Clientes | commercial-lch | `frontend/` | **crincon04** | **M** | **High** — raw-HTML page rewrite + all shell deps missing |

Track A goes first on purpose — it's the hardest rollout track, so it surfaces the unknowns early. B and C may overlap once A's pattern is confirmed, owner schedules
permitting — but **Stage 0 (below) must merge first**, it blocks A *and* C accents.

## Decisions locked (German, 2026-06-18)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Pastel contrast (Pacientes `#FFE0E6` / Clientes `#FFB86B`) | **SPLIT** — pastel kept as a decorative **wash token**; functional `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds) = **`#ff3d63`** (rosa) / **`#e37600`** (ámbar), AA-confirmed. |
| 2 | admission-patient flat-root vs `app/` srcDir | **Migrate to `app/` srcDir** (empirically proven — see Track A recipe). |
| 3 | Backend data scope for first adoption | **Mock-first** through Stages 1–3; real backend only at Stage-5 owner sign-off. |
| 4 | finance-lch 3rd "cobol" theme | **Retire** — `.dark`-only (full theme-mechanism reconciliation, not a one-block delete). |
| 5 | RBAC nav gating (finance) | **Amend the registry contract to a `useMenu()` composable** — shell imports a reactive, auth-filtered nav instead of a static `menu` const. One-time shell change benefiting all apps; needs re-sync + an RFC 0008 note. |
| 6 | Dark accents for the pastel themes | **APPROVED (German, 2026-06-18):** `.dark.theme-recepcion` `#ff6b85` (6.7:1 AA), `.dark.theme-clientes` `#f59e3c` (7.1:1 AA). The pastel themes currently have **no** `.dark` block → without these, dark mode falls back to navy. |
| 7 | Track C quotes-page raw HTML | **In-track prep stage** to rewrite the quotes pages to shadcn primitives; Track C re-budgeted M/High. |

## ⚠️ De-risk corrections (read before executing — from the 2026-06-18 adversarial pass)

The original v2 draft assumed "5 knobs, everything else sync-owned." The de-risk pass proved that
**under-counts the work**. Two systemic fixes apply to **every** track:

1. **The sync ships shell *code*, not the npm *packages* it imports.** Every track needs an explicit
   **dependency-delta** step (per-track lists below). After adding deps, **regenerate the lockfile**
   and commit it — CI runs `pnpm install --frozen-lockfile` and aborts on a stale lockfile.
2. **Gate-fit before Stage 2.** Each app must remove any **non-allowlisted font CDN** (Google Fonts /
   Inter / VT323 → `check-font-allowlist` hard-fails) and have **no raw `<input|select|table|button|textarea>`**
   in `pages/`/`layouts/` (`check-no-raw-html` hard-fails). The full **7-gate `lint-check`** string +
   the `pharos-tokens.css`/`pharos-components.css` `@import`s are required follow-ups (sync prints them).

Corrected per-track effort: A and C are both **High**. C is **not** a blank slate.

## The model — 5-stage deployable track

A Sonnet agent carries stages **1–3**; the owner/architect carries **4–5**.

| Stage | Name | Gate / DoD |
|---|---|---|
| 1 | **Adopt** | Deps added + lockfile regenerated; shell synced + 5 knobs; app builds; renders light + dark |
| 2 | **Gate** | Layer A (pre-commit) + Layer B (`pharos-lint-check.yml`) + Layer D (drift/contrast/font) green; gate-fit done |
| 3 | **Validate** | App's own `e2e/shell-contract.spec.ts` + `test:contract` script + `test-contract` CI job green; **verified by running** (screenshots L+D, nav group expanded to an active leaf) |
| 4 | **Deploy** | `ci-cd.yml` (owner-gated) |
| 5 | **Sign-off** | Owner validates against **real backend**; bump `.implemented.json` |
| 6 | **Retro Gate** | Back-propagate lessons into downstream tracks + prove standard conformance; **next track blocked until the Retro PR merges** (§Retro Gate) |

**Never hand-edit registry-owned files** (`tokens.css`, `registry/app/**`, gate scripts, the lint
workflow) — fix the registry → re-sync.

### Retro Gate (mandatory handoff) · 🟠 architect-gated

A track does **not** hand off on a green VERIFY block. Between one track's **Stage 5** and the
**next track's owner starting**, a mandatory **Retro Gate** runs — to stop three failures: (1) the
next track starting from a **stale plan**, (2) tracks **drifting** off the identical non-negotiable
contract, (3) lessons **dying with the finishing owner**. The chain compounds: **skuger** finishes
Track A → his retro back-propagates into **both** B & C → only then is B handed to **egomez-lch**;
egomez-lch finishes B → his retro refines the remaining **C** → only then is C handed to **crincon04**.

**The gate is ONE PR** against this repo (`.github`), labeled **`retro-gate`**, landing three things
in a single merge-commit:

1. 🔵 **Retro doc** — fill `plans/pharos-track-retro.<track>.md` from
   [`pharos-track-retro.template.md`](pharos-track-retro.template.md). Every lesson row is
   **file-anchored** (symptom → the plan line it contradicts/extends → the downstream edit it
   produced). For the **lead track (A)**, reconcile **every** §De-risk punch-list item — resolved or
   explicitly carried, **none silently dropped**.
2. 🔵 **Back-propagation — VERIFIABLE.** The **same PR** must edit the **not-yet-started** tracks'
   sections of this file. The **`retro-gate` CI check** (required on `.github` `main`) **fails**
   unless the diff shows a **non-empty** change in each downstream section. A genuine "nothing to
   carry" is allowed **only** via an explicit line the check greps for:
   `> Back-propagation: NONE — <one-line justification>` per downstream track. **"No change" is
   visibly suspicious — German reviews the rendered diff.**
3. 🔵 **STANDARD conformance — machine-proven** (assert + paste outputs in the retro doc):
   shell-contract + `test-contract` green · **7-gate `Pháros — lint-check` green** · drift ledger
   bumped **paired with `check-spec-drift` green** (a bare bump fails) · **ZERO registry-owned
   hand-edits** — paste `sync-pharos-registry.sh --dry-run <fe-dir> <root>` showing **nothing to
   copy** · **next repo armed** (its `Pháros — lint-check` registered **required on `develop` AND
   `main`** — see §Enforcement setup).

**Handoff is a machine state, not a conversation.** The next track's tracking issue (**#47** B /
**#48** C) is held by a **native blocked-by** link to the Retro PR **plus** a **`blocked:retro-gate`**
label owners have **no authority** to remove. **German** merges (merge-commit only — preserves the
diff) **and** removes the label — that single act, not any verbal "go," unblocks the next track.
Ritual: *retro-gate CI green · downstream sections diffed · not an `--admin` override of a red
retro-gate check* (`enforce_admins` is OFF by design — the gate binds contributors hard; for German
it rests on this ritual until a second code-owner exists).

### Enforcement setup (one-time, admin/German) — arms the "dictatorial standard"

> ⚠️ **Gap found by the de-risk recon: `pharos-lint-check` is NOT a required check in *any* target
> repo today** (it's 404 in all three) — so the design-system standard is currently **unenforced at
> CI**. These steps arm it; the Retro Gate then verifies the *next* repo is armed before each handoff.

- **(critical)** Per target repo: sync to land `pharos-lint-check.yml`, push to `develop` once so the
  context reports, then register **`Pháros — lint-check`** (confirm the exact context string) as a
  **required status check on `develop` AND `main`** via `gh api … /branches/{develop,main}/protection/required_status_checks`.
  Required checks on `develop` **block even direct pushes** — the load-bearing lever (per `BRANCHING-AND-DEPLOY.md`).
- Add a **`retro-gate.yml`** check to `.github` (fails a `retro-gate`-labeled PR unless it diffs the
  retro doc + each downstream track section; honors the `> Back-propagation: NONE — …` escape);
  register it **required on `.github` `main`**.
- Create labels **`retro-gate`** (`.github`) + **`blocked:retro-gate`** (target repos); optional
  self-healing guard re-applies the block label if removed by anyone but @gczuluaga.
- Minor parity: enable `dismiss_stale_reviews` on **commercial-lch** `main`; add **@SKuger01** to
  **admission-patient** CODEOWNERS.
- **Deferred escalation:** leave `enforce_admins` **OFF** (keeps your solo-merge flow); once a second
  code-owner exists, turn it ON for `.github` so even you can't merge a red `retro-gate` check.

## Corrected spec values — live `registry/spec/*`

| Sub-brand | spec-ver | theme class | `--primary` light / **dark** | glyph | subLabel | sub-name | Intensidad | tab |
|---|---|---|---|---|---|---|---|---|
| **Números** (erp) | `5c38266d` | `theme-numeros` | `#7A5D00` / `#E6C34D` | `ShipWheel` | `ERP · Finanzas y operaciones` | Números | **Sutil** | `Pháros — Números` |
| **Clientes** (crm) | `9d131f69` | `theme-clientes` | fn `#e37600` / **`#f59e3c`** · wash `#FFB86B` | `Telescope` | `CRM · Relaciones comerciales` | Clientes | **Neutro** | `Pháros — Clientes` |
| **Pacientes** (admisiones) | `94b02840` | `theme-recepcion` | fn `#ff3d63` / **`#ff6b85`** · wash `#FFE0E6` | `Anchor` | `Admisiones · Recepción` | **Pacientes** | Neutro | `Pháros — Pacientes` |

Ledger bumps on Stage-5 sign-off: `admisiones 091d6523 → 94b02840` · `erp 8be5e785 → 5c38266d` ·
`crm 8a032836 → 9d131f69` (re-stamped 2026-06-18 by the Stage-0 pastel split + `--brand-wash`; regenerated headlessly via `pnpm regen-spec`).

---

## Stage 0 (rollout-wide pre-req) — pastel SPLIT + contract amendments · 🟠 architect

Blocks Tracks A & C accents. **Fix render + registry + spec + generator together.** All registry /
design-studio changes are **German-merged**.

1. 🔵 **`design-studio` FIRST** (the playground is the source): in `SUB_BRANDS` set admisiones/crm
   light+dark accents to the **functional** values (`#ff3d63`/`#ff6b85`, `#e37600`/`#f59e3c`) and add a
   `wash?: {light,dark}` field holding the old pastels (`#FFE0E6`/`#FFB86B`); extend the `SubBrand`
   type + a `washOf()`; extend `buildSpec` to emit **both** the functional accent **and** the
   decorative `--brand-wash` (non-interactive). Otherwise a regenerated spec re-injects the pastel and
   `check-spec-drift` fires forever.
2. 🔵 **`registry/tokens.css`**: per `.theme-recepcion`/`.theme-clientes` — set the six functional
   slots to the functional values; add a **`--brand-wash`** token (pastel) wired into `@theme inline`;
   and **add the missing `.dark.theme-recepcion` (`#ff6b85`) / `.dark.theme-clientes` (`#f59e3c`)**
   blocks (today only the light `.theme-*` exists → dark de-brands to navy).
3. 🔵 **`registry/app/navigation/menu.example.ts` + `layouts/default.vue`**: amend the contract to a
   **`useMenu()` composable** the shell calls at render (replacing the static `menu` import), so apps
   return reactive auth-filtered nav (Decision 5). Update `CommandPalette` + `findAncestry` to consume it.
4. 🔵 **Registry breadcrumb bug**: `registry/app/components/ui/breadcrumb/{BreadcrumbEllipsis,BreadcrumbSeparator}.vue`
   import a non-existent `@lucide/vue` → change to `lucide-vue-next`. (Latent; fix before any app renders breadcrumb subcomponents.)
5. 🔵 **Regenerate** `admisiones.md`/`crm.md` via the headless `pnpm regen-spec` CLI (no browser); reconcile spec-versions + ledger.
6. 🔵 **Re-sync pharos-lis** + run its `shell-contract` → zero regression. Run `check-contrast`:
   `#ff3d63`/`#e37600` pass AA (5.30/4.91) **with the dark foregrounds — do NOT switch `--primary-foreground` to white** (would hard-fail). Confirm the new `.dark.theme-*` blocks pass too.

---

## Track A — admission-patient «Pacientes» (LEAD ROLLOUT TRACK · XL) · owner skuger

Repo root *is* the Nuxt app. **The srcDir migration is empirically proven green** (baseline build →
migrate → rebuild, 2345 modules, worktree-tested). Sync+shell+knobs is the next, not-yet-built step.

**Stage 1 · Adopt**
- 🔵 **srcDir migration (PROVEN RECIPE):** create `app/`; `git mv` into `app/` —
  `pages components layouts composables middleware plugins stores utils interfaces schemas services
  assets lib app.vue` (**`lib/` is required** — 13+ ui components import `~/lib/utils`; omitting it = hard vite ENOENT). **Leave at root:** `server/ nuxt.config.ts e2e/ playwright.config.* public/`.
  Then in `nuxt.config.ts`: **add `srcDir: "app"`** and change **`shadcn.componentDir → "./app/components/ui"`**.
  (`pinia.storesDirs` and `css: ['~/assets/...']` need **no** change — they follow srcDir; empirically confirmed.)
  `rm -rf node_modules/.cache/nuxt .output` then `pnpm nuxt build` → expect 2345 modules, zero WARN/ERROR.
  **Confirm `pnpm build` + `pnpm test:e2e` (the smoke spec) pass BEFORE touching the shell.**
- 🔵 **Dependency delta:** `pnpm add lucide-vue-next reka-ui && pnpm add -D @nuxt/fonts`; register
  `@nuxt/fonts` (4 families). The app has the *wrong* `@lucide/vue` + `radix-vue` v1 — decide whether they
  stay (used by existing pages) or go. Regenerate the lockfile.
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh .` from repo root (runs AFTER `app/` exists).
- 🟠 **color-mode:** `@nuxtjs/color-mode` is declared but **unregistered + unused** → nothing drives
  `.dark`. Register it (`classSuffix: ''`) and wire the shell toggle to `useColorMode()`, **or** confirm
  the synced shell ships its own `.dark`/localStorage wiring — escalate which.
- 🔵 **Manual follow-ups:** `@import` tokens + components CSS in `app/assets/css/main.css`; full 7-gate
  `lint-check`; merge `pre-commit.snippet.yaml`.
- 🔵 **Knobs:** `htmlAttrs.class: 'theme-recepcion'`, `title: 'Pacientes'`, favicon. `app/app.vue` →
  `<NuxtLayout glyph="Anchor" sub-name="Pacientes" sub-label="Admisiones · Recepción">`. `#user` →
  `SidebarUser` ← admission SSO store; `AppHeader` apps-switcher → `#topbar-end` (**re-wire its
  `useUser()` + the onMounted `applications` fetch — more than a literal knob**).
- 🟠 **nav (router is STRICT):** map the 8 `AdmisionSidebar` sections → `app/navigation/menu.ts` using
  the **exact PascalCase routes** (`/Scheduling /HandlePatient /Cajas …` — copy verbatim, do not re-derive).
  Pre-listed Iconify→Lucide substitutions for one-pass approval: `people-queue`, `waiting-room`,
  `assignment`, `user-management-settings`, `door→DoorOpen` (others map 1:1).
- 🟡 **Server type-import caution:** `server/api/accounting/build-pdf.post.ts` imports `~/interfaces/accounting`
  (type-only — build passed, erased). Run `nuxi typecheck` + hit the accounting route to confirm; if it
  resolves wrong, add a nitro alias or keep a shared type at root.

**Stages 2–5:** gates green → author `e2e/shell-contract.spec.ts` + the **`test:contract` script** (net-new,
mirror lab-qc) + CI job → **VERIFY** → deploy → sign-off + bump `admisiones.md`.

**VERIFY (A):** `pnpm lint-check` green · `pnpm build` (2345 mods) · screenshots L+D · expand a nav group
to an active leaf (rosa beam `#ff3d63` / dark `#ff6b85` + parent-group beam; `Anchor` glyph is `--primary`,
not gray) · `pnpm test:contract` green · `nuxi typecheck` clean · Minio `server/api/accounting/**` respond.

**Stage 6 · Retro Gate (handoff to B & C):** open the `retro-gate` PR — back-propagate every
transferable lesson into the **Track B & C** sections of this plan (the `retro-gate` check fails on an
empty downstream diff) + assert standard conformance; **#46 → #47/#48 blocked until German merges.** See §Retro Gate.

## Track B — finance-lch «Números» · owner egomez-lch

Nuxt 4, clean `app/` srcDir ✓, FE at `finance-lch/frontend`. No migration.

**Stage 1 · Adopt**
- 🔵 **Dependency delta:** `pnpm add -D @nuxt/fonts` + register it (the other shell deps are present).
  **Remove the Google-Fonts CDN `<link>`** (`nuxt.config.ts`) and the `VT323` `@import` (`main.css`) —
  both fail `check-font-allowlist`. Regenerate the lockfile.
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh frontend .` from repo root.
- 🔵 **Manual follow-ups** (Track-B's draft omitted these): `@import` `pharos-tokens.css` +
  `pharos-components.css` into `main.css`; replace `lint-check` with the full **7-gate** string;
  `@nuxt/eslint` + `nuxt prepare` postinstall (present); merge `pre-commit.snippet.yaml`.
- 🔵 **Replace** `app/layouts/default.vue` with the synced shell. Re-home the **currency-scale toggle**
  (old layout `useCurrencyScale()`) into a standalone `#topbar-end` component; `#user` → finance auth store.
  Set `titleTemplate: 'Pháros — %s'` (currently `'%s — LCH'`) + `htmlAttrs.class: 'theme-numeros'`.
- 🔵 **Retire cobol (full reconciliation, NOT a one-block delete):** delete the `:root[data-theme='cobol']`
  blocks + cobol `@import`; **convert the dark token block from `:root[data-theme='dark']` to `.dark`**
  (to match the shell's class mechanism); purge `VT323`/`Cutive Mono`/`Cascadia Code` from `--font-sans`;
  delete the dead `AppNavbar.vue`. **Keep the app's `--lch-*`/`--status-*` token layer** (charts +
  components depend on it) — `@import` the registry tokens *beside* it, do not replace wholesale.
- 🟠 **RBAC nav:** map the capability-gated nav → a `useMenu()` composable (Decision 5) that returns
  the `auth.can(...)`-filtered reactive tree to the shell. (Do **not** hand-roll a static pruned menu —
  it loses per-session reactivity.)
- 🟠 **Charts (FE only plots; backend owns stats):** keep `chart.js`; **do not delete `--lch-*`/`--status-*`**.
  `@unovis` migration is OUT of scope.

**Stages 2–5** as Track A (own shell-contract; tab `Pháros — Números`; bump `erp.md`).

**VERIFY (B):** lint-check green · build · screenshots L+D · active-leaf ámbar beam (`#7A5D00`/`#E6C34D`) ·
cobol gone · charts still colored · RBAC nav hides ungated items per user · `pnpm test:contract` green.

**Stage 6 · Retro Gate (handoff to C):** open the `retro-gate` PR — back-propagate into the **Track C**
section + assert conformance; **#48 blocked until German merges.** See §Retro Gate.

## Track C — commercial-lch «Clientes» · owner crincon04 · **M/High**

Nuxt 4, `app/` srcDir ✓, FE at `commercial-lch/frontend`. **Not** a blank slate.

**Stage 1 · Adopt**
- 🔵 **Dependency delta (all missing):** `pnpm add reka-ui @vueuse/core class-variance-authority clsx
  tailwind-merge lucide-vue-next` + `pnpm add -D @nuxt/fonts @playwright/test`. (`radix-vue` NOT needed —
  registry uses `reka-ui`.) Run `pnpm install` to regenerate + **commit the lockfile** (CI is `--frozen-lockfile`).
- 🔵 **Remove the Inter Google-Fonts CDN** `<link>` from `nuxt.config.ts` (`check-font-allowlist` fail);
  load the 4 fonts via `@nuxt/fonts`. (The Apax TTFs in `public/fonts/` are inert — fine.)
- 🟠 **Quotes-page rewrite (the bulk of the work):** rewrite `app/pages/quotes/{index,[id],new}.vue` raw
  `<input|select|table|button|textarea>` → shadcn `Input/Select/Table/Button/Textarea` (`check-no-raw-html`
  hard-fails otherwise). This is why C is M/High.
- 🔵 **Sync:** `<.github>/scripts/sync-pharos-registry.sh frontend .`. Rename `menu.example.ts` → `menu.ts`
  (the layout imports `~/navigation/menu`). Build `menu.ts` from the pages.
- 🔵 **Knobs:** `app.vue` wrap `<NuxtPage/>` in `<NuxtLayout glyph="Telescope" sub-name="Clientes"
  sub-label="CRM · Relaciones comerciales">`; `theme-clientes` (functional `#e37600` via Stage 0),
  `title: 'Clientes'`. `#user` → commercial auth store. Preserve `server/api/pdf-render.post.ts`.
- 🟠 **Depends on Stage 0** being merged + re-synced (theme-clientes still ships `#FFB86B` until then —
  do not hand-edit `tokens.css`).

**Stages 2–5:** e2e greenfield — add Playwright + config + `shell-contract.spec.ts` + `test-contract` job;
tab `Pháros — Clientes`; bump `crm.md`.

**VERIFY (C):** deps install `--frozen-lockfile` · lint-check green (incl. no-raw-html on rewritten pages) ·
build · screenshots L+D · active-leaf `#e37600` beam · `pdf-render` route intact · `pnpm test:contract` green.

**Stage 6 · Retro Gate (rollout close):** Track C is last — the retro records final lessons + confirms
standard conformance (no downstream back-prop). Closes the rollout. See §Retro Gate.

## RFC 0008 amendment (durable decisions — German merges)

The `2026-06-18` decisions block (branch `feat/0008-rollout-v2-decisions`) records the pastel-split rule,
the spec-name corrections, and the biuman deferral. **To add:** the **`useMenu()` nav-gating contract
amendment** (Decision 5) — the shared shell now exposes a reactive, app-filterable nav, enabling per-session
RBAC without per-app shell forks.

## Opus vs Sonnet — division of labor

- **Opus:** the locked decisions (done); the de-risk synthesis; review of every adaptation diff; the
  pastel-split values + dark accents; the RFC amendment; Stage-5 gating.
- **Sonnet (under Opus review):** the per-app digs, the proven srcDir `git mv`, dep deltas, knob-setting,
  `menu.ts`, the quotes-page rewrite, each `shell-contract.spec.ts`, CI jobs.

🛑 chart statistical parity stays the architect's call. Doc prose English; UI literals es-CO; code/DB English.
