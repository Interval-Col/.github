<!--
OPS / DEVOPS PLAN TEMPLATE — copy into `Interval-Col/operations/plans/` as a
kebab-case `<project>-plan.md`. Use this (NOT plan-template.md) for
devops/deploy/ops execution plans: promote `develop→main`, deploy, migrate a
repo to build-once-promote, rotate secrets, bootstrap a repo, roll out branch
protection. Product/app-feature plans use `plan-template.md`.

WHAT THIS TEMPLATE DROPS vs the full plan-template: the canonical preamble trio
— "How to use this plan", "Conventions", "Working rules". Those onboard the
junior, Spanish-native team; ops plans are run by the lead or a Sonnet agent,
so they are dead weight here. Everything else still applies.

STILL REQUIRED: the frontmatter schema v2 (eight keys), the bilingual title,
the top-of-plan Spanish Resumen, the per-phase Spanish Resumen with a
one-line-per-task list, ✅ Done-when on every phase, 🛑 escalation on choices an
agent must not make, and 🚦 Checkpoints on real gates. Keep Steps
self-contained so `claude-sonnet-4-6` can execute without Opus-level judgment.

FRONTMATTER SCHEMA v2 — see plan-template.md / plan-craft.agent.md. The eight
required keys populate the GitHub project board. `status` enum (= board
columns): proposed → active → in-progress → blocked → done; terminal:
superseded | abandoned. `issue` is the board item + entry point — every plan
gets one unless `issue: none — <reason>`.

Delete this comment when you start filling in.
-->
---
status: proposed
owner: <github-handle>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
issue: <Interval-Col/operations#NN  ·  or:  none — reason>
start: <YYYY-MM-DD>
target: <YYYY-MM-DD>
implementation: <github-handle or "TBD">
model: claude-sonnet-4-6
sources: [<target-repo>, <target-repo-2>]
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# <Ops project name> · <Nombre del proyecto>

> **Resumen (ES).** <3–6 líneas en español: qué operación es (promover,
> desplegar, migrar, rotar secretos…), sobre qué host/repo, por qué ahora, y
> cuál es el resultado esperado. Un lector monolingüe termina esto y sabe qué
> va a pasar.>

<One short English paragraph: what this ops procedure does, the blast radius,
and the urgency if any. Two or three sentences.>

> **Markers** — ✅ **Done-when** (verifiable definition of done) · 🚦
> **Checkpoint** (stop, show <owner> the named evidence) · 🛑 **HUMAN DECISION**
> (an agent must not pick this — escalate to <owner>) · 💡 **Heuristic**
> (a task-earned lesson). *(ES: ✅ terminado-cuando · 🚦 punto de control ·
> 🛑 decisión humana · 💡 heurística.)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que se repiten en este plan,
> con su traducción y una línea de qué significan.

| English | Español | Means |
|---|---|---|
| <e.g. build-once-promote> | <construir-una-vez-promover> | <build one artifact, promote the same image dev→prod> |
| <e.g. branch protection> | <protección de rama> | <required checks/reviews before merge to a branch> |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance.

- <Item 1 — what's deferred.>
- <Item 2>

---

## Phase 1 — <Bootstrap / first gate>

> **Resumen (ES) — Fase 1: <nombre>.**
>
> <1–2 líneas: qué logra esta fase y por qué va primero.>
>
> En orden, las tareas:
>
> 1. **1.1** — <una línea en español resumiendo la tarea 1.1.>
> 2. **1.2** — <una línea en español resumiendo la tarea 1.2.>
>
> <Si hay una 🛑 decisión humana, nómbrala aquí: "Decisión humana: …".>

- [ ] **1.1** — <First concrete step. Exact commands, `gh` invocations, repo +
      branch, expected output.>
- [ ] **1.2** — <Next step.>
  - **Why:** <One line on the non-obvious decision, only if needed.>

🛑 **HUMAN DECISION — <name>.** <Why an agent must not guess; what to confirm;
with whom; where the answer is recorded.> *(ES: <gloss>.)*

✅ **Done-when:** <Literal, executable verification — a command the operator
runs and the output they should see (e.g. `gh run list` shows green; the prod
endpoint returns the new version).> *(ES: <gloss>.)*

🚦 **Checkpoint 1.** Show <owner>: <named evidence — the green CI run, the
deployed version string, the branch-protection API excerpt>.

---

## Phase 2 — <Next phase>

> **Resumen (ES).** <2–4 líneas + lista de tareas.>

- [ ] **2.1** — <step>
- [ ] **2.2** — <step>

✅ **Done-when:** <criteria.> *(ES: <gloss>.)*

<Add 🚦 Checkpoint only on a real gate — the promote, the cutover, the exit.>

---

## Decisions · Decisiones

**Open:**

- 🛑 **<Decision name>** — <one-line>. Pending: <who decides, what's needed>.

**Resolved during planning:**

- **<Decision name>** — <what was decided and why>. *(YYYY-MM-DD.)*

## Risks · Riesgos

> **Resumen (ES).** <Una línea: qué puede salir mal y dónde está la mitigación.>

- **<Risk name>** → <consequence>. **Mitigation:** <concrete move at a specific
  point — and the rollback if it goes wrong>.

## References

- <Counterpart plan / RFC / runbook (`operations/runbooks/…`) / `gh` docs.>
