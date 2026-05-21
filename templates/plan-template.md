<!--
PLAN TEMPLATE — copy this file into the target repo's `plans/` directory
as a kebab-case `<project>-plan.md`. Fill in the placeholders marked
`<…>`. The Marker Vocabulary (💡 🛑 ✅ 🚦), the "How to use this plan"
preamble, the Conventions table, and the Working rules are CANONICAL —
copy them verbatim; only the commit-message example may be adjusted to
the project domain.

Two Spanish-support surfaces are REQUIRED (they replace per-bullet ES
glosses, which bloat the doc):
  - **Glossary section** — fill in 5–12 entries with the technical
    terms this plan keeps using.
  - **Per-phase Resumen** — must list every task in 1 Spanish line
    before the English task block, so a Spanish-native reader gets a
    full map of the phase up front.

Full authoring guidance: see `.github/agents/plan-craft.agent.md`.
Reference plans worth imitating (they predate the Glossary +
task-by-task Resumen convention, so use them for tone and structure,
not as exact-density references):
  - admission-patient/plans/finance-lch-integration-plan.md
  - admission-patient/plans/org-standards-harmonization-plan.md
  - commercial-lch/plans/mvp-quote-generation-plan.md

Delete this comment when you start filling in.
-->
---
status: pending
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
owner: <github-handle>
implementation: <github-handle or "TBD">
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# <Project name> · <Nombre del proyecto>

> **Resumen (ES).** <3–6 lines, in Spanish, describing the whole
> project: the goal, the user, the rough shape. A monolingual reader
> finishes this and knows what the project is.>

<One short English paragraph: what the project is, why it exists,
urgency if any. Two or three sentences, not a wall of text.>

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
plan*, not a failing in you — stop and ask <owner>. A question costs
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
plan*, no una falla tuya — pregúntale a <owner>. Y si el inglés te
frena: cada sección tiene un **Resumen** en español, y tu agente de IA
te traduce o explica cualquier parte en español si se lo pides — hazlo
sin problema.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| 💡 **Heuristic** | A short engineering or working lesson. Worth 30 seconds. *(ES: heurística — lección breve.)* |
| 🛑 **HUMAN DECISION** | A choice the plan deliberately does not make. **Do not let an agent pick it.** Escalate to <owner>. *(ES: decisión humana — no la toma un agente; escala a <owner>.)* |
| ✅ **Done-when** | The Definition of Done. The phase is verified only when every line is literally true. *(ES: terminado-cuando — definición de "hecho".)* |
| 🚦 **Checkpoint** | Stop. Show <owner> the named evidence and answer the questions before continuing. **Mandatory stop — including in auto mode** (see Working rules). *(ES: punto de control — alto obligatorio, también en modo auto.)* |

