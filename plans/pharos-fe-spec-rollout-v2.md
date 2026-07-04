---
status: in-progress
owner: gczuluaga
created: 2026-06-18
updated: 2026-06-30
issue: Interval-Col/.github#48
start: TBD
target: TBD
implementation: skuger (A), egomez-lch (B), crincon04 (C)
effort: XL
model: claude-sonnet-4-6
sources: [admission-patient, finance-lch, commercial-lch]
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# Pháros FE-spec rollout v2 — design system adoption across finance, admission, and commercial apps · Despliegue Pháros FE-spec v2 — adopción del sistema de diseño en finanzas, admisión y clientes

> **Resumen (ES).** Este plan ejecuta el despliegue del sistema de diseño Pháros (RFC 0008, Fases 1–3) sobre las tres apps pendientes: *Admisiones* (Track A, XL, `skuger`), *Finanzas* (Track B, M, `egomez-lch`) y *Clientes* (Track C, M/High, `crincon04`). El punto de referencia es `pharos-lis «Laboratorio»`, ya adoptado y verde. El modelo de trabajo son seis etapas (Adopt → Gate → Validate → Deploy → Sign-off → Retro Gate) donde la *Retro Gate* (Stage 6) es obligatoria y bloqueante entre pistas — German la fusiona, y solo ese acto desbloquea la siguiente. El Stage 0 actualiza el registro y los tokens antes de que cualquier pista arranque. Toda edición a archivos propios del registro se aplica vía el registro; nunca a mano.

## Pháros FE-spec rollout v2 — registry adoption across the 3 remaining apps

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

> **Markers** — ✅ **Done-when** (verifiable definition of done) · 🚦 **Checkpoint** (stop, show owner the named evidence) · 🛑 **HUMAN DECISION** (an agent must not pick this — escalate to owner) · 💡 **Heuristic** (a task-earned lesson) · 🔵 **Mechanical** (Sonnet-executable, no judgment required) · 🟠 **Escalate** (architect/owner decides, do not guess). *(ES: ✅ terminado-cuando · 🚦 punto de control · 🛑 decisión humana · 💡 heurística · 🔵 mecánico · 🟠 escalar al arquitecto.)*

