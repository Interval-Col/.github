---
status: active
created: 2026-06-01
updated: 2026-06-29
owner: gczuluaga
implementation: gczuluaga
language: English body; Spanish "Resumen" + decision/criteria glosses.
home: Interval-Col/.github (org-level — this automation spans every repo's trackers, so it lives here, not in any single app repo)
related:
  - Interval-Col/rfcs#4 (digest thread where the tracker convention was announced)
  - trackers it operates on: Interval-Col/finance-lch#1, Interval-Col/nucleus-db#1,
    Interval-Col/nucleus-db#2, Interval-Col/rfcs#3, Interval-Col/admission-patient#4,
    Interval-Col/admission-patient#5, Interval-Col/commercial-lch#1, Interval-Col/commercial-lch#2
note: >
  End-of-day automation to keep the org's GitHub issue trackers current.
  v1 (central, propose-only) chosen 2026-06-01 as the starting shape;
  v2 (per-dev) and v3 (auto-apply high-confidence) are PARKED here so we
  don't forget them — they are the graduation path, not day-one scope.
---

# EOD tracker-hygiene automation · Automatización de higiene de trackers (fin de día)

> **Resumen (ES).** Una rutina programada de Claude Code se despierta al final
> del día laboral, lee el trabajo fusionado del día y lo reconcilia contra las
> casillas (`- [ ]` / `- [x]`) de los trackers de issues del org en GitHub —
> en vez de la pasada manual que hicimos el 2026-06-01. Es un asunto **a nivel
> de org** (toca trackers en cada repo de app), por eso vive en
> `Interval-Col/.github` y no en el `plans/` de una sola app. La confianza se
> gana por fases: **v1** (central, solo propone) ya está EN VIVO; **v2**
> (rutina por dev) y **v3** (auto-aplicar lo de alta confianza) están
> APARCADAS como el camino de graduación, no como alcance del día uno.

Keep the cross-repo trackers honest **automatically**, instead of by the
manual pass we ran 2026-06-01. A scheduled Claude Code routine wakes at the
end of the working day, reads the day's merged work, and reconciles it
against the trackers' checklists. This is an **org-level** concern — it touches
trackers in every app repo — so the plan lives in `Interval-Col/.github`, not
in any single app's `plans/`.

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
  `type(scope): description` — e.g. `chore(trackers): add eod hygiene routine`.
  `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The `(scope)` is
  **mandatory**. Branch names mirror it: `type/scope-short-description`.
  *(ES: Conventional Commits; el `(scope)` es obligatorio; la rama
  refleja el commit.)*
- **Merge mode is merge-commit, everywhere.** "Allow squash merging" is
  **off** org-wide; merge PRs with a merge commit so the conventional-commit
  history is preserved intact. *(ES: el modo de merge es merge-commit en todo
  el org — el squash está deshabilitado.)*
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
| tracker | tracker / issue de seguimiento | the long-lived GitHub issue that holds a project's checklist of work items |
| task-list checkbox | casilla de lista de tareas | a native `- [ ]` / `- [x]` line — the single source of progress truth, which rolls up in GitHub |
| routine | rutina (agente programado) | a scheduled Claude Code cloud agent that runs on a cron, here at end-of-day |
| propose-only | solo-propone | the routine comments a suggestion but never edits the checkbox itself; the human ticks it |
| auto-apply | auto-aplicar | the routine ticks high-confidence boxes by itself (v3) — needs write permission and guardrails |
| EOD | fin de día | end-of-day — when the routine wakes to reconcile the day's merged work |
| graduation path | camino de graduación | the staged way trust is earned: v1 → v2 → v3, not all at once |
| Done-when | terminado-cuando | the literal checkable list that means the task is verified |
| commit + push | hacer commit y push | save to git locally **and** send to GitHub — both verbs |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte del alcance del día uno
> (v1) — es la ruta de graduación / para después. Si un agente sugiere
> construir algo de esta lista ahora, no lo hagas: v2 y v3 tienen
> prerrequisitos explícitos.

Explicitly out of scope for **v1** (these are the graduation path, kept in
the Phases section so they are not forgotten — not day-one work):

- **Per-dev routines under each dev's own identity (v2)** — deferred until
  every dev is on Claude Code and has created their own routine.
- **Unattended auto-ticking of checkboxes (v3)** — deferred until v1's
  suggestions are demonstrated reliable; introduces unattended **writes** to
  trackers and the write-action guardrails that go with them.
- **Trackers that are co-creation / parked, not week-to-week movers** — only
  the active `eodWatch` set is checked nightly.

---

## The convention it enforces (already agreed) · La convención que hace cumplir

> **Resumen (ES).** La rutina hace cumplir dos reglas ya acordadas en el hilo
> del digest (Interval-Col/rfcs#4): (1) las **casillas nativas** son la única
> fuente de verdad del progreso — un `✅` en prosa NO cuenta y es decoración;
> (2) una línea visible **`Blocked by: #N`** donde exista una dependencia real.

Announced in the digest thread (Interval-Col/rfcs#4):

1. **Native task-list checkboxes** (`- [ ]` / `- [x]`) are the single source
   of progress truth — `✅`-in-prose does NOT roll up and is decoration only.
2. A visible **`Blocked by: #N`** line where a real dependency exists.

💡 **Heuristic.** A *wrong* tick is worse than no tick: it tells the
gate-keeper something is finished when it isn't. Mapping a day's commits/PRs to
checklist items is a **guess** — "fix payer modal" does not cleanly map to
"Phase 4 — Payers · done." We tripped the write-action safety rails twice doing
this by hand with a human watching; an unattended nightly cron multiplies that
risk. That is exactly why v1 is propose-only and trust is earned in phases.
*(ES: una marca equivocada es peor que ninguna — por eso v1 solo propone y la
confianza se gana por fases.)*

---

## Phase 1 — v1: Central, propose-only  ✅ LIVE 2026-06-02

> **Resumen (ES) — Fase 1: v1 central, solo-propone (EN VIVO 2026-06-02).**
>
> Una sola rutina central, bajo @gczuluaga, lee los PRs fusionados del día en
> los repos activos y publica **un** comentario "tracker check-in" por tracker
> activo, sugiriendo qué casillas marcar y @-mencionando al dueño. **No edita
> nada** — el humano marca la casilla, riesgo de marca-equivocada = cero. Se
> corre ~1 semana y se afinan las señales antes de graduar.
>
> En orden, las tareas:
>
> 1. **1.1** — La rutina ya está parada: `trig_01WTXhtzpJfFzRgZSqnCxdQC`, cron
>    de días laborales 19:00 Bogotá, modelo sonnet, env "Interval-Col GH".
> 2. **1.2** — Vigila los 4 trackers activos del set `eodWatch`.
> 3. **1.3** — Lee los PRs fusionados del día por autor, desde git.
> 4. **1.4** — Publica un comentario de sugerencia por tracker, sin auto-editar.
> 5. **1.5** — Córrela ~1 semana y afina qué señales merece confiar.

- [x] **1.1** — Stand up the routine `trig_01WTXhtzpJfFzRgZSqnCxdQC` (manage at
      claude.ai/code/routines), owner @gczuluaga, cron `0 0 * * 2-6` = weekdays
      19:00 Bogotá, model sonnet-4-6, tools Bash/Read/Grep, env
      **"Interval-Col GH"**. Manual test run 2026-06-02 returned 200
      (GitHub access OK).
- [x] **1.2** — Watch the **4 active execution-trackers** (the `eodWatch` set
      from the 2026-06-02 portfolio triage): commercial-lch#1,
      admission-patient#4, admission-patient#5, nucleus-db#5.
  - **Why:** finance-lch#1 + nucleus-db#2 were closed in that triage; the
    others are co-creation/parked, not week-to-week movers — checking them
    nightly is cost with no signal.
- [x] **1.3** — Read the day's merged PRs across the active repos (by author,
      from git).
- [x] **1.4** — Post **one "tracker check-in" comment** per active tracker:
      *"Looks done today: suggest ticking 1.4, 1.5 on #4 — confirm?"* and
      @-mention the owner. **No auto-edits** — the human ticks the box, zero
      mismark risk.
- [x] **1.5** — Run it ~1 week; tune which signals it trusts before graduating.

✅ **Done-when:** the routine `trig_01WTXhtzpJfFzRgZSqnCxdQC` exists and is
enabled on cron `0 0 * * 2-6` under @gczuluaga with env "Interval-Col GH"; a
manual run returns 200; a real nightly run posts exactly one propose-only
check-in comment per active `eodWatch` tracker, @-mentioning the owner, and
edits **no** checkboxes itself. *(ES: la rutina existe y está activa en su
cron; una corrida manual devuelve 200; una corrida real publica un comentario
solo-propone por tracker activo y no edita ninguna casilla.)*

🚦 **Checkpoint 1.** Show gczuluaga: the routine config screen (cron, env,
model, tools), the 200 from the manual run, and a real night's check-in
comments on the four `eodWatch` trackers. Questions:
1. Why is v1 propose-only rather than auto-applying — what's the cost of a
   wrong tick to the gate-keeper? *(ES: ¿por qué v1 solo propone? ¿qué cuesta
   una marca equivocada al gate-keeper?)*
2. Walk one real check-in comment live: did the suggested boxes actually match
   the day's merged work, and would you have ticked them? *(ES: recorre un
   comentario real en vivo — ¿las casillas sugeridas coincidían con el trabajo
   del día y las habrías marcado?)*

