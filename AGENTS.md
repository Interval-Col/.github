# .github — what an agent needs to know about this repo

## Why it exists

The org-wide home for **what every Interval-Col repo has to comply with**: engineering
standards (`ENGINEERING_STANDARDS.md`, `BRANCHING-AND-DEPLOY.md`), the knowledge hub
(`KNOWLEDGE-MANAGEMENT.md`), the shared contracts (`db-tenant-contract.md`,
`auth-contract.md`, `chat-contract.md`) and the reusable workflows and scripts that enforce
them. It also holds the Pháros design-system registry (`brands/pharos_brand/registry/`),
the shared agent definitions (`agents/`) and the doc templates (`templates/`). Index:
`README.md`.

## 🔴 This repo is PUBLIC

It is the **only public repo in the org**, indexed by search engines and readable without
credentials. Anything you write here is published, including history: rewriting history
does not un-publish a commit that a pull-request ref still points to. Before you write,
check the public-surface column of the org's classification table (`SECURITY.md` in the
private operations repo). In short:

- **Never:** internal IP addresses or CIDR ranges, a hostname paired with its address,
  `<user>@<host>` pairs, origin addresses behind a CDN/WAF/VIP, credentials of any kind,
  or **any unremediated weakness** (an unpatched version, a missing control, a known
  misconfiguration).
- **Never:** real people's names in examples, and never patient data. Example data must
  look obviously synthetic (a realistic-looking ID number forces a human ruling to clear
  it).
- **Split the write.** The generic, forward-looking rule goes here. The incident, the
  affected systems, the dates and the PR numbers stay in a private repo (`operations`,
  `rfcs`). No "this happened to us" prose.
- No licensed font binaries or brand masters (`no-font-binaries` blocks fonts). Those
  live in the private `brand-assets` repo. Public contact facts (`contact/*.yml`) do
  belong here, on purpose.

## Trunk and branches

- Trunk: **`main`**, with no `develop`. Every change goes through a PR. `gitleaks` is the
  required check.
- Always merge with a merge commit (`--merge`), never `--squash`. The org disables squash
  and rebase merges (`BRANCHING-AND-DEPLOY.md` §Merge mode).
- Branches are `<type>/<kebab-slug>` (`scripts/check-branch-name.sh`, pre-push).
  Conventional Commits with a scope.
- `CODEOWNERS` routes every path to the harness owners.

## Reglas que obligan a este repo

Una línea por cada RFC aceptada que nombra este repo en `target-repos` (RFC 0039 D4); el detalle y sus excepciones están en la RFC, en `Interval-Col/rfcs`.

- RFC 0004 — Nombra las apps «Pháros <Nombre>» en UI y docs, pero `pharos-*` en minúscula sin tilde en código y repos; no crees apps aparte para Caja, CRM ni QC; en apps multi-tenant toda fila lleva `tenant_id`.
- RFC 0005 — Tu app es dueña de su schema y sus migraciones, pero todo PR de migración lo revisa nucleus-db (CODEOWNERS): PK UUID, `tenant_id`, dinero `NUMERIC(18,2)`, sin DDL ni FK entre schemas.
- RFC 0006 — Todo dato que entre desde COBOL pasa por la ETL de `cobol-migration/services/etl/` y actualiza su fila del coverage tracker (§7) en el mismo PR; un dominio no corta sin el protocolo de corte (§4).
- RFC 0008 — Usa los tokens semánticos y las 4 familias tipográficas compartidas (sin fuentes por app), trae componentes del registry por copy-in (nunca paquete npm ni `cp`), un solo `<Icon>` (Lucide, con Material Symbols Outlined como único fallback gobernado) y pasa los 4 design gates.
- RFC 0009 — Antes de empujar un repo migrado corre `gitleaks` sobre el mirror y quita PHI/secretos con `git-filter-repo`; un repo retirado solo se marca hecho con repo Y runtime (proxy, contenedores, ECR, SSO, DNS, secretos) dispuestos.
- RFC 0010 — Deja el `status:` de cada plan en un solo valor del enum que valida `plan-lint` (`scripts/plan_lint.py`), sin glosa en prosa.
- RFC 0011 — Un plan solo si es un outcome con contexto multi-fase; una fase es `## Phase N` dentro del plan (no otro plan), la tarea suelta es un issue con `parent` al epic, y lo terminado se archiva en `plans/archive/`.
- RFC 0012 — Ningún job de CI guarda una credencial fija del SSO: el registro de permisos lo dispara una persona con su propio token.
- RFC 0013 — El navegador solo habla con tu propio backend (same-origin, `/<app>/api`) y con la sesión del SSO; users-api, cobolql y demás los consume tu backend con service account; el `apiBase` central va relativo.
- RFC 0014 — Toda superficie web para pacientes o público va en `public-web` (monorepo pnpm, Nuxt layers) con la fundación Pháros por copy-in y la piel de clínica en `packages/brands/*`; apps con nombre `lch-*`, nunca «Portal Pacientes».
- RFC 0015 — Cumple `db-tenant-contract.md` (`.db-tenant.yml`, check `db-tenant-check`): migra como paso de deploy, jamás DDL/DML al arrancar, TLS `verify-full` en prod, DSN codificado, y, en cambios rompientes, expand/contract con `lock_timeout` (Fase 5, todavía por ratificar).
- RFC 0016 — Declara `.auth-contract.yml` y pasa `auth-contract-check`: `require_capability` contra el catálogo, los 7 endpoints `/auth/admin/*`, seed de roles como paso de deploy (nunca al arrancar) y autorización local, sin `is_authorized`.
- RFC 0017 — Toda llamada a un LLM va por `pharos-llm-proxy` (sin SDK ni llave de proveedor en tu app); tu chat cumple `chat-contract.md` con `.chat-contract.yml` y usa el widget `PharosHelpChat` del registry.
- RFC 0023 — La política de divulgación del Decreto 780 se escribe una sola vez en `lch-results/backend/app/disclosure/`, protegida por CODEOWNERS: nunca la copies ni agregues métodos de escritura a `ResultsProvider`.
- RFC 0029 — La conformidad se mide, no se declara: un manifest nunca hace pasar un check, un gate sin cablear no cuenta, todo aviso lleva `enforce_by` y todo perfil rebajado `review_by`.
- RFC 0030 — Firma el consentimiento informado solo con el widget `ConsentSignature` del registry contra `api-document-signature`; no reimplementes la pantalla ni llames `POST /pdf_form/fill` por tu cuenta, y pedir la firma nunca tumba el acto clínico.
- RFC 0039 — Mantén `AGENTS.md` (≤200 líneas) como fuente canónica y `CLAUDE.md` como shim `@AGENTS.md`; la sección «Reglas que obligan a este repo» lleva una línea por RFC aceptada, y cada regla de código trae su `scripts/check-rfc-<NNNN>-<qué>`.

