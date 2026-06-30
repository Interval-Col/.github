---
status: proposed
created: 2026-06-27
updated: 2026-06-29
owner: SKuger01
implementation: SKuger01
language: English body; Spanish "Resumen".
builds-on: plans/branching-policy-rollout.md (baseline) + issue #42
issue: https://github.com/Interval-Col/.github/issues/69
start: 2026-06-27
target: TBD
effort: M
model: claude-sonnet-4-6
sources: [finance-lch, pharos-lis, admission-patient, commercial-lch, cobolql, cobol-migration, biuman-lis, biuman-reports, pdf-render-service, api-calendar, employee-management, inventory-management, accounting-interface, operations, rfcs, .github, design-studio, infrastructure]
---

# Escalator enforcement rollout — `feature → develop → main`, made binding · Aplicación del escalator de enforcement

> **Resumen (ES).** Este plan agrega la **capa de enforcement del escalator** encima
> de la línea base ya rastreada en `branching-policy-rollout.md` + issue #42 (gitleaks
> + protección de `main` + chrome). La capa nueva, por repo: (1) el workflow guard
> **`main-only-from-develop`** (un PR a `main` debe venir de `develop`), (2)
> **`enforce_admins`** ON (nadie hace bypass, ni el admin), y (3) **review-count 0**
> mientras seamos solo-maintainer (los checks de CI son la compuerta real, no una
> aprobación humana). Resultado: **`main ⊆ develop` siempre** → nada llega a prod que
> no haya pasado primero por dev. Referencia viva: `nucleus-db` (`docs/PROMOTION.md`).

> **Markers** — ✅ **Done-when** (verifiable definition of done) · 🚦 **Checkpoint** (stop, show @gczuluaga the named evidence) · 🛑 **HUMAN DECISION** (an agent must not pick this — escalate to @gczuluaga) · 💡 **Heuristic** (a task-earned lesson). *(ES: ✅ terminado-cuando · 🚦 punto de control · 🛑 decisión humana · 💡 heurística.)*

## Why this is a separate plan