> **Scope of this spine (RFC 0011 consolidation).** Three workstreams were folded into this single plan. Each has its own tracking issue:
> 1. **Shell rollout** ([#48](https://github.com/Interval-Col/.github/issues/48)) — Tracks A / B / C: design-system adoption in admission-patient, finance-lch, commercial-lch.
> 2. **Component library** ([#73](https://github.com/Interval-Col/.github/issues/73)) — RFC 0008 Phase-1 shared primitives (EntityLookup, SearchableSelect, useFlow, etc.).
> 3. **FE bloat gate** ([#70](https://github.com/Interval-Col/.github/issues/70)) — `check-fe-bloat.mjs` portfolio rollout.
>
> Originals archived under `plans/archive/` (RFC 0011). The three folded-in sections each carry a consolidation note — this block is the single top-level pointer.

## Status

- **Step 0 · pharos-lis «Laboratorio» — ✅ DONE (reference).** `lab-qc/frontend` on `develop @ 3b17aa8`:
  canonical shell, 6 fidelity fixes, reproducible spec (family `092fa725`, lis-clinico `52802ac5`),
  `shell-contract` CI gate green. **This is the pattern every track copies.**
- **Track A · admission-patient «Pacientes» — 🟡 IN PROGRESS · XL. Stage 1 Adopt DONE** (shell wired: nav/knobs/apps-switcher/bell; renders rosa light+dark; `pnpm build` green). **Stage 2 gate-fit DONE — 14/14 pages**: Pre-recepción · Inicio · Gestión médicos/pacientes · Estado de atención · Consultorios · Equipos · Plantillas de notificación · **Recepción** (whole intake flow: page + `PatientForm`/`ConfirmationPatientData`/`OrderCreation`/`OrderDemografic`/`CameraCapture` + the order sub-route) · **Toma de imágenes** (tablet-first capture page; 10 raw buttons → shadcn, tokens, tablet-responsive) · **Agenda** (whole `scheduling/` cluster: page + 12 components + shared colour maps; commit `c8cad86`) · **Gestión domicilios** (conformed for free by the Agenda cluster — page already clean, children done there) · **Cajas** (page + `cajas/CajaMaestra`/`CajaManagers` children; 57+27 child palette → 0, buttons/selects/text-inputs → shadcn, tables/textarea/number-inputs/checkbox + the entrega-destinatario select kept native; commit `b831bf1`) · **Horarios médicos** (page; raw buttons → role/Button + tokens; commit `4e5b561`). All 7 gates light+dark. **Scope learning: the colour gates scan components too → per-page conformance = page + its child components.** Styles only — functional fixes surfaced during the pass (patient-save 422 `null→""`, WS http-scheme for REST `$fetch`, dev caja bypass `import.meta.dev`-guarded) kept out of the style commits, tracked separately. Pushed on `feat/pharos-design-system` (`4e5b561..5602be3`). **Stage 2 «Gate» DONE (repo side) — all 7 gates GREEN:** `6770673` purged 20 dead legacy files (the `calendar/` cluster + old chrome + orphans, ~158 palette/hex hits), `1fd9366` conformed the live `SearchPatient`/`ProcessState`, `5789936` reverted the white `--primary-foreground` override → contrast AA + token-drift, `39ceacd` closed no-raw-html (vendored `ui/table`+`ui/textarea` primitives + converted tables/textarea/number-inputs), `68f63e0` wired Layer A (pre-commit `pharos-design-gates`) + Layer B (`lint-check` runs the 7 gates) mirroring pharos-lis. **Stage 3 «Validate» DONE (repo side, lean Layer-C):** `02a09ea` shell-contract e2e + `test:contract`, `d25cfb4` `test-contract` CI job + `devServer.port=5174`, `5602be3` Vitest alias/exclude fix (2 tests green). Layer-C kept **lean** — the deterministic contract test is the shell guard (no pixel baselines / no re-bless churn). **Remaining (owner/admin):** @gczuluaga flips `pharos-lint-check` to a required check + the `NUXT_PUBLIC_DEBUG_TOKEN` repo secret is set so the `test-contract` CI job authenticates. Then Stage 4 (Deploy) → 5 (Sign-off) → 6 (Retro Gate: open #47/#48).
- **Track B · finance-lch «Números» — ⬜.**
- **Track C · commercial-lch «Clientes» — ⬜. Re-scoped S→M/High (raw-HTML rewrite + all deps missing).**
- **biuman-lis «Movimiento» (antes «Deportivo») — DEFERRED** (out of scope; RFC 0008 Phase 3, separate plan).

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

## The model — 6-stage deployable track

A Sonnet agent carries stages **1–3**; the owner/architect carries **4–5**, then the Retro Gate (Stage 6) closes the track.

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

> Consolida pharos-enforcement-setup.md (RFC 0011; originales archivados en plans/archive/).

> ⚠️ **Gap found by the de-risk recon: `pharos-lint-check` is NOT a required check in *any* target
> repo today** (it's 404 in all three) — so the design-system standard is currently **unenforced at
> CI**. These steps arm it; the Retro Gate then verifies the *next* repo is armed before each handoff.
> Run by the org admin (@gczuluaga) only. Confirm exact context strings from a live run before adding them as required checks.

**A. One-time, before Track A**

- [x] Merge the v2 plan PR (includes `retro-gate.yml`) + the RFC PR. *(done — `retro-gate.yml` confirmed in `.github/workflows/`, plan on origin/main; 2026-06-18)*
- [x] Create labels: *(done — labels created for all listed repos; 2026-06-18)*
  ```sh
  gh label create retro-gate -R Interval-Col/.github -c 5319e7 -d 'Pháros track handoff (Retro Gate) PR'
  for r in admission-patient finance-lch commercial-lch; do
    gh label create blocked:retro-gate -R "Interval-Col/$r" -c b60205 -d 'Blocked: awaiting prior track Retro Gate'
  done
  ```
- [x] **Register `retro-gate` as a required check on `.github` `main`** — after the workflow has run once on a `retro-gate`-labeled PR. Confirm the exact context name (`Pháros — retro-gate` / `retro-gate`) from that run, then add it to required checks (keep `gitleaks`). 🛑 Confirm exact context string before setting required. *(done — required check registered; 2026-06-22)*
- [x] Parity: enable `dismiss_stale_reviews` on `commercial-lch` `main`; add `@SKuger01` to `admission-patient` CODEOWNERS (frontend paths, via PR). *(done — 2026-06-22)*

✅ **Done-when (A):** labels exist in all listed repos; `gh api repos/Interval-Col/.github/branches/main/protection --jq '.required_status_checks.contexts'` lists the `retro-gate` context; `gh api repos/Interval-Col/commercial-lch/branches/main/protection --jq '.required_pull_request_reviews.dismiss_stale_reviews'` returns `true`; a PR against `admission-patient` touching frontend paths auto-assigns `@SKuger01`.

**B. Per-track — during each track's Stage 1–2 (once `pharos-lint-check.yml` is synced)**

- [ ] **(admission-patient)** After `pharos-lint-check.yml` reports at least once on `develop`: confirm exact context string from that run, then add `Pháros — lint-check` to required status checks on **both `develop` and `main`** — alongside existing `gitleaks` + repo required checks; do not remove them.
- [ ] **(finance-lch)** Same as above for Track B.
- [ ] **(commercial-lch)** Same as above for Track C.

> Required checks on `develop` block even direct pushes — the load-bearing lever (per `BRANCHING-AND-DEPLOY.md`). The Retro Gate's STANDARD-conformance step verifies the next repo is armed before each handoff.

✅ **Done-when (B, per repo):** `gh api repos/Interval-Col/<repo>/branches/develop/protection --jq '.required_status_checks.contexts'` and same for `main` both list the `pharos-lint-check` context alongside `gitleaks` and the prior required checks.

**C. Deferred — `enforce_admins`**

- [ ] Once a real second code-owner exists in the org: turn ON `enforce_admins` for `Interval-Col/.github` `main` so even an admin cannot merge a red `retro-gate` check. **Leave OFF until then** (keeps the `gh pr merge --admin` solo-merge flow). 🛑 Activation decision logged with date when triggered.

## Corrected spec values — live `registry/spec/*`

| Sub-brand | spec-ver | theme class | `--primary` light / **dark** | glyph | subLabel | sub-name | Intensidad | tab |
|---|---|---|---|---|---|---|---|---|
| **Números** (erp) | `5c38266d` | `theme-numeros` | `#7A5D00` / `#E6C34D` | `ShipWheel` | `ERP · Finanzas y operaciones` | Números | **Sutil** | `Pháros — Números` |
| **Clientes** (crm) | `9d131f69` | `theme-clientes` | fn `#e37600` / **`#f59e3c`** · wash `#FFB86B` | `Telescope` | `CRM · Relaciones comerciales` | Clientes | **Neutro** | `Pháros — Clientes` |
| **Pacientes** (admisiones) | `94b02840` | `theme-recepcion` | fn `#ff3d63` / **`#ff6b85`** · wash `#FFE0E6` | `Anchor` | `Admisiones · Recepción` | **Pacientes** | Neutro | `Pháros — Pacientes` |

Ledger bumps on Stage-5 sign-off: `admisiones 091d6523 → 94b02840` · `erp 8be5e785 → 5c38266d` ·
`crm 8a032836 → 9d131f69` (re-stamped 2026-06-18 by the Stage-0 pastel split + `--brand-wash`; regenerated headlessly via `pnpm regen-spec`).

---

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que se repiten en este plan, con su traducción y una línea de qué significan en contexto. Si hay un término del plan que no está aquí, pregúntale al agente — no es una falla tuya.

| English | Español | Means |
|---|---|---|
| design token | token de diseño | CSS custom property (e.g. `--primary`, `--brand-wash`) owned by the registry, consumed by the app |
| registry | registro | The `.github` shell + token package — source of truth for tokens, components, gates, and sync scripts |
| shell | cáscara / shell de navegación | The shared Nuxt layout (`layouts/default.vue`) + nav primitives synced from the registry into each app |
| srcDir migration | migración de srcDir | Moving Nuxt source files under `app/` so `nuxt.config.ts` sets `srcDir: "app"` |
| spec-drift | deriva de especificación | Divergence between registry spec and the app's live token values; detected by `check-spec-drift` |
| lint-check | chequeo de gates | The `pharos-lint-check.yml` CI workflow that runs the 7 design-system gates on every PR |
| lockfile | archivo de bloqueo | `pnpm-lock.yaml` — must be committed and current; CI runs `pnpm install --frozen-lockfile` |
| Retro Gate | gate retrospectivo | Mandatory PR between one track's Stage 5 and the next track's start; back-propagates lessons |
| gate-fit | ajuste al gate | Pre-Stage-2 work to remove forbidden raw HTML elements and non-allowlisted font CDNs |
| sub-brand | sub-marca | Per-app theme variant (e.g. `theme-recepcion`, `theme-numeros`, `theme-clientes`) |
| Layer A/B/C/D | capa A/B/C/D | Gate layers: A = pre-commit hook; B = CI lint-check; C = shell-contract e2e; D = drift/contrast/font |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este plan — está diferido o corresponde a otro RFC o equipo. Si un agente sugiere construir algo de esta lista, no lo hagas.

- **biuman-lis «Movimiento»** (antes «Deportivo») — deferred to RFC 0008 Phase 3; separate plan.
- **@unovis charts migration (Track B)** — out of scope; keep `chart.js` and the `--lch-*`/`--status-*` token layer intact.
- **Real backend integration in Stages 1–3** — mock-first; backend wired only at Stage-5 owner sign-off.
- **Pixel-level visual baselines** — no Chromatic/Percy; Layer-C is lean (deterministic shell-contract only, no bless churn).
- **Design-studio playground UI changes beyond Stage-0 spec** — registry tooling maintenance; not an app-facing track.
- **SSO/auth backend changes** — apps wire their existing auth stores into the shell; this plan does not touch auth logic.

---

## Stage 0 (rollout-wide pre-req) — pastel SPLIT + contract amendments · 🟠 architect

> **Status: ✅ DONE — merged (2026-06-18); pharos-lis shell-contract green after re-sync. Track A / B / C may proceed.**

> **Resumen (ES) — Stage 0: Pre-requisito global del rollout.**
>
> Actualiza la fuente de verdad (design-studio, `tokens.css`, contratos) antes de que cualquier track arranque. Los Tracks A y C están bloqueados en sus acentos de color hasta que este stage se fusione. Todas las fusiones del registro las aprueba y fusiona German.
>
> En orden, las tareas:
>
> 1. **0.1** — Actualizar `design-studio` con los valores funcionales y el campo `wash` para los acentos pastel.
> 2. **0.2** — Actualizar `registry/tokens.css`: slots funcionales, `--brand-wash`, y bloques `.dark.theme-recepcion`/`.dark.theme-clientes` faltantes.
> 3. **0.3** — Enmendar el contrato de navegación a un composable `useMenu()` (Decisión 5).
> 4. **0.4** — Corregir el bug de `@lucide/vue` → `lucide-vue-next` en los componentes de breadcrumb del registro.
> 5. **0.5** — Regenerar `admisiones.md`/`crm.md` via `pnpm regen-spec` y reconciliar versiones y ledger.
> 6. **0.6** — Re-sincronizar `pharos-lis`, correr `shell-contract` y `check-contrast`; cero regresiones.
>
> Decisión humana: German aprueba y fusiona todos los cambios del registro.

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

✅ **Done-when:** `design-studio` emits functional accents + `--brand-wash` without re-injecting pastels on regen. `tokens.css` has both `.dark.theme-recepcion` (`#ff6b85`) and `.dark.theme-clientes` (`#f59e3c`) blocks. `useMenu()` composable contract is in `registry/app/navigation/menu.example.ts` and `layouts/default.vue`. `pharos-lis` `shell-contract` CI is green after re-sync. `check-contrast` passes for `#ff3d63`/`#e37600` with dark foregrounds. *(ES: registry fusionado; pharos-lis en cero regresiones; check-contrast verde; bloques `.dark.theme-*` presentes.)*

🚦 **Checkpoint 0.** Show @gczuluaga: (1) the merged Stage-0 PR diff with new `.dark.theme-*` blocks and `--brand-wash` token visible; (2) `pharos-lis` `shell-contract` CI run green after re-sync.

---

## Track A — admission-patient «Pacientes» (LEAD ROLLOUT TRACK · XL) · owner skuger

> **Resumen (ES) — Track A: Adopción en admission-patient «Pacientes» (lead track).**
>
> El track más difícil y el primero en ejecutarse: migración de srcDir probada, sincronización del shell, conformance de 14 páginas con todos sus componentes hijo, y armado de la gate de CI como check requerido. Solo termina cuando la Retro Gate (Stage 6) es fusionada por German, desbloqueando los Tracks B y C.
>
> En orden, las etapas:
>
> 1. **Stage 1 (Adopt)** — Migración de srcDir a `app/`, delta de dependencias, sync del registro, wiring de color-mode y knobs, mapeo del nav con rutas exactas del router.
> 2. **Stage 2 (Gate)** — Gate-fit en 14 páginas + componentes; Layers A, B y D verdes.
> 3. **Stage 3 (Validate)** — Shell-contract e2e + script `test:contract` + job CI verde.
> 4. **Stage 4 (Deploy)** — `ci-cd.yml` owner-gated.
> 5. **Stage 5 (Sign-off)** — Owner valida contra backend real; bump de `admisiones.md`.
> 6. **Stage 6 (Retro Gate)** — PR con lecciones back-propagadas a B y C; German fusiona; #47/#48 desbloqueados.
>
> Decisiones humanas: wiring de color-mode (🟠 Stage 1); mapeo de nav a rutas exactas del router (🟠 Stage 1).

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

✅ **Done-when:** All VERIFY (A) criteria are literally true and verified in the browser. `pharos-lint-check` is registered as a required check on `develop` and `main` in the `admission-patient` repo. Stage-6 Retro Gate PR is merged by @gczuluaga with the `retro-gate` CI check green and non-empty downstream Track B/C diffs in the plan. *(ES: todos los VERIFY verdes y verificados; gate registrado como required; Retro Gate fusionada por German.)*

🚦 **Checkpoint A.** Show @gczuluaga: (1) `pnpm lint-check` green log; (2) browser screenshots light + dark with rosa beam (`#ff3d63`) and Anchor glyph visible; (3) `pnpm test:contract` green CI run URL; (4) the Retro Gate PR URL showing non-empty Track B/C downstream diff.

**Stage 6 · Retro Gate (handoff to B & C):** open the `retro-gate` PR — back-propagate every
transferable lesson into the **Track B & C** sections of this plan (the `retro-gate` check fails on an
empty downstream diff) + assert standard conformance; **#46 → #47/#48 blocked until German merges.** See §Retro Gate.

## Track B — finance-lch «Números» · owner egomez-lch

> **Resumen (ES) — Track B: Adopción en finance-lch «Números».**
>
> App Nuxt 4 con srcDir ya migrado — sin migración de carpetas. El trabajo principal: retirar el tema `cobol`, reconciliar el bloque de tokens `.dark`, añadir `@nuxt/fonts`, sincronizar el shell, y mapear el nav RBAC con el composable `useMenu()`. Comienza solo cuando la Retro Gate del Track A está fusionada.
>
> En orden, las etapas:
>
> 1. **Stage 1 (Adopt)** — Delta de dependencias, sync del registro, reemplazo del layout, retiro completo del tema cobol, wiring de `useMenu()` para el nav RBAC.
> 2. **Stage 2 (Gate)** — Gate-fit; 7 gates verdes preservando la capa de tokens `--lch-*`/`--status-*`.
> 3. **Stage 3 (Validate)** — Shell-contract e2e + script `test:contract` + job CI verde.
> 4. **Stage 4 (Deploy)** — `ci-cd.yml` owner-gated.
> 5. **Stage 5 (Sign-off)** — Owner valida contra backend real; bump de `erp.md`.
> 6. **Stage 6 (Retro Gate)** — Back-propagation de lecciones a Track C; German fusiona; #48 desbloqueado.
>
> Decisión humana: wiring de `useMenu()` con la lógica RBAC existente de finance (🟠).

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

**🔁 Carried from Track A's retro** ([`archive/pharos-track-retro.A.md`](archive/pharos-track-retro.A.md)):
- **Gate-fit = page *+ its components* for colours** — the colour gates scan all of `app/`, not just `pages/` (`no-raw-html` scans only `pages/`/`layouts/`). **Purge dead/legacy components first** (verify 0 refs repo-wide + build-green) before tokenizing — Track A cleared ~158 hits by deleting ~20 dead files.
- ⚠️ **shadcn `<Input>` drops the `v-model.number` modifier** — **critical here, finance is number-heavy**: bind `:model-value` + `@update:model-value="x = Number($event)"`, else amounts become strings and `money()`/math break.
- **`ui/` may lack `Table`/`Textarea`** — vendor thin pass-through primitives to close `no-raw-html` on data tables.
- **e2e auth (SSR):** if finance auth runs server-side, the headless `shell-contract` can't auth in CI (no SSO → logout → no shell). Plan a test/dev auth path (an `import.meta.dev`-guarded bypass or a mock-SSO) **before** wiring `test-contract`.
- **Tooling:** set `nuxt.config.devServer.port` (else the Playwright webServer hangs); point vitest `~`/`@` → `app/` + `exclude: e2e`; **Node 22+** (eslint 10 crashes on Node ≤20). On sync, **drop `packageManager`** (or pin it to the workflow's pnpm version) — `pnpm/action-setup@v4` errors on a mismatch.
- **Visual cohesion (conform, don't patch — gates green ≠ done):** no stray/half-tokenized styles · **no double-sidebar/double-chrome** (side panels = in-flow `<aside>` at page level, never covering the shell nav; full-bleed `-m-6 h-[calc(100%+3rem)]`) · re-check **dark mode** end-to-end (alternating row bg → divider rows) · no stray vertical scroll · breadcrumb-as-title (no duplicated `<h1>`) · status→badges · drop gratuitous shadows · align popovers (`align="end"`).

**Stages 2–5** as Track A (own shell-contract; tab `Pháros — Números`; bump `erp.md`).

**VERIFY (B):** lint-check green · build · screenshots L+D · active-leaf ámbar beam (`#7A5D00`/`#E6C34D`) ·
cobol gone · charts still colored · RBAC nav hides ungated items per user · `pnpm test:contract` green.

✅ **Done-when:** All VERIFY (B) criteria are literally true and verified in the browser. Cobol theme fully retired — no `:root[data-theme='cobol']` blocks remain. `--lch-*`/`--status-*` token layer intact and charts still colored. `pharos-lint-check` registered as required on `develop`/`main`. Stage-6 Retro Gate PR merged with non-empty Track C downstream diff. *(ES: VERIFY verde; cobol retirado; charts intactos; gate required; Retro Gate fusionada.)*

🚦 **Checkpoint B.** Show @gczuluaga: (1) build green; (2) browser screenshots light + dark with ámbar beam (`#7A5D00`/`#E6C34D`); (3) RBAC nav hiding an ungated section for a test user; (4) `pnpm test:contract` green CI run URL; (5) Retro Gate PR URL with non-empty Track C downstream diff.

**Stage 6 · Retro Gate (handoff to C):** open the `retro-gate` PR — back-propagate into the **Track C**
section + assert conformance; **#48 blocked until German merges.** See §Retro Gate.

## Track C — commercial-lch «Clientes» · owner crincon04 · **M/High**

> **Resumen (ES) — Track C: Adopción en commercial-lch «Clientes».**
>
> App Nuxt 4 con srcDir ya migrado. El trabajo más distintivo es la reescritura de las páginas de cotizaciones (HTML crudo → primitivas shadcn) y la instalación del conjunto completo de dependencias del shell (todas ausentes hoy). Comienza solo cuando la Retro Gate del Track B está fusionada.
>
> En orden, las etapas:
>
> 1. **Stage 1 (Adopt)** — Delta completo de dependencias, retirar Google Fonts CDN, reescritura de páginas de cotizaciones (`quotes/{index,[id],new}.vue`), sync del registro, knobs.
> 2. **Stage 2 (Gate)** — Gate-fit; 7 gates verdes incluyendo `no-raw-html` sobre las páginas reescritas.
> 3. **Stage 3 (Validate)** — Playwright greenfield + shell-contract + job `test-contract` CI verde.
> 4. **Stage 4 (Deploy)** — `ci-cd.yml` owner-gated.
> 5. **Stage 5 (Sign-off)** — Owner valida contra backend real; bump de `crm.md`.
> 6. **Stage 6 (Retro Gate de cierre)** — Documenta lecciones finales; confirma conformance estándar; cierra el rollout.
>
> Decisión humana: si el alcance de la reescritura supera `quotes/{index,[id],new}.vue`, escalar a @gczuluaga antes de continuar (🟠).

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

**🔁 Carried from Track A's retro** ([`archive/pharos-track-retro.A.md`](archive/pharos-track-retro.A.md)):
- ⚠️ **`#e37600` (ámbar) white-on-accent trap** — forcing white button text on the ámbar accent **fails the contrast gate** (white-on-ámbar < AA 4.5) **and** drifts the registry-owned `tokens.css`. Keep the **registry foreground**; **never hand-edit `tokens.css`**. (Track A hit this exact trap with rosa `#ff3d63` — reverted the white override to green contrast + drift.)
- **Quotes-page rewrite = *vendor* `Table`/`Textarea` primitives, not just rename** — the `ui/` set likely lacks them (thin pass-through wrappers close `no-raw-html`). And **shadcn `<Input>` drops `v-model.number`** → quote amounts become strings; use `:model-value` + `@update:model-value` with `Number()`.
- **Gate-fit = page *+ its components* for colours**; **purge dead/legacy first** (0 refs + build-green).
- **e2e auth (SSR):** plan a test/dev auth path (an `import.meta.dev`-guarded bypass or mock-SSO) **before** wiring `test-contract` — SSR auth can't be mocked headlessly (no SSO in CI → logout → no shell).
- **Tooling:** set `nuxt.config.devServer.port`; vitest `~`/`@` → `app/` + `exclude: e2e`; **Node 22+**; on sync **drop `packageManager`** (pnpm-version mismatch breaks `pnpm/action-setup@v4`).
- **Visual cohesion (conform, don't patch — gates green ≠ done):** no stray styles · **no double-sidebar/double-chrome** (in-flow `<aside>` at page level, full-bleed, never covering the shell nav) · **dark mode** end-to-end (divider rows, not alternating bg) · no stray vertical scroll · breadcrumb-as-title · status→badges · drop gratuitous shadows · align popovers (`align="end"`).

**Stages 2–5:** e2e greenfield — add Playwright + config + `shell-contract.spec.ts` + `test-contract` job;
tab `Pháros — Clientes`; bump `crm.md`.

**VERIFY (C):** deps install `--frozen-lockfile` · lint-check green (incl. no-raw-html on rewritten pages) ·
build · screenshots L+D · active-leaf `#e37600` beam · `pdf-render` route intact · `pnpm test:contract` green.

✅ **Done-when:** All VERIFY (C) criteria are literally true and verified in the browser. No raw `<input|select|table|button|textarea>` in `pages/`. `pdf-render` route responds correctly. `pharos-lint-check` registered as required on `develop`/`main`. Stage-6 Retro Gate PR merged, rollout officially closed. *(ES: VERIFY verde; sin raw HTML; pdf-render funcional; rollout cerrado y conformance confirmada.)*

🚦 **Checkpoint C.** Show @gczuluaga: (1) `pnpm install --frozen-lockfile` green; (2) browser screenshots light + dark with ámbar (`#e37600`) beam; (3) a rewritten quotes page functional in the browser (shadcn components, no raw HTML); (4) `pnpm test:contract` green CI run URL; (5) Stage-6 Retro Gate PR merged — rollout officially closed.

**Stage 6 · Retro Gate (rollout close):** Track C is last — the retro records final lessons + confirms
standard conformance (no downstream back-prop). Closes the rollout. See §Retro Gate.

## Component library rollout — shared FE primitives (RFC 0008 Phase-1 follow-up)

> Consolida pharos-component-library-rollout.md (RFC 0011; originales archivados en plans/archive/).

> **Resumen (ES).** Este bloque cierra el único ítem abierto que dejó la RFC 0008: **la biblioteca de componentes compartida** (RFC 0008 §5). No es una nueva RFC — es una enmienda a RFC 0008 + ejecución. Complementa el rollout del *shell* (arriba); este bloque despliega los *componentes dentro del shell*. El mecanismo de distribución es el mismo copy-in (`sync-pharos-registry.sh`). `admission-patient` es el primer consumidor. Tracking: Interval-Col/.github#73. Phases 0–3 **DONE**; Phase 4 = siguiente.

> **Status (2026-06-28).** Phases 0–3 DONE: 8 primitivas + 2 composables prototipados en `design-studio` y promovidos al registro (PR #77, mergeado). Registro de iconos expandido a ~94 claves (icon cross-check). **Phase 4 next**: adopción en `admission-patient` (`admission-patient/plans/pharos-component-adoption-plan.md`, tracking #80). La sesión de co-creación (ratificar APIs) corre en paralelo. El set creció de 7 a 8 primitivas — `DatePicker` fue añadido para el flujo cédula-scan prereception.

### Component library — decisions locked (German, 2026-06-28)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Where the standard lives | **Elevate to RFC 0008** (org-wide). 3 layers: RFC amendment (decision) · registry (implementation + distribution) · this plan (execution). |
| 2 | Build venue | **Co-create in `design-studio`** (the playground), not a per-app PoC branch. |
| 3 | Sequencing | **Foundations → Flow → Rest** (lookup/select/shell → flow/back-nav → fetch/form). |
| 4 | Icon collection | **Lucide (house) + Material Symbols Outlined** (one governed clinical fallback). |
| 5 | Icon mechanism | **One shared `<Icon>` tag** (`@iconify/tailwind` CSS classes underneath; collection-agnostic). |
| 6 | design-studio → registry promote path | **Build `promote-to-registry` script FIRST** (Phase 0). |
| 7 | Extraction source per primitive | **Best-in-class per pillar** (evidence-based 3-app maturity comparison — see extraction matrix below). |

> 🛑 Four open sub-decisions (Phase 3–4): fetch-codegen mandate · FormField validation binding · gate posture (per-primitive vs consolidated) · `useFlow` persisted-state migration.

### Per-pillar extraction matrix

| # | Pillar | Best source | Key note |
|---|--------|-------------|----------|
| 1 | **EntityLookup** (+ PatientLookup/PhysicianLookup presets) | admission-patient `SearchPatient`/`usePatientSearch` | rebuild on finance-lch shadcn Combobox substrate |
| 2 | **SearchableSelect** | **finance-lch** reka-ui Combobox family | graft admission-patient `PhysicianCombobox` behavior; handle empty/null `v-model` natively (no `NONE_*` sentinel) |
| 3 | **PageShell + PageHeader** | PageShell = registry sync (already org-owned); **lab-qc** canonical ref | PageHeader is net-new; add full-bleed slot/CSS var to kill `-m-6` hack |
| 4 | **useAsyncState + fetch** | **finance-lch** `apiFetch` + error normalizer; lab-qc `useApi()` shape for component-facing layer | |
| 5 | **FormField** (label + control + error) | **Net-new** in design-studio | vee-validate + @vee-validate/zod + toTypedSchema convention |
| 6 | **useFlow** (back-stack + dialog-state) | admission-patient `useProcessState` | generalize: steps as config, not hardcoded Paciente/Orden |
| 7 | **Icon standard** (`<Icon>` wrapper) | finance-lch / lab-qc Lucide-only baseline | admission-patient migrates 18-collection/149-usage sprawl → Lucide + Material Symbols |
| 8 | **DatePicker** | Net-new | Added for prereception cédula-scan birthdate flow |

### CL Phase 0 — Charter the library + build the promote path · 🟠 architect

- [x] **0.1** — Author the RFC 0008 amendment block (7+1 primitives as Phase-1 library; API-intent contracts; composables convention; icon standard).
- [x] **0.2** — Record that `useFlow` + `useAsyncState` extend the registry's existing composables convention (`useHealthBeacon` is the live precedent).
- [x] **0.3** — Build + test the **`promote-to-registry` script** (design-studio → registry; dry-run first; @gczuluaga gates the registry PR it produces).
- [x] **0.4** — Create per-primitive **design-intent stubs** in `registry/surfaces/` using the `finanzas.md` template.
- [x] **0.5** — File the board issue (Interval-Col/.github#73); update frontmatter `issue:`.

🛑 **HUMAN DECISION (open):** promote-script automation scope — manual-assisted vs fully automated. Recommend manual-assisted v1.

✅ **Done-when (CL Phase 0):** RFC 0008 amendment merged by @gczuluaga; `promote-to-registry --dry-run <primitive>` prints correct `registry/app/**` paths; surface stubs exist per primitive. *(DONE — PR #77 merged.)*

### CL Phase 1 — Foundations: EntityLookup · SearchableSelect · PageShell/PageHeader · Icon wrapper

- [x] **1.1** — Prototype **SearchableSelect** in design-studio (reka-ui Combobox + PhysicianCombobox behavior; empty/null `v-model` natively; land in `registry/app/components/ui/`).
- [x] **1.2** — Prototype **EntityLookup** on SearchableSelect (PatientLookup + PhysicianLookup presets).
- [x] **1.3** — **PageHeader** (title + toolbar/actions slots; shell-level full-bleed slot/CSS var); document **PageShell** from lab-qc as canonical reference; settle one page-title mechanism.
- [x] **1.4** — Build **`<Icon>` wrapper** in design-studio + land in registry; rewrite `registry/frontend-standards.md` §Iconos.
- [x] **1.5** — Add **`design-studio/app/pages/componentes/iconos.vue`** — live catalog (Lucide + allowlisted Material Symbols, all three sizes, copy-to-clipboard).
- [x] **1.6** — Add first adoption gates in **WARN** (e.g. `check-no-raw-combobox.mjs`); verify `sync --dry-run` mirrors new SFCs.

✅ **Done-when (CL Phase 1):** 3 SFCs + `<Icon>` in `registry/app/components/(ui/)`; @gczuluaga merged. design-studio showcases render light + dark + rosa accent, browser-verified. `sync --dry-run` shows SFCs at correct paths. New gates green in WARN. *(DONE.)*

### CL Phase 2 — Flow: useFlow (back-stack + dialog-state composable)

- [x] **2.1** — Prototype **useFlow** in design-studio (arbitrary back-stack + dialog-state; steps as config; `goNext`/`goBack`/`resetSteps`/`setStepStatus`/persist; `v-model:open` for dialogs).
- [x] **2.2** — Land **`registry/app/composables/useFlow.ts`** alongside `useHealthBeacon`; surface doc; settle orders/create's identity in the showcase.
- [x] **2.3** — Sanity-check `sync --dry-run` mirrors `useFlow.ts` into a consumer.
- [x] **2.4** — Decide SSR-safety + persistence (`skipHydrate`).

🛑 **HUMAN DECISION (open):** in-flight persisted-state migration for `useProcessState` → `useFlow` (key remap vs one-time reset) — confirm before Phase 4 adoption.

✅ **Done-when (CL Phase 2):** `useFlow.ts` in registry, merged by @gczuluaga; `sync --dry-run` shows composable path; design-studio drives Recepción intake back-nav with useFlow, browser-verified. *(DONE.)*

### CL Phase 3 — The rest: useAsyncState + FormField

- [x] **3.1** — Land **`registry/app/composables/useAsyncState.ts`** (`{data, status, loading, error, isEmpty, refresh}`; AbortController + stale-response guard; camelCase FE / snake_case BE; `useAsyncData` for idempotent reads, wrapper for mutations).
- [x] **3.2** — Build **`FormField.vue`** (+ `FormItem` context; label + control slot + inline error; vee-validate + @vee-validate/zod + toTypedSchema convention). Land in registry.
- [x] **3.3** — Add optional adoption gates in WARN (e.g. `check-formfield-usage`); update `registry/frontend-standards.md` "Naming de componentes" from "Fase-1 follow-up" to **"shipped."**

🛑 **HUMAN DECISION (open):** fetch-codegen mandate — does `useAsyncState` require generated typed client, or only the wrapper? Recommend wrapper now, codegen separate.
🛑 **HUMAN DECISION (open):** FormField validation binding — `vee-validate`-bound vs validation-agnostic.

✅ **Done-when (CL Phase 3):** `useAsyncState.ts` + `FormField.vue` in registry, merged by @gczuluaga; `frontend-standards.md` says "shipped"; all new gates green (WARN). *(DONE — PR #77 merged.)*

### CL Phase 4 — Adopt in admission-patient (first consumer) + flip gates to hard-fail

> Next executable step (tracking: admission-patient#80).

- [ ] **4.1** — Re-sync admission-patient (`scripts/sync-pharos-registry.sh .`) — picks up all 8 primitives + composables. Confirm `--dry-run` shows **zero hand-edits** to registry-owned files.
- [ ] **4.2** — Refactor app-local duplicates onto registry primitives: delete `PhysicianCombobox`/`SearchPatient` internals → `EntityLookup`/`SearchableSelect`; point Recepción intake/queue + `PatientForm`/`PhysicianForm` at `FormField`/`PageHeader`; `useProcessState` → `useFlow` (apply persisted-state migration decision).
- [ ] **4.3** — Introduce **central fetch wrapper** (`useAsyncState`/`apiFetch`): admission-patient is the outlier (37 composables, no wrapper). Validates the fetch primitive against the most complex consumer.
- [ ] **4.4** — Migrate **icon sprawl**: 18 collections / 149 usages → Lucide + Material Symbols via `<Icon>`. Extend `check-fe-bloat` to ban `@nuxt/icon` and (post-migration) `lucide-vue-next` as a render path; add `registry/scripts/check-icon-collections.mjs` (allowlist = lucide + material-symbols). Standardize all three apps onto 8 gates.
- [ ] **4.5** — **Flip new gates WARN → hard-fail** once lead consumer conforms. Append a supplement note to `archive/pharos-track-retro.A.md` (see note below) so tracks B/C inherit the primitives on their next sync.

  > **Note (retro doc location):** `pharos-track-retro.A.md` lives at `plans/archive/pharos-track-retro.A.md`. To keep it editable, either un-archive it back to `plans/` via a PR, or append the component-library carry-forward as a dated supplement section directly in the archive copy.

> 💡 Copy-in distribution means a primitive defect propagates to every app at once. Treat admission-patient **dev** as the canary; keep version/changelog discipline on registry PRs; never flip a gate to hard-fail before the canary is green.

✅ **Done-when (CL Phase 4):** `pnpm build` + existing design-gate + E2E smoke green in admission-patient with new primitives wired. `sync --dry-run` shows zero hand-edits to registry-owned files. New gates **hard-fail** and `pharos-lint-check` green including them; all three apps run 8 gates. HandlePatient and HandlePhysician visibly converged in the browser, verified by @gczuluaga. Retro doc back-propagates to B/C.

🚦 **Checkpoint CL4 (exit).** Show @gczuluaga: admission-patient in the browser (two lookup pages converged; searchable dropdowns; consistent icons; multi-step flow with working back path); green `lint-check` with hard-fail gates; `sync --dry-run` zero-diff. Walk a full Recepción flow live (forward + back; no state lost).

---

## FE dependency-hygiene gate (`check-fe-bloat`) — portfolio rollout

> Consolida fe-bloat-gate-plan.md (RFC 0011; originales archivados en plans/archive/).

> **Resumen (ES).** Compuerta de CI mandatoria (`check-fe-bloat.mjs`), sincronizada del registry Pháros y encadenada en `lint-check`, que previene el bloat de dependencias FE. Phase 1 **DONE** (ya en registro y en admission-patient PR #53). Tracking: Interval-Col/.github#70.

### FE-bloat Phase 1 — Deterministic rules (monolith ban + one-lib-per-category) · DONE

- [x] **B1.1** — `check-fe-bloat.mjs` in the registry: bans `@iconify/json`; enforces one library per "same-purpose" category (Lucide-for-Vue; Radix/Reka headless-UI); tiny justified `ALLOWLIST`. Zero false-positives.
- [x] **B1.2** — Wire into `lint-check`: add to `sync-pharos-registry.sh`'s canonical chain; the sync loop copies all `check-*.mjs`.
- [x] **B1.3** — Document in `registry/frontend-standards.md` (§ Higiene de dependencias).
- [x] **B1.4** — Adopt in admission-patient as proving ground (PR #53): script + `lint-check`. Verified: passes on clean tree, fails on original (`@iconify/json` + 2 dup categories).

✅ **Done-when (B1):** gate in registry + chain, documented, and green in admission-patient. *(DONE.)*

### FE-bloat Phase 2 — Dead-dependency detection (`knip`)

- [ ] **B2.1** — Add `knip` (replacing stray unused `depcheck` in `telemetry`) with shared base config in the registry; per-app `knip.json` for overrides.
- [ ] **B2.2** — 🛑 **HUMAN DECISION:** tune the allowlist per app until zero false-positives, then decide warn-vs-fail. knip flags runtime-only / type-only / config-only deps that are NOT dead — these need an allowlist before the gate can block merges.
- [ ] **B2.3** — Chain into `lint-check` once per-app allowlist is clean.

✅ **Done-when (B2):** `knip` runs in CI with no false-positives and blocks genuinely-dead deps.

### FE-bloat Phase 3 — Bundle-size budget

- [ ] **B3.1** — Capture each app's current client bundle size as the baseline.
- [ ] **B3.2** — Set a budget (baseline + sane headroom margin) per app. 🛑 HUMAN DECISION: per-app bundle budgets.
- [ ] **B3.3** — Add a post-build size check (not a lint rule — runs after `nuxt build`).

✅ **Done-when (B3):** a bundle that grows past budget fails CI, surfacing build bloat early.

### FE-bloat Phase 4 — Portfolio rollout

- [ ] **B4.1** — Run `sync-pharos-registry.sh` for finance-lch, lab-qc, biuman-lis, design-studio; add `check-fe-bloat.mjs` to each `package.json` `lint-check`.
- [ ] **B4.2** — Fix any app that fails the gate (same cleanup pattern as admission-patient #53).

✅ **Done-when (B4):** `check-fe-bloat.mjs` wired into `lint-check` in every Pháros FE app and CI green across all of them; violations from B4.2 fixed and merged.

🚦 **Checkpoint B4.** Every Pháros FE app passes `check-fe-bloat` in CI; standard is live portfolio-wide.

---

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

---

## Decisions · Decisiones

> Resolved decisions during planning are logged in the **§Decisions locked** table above. Open execution-time decisions appear here and move to that table once resolved, with date.

**Open:**

*(No open decisions — all Stage 1 decisions resolved by Track A Stage 1 completion.)*

**Resolved during planning:**

- **Pastel contrast split** — `#FFE0E6`/`#FFB86B` kept as decorative `--brand-wash`; functional `--primary` = `#ff3d63`/`#e37600`. *(2026-06-18.)*
- **srcDir migration** — Migrate to `app/` srcDir, empirically proven. *(2026-06-18.)*
- **Mock-first backend** — Real backend wired only at Stage-5 sign-off. *(2026-06-18.)*
- **Cobol theme retirement** — Full `.dark` reconciliation in finance-lch (not a one-block delete). *(2026-06-18.)*
- **RBAC nav via `useMenu()` composable** — Registry contract amended so shell calls a reactive, auth-filtered nav. *(2026-06-18.)*
- **Dark accents approved** — `.dark.theme-recepcion` `#ff6b85` (6.7:1 AA); `.dark.theme-clientes` `#f59e3c` (7.1:1 AA). *(2026-06-18.)*
- **Track C quotes-page rewrite** — In-track prep stage added; Track C re-budgeted M/High. *(2026-06-18.)*
- **color-mode wiring (Track A, Stage 1)** — Synced shell ships its own `.dark`/localStorage wiring — no separate `@nuxtjs/color-mode` module needed; confirmed by skuger at Stage 1 completion. *(2026-06-18.)*
- **nav route mapping (Track A, Stage 1)** — Exact PascalCase routes for the 8 `AdmisionSidebar` sections verified against the live router and committed in `menu.ts` at Stage 1. *(2026-06-18.)*

## Risks · Riesgos

> **Resumen (ES).** Los riesgos principales son: lockfile desactualizado que bloquea CI, HTML crudo o CDN prohibido que falla los gates, deriva del registro por edición directa en la app, y autenticación headless que impide el test-contract.

- **Stale lockfile** → CI `--frozen-lockfile` aborts; all stages blocked. **Mitigation:** regenerate and commit lockfile immediately after every `pnpm add` in Stage 1 of each track.
- **Font CDN not removed** → `check-font-allowlist` hard-fails Gate Layer B. **Mitigation:** remove Google Fonts/Inter `<link>` and VT323 `@import` at Stage 1 before running lint-check; do not defer.
- **Raw HTML remaining in pages/components** → `check-no-raw-html` hard-fails Gate Layer B. **Mitigation:** Track C quotes rewrite must be complete before Stage 2; vendor thin `Table`/`Textarea` primitives in Track B where needed.
- **Hand-editing registry-owned files** → spec-drift fires forever; re-sync overwrites the edit. **Mitigation:** never hand-edit `tokens.css`, gate scripts, or `registry/app/**`; fix in the registry, then re-sync.
- **Stage 0 not merged before any track starts** → dark mode de-brands to navy; accent values are pastels not functional. **Mitigation:** Stage 0 must be merged and re-synced before any track's Stage 1 begins.
- **CI headless auth failure for `test-contract`** → SSR auth (no SSO in CI) causes logout → shell not visible → contract test fails. **Mitigation:** add `import.meta.dev`-guarded bypass or mock-SSO path before wiring `test-contract` (documented as a retro carry for Tracks B and C).
- **`v-model.number` stripped by shadcn `<Input>`** → amounts become strings; math breaks silently. **Mitigation:** use `:model-value` + `@update:model-value="x = Number($event)"` on all numeric inputs in Track B (finance) and Track C (quotes).
- **Retro Gate label removed prematurely** → standard drifts; lessons don't carry to the next track. **Mitigation:** `blocked:retro-gate` label on #47/#48; only @gczuluaga removes it on Retro Gate merge.

## References

- [RFC 0008 — Pháros design system + co-creation](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md)
- [pharos-lis — reference implementation (`lab-qc/frontend`, Step 0, DONE)](../pharos-lis/)
- [v1 plan (superseded)](archive/pharos-fe-spec-rollout.md)
- [Retro Gate fill template](pharos-track-retro.template.md)
- [Track A retro (post Stage 5)](archive/pharos-track-retro.A.md)
- [Tracking issue Interval-Col/.github#48](https://github.com/Interval-Col/.github/issues/48) — Track C / rollout
- [Track B issue Interval-Col/.github#47](https://github.com/Interval-Col/.github/issues/47)
- [Track A issue Interval-Col/.github#46](https://github.com/Interval-Col/.github/issues/46)
- [BRANCHING-AND-DEPLOY.md](../.github/BRANCHING-AND-DEPLOY.md) — org CI/branching standards
- [ops-plan-template.md](../templates/ops-plan-template.md) — this plan's template
- [Component library tracking issue Interval-Col/.github#73](https://github.com/Interval-Col/.github/issues/73)
- [FE-bloat gate tracking issue Interval-Col/.github#70](https://github.com/Interval-Col/.github/issues/70)
- [admission-patient component adoption plan](../admission-patient/plans/pharos-component-adoption-plan.md) — per-app execution (tracking #80)
- [`brands/pharos_brand/registry/scripts/check-fe-bloat.mjs`](../brands/pharos_brand/registry/scripts/check-fe-bloat.mjs) — canonical FE-bloat gate
- [`brands/pharos_brand/registry/frontend-standards.md`](../brands/pharos_brand/registry/frontend-standards.md) — §Iconos + §Higiene de dependencias
- [`brands/pharos_brand/BRAND.md`](../brands/pharos_brand/BRAND.md) §8 — iconography canon (Lucide + Material Symbols, size scale, a11y)