## Run and test

```bash
pre-commit run --all-files                         # hygiene, gitleaks, plan-lint
for t in scripts/test_*.py; do python3 "$t"; done  # the script tests
python3 -m unittest discover -s tests/corpus -v    # corpus registry tests (also run by corpus-check)
python3 scripts/corpus_registry.py validate
```

Checks on this repo's own PRs: `gitleaks`, `plan-lint`, `corpus-check`, `issue-link`,
`retro-gate`, `no-font-binaries`, and `pharos-registry-lint` when
`brands/pharos_brand/registry/**` changes.

## Data boundaries

- No database and no PHI, ever (see above). Contracts describe structure only.
- The registry is **consumed by copy**, not imported. Apps sync it with
  `scripts/sync-pharos-registry.sh`, and their own CI checks that it is fresh.

## Deploy

Nothing is deployed from here, but **a merge to `main` is a release to the whole org**:

- **Reusable workflows** (`.github/workflows/*.yml` with `workflow_call`: `changes`,
  `db-tenant-check`, `auth-contract-check`, `plans-check`, `kb-publish`, …) are called as
  `Interval-Col/.github/.github/workflows/<name>.yml@main`, and their scripts are read from
  `main`. A change reaches every caller's next run, with no promotion step.
- **The registry** (`brands/pharos_brand/registry/**`): a push to `main` triggers
  `pharos-registry-resync`, which opens one re-sync PR per consuming app within seconds.
  Until each one merges, that app's freshness gate is red.

## Traps

- 🪤 **A reusable workflow called by several repos declares no `permissions:` block.** A
  called workflow can only *downgrade* the caller's token: if it asks for more than one
  caller grants, that caller's run fails to start. If it asks for less than it needs, the
  calls 403 silently. Document what each mode needs, and let the caller grant it on the
  job.
- 🪤 **Don't `paths-ignore` a workflow that produces a required check.** It never starts,
  so the check stays «Expected — waiting» forever. Gate the job with `if:` instead: a
  skipped job counts as passing. And test `!= 'false'`, never `== 'true'`, so an empty
  output still runs the job.
- 🪤 **Touching the registry costs one PR per consuming app.** Know which file travels:
  - `registry/app/assets/css/pharos-components.css` is synced verbatim;
  - `registry/app/layouts/default.vue` is in the sync's skip list, so it never reaches an
    existing app.

  Check drift before changing it (`registry/README.md`).
- 🪤 A synced barrel (`index.ts`) must not re-export files the sync skips: apps that adopt
  only part of it get dangling imports.
- 🪤 **The agent files in `agents/` are the single source.** The `core` plugin's agents
  only point here, and the plan hook and gate read `agents/plan-craft.agent.md`. Edit
  them here, never in a copy.
- 🪤 `README.md` lists an `instructions/` folder that no longer exists at the repo root
  (measured 2026-10-25).
- Skill, command and `*.agent.md` files are written in English; what they produce is in
  Spanish (`KNOWLEDGE-MANAGEMENT.md`).