`branching-policy-rollout.md` + [#42](https://github.com/Interval-Col/.github/issues/42)
already drive the **baseline** (gitleaks gate + `main`/`develop` protection + chrome)
across the org. This plan adds the **escalator-enforcement layer** on top — the three
rails that turn "feature→develop→main" from *documented discipline* into *CI-enforced
guarantee*. The policy of record is `BRANCHING-AND-DEPLOY.md` §"Branch protection"
(updated 2026-06-27 with this model). Decisions are not re-debated here; this plan is
only the per-repo work to make them real.

## The model (decided 2026-06-27, @gczuluaga)

For a solo gatekeeper, `enforce_admins` + `review:1` deadlocks (you can't approve your
own PR, and can't bypass). The org standard resolves it as:

| Rail | Setting | Why |
|---|---|---|
| **Promotion guard** | `.github/workflows/guard-promotion.yml` required as `main-only-from-develop` | A PR into `main` must come from `develop`. The CI-enforced escalator. |
| **`enforce_admins`** | **ON** | No `--admin` bypass — without this, every rule (incl. the guard) is advisory. |
| **Required approvals** | **0** while solo | The CI checks are the gate, not a human approval. Bump to **1** when a 2nd reviewer joins. |

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que se repiten en este plan, con su traducción y una línea de qué significan.

| English | Español | Means |
|---|---|---|
| branch protection | protección de rama | GitHub settings requiring checks/reviews before merging to a branch |
| enforce_admins | forzar en admins | setting that prevents repo admins from bypassing branch rules via `--admin` |
| guard workflow | workflow de guardia | a CI workflow (`guard-promotion.yml`) that fails if a PR targets `main` from any branch other than `develop` |
| required status check | verificación requerida | a CI check that must pass before GitHub allows a merge |
| escalator | escalator / flujo de promoción | the enforced chain `feature → develop → main`; no commit skips a step |
| baseline | línea base de protección | the foundation set: gitleaks + PR-required + main/develop protection (tracked in #42) |
| concurrency block | bloque de concurrencia | a `concurrency:` key in a GitHub Actions workflow that collapses duplicate queued runs |
| promote / promotion | promover / promoción | merge `develop → main` to push verified changes to production |
| strict up-to-date | actualización estricta | GitHub option requiring a PR branch to be up to date with the base before merging |
| review count 0 | 0 revisiones requeridas | required approvals set to zero; CI checks are the gate, not a human approval |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — se gestiona en otros planes o issues.

- `transmisiones`, `port-mapper` — still on `master`; fold in on the `master→main` rename (tracked in #42 / RFC 0009).
- `legacy-repositories` — archive.

## Per-repo reusable steps (repo that already has baseline + a `develop` branch)

> **Resumen (ES) — Pasos reutilizables por repositorio.**
>
> Secuencia de comandos para aplicar el escalator en cualquier repo que ya tenga la línea base y una rama `develop`. Los cuatro pasos: (1) agregar el workflow guard en `develop` y promoverlo a `main`, (2) activar `enforce_admins`, (3) fijar el conteo de revisiones en 0, (4) abrir el primer PR develop→main para que el check quede seleccionable como requerido en la configuración de protección.

```bash
R=Interval-Col/<repo>
# 1. add the guard workflow on develop, then promote it to main (see step 4)
#    cp the canonical guard-promotion.yml (from nucleus-db) into .github/workflows/ on develop
# 2. enforce_admins ON
gh api -X POST repos/$R/branches/main/protection/enforce_admins
# 3. review count 0 (solo); CI checks are the gate
gh api -X PATCH repos/$R/branches/main/protection/required_pull_request_reviews \
  -F required_approving_review_count=0 -F require_code_owner_reviews=false
# 4. open the first develop→main promote PR → the guard runs (passes) →
#    Settings → Branches → main → Require status checks → add "main-only-from-develop"
```

> ⚠️ Order matters: the guard check is only selectable as *required* **after** it has
> run once (step 4 before adding it to protection). And `enforce_admins` ON + `review:1`
> will deadlock a solo owner — do step 3 (review→0) **before/with** step 2.

## Per-repo checklist (grounded in the 2026-06-27 survey)

> **Resumen (ES) — Lista de repositorios.**
>
> Checklist organizado en cinco grupos según el estado actual de cada repo. Aplicar en este orden: primero los que ya tienen línea base (escalator directo), luego los desprotegidos (línea base primero), luego los livianos (solo `enforce_admins`), y finalmente los que requieren crear la rama `develop`. Verificar con el 🚦 Checkpoint entre grupos antes de continuar.

### ✅ Done (reference)
- [x] `nucleus-db` — full escalator live (enforce_admins, review 0, guard required, `docs/PROMOTION.md`).

### 🟡 Baseline already in place + has `develop` — apply escalator now
Each needs: guard workflow + `enforce_admins` ON + `review:0`. (Required checks already include gitleaks + per-repo CI.)
- [ ] `finance-lch` — enforce_admins + guard (7 CI checks already; review 1→0)
- [ ] `pharos-lis` — enforce_admins + guard (7 checks incl. Alembic; review 1→0)
- [ ] `admission-patient` — enforce_admins + guard (checks: backend, lint-and-build, gitleaks)
- [ ] `commercial-lch` — enforce_admins + guard (Backend/Frontend CI + gitleaks)
- [ ] `cobolql` — enforce_admins + guard (Rust CI, main-source-guard, COBOL lint, gitleaks)
- [ ] `cobol-migration` — enforce_admins + guard (gitleaks; ETL)
- [ ] `biuman-lis` — enforce_admins + guard **+ turn on strict up-to-date** + add a build/test required check (only gitleaks today)
- [ ] `biuman-reports` — enforce_admins + guard **+ strict up-to-date** (+ a CI check if a pipeline exists)

### 🔴 `main` is UNPROTECTED today — baseline FIRST (#42), then escalator
These have a `develop` branch but `main` has **zero protection** (no PR required, no checks). Do the #42 baseline (gitleaks gate + PR-required + protection) **first**, then the escalator steps. Highest risk — front-load.
- [ ] `pdf-render-service` — baseline (#42) → then enforce_admins + guard + review 0
- [ ] `api-calendar` — baseline (#42) → then escalator
- [ ] `employee-management` — baseline (#42) → then escalator
- [ ] `inventory-management` — baseline (#42) → then escalator
- [ ] `accounting-interface` — baseline (#42) → then escalator (handles billing — prioritize within this group)

### 🟢 Lightweight (docs/playground, **no `develop`**) — `enforce_admins` only (no guard)
No escalator (no develop branch); just close the bypass hole. Add strict up-to-date where off.
- [ ] `operations` — enforce_admins
- [ ] `rfcs` — enforce_admins + strict up-to-date
- [ ] `.github` — enforce_admins
- [ ] `design-studio` — enforce_admins + strict up-to-date

### 🔵 Adopt-develop-first
- [ ] `infrastructure` — **create a `develop` branch** (IaC → prod hosts; currently merges straight to main), then apply the full escalator. Prioritize: this deploys to prod infrastructure.

## Plus: workflow concurrency (every repo with CI/CD)

> **Resumen (ES) — Bloque de concurrencia en todos los workflows.**
>
> Agregar un bloque `concurrency:` a cada `ci-cd.yml` (deploy) y `ci.yml` (PR gate) para evitar colas de ejecuciones encadenadas que saturen o derrumben los runners. Incluir este cambio en el mismo PR de escalator de cada repo.

Folded in 2026-06-27 after a `develop`-deploy pile-up starved + OOM-ed the dev
runner fleet. **Every repo's workflows get a `concurrency` block** so superseded
runs self-collapse instead of queueing N-deep (see `BRANCHING-AND-DEPLOY.md`
§"Concurrency"):
- **`ci-cd.yml` (deploy):** `group: deploy-${{ github.ref }}`, **`cancel-in-progress: false`** (collapse the pending queue to the newest; never interrupt a live deploy).
- **`ci.yml` (PR gate):** `group: ci-${{ github.workflow }}-${{ github.head_ref || github.ref }}`, `cancel-in-progress: true`.

This is a quick per-repo workflow edit; bundle it with each repo's escalator PR.
(Related infra fix, tracked separately: move runners to a dedicated VM + push
build/test to GitHub-hosted so CI can't starve app hosts — RFC 0007.)

## ✅ Done-when (per repo)
1. `gh api repos/Interval-Col/<repo>/branches/main/protection/enforce_admins` → `enabled: true`.
2. `main` required status checks include `main-only-from-develop` (for develop/main repos) + `gitleaks`.
3. A test PR from a `feat/*` branch **into `main` fails** the guard; a `develop → main` PR **passes**.
4. `ci-cd.yml` + `ci.yml` carry the `concurrency` block (no more queue pile-ups).
5. The repo's row here is checked.

## 🚦 Checkpoint (per group)
Show @gczuluaga: the `gh api … protection` output for one repo in the group + a screenshot of a feature→main PR being blocked by the guard. Confirm before moving to the next group.

---

## Decisions · Decisiones

**Open:**

- 🛑 **Target date** — No enforcement deadline is set (`target: TBD` in frontmatter). Pending: @gczuluaga sets the timeline and updates the frontmatter `target:` field. *(ES: fecha límite de enforcement — pendiente de definición por @gczuluaga.)*

**Resolved during planning:**

- **Solo-gatekeeper enforcement model** — `enforce_admins` ON + `review:0` resolves the deadlock where an admin cannot approve their own PR and cannot bypass via `--admin`. Bump to `review:1` when a second maintainer joins. *(2026-06-27.)*
- **Concurrency strategy** — `ci-cd.yml` uses `cancel-in-progress: false` (never interrupt a live deploy); `ci.yml` uses `cancel-in-progress: true` (collapse stale PR gate runs). *(2026-06-27.)*
- **biuman repos get strict up-to-date flag** — `biuman-lis` and `biuman-reports` currently have only gitleaks as a required check; adding strict up-to-date is noted explicitly in the checklist as a signal to add a real build/test check. *(2026-06-27 survey.)*

## Risks · Riesgos

> **Resumen (ES).** El riesgo principal es habilitar `enforce_admins` antes de que el guard sea un check requerido — el bypass desaparece pero el guard queda advisory. El segundo riesgo es aplicar `review:1` en lugar de `review:0`, lo que bloquea al mantenedor solitario. El orden de los pasos en la sección de pasos reutilizables es la mitigación.

- **`enforce_admins` enabled before guard is a required check** → admin bypass is removed, but a direct feature→main PR can still reach `main` because the guard is only advisory. **Mitigation:** complete step 4 (open the first develop→main PR to trigger the guard check) *before* adding it as a required check in branch settings — the step order in `## Per-repo reusable steps` encodes this sequence.
- **`review:1` set instead of `review:0` on a solo repo** → deadlock: the admin cannot approve their own PR and cannot use `--admin` bypass. **Mitigation:** step 3 in the reusable steps explicitly sets `required_approving_review_count=0`; verify the API response confirms the new value after running.
- **`biuman-lis` / `biuman-reports` lack a build/test required check** → the escalator guard alone does not catch code regressions on these repos. **Mitigation:** the checklist note ("add a build/test required check if a pipeline exists") tracks this; treat as a follow-up once CI is added to those repos.
- **`infrastructure` deploys directly to prod hosts from `main`** → highest blast radius of any repo in scope; creating `develop` is a prerequisite before any escalator steps. **Mitigation:** front-load within the `🔵 Adopt-develop-first` group; @gczuluaga gates the first develop→main promote PR for this repo.

## References

- `plans/branching-policy-rollout.md` — baseline plan (gitleaks + protection) this plan builds on top of.
- [#42](https://github.com/Interval-Col/.github/issues/42) — baseline tracking issue (gitleaks + protection rollout).
- [#69](https://github.com/Interval-Col/.github/issues/69) — this plan's linked issue.
- `BRANCHING-AND-DEPLOY.md` §"Branch protection" and §"Concurrency" — policy of record; updated 2026-06-27.
- `nucleus-db/docs/PROMOTION.md` — canonical reference implementation of the full escalator.
- RFC 0009 — Bitbucket→GitHub migration; scope for `transmisiones`, `port-mapper`, and the `master→main` rename.
