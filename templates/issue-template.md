<!--
ISSUE-BODY TEMPLATE — the team-facing entry point for a plan.

Pairs with `templates/plan-template.md`. The **plan** is the source of
truth (the full contract: phases, Done-when, checkpoints); this **issue**
is the short, bilingual front door that points at it. Authoring guidance:
`.github/agents/plan-craft.agent.md` § "Plan ≠ Issue".

Golden rule: **do NOT restate the plan here — link to it.** If you find
yourself copying phases or Done-when criteria into the issue, stop; that
content lives in the plan and drifts the moment you duplicate it.

Title convention (issue title field, not in the body):
  `type(scope): short imperative description`
  `type` ∈ feat | fix | refactor | test | chore | docs | hotfix | ci
  — same vocabulary as Conventional Commits and branch names
  (`type/scope-short-description`). Examples:
    feat(quotes): MVP quote generation
    refactor(auth): move CSRF handling to shared middleware
    chore(ci): roll out gitleaks required check

Fill the `<…>` placeholders. The `> **Resumen (ES).**` line is REQUIRED
— one Spanish line so a monolingual reader knows what this issue is for
before the English. Delete this comment when you start filling in.
-->

> **Resumen (ES).** <Una línea en español: qué se construye/arregla y
> para quién. El detalle completo está en el plan enlazado abajo — esta
> issue solo es la puerta de entrada.>

<One or two English sentences: what this issue covers and why now. Not a
phase list — that is the plan's job.>

## Plan · Plan

**Source of truth:** [`<repo>/plans/<project>-plan.md`](<relative-or-gh-link>)

The plan carries the phases, `✅ Done-when` criteria, and `🚦`
checkpoints. Execute against the plan, not against this issue.
*(ES: la verdad está en el plan — ejecuta contra el plan, no contra esta
issue.)*

## Scope · Alcance

- **In scope:** <one line — the slice this issue tracks. If the plan has
  multiple phases, name which ones this issue covers.>
- **Out of scope:** <one line, or "see the plan's *Out of scope* section.">

## Done when · Terminado cuando

This issue closes when the plan's `✅ Done-when` lines for the phases in
scope are **verified** (not just coded) and every `🚦` checkpoint in
range has been walked with the checkpoint owner. *(ES: esta issue se
cierra cuando el `Done-when` del plan está verificado — no solo escrito —
y los `🚦` en alcance se recorrieron con quien los revisa.)*

- [ ] All in-scope phases complete and pushed
- [ ] Frontend verified in the browser (if UI is touched — a `200` is not a feature)
- [ ] `🚦` checkpoint(s) walked with the checkpoint owner

## People · Personas

| Role | Handle |
|---|---|
| Assignee(s) · Quién ejecuta | <@handle> |
| Lead · Líder | @gczuluaga |
| Checkpoint owner · Revisor de checkpoints | <@handle or @gczuluaga> |

## Execution order · Orden de ejecución

<Only if this issue interacts with other plans/issues. State the order
and the blocker. e.g. "Blocked by #NN (schema migration must land first)."
If standalone, write "Standalone — no cross-plan ordering.">
*(ES: si depende de otra issue/plan, di el orden y el bloqueo aquí.)*

## Working vocabulary · Vocabulario

- **Commits / branches** follow Conventional Commits with a **mandatory
  scope**: `type(scope): description` and `type/scope-short-description`.
  `type` ∈ `feat | fix | refactor | test | chore | docs | hotfix | ci`.
  *(ES: Conventional Commits con `(scope)` obligatorio; la rama refleja
  el commit.)*

<!--
LABELS / PROJECT HINTS (set via the GitHub UI or `gh`, not in the body):
  - type label mirrors the title `type`:
      feat→enhancement · fix/hotfix→bug · docs→documentation ·
      chore/ci/refactor/test→maintenance
  - scope/area label: the `(scope)` from the title (e.g. `area:auth`,
    `area:quotes`).
  - status: `status:planned` on open; flip to `status:in-progress` /
    `status:blocked` as it moves.
  - add to the team Project board and set the milestone if the plan
    targets one.
  - `gh issue create --title "feat(scope): …" --body-file <this> \
       --label enhancement,area:scope,status:planned --assignee <handle>`
-->
