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

Legend: ✅ done · ⚠️ partial · ❌ missing · ❓ unknown / needs admin

| Repo | BP main | BP develop | Repo settings | CODEOWNERS | PR template | Stale wf | Pre-commit | CI/CD shape |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `Interval-Col/.github` | ❌ | ❌ (no branch) | ❌ | ❌ | ❌ | ❌ | ❌ | n/a (meta-repo) |
| `Interval-Col/finance-lch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ (3/8 base hooks, 0/5 policy hooks) | ⚠️ rebuild-per-env |
| `Interval-Col/lab-qc` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ (0/5 policy hooks) | ⚠️ rebuild-per-env |
| `Interval-Col/commercial-lch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ (0/5 policy hooks) | ⚠️ CI-only, no deploy yet |
| `Interval-Col/cobol-migration` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (no config) | ⚠️ rebuild-per-env, on develop only |
| `Interval-Col/admission-patient` | ❌ (default=`master`) | ❌ | ❌ | ✅ | ❌ | ❌ | ⚠️ (case-collision present, 4/5 missing) | ⚠️ CI-only, deploy not ported |

Headline: zero repos have branch protection today, zero have the policy hook
set, only one has a CODEOWNERS file. The rollout is wide but each repo is a
small amount of work — the bulk of effort is the CI/CD migration in the three
repos that already deploy.

---

## `Interval-Col/.github`

**Status:** the meta-repo that publishes the policy is itself unprotected and
missing the chrome it prescribes; needs a bootstrap pass before it can be the
template source for the other repos.

- [ ] Create `develop` branch off `main` (does not exist yet)
- [ ] Enable branch protection on `main` per §"main — today" (PR required, 1 reviewer, resolved threads, linear history, CODEOWNERS review, no force-push, no deletions)
- [ ] Enable branch protection on `develop` per §"develop — today" (no force-push, required status checks on direct push)
- [ ] Add `.github/CODEOWNERS` — route `BRANCHING-AND-DEPLOY.md`, `ENGINEERING_STANDARDS.md`, `agents/`, `templates/`, `instructions/` to `@SKuger01` + Gloria
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md` — this will become the org-default for any repo without its own
- [ ] Add `.github/workflows/stale.yml` (30d warn / 60d notify / 90d archive) — needed even here so policy/template PRs don't rot
- [ ] Add `.pre-commit-config.yaml` with the 5 policy hooks (this repo will host the reference config the others copy)
- [ ] Repo settings: turn on auto-delete-on-merge, disable merge-commit + rebase-merge (squash-only), enable Discussions
- [ ] Land `commitlint.config.js` + `branch-name-lint.config.js` at the root as the canonical copies the other repos can vendor

**Owner:** <TBD>

Estimated effort: ~2h end-to-end — this is mostly file creation + a settings toggle pass, plus the one-time job of authoring the canonical hook configs. No CI/CD migration here.

---

## `Interval-Col/finance-lch`

**Status:** policy chrome entirely absent (no protection, no CODEOWNERS, no PR template, no stale workflow); pre-commit exists but lacks all 5 policy hooks; ci-cd.yml is the worst offender on rebuild-per-env.

- [ ] Land policy assets on `main` directly (the audit notes `main` has no `.github/` tree — assets currently live on `develop` only)
- [ ] Add `.github/CODEOWNERS` — `backend/` → API leads, `frontend/` → FE leads, `alembic*/` + `seeds/` → DB owners (per `database.agent.md`), `.github/` → platform
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md` — Why / What changed / Test plan / Rollout notes, with DS gates checkbox row
- [ ] Add `.github/workflows/stale.yml` (30/60/90)
- [ ] Extend `.pre-commit-config.yaml` with the 5 missing hooks: `case-collision`, `gitleaks`, `format-on-stage`, `commit-msg-lint`, `branch-name-lint`
- [x] Already done: pre-commit baseline (`end-of-file-fixer`, `trailing-whitespace`, `check-merge-conflict`, `check-yaml`, `check-added-large-files`, `ruff`, `ruff-format`, `eslint`) — Phase-0 baseline mirrors lab-qc
- [x] Already done: `ci.yml` runs `lint-frontend`, `lint-backend`, `test-frontend`, `test-backend` on PR — these become the required status checks
- [ ] Add a `verify-api-contract` job (currently absent) before wiring required checks on `main`
- [ ] Add design-system gates job (none today)
- [ ] Enable branch protection on `main` — required checks: `lint-frontend`, `lint-backend`, `test-frontend`, `test-backend`, `verify-api-contract`, DS gates; 1 reviewer; resolved threads; linear history; CODEOWNERS review; no force-push; no deletions
- [ ] Enable branch protection on `develop` — required status checks on direct push, no force-push
- [ ] Repo settings: auto-delete on, disable merge-commit + rebase-merge (squash-only), enable Discussions
- [ ] Migrate `ci-cd.yml` from rebuild-per-env to build-once-promote (see Cross-cutting §1 below) — this is the load-bearing item