---

## Phase 2 — v2: Per-dev routines  ⏸ PARKED (graduation)

> **Resumen (ES) — Fase 2: rutinas por dev (APARCADA, graduación).** Cada dev
> corre **su propia** rutina EOD bajo **su propia identidad**, así conoce el
> trabajo real de su día y la atribución es correcta. **Prerrequisito:** que
> todos estén en Claude Code y hayan creado su rutina; hasta entonces, el modelo
> central de v1 es la única opción. Mejor precisión y autoría que el central, a
> cambio de más configuración por persona.

🛑 **HUMAN DECISION — when to graduate from v1 to v2.** An agent must not flip
this on: it requires confirming that **every dev is on Claude Code and has
created their own routine** under their own identity. Until that prerequisite
is met, v1's central model is the only option. gczuluaga decides when the
prerequisite is met; the decision gets logged below. *(ES: decisión humana —
no la toma un agente; requiere que todos los devs estén en Claude Code con su
rutina creada; gczuluaga decide y se registra abajo.)*

- [ ] **2.1** — Each dev runs their **own** EOD routine, under their **own
      identity**, so it knows their actual day's work and attribution is
      correct.
- [ ] **2.2** — Confirm the prerequisite is met: every dev is on Claude Code and
      has created their routine.
- [ ] **2.3** — Compare accuracy + authorship against v1's central model before
      retiring the central routine.

