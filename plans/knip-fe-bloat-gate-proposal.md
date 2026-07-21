---
status: proposed
owner: gczuluaga
created: 2026-07-21
updated: 2026-07-21
issue: Interval-Col/.github#70
start: TBD
target: TBD
implementation: TBD
effort: S
rfc: 0008
language: English body; Spanish "Resumen" + decision/criteria glosses.
related: scripts/check-fe-bloat.mjs (deterministic FE-bloat gate) · sync-pharos-registry.sh (registry copy-in model) · RFC 0008 design-system / registry track
---

# Knip as a frontend dead-code / anti-bloat CI gate · Knip como gate de CI contra código muerto y bloat en el frontend

> **Resumen (ES).** Propuesta **para decisión de German** (no es un hecho consumado). Nuestras
> apps de frontend acumulan **bloat silencioso**: archivos, `exports`, tipos y dependencias que ya
> nadie usa. Ni ESLint ni los 8 *design gates* actuales los detectan — el tree-shaking los esconde
> del bundle final pero siguen pesando en el repo, en el mantenimiento y en la superficie mental.
> `knip` (https://knip.dev) es un linter de TS/JS que encuentra exactamente eso. Ya lo dejamos
> anotado como *fast-follow* en el header de `check-fe-bloat.mjs` (issue **#70**). Esta propuesta
> plantea adoptarlo **primero en `lab-qc/frontend`**, en modo **solo-reporte / no bloqueante**,
> establecer una línea base, arreglar el código muerto real, y **solo después** volverlo un check
> requerido — y luego extenderlo al resto de frontends Pháros. El **riesgo #1** es que Nuxt
> auto-importa `app/composables/**`, `app/utils/**` y `app/components/**`: sin el plugin de Nuxt de
> knip (o la config correcta) knip los reporta como no usados y **inunda de falsos positivos**. El
> segundo riesgo son los **archivos sincronizados del registro** (shadcn-vue vendorizado): knip debe
> ignorarlos, y el manifiesto `pharos-registry.sha256` ya nos dice exactamente cuáles son.

**Author:** German (@gczuluaga) · **Date:** 2026-07-21 · **Status:** Proposed — draft for decision.

This document proposes adopting [`knip`](https://knip.dev) as a **dead-code / anti-bloat** CI gate
across the Pháros / Interval-Col frontends, starting with `lab-qc/frontend`. It advances the open
**"pharos-fe-bloat-gate"** initiative (`Interval-Col/.github#70`) and sits in the RFC 0008
design-system / registry track. It is a **proposal for German's decision**, not a merged standard —
the rollout is deliberately staged so nothing becomes blocking until a baseline is triaged.

> **Markers.** 🛑 **HUMAN DECISION** — a choice this doc deliberately does not make; escalate to the
> owner. 💡 **Heuristic** — a short engineering lesson. *(ES: 🛑 decisión humana; 💡 heurística.)*

---

## 1 · Problem — bloat accumulates silently · El bloat se acumula en silencio

> **Resumen (ES).** El frontend junta archivos, `exports`, tipos y dependencias que ya nadie usa.
> El tree-shaking los saca del bundle, así que "compila y pesa menos" nos engaña: el peso muerto
> sigue en el repo. ESLint y los 8 design gates no los ven — cada uno mira otra cosa.

Frontend code rots quietly. Over a codebase's life it accumulates:

- **Unused files** — a page, composable, or component that lost its last import in a refactor but
  was never deleted.
- **Unused exports and exported types** — a function/`interface`/`type` that is `export`ed but no
  longer imported anywhere (the `DisplayAnalyte` export-hygiene noise we already see in typecheck
  is exactly this family of signal).
- **Unused `dependencies` / `devDependencies`** — packages in `package.json` that no file imports
  anymore, plus the inverse (imported-but-unlisted).

None of this is caught today:

| Tool | What it checks | Blind to bloat? |
|---|---|---|
| `eslint --max-warnings 0` | per-file lint rules, style, some unused **locals** | Yes — it does not see cross-file "no one imports this" |
| 8 design gates (`check-no-raw-html`, `check-no-hex-colors`, `token-drift`, `registry-drift`, `contrast`, `font-allowlist`, …) | design-system conformance | Yes — orthogonal concern |
| `check-fe-bloat.mjs` (#70) | banned monolith deps + one-lib-per-category (2 **deterministic** rules) | Partially — it deliberately scopes to zero-false-positive `package.json` rules; **dead-dep / unused-file / unused-export detection was left as a knip fast-follow** |
| tree-shaking / `nuxt build` | strips dead code **from the bundle** | Hides the problem — the build stays green while the repo carries the weight |

💡 **Heuristic.** "The bundle is small" is not "the repo is clean." Tree-shaking optimizes the
*output*; it does nothing for the *source* a human has to read, grep, and reason about. Dead source
is a maintenance tax and an onboarding tax, not a bundle-size tax. *(ES: bundle pequeño ≠ repo
limpio; el código muerto se paga en mantenimiento, no en bytes servidos.)*

The `check-fe-bloat.mjs` header already records the intent verbatim: *"Dead-dep detection (knip) and
a bundle-size budget are tracked as fast-follows — see Interval-Col/.github#70."* This proposal is
that fast-follow.

---

## 2 · Proposal — adopt `knip` alongside `lint-check` · Adoptar knip junto a lint-check

> **Resumen (ES).** Adoptar `knip` como gate de bloat que corre **al lado** de `lint-check` (no lo
> reemplaza). Detecta archivos, `exports`, tipos y dependencias sin usar. Empieza en
> `lab-qc/frontend`, primero **advisory**.

Adopt **`knip`** as the dead-code / anti-bloat layer. It is a single dev-dependency + a small
config file; it complements — does not replace — the existing gates.

**What knip detects** (the relevant subset):

- Unused **files**, unused **exports**, unused **exported types** (`interface` / `type`).
- Unused **`dependencies`** and **`devDependencies`**; unlisted (imported-but-undeclared) deps;
  unresolved imports; duplicate exports.
- Optionally: unused enum/class members (off by default — noisy; leave off initially).

**Where it runs.** As a new script, e.g. `pnpm knip`, run **beside** the existing
`lint-check` — same CI job family, its own step so a failure is legible on its own. It is **not**
folded into the `lint-check` string in Phase 1 (that string is a hard gate today; knip must earn
"required" status through a baseline first — see §4). The deterministic `check-fe-bloat.mjs` keeps
running as-is; knip is the **non-deterministic, config-tuned** sibling that needs tuning + triage,
which is precisely why it was split out from the zero-false-positive deterministic gate.

`knip` = **k**ill **n**ot-**i**n-**u**se **p**ackages (and files, and exports). One tool, one config,
runs in seconds on a project this size.

---

## 3 · Key adoption risks & mitigations · Riesgos de adopción y mitigaciones

> **Resumen (ES).** Tres riesgos. (1) Nuxt **auto-importa** composables/utils/components → sin el
> plugin de Nuxt de knip, todo eso parece "no usado" y knip **explota en falsos positivos** — este
> es el riesgo grande. (2) Los **archivos del registro** (shadcn-vue vendorizado) hay que
> ignorarlos; el manifiesto ya los lista. (3) Es un **monorepo** (lab-qc/telemetry/pathology) →
> config por-app o `workspaces`.

### 3.1 🛑 Nuxt auto-imports — the make-or-break risk

Nuxt globally **auto-imports** everything under `app/composables/**`, `app/utils/**`, and
`app/components/**` (and more via modules). A file that is *never explicitly `import`ed* is still
used — Nuxt wires it in by convention. A naïve knip run treats "no explicit importer" as "dead" and
**floods false positives** across half the app (e.g. `app/utils/resultsReleaseMapper.ts`'s
`DisplayAnalyte` / `mapWireAnalyteToDisplay`, `app/composables/*`, every auto-registered component).

**Mitigation — mandatory before the first meaningful run:**

- Enable knip's **Nuxt plugin** (auto-detected when `nuxt` is a dependency and a `nuxt.config.*`
  exists). It seeds the Nuxt convention dirs as entry points so auto-imported modules count as used.
- **Belt-and-suspenders:** also declare the auto-import roots explicitly in `entry`
  (`app/composables/**`, `app/utils/**`, `app/components/**`, `app/pages/**`, `app/middleware/**`,
  `app/plugins/**`, `nuxt.config.ts`, `app/app.vue`, `server/**` if present).
- **Verify empirically:** the first run's success criterion is *"the auto-import dirs are not a wall
  of false positives."* If they are, the config — not the code — is wrong; fix config, re-run.

💡 **Heuristic.** For a convention-driven framework (Nuxt, Nitro), a dead-code tool is only as good
as its entry-point model. Get `entry` + the framework plugin right **first**; only then is a
"unused" verdict trustworthy. *(ES: en Nuxt, primero los entry points + el plugin; recién ahí un
"no usado" es creíble.)*

### 3.2 Registry-synced files must be ignored

The Pháros registry ships shared primitives into each app by **copy-in**
(`scripts/sync-pharos-registry.sh`), which drops a manifest at
`app/assets/pharos-registry.sha256` — one `sha256  <path-under-app>` line per synced file (101 files
in `lab-qc/frontend` today: `app/components/ui/**`, plus a handful like `app/components/SidebarUser.vue`,
`app/components/PharosHelpChat.vue`, `app/composables/useCan.ts`). These are **vendored** — a shadcn-vue
primitive legitimately exports variants the app doesn't use yet, and hand-editing them is already
forbidden and enforced by `check-registry-drift` / `check-registry-fresh`.

**Mitigation:** knip must **ignore** every registry-owned path. Two options:

- **Simple:** `ignore: ["app/components/ui/**"]` covers the bulk; add the few non-`ui/` synced paths
  explicitly.
- **Robust (recommended):** derive the ignore list **from the manifest** so it stays in lockstep
  with `check-registry-drift` — the manifest is already the machine-readable source of truth for
  "which files are registry-owned." A tiny build step can emit the knip `ignore` array from
  `pharos-registry.sha256`. Per-app adaptations tagged `pharos-registry:keep` (excluded from the
  manifest) are the app's own code and **should** be linted.

### 3.3 Monorepo shape

`pharos-lis` houses multiple apps (`lab-qc/`, `telemetry/`, `pathology/`), each with its own
frontend and its own `package.json`; CI lives at the repo root. Two viable shapes:

- **Per-app config (recommended to start):** a `knip.json` inside each app's `frontend/`, run
  per-app — mirrors how `lint-check` already works per-app and keeps blast radius contained.
- **`workspaces` config:** a single root `knip.json` with a `workspaces` map if/when a root pnpm
  workspace is adopted. Defer unless the monorepo grows a shared root install.

Other frontends (`finance-lch`, `admission-patient`, `public-web`, `biuman-lis`) each get their own
config at rollout time.

---

## 4 · Rollout — advisory → baseline → required · Despliegue: advisory → baseline → requerido

> **Resumen (ES).** Tres fases. **Fase 1:** knip corre **sin bloquear** (`--no-exit-code`), se
> triagea todo y se fija una línea base. **Fase 2:** se borra el código muerto real. **Fase 3:** se
> vuelve check **requerido**. Se empieza por `lab-qc/frontend` y luego se extiende al resto.

| Phase | Goal | Blocking? | Exit |
|---|---|---|---|
| **1 · Baseline** | Add knip + tuned Nuxt/registry config; run in **report-only** mode; triage every finding into real-dead vs false-positive; encode accepted exceptions as config | **No** (`--no-exit-code`) | A green *advisory* run + a triaged findings list |
| **2 · Cleanup** | Delete the real dead files/exports/deps the baseline surfaced; shrink the config `ignore`s as false-positive causes are fixed at the source | No | Findings list → near-zero real dead code |
| **3 · Enforce** | Flip knip to a **required** check on the app; extend to the next frontend | **Yes** | knip in required status checks alongside `gitleaks` + the design gates |

**Phase 1 mechanics (advisory).** Run `knip --no-exit-code` so CI reports but never fails.
knip has no first-class "baseline snapshot" file — the de-facto baseline is the **config
`ignore` / `ignoreDependencies` set**: each accepted finding is encoded there with a one-line
justification (same discipline as the `check-fe-bloat.mjs` ALLOWLIST). A markdown/JSON reporter
(`--reporter`) can post the summary to the PR.

**Order of adoption:**

1. **`lab-qc/frontend`** — the pilot (this is the reference app for the design gates already).
2. Then, one at a time: **`finance-lch`**, **`admission-patient`**, **`public-web`**,
   **`biuman-lis`** — each starting advisory, each earning "required" through its own baseline.

💡 **Heuristic.** Never ship a new lint tool as blocking on day one — a first run on a mature repo
is *all* findings, real and false, and a hard gate then just gets `# knip-ignore`'d into
uselessness. Advisory-first + triage is how the tool earns trust. *(ES: nunca arranques un linter
nuevo como bloqueante; advisory + triage primero, si no la gente lo silencia y muere.)*

---

## 5 · Proposed config sketch (ILLUSTRATIVE) · Boceto de configuración (ILUSTRATIVO)

> **Resumen (ES).** Ejemplo **ilustrativo** — no es config final. Muestra la forma tuneada para
> Nuxt: entry points de las carpetas auto-importadas, `ignore` de los archivos del registro, y
> `ignoreDependencies` para paquetes que Nuxt/Tailwind cargan sin un `import` explícito.

> ⚠️ **ILLUSTRATIVE ONLY.** Values below are a starting shape to be verified against a real run —
> not a ratified config. The `entry` + Nuxt-plugin story (§3.1) and the manifest-derived `ignore`
> (§3.2) are the parts that must be confirmed empirically first.

`knip.json` inside `lab-qc/frontend/`:

```jsonc
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  // Entry points: Nuxt auto-imports these dirs — declare them so their
  // exports are treated as USED even with no explicit importer.
  "entry": [
    "nuxt.config.ts",
    "app/app.vue",
    "app/pages/**/*.vue",
    "app/composables/**/*.{ts,js}",
    "app/utils/**/*.{ts,js}",
    "app/components/**/*.vue",
    "app/middleware/**/*.ts",
    "app/plugins/**/*.ts",
    "server/**/*.ts"
  ],
  "project": ["app/**/*.{ts,js,vue}", "scripts/**/*.mjs"],
  // Registry-owned, vendored primitives — ignore (ideally generate this
  // array from app/assets/pharos-registry.sha256 so it tracks the manifest).
  "ignore": [
    "app/components/ui/**",
    "app/assets/**"
  ],
  // Packages loaded by Nuxt/Tailwind/tooling without an explicit `import`
  // in app code — declare so knip does not report them as unused.
  "ignoreDependencies": [
    "@nuxt/eslint",
    "@nuxt/fonts",
    "shadcn-nuxt",
    "@pinia/nuxt",
    "tw-animate-css"
  ]
  // The `nuxt` plugin is auto-detected from the `nuxt` dependency +
  // nuxt.config.ts; keep it enabled (do not disable plugins).
}
```

`package.json` script (added beside `lint-check`, not inside it, in Phase 1):

```jsonc
{
  "scripts": {
    "knip": "knip",
    "knip:ci": "knip --no-exit-code --reporter compact"
  }
}
```

The `ignoreDependencies` list above is a *hypothesis* from the current `nuxt.config.ts` modules
(`@nuxt/eslint`, `@pinia/nuxt`, `shadcn-nuxt`, `@nuxt/fonts`) — the real list comes out of the first
run, not from guessing.

---

## 6 · Open questions for German · Preguntas abiertas para German

> **Resumen (ES).** Decisiones que **no** toma esta propuesta — las decide German.

- 🛑 **Org-wide vs per-repo.** Should knip config + the CI step be **synced from the registry**
  (like the design gates and `check-fe-bloat.mjs`, one canonical copy distributed by
  `sync-pharos-registry.sh`), or authored **per-repo**? A synced gate keeps the portfolio in
  lockstep; a per-repo gate lets each app tune `entry`/`ignore` to its own shape. *(ES: ¿gate
  sincronizado desde el registro, o por-repo?)*
- 🛑 **Blocking vs advisory end-state.** Is the target a **required** check (§4 Phase 3), or does
  knip stay permanently **advisory** (a visible drift signal, like `plan-lint` is today)? *(ES:
  ¿requerido al final, o advisory permanente como plan-lint?)*
- 🛑 **Who owns the baseline.** Who triages the Phase-1 findings and owns the `ignore` set + its
  justifications going forward? *(ES: ¿quién es dueño de la línea base y del set de `ignore`?)*
- 🛑 **Interaction with the registry sync model.** Ratify the manifest-derived `ignore` approach
  (§3.2): do we add a small step that emits knip's `ignore` array from `pharos-registry.sha256`, so
  registry-owned paths are ignored automatically and stay aligned with `check-registry-drift`?
  *(ES: ¿derivar el `ignore` de knip desde el manifiesto del registro?)*
- 🛑 **Relationship to #70's other fast-follow.** #70 also parks a **bundle-size budget**. Keep that
  a separate track, or fold both non-deterministic bloat signals under one umbrella? *(ES: ¿el
  presupuesto de tamaño de bundle va aparte o junto con knip?)*

---

## Glossary · Glosario

> **Resumen (ES).** Términos en inglés que se repiten; si falta uno, pregúntale a tu agente.

| English | Español | Means |
|---|---|---|
| dead code | código muerto | files/exports/deps that nothing imports or uses anymore |
| auto-import | auto-importación | Nuxt convention: modules under `app/composables\|utils\|components` are usable without an explicit `import` |
| entry point | punto de entrada | a file knip treats as a root of the "used" graph; everything reachable from it is alive |
| tree-shaking | tree-shaking / sacudida de árbol | the bundler dropping unreachable code from the built output (not from the source) |
| baseline | línea base | the initial triaged set of findings; accepted ones are encoded as config `ignore`s |
| advisory (gate) | gate advisory / no bloqueante | a CI check that annotates/reports but does not fail the build |
| registry sync / copy-in | sincronización del registro | `sync-pharos-registry.sh` copying shared primitives into each app + a sha256 manifest |
| manifest | manifiesto | `app/assets/pharos-registry.sha256` — the list of registry-owned files + their hashes |
| dev-dependency | dependencia de desarrollo | a package needed to build/test but not shipped at runtime (`devDependencies`) |

## Risks · Riesgos

> **Resumen (ES).** Dónde puede salir mal y qué hacer, sin generalidades.

- **Auto-import false-positive flood** → knip reports half the app as dead, the team loses trust and
  ignores it. **Mitigation:** §3.1 — Nuxt plugin + explicit `entry` for auto-import dirs, verified
  on run one *before* anyone reviews findings.
- **Registry drift** → knip flags vendored shadcn-vue exports, or its `ignore` list rots out of sync
  with the manifest. **Mitigation:** §3.2 — derive `ignore` from `pharos-registry.sha256`.
- **Gate fatigue** → shipped blocking on day one, gets silenced. **Mitigation:** §4 — advisory →
  baseline → required, never blocking before a triaged baseline.
- **Type-only export nuance** → knip's verdict on exported types (e.g. `DisplayAnalyte`) needs
  reading against auto-import + type-only realities before deleting anything. **Mitigation:** Phase
  2 deletes are reviewed, not auto-applied.

## References

- [`knip.dev`](https://knip.dev) — the tool.
- `scripts/check-fe-bloat.mjs` (registry canonical copy) — the deterministic FE-bloat gate whose
  header parks knip as the fast-follow tracked at `Interval-Col/.github#70`.
- `scripts/sync-pharos-registry.sh` + `check-registry-drift.mjs` / `check-registry-fresh.mjs` — the
  registry copy-in model and its integrity gates.
- [ENGINEERING_STANDARDS.md](../ENGINEERING_STANDARDS.md) → "Design-system CI gates" — where the
  existing `lint-check` gates are documented.
- RFC 0008 — Pháros design system + registry track.
