---
status: superseded
created: 2026-06-13
updated: 2026-06-17
owner: gczuluaga
implementation: folded into pharos-fe-spec-rollout.md
language: English body; Spanish "Resumen" + decision/criteria glosses.
tracking-issue: Interval-Col/.github#25 (folded into #43)
superseded-by: pharos-fe-spec-rollout.md (§Charts → @unovis) · Interval-Col/.github#43
superseded-on: 2026-06-17
---

# Charting migration → @unovis (org standard) · Migración de gráficos a @unovis

> ⚠️ **SUPERSEDED 2026-06-17 — folded into the FE-spec rollout.** This standalone plan and its
> tracker `.github`#25 are now part of **`pharos-fe-spec-rollout.md` → §Charts → @unovis** (`#43`).
> *Why fold:* the chart-token foundation (`--chart-1..5`) already shipped in
> `.github/brands/pharos_brand/registry/tokens.css`, and the live chart surface is just two apps
> the rollout already owns (finance-lch + pharos-lis/lab-qc) — `correlacion-metodos.vue` +
> `clsi-ep15.vue` are placeholders, so they are greenfield @unovis, not parity ports. **Kept here
> for history:** the bilingual rationale, glossary, and the QC statistical-parity checkpoints below
> remain the reference for the lab-qc QC port.
> *(ES) Plan archivado: el trabajo vive ahora en `pharos-fe-spec-rollout.md` (§Charts → @unovis,
> issue #43). Se conserva aquí por su detalle bilingüe y los checkpoints de paridad estadística QC.*

> **Resumen (ES).** Estandarizamos los gráficos de todos los apps Pháros sobre
> **`@unovis`** (decisión de RFC 0008 Q11). Hoy `finance-lch` y `lab-qc` arman
> gráficos a mano sobre **Chart.js**; este plan los migra. La forma de token
> compartida es **`--chart-1..5`** (coloreada desde la paleta de familia, la
> convención nativa de shadcn-vue). No se empieza ninguna migración de app hasta
> que (1) RFC 0008 esté aceptado y (2) exista la Fase 0: tokens y componentes de
> gráfico compartidos en el registro, prototipados y validados en el brand
> playground.

Per **RFC 0008 Q11** (decided 2026-06-13): **`@unovis` is the shared charting
standard for all Pháros apps**, and the shared **chart-token shape is numbered
`--chart-1..5`** (brand-colored from the family palette — it's shadcn-vue's
native chart-token convention; shadcn-vue's chart components are themselves built
on @unovis). This plan migrates the apps currently hand-building on **Chart.js**
off it.

Why @unovis (diligence summary): F5-backed and **dogfooded as F5 Distributed
Cloud's own viz engine** (strong maintenance incentive), v1.6.5 (Apr 2026),
**Apache-2.0**, SVG + **CSS-variable-native** (charts obey the token cascade like
every other component, unlike Chart.js's canvas which needs a manual JS bridge),
and consumed **copy-in** via the shadcn-vue registry → you own the source, never
trapped (the alexandria lesson). SVG perf is fine at LCH's chart scale
(hundreds–low-thousands of points).

---

## How to use this plan · Cómo usar este plan

**EN.** This plan is written to be executed with AI-agent assistance —
that is expected and encouraged. The plan, not the agent, makes the
technical decisions. Your job has three parts: **execute** the tasks,
**verify** each one against its Done-when list, and **escalate** the
decisions the plan marks for a human.

Read each task fully — including its **Why** and **Done-when** — *before*
you start it. A task is not finished because an agent said so; it is
finished when every Done-when line is literally true and you have
checked it yourself.

If a task or its **Why** doesn't make sense, that is a gap in *this
plan*, not a failing in you — stop and ask gczuluaga. A question costs
minutes; a misunderstanding shipped costs days.

**If the English here slows you down:** every section opens with a
Spanish **Resumen**, and your AI agent will translate or explain any
part of this plan in Spanish if you ask it — that is a completely
legitimate thing to do. Don't let the language be the reason a task
stalls.

**ES.** Este plan está escrito para ejecutarse con ayuda de agentes de
IA — eso se espera y se fomenta. Las decisiones técnicas las toma el
plan, no el agente. Tu trabajo tiene tres partes: **ejecutar** las
tareas, **verificar** cada una contra su lista *Done-when*, y **escalar**
las decisiones que el plan marca para un humano.

Lee cada tarea completa — incluyendo su **Why** y su **Done-when** —
*antes* de empezarla. Una tarea no está terminada porque un agente lo
diga; está terminada cuando cada línea *Done-when* es literalmente cierta
y tú mismo la verificaste.

Si una tarea o su **Why** no te quedan claras, eso es un vacío de *este
plan*, no una falla tuya — pregúntale a gczuluaga. Y si el inglés te
frena: cada sección tiene un **Resumen** en español, y tu agente de IA
te traduce o explica cualquier parte en español si se lo pides — hazlo
sin problema.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| 💡 **Heuristic** | A short engineering or working lesson. Worth 30 seconds. *(ES: heurística — lección breve.)* |
| 🛑 **HUMAN DECISION** | A choice the plan deliberately does not make. **Do not let an agent pick it.** Escalate to gczuluaga. *(ES: decisión humana — no la toma un agente; escala a gczuluaga.)* |
| ✅ **Done-when** | The Definition of Done. The phase is verified only when every line is literally true. *(ES: terminado-cuando — definición de "hecho".)* |
| 🚦 **Checkpoint** | Stop. Show gczuluaga the named evidence and answer the questions before continuing. **Mandatory stop — including in auto mode** (see Working rules). *(ES: punto de control — alto obligatorio, también en modo auto.)* |

> **On the checkpoints.** Each 🚦 lists evidence to show and questions to
> answer. The questions are **not a test of you** — they test whether
> the plan explained things well enough. gczuluaga may also ask any of
> them at any time. *(ES: las preguntas del checkpoint no son un examen
> tuyo — prueban si el plan explicó bien; gczuluaga puede preguntarlas en
> cualquier momento.)*

## Working rules · Reglas de trabajo

These apply to every phase.

- **Commit and push after every slice.** When a task group or a phase is
  done and its Done-when checks pass, commit and push to GitHub
  **immediately**. Work that lives only on your laptop cannot be seen,
  reviewed, helped with, or recovered. *(ES: haz commit y push a GitHub
  apenas termines — el trabajo que solo vive en tu laptop no existe para
  el equipo.)*
- **Commit messages — Conventional Commits, scope required.**
  `type(scope): description` — e.g. `feat(finance-lch): port KpiCard to @unovis`.
  `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The `(scope)` is
  **mandatory**. Branch names mirror it: `type/scope-short-description`.
  *(ES: Conventional Commits; el `(scope)` es obligatorio; la rama
  refleja el commit.)*
- **Merge mode is merge-commit, everywhere.** "Allow squash merging" is
  **off** org-wide — PRs land as merge commits, never squashed. *(ES: el
  modo de merge es merge-commit en todas partes; el squash está
  deshabilitado.)*
- **Review the frontend yourself, in the browser.** A phase that touches
  the UI is **not verified** because the backend endpoint returned `200`
  — it is verified when you have opened the app, clicked through what
  you built, and seen it work the way a real user would use it. *(ES:
  revisa el frontend tú mismo, en el navegador — un `200` del backend no
  es una funcionalidad que sirve.)*
- **Which AI tool:** Claude **Sonnet** by default; **Opus** when a task
  is hard or you are stuck; **Copilot** for inline autocomplete and
  quick questions — not for executing a whole task. *(ES: Sonnet por
  defecto; Opus cuando es difícil o te atascas; Copilot para
  autocompletar.)*
- **You can tell your agent to skip the Why boxes — we won't stop you.**
  But the 🚦 checkpoint questions are asked by a person, and that you
  cannot outsource. Reading as you go is the cheap way to be ready.
  *(ES: puedes pedirle a tu agente que se salte las explicaciones — pero
  las preguntas del checkpoint las hace una persona; eso no se delega.)*
- **Auto mode is slice-bounded.** Auto mode (running without clarifying
  questions between turns) is allowed for the duration of **one
  slice** — a single numbered task, or one phase when the plan groups
  tasks that way. At the end of every slice, the agent **STOPS**,
  surfaces what landed (Done-when items verified, files touched,
  what's next), and waits for explicit human acknowledgement before
  starting the next slice. At 🚦 Checkpoints the stop is stronger —
  the human walks the evidence with the agent. Auto mode is **never**
  "execute the whole plan unattended." *(ES: el modo auto va por
  slice, no por plan entero. Al final de cada slice, el agente
  **PARA**, te muestra qué cerró (Done-when, archivos tocados, qué
  viene) y espera tu visto bueno antes del siguiente slice. En los
  🚦 el alto es más fuerte — recorres la evidencia con el agente.
  Auto **nunca** significa "ejecuta el plan completo solo".)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que vas a ver muchas
> veces en este plan, con su traducción y una línea de qué significan.
> Si te encuentras un término del plan que no está aquí y no lo
> entiendes, pregúntale a tu agente — no es una falla tuya, es un vacío
> de esta tabla.

| English | Español | Means |
|---|---|---|
| chart token (`--chart-1..5`) | token de gráfico | the numbered CSS-variable series shadcn-vue uses to color chart series, fed from the family palette |
| copy-in (registry) | copiar-adentro (registro) | you copy the component source into your repo via the registry instead of installing an npm package — you own the source, never trapped |
| CSS-variable-native | nativo de variables CSS | the chart reads its colors from the CSS token cascade directly, with no manual JS bridge |
| JS bridge | puente JS | hand-written JS that copies CSS-var values into a chart library's JS config (Chart.js's canvas needs this; @unovis does not) |
| statistical-parity port | migración con paridad estadística | a port verified by matching the computed/rendered statistics (control limits, regression, EP15 bands), not just visual likeness |
| visual-regression snapshot | captura de regresión visual | a stored image of a rendered component that CI diffs against future renders to catch unintended visual changes |
| Done-when | terminado-cuando | the literal checkable list that means the task is verified |
| commit + push | hacer commit y push | save to git locally **and** send to GitHub — both verbs |
| slice | rebanada / unidad de trabajo | a small piece of work that can ship on its own |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> v1+ / para después. Si un agente sugiere construir algo de esta lista,
> no lo hagas.

Explicitly out of scope — not for this plan:

- **admission-patient + biuman-lis chart migration** — they have no
  significant chart surfaces today; they adopt @unovis natively when they
  build charts. Nothing to migrate now.
- **New chart types / dashboards** — this plan ports existing surfaces to
  @unovis; it does not add new visualizations.

---

## Gating · Gating

> **Resumen (ES) — Gating.** No se arranca ninguna migración de app hasta
> que se cumplan dos condiciones: (1) RFC 0008 aceptado, y (2) la Fase 0
> exista en el registro (tokens `--chart-1..5` y componentes de gráfico
> compartidos). Los gráficos se prototipan y validan **primero** en el
> brand playground (artefacto de RFC 0008 Q5).

Do **not** start app migrations until: (1) RFC 0008 is accepted, and (2) the
Phase-0 foundation exists — the shared `--chart-1..5` tokens are defined in the
token contract and the shared chart components are in the registry. Charts are
**prototyped + validated in the brand playground** (RFC 0008 Q5 artifact) first.

🛑 **HUMAN DECISION — gate release.** Do not let an agent declare the gate
open. App migration (Phase 1+) starts only once gczuluaga confirms RFC 0008
is accepted **and** the Phase-0 foundation has landed in the registry.
*(ES: decisión humana — solo gczuluaga abre el gate; ningún agente lo
declara abierto.)*

## Inventory (apps on Chart.js today) · Inventario

> **Resumen (ES) — Inventario.** Los apps que hoy usan Chart.js y deben
> migrar: `finance-lch` (riesgo bajo–medio, KPIs/tendencias) y `lab-qc`
> (riesgo **alto**, gráficos QC estadísticamente especializados).

| App | Chart surfaces | Library today | Risk |
|---|---|---|---|
| **finance-lch** | `KpiCard`, `KpiTrendModal` (dashboards) | `chart.js ^4.5.1` + `vue-chartjs ^5.3.3` | Low–medium — standard KPI/trend charts |
| **lab-qc** | media-móvil, correlación, **CLSI-EP15**, Levey-Jennings-style QC charts | `chart.js ^4.4.1` | **High** — statistically specialized; needs output parity |

*(admission-patient + biuman-lis have no significant chart surfaces today — they
adopt @unovis natively when they build charts.)*

---

## Phase 0 — Foundation (in the registry, gated above)

> **Resumen (ES) — Fase 0: Fundamentos (en el registro, sujeta al gating).**
>
> Esta fase crea la base compartida antes de tocar cualquier app: los tokens
> de gráfico y los componentes @unovis en el registro, con regresión visual.
> Viene primero porque la base rota se descubre cara después.
>
> En orden, las tareas:
>
> 1. **0.1** — Definir `--chart-1..5` en el contrato de tokens, coloreados desde
>    la paleta de familia; documentar extensiones semánticas por dominio (p. ej.
>    gráficos QC de lab-qc).
> 2. **0.2** — Agregar al registro los componentes de gráfico @unovis compartidos
>    (área/barra/línea/dona + leyenda/tooltip), prototipados en el playground.
> 3. **0.3** — Cablear las capturas de regresión visual (Q9) para esos componentes.
>
> Decisión humana: el gate de release (ver Gating arriba).

- [ ] **0.1** — Define `--chart-1..5` in the shared token contract, colored from
      the family palette; document semantic chart-token *extensions* for domains
      that need them (e.g. lab-qc QC charts).
  - **Why:** `--chart-1..5` is shadcn-vue's native chart-token convention and
    @unovis reads tokens straight from the CSS cascade — so defining them in the
    contract is what makes every downstream chart theme itself for free, with no
    per-app JS bridge.
- [ ] **0.2** — Add the shared @unovis-based chart components to the registry
      (area/bar/line/donut + legend/tooltip), prototyped in the playground.
- [ ] **0.3** — Wire Q9 visual-regression snapshots for the shared chart components.

✅ **Done-when:** `--chart-1..5` exist in the token contract and a domain
chart-token extension is documented; the area/bar/line/donut + legend/tooltip
components exist in the registry and render in the brand playground reading
those tokens; visual-regression snapshots for the shared chart components run
in CI. *(ES: los tokens `--chart-1..5` existen en el contrato y hay una
extensión de dominio documentada; los componentes están en el registro y
renderizan en el playground leyendo esos tokens; las capturas de regresión
visual corren en CI.)*

🚦 **Checkpoint 0.** Show gczuluaga: the pushed token-contract change, the
chart components rendering in the brand playground, and the green
visual-regression CI run. Questions:
1. Why does defining `--chart-1..5` in the token contract remove the need for
   a per-app JS color bridge? *(ES: ¿por qué definir `--chart-1..5` en el
   contrato elimina la necesidad de un puente JS de color por app?)*
2. Walk the playground live with gczuluaga: switch theme/accent and show the
   chart series recoloring from the token cascade. *(ES: recorre el playground
   en vivo — cambia tema/acento y muestra las series recoloreándose desde el
   cascade de tokens.)*

---

## Phase 1 — finance-lch (lower risk first)

> **Resumen (ES) — Fase 1: finance-lch (lo de menor riesgo primero).**
>
> Migramos los gráficos KPI/tendencia de finance-lch a los componentes @unovis
> compartidos y quitamos Chart.js. Va primero porque son gráficos estándar:
> bajo riesgo, buen rodaje de la base de la Fase 0.
>
> En orden, las tareas:
>
> 1. **1.1** — Portar `KpiCard` + `KpiTrendModal` a los componentes @unovis compartidos.
> 2. **1.2** — Reemplazar el puente JS `getChartPalette()` por theming nativo de variables CSS.
> 3. **1.3** — Quitar las deps `chart.js` + `vue-chartjs` cuando ninguna superficie las use.
> 4. **1.4** — Verificar paridad visual y de comportamiento contra los dashboards actuales.

- [ ] **1.1** — Port `KpiCard` + `KpiTrendModal` to the shared @unovis components.
- [ ] **1.2** — Replace `getChartPalette()` JS-bridge with token-native CSS-var theming.
  - **Why:** the `getChartPalette()` bridge exists only because Chart.js's canvas
    can't read CSS vars; @unovis reads them directly, so the bridge becomes dead
    code once the charts are token-native.
- [ ] **1.3** — Remove `chart.js` + `vue-chartjs` deps once no surface uses them.
- [ ] **1.4** — Visual + behavioral parity check against the current dashboards.

✅ **Done-when:** `KpiCard` and `KpiTrendModal` render via the shared @unovis
components in the running app; `getChartPalette()` is gone and series colors come
from CSS vars; `chart.js` and `vue-chartjs` are removed from the dependency tree
and the app builds clean; the dashboards match the previous Chart.js output on
visual and behavioral review in the browser. *(ES: los dos componentes
renderizan vía @unovis en el app corriendo; `getChartPalette()` ya no existe y
los colores vienen de variables CSS; `chart.js` y `vue-chartjs` están fuera del
árbol de deps y el app compila limpio; los dashboards coinciden con la salida
previa en revisión visual y de comportamiento en el navegador.)*

🚦 **Checkpoint 1.** Show gczuluaga: the finance-lch dashboards in the browser
(side-by-side or before/after with the old Chart.js output), and the
dependency-removal diff dropping `chart.js` + `vue-chartjs`. Questions:
1. Why is finance-lch sequenced before lab-qc? *(ES: ¿por qué finance-lch va
   antes que lab-qc?)*
2. Walk the dashboards live with gczuluaga and show theme/accent recoloring the
   ported charts. *(ES: recorre los dashboards en vivo y muestra el cambio de
   tema/acento recoloreando los gráficos portados.)*

---

## Phase 2 — lab-qc (specialized, port carefully)

> **Resumen (ES) — Fase 2: lab-qc (especializado, portar con cuidado).**
>
> Migramos los gráficos QC de lab-qc (media-móvil, correlación, CLSI-EP15,
> Levey-Jennings). Son **paridad estadística**: hay que verificar que los
> límites de control, la regresión y las bandas EP15 coincidan exactamente con
> Chart.js — no basta el parecido visual.
>
> En orden, las tareas:
>
> 1. **2.1** — Portar los gráficos QC como migración con paridad estadística verificada.
> 2. **2.2** — Mantener los tokens de gráfico semánticos de lab-qc como extensiones por app, mapeando a la base compartida donde se pueda.
> 3. **2.3** — Quitar `chart.js` cuando todas las superficies QC estén portadas.
>
> Decisión humana: la firma de paridad estadística (ver marcador abajo).

🛑 **HUMAN DECISION — statistical-parity sign-off.** The QC charts encode clinical
statistics (control limits, regression, CLSI-EP15 bands). An agent must not
declare parity by eyeballing the rendered chart — a port that looks right but
computes/renders bands wrong is a correctness bug. gczuluaga (or the named QC
owner) confirms parity against the current Chart.js output before Phase 2 is
considered done; the verification is recorded on the tracking issue. *(ES:
decisión humana — la firma de paridad estadística no la da un agente a ojo;
gczuluaga o el dueño de QC confirma contra la salida actual y queda registrado
en el issue de seguimiento.)*

- [ ] **2.1** — Port the QC charts (media-móvil, correlación, CLSI-EP15, Levey-Jennings).
      Treat these as **statistical-parity** ports: verify the rendered
      statistics (control limits, regression, EP15 bands) match the current
      Chart.js output exactly — not just visual likeness.
- [ ] **2.2** — Keep lab-qc's semantic chart tokens as per-app extensions if the QC charts
      read them at runtime; map onto the shared base where possible.
- [ ] **2.3** — Remove `chart.js` once all QC surfaces are ported.

✅ **Done-when:** every QC chart (media-móvil, correlación, CLSI-EP15,
Levey-Jennings) renders via @unovis with its control limits, regression, and
EP15 bands verified to match the current Chart.js output exactly (statistical
parity, signed off — see the 🛑 above, not eyeballed); lab-qc's semantic chart
tokens are mapped onto the shared base where possible and kept as per-app
extensions otherwise; `chart.js` is removed and the app builds clean. *(ES:
cada gráfico QC renderiza vía @unovis con sus límites de control, regresión y
bandas EP15 verificados como idénticos a la salida actual (paridad estadística,
firmada — ver el 🛑, no a ojo); los tokens semánticos de lab-qc mapean a la base
compartida donde se pueda y quedan como extensiones por app si no; `chart.js`
está fuera y el app compila limpio.)*

🚦 **Checkpoint 2 (exit).** Show gczuluaga: each ported QC chart in the browser
with the parity verification artifact (computed control limits / regression /
EP15 bands vs the current Chart.js output), and the diff removing `chart.js`.
This is the exit checkpoint — the plan is not archived until Checkpoints 0 and 1
have also been walked. Questions:
1. Why is statistical parity verified against computed output, not visual
   likeness? *(ES: ¿por qué se verifica la paridad contra la salida calculada y
   no contra el parecido visual?)*
2. Walk one QC chart end-to-end with gczuluaga, comparing rendered bands/limits
   against the old output. *(ES: recorre un gráfico QC de punta a punta con
   gczuluaga, comparando bandas/límites contra la salida anterior.)*

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions
> logged below for traceability.

**Open:**

- 🛑 **Gate release** — when app migration (Phase 1+) may start. Pending:
  gczuluaga confirms RFC 0008 accepted **and** Phase-0 foundation landed in the
  registry.
- 🛑 **Statistical-parity sign-off (lab-qc)** — confirming the ported QC charts
  match the current Chart.js statistics exactly. Pending: gczuluaga or the named
  QC owner verifies and records it on the tracking issue.

**Resolved during planning:**

- **@unovis as the shared charting standard** — chosen over Chart.js: F5-backed
  and dogfooded, Apache-2.0, SVG + CSS-variable-native (no JS color bridge),
  consumed copy-in via the shadcn-vue registry. *(RFC 0008 Q11, 2026-06-13.)*
- **Chart-token shape `--chart-1..5`** — adopt shadcn-vue's native numbered
  chart-token convention, colored from the family palette. *(RFC 0008 Q11,
  2026-06-13.)*

## Risks · Riesgos

> **Resumen (ES).** Lo que puede salir mal: que la paridad estadística de
> lab-qc se valide a ojo (bug de correctitud), la comunidad más delgada de
> @unovis (tiempo de aprendizaje), y que el alcance ensanche el design system
> hacia data-viz (superficie de mantenimiento).

- **Statistical-chart parity (lab-qc)** → the QC charts encode clinical
  statistics; a port that looks right but computes/renders bands wrong is a
  correctness bug. **Mitigation:** gate Phase 2 on the statistical-parity
  sign-off (the 🛑 in Phase 2) — verify computed output, not eyeballing.
- **Thinner community than Chart.js** → fewer SO answers; slower debugging.
  **Mitigation:** budget learning time in Phase 0 while prototyping in the
  playground, before any app migration depends on it.
- **Scope creep into data-viz** → this widens the design system into a
  data-viz maintenance surface. **Mitigation:** courtesy-ratified with
  @SKuger01 alongside RFC 0008; keep the shared components minimal
  (area/bar/line/donut + legend/tooltip) and push domain specifics to per-app
  token extensions.

## References

- RFC 0008 Q11 (`rfcs/0008-pharos-design-system.md` — decision-walk now inlined as Appendix A).
- shadcn-vue charts (built on @unovis): <https://www.shadcn-vue.com/charts>.
- @unovis: <https://unovis.dev/> · <https://github.com/f5/unovis> (Apache-2.0).
- Tracking issue: Interval-Col/.github#25.
