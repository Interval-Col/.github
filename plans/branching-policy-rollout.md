---
status: in-progress
created: 2026-06-04
updated: 2026-06-16
owner: gczuluaga
implementation: gczuluaga
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# Branching & Deploy Policy — Per-Repo Rollout · Política de ramas y despliegue — Despliegue por repo

> **Resumen (ES).** Este plan rastrea, repo por repo, la aplicación de la
> política de ramas y despliegue (`BRANCHING-AND-DEPLOY.md`). Para cada uno de
> los siete repos en alcance fija el mismo conjunto: protección de ramas en
> `main` y `develop`, CODEOWNERS, plantilla de PR, workflow de stale, los 5
> hooks de pre-commit obligatorios, y la migración CI/CD a build-once-promote.
> El objetivo es llevar cada repo a "cumplido" sin perder de vista en qué etapa
> está cada uno. Las decisiones ya cerradas (GitFlow-lite, merge-commit vía PR,
> conventional commits, build-once-promote) **no** se debaten aquí — solo el
> trabajo de hacerlas reales por repo.

This plan tracks per-repo enforcement of the branching-and-deploy policy that
landed in [PR Interval-Col/.github#4](https://github.com/Interval-Col/.github/pull/4)
(`BRANCHING-AND-DEPLOY.md`), with companion org discussion at
[Interval-Col/rfcs#6](https://github.com/Interval-Col/rfcs/discussions/6). The
audit below was run on 2026-06-04 across the six repos in scope; this document
turns each audit's gap list into a per-repo checklist so we can roll out the
policy without losing track of which repo is at which stage. Locked decisions
(GitFlow-lite, merge-commit via PR, conventional commits, 5 pre-commit hooks,
build-once-promote, etc.) are not up for debate here — only the work to make
them real per repo.

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
plan*, not a failing in you — stop and ask @gczuluaga. A question costs
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
plan*, no una falla tuya — pregúntale a @gczuluaga. Y si el inglés te
frena: cada sección tiene un **Resumen** en español, y tu agente de IA
te traduce o explica cualquier parte en español si se lo pides — hazlo
sin problema.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| 💡 **Heuristic** | A short engineering or working lesson. Worth 30 seconds. *(ES: heurística — lección breve.)* |
| 🛑 **HUMAN DECISION** | A choice the plan deliberately does not make. **Do not let an agent pick it.** Escalate to @gczuluaga. *(ES: decisión humana — no la toma un agente; escala a @gczuluaga.)* |
| ✅ **Done-when** | The Definition of Done. The phase is verified only when every line is literally true. *(ES: terminado-cuando — definición de "hecho".)* |
| 🚦 **Checkpoint** | Stop. Show @gczuluaga the named evidence and answer the questions before continuing. **Mandatory stop — including in auto mode** (see Working rules). *(ES: punto de control — alto obligatorio, también en modo auto.)* |

> **Status-matrix legend (this plan's tracker uses a second, distinct
> vocabulary in the at-a-glance matrix below):** ✅ done · ⚠️ partial /
> nuance · ❌ missing · ❗ active problem · ⏸️ deferred · n/a not
> applicable · "develop only" = artifact exists on `develop` but **not on
> the default branch**, so it does not enforce (GitHub reads CODEOWNERS +
> produces Actions checks from the default branch). *(ES: la matriz de
> estado usa este segundo juego de íconos — no confundir con los markers
> de arriba.)*

> **On the checkpoints.** Each 🚦 lists evidence to show and questions to
> answer. The questions are **not a test of you** — they test whether
> the plan explained things well enough. @gczuluaga may also ask any of
> them at any time. *(ES: las preguntas del checkpoint no son un examen
> tuyo — prueban si el plan explicó bien; @gczuluaga puede preguntarlas en
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
  `type(scope): description` — e.g. `chore(lab-qc): add policy chrome`.
  `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The `(scope)` is
  **mandatory**. Branch names mirror it: `type/scope-short-description`.
  (`hotfix` and `ci` are both valid here — `hotfix` is a branch type *and*
  a commit type; `ci` was added org-wide for pipeline-only changes.)
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
| branch protection (BP) | protección de rama | the GitHub ruleset on `main`/`develop` that forces PR + checks + reviews before a merge |
| hollow protection | protección hueca | `main` requires checks whose producing workflows live only on `develop` — the rule exists but enforces nothing real |
| chrome | "chrome" / herrajes de gobierno | the governance files a repo needs: CODEOWNERS, PR template, `stale.yml`, `gitleaks.yml` |
| build-once-promote | construir-una-vez-y-promover | build the image once on `develop`, then retag the *same* digest `:dev → :prod` — never rebuild per env |
| promote (develop → main) | promover | a merge-commit PR carrying develop's state to main; for deploy repos it also retags the image to prod |
| pre-commit hook | hook de pre-commit | a local git check (gitleaks, ruff, branch-name-lint, etc.) that runs before a commit/push lands |
| required status check | check requerido | a CI job GitHub forces green before a PR can merge (e.g. `gitleaks`) |
| merge-commit model | modelo merge-commit | merges create a merge commit using the PR title; squash and rebase are **off** |
| Done-when | terminado-cuando | the literal checkable list that means the task is verified |
| commit + push | hacer commit y push | save to git locally **and** send to GitHub — both verbs |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> para después o pertenece a otro workstream. Si un agente sugiere
> construir algo de esta lista, no lo hagas.

Explicitly out of scope — not for this plan:

- **Design-system (DS) gates job.** No repo implements a DS-gate required
  check today; tracked as a separate cross-cutting workstream (the Pháros
  registry rollout), not here. This rollout closes without it.
- **Required-status-check name standardization.** Each repo's job names
  differ (`lint-frontend` vs `lint`, etc.); enumerate per-repo for now,
  standardize as a follow-up.
- **Prod go-live for `cobol-migration`** (wiring `production` secrets +
  flipping the flag) — owned separately by @ychejne-jpg via issue #7.

---

## At-a-glance status matrix · Matriz de estado

> **Resumen (ES).** Una fila por repo, una columna por artefacto de la
> política. Lee la celda como el estado en la rama **por defecto** (lo que
> GitHub realmente exige). Corregida el 2026-06-13 tras un re-verify en
> vivo con `gh api` de los 7 repos.

Legend: see the **status-matrix legend** under Conventions above.

> **Corrected 2026-06-13 from a live `gh api` re-verify of all 7 repos** (see the
> RE-VERIFY note below). The previous matrix overstated finance-lch / lab-qc / cobol-migration
> by counting develop-side work as done; the dominant gap is that **the chrome was never
> promoted `develop → main`**, leaving main's branch protection hollow.

| Repo | BP main | BP develop | Repo settings | CODEOWNERS | PR template | Stale wf | Pre-commit | CI/CD shape |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `Interval-Col/.github` | ✅ | n/a (no `develop`) | ✅ (merge-commit-only per policy) | ✅ | ✅ | ✅ | ✅ (4 hooks) | n/a deploy · ✅ gitleaks |
| `Interval-Col/finance-lch` | ⚠️ hollow (req. checks + CODEOWNERS on `develop` only) | ✅ (no review reqs) | ✅ (merge-commit-only per policy) | ⚠️ develop only | ⚠️ develop only | ⚠️ develop only | ✅ 4/4 on `develop` (absent on `main`) | ✅ build-once-promote · ✅ gitleaks (develop) |
| `Interval-Col/lab-qc` | ⚠️ hollow (7 req. checks, 0 producing workflows on main) | ✅ | ✅ (merge-commit-only per policy) | ❌ main (develop only → unenforced) | ❌ main | ❌ main | ✅ 4/4 on `develop` (`main` stale: 0/4) | ✅ build-once-promote · ❌ gitleaks (orphaned required check, wf on develop only) |
| `Interval-Col/commercial-lch` | ✅ (1 review + CODEOWNERS + 3 checks + conv-res) | ✅ (3 checks, PR-optional) | ✅ (merge-commit-only, auto-delete, discussions) | ✅ | ✅ | ✅ | ✅ 5/5 hooks | ✅ **build-once-promote** (main retags :dev→:prod, PRs CI-only) · ✅ gitleaks gate |
| `Interval-Col/cobol-migration` | ✅ (gitleaks + 1 review + CODEOWNERS; chrome on `main`) | ✅ (gitleaks, PR-optional) | ✅ (merge-commit, auto-delete, discussions) | ✅ (on `main`) | ⚠️ org-default | ✅ (on `main`) | ✅ 4 hooks (on `main`) | ✅ **build-once-promote** (prod deploy flag-gated) · ✅ gitleaks |
| `Interval-Col/admission-patient` | ✅ (renamed `master`→`main`) | ✅ | ✅ (merge-commit-only) | ✅ | ✅ | ✅ | ✅ 4/4 hooks | ⚠️ CI-only, **deploy port deferred (H2)** · ✅ gitleaks gate |
| `Interval-Col/operations` | ✅ | n/a (no `develop` — docs-only) | ✅ (merge-commit-only per policy) | ✅ | ✅ | ✅ | ✅ (4 hooks) | n/a deploy · ✅ gitleaks |

Headline (audit 2026-06-04): zero repos had branch protection, zero had the
policy hook set, only one had a CODEOWNERS file. The rollout is wide but each
repo is a small amount of work — the bulk of effort is the CI/CD migration in
the three repos that already deploy.

**Update 2026-06-04**: `finance-lch` is **done** end-to-end — chrome,
branch protection on both `main` and `develop`, build-once-promote
migration, repo settings. It now serves as the reference implementation
the other repos can copy. See its row above for the concrete artifacts
(PR Interval-Col/finance-lch#8, the `gh api` ruleset, the `promote-*`
jobs pattern).

**Update 2026-06-05**: `lab-qc` is **develop-side done** — chrome (CODEOWNERS,
PR template, stale), all 5 pre-commit policy hooks (lockstep with finance-lch),
`ci-cd.yml` migrated to build-once-promote (merged to `develop` via PR
Interval-Col/lab-qc#3; the `promote-*` jobs correctly skip on a `develop` push
and the dev deploy is green), repo settings (merge-commit-only + auto-delete +
Discussions), and branch protection on `develop`. **Deferred by the owner**: the
first `develop → main` promote (which exercises the prod promote path) and branch
protection on `main` — these are bundled to land together in a later prod-side
session. So lab-qc is NOT yet end-to-end "done"; its `BP main` cell is ⏸️.

**Update 2026-06-06**: `operations` is **DONE** end-to-end as a docs-only
rollout. No code → no CI/CD migration, no `develop` branch, no
build-once-promote. The policy applied in a slimmed-down form: chrome +
protection + a minimum pre-commit set where **gitleaks is the load-bearing
hook** (the whole repo is sensitive ops content). Landed in two PRs:
**operations#2** (CODEOWNERS + a substantially refined SECURITY.md that
codifies "show how to find it, don't write it down" as the named pattern and
adds the "what goes where" decision table); **operations#3** (PR template,
stale workflow, slimmed `.pre-commit-config.yaml`, server-side
`.github/workflows/gitleaks.yml`). Repo settings + branch protection on
`main` then applied via `gh api`; required status check is `gitleaks` only.
operations is now the docs-only reference implementation for the rollout —
it shows how the policy adapts to repos with no code.

**Update 2026-06-13: `admission-patient` PREPPED.** The "KNOWN-RED CI / H2
blocker" turned out to be resolved — `@intervalica/alexandria` (the unreachable
private package) was removed in the shadcn migration, so CI is green. With that
cleared: `master`→`main` rename (#19 promote made `main` current, source-only —
no deploy), full chrome + 4/4 hooks, repo settings, and branch protection on
both `main` and `develop`. First full-history gitleaks scan was clean. **Only
the deploy-pipeline port (H2) remains deferred.** This was the last repo thought
to be "parked"; it's now compliant on everything except deploy. See its row +
section.

**RE-VERIFY 2026-06-13 (live `gh api` audit of all 7 repos — supersedes the
optimistic ✅ marks in the 06-04/05/06 notes above).** A full audit found the
tracker materially overstated three repos. Root cause: **policy chrome was done
on `develop` and never promoted to `main`.** Concretely:

- **finance-lch + lab-qc + cobol-migration**: `CODEOWNERS`, `PULL_REQUEST_TEMPLATE.md`,
  `stale.yml`, `gitleaks.yml`, and (for lab-qc/cobol) `.pre-commit-config.yaml`
  exist **only on `develop`**. They are 404 on `main`. Because GitHub reads
  CODEOWNERS and runs required-check workflows **from the default branch**, the
  branch protection on `main` is **hollow**: it requires checks no workflow on
  `main` produces, and enforces code-owner review against a CODEOWNERS file that
  isn't there. lab-qc `main` requires **7 status checks** (incl. `gitleaks`) with
  **zero** producing workflows on `main` — a real PR to `main` would block forever.
- **Pre-commit hook drift** (not the claimed lockstep): finance-lch has **2/4**
  policy hooks (missing `check-case-conflict`, branch-name-lint); lab-qc has
  **0/4** (ruff+eslint only); cobol-migration has 4/4 (on develop). Only operations
  and `.github` are clean.
- **Merge mode — NOT a discrepancy** (corrected on second look): `.github`,
  finance-lch, lab-qc, and operations are all **merge-commit-only**
  (`squash=false, merge=true, rebase=false`). The audit first flagged this as a
  "reversion from squash-only," but **the policy itself changed between sessions** —
  BRANCHING-AND-DEPLOY.md §"Merge mode" now mandates **merge-commit-only** with the
  PR title as the merge-commit subject (squash + rebase disabled; linear history
  intentionally off). So these repos are **compliant**; the audit compared against
  the stale squash-only rule. One thing still worth checking during the promote
  work: any repo whose `main` protection has `required_linear_history=true` is now
  **incompatible** with merge-commit-only and would block merges — verify + turn it
  off where set.
- **commercial-lch was understated**: the tracker said "CI-only, no deploy"; in
  fact `ci.yml` is a full **rebuild-per-env pipeline that already deploys dev +
  prod over SSH**. So it needs the build-once-promote migration too, not just chrome.
- **admission-patient + operations + `.github`** audited as accurate (modulo the
  merge-settings nuance).

The good news: most "missing" artifacts **exist on `develop`** — the dominant fix
is a `develop → main` promote on finance-lch / lab-qc / cobol-migration, not a
rebuild. The per-repo sections below still describe the develop-side work that was
done; treat their "DONE" language as **develop-side only** until the promote lands.

**Correction 2026-06-13 (same day):** the first pass of this RE-VERIFY recorded
the audit's pre-commit hook counts verbatim — finance-lch "2/4", lab-qc "0/4".
Both were **false negatives**: on a direct per-branch read, finance-lch and lab-qc
each have **4/4 policy hooks on `develop`** (the "0/4" is only true of `main`, the
stale snapshot). The matrix hook cells are corrected. Root cause + the rule that
would have caught it are in **["Re-verifying this tracker"](#re-verifying-this-tracker--read-this-before-trusting-or-editing-the-matrix)** below — this episode is the cautionary tale that section exists for.

---

## Org-wide compliance audit (2026-06-16) — beyond the 7-repo scope

> **Resumen (ES).** Barrido automatizado de **los 21 repos** de la org (no solo
> los 7 de este plan). Resultado: **6 cumplen · 3 parciales · 12 NO cumplen.**
> El hallazgo de fondo: este plan solo cubrió 7 repos; los otros 14 nunca se
> rastrearon aquí, y la mayoría no tiene la compuerta de `gitleaks` ni protección
> en `main` — el riesgo #1 (fuga de secretos). Abajo: la matriz completa + el
> backlog priorizado para los repos antes fuera de alcance.

A read-only automated sweep (one checker per repo + an adversarial verify pass)
audited **all 21 active org repos** against the policy CORE: default branch
`main`, merge-commit-only, `main`/`develop` protection requiring a `gitleaks`
check, and the gitleaks workflow + config in-repo. This plan's Phase 1 only ever
scoped **7 repos**; the audit covers the rest.

**Result: 21 repos · ✅ 6 compliant · ⚠️ 3 partial · ❌ 12 non-compliant.**

> **Remediation tracked in [#42](https://github.com/Interval-Col/.github/issues/42)** (@gczuluaga · Start 2026-06-04 · Target 2026-07-10). The matrix below is the **as-found snapshot**; live progress is in the **Remediation log** at the end of this section.

| Repo | Default | Merge-only | main+gitleaks | develop+gitleaks | gitleaks files | chrome | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `port-mapper` | ❌ master | ❌ | ❌ | — | ❌ | ❌ | ❌ |
| `transmisiones` | ❌ master | ❌ | ❌ | — | ❌ | ❌ | ❌ |
| `accounting-interface` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `api-calendar` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `biuman-lis` | ✅ | ✅ | ❌ | ❌ | ❌ | ⚠️ | ❌ |
| `biuman-reports` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `design-studio` | ✅ | ❌ | ❌ | — | ❌ | ❌ | ❌ |
| `employee-management` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `inventory-management` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `legacy-repositories` | ✅ | ✅ | ❌ | — | ❌ | ❌ | ❌ |
| `rfcs` | ✅ | ✅ | ❌ | — | ❌ | ❌ | ❌ |
| `pdf-render-service` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `finance-lch` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⚠️ |
| `lab-qc` | ✅ | ✅ | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| `operations` | ✅ | ✅ | ✅ | — | ⚠️ | ✅ | ⚠️ |
| `.github` | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| `admission-patient` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cobol-migration` | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| `commercial-lch` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `infrastructure` | ✅ | ✅ | ✅ | — | ✅ | ⚠️ | ✅ |
| `nucleus-db` | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |

**Reconciliation with the 2026-06-13 RE-VERIFY.** The `gitleaks files ❌` on
**finance-lch** and **lab-qc** is the *same* finding this plan already records:
the gitleaks workflow/config live on `develop`, 404 on `main` (the default branch
the required check reads) → "hollow main protection." Not a new or false finding —
the `develop → main` promote already on the backlog fixes it. (`operations` is
`⚠️`: workflow present, `.gitleaks.toml` missing.)

**Scope gap — the real story.** The 12 non-compliant repos are almost all
**outside this plan's original 7-repo scope** and were never tracked here:
`accounting-interface, api-calendar, biuman-lis, biuman-reports, design-studio,
employee-management, inventory-management, legacy-repositories, rfcs,
pdf-render-service` + `port-mapper, transmisiones`. **Decision needed:** extend
the rollout to these, or explicitly defer each (with a reason) — but several are
active/sensitive (`rfcs` is public; `biuman-lis` is a live LIS app;
`accounting-interface` handles billing).

### Remediation backlog (by severity)

**🔴 High**
- **Still on `master`** (`port-mapper`, `transmisiones`): rename `master → main`,
  set default, protect. ⚠️ Coordinated-window human step (clones + open PRs) —
  per Working rules, never ad-hoc.
- **`main` unprotected + no `gitleaks` gate** (10): `accounting-interface,
  api-calendar, biuman-lis, biuman-reports, design-studio, employee-management,
  inventory-management, legacy-repositories, rfcs, pdf-render-service` — add
  `gitleaks.yml` + `.gitleaks.toml`, protect `main` requiring the check.
  **This is the #1-fear (secret-leak) gap.**
- **Merge model not merge-commit-only** (squash/rebase on) (6):
  `accounting-interface, api-calendar, design-studio, employee-management,
  inventory-management, pdf-render-service` — turn squash + rebase off
  (quick, reversible `gh repo edit` toggle).

**🟡 Medium**
- **finance-lch / lab-qc**: promote chrome `develop → main` so the required
  `gitleaks` check actually runs on `main` (de-hollow protection) — already the
  Phase-1 backlog item.
- **operations**: add `.gitleaks.toml`.
- **`develop` unprotected** where it exists (`accounting-interface, api-calendar,
  biuman-lis, biuman-reports, employee-management, inventory-management,
  pdf-render-service`): protect, requiring gitleaks.

**⚪ Low (chrome)**
- pre-commit hooks / PR template / stale workflow missing broadly — including a
  few otherwise-compliant repos (`cobol-migration, infrastructure, nucleus-db`
  carry a `⚠️` chrome cell).

> **Method note.** The sweep is reproducible (one read-only `gh` check matrix per
> repo); it could run periodically to keep this matrix honest — the same pattern
> as the memory-hygiene drift detector. Verdicts are high-confidence: every
> non-compliant repo was adversarially re-checked, and the one nuance
> (finance-lch/lab-qc files-on-`develop`) is reconciled above.

### Remediation log

Live deltas against the as-found snapshot above (the matrix is left as-found).
Tracked org-wide in [#42](https://github.com/Interval-Col/.github/issues/42)
(@gczuluaga · Start 2026-06-04 · Target 2026-07-10).

- **2026-06-16 · `rfcs` → ✅ compliant** (was ❌). Docs-only rollout mirroring
  `operations`: gitleaks gate (`.github/workflows/gitleaks.yml` + the canonical
  `.gitleaks.toml`) + the 4 policy pre-commit hooks + `scripts/check-branch-name.sh`
  + `.github/CODEOWNERS` + PR template + stale sweeper (merge `f63aae3`);
  full-history gitleaks pre-scan clean (68 commits, 0 leaks); `gitleaks` check
  green on `main`; `main` branch protection enabled requiring `gitleaks`
  (status-check-only — required-reviewers is a paid feature on this private repo,
  same as `operations`). Net after this: **7 compliant · 3 partial ·
  11 non-compliant.**

---

## Re-verifying this tracker — read this before trusting or editing the matrix

> **Resumen (ES).** Este tracker es una **vista derivada**, no la fuente de
> verdad — los repos en vivo lo son. Se edita a mano entre sesiones y **se
> pone obsoleto**. Las 5 reglas de abajo evitan los errores sutiles que
> mordieron repetidamente el 2026-06-13. Síguelas o los repetirás.

💡 **Heuristic.** This tracker is a **derived view**, not the source of
truth — the live repos are. It is hand-edited across sessions and **goes
stale**. On 2026-06-13 a full re-verify produced *four* wrong intermediate
findings before the truth settled; the traps below are subtle and bit
repeatedly. Follow the rules or repeat them. *(ES: la matriz miente con el
tiempo — re-deriva con estas reglas y pon fecha.)*

1. **A cell reflects the DEFAULT branch — that's what GitHub enforces.** Branch
   protection, CODEOWNERS routing, and required-check *producers* are all read by
   GitHub from `main`. A repo mid-rollout can have the work complete on `develop`
   but **not promoted to `main`** → "done but unenforced." Represent that
   explicitly (`✅ develop / ❌ main`); never collapse it to a bare ✅ or ❌. The
   whole "hollow main protection" story is this: `main` requires checks whose
   workflows live only on `develop`.

2. **Always pass `?ref=<branch>`, and check BOTH `main` and `develop`.**
   `gh api .../contents/PATH` with no `?ref` reads the default branch. Multiple
   false findings came from reading `main` (a weeks-stale snapshot) and reporting
   "missing everywhere."

3. **Never test presence with `[ -n "$(gh api … --jq .path 2>/dev/null)" ]`.** A
   404 piped through `--jq '.path'` prints `"null"` — **non-empty** — so every
   absent file reports "PRESENT." This one bug made an entire per-branch sweep
   report all-green. Instead: list the parent dir (`--jq '.[].name'`) and check
   the **exit code**; keep stderr visible (don't `2>/dev/null` the signal away).

4. **An automated/agent audit is a hypothesis, not fact.** The structured 7-repo
   audit that seeded the 2026-06-13 correction was directionally useful but wrong
   on specifics (branch-ref + grep-scope errors → false "2/4"/"0/4" hook counts
   that briefly landed in this matrix). Verify every consequential claim with a
   direct read before recording it; confirm surprises with a second independent
   method.

5. **Prefer a local working-tree read for committed files.** When the repo is
   cloned and `git rev-parse HEAD == origin/<branch>`, reading the file on disk
   beats a contents-API round-trip (no ref ambiguity, no 404→"null" trap).

When in doubt, **re-derive** with these rules and **timestamp** the result — the
ground moves between sessions.

---

## Phase 1 — Per-repo rollout (one section per repo)

> **Resumen (ES) — Fase 1: Despliegue por repo.**
>
> Esta fase es el grueso del trabajo: llevar cada uno de los 7 repos al
> estado "cumplido" de la política. Cada repo es su propia sub-sección con
> su checklist y su dueño.
>
> En orden, los repos:
>
> 1. **1.1 `.github`** — el meta-repo que hospeda los configs canónicos que
>    los demás copian. ✅ Hecho.
> 2. **1.2 `finance-lch`** — implementación de referencia (lado develop);
>    falta promover el chrome a `main`.
> 3. **1.3 `lab-qc`** — lado develop hecho; el bundle de prod (promote +
>    BP main) ya entró el 06-07.
> 4. **1.4 `commercial-lch`** — totalmente cumplido, primer pipeline
>    build-once-promote probado en prod.
> 5. **1.5 `cobol-migration`** — totalmente cumplido; deploy a prod
>    flag-gated hasta que pasen los gates de readiness.
> 6. **1.6 `admission-patient`** — listo en todo menos el port del deploy
>    (H2), diferido a propósito.
> 7. **1.7 `operations`** — docs-only; cumplido en forma reducida (gitleaks
>    como hook de carga).

### 1.1 `Interval-Col/.github`

**Status (2026-06-06):** ✅ **DONE.** The meta-repo now carries the chrome it prescribes and hosts the canonical configs the other repos copy. Docs-only/meta repo — **no `develop`, no CI/CD** (same shape as `operations`). Chrome landed via the `.github` chrome PR; repo settings + branch protection on `main` applied via `gh api` immediately after.

- [x] **Skip**: `develop` branch — docs/meta repo with no integration-branch model (same pattern as `operations`).
- [x] Enable branch protection on `main` — PR required (the gate), 1 reviewer + CODEOWNERS, resolved threads, up-to-date, **linear-history OFF** (merge-commit model — see BRANCHING-AND-DEPLOY.md §"Merge mode"), no force-push, no deletions. `enforce_admins:false`.
- [x] **Skip**: branch protection on `develop` — no `develop` branch.
- [x] Add `.github/CODEOWNERS` — catch-all `@gczuluaga`; `BRANCHING-AND-DEPLOY.md`, `ENGINEERING_STANDARDS.md`, `agents/`, `templates/`, `instructions/` → `@gczuluaga` + `@SKuger01`.
- [x] Add `.github/PULL_REQUEST_TEMPLATE.md` — generic **org-default** for any repo without its own.
- [x] Add `.github/workflows/stale.yml` (30/60/90, `actions/stale@v9`).
- [x] Add `.github/workflows/gitleaks.yml` — server-side secret-scan (the required check); pinned binary; auto-uses the canonical `.gitleaks.toml`.
- [x] Add `.pre-commit-config.yaml` — 4 docs-only policy hooks (case-collision, gitleaks, conventional-pre-commit, branch-name). ruff/eslint dropped — no code to format.
- [x] Add **canonical `.gitleaks.toml`** — the org's single source of truth for "what counts as a leak"; other repos copy / sync it.
- [x] Add `scripts/check-branch-name.sh` — the reusable branch-name linter (canonical copy).
- [x] Repo settings: **merge-commit-only** (squash + rebase off), **PR title as merge-commit message**, auto-delete-on-merge, Discussions on.
- [x] Canonical hook configs landed: `.gitleaks.toml` + `scripts/check-branch-name.sh`. Conventional-Commits is enforced via the `conventional-pre-commit` hook (no separate `commitlint.config.js` needed).

**Owner:** @gczuluaga (with @SKuger01 as second reviewer for policy paths via CODEOWNERS).

---

### 1.2 `Interval-Col/finance-lch`

> ⚠️ **SUPERSEDED by the 2026-06-13 re-verify** (see RE-VERIFY note above). The
> "DONE" status below reflects **develop-side** work. The governance chrome
> (CODEOWNERS, PR template, stale.yml, the check-producing workflows) is on
> `develop` only and **404 on `main`**, so `main` branch protection is hollow.
> The "follow-up develop → main PR" referenced below did not actually carry the
> `.github/` chrome to `main`. Real remaining work: promote chrome to `main` +
> backfill pre-commit hooks (currently 2/4 on `main`; 4/4 on `develop`).

**Status (2026-06-04, develop-side):** All policy chrome landed on `develop`, ci.yml/ci-cd.yml migrated to build-once-promote. Landed via PR Interval-Col/finance-lch#8. Repo settings + branch-protection rules applied via `gh api`.

**Update 2026-06-06:** server-side **gitleaks gate** added — required status check on `main` + `develop` (PR Interval-Col/finance-lch#9) — and the repo flipped to the **merge-commit model** (squash off, linear-history off, PR-title merge messages). A one-time full-history gitleaks audit surfaced a real leak: `cobolql` API tokens + `finance_user` DB creds in `jobs/config.json` history (file already removed from `develop`). **Rotated by @gczuluaga**; the dead values are allowlisted in finance-lch's own `.gitleaks.toml` with an incident pointer, and mock-IAM / `dev-admin` placeholders are allowlisted via the canonical `.github/.gitleaks.toml`. Full-history scan: clean (462 commits).

- [x] Land policy assets — landed via PR #8 to `develop`, then promoted to `main` through the policy's own PR/merge-commit flow.
- [x] Add `.github/CODEOWNERS` — initial domain map (backend / frontend / contabilidad / infra / plans+docs), catch-all `*` → `@gczuluaga`; `frontend/` → `@SKuger01`; contabilidad cross-cutting paths require both.
- [x] Add `.github/PULL_REQUEST_TEMPLATE.md` — Why / What changed / Test plan / Rollout notes, with the CC-format reminder in the HTML preamble (the merge-commit model makes the PR title load-bearing).
- [x] Add `.github/workflows/stale.yml` — `actions/stale@v9`, 30d warn / 60d notify / 90d archive, daily 13:00 UTC, opt-out via `do-not-stale` label.
- [x] Extend `.pre-commit-config.yaml` with the 5 policy hooks — `check-case-conflict`, `gitleaks` (v8.21.2), `ruff`/`ruff-format` (format-on-stage), `conventional-pre-commit` (v3.6.0, commit-msg stage), local `scripts/check-branch-name.sh` (pre-push stage). 12 hooks total across 3 stages.
- [x] `ci.yml` was already at parity with the policy on this — `Frontend lint (ESLint)`, `Backend lint (Ruff + Pyright)`, `Frontend tests (Vitest)`, `Backend tests (pytest)`, `Verify API contract (regenerate then diff)`, and `Block local IAM from leaking into deploy compose` are all 6 wired into branch protection as the required check set. The audit originally flagged `verify-api-contract` as missing — that was stale; the job has existed since the API-contract slice landed in Phase 3.
- [ ] Add design-system gates job — **deferred** (see Decisions / Out of scope). No repo implements this yet; tracked as a separate workstream.
- [x] Enable branch protection on `main` — applied via `gh api PUT /repos/.../branches/main/protection`. Ruleset: 6 required checks (above), 1 reviewer, dismiss stale on new commits, CODEOWNERS review required, linear-history off (merge-commit model), resolved conversations required, no force-push, no deletions. `enforce_admins: false` (admin-included is the planned escalation per policy).
- [x] Enable branch protection on `develop` — applied via `gh api`. Same 6 required checks; PR optional (direct push allowed); no force-push, no deletions; linear history not required.
- [x] Repo settings — `gh api PATCH /repos/...`: `delete_branch_on_merge=true`, `allow_squash_merge=false`, `allow_merge_commit=true`, `allow_rebase_merge=false`, `has_discussions=true` (merge-commit-only).
- [x] Migrate `ci-cd.yml` to build-once-promote — push to `develop` builds `${REPO}:dev` + `${REPO}:<sha>` and deploys dev; push to `main` runs new `promote-frontend`/`promote-backend` jobs that **pull `${REPO}:dev`, retag as `${REPO}:prod` + `${REPO}:<main-sha>`, push**. Same `sha256` digest from dev → prod. `workflow_dispatch` action set expanded with `promote-and-deploy` and `promote-only`. A safety check in the `config` job refuses to BUILD a prod image from a push event.

**Owner:** @gczuluaga (executed 2026-06-04).

Actual effort: ~3h end-to-end including the chrome, hook configs, CI/CD migration, post-merge `gh api` calls, and exercising the policy's own PR-to-`main` flow as the bootstrap moment. The CI/CD migration was the bulk; chrome + settings were ~30 min total.

---

### 1.3 `Interval-Col/lab-qc`

> ⚠️ **SUPERSEDED by the 2026-06-13 re-verify** (see RE-VERIFY note above). This
> section's "done" claims are **develop-side only and partly inaccurate**. Live
> `gh api` audit found: CODEOWNERS, PR template, stale.yml, and `gitleaks.yml`
> are **404 on `main`** (develop only); `main` branch protection requires **7
> status checks with zero producing workflows on `main`** (incl. an orphaned
> `gitleaks` check), so PRs to `main` would block; the `.pre-commit-config.yaml`
> on `main` carries **0/4 policy hooks** (ruff+eslint only) vs **4/4 on `develop`**.
> The 2026-06-07 leak rotation below is real and stands. Real remaining work:
> promote chrome to `main`, confirm the gitleaks workflow reaches `main` so its
> required check has a producer.

**Status (2026-06-05):** ⏸️ **DEVELOP-SIDE DONE; prod bundle deferred.** Chrome,
all 5 pre-commit hooks, build-once-promote migration, repo settings, and branch
protection on `develop` all landed via PR Interval-Col/lab-qc#3 (merge-commit to
`develop`; dev deploy green). The owner deliberately deferred the first
`develop → main` promote and branch protection on `main` to a later prod-side
session — see the 2026-06-05 headline note above.

**Update 2026-06-07:** ✅ `main` branch protection **now enabled** (the previously-deferred prod-side gate) and the server-side **gitleaks gate** added — required on `main` + `develop` (PR Interval-Col/lab-qc#5) — with the repo flipped to the **merge-commit model** (squash off). A one-time full-history gitleaks audit surfaced a real leak: analyte-ETL tokens + a `postgres` dev DB password in `jobs/config.json` + `backend/api/logic.py` history (both files already removed from `develop`). **Rotated by @gczuluaga**; dead values allowlisted in lab-qc's own `.gitleaks.toml` with an incident pointer. Full-history scan: clean (319 commits). *(The `develop → main` build-once-promote deploy itself is separate and still to be exercised — only the `main` branch-protection gate was added here.)*

- [x] Add `.github/CODEOWNERS` — adapted to lab-qc's real layout (`backend/`, `backend/alembic/`, `frontend/app/{components,pages,stores}`, `frontend/e2e/`, `.github/`, `docs/`, `plans/`); catch-all → @gczuluaga, frontend → @SKuger01.
- [x] Add `.github/PULL_REQUEST_TEMPLATE.md` — Why / What / Test plan / Rollout, CC-format reminder.
- [x] Add `.github/workflows/stale.yml` (30/60/90, `actions/stale@v9`).
- [x] Extend `.pre-commit-config.yaml` with the missing policy hooks — added `check-case-conflict`, `gitleaks`, `conventional-pre-commit` (commit-msg), `branch-name-lint` (pre-push) + `scripts/check-branch-name.sh`. ruff format-on-stage was already present (the audit's "0/5" was stale — it was 1/5), so the file now carries the full 5-hook set and is byte-for-byte in lockstep with finance-lch.
- [x] Already done: pre-commit baseline (lint/format hooks installed)
- [x] Already done: `ci.yml` lint+tests pipeline that can feed required-status-checks
- [x] Already done: `environment: production` already wired in `ci-cd.yml` — promote gate in place; now gates a retag instead of a rebuild
- [x] Enable branch protection on `main` per policy §"main — today" — **applied 2026-06-07** via `gh api PUT`: 1 reviewer + CODEOWNERS, 7 required checks (the 6 develop checks + `gitleaks`), `strict=true`, linear-history off, no force-push/deletions, conversation-resolution required, `enforce_admins=false`.
- [x] Enable branch protection on `develop` — applied via `gh api PUT`: 6 required checks (`Frontend lint (ESLint)`, `Backend lint (Ruff + Pyright)`, `Frontend tests (Vitest)`, `Backend tests (pytest)`, `Backend migrations (Alembic)`, `Verify API contract (regenerate then diff)`); `strict=false`; PR optional; no force-push; no deletions. E2E excluded (deferred).
- [x] Repo settings — `gh api PATCH`: `delete_branch_on_merge=true`, `has_discussions=true`. **(2026-06-07: flipped to the merge-commit model — `allow_merge_commit=true`, `allow_squash_merge=false`, `allow_rebase_merge=false`, `merge_commit_title=PR_TITLE`.)**
- [x] Migrate `ci-cd.yml` to build-once-promote — push to `develop` builds `:<sha>` + `:dev` and deploys dev; push to `main` runs new `promote-frontend`/`promote-backend` jobs that pull `:dev`, retag `:prod` + `:<main-sha>`, push (no rebuild). `config` job refuses to BUILD a prod image from a push event. **Not yet exercised `develop → main`** (deferred with the prod bundle).

**Owner:** @gczuluaga (develop-side executed 2026-06-05; prod bundle pending).

Actual effort (develop-side): ~2h — chrome + hooks + ci-cd migration + local gates (pytest 356✓, vitest 63✓, lint✓) + PR #3 + post-merge `gh api` settings/protection. The prod bundle (develop→main promote + main protection) remains.

---

### 1.4 `Interval-Col/commercial-lch`

**Status (2026-06-13):** ✅ **FULLY DONE — chrome + gitleaks + protection + settings + build-once-promote.** Unlike the other deploy-capable repos, everything was taken **all the way to `main` the same day** (default branch was already `main`), so branch protection is **real, not hollow**, and commercial-lch is the **first repo with a verified build-once-promote pipeline live on prod**.

- [x] **Chrome → `develop`** (PR Interval-Col/commercial-lch#17, merge-commit): `.github/CODEOWNERS` (`backend/`→@gczuluaga, `frontend/`→@SKuger01, `.github/`+plans/docs→@gczuluaga), `.github/PULL_REQUEST_TEMPLATE.md` (backend/+frontend/ layout + deploy note), `.github/workflows/stale.yml`, `.github/workflows/gitleaks.yml` + genericized `.gitleaks.toml`, `scripts/check-branch-name.sh`.
- [x] **`develop → main` promote** (PR Interval-Col/commercial-lch#18, merge-commit) — chrome now on `main`. **This triggered a PROD deploy** (rebuild-per-env pipeline) which **succeeded** — effectively a redeploy + chrome, no app-code change. Confirmed safe-to-deploy by owner.
- [x] **Pre-commit 5/5 policy hooks** — `check-case-conflict` (case-collision), gitleaks v8.21.2, ruff/ruff-format (`backend/` format-on-stage), conventional-pre-commit v3.6.0 (commit-msg, --strict), branch-name-lint (pre-push). Existing ruff + frontend eslint (`pnpm lint-check`) baseline preserved.
- [x] **First full-history gitleaks scan: CLEAN** (no leak — no rotation needed, unlike lab-qc).
- [x] **Repo settings** via `gh api`: merge-commit-only (`squash=false, rebase=false, merge_commit=true`), `delete_branch_on_merge=true`, `has_discussions=true`.
- [x] **Branch protection on `main`**: checks `[Backend CI, Frontend CI, gitleaks]` (strict), 1 review, code-owner review, conversation-resolution, no force-push, no deletions, `enforce_admins=false`, linear-history off (merge-commit model).
- [x] **Branch protection on `develop`**: same 3 checks (strict), PR-optional (direct push allowed), no force-push, no deletions.
- [x] **Lingering `master`**: none — default was already `main`, no `master` ref existed (no-op).
- [x] **Build-once-promote migration — DONE 2026-06-13** (PR Interval-Col/commercial-lch#19 → develop, cutover PR #20 → main). New `promote` job: push-to-`main` resolves to `promote-and-deploy`, pulls the `:dev` digest the last develop push built, retags `:prod` + `:<main-sha>` (no rebuild), deploys prod. PRs are now **CI-only** (`pull_request` → `ci-only`; the old config deployed dev on every PR). Added `promote-and-deploy`/`promote-only` to `workflow_dispatch` + a guard refusing a prod BUILD from an automatic push. **Verified end-to-end**: PR ran CI-only (no deploy); develop push built+deployed dev; a `promote-only` dry-run + the real main cutover both retagged identical digests (backend `a1f15e1a…`, frontend `8f66a91d…`) across `:dev`/`:prod`/`:<sha>`; prod containers came up Up on `:prod`. `commercial-migrate` stays in its `with-db` stand-by profile (DB not wired yet) — preserved, no migration runs on deploy until the DB is provisioned. (Note: a `db/data-migration` branch carries related DB work — do not delete.)
- [ ] DS gates job (only `verify-api-contract` today) — tracked as the cross-cutting DS workstream, not this rollout.

**Owner:** @gczuluaga (full rollout executed 2026-06-13).

Net: commercial-lch is **fully policy-compliant** — branching + protection + chrome + hooks + settings + a verified build-once-promote pipeline live on prod. Nothing remains for this repo in this rollout.

---

### 1.5 `Interval-Col/cobol-migration`

**Status (2026-06-13):** ✅ **FULLY DONE — chrome + gitleaks + protection + settings + build-once-promote (prod deploy flag-gated).** Chrome bootstrapped on `develop` (PR #1), then everything promoted to `main` (PR #6) so branch protection is **real, not hollow**. The `ci-cd.yml` is now build-once-promote (PR #4) with the prod deploy **gated behind `COBOL_PROD_DEPLOY_ENABLED`** (PR #5) — a push to `main` promotes the `etl-cobol:dev` image to `:prod` but **skips the deploy** (golden rule: no income to prod until the RFC 0002 CSRF decision). Prod go-live (Phase 1) is owned by @ychejne-jpg via issue #7 + `operations/plans/cobol-migration-promote-to-prod.md`.

- [x] Bootstrap the full `.github/` chrome on `develop` (PR #1).
- [x] `.pre-commit-config.yaml` with the policy hooks + lint/format baseline (PR #1).
- [x] `.github/CODEOWNERS` (PR #1; now on `main`).
- [x] PR template — inherits the org-default in `Interval-Col/.github` (no per-repo file needed).
- [x] `.github/workflows/stale.yml` (PR #1; now on `main`).
- [x] Repo settings: merge-commit-only (squash + rebase off), auto-delete on, Discussions on.
- [x] Branch protection on `develop` (gitleaks, PR-optional) and `main` (gitleaks + 1 review + CODEOWNERS) — real now that the gitleaks workflow is on `main`.
- [x] **Migrate `ci-cd.yml` to build-once-promote** (PR #4): push to `main` → `promote-and-deploy` retags `:dev`→`:prod` (no rebuild). Verified via a `promote-only` dry-run (identical digest `ccfe3eae…160cc`) + the real main-push run (Build skipped, Promote success, Deploy gated-skipped).
- [x] **Gate the prod deploy** behind `COBOL_PROD_DEPLOY_ENABLED` (PR #5) — environment required-reviewers aren't available on this repo tier, so an in-workflow flag is the gate.
- [x] **Promote `develop → main`** (PR #6) — chrome + pipeline + ~30 commits of ETL work on `main`; prod deploy gated-skipped, prod untouched.
- [ ] **Prod go-live — DEFERRED (Phase 1, gated).** Wire the `production` env secrets + flip `COBOL_PROD_DEPLOY_ENABLED` + first prod deploy. Gated on RFC 0002 CSRF (@SKuger01) + prod nucleus-db host (@ychejne) + CobolQL service account. Owned by @ychejne-jpg via issue #7 + `operations/plans/cobol-migration-promote-to-prod.md`.
- [ ] Audit stale feature branches (`docs/income-prod-plan-refresh` etc.) — auto-delete is on for future merges; existing ones are pre-existing cruft.

**Owner:** @gczuluaga (rollout executed 2026-06-13); prod go-live @ychejne-jpg (issue #7).

Net: cobol-migration is **fully policy-compliant** — chrome + protection + settings + a verified build-once-promote pipeline on `main`, with the prod deploy deliberately flag-gated until the prod readiness gates clear.

---

### 1.6 `Interval-Col/admission-patient`

**Status (2026-06-13):** ✅ **PREPPED** (deploy port deferred). The "KNOWN-RED CI / Phase H2 blocker" is **resolved**: `@intervalica/alexandria` (the unreachable private package) was removed in the shadcn-vue migration, so CI is green again — no OIDC/private-registry work needed. With CI green, the full rollout landed. **The only deferred piece is the deploy pipeline** (Bitbucket-era ECR/SSH → build-once-promote), which is genuine H2 work and doesn't block the rest.

- [x] **Rename `master` → `main`** — done via the GitHub branch-rename API (default branch moved, `master` ref deleted; no open PR targeted `master` so nothing to retarget). `ci.yml` push trigger flipped `[master, develop]` → `[main, develop]`.
- [x] **`develop → main` promote** — `main` was 301 commits stale; promoted via PR Interval-Col/admission-patient#19 (merge-commit). **Source-only — no deploy fired** (no pipeline). `main` is now current and carries the chrome, so its branch protection is real (not hollow).
- [x] **Chrome** (PR Interval-Col/admission-patient#18 → develop, then promoted): `.github/PULL_REQUEST_TEMPLATE.md` (adapted: Nuxt-at-root + Python `backend/`), `.github/workflows/stale.yml`, `.github/workflows/gitleaks.yml` + genericized `.gitleaks.toml`, `scripts/check-branch-name.sh`.
- [x] **Pre-commit 4/4 policy hooks** — added gitleaks, ruff/ruff-format (`backend/` format-on-stage), conventional-pre-commit (commit-msg), branch-name-lint (pre-push). Replaced the custom `check-case-collisions` hook with the standard `check-case-conflict` for lockstep (script left on disk, unwired). Root eslint kept.
- [x] **First full-history gitleaks scan: CLEAN** (301 commits, no leak — unlike lab-qc, no rotation needed).
- [x] **Repo settings** via `gh api`: merge-commit-only (`squash=false, rebase=false`), `delete_branch_on_merge=true`, `has_discussions=true`.
- [x] **Branch protection on `main`** per §"main — today": checks `[backend, gitleaks, lint-and-build]`, 1 review, code-owner review, dismiss-stale, conversation-resolution, no force-push, no deletions, `enforce_admins=false`, linear-history off (merge-commit model).
- [x] **Branch protection on `develop`**: same 3 checks, PR-optional (direct push allowed), no force-push, no deletions.
- [ ] **Deploy pipeline — DEFERRED (H2).** No deploy today; merging to `main` is source-only. Porting the Bitbucket-era ECR/SSH deploy to build-once-promote is separate, ~½ day, owner's call on timing.

**Owner:** @gczuluaga (prep executed 2026-06-13).

Net: admission-patient is policy-compliant on branching + protection + chrome + hooks. Only the deploy-pipeline port remains, deliberately deferred.

---

### 1.7 `Interval-Col/operations`

**Status (2026-06-06):** ✅ **DONE.** Private operational docs repo. **No code → no CI/CD migration**, no build-once-promote, no deploy pipeline. The policy applied in a slimmed-down form: chrome + protection + a minimum pre-commit set where **gitleaks is the load-bearing hook** (the whole repo is sensitive ops content; a credential leak here is the worst case the convention is designed to prevent). Wave 1 chrome landed via PR Interval-Col/operations#3; repo settings + branch protection on `main` applied via `gh api` immediately after.

- [x] **Done via PR Interval-Col/operations#2 (merged 2026-06-06):**
  - `.github/CODEOWNERS` — catch-all → `@gczuluaga`; `SECURITY.md` + `policies/` → `@gczuluaga` + `@SKuger01` (org-level policy rules get a second pair of eyes); `access/`, `runbooks/`, `incidents/` → `@gczuluaga` (sensitive operational content).
  - `SECURITY.md` substantially refined: codifies "show how to find it, don't write it down" as the named pattern, adds the "what goes where" decision table (11 rows + the IP+port+user+role tuple rule), two-part incident response (secret leak vs non-secret-but-policy-violating leak), and the verify-the-filter command for `git-crypt`.
- [x] Add `.github/PULL_REQUEST_TEMPLATE.md` — Why / What changed / Test plan (docs-only) / Rollout (revert-harmless) sections, with the load-bearing review prompt to keep `SECURITY.md`'s asset table authoritative on any PR that touches it. **(operations#3)**
- [x] Add `.github/workflows/stale.yml` (30/60/90 via `actions/stale@v9`, `do-not-stale` opt-out). **(operations#3)**
- [x] Add `.github/workflows/gitleaks.yml` — **added beyond the original checklist**: the branch-protection rule below requires a `gitleaks` *status check*, but a pre-commit hook produces no GitHub check. This workflow runs the pinned gitleaks v8.21.2 binary (avoids the `GITLEAKS_LICENSE` requirement of `gitleaks-action@v2` on org repos), job named `gitleaks` so the check context matches. It is the server-side enforcement a local `--no-verify` can't bypass. **(operations#3)**
- [x] Add `.pre-commit-config.yaml` — minimum set:
  - `check-case-conflict` — universal hygiene.
  - **`gitleaks`** (v8.21.2, lockstep with the workflow) — load-bearing for this repo.
  - `conventional-pre-commit` (commit-msg stage) — same as the other repos.
  - Local `scripts/check-branch-name.sh` (pre-push stage) — byte-for-byte from finance-lch/lab-qc.
  - **Skipped `ruff`/`ruff-format`/`eslint` (format-on-stage)** — nothing to format. The hook set adapts to the repo shape. **(operations#3)**
- [x] Repo settings via `gh api PATCH /repos/Interval-Col/operations`:
  - `delete_branch_on_merge=true`, `has_discussions=true`. **(2026-06-13: flipped to the merge-commit model per the policy change — `allow_merge_commit=true, allow_squash_merge=false, allow_rebase_merge=false`, PR-title merge messages.)**
- [x] Enable branch protection on `main` per §"main — today":
  - PR required, 1 reviewer (CODEOWNERS auto-routes the right person per path), resolved threads, dismiss-stale-on-new-commits, linear-history off (merge-commit model), no force-push, no deletions. `enforce_admins: false` (admin-included is the planned escalation, same as finance-lch — keeps the solo owner from being deadlocked on self-review).
  - **Required status checks**: only `gitleaks` (the meaningful gate for a docs-only repo). The `Frontend lint` / `Backend lint` / `*tests` / `verify-api-contract` set from finance-lch doesn't apply here — there's no code to lint, no tests to run, no API contract.
- [x] **Skip**: branch protection on `develop` — operations has no `develop` branch and doesn't need one. Docs-only repos with no integration-branch model (same pattern as `Interval-Col/.github`).
- [x] **Skip**: `ci-cd.yml` migration — no deploy pipeline. No "rebuild per env" problem because there's no build.

**Owner:** @gczuluaga (with @SKuger01 as second reviewer for policy paths via CODEOWNERS).

Estimated effort: ~45 min end-to-end for the remaining items. Mostly file creation + a single `gh api PATCH` for repo settings + branch protection on `main` only.

✅ **Done-when (per repo — applies to every section in Phase 1):**
- Branch protection enforced on `main` **and** `develop` per the policy (and **real, not hollow** — the producing workflows + CODEOWNERS live on the default branch).
- CODEOWNERS in place on the default branch.
- PR template in place (per-repo or org-default).
- Stale workflow live.
- All required pre-commit hooks installed (5 for code repos, 4 for docs/meta) and running in CI.
- `ci-cd.yml` migrated to build-once-promote (or authored that way for green-field repos), or explicitly n/a for docs-only repos.
- Repo settings: auto-delete + **merge-commit-only** (squash + rebase off, PR title as merge-commit subject) verified.

*(ES: un repo está "desplegado" cuando todas las casillas de arriba están en
verde sobre la rama por defecto; si el chrome solo vive en `develop`, la
protección de `main` es hueca y el repo NO está hecho.)*

🚦 **Checkpoint 1 — per repo, before flipping its matrix row to all-✅.** Show
@gczuluaga: the `gh api` ruleset on `main` + `develop`, a real PR that ran the
required checks green, and a per-branch read confirming the chrome exists on the
**default branch** (not just `develop`). Questions:
1. For this repo, is `main`'s branch protection **real or hollow** — i.e. do the
   required-check workflows and CODEOWNERS actually live on `main`? Walk the
   per-branch read live. *(ES: ¿la protección de `main` es real o hueca? Muestra
   la lectura por rama en vivo.)*
2. If this is a deploy repo, demonstrate that a `develop → main` promote retags
   the **same image digest** `:dev → :prod` (no rebuild). *(ES: demuestra que el
   promote re-etiqueta el mismo digest, sin reconstruir.)*

---

## Phase 2 — Cross-cutting work

> **Resumen (ES) — Fase 2: Trabajo transversal.**
>
> Tres piezas que cruzan todos los repos y se rastrean una sola vez (no por
> repo): la migración CI/CD a build-once-promote, el rollout de los hooks de
> pre-commit, y el procedimiento de protección de ramas que un dueño con
> permiso de admin corre una vez por repo.
>
> En orden, las tareas:
>
> 1. **2.1** — migrar cada `ci-cd.yml` a build-once-promote (construir una vez
>    en develop, re-etiquetar `:dev → :prod` en main).
> 2. **2.2** — instalar los hooks de pre-commit obligatorios y un job de CI que
>    los corra (`pre-commit run --all-files`).
> 3. **2.3** — el procedimiento de protección de ramas, corrido verbatim por
>    repo por un admin.

### 2.1 Build-once-promote CI/CD migration

Today (per audit) finance-lch, lab-qc, and cobol-migration each rebuild on
every environment. Policy mandates one build artifact promoted across envs.
The template diff for each repo's `ci-cd.yml`:

**Before (rebuild-per-env, simplified):**

```yaml
on:
  push:
    branches: [develop]   # builds with TAG=dev
  workflow_dispatch:      # builds with TAG=prod (same Dockerfile, same SHA)
jobs:
  build-and-deploy:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t $ECR:${{ env.TAG }} .
      - run: docker push $ECR:${{ env.TAG }}
      - run: ./deploy.sh ${{ env.TAG }}
```

**After (build-once-promote):**

```yaml
on:
  push:
    branches: [develop]
jobs:
  build:
    runs-on: self-hosted
    outputs:
      image_sha: ${{ steps.tag.outputs.sha }}
    steps:
      - uses: actions/checkout@v4
      - id: tag
        run: echo "sha=${GITHUB_SHA::12}" >> $GITHUB_OUTPUT
      - run: docker build -t $ECR:${{ steps.tag.outputs.sha }} -t $ECR:dev .
      - run: docker push $ECR --all-tags
      - run: ./deploy.sh dev

# Separate workflow: promote-to-prod.yml
on:
  workflow_dispatch:
    inputs:
      sha:
        required: true
jobs:
  promote:
    environment: production   # gates on approval
    runs-on: self-hosted
    steps:
      - run: docker pull $ECR:${{ inputs.sha }}
      - run: docker tag $ECR:${{ inputs.sha }} $ECR:prod
      - run: docker push $ECR:prod
      - run: ./deploy.sh prod
```

Per-repo migration checkbox:

- [x] `finance-lch` — **done 2026-06-04** (PR #8). Split build/deploy; new `promote-*` jobs pull `:dev`, retag as `:prod` + `:<main-sha>`, push. Push-to-`main` auto-triggers the promote path. `config` job refuses to BUILD a prod image from a push event.
- [x] `lab-qc` — **migrated 2026-06-05** (PR #3). Split build/promote; new `promote-*` jobs pull `:dev`, retag `:prod` + `:<sha>`, push. Proven on `develop` (promote jobs skip correctly; dev deploy green). **Not yet exercised `develop → main`** — deferred with the prod bundle.
- [x] `cobol-migration` — **DONE 2026-06-13** (PR #4 + promote #6). Single `etl-cobol` image → one `promote` job retags `:dev`→`:prod` on a main push (no rebuild). Prod deploy **flag-gated** (`COBOL_PROD_DEPLOY_ENABLED`, default off) until prod readiness clears. Verified via `promote-only` dry-run + real main-push (deploy gated-skipped).
- [x] `commercial-lch` — **DONE 2026-06-13** (PR #19 + cutover #20). Was NOT green-field (live audit: it already rebuilt+deployed dev+prod per env). New `promote` job retags `:dev`→`:prod` on a main push (no rebuild); PRs flipped to CI-only. Verified end-to-end incl. a `promote-only` dry-run with identical digests + a real prod cutover (prod Up on `:prod`). **First repo with a proven build-once-promote pipeline.**
- [ ] `admission-patient` — H2 blocker (private-pkg + OIDC) **resolved** (alexandria removed in shadcn migration); deploy port still deferred per plan, owned by @ychejne-jpg via issue #21 + `plans/deploy-pipeline-go-live-plan.md`

### 2.2 Hook installation rollout

The 5 required policy hooks and reference configs:

| Hook | Reference / source |
|---|---|
| `case-collision` | `pre-commit-hooks-org/check-case-conflict` (admission-patient has a local-script equivalent named `check-case-collisions` — keep or replace at owner discretion) |
| `gitleaks` | `gitleaks/gitleaks` pre-commit mirror |
| `format-on-stage` | wrap project formatter (ruff-format / prettier / eslint --fix) in a `local` repo block that runs on staged files only |
| `commit-msg-lint` | `commitlint` + `@commitlint/config-conventional`; runs in `commit-msg` stage. Allowed types: `feat|fix|refactor|test|chore|docs|hotfix|ci` (the canonical set) |
| `branch-name-lint` | `branch-name-lint` npm pkg in a `local` repo `pre-push` hook; config restricts to `<type>/<short-kebab-slug>` where `<type>` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci` |

Canonical `.pre-commit-config.yaml` + `commitlint.config.js` +
`branch-name-lint.config.js` will live in `Interval-Col/.github` (see that
repo's checklist above). Each app repo copies + tunes the patterns.

Per-repo install checkbox:

- [ ] `.github` — author the canonical configs
- [x] `finance-lch` — **done 2026-06-04** (PR #8). All 5 policy hooks installed (`check-case-conflict`, `gitleaks` v8.21.2, `ruff`/`ruff-format`, `conventional-pre-commit` v3.6.0 at commit-msg, local `scripts/check-branch-name.sh` at pre-push). `default_install_hook_types: [pre-commit, commit-msg, pre-push]` so a single `pre-commit install` activates all stages.
- [x] `lab-qc` — **done 2026-06-05** (PR #3). All 5 policy hooks (`check-case-conflict`, `gitleaks`, `ruff`/`ruff-format`, `conventional-pre-commit` at commit-msg, local `scripts/check-branch-name.sh` at pre-push) + `default_install_hook_types`. Byte-identical to finance-lch.
- [x] `commercial-lch` — **done 2026-06-13** (PR #17). All 5 policy hooks (`check-case-conflict`, `gitleaks` v8.21.2, `ruff`/`ruff-format` on `backend/`, `conventional-pre-commit` v3.6.0 at commit-msg, local `scripts/check-branch-name.sh` at pre-push) + `default_install_hook_types`. Existing ruff + frontend `pnpm lint-check` eslint preserved.
- [x] `cobol-migration` — **done** (PR #1; now on `main` via promote #6). Policy hooks + lint/format baseline created from scratch.
- [ ] `admission-patient` — copy + commit (only 4 of 5 needed — `check-case-collisions` already present)

Also add a CI job in each repo that runs `pre-commit run --all-files` so the
hooks are enforced even when contributors haven't run `pre-commit install`
locally. This becomes a required status check.

### 2.3 Branch protection enforcement procedure

For each repo, an owner with admin permission runs the following once:

1. GitHub → repo → **Settings** → **Branches** → **Add branch protection rule** → **Branch name pattern: `main`**
2. Check the boxes that match policy §"main — today":
   - [x] Require a pull request before merging
     - Required approvals: **1**
     - Dismiss stale approvals on new commits: **on**
     - Require review from Code Owners: **on**
   - [x] Require status checks to pass before merging
     - Require branches to be up to date: **on**
     - Required checks: `lint`, `unit tests`, `verify-api-contract`, design-system gates (per repo)
   - [x] Require conversation resolution before merging: **on**
   - [ ] Require linear history: **off** (merge-commit model — linear history intentionally off; see BRANCHING-AND-DEPLOY.md §"Merge mode")
   - [x] Do not allow bypassing the above settings: **on**
   - [ ] Allow force pushes: **off**
   - [ ] Allow deletions: **off**
3. **Add branch protection rule** → **Branch name pattern: `develop`** with policy §"develop — today":
   - [x] Require status checks to pass before merging (applies on direct push too via "Restrict pushes" rule) — required checks: lint + tests
   - [ ] Allow force pushes: **off**
   - PR-required: **off** (policy does not require it for develop)
4. **Settings** → **General** → **Pull Requests**:
   - Allow squash merging: **off**
   - Allow merge commits: **on** (default merge-commit message: **Pull request title**)
   - Allow rebase merging: **off**
   - Automatically delete head branches: **on**

Run this checklist verbatim per repo. The audit-derived checklists above flag
which gates each repo is missing — the procedure here is the "how".

✅ **Done-when (Phase 2):**
- Every deploy repo's `ci-cd.yml` builds once on `develop` and **retags** the
  same digest `:dev → :prod` on a `main` push (verified by an identical-digest
  `promote-only` dry-run), with a guard refusing a prod BUILD from a push event.
- Every code repo carries the 5 policy hooks (4 for docs/meta) + a CI job running
  `pre-commit run --all-files` as a required status check.
- The branch-protection procedure has been run verbatim on each repo and the
  General → Pull Requests settings read **merge-commit-only** (squash + rebase off,
  PR title as the merge-commit subject).

*(ES: hecho cuando cada repo de deploy re-etiqueta el mismo digest sin
reconstruir, todos tienen los hooks + el job de CI que los corre, y el
procedimiento de protección quedó corrido con merge-commit-only.)*

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions logged below
> for traceability. *(ES: decisiones humanas abiertas arriba, resueltas abajo.)*

**Open:**

- 🛑 **`Interval-Col/.github` develop branch** — policy assumes
  `main ← develop ← <type>/<slug>` everywhere, but a meta/policy repo arguably
  doesn't need `develop` (no deploy pipeline, no integration branch). Pending:
  exempt it, or create `develop` for consistency? *Recommendation: create it —
  cost is zero, policy stays uniform.* Decides: @gczuluaga.
- 🛑 **Admin permission scope** — the audit ran with read-level token access for
  protection endpoints (HTTP 404 on unprotected branches looks the same as "we
  can't see it"). Pending: before any owner runs the enforcement procedure,
  confirm they have admin on each repo — Gloria + @SKuger01 are the likely set
  but not verified. Decides: @gczuluaga.
- 🛑 **Required status check names** — policy lists "lint + unit tests +
  verify-api-contract + design-system gates" but each repo's check names differ
  (`lint-frontend` vs `lint`, `test-backend` vs `unit tests`, etc.). Pending:
  standardize the job names across repos as part of this rollout, or accept
  per-repo names and enumerate them per protection rule? *Recommendation:
  enumerate per-repo for Wave 1–2 (don't block on rename), standardize as a
  follow-up.* Decides: @gczuluaga.
- 🛑 **DS gates job** — finance-lch and lab-qc have no design-system gate today;
  commercial-lch has only contract diff. Required check "design-system gates" is
  policy but no repo implements it. Pending: out of scope here, or in-scope?
  *Recommendation: out of scope — track as the separate Pháros-registry
  cross-cutting workstream so this plan can close.* Decides: @gczuluaga / @SKuger01.
- 🛑 **cobol-migration extra branches** — `feat/etl-shared-harness` and
  `feat/etl-tui-enhancements` are in-flight; stale-bot will start counting against
  them once it ships. Pending: confirm with the ETL lead whether they're active
  before Wave 1 to avoid surprise archival warnings. Decides: ETL lead /
  @ychejne-jpg.

**Resolved during planning:**

- **`admission-patient` default branch** — renamed `master` → `main` (no open PR
  targeted `master`; `ci.yml` triggers updated; `develop → main` promote made it
  current). *(2026-06-13.)*
- **Merge mode** — adopted **merge-commit-only** org-wide (squash + rebase
  disabled, PR title as the merge-commit subject, linear history intentionally
  off). The earlier squash-only rule is superseded; repos already on
  merge-commit-only are compliant, not a reversion. *(2026-06-13.)*
- **Conventional-commit + branch type set** — the canonical set is
  `feat|fix|refactor|test|chore|docs|hotfix|ci` (`hotfix` is valid as both a
  branch type and a commit type; `ci` was added org-wide for pipeline-only
  changes). *(2026-06-15.)*
- **Merge settings enforced live** — on 2026-06-15, `scripts/enforce-merge-policy.sh`
  was run across all 13 GitHub repos, setting **merge-commit-only + auto-delete-on-merge**
  (squash + rebase off). Spot-verified on `.github`, `finance-lch`, `biuman-reports`.
  The script is idempotent and reversible; re-run to re-assert. *(2026-06-15.)*

## Risks · Riesgos

> **Resumen (ES).** El riesgo dominante es la "protección hueca" — chrome en
> `develop` que nunca se promovió a `main`, así que GitHub exige checks sin
> productor. Las mitigaciones son lecturas por rama y promotes explícitos.

- **Hollow `main` protection** → branch protection that requires checks no
  workflow on `main` produces, blocking real PRs forever (lab-qc `main` requires
  7 checks with 0 producers). **Mitigation:** before flipping a matrix row to ✅,
  run the per-branch read in 🚦 Checkpoint 1 and land the `develop → main` promote
  that carries the chrome to the default branch.
- **Stale tracker** → the matrix is a hand-edited derived view and drifts between
  sessions; four false findings landed on 2026-06-13. **Mitigation:** follow the
  five rules in "Re-verifying this tracker" — always pass `?ref=<branch>`, never
  test presence via `--jq .path`, treat agent audits as hypotheses, prefer a local
  working-tree read, and timestamp the re-derive.
- **Linear-history left on** → a repo whose `main` protection still has
  `required_linear_history=true` is now **incompatible** with merge-commit-only
  and would block merges. **Mitigation:** during the promote work, verify and turn
  it off wherever set.
- **Prod deploy fires on a chrome-only promote** → a `develop → main` promote on a
  deploy repo can trigger a real prod deploy (commercial-lch #18 did). **Mitigation:**
  confirm safe-to-deploy with the owner before the promote; for cobol-migration,
  the prod deploy is flag-gated (`COBOL_PROD_DEPLOY_ENABLED`) until readiness clears.
- **Surprise stale-bot archival** → in-flight feature branches (cobol-migration
  `feat/etl-*`) get archival warnings once `stale.yml` ships. **Mitigation:**
  confirm active branches with the ETL lead before Wave 1; use the `do-not-stale`
  opt-out label.

---

## Rollout order recommendation · Orden de despliegue recomendado

> **Resumen (ES).** Cuatro olas: chrome de bajo riesgo primero (docs/meta),
> luego chrome + protección en repos que ya despliegan, luego la migración
> build-once-promote, y al final los bloqueados por otro trabajo.

**Wave 1 (low-risk chrome, no CI/CD changes):** ✅ **`Interval-Col/operations`
done first** (2026-06-06, PR operations#2 + #3) — landed as the docs-only
reference implementation; gitleaks as the sole required check.
**Remaining in Wave 1**: `Interval-Col/.github` (the meta-repo that hosts the
canonical configs the others copy from — bootstrapping itself is paradoxical
but valuable) and `commercial-lch` (has no deploy pipeline yet, so the chrome
+ protection rollout is risk-free and won't break any release). The
`operations` PRs are the most direct precedent for `.github` because both
are docs/meta repos without a `develop` branch.

**Wave 2 (chrome + protection on repos that already deploy):** ~~`lab-qc` then
`finance-lch`.~~ Originally planned chrome + protection only with the CI/CD
reshape deferred to Wave 3 — in practice, **`finance-lch` did Waves 2 and 3
together** on 2026-06-04 because the two were tightly coupled and the team
was already in flight. That worked; the same one-shot approach is now
recommended for `lab-qc` too, using `finance-lch`'s PR #8 as the template.

**Wave 3 (build-once-promote migration):** ✅ `finance-lch` done (folded
into Wave 2). Remaining: `lab-qc` → `cobol-migration`. lab-qc copies the
`promote-*` jobs from `finance-lch`/.github/workflows/ci-cd.yml — `environment:
production` is already wired there, so the migration should be even cleaner.
`cobol-migration` last because it needs the `chore/etl-cicd` merge to `main`
as a pre-req. Backfill `commercial-lch` with the same green-field pipeline
once the template is proven.

**Wave 4 (blocked-on-other-work):** `admission-patient`. Cannot protect a
permanently-red CI; cannot deploy without Phase H2. Sequence: Phase H2 (OIDC
+ private package) → CI green → chrome + protection → deploy pipeline. Treat
this repo as parked on this plan until H2 lands. *(2026-06-13: the H2 CI
blocker resolved — alexandria removed in the shadcn migration — so the chrome
+ protection landed; only the deploy port remains deferred.)*

---

## References

- `Interval-Col/.github/BRANCHING-AND-DEPLOY.md` — the policy this plan enforces
  (§"Merge mode", §"main — today", §"develop — today").
- [PR Interval-Col/.github#4](https://github.com/Interval-Col/.github/pull/4) —
  where `BRANCHING-AND-DEPLOY.md` landed.
- [Interval-Col/rfcs#6](https://github.com/Interval-Col/rfcs/discussions/6) —
  companion org discussion.
- `Interval-Col/finance-lch` PR #8 — the reference build-once-promote + chrome
  implementation other repos copy.
- `operations/plans/cobol-migration-promote-to-prod.md` + issue #7 — the
  cobol-migration prod go-live (owned by @ychejne-jpg).
- `admission-patient/plans/deploy-pipeline-go-live-plan.md` + issue #21 — the
  deferred admission-patient deploy port (H2).
- `.github/templates/plan-template.md` — the canonical plan shape this document
  conforms to.