✅ **Done-when:** every active dev has a personal EOD routine running under
their own identity; the check-in suggestions carry correct authorship; and the
central v1 routine is either retired or explicitly kept as a fallback by a
logged decision. *(ES: cada dev activo tiene su rutina personal bajo su propia
identidad, con autoría correcta, y la rutina central v1 se retira o se mantiene
como respaldo por decisión registrada.)*

---

## Phase 3 — v3: Auto-apply high-confidence  ⏸ PARKED (graduation)

> **Resumen (ES) — Fase 3: auto-aplicar lo de alta confianza (APARCADA,
> graduación).** La rutina **solo auto-marca** las casillas cuyo PR nombra
> explícitamente el issue + el ítem (p. ej. rama/título `…#4 1.5`); todo lo
> difuso sigue siendo *sugerencia*. Solo después de que v1 haya demostrado que
> sus sugerencias son confiablemente correctas. Aquí es donde la rutina empieza
> a **escribir** a los trackers sin supervisión: necesita permiso de escritura
> con alcance y reaparecen los mismos guardarraíles de acción-de-escritura que
> tocamos a mano.

🛑 **HUMAN DECISION — turning on unattended writes.** An agent must not enable
auto-apply: this is the point where the routine starts **writing** to trackers
unattended. It needs scoped issue-edit permission and will surface the same
write-action guardrails we hit manually. Only graduate here **after v1 has
shown the suggestions are reliably right**, and only with gczuluaga's explicit
sign-off, logged below. *(ES: decisión humana — encender escrituras
desatendidas; requiere permiso de edición con alcance y el visto bueno explícito
de gczuluaga, registrado abajo, solo tras probar que v1 acierta.)*