**Owner:** <TBD>

Estimated effort: ~1h for protection + settings + CODEOWNERS + PR template + stale + hook config; ~½ day for the ci-cd.yml migration (self-hosted runner + AWS ECR retag is straightforward but the prod path is workflow_dispatch today and needs reshaping).

---

## `Interval-Col/lab-qc`

**Status:** mirrors finance-lch's gaps almost exactly; both main and develop exist but neither is protected; lab-qc is the closer-to-canonical repo so its config will become the template for finance-lch.

- [ ] Add `.github/CODEOWNERS` — `backend/` → backend owners, `frontend/` → FE owners, `.github/` + `alembic*/` → infra/db owners
- [ ] Add `.github/PULL_REQUEST_TEMPLATE.md` (summary, scope, screenshots, DS gates checklist)
- [ ] Add `.github/workflows/stale.yml` (30/60/90)
- [ ] Extend `.pre-commit-config.yaml` with the 5 missing policy hooks
- [x] Already done: pre-commit baseline (lint/format hooks installed)
- [x] Already done: `ci.yml` lint+tests pipeline that can feed required-status-checks
- [x] Already done: `environment: production` already wired in `ci-cd.yml` — promote gate is in place, just needs to gate a retag instead of a rebuild
- [ ] Enable branch protection on `main` per policy §"main — today"
- [ ] Enable branch protection on `develop` per policy §"develop — today"
- [ ] Repo settings: auto-delete on, disable merge-commit + rebase-merge, enable Discussions
- [ ] Migrate `ci-cd.yml` to build-once-promote: keep build on push-to-develop, replace prod `workflow_dispatch` rebuild with `docker pull <dev-tag> && docker tag :dev :prod && docker push :prod` step

**Owner:** <TBD>

Estimated effort: ~1h for chrome + protection + settings; ~½ day for the ci-cd.yml migration (cleaner than finance-lch because the production environment gate is already wired).

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

- [ ] `finance-lch` — split build/deploy; prod path becomes retag-only (currently workflow_dispatch rebuilds)
- [ ] `lab-qc` — same pattern as finance-lch; `environment: production` already wired so the approval gate is free
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
- [ ] `finance-lch` — copy + commit
- [ ] `lab-qc` — copy + commit
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

**Wave 1 (low-risk chrome, no CI/CD changes):** `Interval-Col/.github` first,
because it hosts the canonical configs the others copy; then `commercial-lch`
because it has no deploy pipeline yet, so the chrome + protection rollout is
risk-free and won't break any release. These two give us a working template
and an end-to-end dry run.

**Wave 2 (chrome + protection on repos that already deploy):** `lab-qc` then
`finance-lch`. Chrome + branch protection only; defer the build-once-promote
migration to Wave 3 so we don't conflate "policy chrome" with "CI/CD reshape".
lab-qc goes first because its `environment: production` gate is already wired.

**Wave 3 (build-once-promote migration):** `lab-qc` → `finance-lch` →
`cobol-migration`. lab-qc's migration becomes the template; finance-lch
mirrors it; cobol-migration last because it also needs the chore/etl-cicd
merge to `main` as a pre-req. Then backfill `commercial-lch` with the
green-field pipeline once the template is proven.

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
