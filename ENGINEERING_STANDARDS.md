# 🏗️ Engineering Standards — Interval-Col

This document defines the official engineering standards for all primary projects under the Interval-Col GitHub organization, especially as adopted by and standardized in [biuman-reports](https://github.com/Interval-Col/biuman-reports), [lab-qc](https://github.com/Interval-Col/lab-qc), and [finance-lch](https://github.com/Interval-Col/finance-lch) (a primary adopter).

> **Companion guide (recommendation, not enforced):** [Agent Chat Hygiene](AGENT-CHAT-HYGIENE.md) · [español](AGENT-CHAT-HYGIENE.es.md) — keeping Claude Code sessions cheap and durable: one chat per task, save durable knowledge to the repo/memory, and when to `/compact` / `/clear` / delete.

---

## 🚀 Stack & Architecture

### **Backend (Python)**
- FastAPI
- Pydantic v2
- SQLAlchemy
- pytest for testing
- Directory structure:
  ```
  backend/
    app/
      core/
      features/
      main.py
      ...
    tests/
    scripts/
    Dockerfile
    pyproject.toml (preferred) or requirements.txt
  ```
- Pin Python version ≥ 3.11
- `.env.example` with all required config variables
- Apps on the shared `nucleus_db` cluster follow the **[DB tenant contract](db-tenant-contract.md)** (RFC 0015): migrate-as-deploy-step, no startup DDL, TLS `verify-full`, URL-encoded DSN, `/health` + `/ready` — machine-checked by the reusable `db-tenant-check` workflow.
- Apps with a self-serve roles/capabilities module follow the **[auth contract](auth-contract.md)** (RFC 0016): local authz (IAM = identity only), the `require_capability` gate, the seven `/auth/admin/*` endpoints, deploy-step seeding (never on startup), a runtime role registry, and FE↔BE capability sync — machine-checked by the reusable `auth-contract-check` workflow.

### **Frontend (Nuxt 4, Vue 3, TypeScript)**
- Nuxt 4 as framework — **SSR by default**. Opt a route out with
  **`routeRules`**, not `definePageMeta`:

  ```ts
  routeRules: { '/etiquetas': { ssr: false } }
  ```

  ⚠️ **`definePageMeta({ ssr: false })` does nothing in Nuxt 4** — `ssr` is not
  a `definePageMeta` key. A page "opted out" that way still renders on the
  server. `routeRules` is the Nuxt-native per-route mechanism and the one both
  live apps use.

  Opt out when the route is auth-gated **and** loads its data client-side, so
  SSR would only render an empty skeleton and add hydration risk. A whole app
  may render client-side when it is internal-only with no SEO surface —
  finance-lch does exactly that (`'/**': { ssr: false }`), deliberately.
  Reference implementations: `finance-lch/frontend/nuxt.config.ts` (whole app)
  and `pharos-lis/lab-qc/frontend/nuxt.config.ts` (single route).
- Vue 3, Vite, Pinia, Tailwind v4, TypeScript
- Pin Node version in `package.json` and/or `.nvmrc`
- `.env.example` in `frontend/`
- Directory structure:
  ```
  frontend/
    ...
    Dockerfile
    ...
  ```

---

## 📝 Branching, Commits, and CI/CD

| Practice           | Standard                                                            |
|--------------------|---------------------------------------------------------------------|
| Branch model       | **GitFlow-lite**: `main` ← `develop` ← `<type>/<slug>`              |
| Default Branch     | `main` (PR required, 1 reviewer, green CI, merge-commit)            |
| Integration Branch | `develop` (direct push allowed; CI still required)                  |
| Feature Branches   | `<type>/<short-kebab-slug>` — types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `hotfix`, `ci` |
| Commit & PR title  | [Conventional Commits](https://www.conventionalcommits.org/) — enforced on **both** |
| Merge mode         | **Merge commit** everywhere; auto-delete merged branches            |
| CI/CD              | GitHub Actions in `.github/workflows/`; push-to-`develop` deploys dev server, push-to-`main` deploys prod (the PR review IS the deploy approval) |
| Releases           | Semver tag (`v1.2.3`) + GitHub Release per prod deploy, auto-drafted notes |
| Hotfix             | `hotfix/*` off `main` → PR to `main` → merge `main` forward into `develop` |

> **Full operational policy**, including branch-protection settings,
> required CI checks, the hook set, CODEOWNERS, stale-branch
> automation, three-environment topology, and per-repo bootstrap
> checklist: see **[`BRANCHING-AND-DEPLOY.md`](BRANCHING-AND-DEPLOY.md)**.
> That doc is the source of truth for the per-setting choices; this
> table is the elevator pitch.

> **Solo-maintainer note.** The org standard for a single Code Owner is: required
> approvals **0** — green CI, not a human approval, is what gates a merge — with
> `enforce_admins` **on** so the rules bind admins too. Approvals go to 1 when a
> second reviewer joins. Detail:
> [`BRANCHING-AND-DEPLOY.md`](BRANCHING-AND-DEPLOY.md) → `main` branch protection.
>
> ⚠️ **That is the standard, not a guarantee about a given repo.** Settings drift,
> and several repos do not match it today. Before assuming how a merge is gated,
> read the repo:
> `gh api repos/Interval-Col/<repo>/branches/<branch>/protection`.

### 🧬 No orphan code — anything that runs is in a repo

| Rule | Standard |
|---|---|
| **A branch is a backup, not a commitment** | Pushing a branch **never** requires an open decision to be resolved first. A pending decision gates **merging**, **deploying**, and **creating a new repo** — it never gates **versioning**. If you are waiting on a decision, push a `wip/<slug>` branch and keep working. |
| **Arrival = repo + runtime** | The mirror of RFC 0009's *"Retirement = repo + runtime"*. Nothing runs in the estate whose source is not in a repo: a service arriving needs **both** surfaces, exactly as a service retiring needs both removed. |
| **No authoring on a host** | A server is where code **runs**, never where it is **written**. The moment a task turns from *configuring a tool* into *authoring a file*, the file needs a repo — even if it is "temporary", even if it is one file. |
| **Interim home** | No repo decided yet? The code goes to a `wip/` branch of the **repo that will consume it**, or of the closest owning repo. A folder can be extracted into its own repo later **with history** (`git subtree split`) — the org has done it (`pharos-llm-proxy` ← `finance-lch`). Starting versioned is never the expensive choice. |
| **Provenance is the test** | A running container whose image was built **on the host** rather than pulled from the org registry is orphan code by definition. Image provenance, not good intentions, is what makes this auditable. |

> **Why this is a standard and not advice.** The failure mode is silent and it
> compounds. A gated decision stalls the repo; the work continues because the
> work is urgent; the artefact grows one reasonable file at a time; and **no CI
> check can ever see it**, because every gate in this org — secret scan, lint,
> tenant check, code owners — runs on pull requests. Code that never reached a PR
> is invisible **by construction**, so the only copy of a load-bearing service can
> sit on one unbacked disk with nothing anywhere reporting a problem. The stalled
> tasks *are* the alarm, and a stalled task looks exactly like orderly progress.

> **Tenant identity travels with the repo.** One repo = one nucleus-db tenant:
> the manifest in [`db-tenant-contract.md`](db-tenant-contract.md) takes a single
> `app:` and a single set of owned `schemas:`, applied by that app's one migrate
> one-shot under that app's role. So **"does this need its own repo?" and "does
> this own its own schema and role?" are the same question asked twice.** A
> component that must own a schema separately — its own owner role, its own
> privilege split — is its own tenant, and therefore its own repo. Deciding the
> schema first and the repo later, or the reverse, is how the two answers end up
> contradicting each other.

---

## 🤖 Tooling, Lint, Format

### Python Backend

- **Linter:** [Ruff](https://beta.ruff.rs/docs/)
- **Formatter:** [Black](https://black.readthedocs.io/en/stable/)
- **Test runner:** pytest
- **Type checks:** pyright (required in CI)

### Frontend

- **Linter:** ESLint
- **Formatter:** Prettier
- **Test runner:** Vitest or Jest
- **Style:** Tailwind v4

#### Design-system CI gates (Nuxt + shadcn-vue projects)

The org package manager is **pnpm**. In addition to ESLint, every
Nuxt + shadcn-vue project (srcDir `app/`) chains four design-system
gates into `pnpm lint-check`. Each gate enforces a rule that ESLint
can't catch and that has historically drifted across PRs. The
governing rule, stated once here: **semantic tokens over raw
color/markup, and scoped `<style>` only in `app/components/` — never
in `app/pages/` or `app/layouts/`** (those use Tailwind utilities and
shadcn-vue primitives). The semantic-token source of truth is
[`brands/pharos_brand/registry/tokens.css`](brands/pharos_brand/registry/tokens.css).

| Gate | What it forbids | Where to add it |
|---|---|---|
| `check-no-scoped-pages.mjs` | `<style scoped>` blocks in `app/pages/**` and `app/layouts/**` (Tailwind utilities required; scoped `<style>` allowed only in `app/components/**`) | `frontend/scripts/` |
| `check-no-raw-html.mjs` | raw `<button>`, `<table>`, `<input>`, `<select>`, `<textarea>` in pages/layouts (shadcn-vue primitives required) | `frontend/scripts/` |
| `check-no-hex-colors.mjs` | hex literals (`#abc`, `#abcdef`) outside `app/assets/css/` (semantic tokens required) | `frontend/scripts/` |
| `check-no-palette-colors.mjs` | Tailwind palette utilities (`text-green-600`, `bg-amber-100`, …) outside `app/components/ui/` (semantic tokens required) | `frontend/scripts/` |

**Wiring.** In `frontend/package.json`, chain all four:

```json
{
  "scripts": {
    "lint-check": "eslint . --max-warnings 0 && node scripts/check-no-scoped-pages.mjs && node scripts/check-no-raw-html.mjs && node scripts/check-no-hex-colors.mjs && node scripts/check-no-palette-colors.mjs"
  }
}
```

The chained `&&` is intentional: a single failure blocks the merge,
and each gate's output appears in CI logs without being short-
circuited. Ordering matters — ESLint runs first because it has the
broadest false-positive surface; the design-system gates run after
so their output isn't masked by a separate ESLint failure (a real
incident in lab-qc Phase 5).

**Reference implementation.** Copy verbatim from
[`lab-qc/frontend/scripts/`](https://github.com/Interval-Col/lab-qc/tree/main/frontend/scripts).
Keep the file headers — they document the rule, the allowlist
philosophy, and the migration mapping table.

**Allowlists are intentional.** Each gate exposes a small, in-file
ALLOWLIST that grandfathers pre-shadcn pages and documented exceptions
(reka-ui combobox slots, `<input type="file">`). Each allowlist entry
must reference the migration plan (typically
`lab-qc/docs/HARMONIZATION.md`) that will retire it. New violations
go through code review — they cannot be added to the allowlist
without explicit reviewer attention because the file is reviewed.

**Escape-hatch comments.**
- `// lint-allow-hex` — exempts the line from `check-no-hex-colors`
- `// lint-allow-palette` — exempts the line AND the following non-
  blank lines (block scope) from `check-no-palette-colors`

Use sparingly. Both serve cases like the audit-log action-color map
where the design genuinely needs raw palette differentiation across
more categories than the semantic token set enumerates.

---

## 🔠 Cross-platform path safety

Mac developers + Linux CI is a mixed-FS environment. macOS APFS is
case-insensitive by default; Git is case-sensitive. **Never commit
two files whose paths differ only in case** (e.g. `Order.ts` and
`order.ts` in the same folder). On Linux they coexist; on macOS the
filesystem can hold only one of the pair, leaving the other
permanently "modified" in `git status` because the disk content can
never match both blobs simultaneously. Recovery from a Mac is
expensive (see the biuman-lis runbook linked below); prevention is
cheap.

### Required in every repo

1. **Pre-commit hook** rejecting any commit that introduces a
   case-collision pair — the enforcement everywhere (including this
   docs-only repo) is the upstream
   [`pre-commit-hooks`](https://github.com/pre-commit/pre-commit-hooks)
   `check-case-conflict` hook. In **code repos** this is additionally
   backed by a case-collision **CI check**; reference implementation:
   [`biuman-lis/scripts/check-case-collisions.sh`](https://github.com/Interval-Col/biuman-lis/blob/main/scripts/check-case-collisions.sh).
   The detection is a one-liner:
   ```bash
   git ls-tree -r HEAD | awk '{print $4}' \
     | awk '{print tolower($0), $0}' | sort \
     | awk '{ if ($1==prev) { print "case-collision:", lastpath, "vs", $2; bad=1 } prev=$1; lastpath=$2 } END { exit bad }'
   ```
2. **Repo-level convention**: pick one casing style per folder
   (`PascalCase.ts` for components, `camelCase.ts` for utilities,
   `kebab-case.vue` for pages — whatever the repo settles on) and
   keep it consistent. Mixed casing within a folder is the
   precondition for collisions.

### If a collision lands on `main` anyway

Fix from a case-sensitive system (Linux container, WSL, or a
case-sensitive APFS volume on Mac) — `git rm --cached <dead-path>`
on the dead casing, commit, push. Trying to fix it from a vanilla
Mac requires the index-mirror dance documented in the biuman-lis
[`CONTRIBUTING.md`](https://github.com/Interval-Col/biuman-lis/blob/main/CONTRIBUTING.md)
case-collision runbook because `git stash` and `git reset --hard`
oscillate the dirty status without ever clearing it.

---

## 🛡️ Security & Config

- No secrets/config in source; use `.env.example` for all config.
- All `.env` files listed in `.gitignore`.
- Python/node versions pinned.
- Separate `Dockerfile` for BE and FE.
- Root-level `docker-compose.yml` or `compose.yaml`.

### 🗝️ Secrets & vaults

**Bitwarden is the org vault.** All shared infrastructure credentials
(DB passwords, deploy-user SSH keys, host fingerprints, third-party
API keys used at deploy time) live in Bitwarden. 1Password is **not**
used at the org level — any older docs that mention it are historical.

**Collection layout — by environment, not by app:**

| Collection | Holds |
|---|---|
| `staging` | every service's staging credentials (e.g. `nucleus-db/nucleus_admin`, `nucleus-db/finance_user`) |
| `prod` | every service's prod credentials, same item-naming convention |
| `dev` | shared dev-only secrets (rare — most dev creds are per-developer) |

**Why per-environment, not per-app:** lets us tighten prod-only access
to a smaller subset of people without restructuring the vault, and
every item's env is implicit in its parent collection so you cannot
accidentally save a prod password under a staging name.

**Item naming inside a collection:** `<service>/<role>` — e.g.
`nucleus-db/nucleus_admin`, `nucleus-db/finance_user`,
`staging-vm/deploy`. Match the role name used in the DB / system,
not a friendly label.

**Access:** `staging` and `prod` vault access is restricted to
@gczuluaga only (sole, as of 2026-06-15). Other devs request a
credential through the caretaker; they don't
get blanket vault access. Document any access change in the relevant
RFC's Decisions log.

**GitHub Actions secrets are downstream of Bitwarden.** Bitwarden is
the source of truth; GH secrets are *copies* needed at deploy time.
Prefer **org-level GitHub secrets** (Interval-Col org settings → Secrets
and variables → Actions → New organization secret) so the rotation
story is one place per credential. Per-repo secrets are acceptable
only when the secret is genuinely repo-scoped. When a credential
rotates: update Bitwarden first, then the org-level secret, then any
repo-level overrides.

**The shared CI/CD credentials are org-level — repos *reference*, never recreate.**
`AWS_OIDC_ROLE_ARN`, `AWS_REGION`, `AWS_REGISTRY`, the `DEV_*`/`PROD_*` host triples
(`*_HOST` / `*_USER` / `*_KEY`), and `BUILDER_*` are **org-level GitHub secrets inherited
by every repo** — the `AWS_OIDC_ROLE_ARN` role trusts `repo:Interval-Col/*` with `repository/*`
ECR perms, so a migrated repo needs **no new IAM**. Its workflow simply `secrets.*`-references
them; **do not create per-repo copies.** Only **app-specific, per-environment** values (service
ports, GraphQL/SSO endpoints, licenses, SMB/host paths) are set per-repo, scoped to the repo's
GitHub Environments. ⚠️ Environment **required-reviewers are *not* available on our plan** for
private repos (`422`) — gate prod deploys with an in-workflow flag (e.g. `<APP>_PROD_DEPLOY_ENABLED`,
default off), not environment protection. Seeding a migrated repo's per-env values: see
`Interval-Col/operations` → `runbooks/ci-cd-secrets-seeding.md` (Docker → Bitwarden → GitHub, no value echoed).

### SSO auth debugging — "User not found" can mean LOCKED

The SSO (`sso-backend`, `POST /auth/v1/session/login`) returns a misleading `"User not found"` (status flips 404/422) when an account is **rate-limited / locked** by a login burst (~3 failed logins → exponential ~5 min × attempt) — *not only* for a genuinely-unknown user, and the *same* error also covers a wrong password. Rules for any service authing to this SSO:

1. On a login `404` / "User not found", **suspect lockout first** — prove the creds with a single browser/one-shot login (a `200` resets the counter) **before** changing any secret.
2. **Never bulk-retry logins** — manual loops trip *and* sustain the lock (shared `failed_login_attempts`).
3. **Cache the token and pace the caller** — a cached token + scheduler cadence is the safe steady state.
4. SSO clients **SHOULD ship a login circuit-breaker** — negative-cache failed logins + exponential backoff past the lock window. Reference implementation: `cobol-migration/services/etl/auth.py`.

See `operations/incidents/2026-06-sso-lockout-user-not-found.md`.

---

## 🔬 Marking a view as «en verificación» (Pháros apps)

A Pháros view that is **deployed but not yet released** under `PROT-SW-001` looks
exactly like a released one unless it is marked. `PROT-SW-001` §6 is explicit that such
a functionality «puede estar **desplegada y en uso en paralelo**, pero **no** se retira
su predecesora» — the mark is that state, on screen: a banner, a subtle canvas wash, and
a dot/chip in the nav and breadcrumb so it is visible *before* entering the view.

**This applies to every Pháros app**, not just the one it shipped in.

### To mark a new view

Hand this to whoever (or whatever) does the work — it is complete as written:

```
Marca la vista <RUTA> como «en verificación» (PROT-SW-001).
Responsable: <NOMBRE COMPLETO> · <CARGO>. Revisar antes de: <YYYY-MM-DD>.

Dos pasos:
1. Agrega la entrada en app/verification.manifest.ts — el responsable va EN LÍNEA,
   nunca factorizado a una constante compartida.
2. Envuelve la vista en su página, SIN re-indentar el cuerpo:
   <ViewVerification :v="verificationFor($route.path)">…</ViewVerification>

Verifica con: pnpm lint-check
```

Removing the mark is the same two files in reverse: delete the manifest entry **and**
the wrapper. The gate requires both, so a `grep` always tells the truth about which
views are marked.

### The three inputs an agent must never invent

| Input | Why it is a human's to give |
|---|---|
| **Which view** | A domain call — Quality and Medical Direction, not engineering. |
| **`responsable`** | Full name + role, **never a `@handle`** (`SOP-000` §4). It is who the person at the bench would actually ask. |
| **`revisarAntes`** | Quality's date. Past due **fails the build**, on purpose. |

The `check-view-verification.mjs` gate catches all three if they are wrong — but the
point is not to get there. And note the asymmetry: **`liberada` renders nothing at all.**
The absence of the mark *is* the released state; a green "verificado" seal would be an
attestation nobody removes once it stops being true.

### First time in an app

One-off, then never again:

```bash
scripts/sync-pharos-registry.sh --add components/ViewVerification.vue \
  --add components/ViewVerificationMark.vue <app-fe-dir> [repo-root]
```

The vocabulary, the manifest bridge and the manifest **seed** follow automatically as
declared companions. Two things the sync deliberately cannot do for you:

- **Mount `<ViewVerificationMark>` in `app/layouts/default.vue`** — app-owned scaffold
  the sync never touches. Without it there is a banner *inside* the view but no warning
  *before* entering. Check 8 of the gate fails until you do.
- **Add `node scripts/check-view-verification.mjs`** to the `lint-check` script.

⚠️ `app/verification.manifest.ts` is a **seed, not a contract**: it carries
`pharos-registry:keep`, so it lands once and is yours from then on — a re-sync never
overwrites what Quality declared, and Lock 3 never flags your edits as drift.

Detail — the states, the colour registers, the eight checks:
[`brands/pharos_brand/registry/README.md`](brands/pharos_brand/registry/README.md)
§ *Vista en verificación*.

## 🧪 Two threads: engineering vs. laboratory Quality verification

A clinical functionality under `PROT-SW-001` is tracked in **two issues, never one**
(German, 2026-08-23 — after the sample-collection port mixed both in `pharos-lis#357`
and the expediente became unreadable for Quality):

| Thread | Who reads it | What goes in | Example |
|---|---|---|---|
| **Engineering** | the dev team | plan, PRs, deploys, defects, diagnostics, «registro de ingeniería» notes | `pharos-lis#357`, `#91` |
| **Verification** («hilo único de verificación») | Coordinación de Calidad + Dirección Médica | the `FOR-SW-001` expediente, the soak proposal (C.1/C.2), Quality's verdicts per dimension, signatures | `pharos-lis#397`, `#302` |

Rules:

- **Open the verification thread only when engineering is *observable*** — the screens
  reachable in prod, the version anchored, the expediente pre-filled by Development.
  Before that, nothing engineering writes is evidence; say so in each entry
  («registro de ingeniería, no evidencia de PROT-SW-001»).
- **The verification thread is written for Quality, not for engineers**: plain Spanish,
  evidence by permanent links into the engineering thread and CI, zero jargon a bench
  technologist would not use. Its opening comment tells Quality exactly what it must do
  and nothing else (read, approve coverage, verdicts, authorise the real-data case).
- **Findings cross in one direction.** A finding raised in verification that needs code
  opens (or links) an item in the engineering thread; the verification thread records
  only the finding and its disposition. The engineering thread never hosts verdicts.
- **Title convention:** `<Funcionalidad> — hilo único de verificación (Calidad + Dirección)`,
  label `documentation`, same repo as the engineering thread.
- **Zero patient data in either thread.** The verification thread additionally carries no
  case identifiers (bitácoras by category / internal consecutive; the mapping stays in
  Quality's custody — `ANEXO-PROT-SW-001-01` R1/R8).
- What `lch-kb` holds stays unchanged: protocol and blank templates only. A filled
  expediente is a *record* and never lands there.

## 📄 Project Documentation

- Root `README.md` must document:
  - Architecture overview
  - Setup (BE & FE)
  - How to run tests
  - Local development with Docker
  - Deployment instructions

- Refer to this `ENGINEERING_STANDARDS.md` for any refactor, migration, or new major feature.

### 📋 Plan craft

Execution plans for delivery work (the `plans/*.md` files each repo
carries) follow a shared **plan-craft methodology**, calibrated to a
junior, Spanish-native, AI-agent-assisted dev team. It standardises:

- **Bilingual layout** — English body with a Spanish `Resumen` per
  section and inline `(ES: …)` glosses on the high-cost-of-misread
  parts (decisions, acceptance criteria, checkpoint questions).
- **Marker vocabulary** — `💡 Heuristic`, `🛑 HUMAN DECISION`,
  `✅ Done-when`, `🚦 Checkpoint`, each with strict semantics.
- **Working rules block** that every plan carries verbatim: commit +
  push per slice; Conventional Commits with required scope (see
  [`lab-qc/docs/STANDARDS.md`](https://github.com/Interval-Col/lab-qc/blob/main/docs/STANDARDS.md));
  review-the-frontend-in-the-browser; AI-tool guidance; the
  bypass-honesty note; and the **auto-mode-is-slice-bounded** rule
  (auto mode is allowed within one slice, the agent stops at every
  slice boundary and at every 🚦 Checkpoint to surface Done-when
  status and wait for human acknowledgement — auto mode is never
  "execute the whole plan unattended").
- **Non-condescending tone** — gaps are framed as the *plan's* fault,
  not the reader's; seniority is never mentioned.

Authoritative artefacts (canonical sources of truth):

- **Agent prompt** — [`agents/plan-craft.agent.md`](agents/plan-craft.agent.md).
  System prompt for an AI agent helping a lead author or rebuild a plan
  in this style. Includes the audience model, required structure,
  tone "do / never," and a re-baselining recipe for plans the team has
  already partly implemented.
- **Template** — [`templates/plan-template.md`](templates/plan-template.md).
  Copy into the target repo's `plans/` directory and fill in the
  placeholders; canonical blocks are verbatim-ready.

Reference plans worth reading as exemplars: `admission-patient/plans/`,
`commercial-lch/plans/mvp-quote-generation-plan.md`.

---

## 🧑‍💻 Review & Collaboration

- Branch protection on `main` and `develop` — see
  [`BRANCHING-AND-DEPLOY.md` §"Branch protection"](BRANCHING-AND-DEPLOY.md#branch-protection)
  for the exact ruleset (required reviewers, required status checks,
  force-push policy, planned escalation to signed commits).
- Use PR and Issue templates from `.github/`.
- CODEOWNERS required per repo — see
  [`BRANCHING-AND-DEPLOY.md` §"CODEOWNERS"](BRANCHING-AND-DEPLOY.md#codeowners).
- All teams/contributors must follow the standards here for all major projects.

---

## Example Project Checklist

- [ ] BE Python: FastAPI, Ruff, Black, pytest, Pydantic v2, `.env.example`, `Dockerfile`
- [ ] FE: Nuxt 4, Vue 3, TypeScript, Pinia, Tailwind v4, ESLint, Prettier, `.env.example`, `Dockerfile`
- [ ] `README.md` present and cross-links the org-wide `ENGINEERING_STANDARDS.md` (single doc, not copied per repo)
- [ ] `.github/` directory with workflows and templates
- [ ] **CI must run all tests, lint, and builds**
- [ ] Branch protection enabled on `main`
- [ ] Case-collision check installed (pre-commit `check-case-conflict` everywhere; CI step in code repos) — see "Cross-platform path safety"
- [ ] Secret scanning (gitleaks) installed — pre-commit hook **and** required CI check named `gitleaks` (every repo, incl. docs-only) — see [`BRANCHING-AND-DEPLOY.md` §"Hooks"](BRANCHING-AND-DEPLOY.md#hooks)

---

_This standards file is the source of truth for new code, refactors, upgrades, and onboarding._