- [ ] **3.1** — Routine **auto-ticks only** boxes whose PR explicitly names the
      issue + item (e.g. branch/title `…#4 1.5`); everything fuzzy stays a
      *suggestion*.
- [ ] **3.2** — Grant the routine scoped **issue-edit** permission (it already
      has issue-comment from v1).
- [ ] **3.3** — Re-validate against the write-action guardrails that surfaced
      during the manual passes before running it unattended.

✅ **Done-when:** the routine auto-ticks **only** boxes whose PR explicitly
names the issue + item; every fuzzy match remains a propose-only suggestion;
the routine has scoped issue-edit permission and runs unattended without
tripping the write-action guardrails. *(ES: la rutina auto-marca solo casillas
cuyo PR nombra explícitamente issue + ítem; lo difuso queda como sugerencia;
tiene permiso de edición con alcance y corre sin disparar los guardarraíles.)*

🚦 **Checkpoint 3 (exit).** This is the exit gate. Show gczuluaga: a run where
an explicit `#N i.j`-named PR auto-ticked its box AND a fuzzy match was left as
a suggestion; the scoped permission grant; and a clean unattended run. Do not
archive this plan until Checkpoint 1 has also been walked. Questions:
1. How does the routine distinguish an "explicit" match it may auto-tick from a
   "fuzzy" one it must only suggest — show the rule in the run? *(ES: ¿cómo
   distingue la rutina un match explícito (que puede auto-marcar) de uno difuso
   (que solo sugiere)? muéstralo en la corrida.)*
2. Walk the write-action guardrails live: what stops an unattended wrong write?
   *(ES: recorre los guardarraíles en vivo — ¿qué frena una escritura
   equivocada desatendida?)*

---

## Setup — how to connect GitHub (learned the hard way, 2026-06-02) · Cómo conectar GitHub

> **Resumen (ES).** El acceso a GitHub de una rutina **no** viene solo de la
> GitHub App del org. La rutina corre como agente en la nube y necesita el
> **token de GitHub de tu cuenta de claude.ai**, y llevarlo allí tiene dos
> requisitos no obvios: (1) corre `/web-setup` en la **CLI de terminal** (la
> extensión de VS Code no expone `/web-setup`); (2) usa un **entorno conectado a
> GitHub** ("Interval-Col GH"), no el "Default" genérico.

A routine's GitHub access does NOT come from the org GitHub App alone. The
routine runs as a cloud agent that needs **your claude.ai account's GitHub
token**, and getting it there has two non-obvious requirements:

1. **Run `/web-setup` in the TERMINAL CLI** — the **VS Code extension does not
   expose `/web-setup`**. Install the standalone CLI first
   (`npm install -g @anthropic-ai/claude-code`), run `claude` in a terminal
   (sign in as the **same account** that owns the routine), then `/web-setup`
   and authorize GitHub. This syncs the `gh` token the routine uses.
2. **Use a GitHub-connected environment** — after `/web-setup`, `/schedule`
   offers an env named **"Interval-Col GH"**. The old generic "Default" env
   fails with `github_repo_access_denied`.

