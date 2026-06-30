---
status: proposed
owner: gczuluaga
created: 2026-06-27
updated: 2026-06-27
issue: Interval-Col/.github#70
start: 2026-06-27
target: 2026-07-11
implementation: gczuluaga
language: English body; Spanish "Resumen" + glosses.
rfc: 0008
model: claude-sonnet-4-6
sources: [.github, admission-patient, finance-lch, pharos-lis, biuman-lis]
---

# Pháros FE dependency-hygiene gate (`check-fe-bloat`) · Compuerta de higiene de dependencias FE

> **Resumen (ES).** Una compuerta de CI mandatoria, sincronizada del registry Pháros y
> encadenada en `lint-check`, que previene el bloat de dependencias del frontend (el que
> limpiamos en admission-patient: monolito `@iconify/json` de 399 MB, libs de íconos y
> UI duplicadas). Arrancamos con **2 reglas deterministas** (cero falsos positivos) ya
> implementadas y probadas; `knip` (deps muertas) y un presupuesto de bundle quedan como
> **fast-follow** porque requieren afinado. Fechas tentativas — sin compromiso firme aún.

> **Markers** — ✅ **Done-when** · 🚦 **Checkpoint** · 🛑 **HUMAN DECISION** · 💡 **Heuristic**.

This plan tracks turning the dependency-hygiene rules surfaced while cleaning
admission-patient (PR #53) into a **mandatory, portfolio-wide CI gate**. The gate mirrors
the existing design-system gates (`check-*.mjs`): a canonical script in the Pháros
registry, synced into every app and chained into `pnpm lint-check`.

## Glossary · Glosario

| English | Español | Means |
|---|---|---|
| gate / lint gate | compuerta | A `check-*.mjs` script chained in `lint-check` that fails CI on a rule violation |
| registry | registry | `.github/brands/pharos_brand/registry/` — the copy-in source of truth synced to apps |
| iconify monolith | monolito de iconify | The full `@iconify/json` package (~400 MB, every icon collection) |
| per-collection | per-collection | Individual `@iconify-json/<prefix>` packages — only the icon sets actually used |
| knip | knip | A tool that finds unused files/dependencies/exports in a JS/TS project |
| bundle budget | presupuesto de bundle | A post-build size threshold that fails CI if the client bundle grows past it |

## Out of scope · Fuera de alcance
- The host-capacity OOM fix (`admission-patient#54`) — different problem (build *memory*, not deps).
- Reworking the existing design-system gates or the stale gate table in `ENGINEERING_STANDARDS.md`.

---

## Phase 1 — Deterministic rules (monolith ban + one-lib-per-category) · Reglas deterministas

> **Resumen (ES).** 1.1 escribir el script canónico con las 2 reglas; 1.2 sincronizar
> en `lint-check` (registry + recordatorio del sync); 1.3 documentar en
> `frontend-standards.md`; 1.4 adoptar en admission-patient como banco de pruebas.
> **Esta fase ya está hecha en este PR + el wiring en admission-patient PR #53.**

- [x] **1.1** — `check-fe-bloat.mjs` in the registry: bans `@iconify/json`; enforces one
      library per "same-purpose" category (Lucide-for-Vue; Radix/Reka headless-UI), with a
      tiny justified `ALLOWLIST`. Deterministic, zero false-positives.
- [x] **1.2** — Wire into `lint-check`: add to `sync-pharos-registry.sh`'s canonical chain
      reminder (so future syncs include it); the sync loop already copies all `check-*.mjs`.
- [x] **1.3** — Document in `registry/frontend-standards.md` (§ Higiene de dependencias).
- [x] **1.4** — Adopt in admission-patient as the proving ground (PR #53): script + `lint-check`.
      Verified: passes on the cleaned tree, fails on the original (`@iconify/json` + 2 dup categories).

✅ **Done-when:** the gate is in the registry + chain, documented, and green in admission-patient.

## Phase 2 — Dead-dependency detection (`knip`) · Deps muertas

> **Resumen (ES).** 2.1 añadir `knip` con config + allowlist por app; 2.2 afinar para
> eliminar falsos positivos (deps de runtime/tipos/config); 2.3 encadenar en `lint-check`.

- [ ] **2.1** — Add `knip` (replacing the stray unused `depcheck` in `telemetry`) with a
      shared base config in the registry; per-app `knip.json` for overrides.
- [ ] **2.2** — 🛑 **HUMAN DECISION:** tune the allowlist per app until zero false-positives,
      then decide warn-vs-fail. knip flags runtime-only / type-only / config-only deps that
      are NOT actually dead — these need an allowlist before the gate can block merges.
- [ ] **2.3** — Chain into `lint-check` once the per-app allowlist is clean.

✅ **Done-when:** `knip` runs in CI with no false-positives and blocks genuinely-dead deps.

## Phase 3 — Bundle-size budget · Presupuesto de bundle

> **Resumen (ES).** 3.1 medir el tamaño base del client bundle por app; 3.2 fijar un
> presupuesto con margen; 3.3 chequeo post-build que falla si se excede.

- [ ] **3.1** — Capture each app's current client bundle size as the baseline.
- [ ] **3.2** — Set a budget (baseline + a sane headroom margin) per app.
- [ ] **3.3** — Add a post-build size check (not a lint rule — runs after `nuxt build`).

✅ **Done-when:** a bundle that grows past budget fails CI, surfacing "build bloat" early.

## Phase 4 — Portfolio rollout · Despliegue al portafolio

> **Resumen (ES) — Fase 4: Despliegue al portafolio.**
>
> Sincronizar el script canónico a todas las apps Pháros y corregir cualquier violación
> que el gate detecte, para que el estándar quede activo en todo el portafolio.
>
> En orden, las tareas:
>
> 1. **4.1** — Ejecutar `sync-pharos-registry.sh` en finance-lch, lab-qc, biuman-lis y design-studio; añadir `check-fe-bloat.mjs` al `lint-check` de cada `package.json`.
> 2. **4.2** — Corregir las apps que fallen el gate (mismo patrón de limpieza que admission-patient #53).

- [ ] **4.1** — Run `sync-pharos-registry.sh` for finance-lch, lab-qc, biuman-lis, design-studio;
      add `check-fe-bloat.mjs` to each `package.json` `lint-check`.
- [ ] **4.2** — Fix any app that fails the gate (same cleanup pattern as admission-patient #53).

✅ **Done-when:** `check-fe-bloat.mjs` is wired into `lint-check` in every Pháros FE app and CI is green across all of them; any violations found in 4.2 are fixed and merged. *(ES: el gate está activo y pasando en todo el portafolio.)*

🚦 **Checkpoint 4.** Every Pháros FE app passes `check-fe-bloat` in CI; the standard is live portfolio-wide.

## Decisions · Decisiones
- ✅ 2026-06-27 — Start with the 2 deterministic rules; defer knip + bundle-budget (need tuning). Rationale: ship zero-false-positive value now; avoid blocking merges on noisy checks.
- 🛑 OPEN — warn-vs-fail for knip (Phase 2.2), and the per-app bundle budgets (Phase 3.2).

## Risks · Riesgos

> **Resumen (ES).** Tres vectores de riesgo principales: falsos positivos que bloquean CI, allowlist de knip que nunca converge, y apps nuevas que se unen al portafolio sin pasar por el sync.

- **False-positive block on a live CI pipeline** → a gap in the `ALLOWLIST` causes a legitimate dep to be flagged, blocking merges in an app. **Mitigation:** verify the gate passes on the clean tree (Phase 1.4 precedent) before chaining into `lint-check` in each app during 4.1; treat any new failure as a tuning gap, not a rollback trigger.
- **knip allowlist never stabilises (Phase 2)** → noisy output delays chaining into `lint-check` indefinitely. **Mitigation:** the 🛑 HUMAN DECISION in 2.2 forces an explicit warn-vs-fail call; if tuning drags past one sprint, record the decision and ship knip in warn mode to preserve partial value rather than blocking on perfection.
- **Portfolio drift** → a new Pháros FE app is added without running `sync-pharos-registry.sh`, skipping the gate entirely. **Mitigation:** add a "run sync after any new app scaffold" reminder to `registry/frontend-standards.md` and the onboarding checklist for new Pháros apps.

## References
- Interval-Col/.github#70 — tracking issue.
- admission-patient PR #53 — the cleanup that motivated this + the proving-ground adoption.
- `brands/pharos_brand/registry/scripts/check-fe-bloat.mjs` — the canonical gate.
- `brands/pharos_brand/registry/frontend-standards.md` § Higiene de dependencias.
- RFC 0008 §6 — design/standards CI gates.
