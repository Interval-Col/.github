# Branching, CI/CD, and deploy policy

The org-wide standard for git branching, pull requests, branch
protection, CI gates, deploys, hooks, releases, and hotfixes.

Lives in `.github` so every repo can link to one source of truth.
[`ENGINEERING_STANDARDS.md`](ENGINEERING_STANDARDS.md) summarizes; this
doc is the detailed reference.

---

## TL;DR — quick reference

| Topic | Standard |
|---|---|
| Branch model | **GitFlow-lite**: `main` ← `develop` ← `<type>/<slug>` |
| Default branch | `main` |
| Integration branch | `develop` |
| Feature branch format | `<type>/<short-kebab-slug>` (e.g. `feat/sso-mock`) |
| `<type>` prefixes | `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `hotfix`, `ci` |
| Commit & PR title format | Conventional Commits, **enforced on both** |
| Merge mode | **Merge commit** (everywhere) — PR-gated; no direct pushes to protected branches |
| Auto-delete merged branches | **Yes** |
| PR required for `main` | **Yes** — green CI incl. the `main-only-from-develop` guard; **`enforce_admins` ON** (no bypass); reviewers **0** while solo / **1** with a 2nd reviewer |
| PR required for `develop` | No — direct push allowed; CI still required |
| Force-push on `main` / `develop` | **Never** (protected) |
| Required CI on PR-to-`main` | `gitleaks` (the one universally-required context) + the repo's lint, unit-test and API-contract checks — **exact job/context names are per-repo** (illustratively `lint-frontend`/`test-backend`/`verify-api-contract`) — plus any repo-specific design-system gates. Docs-only repos require `gitleaks` only. |
| Prod deploy trigger | **Auto on merge to `main`** (PR review = deploy approval) |
| Dev-server deploy trigger | Auto on push to `develop` |
| Build / promote model | **Build once on `develop`, promote SAME image to prod** — never rebuild per environment (see §"Build-once-promote") |
| Image tagging | Built with `<commit-sha>`; retagged `v1.2.3` on promote; deploys ideally pin by `sha256` digest |
| Release tag on `main` | **Semver** (`v1.2.3`) + GitHub Release per deploy |
| Hotfix flow | `hotfix/*` off `main` → PR to `main` → merge `main` forward into `develop` |
| Stale branch policy | Warn @30d (label `stale`) / archive + close @90d (label `stale-archived`) — `actions/stale` re-comments naturally as the close window advances; no separate 60-day ping |
| CODEOWNERS | Required per repo |
| Pre-commit hooks | case-collision + secret scan + format-on-stage + commit-msg lint + branch-name lint |

---

## Three environments

Every change flows through these three:

| Environment | Where it runs | Branch source | `IAM_URL` |
|---|---|---|---|
| **Local laptop** | developer's machine | feature branch checked out | mock IAM in `docker-compose.yml` |
| **Develop server** | hosted, LAN/VPN access to corp SSO | `develop` head, auto-deployed by CI/CD | real dev SSO (e.g. `devapi.hematologico.com/auth`) |
| **Prod** | hosted, LAN access | `main` head, auto-deployed by CI/CD | real prod SSO |

Both hosted environments use the same deploy artifact (`docker-compose.deploy.yml`)
with environment-specific env values injected by CI/CD. The mock IAM
only ever runs on a laptop — see each repo's `docs/DEV-LOGIN.md`.

Pushes to `develop` exercise the real corp SSO on the develop server,
so any integration breakage is caught **before** merge to `main`.

---

## Daily flow

```
┌─────────────────────────┐
│ feat/my-thing branch    │ ← created from `develop`
└─────────────────────────┘
            │ commits + pushes (CI runs on every push)
            ▼
   ╔══════════════════════════════════════╗
   ║  PR → develop                        ║
   ║  (optional — direct push is allowed) ║
   ╚══════════════════════════════════════╝
            │ merge-commit via PR OR direct push (CI must pass)
            ▼
┌─────────────────────────┐
│ develop                 │ → auto-deploys to dev server (real SSO)
└─────────────────────────┘
            │ batched into a PR when ready to ship
            ▼
   ╔══════════════════════════════════════╗
   ║  PR → main  (REQUIRED)               ║
   ║  + 1 reviewer + green CI + threads   ║
   ║    resolved                          ║
   ╚══════════════════════════════════════╝
            │ merge-commit (via PR)
            ▼
┌─────────────────────────┐
│ main                    │ → auto-deploys to prod
└─────────────────────────┘
            │ post-deploy
            ▼
   tag `v1.2.3` + GitHub Release with auto-drafted notes
```

A PR-to-`main` is typically a "promote develop to prod" — the PR's
diff is whatever is on `develop` that's not on `main`. The PR review
*is* the deploy approval.

---

## Pull requests

### PR title

Must follow **Conventional Commits**:

```
<type>(<scope>)?: <short summary>
```

Examples:
- `feat(frontend): re-enable Nuxt SSR, opt out client-only dashboards`
- `fix(auth): respect ALLOW_LOCAL_IAM in startup guard`
- `docs: codify SSR rendering-mode standard`

The PR title **becomes the merge-commit subject on `main` /
`develop`** (each repo's merge button is configured to use the PR
title, not the default `Merge pull request #N from …`). A bad PR
title = a bad git log entry forever. CI rejects non-conforming titles.

### PR description

Use the repo's PR template — or, if a repo has none, the **org-default**
at [`Interval-Col/.github/.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/Interval-Col/.github/blob/main/.github/PULL_REQUEST_TEMPLATE.md)
applies automatically (GitHub falls back to the `.github` repo's
template for any repo without its own — so docs/meta repos don't need
their own copy). Required sections (template-enforced):

- **Why** — what problem this solves; link the plan / issue if any.
- **What changed** — short paragraph; readers should not have to read
  the diff to understand the shape of the change.
- **Test plan** — what was verified, and how. Include test names,
  manual-verification steps, or screenshots.
- **Rollout / rollback notes** — if it affects deploys (env vars,
  migrations, feature flags).

### Reviewers

- PR to `main`: **1 approval required** + green CI + all threads
  resolved.
- PR to `develop`: review optional, but use a PR if you want one.
- CODEOWNERS auto-requests reviewers based on the paths touched (see
  [CODEOWNERS](#codeowners)).

### Merge mode

**Merge commit** — everywhere, always. Every PR lands as a GitHub
merge commit, so the branch's work shows as a visible **arc** in the
graph and you can see exactly what merged when. Configure each repo's
GitHub settings to:
- **Enable** "Allow merge commits"
- Disable "Allow squash merging"
- Disable "Allow rebase merging"
- Default merge-commit message: **"Pull request title"** — so the
  merge commit's subject is the Conventional-Commits PR title, not the
  noisy default `Merge pull request #N from …`.

> ⚙️ **Order-of-operations gotcha.** If the repo *already* has branch
> protection requiring **linear history**, flipping it to merge-only
> will `422` ("you must allow squash or rebase") — merge-commit +
> required-linear-history leaves no usable strategy. Turn
> `required_linear_history` **off** in branch protection *first*, then
> set the repo to merge-only. (New repos with no protection yet aren't
> affected.)

**History stays clean by *gating*, not by flattening.** Arcs reach
`main`/`develop` only through a reviewed PR that GitHub merges for
you — never a hand-made `git merge` a developer pushes. The
PR-required + up-to-date + review rules in
[Branch protection](#branch-protection) are what enforce this.
`main`'s first-parent backbone is therefore a clean line of one merge
commit per PR; the feature commits live on the arc's side, reachable
but out of the way.

> Trade-off vs. squash: we regain the visual branch topology (the
> reason we switched) at the cost of feature-branch WIP commits being
> visible inside each arc. Accepted — the gate keeps the backbone
> readable.

### Auto-delete branches

Repo setting: **Automatically delete head branches** = on. Merged
feature branches are removed; they remain reachable via the closed PR
if anyone needs to dig.

---

## Branch protection

Configure via GitHub → Settings → Branches → "Add classic branch
protection rule" (or Repository rulesets if your repo is on the newer
ruleset model). Apply the rule to the named branch.

### `main` — today

| Setting | Value |
|---|---|
| Require a pull request before merging | ✅ **(the gate — the only way an arc reaches `main`; no direct pushes)** |
| Required approvals | **0** while the org is a solo gatekeeper (the CI gate below is the enforcement, not a human approval); **1** once a 2nd reviewer exists |
| Dismiss stale pull-request approvals when new commits are pushed | ✅ |
| Require review from Code Owners | ✅ |
| Require status checks to pass before merging | ✅ |
| Required status checks | **`gitleaks`** (secret scan — the one context required on every repo, even docs-only). Code repos additionally require their lint, unit-test and API-contract checks; **the job/context names are per-repo** and must be set to match that repo's actual CI (illustratively `lint-frontend`/`lint-backend`/`test-frontend`/`test-backend`/`verify-api-contract`), plus any repo-specific design-system gates (e.g. `block-mock-iam-in-deploy`). Code-less repos require only **`gitleaks`**. On every repo that has a `develop` branch, also require **`main-only-from-develop`** (the promotion guard — see below). |
| Require branches to be up to date before merging | ✅ (anchors each arc to current `main`) |
| Require conversation resolution before merging | ✅ |
| Require linear history | ❌ (incompatible with merge commits — intentionally off; the PR-required gate above keeps history clean instead) |
| Lock branch | ❌ |
| Do not allow bypassing the above settings (`enforce_admins`) | ✅ **ON** — the rules bind admins too; no `--admin` override. This is what makes the gate *enforced*, not advisory. |
| Allow force pushes | ❌ (never) |
| Allow deletions | ❌ |

> **Solo-maintainer reality.** With a single Code Owner (`@gczuluaga`), GitHub
> won't let an author approve their own PR, so a **Required approvals: 1** rule
> would be unsatisfiable on the gatekeeper's own PRs. The tempting fix — turn
> `enforce_admins` *off* and merge via `--admin` override — also bypasses the CI
> gate, which makes the escalator merely advisory (an admin can push anything to
> `main`). So the standard instead sets **Required approvals: 0** and keeps
> **`enforce_admins` ON**: the **CI checks become the gate** — `gitleaks` + the
> `main-only-from-develop` guard must pass, and nobody (admin included) can bypass
> them. When a second reviewer joins, bump approvals to **1** (the other person
> satisfies it) and keep `enforce_admins` on. This is the only configuration that
> *enforces* the escalator for a solo gatekeeper instead of relying on discipline.

### `main` — planned escalation

`enforce_admins` (do-not-allow-bypassing) is **already standard** (see the table
above) — it moved out of this section once the *Required approvals: 0*
accommodation made it solo-compatible. The one remaining future tightening:

| Setting | Value |
|---|---|
| Require signed commits | ✅ |

This adds setup friction (GPG/SSH signing per developer); it lands when the team
has the key-management workflow in place.

### `develop` — today

| Setting | Value |
|---|---|
| Require a pull request before merging | ❌ (direct push allowed) |
| Require status checks to pass before merging | ✅ |
| Required status checks | same set as `main` |
| Allow force pushes | ❌ (never) |
| Allow deletions | ❌ |

A direct push to `develop` still needs CI to pass — GitHub enforces
this when "Require status checks" is on regardless of whether a PR
was used.

### Feature branches

No protection. Free-for-all on `feat/*`, `fix/*`, etc. — including
force-push within your own feature branch.

### Promotion guard — `main-only-from-develop`

GitHub can't natively restrict a PR's *source* branch, so a tiny required check
enforces the escalator: **a PR into `main` must come from `develop`.** Combined
with `enforce_admins` on, this guarantees **`main ⊆ develop`** — nothing reaches
`main` (→ prod) that wasn't on `develop` (→ deployed + tested on dev) first. Add
it to every repo that has a `develop` branch and wire `main-only-from-develop`
into `main`'s required status checks.

```yaml
# .github/workflows/guard-promotion.yml
name: Promotion guard
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  main-only-from-develop:
    name: main-only-from-develop
    runs-on: ubuntu-latest
    steps:
      - name: Require main PRs to originate from develop
        env:
          HEAD_REF: ${{ github.head_ref }}
        run: |
          if [[ "$HEAD_REF" != "develop" ]]; then
            echo "::error::PR into 'main' must come from 'develop' (got '$HEAD_REF'). Promote via develop → main; never merge a feature branch straight to main."
            exit 1
          fi
          echo "✓ main PR originates from develop."
```

> **The check only becomes selectable as "required" after it has run once** — open
> the first `develop → main` promote PR, let the guard run (it passes, since the
> head *is* `develop`), then add `main-only-from-develop` to `main`'s required
> checks. Reference implementation: `Interval-Col/nucleus-db`
> (`.github/workflows/guard-promotion.yml` + `docs/PROMOTION.md`).

Repos **without** a `develop` branch (docs-only) skip the guard — they have no
escalator; their rails are `enforce_admins` + `gitleaks` + PR-required.

---

## CI / CD

Every repo uses GitHub Actions. Two workflow files per repo:

### `.github/workflows/ci.yml` — PR / push gate

- Triggers: `pull_request` and `push` against `main`, `develop`,
  feature branches.
- Jobs: lint (frontend ESLint + design-system gates; backend ruff +
  pyright), tests (Vitest + pytest), `verify-api-contract` for
  full-stack repos, any repo-specific gates.
- All jobs are **required** on PR-to-`main`. See the "Required CI"
  list under Branch protection above.

### `.github/workflows/ci-cd.yml` — deploy

- Triggers:
  - `push: branches: [develop]` → builds + deploys all services to
    the **develop server**.
  - `push: branches: [main]` → builds + deploys to **prod**.
  - `workflow_dispatch` → manual run with `environment` + `services`
    + `action` inputs (used for re-deploys, single-service deploys,
    etc.).
- Builds Docker images, pushes to the org registry, SSHes to the
  target host and `docker compose -f docker-compose.deploy.yml pull
  && up -d`.
- **Deploy gating:** none beyond merge — merging to `main` IS the
  prod deploy approval. The PR review is the human gate.
- If you need a deploy without a code change (env-var rotation,
  re-pull a tag), use `workflow_dispatch` with `action: deploy-only`.

### Concurrency — collapse the queue, never pile up

Every workflow sets a `concurrency` group so superseded runs don't stack on the
self-hosted runners. A pile-up of `develop` deploys waiting on one busy runner
can starve (and has OOM-ed) the fleet — concurrency makes the queue self-collapse
to the latest instead.

- **Deploy (`ci-cd.yml`)** — one run per branch; pending runs collapse to the
  newest; a *running* deploy is **never** interrupted (no half-deploys):
  ```yaml
  concurrency:
    group: deploy-${{ github.ref }}
    cancel-in-progress: false   # let the live deploy finish; collapse the pending queue
  ```
- **PR gate (`ci.yml`)** — cancel superseded runs for the same PR/branch (saves
  runner time; safe to interrupt a build):
  ```yaml
  concurrency:
    group: ci-${{ github.workflow }}-${{ github.head_ref || github.ref }}
    cancel-in-progress: true
  ```

`cancel-in-progress: false` on deploys is deliberate: GitHub still collapses
multiple *pending* runs to the newest while the in-flight one finishes — you get
the de-dup without ever interrupting a deploy mid-rollout.

### Deploying over a remote daemon (`DOCKER_HOST=ssh`) — gotchas

The deploy jobs run on a **self-hosted runner** but target the app host
via `DOCKER_HOST=ssh://<user>@<host>`, so `docker compose pull`/`up`
execute on the **remote** daemon, not the runner. Three traps follow
from that — all three bit the pharos-lis prod-DB-TLS deploy
(pharos-lis `#34`, `#35`):

1. **ECR auth must reach the *remote* daemon.** The `Login to Amazon
   ECR` step only configures the runner's docker; the remote daemon has
   no creds, so the pull fails with `no basic auth credentials`. Inside
   the deploy step, re-login into a **clean `DOCKER_CONFIG`** (no
   `credsStore`) so the token is stored as base64 and forwarded to the
   remote daemon via the `X-Registry-Auth` header on pull:
   ```bash
   export DOCKER_CONFIG="$(mktemp -d)"
   aws ecr get-login-password --region "$AWS_REGION" \
     | DOCKER_HOST= docker login --username AWS --password-stdin "$AWS_REGISTRY"
   docker compose ... pull ...
   ```
   Works even if the app host has no AWS access. **This applies to every
   repo with the self-hosted-runner → remote-docker deploy shape.**

2. **A shared compose file is parsed in full by *every* deploy job.**
   `docker compose up <one-service>` still **validates all services** in
   the file. So an env-var bind-mount source that only one job sets
   (e.g. a cert path exported by the backend job) is blank in the other
   jobs → `invalid spec: :/path:ro: empty section between colons`. Give
   such mounts a default: `${VAR:-/dev/null}`.

3. **Stage host-side files into the deploy user's `$HOME`, not `/opt`.**
   The deploy user (e.g. `manager`) is unprivileged and can't write
   root-owned dirs. Resolve the path at deploy time
   (`ssh … 'echo "$HOME"'`), write there, and export the absolute path
   via `$GITHUB_ENV` for the compose bind mount.

### Landing an app on prod — go-live checklist

Distilled from the **pharos-lis** go-live (the first app on the shared prod
`nucleus-db`, 2026-06-20). A *green deploy is not a working app* — the chain
below is what actually has to be true. **Most of it needs no server login** —
GH secrets/vars, PRs, and `workflow_dispatch` only. The 🖥️ items touch the
host/DB and are **senior/infra work via git/Ansible/dispatch**, not for the app
implementer (see the org rule: app deploys must be junior-runnable without SSH).

1. **DB connectivity (🖥️ first).** App's prod DB role + password exist
   (Bitwarden `SRV_Nucleus-db`) and grants are applied (nucleus-db
   `apply-grants`); a `hostssl <app-host>/32 … scram-sha-256` line is in
   nucleus-db `operations/pg_hba.prod.conf` (PR → nucleus-db prod deploy); ufw
   allows the app host (infra `firewall_scoped_rules`) + a FortiGate policy if
   cross-subnet (Yanna).
2. **App-side DB TLS.** `DATABASE_URL` → `?sslmode=verify-full&sslrootcert=…`
   (psycopg2 reads it from the URL; **asyncpg does not**). `DB_SSLMODE`
   pipeline-forced to `verify-full` in prod (dev `prefer`). Ship the **public CA
   cert** as a GH **variable** (`bw | gh`), staged at deploy into the deploy
   user's **`$HOME`** (never `/opt`), mounted read-only; give the compose mount a
   default (`${CA_CERT_HOST_PATH:-/dev/null}`).
3. **ECR auth on the remote daemon** — the deploy step re-logs into a clean
   `DOCKER_CONFIG` (see the gotchas above) so `compose pull` over
   `DOCKER_HOST=ssh` authenticates.
4. **Base + API base (the #1 silent breaker).** `NUXT_APP_BASE_URL=/<app>/`
   (served under a path prefix) and **`NUXT_PUBLIC_API_BASE=https://<apps-host>/<app>/api`**
   — the full prefixed, **same-origin** URL. Empty/bare-host → root-relative
   calls → 404. It's **runtime** config: set the var + `deploy-only`, no rebuild.
5. **Proxy routes — live BEFORE go-live.** Add `location /<app>` (→ frontend)
   **and** `location /<app>/api` (rewrite + → backend) to **both**
   `intervalica-api.conf` (api host) **and** `lch-apps.conf` (apps host) in the
   `proxy` repo. The proxy **bakes config into its image**: merge to `master`,
   then run **`deploy_production` from `master` HEAD** (build is master-only;
   promoting a feature-branch commit → `no such manifest`). Recreating the proxy
   is an org-wide few-second blip.
6. **Auth (`iam`) + SSO registration.** Auth pipeline-forced to `iam` in prod
   (never silent `mock` on PHI). Register the SSO **capability**: match on the
   **live route** (`/<app>`, add both the **APP** and **API** routes), grant to
   the **prod** group (not `devapps`); the capability *label* can be the brand
   name.
7. **Promote + verify (no login).** `develop → main` build-once-promote (ship the
   bit-identical dev image). Verify via `curl`/browser only: `…/<app>/api/health`
   & `/ready` → 200, `whoami`/`permissions` → 200, FE bounces to SSO, one real
   login. Then **48 h soak**.

### Per-environment secrets

GitHub Secrets are populated from Bitwarden via the per-environment
collections layout documented in
[ENGINEERING_STANDARDS.md §"Secret management"](ENGINEERING_STANDARDS.md#-secret-management).
Never hand-edit GitHub Secrets in the UI — Bitwarden is the source of
truth.

### CI escalation

Two known escalations are deferred until the prerequisite is in place:

1. **Playwright e2e blocking** — add the e2e job to the required-status-checks
   set once each repo's suite is stable enough that flakes don't
   block merges. finance-lch's e2e is green as of 2026-05; lab-qc has
   15 specs already green.
2. **Branch protection — strict mode** — see `main` escalation row
   above.

Both should land as their own small PRs that update this doc + the
branch ruleset + the workflow's `if: false` flag.

---

## Build-once-promote (the image-promotion model)

**Standard:** the image deployed to prod MUST be bit-identical to the
image that ran on the dev server. The only way to guarantee that is
**build once, promote** — never rebuild from source for a different
environment.

### Two patterns — only one is the standard

| Pattern | What happens | Status |
|---|---|---|
| **Rebuild per environment** | Push to `develop` → build image A → deploy. Merge to `main` → rebuild image B from the same code → deploy. A and B have different bits. | ❌ **non-conforming** |
| **Build once, promote** | Push to `develop` → build, tag, push to registry → deploy. Merge to `main` → pull the SAME image from the registry, add the prod tag, deploy. No second build. | ✅ **standard** |

### Why this is the standard

Even when the source commit is identical, two builds aren't:
- Floating base-image tags (`python:3.12-slim` is a moving target —
  same tag, different bits week to week)
- Transitive dependency resolution windows (lockfiles can pick
  different sub-deps if the registry state changes mid-merge)
- Build-environment differences (runner OS patch, mirror availability)
- Layer timestamp drift

A green dev test means nothing for prod if prod is a different
binary. Build-once-promote is what makes "we tested it on dev" a real
guarantee.

**Other wins:** ~5–15 min off every prod deploy (no build step at the
prod gate), trivial rollback by re-pulling the prior tag/digest,
exact audit trail via the image digest, half the CI build cost.

This is the recommendation in *Continuous Delivery* (Humble & Farley)
and *Accelerate* (Forsgren et al.), and what every mature CD pipeline
does.

### Prerequisites — we have them

1. **Config externalized from the image.** ✅ Met — env vars are
   injected at runtime via `docker-compose.deploy.yml`, not baked into
   the image. (If you find a repo that bakes env-specific values
   into the build, that's a separate bug to fix.)
2. **A real container registry.** ✅ Met — the org ECR
   (`${AWS_REGISTRY}` in every repo's compose).

### Tagging model — three layers

Best practice is to keep three distinct identifiers and use each for
what it's good at:

| Layer | Example | What it's for | Stability |
|---|---|---|---|
| **Human version** (git tag) | `v1.2.3` | Release name; release notes; "what shipped" | Stable, human-readable |
| **Image tag** | `repo:v1.2.3`, `repo:<sha>` | Discoverable label on the image in the registry | Mutable (deliberately) |
| **Image digest** | `sha256:abc123...` | The actual immutable content hash | Immutable — the source of truth for "what is running" |

We are **git-driven**: the semver git tag is the release version, and
the image tag mirrors it. Image-driven versioning (where the image
build number IS the version, no semver, no git tag) fits trunk-based +
GitOps shops, but conflicts with every other choice in this doc
(GitFlow-lite, semver, Conventional Commit auto-bump, GitHub
Releases). Not our model.

### How the pipeline implements it

1. **`develop` push** (CI/CD `dev` job):
   - Build the image once.
   - Tag with the build SHA: `${ECR_REPO}:<commit-sha>`.
   - Push to the registry.
   - Deploy to dev server pulling that tag.
   - Record the digest in the workflow log.

2. **Merge to `main`** (CI/CD `prod` job):
   - **Do not rebuild.** Pull `${ECR_REPO}:<develop-sha>` from the
     registry (the SHA of the head commit on `develop` at promote time,
     captured from the PR's merge base or from the workflow input).
   - Add the prod tag: `docker tag` → `${ECR_REPO}:v1.2.3` (the next
     semver, computed from CC types since the last release).
   - Push the new tag (same digest under both labels).
   - Deploy to prod pulling that tag.
   - Create the GitHub Release for `v1.2.3` with auto-drafted notes.
   - Record the digest in the workflow log + release body.

3. **Rollback** (manual, `workflow_dispatch`):
   - Pick a prior tag, pull, restart. Or pin by digest for absolute
     certainty.

### The two-SHA wrinkle

`develop` and `main` get **different commit SHAs for the same
release** — true under any merge mode (the merge commit on `develop`
is a distinct object from the one on `main`). Build-once-promote
handles this naturally:
- The image is built from `<develop-sha>` (the merge commit on
  `develop` after PR-to-develop landed, OR the develop-tip at
  promote time).
- The image is **the same** across both tags — we just *retag*; we
  don't rebuild.
- Multiple tags pointing at the same digest is exactly what container
  registries are designed for.

### Migration plan

Current `ci-cd.yml` in finance-lch and lab-qc rebuilds per environment
(non-conforming). Each repo gets its own small migration PR — ~half a
day per repo:

- Split the `build` job from the `deploy` job in `ci-cd.yml`.
- `build` runs on push-to-`develop` (and on push-to-feature-branches
  if you want pre-merge build verification).
- Dev `deploy` pulls `<commit-sha>` and brings up the stack.
- Prod `deploy` does NOT build — it pulls `<commit-sha>`, retags
  `v1.2.3`, pushes, deploys.

Track in `plans/build-once-promote-migration.md` (each affected repo
gets a checkbox).

---

## Dockerfile standard

Every repo's image build follows the same shape. The Phase 2
"Backend Dockerfile shape" section of
[`STANDARDS.md`](https://github.com/Interval-Col/lab-qc/blob/main/docs/STANDARDS.md#phase-2--build--deploy-hardening)
specifies the multi-stage layout (test stage + runtime stage); this
section codifies the security + operability rules that aren't in
STANDARDS yet.

### Required

| Rule | Why | Reference |
|---|---|---|
| **Multi-stage build** (`FROM … AS build` + `FROM … AS runtime`) | Compilers / dev deps / test deps stay in the build stage — they don't ship to prod. Typical 5–10× image-size cut. | finance-lch `backend/Dockerfile` |
| **Pinned base image** with patch version (`python:3.12.7-slim`, not `python:3.12-slim`) | Same reproducibility argument as build-once-promote: a floating tag is a moving target across builds and across teams. | — |
| **Non-root runtime user** (`USER appuser` at uid 1001) | If the container is compromised, attacker doesn't have root in the namespace. Cheap; ~3 lines in the Dockerfile. | finance-lch `backend/Dockerfile` (`appuser` uid/gid 1001) |
| **`HEALTHCHECK`** instruction targeting the readiness endpoint (`/ready` for FastAPI apps per Phase-5 standard) | Docker / orchestrators detect hung containers. Without it, a wedged process looks healthy. | — |
| **`.dockerignore`** at repo root, excluding `node_modules/`, `.venv/`, `.nuxt/`, `test-results/`, `*.log`, `.git/`, anything not needed in the build context | Smaller context = faster builds + can't accidentally bake local dev state into the image | — |
| **Layer ordering for cache hygiene**: `COPY` lockfiles → install deps → `COPY` source code | Source changes don't bust the deps layer — saves minutes per rebuild on every PR | finance-lch `backend/Dockerfile` |
| **System packages cleaned in same `RUN`** (`apt-get update && apt-get install -y X && rm -rf /var/lib/apt/lists/*`) | Layer caching captures the un-cleaned state if you split into two RUNs — image stays bigger forever | — |

### Recommended

- `COPY --chown=appuser:appuser` when copying application files, so the
  runtime user actually owns its working directory.
- `WORKDIR /app` (or similar) — not the default `/`. Predictable
  filesystem layout.
- `ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1` for Python images
  — keeps `.pyc` out of the image, flushes stdout for log capture.
- `EXPOSE` the listening port — documentation only (doesn't actually
  publish), but tools (`docker scout`, IDE plugins) read it.

### Documented exceptions

Tiny single-purpose dev-only images can skip the multi-stage + non-root
rules if the rationale is in a comment at the top of the Dockerfile.
The mock-IAM image (`tools/mock-iam/Dockerfile`) is the canonical
example: 4 files, no test gate needed, runs as root inside the
container because it's never deployed to a hosted environment (defined
only in `docker-compose.yml`, not `docker-compose.deploy.yml`).
**Exceptions must be one-time** — production-running images don't
qualify.

### Reference implementations

- `finance-lch/backend/Dockerfile` — Python / FastAPI, multi-stage with
  pytest gate as the test stage, non-root `appuser` (uid 1001).
- `lab-qc/backend/Dockerfile` — same pattern, kept in cross-repo
  lockstep per the STANDARDS Phase-2 entry.

When bootstrapping a new repo, copy one of these as the starting
template; do not invent a new Dockerfile shape.

---

## Hooks

Every repo MUST install the following pre-commit hooks at clone time
via `.pre-commit-config.yaml`:

| Hook | What it does | Reference impl |
|---|---|---|
| **Case-collision check** | Rejects two paths that differ only in case (catches macOS APFS / Linux ext4 footgun) | upstream [`check-case-conflict`](https://github.com/pre-commit/pre-commit-hooks) (from `pre-commit/pre-commit-hooks`) — the actually-configured hook. (`biuman-lis/scripts/check-case-collisions.sh` is the bespoke script equivalent for repos that need custom logic; new repos should prefer the upstream `check-case-conflict`.) |
| **Secret scanning** | Rejects commits that introduce credentials, API keys, signing keys | [gitleaks](https://github.com/gitleaks/gitleaks) — the upstream pre-commit hook (bare `id: gitleaks`, which runs `gitleaks git --pre-commit` on the staged change); CI runs the pinned binary as `gitleaks detect --source . --redact --exit-code 1`. Both auto-load the repo-root `.gitleaks.toml`. |
| **Format-on-stage** | Auto-formats staged files (ruff format for Python, eslint --fix for JS/TS) | Each repo's `.pre-commit-config.yaml` (see existing lab-qc / finance-lch configs) |
| **Commit-message lint** | Rejects commit messages that don't match Conventional Commits | [`conventional-pre-commit`](https://github.com/compilerla/conventional-pre-commit) (`compilerla/conventional-pre-commit`, `--strict`, `commit-msg` stage) — the actually-enforced hook; no commitlint/husky is used |
| **Branch-name lint** | Rejects branches that don't match `<type>/<kebab-slug>` | Small custom hook (~10 lines of bash) calling `git rev-parse --abbrev-ref HEAD` |

For **code repos**, the lint/test side of this set is mirrored in CI
(so a developer who skipped the hook install — or used `git commit
--no-verify` — doesn't get a free pass): the pre-commit step is *fast
feedback*; the CI check is the gate of record. The one exception is
case-collision — there is no dedicated CI case-collision workflow in
this `.github` repo, so for **docs-only repos the pre-commit
`check-case-conflict` hook is the only enforcement**. (CI
case-collision applies in code repos via their lint pipeline.) Secret
scanning is enforced server-side everywhere — see below.

**Secret scanning is the one hook every repo MUST also enforce as a
required CI status check named `gitleaks`** — including docs-only
repos with no lint/test jobs, because a leaked credential is the worst
case regardless of whether the repo holds code.

- **Implementation:** run the pinned `gitleaks` **binary** in a
  workflow (`gitleaks detect`), *not* `gitleaks-action` — the action
  requires a paid `GITLEAKS_LICENSE` for org-owned repos and would put
  a third-party license check on the merge-critical path. Reference
  impl: [`operations/.github/workflows/gitleaks.yml`](https://github.com/Interval-Col/operations/blob/main/.github/workflows/gitleaks.yml).
- **Shared config:** the ruleset/allowlist lives in
  `Interval-Col/.github/.gitleaks.toml` (canonical); repos reference or
  copy it so "what counts as a leak" is consistent org-wide.
- **Rolling the gate onto an existing repo:** run the scan once →
  triage findings (rotate real secrets per the [incident process in
  `operations/SECURITY.md`](https://github.com/Interval-Col/operations/blob/main/SECURITY.md#incident-response),
  then allowlist the now-dead value **by its exact string, with a
  comment** noting it's rotated; allowlist genuine false positives by
  path/pattern) → *then* mark the check required. Never enable
  enforcement before the first scan is green, or you block every PR.
  Repos that already have history leaks keep a repo-specific allowlist
  block in their own `.gitleaks.toml` (a copy of the canonical config +
  the dead values) — see `finance-lch` / `lab-qc` for the pattern.

Install once per checkout:

```bash
pip install pre-commit && pre-commit install
```

---

## Conventional Commits

Format:

```
<type>(<optional-scope>): <description>

<optional body>

<optional footer(s)>
```

### `<type>` set

| Type | Use for |
|---|---|
| `feat` | new user-visible feature |
| `fix` | bug fix |
| `refactor` | code change that doesn't change behavior |
| `test` | adding or fixing tests |
| `chore` | tooling, build, dependency bumps |
| `docs` | documentation only |
| `ci` | CI/CD pipeline or workflow changes (`.github/workflows/*`, hooks config) |
| `hotfix` | an urgent prod fix — valid as **both** a branch type (`hotfix/*`, see [Hotfix flow](#hotfix-flow)) **and** a commit type (the enforced commit-msg hook accepts it) |

Same set is used for both **commit messages** AND **branch prefixes**.
The `conventional-pre-commit` allowlist accepts all of the above —
`feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `hotfix`, `ci`.

### Enforced where

- **PR title** — must follow Conventional Commits; the merge commit's
  subject is set to the PR title on `main`/`develop`, so this is the
  *load-bearing* check. (Wire a title-lint job — e.g. a
  `conventional-pre-commit` run over the title — into code repos' CI to
  block the PR; the docs-only `.github` repo gates on `gitleaks` only.)
- **Every commit** — the `conventional-pre-commit` commit-msg hook runs
  locally (`compilerla/conventional-pre-commit`, `--strict`). Catches
  `wip` / `tmp` commits before they leave the laptop.

Yes, both — the cost is one hook install; the win is that the
individual-commit history is reviewable on the PR page AND preserved
on the arc after merge.

---

## Branch naming

Format: `<type>/<short-kebab-slug>`.

Valid:
- `feat/sso-mock`
- `fix/login-redirect`
- `refactor/move-tipos-to-catalog`
- `docs/branching-and-deploy-policy`
- `hotfix/iam-startup-guard`

Invalid (the branch-name pre-commit hook rejects these):
- `my-branch` (no type)
- `feat/MySSO Mock` (not kebab; uppercase; space)
- `feature/sso-mock` (wrong type — use `feat`)
- `gczuluaga-thing` (personal-name branches discouraged)

Stale-branch automation also keys off the format — non-conforming
branches don't get the friendly stale@30d / close@90d notifications,
they just sit.

---

## Releases & tagging

### Tag per prod deploy

Every merge to `main` deploys to prod (auto, see CI/CD section). After
the deploy succeeds, the CI/CD workflow:

1. Tags the merge commit with the next **semver** version
   (`v<major>.<minor>.<patch>`).
2. Creates a **GitHub Release** for that tag.
3. Auto-drafts the release notes from the merge commits since the
   previous tag (each merge commit's subject is a PR title in
   Conventional Commits format — they group cleanly into Features /
   Fixes / Refactors / etc.).

### Semver bumping rules

- **patch** (`v1.2.3` → `v1.2.4`) — `fix`, `chore`, `docs`,
  `refactor`, `test`-only PRs.
- **minor** (`v1.2.3` → `v1.3.0`) — any `feat` PR.
- **major** (`v1.2.3` → `v2.0.0`) — breaking change. PR title or
  body includes `BREAKING CHANGE:` footer.

The release workflow infers the bump from the Conventional Commit
types in the diff. Override by adding `release-as: <version>` to the
merge commit message footer when needed.

### Pre-release / canary tags

**Not used.** Three reasons specific to our scale:

1. **The develop server IS the pre-prod gate.** Code runs on a real
   hosted server with the real corp SSO before it merges to `main`
   (see §"Three environments"). That's the role that pre-release
   tags (`v1.2.3-rc.1`) play in shops with no integration environment.
2. **Single tenant.** LCH runs every instance of every app — there's
   no "beta customer cohort" that would need a release-candidate
   artifact distinct from the GA artifact.
3. **No canary infrastructure.** Canary tags (`v1.2.3-canary.*`)
   require traffic-splitting (Istio / Linkerd / Argo Rollouts / nginx
   canary) so a small slice of traffic hits the new image while the
   rest stays on the old one. We don't have any of that. A "canary
   deploy" with no traffic splitter is just a deploy.

Adding pre-release tags or canary tags would smuggle a fourth
environment back in — which is exactly what we said NO to in the
"Branch model" decision (we picked GitFlow-lite, not three-stage).
If a future product needs canary-style rollout, that becomes its own
infrastructure RFC, not a tagging convention.

---

## Hotfix flow

When prod is broken and waiting for `develop` to catch up isn't an
option:

```
   main  ◀────────────── tag v1.2.4 ───────────────┐
    │                                              │
    └─▶ hotfix/iam-bug ─▶ PR to main ─▶ merge to main
    │                                              │
    │   (auto-deploys to prod, tags v1.2.4)        │
    │                                              │
    ▼                                              │
  develop ◀────── merge main forward into develop ─┘
                  (separate PR, fast-track review)
```

Steps:

1. `git checkout main && git pull && git checkout -b hotfix/<slug>`
2. Fix, push, open PR-to-`main`, get review, merge via PR.
3. Prod auto-deploys; tag bumps a patch version.
4. **Immediately** open a follow-up PR `chore: merge main into develop`
   so `develop` carries the fix forward. Conflicts (if any) are
   resolved in this PR, not in the hotfix.

Do not cherry-pick — the merge-forward is more reliable and surfaces
conflicts in a reviewable PR.

- **Orphaned commit after a merged PR.** A commit pushed to a feature branch *after* that branch's PR has already merged lands on **no merged ref** — it never reaches `main` (or `develop`), silently. (2026-06-22: a `verify-full` cert fix `7817b1f`, pushed onto an already-merged #28 branch, left prod cert-less; re-landed via a fresh PR #31 + promote #32.) **Always re-land late work via a new PR; never assume a `git push` to the old branch reaches a deploy ref.** When in doubt: `git branch --contains <sha>`.

---

## Stale branches

Automated by a GitHub Actions workflow in `.github/workflows/stale.yml`
(the canonical [`actions/stale`](https://github.com/actions/stale)
action). Same config in every repo.

| Age (no activity) | Action |
|---|---|
| **30 days** | Bot comments on the PR / issue: "This has been inactive for 30 days. It will be archived in 60 more days if there's no activity." Adds `stale` label. |
| **60 days** | No separate ping tier. `actions/stale` only does stale@30d + close@90d; the natural re-comment as the close window advances is the only "60-day" surface — there is no active author+assignee re-ping. |
| **90 days** | Bot closes the PR and archives the branch (label `stale-archived`). Re-open by removing the label or pushing a new commit. |

"Activity" counts: any commit, comment, review, or label change.
Drafts that explicitly say "blocked on X" can opt out with the
`do-not-stale` label.

### Don't let branches drift (author hygiene)

The bot above is a backstop for *inactive* PRs — not a substitute for
keeping your own branches current. Two rules:

- **Delete a branch at merge.** Auto-delete-on-merge is enabled (see
  [Auto-delete branches](#auto-delete-branches)) — don't leave merged
  branches lying around on the remote *or* locally.
- **Rebase long-lived branches onto `develop` regularly.** A branch that
  drifts far enough becomes *un-mergeable*: one that predates a structural
  change (a framework/dir migration like Nuxt's `app/` move, a schema
  cutover) will fight every relocated file, and by then its work is often
  already done elsewhere. If a branch is too stale to merge cleanly,
  **do not blind-merge it** — you'll resurrect the old structure. Rebase
  it, or cherry-pick only the still-relevant commits onto the current
  tree, checking each isn't already superseded.

Rule of thumb: a branch should merge or rebase within **days, not
months**. A real example that cost a cleanup: a feature branch left ~150
commits behind (across the `app/` migration) whose headline feature had
since been built in two other places — it had to be dropped, not merged.

---

## CODEOWNERS

Every repo MUST have a `.github/CODEOWNERS` file mapping paths to
people / teams. The example below is **illustrative only** — substitute
your repo's actual owner(s). It shows the path-mapping *patterns*, not a
prescribed roster; today most repos run a sole-gatekeeper model where a
single owner covers every path (see the org CODEOWNERS).

```
# Illustrative — replace @org-owner with your repo's real owner/team.
# Backend
backend/                      @org-owner
backend/app/auth/             @org-owner @org-security-team

# Frontend
frontend/                     @org-owner

# Docs + meta
docs/                         @org-owner
.github/                      @org-owner
plans/                        @org-owner
```

Effects:
- PRs touching a path auto-request review from the path's owner(s).
- "Require review from Code Owners" branch-protection setting becomes
  load-bearing on `main` (see above).
- Single-owner paths get exactly one reviewer (matches the 1-reviewer
  rule cleanly).

---

## Per-repo setup checklist

When bootstrapping a new repo (or auditing an existing one), copy this
checklist:

- [ ] `.github/workflows/gitleaks.yml` — secret-scan; required check `gitleaks` (**every repo**, including docs-only)
- [ ] `.github/workflows/ci.yml` — runs the repo's lint, unit-test and API-contract checks; **name the required contexts to match your CI** (illustratively `lint-frontend`/`lint-backend`/`test-frontend`/`test-backend`/`verify-api-contract` for full-stack) _(code repos only; docs-only repos require `gitleaks` + stale only)_
- [ ] `.github/workflows/ci-cd.yml` — push-to-develop → dev server; push-to-main → prod _(code repos only; docs-only repos require `gitleaks` + stale only)_
- [ ] `.github/workflows/stale.yml` — stale@30d + close@90d cleanup
- [ ] `.github/CODEOWNERS` — at minimum, one owner per top-level dir
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` — Why / What / Test plan / Rollout
- [ ] `.pre-commit-config.yaml` — case-collision (`check-case-conflict`) + gitleaks + format + `conventional-pre-commit` (commit-msg) + branch-name
- [ ] Branch protection on `main` — see [§"main — today"](#main--today)
- [ ] Branch protection on `develop` — see [§"develop — today"](#develop--today)
- [ ] Repo settings → "Automatically delete head branches" = on
- [ ] Repo settings → merge-commit-only merge button (PR title as merge-commit message)
- [ ] `README.md` cross-links this doc

A future bootstrap script in `.github/scripts/` will set these
automatically; until then, the checklist is the source of truth.

---

## Open / future items

These are deferred decisions, tracked here so they don't get lost:

- **Build-once-promote migration.** Every active repo's `ci-cd.yml`
  today rebuilds the image per environment (non-conforming with
  §"Build-once-promote"). Per-repo migration PRs land as small,
  focused changes (~half a day each). Tracker:
  `plans/build-once-promote-migration.md`.
- **Pin deploys by image digest, not tag.** Once the build-once
  pipeline is in place, the next refinement is to have
  `docker-compose.deploy.yml` reference images by `sha256` digest
  rather than by tag. Tags are mutable (someone can `docker tag` a
  new image to an old name); digests can't lie. The CI workflow
  captures the digest at build time and substitutes it into the
  compose at deploy time.
- **Playwright e2e as a required check.** Today `if: false` in CI.
  Flip when the suites are flake-free for a 2-week stretch.
- **Branch protection — strict mode** (signed commits, no admin
  bypass). Lands when key-management is in place.
- **Release-as-needed** flag on the auto-bump workflow — for the rare
  case where you want a `chore`-only PR to bump a minor (e.g., a
  dependency major bump that's effectively a minor for our app).
- **Pre-deploy migration gate** — once Alembic migrations get larger,
  add a step that runs `alembic check` against the deploy DB before
  the container restart. Cross-link the `nucleus-db` plan when that
  lands.
- **SBOM generation (syft).** Software Bill of Materials per image,
  attached to the GitHub Release as an artifact. Cheap (~30s in CI,
  no signing infrastructure required) and gives a real
  vulnerability-response capability — "am I exposed to CVE-X?"
  answered by querying the SBOM, no rebuild needed. **Deliberately
  not adding image signing (cosign) at this scale:** internal-only
  deploys, on-prem registry we control, no external trust requirement.
  Revisit signing if the Pharos portfolio (RFC 0004) ever ships images
  to an external party.

---

## Why this doc lives here

`ENGINEERING_STANDARDS.md` is the broad sweep — "we use Nuxt 4, ruff,
shadcn-vue, Conventional Commits, branch protection on main." It's the
elevator pitch.

This doc is the *operational manual*: every per-setting choice, every
trigger, every required check, every escalation path. Where
ENGINEERING_STANDARDS says "branch protection enabled," this doc
specifies which rules and why. Where it says "CI/CD via GitHub
Actions," this doc lists the required checks and the deploy triggers.

The two are designed to be read together but maintained
independently: STANDARDS rarely changes; this doc evolves as policy
tightens.

---

_Last revised: 2026-05. Decisions captured in this doc were ratified
by the team via a structured-questions session — see commit message
for the audit trail._