**Red herrings that cost ~1 hour on 2026-06-02 (don't repeat):**

- Installing the org **GitHub App** (repos=all) — needed for interactive
  sessions, NOT sufficient for routines.
- The org's **"Access restricted" OAuth third-party policy** — irrelevant; the
  Claude integration is a **GitHub App**, not an OAuth App. Do NOT click
  "Remove restrictions"; it wouldn't help and weakens the org.
- Recreating the routine / waiting for propagation — neither fixed it.

🛑 **Failure signature (so you recognize it):** routine run → HTTP 400
`github_repo_access_denied` ("re-authorize GitHub in settings"); a scheduled
run auto-disables with `ended_reason: auto_disabled_repo_access`. *(ES: firma
del fallo — HTTP 400 `github_repo_access_denied`; una corrida programada se
auto-deshabilita con `ended_reason: auto_disabled_repo_access`.)*

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions
> logged below for traceability.

**Open:**

- 🛑 **Graduate v1 → v2 (per-dev routines)** — flip only once every dev is on
  Claude Code with their own routine. Pending: gczuluaga confirms the
  prerequisite is met.
- 🛑 **Graduate v1 → v3 (auto-apply unattended writes)** — enable only after v1
  suggestions are proven reliable. Pending: gczuluaga sign-off + scoped
  issue-edit permission + write-action guardrail re-validation.
- 🛑 **Schedule** — one fixed time (e.g. 19:00 America/Bogotá) vs per-dev EOD.
  *(v1 runs the fixed-time central model; per-dev EOD timing is a v2 question.)*
- 🛑 **Scope** — which repos/trackers are "active" enough to be worth a nightly
  check. *(v1 currently scopes to the 4 `eodWatch` trackers; revisit as the
  portfolio shifts.)*
- 🛑 **Cost** — cloud-agent tokens × repos × weekdays — confirm acceptable.
- 🛑 **Permission** — the routine needs issue-comment rights (v1, granted); an
  auto-apply (v3) routine needs issue-edit rights.

**Resolved during planning:**

- **v1 as the starting shape** — chose **v1 (central, propose-only)** as the
  starting shape; parked v2 (per-dev) + v3 (auto-apply) as the graduation path
  so they are not forgotten. (gczuluaga, *2026-06-01*.)
- **Plan home is org-level** — relocated this plan from `finance-lch/plans/` to
  `Interval-Col/.github/plans/` — it's org-level, not finance-specific.
  (gczuluaga, *2026-06-01*.)
- **v1 stood up and verified** — `trig_01WTXhtzpJfFzRgZSqnCxdQC`, env
  "Interval-Col GH"; manual run returned 200. Scoped to the 4 `eodWatch`
  trackers from that day's portfolio triage. (gczuluaga, *2026-06-02*.)
- **GitHub-connection requirement recorded** — `/web-setup` in the terminal CLI
  + a GitHub-connected env, after an hour of dead ends — see the **Setup**
  section. (gczuluaga, *2026-06-02*.)

## Risks · Riesgos

> **Resumen (ES).** Lo que puede salir mal está concentrado en dos puntos: una
> marca equivocada que engaña al gate-keeper, y el acceso a GitHub de la rutina
> que se cae con una firma de fallo específica. Las mitigaciones están en el
> diseño por fases y en la sección Setup.

- **Wrong tick misleads the gate-keeper** → a checkbox marked done when the
  work isn't tells the gate-keeper something shipped that didn't. **Mitigation:**
  v1 is propose-only (the human ticks); v3 auto-ticks **only** explicit
  `#N i.j`-named PRs and leaves fuzzy matches as suggestions; gate v3 behind
  Checkpoint 3 and write-action guardrail re-validation.
- **Routine loses GitHub access** → run returns HTTP 400
  `github_repo_access_denied`, scheduled run auto-disables
  (`ended_reason: auto_disabled_repo_access`). **Mitigation:** keep the
  `/web-setup`-synced token current and use the "Interval-Col GH" env (Setup
  section); recognize the failure signature instead of chasing the red herrings.
- **Nightly cost creep** → cloud-agent tokens × repos × weekdays can grow as
  the portfolio grows. **Mitigation:** scope to the `eodWatch` active-tracker
  set and revisit scope as the portfolio shifts (open Decision).

## References

- Interval-Col/rfcs#4 — digest thread where the tracker convention was announced.
- Trackers it operates on: Interval-Col/finance-lch#1, Interval-Col/nucleus-db#1,
  Interval-Col/nucleus-db#2, Interval-Col/rfcs#3, Interval-Col/admission-patient#4,
  Interval-Col/admission-patient#5, Interval-Col/commercial-lch#1,
  Interval-Col/commercial-lch#2; active `eodWatch` set: commercial-lch#1,
  admission-patient#4, admission-patient#5, nucleus-db#5.
- Routine: `trig_01WTXhtzpJfFzRgZSqnCxdQC` (manage at claude.ai/code/routines).
- Plan template + authoring guidance: `.github/templates/plan-template.md`,
  `.github/agents/plan-craft.agent.md`.
