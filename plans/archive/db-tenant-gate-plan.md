---
status: done
owner: gczuluaga
created: 2026-07-07
updated: 2026-07-08
issue: Interval-Col/.github#106
start: 2026-07-07
target: 2026-07-21
implementation: gczuluaga
effort: M
language: English body; Spanish "Resumen" + decision/criteria glosses.
rfc: 0015
---

# db-tenant conformance gate · Gate de conformidad db-tenant

> **Resumen (ES).** El RFC 0015 (aceptado) define el "contrato de tenant" para
> las seis apps que comparten el cluster Postgres nucleus-db. Este plan ejecuta
> su Fase 1: el contrato normativo (`db-tenant-contract.md`), un workflow
> reusable (`db-tenant-check`) que cada app corre desde su propio CI, un
> dashboard de conformidad, un ciclo de convergencia en modo advisory, y al
> final el flip a check requerido. Nada de esto toca la base de datos — es
> CI + documentación.

Executes RFC 0015 Phase 1: the tenant contract + CI conformance gate, warn one
cycle → required (OQ4). Two of four landed tenants already drifted from ratified
standards; this moves the contract from markdown into CI, mirroring the gitleaks
rollout recipe.

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
  `type(scope): description` — e.g. `ci(db-tenant): <description>`.
  `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The `(scope)` is
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

| English | Español | Means |
|---|---|---|
| tenant (DB) | tenant / inquilino de la base | an app holding a connection to the shared `nucleus_db` cluster, owning or writing into schemas — NOT brand tenancy |
| manifest | manifiesto | the `.db-tenant.yml` file where each repo declares its shape (schemas, compose file, migrate chain) |
| gate / required check | check requerido | a CI status that must be green before a PR can merge |
| advisory mode | modo advisory | the gate runs and reports drift but never blocks a merge (`enforce: false`) |
| drift | drift / desviación | any gap between what the contract requires and what the repo actually does |
| one-shot | contenedor de un solo uso | a compose service that runs once to completion (migrate/seed) before the app starts |
| allowlist | lista de excepciones | manifest entries (file + reason) that exempt a specific known-good pattern from a check |
| readiness probe | sonda de readiness | the `/ready` endpoint that answers 200 only when the DB responds to `SELECT 1` |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> de otras fases del RFC 0015 o de otros sistemas.

- C-lite schema shells + grants (RFC 0015 Phase 2 — nucleus-db epic; ndb#64 is its first customer, do **not** grant-patch it here).
- The shared plumbing kit (Phase 3) and squawk/`database.agent.md` (Phase 4) — the gate leaves a slot; nothing more.
- telemetry (MySQL) and frozen pathology — not nucleus-db tenants.
- biuman-lis full conformance — it is not on nucleus-db yet; it adopts `profile: pre-onboarding` only.

---

## Phase 1 — Centerpiece in `.github`

> **Resumen (ES) — Fase 1: la pieza central.**
>
> El contrato, el script verificador y el workflow reusable, en el repo
> org-wide `.github`.
>
> En orden, las tareas:
>
> 1. **1.1** — Escribir el contrato normativo `db-tenant-contract.md`.
> 2. **1.2** — Escribir `scripts/db-tenant-check.py` (solo stdlib) y probarlo localmente contra los seis repos.
> 3. **1.3** — Escribir el workflow reusable `.github/workflows/db-tenant-check.yml`.
> 4. **1.4** — Cross-links en README, ENGINEERING_STANDARDS y BRANCHING-AND-DEPLOY.

- [x] **1.1** — `db-tenant-contract.md` at repo top level: clauses C1–C7, manifest schema, profiles, rollout recipe. Cites ADR 0004 / RFC 0005 / runbooks instead of restating.
- [x] **1.2** — `scripts/db-tenant-check.py`: stdlib-only (no PyPI on the merge path — same rule as `plan_lint.py`), strict mini-YAML manifest parser + compose scanner, checks T1–T7, `--enforce` / `--json`, `$GITHUB_STEP_SUMMARY` output. Verified locally against all six tenant repos; results match the RFC's audit (commercial 4×FAIL, ETL 1×FAIL, rest conformant).
  - 💡 **Heuristic.** A conformance gate's parsers must fail loudly on input they don't understand — a misparse that silently passes is worse than no gate. *(ES: si el parser no entiende algo, debe fallar ruidosamente; un falso "pasa" es peor que no tener gate.)*
- [x] **1.3** — Reusable workflow `db-tenant-check.yml`: `workflow_call`, `runner` JSON input (default `["self-hosted"]` — Team plan $0 hosted-minutes cap), `enforce` (default false), `manifest` path input; checks out the caller repo + this repo (for the script); no secrets.
- [x] **1.4** — Cross-links: README "Guides & standards" list; `ENGINEERING_STANDARDS.md` pointer; `BRANCHING-AND-DEPLOY.md` "pre-deploy migration gate" seam note.

✅ **Done-when:** the `.github` PR is merged to `main`; `python3 scripts/db-tenant-check.py --manifest <m>` run from each tenant repo root reproduces the audit table; the contract doc renders with all links resolving. *(ES: PR merged; el script reproduce la tabla del audit en los seis repos.)*

🚦 **Checkpoint 1.** Show gczuluaga: the local six-repo run output and the PR. Questions:
1. Why is the checker stdlib-only instead of using pyyaml? *(ES: ¿por qué el script no usa pyyaml?)*
2. Walk the commercial-lch FAIL rows — which open PRs fix which row? *(ES: recorre los FAIL de commercial y qué PR arregla cada uno.)*

---

## Phase 2 — Adoption wave (six repos, advisory)

> **Resumen (ES) — Fase 2: adopción en los seis repos.**
>
> Un PR por repo: el manifiesto `.db-tenant.yml` + el caller workflow en modo
> advisory. Para cobol-migration y biuman-lis este es su primer workflow de CI
> disparado por PR (hoy solo corren gitleaks).
>
> En orden, las tareas:
>
> 1. **2.1** — PRs a finance-lch, pharos-lis, commercial-lch, admission-patient (manifiesto + caller).
> 2. **2.2** — PRs a cobol-migration y biuman-lis (manifiesto + caller; primer PR-CI del repo).
> 3. **2.3** — Merge de `.github` primero; luego los seis (el caller referencia `@main`).

- [x] **2.1** — Caller PRs: finance-lch#106, pharos-lis#71 (manifest at `lab-qc/.db-tenant.yml`, paths repo-root-relative), commercial-lch#71, admission-patient#163. Standalone workflow file (never inside the app's `ci.yml` — same isolation rationale as `pharos-lint-check.yml`), `enforce: false`.
- [x] **2.2** — Caller PRs: cobol-migration#84 (`dml-only` profile, preflight allowlisted), biuman-lis#24 (`pre-onboarding`). Both retargeted from `main` to `develop` — these repos deploy on push to `main` (main merge = prod release; PRs go develop-first).
- [ ] **2.3** — Merge order: `.github` PR first (callers reference the reusable workflow `@main` — they parse-fail until it exists), then the six adopters in any order.

✅ **Done-when:** every tenant repo has a green (advisory) `db-tenant-check` run on its default branch; commercial-lch and cobol-migration show their known drift as annotations, not failures. *(ES: los seis repos corren el check en verde-advisory; commercial y ETL muestran su drift como anotaciones.)*

---

## Phase 3 — Conformance dashboard

> **Resumen (ES) — Fase 3: dashboard.**
>
> Una tabla markdown (fila por app, green/drift) en
> `operations/ops/db-tenant/DASHBOARD.md`, siguiendo el patrón de
> plan-sweep/estate-hygiene. Nunca GitHub Pages (en el plan Team, Pages de un
> repo privado se sirve público).
>
> 1. **3.1** — Crear el dashboard sembrado con los resultados reales del audit.
> 2. **3.2** — Documentar cómo se refresca (re-run local o `--json` de los runs de CI).

- [ ] **3.1** — `operations/ops/db-tenant/DASHBOARD.md`: row per app (status, failing checks, tracking links com#68/#69, ETL `/ready`, biuman Phase-2). Seeded from the verified local runs.
- [ ] **3.2** — A "how to refresh" note in the same file (re-run the six-repo loop; the check's `--json` output is the machine-readable row source if this later automates).

✅ **Done-when:** the dashboard is merged in `operations`, matches the latest real check output, and is linked from the contract doc. *(ES: dashboard merged y consistente con la última corrida real.)*

---

## Phase 4 — Convergence (close the drift)

> **Resumen (ES) — Fase 4: convergencia.**
>
> Cerrar el drift conocido durante el ciclo advisory: commercial (TLS/DSN ya
> abiertos como #68/#69 + wiring del migrate) y el `/ready` del ETL.

- [x] **4.1** — commercial-lch: #68 (URL-encode DSN + TLS) + #69 (cross-schema read doc) merged; un-park `commercial-migrate` (removed `profiles:`, kept `depends_on` chain) in #73 — T2/T4/T5 green.
- [x] **4.2** — commercial-lch: `/ready` with DB probe added in #73 (canonical lab-qc shape) — T6 green. Also folded C-lite env.py (guard `CREATE SCHEMA` behind `has_schema()`) so `commercial_user` needs no CREATE ON DATABASE (crm shell = nucleus-db#71).
- [x] **4.3** — cobol-migration: add `/ready` (DB `SELECT 1`) alongside the existing `/health` — T6 green. *(Rides cobol-migration#84 together with the enforce flip; verified conformant under `--enforce`.)*

✅ **Done-when:** all six repos report **conformant** (or documented-informational) on their default branches. *(ES: los seis repos en "conformant" en su rama default.)*

---

## Phase 5 — Flip to required

> **Resumen (ES) — Fase 5: el flip.**
>
> Con todo verde, cambiar `enforce: true` por repo y marcar `db-tenant-check`
> como check requerido en branch protection. Decisión humana: el momento del
> flip lo decide gczuluaga por repo.

~~🛑 HUMAN DECISION — flip timing per repo.~~ **RESOLVED 2026-07-08
(gczuluaga): flip all six immediately** — every adopter was green on day one;
required contexts armed everywhere; `enforce: true` rides the convergence PRs
in the two drifting repos so nothing blocks. Standing rule: new apps comply
from day one. *(ES: decidido — flip inmediato en los seis; apps nuevas cumplen
desde el día uno.)*

- [x] **5.1a** — Required context `db-tenant-check / db-tenant-check` added to branch protection on `develop`+`main` in all six repos (2026-07-08).
- [x] **5.1b** — `enforce: true` per repo — all merged 2026-07-08: finance-lch#109 · pharos-lis#72 · admission-patient#164 · cobol-migration#84 (rider, +`/ready`) · biuman-lis#24 (pre-onboarding) · **commercial-lch#73** (converge, after #68).
- [x] **5.2** — Update `BRANCHING-AND-DEPLOY.md` required-checks section to list `db-tenant-check` for tenant repos (#108); the "pre-deploy migration gate" open item was already updated in #107.
- [x] **5.3** — RFC 0015 Phase 1 checkboxes ticked (rfcs#93); this plan flipped to `status: done`.

✅ **Done-when:** every tenant repo blocks merges on contract drift; docs updated; RFC 0015 §Phase 1 boxes ticked. *(ES: los seis repos bloquean merges por drift; docs y RFC actualizados.)* — **met 2026-07-08.**

🚦 **Checkpoint 2 (exit) — satisfied in practice.** No separate broken-PR demo
was staged; the equivalent live evidence is **commercial-lch#73**, whose own
`enforce: true` `db-tenant-check` ran against itself and had to be green to
merge — a self-enforcing gate proving drift blocks. Answers on record: **(1)**
a buggy checker after the flip is fixed centrally in `.github@main` and heals
every tenant at once (the check is checked out from `@main` per run); the
per-repo escape hatch is a manifest allowlist entry with a reason. **(2)** still
prose-only: C6 pool/retry baseline (machine-checked when the Phase 3 kit lands)
and the migration-safety clauses (RFC 0015 Phase 5 / squawk in Phase 4).

---

## Decisions · Decisiones

**Open:** *(none)*

**Resolved during execution:**

- **Flip all six immediately (OQ4 superseded)** — every adopter green on day one; required contexts armed on develop+main across the six; enforce rides the convergence PRs (commercial, ETL) so no lane blocks; new apps comply from day one. Decision: gczuluaga. *(2026-07-08.)*

**Resolved during planning:**

- **Reusable workflow over copy-in** — the check must evolve centrally (contract tightening propagates without 6 sync PRs); copy-in stays the pattern for runtime code (Phase 3 kit). Precedent: `auto-add-to-project.yml`. *(2026-07-07.)*
- **stdlib-only checker** — no PyPI on the merge path (gitleaks pinned-binary lesson; `plan_lint.py` precedent). *(2026-07-07.)*
- **Per-repo manifest (`.db-tenant.yml`)** — RFC 0012 structural template: per-repo declaration, shared mechanism; the manifest doubles as the allowlist ledger (every exception carries a reason). *(2026-07-07.)*
- **biuman-lis adopts as `pre-onboarding`** — audit showed it is not on nucleus-db yet (own Postgres, no `sports_lab`); full contract applies at Phase-2 onboarding. *(2026-07-07.)*

## Risks · Riesgos

> **Resumen (ES).** Los riesgos reales son falsos positivos del gate después
> del flip y el acople al merge de `.github`.

- **False positive blocks all merges after the flip** (solo-gatekeeper repos: CI *is* the gate) → **Mitigation:** heuristics are narrow + allowlist-with-reason escape hatch; one full advisory cycle on real PRs before any flip; the script lives centrally, so a fix in `.github@main` heals every repo at once.
- **Caller PRs red until `.github` merges** → **Mitigation:** explicit merge order in every caller PR body (Phase 2.3); advisory mode means nothing blocks either way.
- **Compose/manifest layout the parsers don't understand** → **Mitigation:** parsers fail loudly (FAIL, never silent pass); the six real repos are already parsed correctly (verified 2026-07-07).

## References

- `rfcs/0015-shared-db-tenant-contract.md` (§Phase 1) + rfcs#91/#92
- `db-tenant-contract.md` (this repo, the normative artifact)
- nucleus-db ADR 0004 · RFC 0005 §2.1 · RFC 0012 (structural template)
- `BRANCHING-AND-DEPLOY.md` §Hooks (gitleaks rollout recipe) + §Open items (migration-gate seam)
- `operations/guides/base-compartida-nucleus-db.md` (conceptual explainer)
- Tracking: Interval-Col/.github#106 · quick-wins commercial-lch#68/#69
