---
status: pending
created: 2026-06-04
owner: gczuluaga
---

# Branching & Deploy Policy — Per-Repo Rollout

This plan tracks per-repo enforcement of the branching-and-deploy policy that
landed in [PR Interval-Col/.github#4](https://github.com/Interval-Col/.github/pull/4)
(`BRANCHING-AND-DEPLOY.md`), with companion org discussion at
[Interval-Col/rfcs#6](https://github.com/Interval-Col/rfcs/discussions/6). The
audit below was run on 2026-06-04 across the six repos in scope; this document
turns each audit's gap list into a per-repo checklist so we can roll out the
policy without losing track of which repo is at which stage. Locked decisions
(GitFlow-lite, squash-only, conventional commits, 5 pre-commit hooks,
build-once-promote, etc.) are not up for debate here — only the work to make
them real per repo.

## At-a-glance status matrix

Legend: ✅ done · ⚠️ partial · ❌ missing · ❓ unknown / needs admin · ⏸️ deferred (by owner)

| Repo | BP main | BP develop | Repo settings | CODEOWNERS | PR template | Stale wf | Pre-commit | CI/CD shape |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `Interval-Col/.github` | ✅ | — n/a (no `develop`) | ✅ | ✅ | ✅ | ✅ | ✅ (4 policy hooks) | **n/a deploy · ✅ gitleaks gate** |
| `Interval-Col/finance-lch` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (all 5 policy hooks) | ✅ build-once-promote · ✅ gitleaks gate |
| `Interval-Col/lab-qc` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (all 5 policy hooks) | ✅ build-once-promote · ✅ gitleaks gate |
| `Interval-Col/commercial-lch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ (0/5 policy hooks) | ⚠️ CI-only, no deploy yet |
| `Interval-Col/cobol-migration` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (no config) | ⚠️ rebuild-per-env, on develop only |
| `Interval-Col/admission-patient` | ❌ (default=`master`) | ❌ | ❌ | ✅ | ❌ | ❌ | ⚠️ (case-collision present, 4/5 missing) | ⚠️ CI-only, deploy not ported |
| `Interval-Col/operations` | ✅ | — n/a (no `develop` — docs-only) | ✅ | ✅ | ✅ | ✅ | ✅ (4 policy hooks) | **n/a deploy · ✅ gitleaks gate** |

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
and the dev deploy is green), repo settings (squash-only + auto-delete +
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

---

## `Interval-Col/.github`

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

## `Interval-Col/finance-lch`

**Status (2026-06-04):** ✅ **DONE.** All policy chrome landed, branch protection enforced on `main` and `develop`, ci-cd.yml migrated to build-once-promote. Closed via PR Interval-Col/finance-lch#8 (merged to `develop`) and the follow-up `develop` → `main` PR; repo settings + branch protection rules applied via `gh api` immediately after. This row is the first concrete reference implementation other repos can copy.

**Update 2026-06-06:** server-side **gitleaks gate** added — required status check on `main` + `develop` (PR Interval-Col/finance-lch#9) — and the repo flipped to the **merge-commit model** (squash off, linear-history off, PR-title merge messages). A one-time full-history gitleaks audit surfaced a real leak: `cobolql` API tokens + `finance_user` DB creds in `jobs/config.json` history (file already removed from `develop`). **Rotated by @gczuluaga**; the dead values are allowlisted in finance-lch's own `.gitleaks.toml` with an incident pointer, and mock-IAM / `dev-admin` placeholders are allowlisted via the canonical `.github/.gitleaks.toml`. Full-history scan: clean (462 commits).

- [x] Land policy assets — landed via PR #8 to `develop`, then promoted to `main` through the policy's own PR/squash-merge flow.
- [x] Add `.github/CODEOWNERS` — initial domain map (backend / frontend / contabilidad / infra / plans+docs), catch-all `*` → `@gczuluaga`; `frontend/` → `@SKuger01`; contabilidad cross-cutting paths require both.
- [x] Add `.github/PULL_REQUEST_TEMPLATE.md` — Why / What changed / Test plan / Rollout notes, with the CC-format reminder in the HTML preamble (squash-merge makes the PR title load-bearing).
- [x] Add `.github/workflows/stale.yml` — `actions/stale@v9`, 30d warn / 60d notify / 90d archive, daily 13:00 UTC, opt-out via `do-not-stale` label.
- [x] Extend `.pre-commit-config.yaml` with the 5 policy hooks — `check-case-conflict`, `gitleaks` (v8.21.2), `ruff`/`ruff-format` (format-on-stage), `conventional-pre-commit` (v3.6.0, commit-msg stage), local `scripts/check-branch-name.sh` (pre-push stage). 12 hooks total across 3 stages.
- [x] `ci.yml` was already at parity with the policy on this — `Frontend lint (ESLint)`, `Backend lint (Ruff + Pyright)`, `Frontend tests (Vitest)`, `Backend tests (pytest)`, `Verify API contract (regenerate then diff)`, and `Block local IAM from leaking into deploy compose` are all 6 wired into branch protection as the required check set. The audit originally flagged `verify-api-contract` as missing — that was stale; the job has existed since the API-contract slice landed in Phase 3.
- [ ] Add design-system gates job — **deferred** (see Open Questions). No repo implements this yet; tracked as a separate workstream.
- [x] Enable branch protection on `main` — applied via `gh api PUT /repos/.../branches/main/protection`. Ruleset: 6 required checks (above), 1 reviewer, dismiss stale on new commits, CODEOWNERS review required, linear history, resolved conversations required, no force-push, no deletions. `enforce_admins: false` (admin-included is the planned escalation per policy).
- [x] Enable branch protection on `develop` — applied via `gh api`. Same 6 required checks; PR optional (direct push allowed); no force-push, no deletions; linear history not required.
- [x] Repo settings — `gh api PATCH /repos/...`: `delete_branch_on_merge=true`, `allow_squash_merge=true`, `allow_merge_commit=false`, `allow_rebase_merge=false`, `has_discussions=true`.
- [x] Migrate `ci-cd.yml` to build-once-promote — push to `develop` builds `${REPO}:dev` + `${REPO}:<sha>` and deploys dev; push to `main` runs new `promote-frontend`/`promote-backend` jobs that **pull `${REPO}:dev`, retag as `${REPO}:prod` + `${REPO}:<main-sha>`, push**. Same `sha256` digest from dev → prod. `workflow_dispatch` action set expanded with `promote-and-deploy` and `promote-only`. A safety check in the `config` job refuses to BUILD a prod image from a push event.

**Owner:** @gczuluaga (executed 2026-06-04).

Actual effort: ~3h end-to-end including the chrome, hook configs, CI/CD migration, post-merge `gh api` calls, and exercising the policy's own PR-to-`main` flow as the bootstrap moment. The CI/CD migration was the bulk; chrome + settings were ~30 min total.

---

## `Interval-Col/lab-qc`

**Status (2026-06-05):** ⏸️ **DEVELOP-SIDE DONE; prod bundle deferred.** Chrome,
all 5 pre-commit hooks, build-once-promote migration, repo settings, and branch
protection on `develop` all landed via PR Interval-Col/lab-qc#3 (squash-merged to
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

## `Interval-Col/commercial-lch`

**Status:** lightest-lift app repo — no deploy pipeline today, so the build-once-promote work is "add the right pipeline" rather than "migrate"; CI already has `verify-api-contract` which is a leg up.

- [ ] Add `.github/CODEOWNERS` — `backend/` + `frontend/` to lead dev + Gloria as gate-keeper
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Add `.github/workflows/stale.yml`
- [ ] Extend `.pre-commit-config.yaml` with the 5 missing hooks
- [x] Already done: pre-commit baseline
- [x] Already done: `verify-api-contract` job present in `ci.yml` (ready to be a required check)
- [x] Already done: backend lint/format/pyright/pytest + frontend lint/vitest in `ci.yml`
- [ ] Add DS gates job (only contract diff today)
- [ ] Enable branch protection on `main` — required checks should include backend + frontend lint/tests + `verify-api-contract` + DS gates
- [ ] Enable branch protection on `develop`
- [ ] Repo settings: auto-delete on, disable merge-commit + rebase-merge
- [ ] Add a deploy workflow that implements build-once-promote from day one (no migration debt — this is the green-field win)

**Owner:** <TBD>

Estimated effort: ~1h for chrome + protection + settings + hooks; ~2-3h to author the new deploy workflow (it can copy the lab-qc one once that's migrated, so timing this last among the deploy-capable repos saves work).

---

## `Interval-Col/cobol-migration`

**Status:** the bare-cupboard repo — no pre-commit config at all, no CODEOWNERS, ci-cd.yml lives only on `develop` (unmerged to `main`, matches the open `chore/etl-cicd` branch noted in my own memory); needs the full chrome bootstrap before policy can attach.

- [ ] Merge `chore/etl-cicd` (or its successor) so `main` actually has a `.github/` tree to attach policy to
- [ ] Create `.pre-commit-config.yaml` from scratch — install all 5 policy hooks plus the lint/format baseline used elsewhere
- [ ] Add `.github/CODEOWNERS` — `services/etl/*` → ETL lead, `.github/workflows/*` → ops/platform
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md` (summary, test plan, deploy notes)
- [ ] Add `.github/workflows/stale.yml`
- [ ] Audit extra branches (`feat/etl-shared-harness`, `feat/etl-tui-enhancements`) and either rebase to `develop` or close before stale-bot starts marking them
- [ ] Enable branch protection on `main`
- [ ] Enable branch protection on `develop`
- [ ] Repo settings: auto-delete on, disable merge-commit + rebase-merge, enable Discussions
- [ ] Migrate `ci-cd.yml` to build-once-promote — currently `push to develop → build+deploy dev tag` and `push to main → build+deploy prod tag` each rebuild from source; target: build once on develop with `:sha` tag, then a separate `main` workflow that pulls + retags ECR image to `:prod`

**Owner:** <TBD>

Estimated effort: ~2-3h for full chrome bootstrap (more than the others because pre-commit config is being created from zero); ~½ day for ci-cd.yml migration once the `develop` workflow is on `main`.

---

## `Interval-Col/admission-patient`

**Status:** odd one out — default branch is `master` (not `main`), CI is intentionally KNOWN-RED pending Phase H2 (private `@intervalica/alexandria` package unreachable from cloud runners), and there's no deploy pipeline yet; CODEOWNERS is the only repo here that already has it.

- [ ] **Decision needed:** rename `master` → `main`, or grandfather `master` as the protected branch? (See Open questions below.) Default assumption for this checklist: rename to `main`.
- [ ] Rename default branch `master` → `main` (ProTip: open a tracking PR first that retargets any active branches off `master`)
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md` (Summary / Risk / Rollback)
- [ ] Add `.github/workflows/stale.yml`
- [ ] Extend `.pre-commit-config.yaml` with the 4 still-missing policy hooks: `gitleaks`, `format-on-stage`, `commit-msg-lint`, `branch-name-lint`
- [x] Already done: `.github/CODEOWNERS` present (only repo in the org with this today — its mapping should be sanity-checked against the policy but the file exists)
- [x] Already done: pre-commit `check-case-collisions` hook present (functional equivalent to the policy `case-collision` hook)
- [x] Already done: pre-commit baseline (`end-of-file-fixer`, `trailing-whitespace`, `check-merge-conflict`, `check-yaml`, `check-added-large-files`, `eslint`)
- [ ] Fix CI before flipping required-status-checks on main: the `@intervalica/alexandria` private-package issue must land first (Track 2 Phase H2 — GitHub OIDC + AWS trust); protecting `main` against a permanently-red check is worse than no protection
- [ ] Enable branch protection on `main` (or `master` if not renamed) per §"main — today" — gate behind the CI-green fix above
- [ ] Enable branch protection on `develop`
- [ ] Repo settings: auto-delete on, disable merge-commit + rebase-merge
- [ ] Add deploy pipeline implementing build-once-promote (currently no deploy at all; Bitbucket-era ECR/SSH deploy not yet ported — Phase H2 work)

**Owner:** <TBD>

Estimated effort: ~1h for chrome + hook + PR template + stale once CI is green; protection enforcement is blocked on Phase H2 (KNOWN-RED CI); deploy pipeline ~½ day after H2 lands.

---

## `Interval-Col/operations`

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
  - `delete_branch_on_merge=true`, `allow_squash_merge=true`, `allow_merge_commit=false`, `allow_rebase_merge=false`, `has_discussions=true`. Applied + verified.
- [x] Enable branch protection on `main` per §"main — today":
  - PR required, 1 reviewer (CODEOWNERS auto-routes the right person per path), resolved threads, dismiss-stale-on-new-commits, linear history, no force-push, no deletions. `enforce_admins: false` (admin-included is the planned escalation, same as finance-lch — keeps the solo owner from being deadlocked on self-review).
  - **Required status checks**: only `gitleaks` (the meaningful gate for a docs-only repo). The `Frontend lint` / `Backend lint` / `*tests` / `verify-api-contract` set from finance-lch doesn't apply here — there's no code to lint, no tests to run, no API contract.
- [ ] **Skip**: branch protection on `develop` — operations has no `develop` branch and doesn't need one. Docs-only repos with no integration-branch model (same pattern as `Interval-Col/.github`).
- [ ] **Skip**: `ci-cd.yml` migration — no deploy pipeline. No "rebuild per env" problem because there's no build.

**Owner:** @gczuluaga (with @SKuger01 as second reviewer for policy paths via CODEOWNERS).

Estimated effort: ~45 min end-to-end for the remaining items. Mostly file creation + a single `gh api PATCH` for repo settings + branch protection on `main` only.

---

# Cross-cutting work

## 1. Build-once-promote CI/CD migration

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
- [ ] `cobol-migration` — merge ci-cd.yml to `main` first, then split
- [ ] `commercial-lch` — green-field: author the build-once-promote workflow from the start (no migration debt)
- [ ] `admission-patient` — blocked on Track 2 Phase H2 (private-pkg + OIDC); author once H2 lands

## 2. Hook installation rollout

The 5 required policy hooks and reference configs:

| Hook | Reference / source |
|---|---|
| `case-collision` | `pre-commit-hooks-org/check-case-conflict` (admission-patient has a local-script equivalent named `check-case-collisions` — keep or replace at owner discretion) |
| `gitleaks` | `gitleaks/gitleaks` pre-commit mirror |
| `format-on-stage` | wrap project formatter (ruff-format / prettier / eslint --fix) in a `local` repo block that runs on staged files only |
| `commit-msg-lint` | `commitlint` + `@commitlint/config-conventional`; runs in `commit-msg` stage |
| `branch-name-lint` | `branch-name-lint` npm pkg in a `local` repo `pre-push` hook; config restricts to `<type>/<short-kebab-slug>` |

Canonical `.pre-commit-config.yaml` + `commitlint.config.js` +
`branch-name-lint.config.js` will live in `Interval-Col/.github` (see that
repo's checklist above). Each app repo copies + tunes the patterns.

Per-repo install checkbox:

- [ ] `.github` — author the canonical configs
- [x] `finance-lch` — **done 2026-06-04** (PR #8). All 5 policy hooks installed (`check-case-conflict`, `gitleaks` v8.21.2, `ruff`/`ruff-format`, `conventional-pre-commit` v3.6.0 at commit-msg, local `scripts/check-branch-name.sh` at pre-push). `default_install_hook_types: [pre-commit, commit-msg, pre-push]` so a single `pre-commit install` activates all stages.
- [x] `lab-qc` — **done 2026-06-05** (PR #3). All 5 policy hooks (`check-case-conflict`, `gitleaks`, `ruff`/`ruff-format`, `conventional-pre-commit` at commit-msg, local `scripts/check-branch-name.sh` at pre-push) + `default_install_hook_types`. Byte-identical to finance-lch.
- [ ] `commercial-lch` — copy + commit
- [ ] `cobol-migration` — create `.pre-commit-config.yaml` from scratch using the canonical set
- [ ] `admission-patient` — copy + commit (only 4 of 5 needed — `check-case-collisions` already present)

Also add a CI job in each repo that runs `pre-commit run --all-files` so the
hooks are enforced even when contributors haven't run `pre-commit install`
locally. This becomes a required status check.

## 3. Branch protection enforcement procedure

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
   - [x] Require linear history: **on**
   - [x] Do not allow bypassing the above settings: **on**
   - [ ] Allow force pushes: **off**
   - [ ] Allow deletions: **off**
3. **Add branch protection rule** → **Branch name pattern: `develop`** with policy §"develop — today":
   - [x] Require status checks to pass before merging (applies on direct push too via "Restrict pushes" rule) — required checks: lint + tests
   - [ ] Allow force pushes: **off**
   - PR-required: **off** (policy does not require it for develop)
4. **Settings** → **General** → **Pull Requests**:
   - Allow squash merging: **on**
   - Allow merge commits: **off**
   - Allow rebase merging: **off**
   - Automatically delete head branches: **on**

Run this checklist verbatim per repo. The audit-derived checklists above flag
which gates each repo is missing — the procedure here is the "how".

---

## Definition of done (per repo)

- [ ] Branch protection enforced on `main` and `develop` per the policy
- [ ] CODEOWNERS in place
- [ ] PR template in place
- [ ] Stale workflow live
- [ ] All 5 required pre-commit hooks installed and running in CI
- [ ] `ci-cd.yml` migrated to build-once-promote (or authored that way for green-field repos)
- [ ] Repo settings: auto-delete + squash-only verified

A repo is "rolled out" when every box above is checked. Track per-repo
completion by checking off the per-repo sections — when a section is all-green,
update the at-a-glance matrix.

---

## Rollout order recommendation

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
this repo as parked on this plan until H2 lands.

---

## Open questions

- **`admission-patient` default branch**: rename `master` → `main` (aligns with policy and the rest of the org) or grandfather `master`? Renaming requires retargeting any open PRs + updating CI triggers + dev-facing remote tracking. Recommendation: rename, but explicit go/no-go needed before Wave 4 starts.
- **`Interval-Col/.github` develop branch**: policy assumes `main ← develop ← <type>/<slug>` everywhere, but a meta/policy repo arguably doesn't need `develop` (no deploy pipeline, no integration branch). Should we exempt it, or create `develop` for consistency? Recommendation: create it for consistency — cost is zero, policy stays uniform.
- **Admin permission scope**: the audit ran with read-level token access for protection endpoints (HTTP 404 on unprotected branches looks the same as "we can't see it"). Before any owner runs the enforcement procedure, confirm they have admin on each repo — Gloria + @SKuger01 are the likely set but not verified here.
- **Required status check names**: policy lists "lint + unit tests + verify-api-contract + design-system gates" but each repo's check names differ (`lint-frontend` vs `lint`, `test-backend` vs `unit tests`, etc.). Do we standardize the job names across repos as part of this rollout, or accept per-repo names and just enumerate them in each protection rule? Recommendation: enumerate per-repo for Wave 1-2 (don't block on rename), standardize as a follow-up.
- **DS gates job**: finance-lch and lab-qc have no design-system gate today; commercial-lch has only contract diff. Required check "design-system gates" is policy but no repo implements it. Out of scope for this rollout, or in-scope? Recommendation: out of scope here — track as a separate cross-cutting workstream so this plan can close.
- **cobol-migration extra branches**: `feat/etl-shared-harness` and `feat/etl-tui-enhancements` are in-flight; stale-bot will start counting against them once it ships. Confirm with the ETL lead whether they're active before Wave 1 to avoid surprise archival warnings.
