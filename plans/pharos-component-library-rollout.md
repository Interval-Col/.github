---
status: proposed
owner: gczuluaga
created: 2026-06-28
updated: 2026-06-28
issue: none — filed on approval (board entry created in Phase 0)
start: 2026-06-30
target: 2026-08-29
implementation: SKuger01
language: English body; Spanish "Resumen" + decision/criteria glosses.
rfc: rfcs/0008-pharos-design-system.md
related: .github/plans/pharos-fe-spec-rollout-v2.md
---

# Pháros component library — shared FE primitives · Biblioteca de componentes Pháros

> **Resumen (ES).** Cerramos el único punto abierto que dejó la [RFC 0008](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md): **la biblioteca de componentes compartida**. Hoy cada app (y cada sesión de "vibe coding") reinventa a su manera la búsqueda de personas, los desplegables, el encabezado de página, los formularios, el fetch y la navegación-hacia-atrás — eso es la incoherencia que el líder quiere eliminar. El plan eleva **7 primitivas** al sistema de diseño Pháros, las co-crea en `design-studio`, las ratifica en la RFC 0008 + el registro, y las distribuye por el mecanismo **copy-in** que ya existe (`sync-pharos-registry.sh`) — sin paquete npm, sin infraestructura nueva de aplicación. Orden: **fundaciones → flujo → resto**, y `admission-patient` es el **primer consumidor**. No es un rewrite: es estandarización pragmática sobre lo que shadcn-vue ya da.

This plan closes RFC 0008's own deferred Phase-1 follow-up — **the shared Pháros component library** (RFC 0008 §5 names it as the "registry seed list … beyond the app-shell"). It is the FE-coherence fix the team lead asked for, elevated org-wide: a small set of **named, reusable primitives** that the dev group and AI-assisted sessions converge on, so output stops diverging. It complements [`pharos-fe-spec-rollout-v2.md`](pharos-fe-spec-rollout-v2.md) (which rolled out the *shell*); this plan rolls out the *components inside it*. It is not a new RFC — it is an **RFC 0008 amendment** + this execution plan, reusing the registry, the copy-in sync, the lint-check chain, the escalator, and the design-studio playground that the v2 rollout already proved in production.

---

## Decisions locked (this session — German, 2026-06-28)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Where the standard lives | **Elevate to RFC 0008** (org-wide), NOT admission-patient-local. 3 layers: RFC amendment (decision) · registry (implementation + distribution) · this plan (execution). |
| 2 | Build venue | **Co-create in `design-studio`** (the playground), not a per-app PoC branch. |
| 3 | Sequencing | **Foundations → Flow → Rest** (lookup/select/shell → flow/back-nav → fetch/form). |
| 4 | Icon collection | **Lucide (house) + Material Symbols Outlined (one governed clinical fallback).** Per BRAND.md §8; Material Symbols pairs with Lucide because both are outline-stroke (MDI is filled → clashes). |
| 5 | Icon mechanism | **One shared `<Icon>` tag** for the whole org; `@iconify/tailwind` `icon-[…]` CSS classes underneath (collection-agnostic). |
| 6 | design-studio → registry promote path | **Build the `promote-to-registry` script FIRST** (Phase 0) — it is the one piece of infra that does not exist today. |
| 7 | Extraction source per primitive | **Best-in-class per pillar, not defaulted to admission-patient** (see the extraction matrix) — sourced from an evidence-based 3-app maturity comparison. |

> 🛑 Four sub-decisions remain open and are escalated in the **Decisions** section: the fetch-codegen mandate, FormField's validation binding, gate posture (per-primitive vs consolidated), and the promote-script automation scope. *(ES: cuatro sub-decisiones siguen abiertas — ver §Decisions.)*

## Marker legend · Leyenda

| Marker | Meaning |
|---|---|
| 🛑 **HUMAN DECISION** | A choice the plan does not make. Escalate to @gczuluaga; do not let an agent guess. *(ES: decisión humana.)* |
| ✅ **Done-when** | Definition of Done — verified only when every line is literally true. *(ES: terminado-cuando.)* |
| 🚦 **Checkpoint** | Mandatory stop. Show the named evidence to @gczuluaga before continuing — **including in auto mode.** *(ES: punto de control — alto obligatorio.)* |
| 🔵 mechanical / 🟠 escalate | A step an agent can run vs one the architect decides. |

> **Profile note.** This plan mirrors the lean shape of its sibling `pharos-fe-spec-rollout-v2.md` (senior implementer @SKuger01 under Opus review), so it omits the full junior preamble trio (How-to-use / Conventions / Working-rules verbatim). The Working rules of that plan apply unchanged: commit + push after every slice; Conventional Commits with a mandatory scope (`feat(pharos-ui): …`); review the FE in the browser; **auto mode is slice-bounded**; a 🚦 is never skipped.

## Glossary · Glosario