> **On the checkpoints.** Each 🚦 lists evidence to show and questions to
> answer. The questions are **not a test of you** — they test whether
> the plan explained things well enough. <owner> may also ask any of
> them at any time. *(ES: las preguntas del checkpoint no son un examen
> tuyo — prueban si el plan explicó bien; <owner> puede preguntarlas en
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
  `type(scope): description` — e.g. `feat(<domain>): <description>`.
  `type` ∈ `feat|fix|chore|docs|refactor|test|ci`. The `(scope)` is
  **mandatory**. Branch names mirror it: `type/scope-short-description`.
  *(ES: Conventional Commits; el `(scope)` es obligatorio; la rama
  refleja el commit.)*
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

5–12 entries — keep it to the English terms that recur across the plan
and that a Spanish-native reader could plausibly stumble on. Skip
universal terms (`URL`, `JSON`, `git`); skip terms that only appear
once.

| English | Español | Means |
|---|---|---|
| <e.g. compat shim> | <capa de compatibilidad> | <a temporary endpoint that speaks the old API shape while the client catches up> |
| <e.g. payload> | <cuerpo de la petición / payload> | <the JSON body sent in a POST/PATCH> |
| <e.g. Done-when> | <terminado-cuando> | <the literal checkable list that means the task is verified> |
| <e.g. commit + push> | <hacer commit y push> | <save to git locally **and** send to GitHub — both verbs> |
| <e.g. slice> | <rebanada / unidad de trabajo> | <a small piece of work that can ship on its own> |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> v1+ / para después. Si un agente sugiere construir algo de esta lista,
> no lo hagas.

Explicitly out of scope — not for this plan:

- <Item 1 — what's deferred and why is implicit (label says it all).>
- <Item 2>
- <Item 3>

---

## Phase 1 — <Bootstrap / foundation phase name>

> **Resumen (ES) — Fase 1: <Spanish phase name>.**
>
> <1–2 lines in Spanish: what this phase achieves and why it comes
> first.>
>
> En orden, las tareas:
>
> 1. **1.1** — <one Spanish line summarising task 1.1.>
> 2. **1.2** — <one Spanish line summarising task 1.2.>
> 3. **1.3** — <one Spanish line summarising task 1.3.>
>
> <If the phase has an open 🛑 HUMAN DECISION, name it on its own line:
> "Decisión humana: …".>

<Optional 1–2 line English context — only if the Resumen leaves
something unclear.>

- [ ] **1.1** — <First concrete task. Be specific: file paths,
      commands, exact endpoint shapes if known.>
- [ ] **1.2** — <Next task.>
  - **Why:** <One short paragraph on the non-obvious decision behind
    this task. Skip if the task is self-explanatory.>
- [ ] **1.3** — <Next task.>
  - 💡 **Heuristic.** <A short, task-earned engineering lesson — 2–4
    lines, never generic. Only add if this phase genuinely teaches
    something. If not, omit.> *(ES: <heurística en español, si
    aplica>.)*

✅ **Done-when:** <Literal, executable verification criteria. Each line
is something the implementer can *do* and observe. "The app at
`http://localhost:5174` shows the new page" — yes. "The frontend
works" — no.> *(ES: <gloss>.)*

🚦 **Checkpoint 1.** Show <owner>: <named evidence — the pushed
commit, the table in the DB, the page in the browser, the green CI
run>. Questions:
1. <An open-ended "why" question about a decision made in this phase.>
   *(ES: <gloss>.)*
2. <A second question that requires the implementer to walk an artefact
   live with <owner>, not just glance at it.> *(ES: <gloss>.)*

---

## Phase 2 — <Next phase name>

> **Resumen (ES).** <2–4 lines.>

<If this phase has a 🛑 HUMAN DECISION the implementer must escalate
*before* starting, place the marker here, prominently:>

🛑 **HUMAN DECISION — <name of the choice>.** <Why an agent must not
guess this; what needs to be confirmed; with whom; where the answer
gets recorded once made.> *(ES: <gloss>.)*

- [ ] **2.1** — <task>
- [ ] **2.2** — <task>
- [ ] **2.3** — <task>

✅ **Done-when:** <verification criteria.> *(ES: <gloss>.)*

<Add 🚦 Checkpoint here only if this phase is a meaningful gate.
Checkpoints belong at: foundation, first real UI, the core-loop, the
exit. Not on every phase.>

---

## Phase N — <Pattern>

> **Resumen (ES).** <…>

<Duplicate the structure above as needed. Typical patterns:>

- A *bootstrap* phase (Phase 1) usually warrants a 🚦 Checkpoint — the
  foundation is the most expensive thing to discover broken later.
- The *first phase that exposes UI* warrants a 🚦 Checkpoint — this is
  where "the FE wasn't checked" failure modes live.
- The *core-loop* phase (the user's end-to-end happy path) warrants a
  🚦 Checkpoint — the seam between layers is where bugs hide.
- The *exit* phase warrants a 🚦 Checkpoint — and its Done-when blocks
  archiving the plan until every earlier checkpoint has been walked.

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions
> logged below for traceability.

**Open:**

- 🛑 **<Decision name>** — <one-line description>. Pending: <who
  decides, what's needed>.

**Resolved during planning:**

- **<Decision name>** — <one-line summary of what was decided and why>.
  *(YYYY-MM-DD.)*

## Risks · Riesgos

> **Resumen (ES).** <Una línea sobre qué puede salir mal y dónde están
> las mitigaciones — sin generalidades.>

- **<Risk name>** → <consequence>. **Mitigation:** <what to do; when to
  do it — phrase mitigations as concrete moves at specific points in
  the plan, not vague "be careful.">
- **<Risk name>** → <consequence>. **Mitigation:** <…>

## References

- <Counterpart plan / RFC / agent file / external API doc — link with
  relative paths where possible.>
- <…>