| English | Español | Means |
|---|---|---|
| primitive | primitiva | a shared, reusable component or composable everyone is expected to use instead of hand-rolling |
| registry | registro | `.github/brands/pharos_brand/registry/` — the single source of truth, copied into apps |
| copy-in / sync | copiar-hacia-dentro / sincronizar | `sync-pharos-registry.sh` mirrors `registry/app/**` into each app at the same paths; apps own the copy |
| composable | composable | a reusable Vue `useXxx()` function (state/logic), e.g. `useFlow`, `useAsyncState` |
| escalator | escalador | the branch-flow ratchet (main-only-from-develop + required checks) that makes gates binding |
| gate | compuerta | a `check-*.mjs` script in `lint-check` that fails CI when a banned pattern appears |
| WARN → hard-fail | aviso → bloqueo | a gate first warns during migration, then blocks once the lead app conforms |
| extraction source | fuente de extracción | the app whose existing implementation we lift the org primitive from |
| Done-when | terminado-cuando | the literal, checkable list that means a phase is verified |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es de este plan — es para después. Si un agente propone construir algo de esta lista, no lo hagas.

- **A runtime npm package** (`@pharos/ui`). RFC 0008 §7 rejected it (the `@intervalica/alexandria` private-registry CI trap). Distribution stays **copy-in**.
- **A full rewrite of any app.** This is extraction + adoption, not a greenfield.
- **biuman-lis adoption.** Deferred to RFC 0008 Phase 3 (separate plan), as in the v2 rollout.
- **Monolith decomposition** (Reception 1341, HorariosMedicos 1343, finance-lch CausacionPanel 1480 / bills.vue 1462) — named as a companion track below, **not gated on by this plan**.
- **finance-lch / lab-qc form migration onto FormField.** They hand-roll forms today; their migration is a later, separate phase — not a precondition for shipping the primitive.

---

## Standard home — three layers

| Layer | Where | Owns |
|---|---|---|
| **Decision** | `rfcs/0008-pharos-design-system.md` (amendment block) | *that* the 7 primitives are the Phase-1 library; each primitive's API intent; that composables are now a sanctioned registry artifact class |
| **Implementation + distribution** | `.github/brands/pharos_brand/registry/` | the actual SFCs (`registry/app/components/(ui/)`) + a **new** `registry/app/composables/`; surface docs (`registry/surfaces/*.md`); the new gate scripts (`registry/scripts/`) |
| **Execution** | this plan (`.github/plans/`) | the rollout. `admission-patient/plans/` gets only a pointer + a Track entry — it is a *consumer*, not the owner of the standard |

## Reuse, don't rebuild — the infra is already here

The v2 rollout proved all of this in production. This plan **adds to it**, it does not fork it:

- **The registry** — single source of truth; the component library is its own named open item (RFC 0008 §5). Do **not** create a new home.
- **`sync-pharos-registry.sh`** — copy-in distributor. Its `find registry/app -type f` mirror (§4b) is path-agnostic, so new SFCs **and** composables distribute with **zero new tooling**. (Caveat: `registry/app/composables/` has never been synced — Phase 2 verifies it with `--dry-run`.)
- **The 8-gate `pharos-lint-check`** (eslint + no-scoped-pages / no-raw-html / no-hex / palette / token-drift / contrast / font-allowlist / **fe-bloat** — the last merged via #71) — new primitives add **one new `check-*.mjs` each** to this synced chain. No parallel enforcer.
- **The escalator** (main-only-from-develop + required-check-blocks-push) — a new gate inherits binding force automatically once it is in the chain.
- **The design-studio playground** + `buildSpec`/`regen-spec` → `registry/spec/*.md` + `check-spec-drift` — the co-creation + drift-tracking surface.

**Never hand-edit registry-owned files in an app** (fix the registry → re-sync). The only net-new piece of infra is the **design-studio → registry promote path** (Phase 0).

## Per-pillar extraction matrix — best-in-class, evidence-based

> **Resumen (ES).** Cada primitiva se extrae de la app que **ya la hace mejor** — no por defecto de admission-patient. Esto sale de una comparación de madurez de 3 apps; así el líder ve que la decisión de "app de referencia" está respaldada por evidencia, no por costumbre.

| # | Pillar | Best source | Rework on the way out |
|---|--------|-------------|------------------------|
| 1 | **EntityLookup** (+ `PatientLookup` / `PhysicianLookup` presets) | admission-patient `SearchPatient` / `usePatientSearch` (only reused entity-search, ×3 sites) | rebuild on finance-lch's shadcn **Combobox** substrate (loading/empty/error states) instead of the ad-hoc Dialog |
| 2 | **SearchableSelect** (type-to-filter dropdown) | **finance-lch** — full reka-ui shadcn **Combobox** family (the accessible substrate) | graft admission-patient `PhysicianCombobox`'s behavior (250 ms debounce, arrow/enter/escape nav, reused ×4). **Acceptance: handle empty/null `v-model` natively** so nobody reinvents finance-lch's `NONE_*` sentinel (47 occurrences) |
| 3 | **PageShell + PageHeader** | page-shell is **already org-owned via registry sync** (no extraction); **lab-qc** `layouts/default.vue` is the documented canonical reference | `PageHeader` is the net-new piece; add a shell-level **full-bleed slot / CSS var** to kill admission-patient `Reception`'s `-m-6` hack |
| 4 | **useAsyncState + fetch** | **finance-lch** `apiFetch` (Bearer + 401→SSO bounce) + per-domain store `loading/error` scaffold + error normalizer + generated typed client | borrow **lab-qc** `useApi()`'s per-composable `loading/error/items` shape for the component-facing layer |
| 5 | **FormField** (label + control + error) | **NET-NEW — no app has it.** Built fresh in design-studio | validation convention from admission-patient (`vee-validate` + `@vee-validate/zod` + `toTypedSchema`); first refactor removes ~58 manual `errors[…]` blocks in `PatientForm` alone |
| 6 | **useFlow** (back-stack + dialog-state) | admission-patient `useProcessState` (only real flow primitive: `goNext/goBack/resetSteps/setStepStatus` + persist + step indicator) | **generalize** — steps as config, not hardcoded Paciente/Orden; migrate in-flight persisted `localStorage` state |
| 7 | **Icon standard** (`<Icon>` wrapper + collections) | **finance-lch / lab-qc** Lucide-only baseline | codify admission-patient's `check-fe-bloat` per-collection gate as the documented exception; admission-patient migrates its 18-collection / 149-usage sprawl down to Lucide + Material Symbols |

### Lead-consumer framing

`admission-patient` stays the **first consumer / first integrator** — it is the only app that exercises **all 7 pillars** in production, so it is the natural proving ground (PhysicianCombobox ×4, SearchPatient ×3, useProcessState) and the only one with a real form-validation foundation. **But it is demoted from "reference for everything" to "reference for 4 of 7"** (form, flow, lookup, searchable-select-behavior). **finance-lch** is the co-reference for **fetch + icons**; **lab-qc** for **shell + sync discipline**. Being the lead consumer does **not** make it the source for the fetch/icon primitives — extracting those from finance-lch/lab-qc and making admission-patient *adopt* them is the cleaner direction, and doubles as the migration that finally gives admission-patient the central fetch wrapper it lacks.

## The model — co-create → ratify → land → adopt

A design-studio prototype is not the standard until it is ratified and landed in the registry. Per primitive:

| Stage | Name | Gate / DoD |
|---|---|---|
| 1 | **Prototype** | built in `design-studio` with a showcase page under live theme controls (ported from the extraction source via shadcn-vue CLI grain — never `cp` legacy) |
| 2 | **Co-decide** | @gczuluaga + @SKuger01 walk the API (props/emits/slots) + behavior in a playground session; resolutions captured |
| 3 | **Ratify** | decision written into the RFC 0008 amendment block; per-primitive design intent authored into `registry/surfaces/*.md` (finanzas.md template) |
| 4 | **Land** | the ratified SFC/composable promoted into `registry/app/**` (via the Phase-0 promote script); matching `check-*.mjs` added in **WARN**; **@gczuluaga merges the registry PR** (sole registry approver) |
| 5 | **Adopt** | re-sync into the consumer; refactor the app-local duplicate onto the registry primitive; flip the gate **WARN → hard-fail** once the lead consumer conforms |

### Governance

Inherits RFC 0008's locked governance (Decisions 2026-06-17): **@gczuluaga = gate-keeper / sole registry approver / merger; @SKuger01 = implementation lead.** Co-creation happens in @gczuluaga + @SKuger01 playground sessions (the proven Phase-0 pattern). German merges his own registry PRs.

### Companion tracks (named, NOT gated on by this plan)

- **Monolith decomposition** — Reception (1341), HorariosMedicos (1343), finance-lch CausacionPanel (1480) / bills.vue (1462). Primitive extraction *helps* but does not wait on this.
- **8-gate parity** — `check-fe-bloat` is now in the registry (merged #71); lab-qc and finance-lch (7 gates today) pick it up on their next `sync-pharos-registry.sh` → standardize all three on 8.

---

## Phase 0 — Charter the library + build the promote path

> **Resumen (ES) — Fase 0: Constituir la biblioteca + construir el puente.**
>
> Ratificamos que las 7 primitivas son la biblioteca Phase-1, bendecimos los composables como nuevo tipo de artefacto del registro, y construimos lo único que falta: el script que **promueve** un componente del playground al registro.
>
> En orden, las tareas:
>
> 1. **0.1** — Escribir el bloque de enmienda en la RFC 0008 (decisión + contrato de API por primitiva).
> 2. **0.2** — Bendecir `registry/app/composables/` como artefacto sincronizado.
> 3. **0.3** — Construir y probar el script `promote-to-registry` (design-studio → registro).
> 4. **0.4** — Crear stubs de intención de diseño por primitiva en `registry/surfaces/`.
> 5. **0.5** — Abrir el issue de tablero para este plan.
>
> Decisión humana: el alcance de automatización del promote-script (ya decidido "construirlo primero"; confirmar si es manual-asistido o totalmente automático).

- [ ] **0.1** — Author the **RFC 0008 amendment block** `Decisions resolved (2026-06-XX): shared component library`, mirroring the existing dated blocks (e.g. 2026-06-18) and the `useMenu()` amendment. It records: (a) the 7 primitives are ratified as the Phase-1 component library; (b) each primitive's **one-paragraph API-intent contract** (props/emits/slots at the level of intent, not code); (c) that `registry/app/composables/` is a **sanctioned, synced artifact class** (precedent-setting — the registry has only ever shipped CSS + SFCs + gates); (d) the icon standard (Decisions 4–5). Update RFC 0008 §5 / Phase 1 to mark the open item as in-progress.
  - **Why:** the component library is RFC 0008's *own* named open item — this closes it, it does not open a new RFC. The amendment is the durable decision record the registry implements.
- [ ] **0.2** — In the amendment, explicitly bless `registry/app/composables/` and confirm `sync-pharos-registry.sh` is expected to mirror it (it works mechanically — `find registry/app` is path-agnostic — but has never been exercised; Phase 2 proves it).
- [ ] **0.3** — Build the **`promote-to-registry` script** (the one missing piece of infra). Today `design-studio` only *consumes* the registry (copy-in) and exports `spec/*.md` via `regen-spec`; there is **no** mechanism to push a composed SFC/composable from the playground into `registry/app/`. The script lifts a named primitive from `design-studio/app/{components,composables}/**` into `registry/app/**` at the correct path, normalizing imports. Dry-run first; @gczuluaga gates the registry PR it produces.
  - **Why:** without it, primitives get hand-copied inconsistently and drift from their playground source — the exact incoherence this plan exists to kill.
- [ ] **0.4** — Create per-primitive **design-intent stubs** in `registry/surfaces/` using the `finanzas.md` template (audience → component inventory with Props + Vue blocks → domain patterns → target paths → "ported from"). One stub per primitive; they get filled as each lands.
- [ ] **0.5** — File the board issue for this plan (`Interval-Col/.github#NN`), bilingual, pointing at this plan as source of truth; update the frontmatter `issue:` key.

🛑 **HUMAN DECISION — promote-script automation scope.** German chose "build it first." Confirm whether v1 is **manual-assisted** (script stages the copy, human reviews + opens the PR) or **fully automated** (script opens the PR). Recommend manual-assisted v1. *(ES: confirmar si el script abre el PR solo o lo prepara para revisión humana — se recomienda asistido.)*

✅ **Done-when:**
- The RFC 0008 amendment PR is open and **merged by @gczuluaga**; RFC 0008 §5/Phase-1 shows the library item as in-progress. *(ES: la enmienda está fusionada por German.)*
- Each of the 7 primitives has a one-paragraph ratified API contract in the amendment. *(ES: cada primitiva tiene su contrato.)*
- `promote-to-registry --dry-run <primitive>` runs and prints the exact files it *would* write into `registry/app/**`, with zero unintended paths. *(ES: el dry-run del promote-script imprime los archivos correctos.)*
- A `registry/surfaces/` stub exists for each primitive. *(ES: existe un stub por primitiva.)*

🚦 **Checkpoint 0.** Show @gczuluaga: the merged RFC amendment diff, the `promote-to-registry --dry-run` output, the surface stubs. Questions:
1. Why is closing RFC 0008's existing open item the right home, rather than a new admission-patient doc or a new RFC? *(ES: ¿por qué la enmienda y no un doc/RFC nuevo?)*
2. Walk the `--dry-run` live: show that the script lands a composable under `registry/app/composables/` and that a subsequent `sync --dry-run` would mirror it into a consumer. *(ES: recorrer el dry-run en vivo.)*

---

## Phase 1 — Foundations: EntityLookup · SearchableSelect · PageShell/PageHeader (+ Icon wrapper)

> **Resumen (ES) — Fase 1: Fundaciones.**
>
> Las tres primitivas de mayor impacto visible + el envoltorio de iconos. Aquí se resuelve el dolor #1 del líder (desplegables buscables) y la divergencia HandlePatient ↔ HandlePhysician.
>
> En orden:
>
> 1. **1.1** — `SearchableSelect` sobre el `Combobox` de finance-lch + el comportamiento de `PhysicianCombobox`.
> 2. **1.2** — `EntityLookup` (+ presets Paciente/Médico) reconstruido sobre `SearchableSelect`.
> 3. **1.3** — `PageHeader` + slot full-bleed del shell; `PageShell` documentado desde lab-qc.
> 4. **1.4** — Envoltorio `<Icon>` (Lucide + Material Symbols) en el registro.
> 5. **1.5** — Catálogo de iconos `iconos.vue` en design-studio.
> 6. **1.6** — Compuertas de adopción en modo WARN + verificación de sync.

- [ ] **1.1** — Prototype **SearchableSelect** in design-studio: substrate = finance-lch's reka-ui `Combobox` family inside a `Popover`; behavior layer ported from admission-patient `PhysicianCombobox` (single `DEBOUNCE_MS = 300`, arrow/enter/escape nav, suppress-on-pick). Props: `v-model`, `items` (static, client-filtered) **and/or** `searchFn(query)` (async), `labelKey`/`valueKey`, `groupBy`, an item slot, `required`/`disabled`/`error`. **Acceptance: empty/null `v-model` handled natively** (no `NONE_*` sentinel). Land in `registry/app/components/ui/`.
- [ ] **1.2** — Prototype **EntityLookup** built *on* SearchableSelect, parameterized by a `searchFn` + result-row slot; ship `PatientLookup` / `PhysicianLookup` presets (default debounce, columns, empty/notfound copy, the shared `idle|searching|found|notfound` state). Source the search-API→filter→select+emit shape from `SearchPatient`/`usePatientSearch`. Land in `registry/app/components/`.
  - **Why:** this is the lead's central complaint — HandlePatient and HandlePhysician share zero code today. One component + two presets makes patient and physician lookup converge *by construction*.
- [ ] **1.3** — **PageHeader** (title slot + optional toolbar/actions slots) — net-new. Document **PageShell** from lab-qc's `layouts/default.vue` as the canonical reference (no extraction — it is already registry-synced). Add a **shell-level full-bleed slot / CSS var** so pages stop hand-cancelling shell padding (kills admission-patient `Reception`'s `-m-6` hack). Settle **one** page-title mechanism (recommend `definePageMeta` + breadcrumb-from-route; retire `usePageTitle`).
- [ ] **1.4** — Build the **`<Icon>` wrapper** in design-studio and land it in the registry: `<Icon name="lucide:search" :size="5" />` → renders `icon-[lucide--search]` via `@iconify/tailwind`; `aria-hidden` by default (meaningful icons pass `aria-label`); size scale `size-4`/`size-5`/`size-6` = 16/20/24 px (BRAND.md §8); semantic color tokens only; Lucide default + **Material Symbols Outlined** fallback for clinical glyphs. Rewrite `registry/frontend-standards.md` §Iconos to this canonical form (it currently shows a contradictory `<Icon name>` @nuxt/icon snippet **and** a 20/24/32 px scale that disagrees with BRAND.md §8's 16/20/24).
  - **Why:** there are 3 incompatible icon mechanisms across apps today and the registry doc documents a 4th nobody uses. One wrapper makes "which mechanism underneath" a one-time internal choice; copy-paste between apps then always works.
- [ ] **1.5** — Add **`design-studio/app/pages/componentes/iconos.vue`** — a live catalog of the endorsed Lucide set + the allowlisted Material Symbols glyphs, each rendered through `<Icon>` at all three sizes, with a search box and copy-to-clipboard of the canonical snippet. This is the discovery surface that stops per-app reinvention.
- [ ] **1.6** — Add the first **adoption gates in WARN**: e.g. `registry/scripts/check-no-raw-combobox.mjs` (flags hand-rolled type-to-filter selects in `pages/`/`layouts/`) joining the synced `lint-check` string. Verify `sync-pharos-registry.sh --dry-run` mirrors the new SFCs into a consuming app.
  - 💡 **Heuristic.** Land gates in **WARN** while the primitive is still spreading. A hard-fail gate shipped before the component exists everywhere red-walls every repo at once — the v2 color gates took exactly this WARN-then-flip posture for a reason. *(ES: la compuerta nace en aviso; se vuelve bloqueo solo cuando la app líder ya cumple.)*

✅ **Done-when:**
- The 3 SFCs + the `<Icon>` wrapper live in `registry/app/components/(ui/)` and **@gczuluaga merged** the registry PR(s). *(ES: las primitivas están en el registro, fusionadas por German.)*
- design-studio showcase pages (incl. `iconos.vue`) render the primitives under **light + dark + the rosa accent**, verified in the browser. *(ES: se ven en el navegador en claro/oscuro.)*
- `sync-pharos-registry.sh --dry-run <consumer>` shows the new SFCs landing at the right paths. *(ES: el dry-run del sync muestra las rutas correctas.)*
- The new gate(s) run **green in WARN** in `lint-check`. *(ES: la compuerta corre en aviso.)*

🚦 **Checkpoint 1 (first real UI).** Show @gczuluaga: the showcase pages in the browser (SearchableSelect filtering live; PatientLookup + PhysicianLookup side by side; the icon catalog with copy-to-clipboard). Questions:
1. Why does building EntityLookup *on* SearchableSelect (rather than as a separate widget) make the two lookup pages converge? *(ES: ¿por qué EntityLookup encima de SearchableSelect?)*
2. Walk the empty/null `v-model` case live on SearchableSelect — show it needs no `NONE_*` sentinel. *(ES: mostrar el caso de valor vacío sin sentinel.)*

---

## Phase 2 — Flow: useFlow (the first registry composable)

> **Resumen (ES) — Fase 2: Flujo y navegación-hacia-atrás.**
>
> Generalizamos el `useProcessState` de admission-patient a un `useFlow` reutilizable — y como es el **primer composable** del registro, probamos explícitamente que la sincronización de `registry/app/composables/` funciona.
>
> En orden:
>
> 1. **2.1** — Prototipar `useFlow` (back-stack arbitrario + estado de diálogo) desde `useProcessState`.
> 2. **2.2** — Aterrizar `registry/app/composables/useFlow.ts` + su surface doc.
> 3. **2.3** — Verificar el camino de sync de composables con `--dry-run` (nunca antes ejercido).
> 4. **2.4** — Decidir SSR-safety + persistencia (`skipHydrate`).
>
> Decisión humana: la migración del estado persistido en `localStorage` de órdenes en vuelo.

- [ ] **2.1** — Prototype **useFlow** in design-studio: arbitrary back-stack + dialog-state, **steps as config** (labels + status), exposing the same `goNext`/`goBack`/`resetSteps`/`setStepStatus`/persist contract as `useProcessState` but **not hardcoded** to Paciente/Orden. Standardize dialog open-state on `v-model:open` (retire the `ref(boolean)` / `ref(object-of-flags)` variants).
- [ ] **2.2** — Land **`registry/app/composables/useFlow.ts`** (the first registry composable) + its surface doc. Decide orders/create's identity in the showcase: modal-in-flow OR full page with a visible *Volver* — not a modal-on-a-route dead-end.
- [ ] **2.3** — **Explicitly verify** `sync-pharos-registry.sh --dry-run` mirrors `registry/app/composables/**` correctly — this path has **never** been exercised. If it misses, fix the sync (registry-side) before relying on it.
  - **Why:** composables are a new artifact class for the registry (CSS + SFCs + gates only, until now). A silent sync miss here would break every downstream composable; prove it on the first one.
- [ ] **2.4** — Decide SSR-safety + persistence (`skipHydrate`) per `frontend-standards`; ensure a mid-flow reload keeps the operator on the right step.

🛑 **HUMAN DECISION — in-flight persisted-state migration.** `useProcessState` persists order steps to `localStorage` under specific keys. Generalizing it risks breaking admission-patient's mid-order reload behavior if the keys/shape change. Confirm the migration handling (key remap vs one-time reset) before adoption in Phase 4. *(ES: confirmar cómo migrar el estado persistido de órdenes en vuelo.)*

✅ **Done-when:**
- `registry/app/composables/useFlow.ts` lands and **@gczuluaga merged** it. *(ES: useFlow en el registro, fusionado.)*
- `sync --dry-run` is shown mirroring a file under `registry/app/composables/` into a consumer. *(ES: el sync copia composables — probado.)*
- The design-studio showcase drives at least the Recepción intake back-nav with `useFlow` (steps passed as config), verified in the browser. *(ES: useFlow maneja la navegación de Recepción en el playground.)*

🚦 **Checkpoint 2.** Show @gczuluaga: the composables sync `--dry-run` output + the flow showcase with a working back path. Question: why must the composables sync path be proven on the *first* composable rather than assumed? *(ES: ¿por qué probar el sync de composables en el primero?)*

---

## Phase 3 — The rest: useAsyncState + FormField

> **Resumen (ES) — Fase 3: Lo demás.**
>
> Aterrizamos el envoltorio de fetch con estados de carga/vacío/error uniformes y el envoltorio de campo de formulario (label + control + error). Con esto, la biblioteca Phase-1 queda completa.
>
> En orden:
>
> 1. **3.1** — `registry/app/composables/useAsyncState.ts` (fetch + carga/vacío/error).
> 2. **3.2** — `registry/app/components/FormField.vue` (+ contexto FormItem).
> 3. **3.3** — Compuertas de adopción opcionales en WARN + actualizar la nota "Naming de componentes".
>
> Decisión humana: ¿la primitiva de fetch exige codegen o solo el wrapper? · ¿FormField atado a vee-validate o agnóstico?

- [ ] **3.1** — Land **`registry/app/composables/useAsyncState.ts`** (the second registry composable): `useAsyncState(fetcher, {default})` returning `{data, status, loading, error, isEmpty, refresh}`, honoring the `frontend-standards` `useFetch` contract (camelCase FE / snake_case BE, same-origin relative base, **AbortController + stale-response guard**). Source the wrapper + error-normalizer from finance-lch `apiFetch`; the component-facing `loading/error/items` shape from lab-qc `useApi()`. Document the rule: `useAsyncData` for idempotent reads, the wrapper for mutations; **empty is modeled explicitly, never conflated with error.**
- [ ] **3.2** — Build **`FormField.vue`** (+ a `FormItem` context): label + control slot + inline error, on the admission-patient validation convention (`vee-validate` + `@vee-validate/zod` + `toTypedSchema`). Land in the registry. First refactor target (Phase 4) = admission-patient `PatientForm`/`PhysicianForm` (removes ~58 manual `errors[…]` blocks in `PatientForm` alone).
- [ ] **3.3** — Add optional adoption gates in WARN (e.g. `check-formfield-usage`); update `registry/frontend-standards.md` "Naming de componentes" from *"Fase-1 follow-up, built in the playground"* to **"shipped — these primitives live in `registry/app/**`."**

🛑 **HUMAN DECISION — fetch-codegen mandate.** Does the org `useAsyncState` primitive **mandate** finance-lch's generated typed client (`~/lib/api/generated`), or only the wrapper + error-normalizer? admission-patient has no codegen today; adopting the wrapper without it yields a half-adopted pattern. Recommend: **wrapper now, codegen as a separate convention.** *(ES: ¿la primitiva exige codegen o solo el wrapper? Se recomienda wrapper ahora, codegen aparte.)*

🛑 **HUMAN DECISION — FormField validation binding.** `vee-validate`-bound (best ergonomics for the apps that use it) vs validation-agnostic (lab-qc/finance-lch hand-roll forms). This sets the reusability ceiling. *(ES: ¿FormField atado a vee-validate o agnóstico?)*

✅ **Done-when:**
- `useAsyncState.ts` + `FormField.vue` land and **@gczuluaga merged** them. *(ES: ambos en el registro, fusionados.)*
- `frontend-standards.md` reflects the **shipped** library (no longer "Fase-1 follow-up"). *(ES: el doc dice "shipped".)*
- All new gates run green (WARN). *(ES: las compuertas en aviso, verdes.)*

---

## Phase 4 — Adopt in admission-patient (first consumer) + flip gates to hard-fail

> **Resumen (ES) — Fase 4: Adopción en admission-patient + bloqueo de compuertas.**
>
> Re-sincronizamos admission-patient, reescribimos sus duplicados locales (PhysicianCombobox / SearchPatient / useProcessState / formularios / iconos) sobre las primitivas del registro, le damos el wrapper de fetch que le falta, y **recién entonces** volvemos las compuertas de aviso a bloqueo.
>
> En orden:
>
> 1. **4.1** — Re-sync admission-patient (recoge las 7 primitivas).
> 2. **4.2** — Refactor: borrar duplicados, apuntar Recepción/colas/formularios a las primitivas.
> 3. **4.3** — Introducir el wrapper de fetch central (arregla su debilidad #1).
> 4. **4.4** — Migrar la maraña de iconos a Lucide + Material Symbols vía `<Icon>`.
> 5. **4.5** — Voltear las compuertas WARN → bloqueo; actualizar el retro doc para B/C.

- [ ] **4.1** — Re-sync admission-patient (`scripts/sync-pharos-registry.sh .`) — picks up all 7 primitives + composables. Confirm `--dry-run` shows **zero hand-edits** to registry-owned files.
- [ ] **4.2** — Refactor app-local duplicates onto the registry primitives: delete `PhysicianCombobox`/`SearchPatient`'s bespoke internals → `EntityLookup`/`SearchableSelect`; point Recepción intake/queue + `PatientForm`/`PhysicianForm` at the registry `FormField`/`PageHeader`; `useProcessState` → `useFlow` (apply the Phase-2 persisted-state migration).
- [ ] **4.3** — Introduce the **central fetch wrapper** (`useAsyncState`/`apiFetch` pattern) — admission-patient is the outlier (37 composables, no wrapper). This fixes its #1 weakness and validates the fetch primitive against the most complex consumer.
- [ ] **4.4** — Migrate the **icon sprawl**: 18 collections / 149 usages → Lucide + Material Symbols, all through `<Icon>`. Extend `check-fe-bloat` to ban `@nuxt/icon` and (post-migration) `lucide-vue-next` as a render path; add `registry/scripts/check-icon-collections.mjs` (allowlist = lucide + material-symbols, modeled on `check-font-allowlist`). Standardize all three apps onto 8 gates.
- [ ] **4.5** — **Flip the new gates WARN → hard-fail** now that the lead consumer conforms. Update the live retro doc ([`pharos-track-retro.A.md`](pharos-track-retro.A.md)) so tracks B/C inherit the primitives on their next sync.
  - 💡 **Heuristic.** Copy-in distribution means a primitive defect propagates to every app at once. Treat admission-patient **dev** as the canary, keep version/changelog discipline on registry PRs, and never flip a gate to hard-fail until the canary is green. *(ES: el copy-in propaga un defecto a todas las apps; admission-patient dev es el canario.)*

✅ **Done-when:**
- admission-patient `pnpm build` + the existing design-gate + E2E smoke are green with the new primitives wired. *(ES: admission-patient compila y pasa sus pruebas con las primitivas.)*
- `sync --dry-run` shows **zero hand-edits** to registry-owned files. *(ES: cero ediciones a archivos del registro.)*
- The new gates are **hard-fail** and `pharos-lint-check` is green including them; all three apps run 8 gates. *(ES: compuertas en bloqueo, verdes; 3 apps con 8 compuertas.)*
- HandlePatient and HandlePhysician are visibly converged in the browser (same lookup, same shell, same icons), verified by @gczuluaga. *(ES: las dos páginas se ven y funcionan igual — verificado en el navegador.)*
- The retro doc back-propagates to B/C. *(ES: el retro doc propaga a B/C.)*

🚦 **Checkpoint 4 (exit).** Show @gczuluaga: admission-patient in the browser (the two lookup pages converged; searchable dropdowns; consistent icons; a multi-step flow with a working back path), the green `lint-check` with hard-fail gates, the `sync --dry-run` zero-diff. Questions:
1. Why is making the *riskiest, PHI-adjacent* app the first integrator the right call rather than the safest one? *(ES: ¿por qué la app más riesgosa va primero?)*
2. Walk a full Recepción flow live — forward through the steps and back — and show no state is lost. *(ES: recorrer un flujo de Recepción completo, ida y vuelta.)*

> This exit checkpoint blocks archiving the plan until Checkpoints 0–2 have been walked.

---

## Decisions · Decisiones

**Open (🛑 — escalated to @gczuluaga):**

- 🛑 **Promote-script automation scope** — manual-assisted vs fully automated (Phase 0). Recommend manual-assisted v1.
- 🛑 **Fetch-codegen mandate** — does `useAsyncState` require the generated typed client, or only the wrapper? (Phase 3). Recommend wrapper now, codegen separate.
- 🛑 **FormField validation binding** — `vee-validate`-bound vs agnostic (Phase 3).
- 🛑 **Gate posture** — one `check-*.mjs` per primitive vs a single consolidated `curated-primitive-usage` gate; confirm WARN→hard-fail timing (per phase).
- 🛑 **useFlow persisted-state migration** — key remap vs one-time reset for in-flight orders (Phase 2/4).

**Resolved during planning (2026-06-28, German):**

- **Elevate to RFC 0008** (org-wide), 3-layer home. · **Co-create in design-studio.** · **Foundations → Flow → Rest.** · **Icons: one `<Icon>` tag; Lucide + Material Symbols Outlined.** · **Build the promote-to-registry script first.** · **Per-pillar best-in-class extraction** (matrix above).

## Risks · Riesgos

> **Resumen (ES).** Lo que puede salir mal y dónde está la mitigación — concreto, no genérico.

- **Multi-source integration coherence** → the form primitive (admission-patient zod idiom) and the fetch primitive (finance-lch `apiFetch` idiom) come from different apps and could feel like two grafts. **Mitigation:** reconcile them in design-studio in Phase 3 so a validated form submitting through the standard wrapper is one showcase, not two.
- **Riskiest-first integrator** → admission-patient is PHI-adjacent, socket-driven, with a 1341-LOC Reception; primitive churn lands there first. **Mitigation:** sequence the copy-in behind admission-patient's existing design-gate + E2E smoke; verify in **dev** before any prod promote (Phase 4 / Checkpoint 4).
- **Composables sync never exercised** → `registry/app/composables/` could silently fail to mirror. **Mitigation:** Phase 2 proves it with `--dry-run` on the first composable before anything depends on it.
- **Copy-in blast radius** → a primitive defect propagates to every app on next sync. **Mitigation:** admission-patient-dev as canary; version/changelog discipline on registry PRs; never flip a gate to hard-fail before the canary is green.
- **WARN→hard-fail timing** → flipping too early red-walls every repo. **Mitigation:** flip only after the lead consumer conforms (Phase 4), the v2 color-gate posture.
- **Over-generalization** → `SearchPatient` is patient-specific and `useProcessState` is a 2-step wizard; forcing fully generic APIs up front risks an API nobody uses well. **Mitigation:** ground each generalization in admission-patient's real call-sites (it's the first consumer), then lift.
- **Two parallel `.github/plans` rollouts** → this plan + `pharos-fe-spec-rollout-v2.md` share repos + the retro chain. **Mitigation:** sequence this plan **under/after** v2's shell adoption per app; **reuse** the existing retro-gate, don't add a second handoff chain.
- **Perception risk** → if the plan kept admission-patient as lead without the evidence, it would read as ignoring German's maturity concern. **Mitigation:** the per-pillar extraction matrix is surfaced prominently so the lead-consumer decision is visibly evidence-based.

## References

- [RFC 0008 — Pháros design system](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) — §5 Components (the open "registry seed list"), §7 Distribution (copy-in, not a package), Phase 1 "Extract the foundation"; the dated `Decisions resolved` blocks this plan's amendment mirrors.
- [`pharos-fe-spec-rollout-v2.md`](pharos-fe-spec-rollout-v2.md) — the sibling rollout (the *shell*); this plan rolls out the *components* and reuses its registry / sync / lint-check / escalator / retro-gate machinery.
- [`pharos-track-retro.A.md`](pharos-track-retro.A.md) — the live retro doc the Phase-4 back-propagation updates.
- `.github/brands/pharos_brand/registry/` — the registry (home + distribution); `registry/frontend-standards.md` §Iconos (to rewrite); `registry/surfaces/finanzas.md` (the surface-doc template); `registry/scripts/` (gate scripts).
- `.github/brands/pharos_brand/BRAND.md` §8 — iconography canon (to expand: mechanism, Lucide + Material Symbols, size scale, color tokens, a11y).
- `Interval-Col/design-studio` — the playground (co-creation venue); `app/pages/componentes/finanzas.vue` (showcase-page pattern); the new `iconos.vue` catalog.
- `Interval-Col/admission-patient` — first consumer; extraction sources `PhysicianCombobox` / `SearchPatient` / `usePatientSearch` / `useProcessState` / `PatientForm` / `check-fe-bloat.mjs`.
