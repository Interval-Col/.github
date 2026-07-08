# The nucleus-db tenant contract

> **Normative** org standard — RFC 0015 Phase 1 (`rfcs/0015-shared-db-tenant-contract.md`).
> Machine-checked subset enforced by the reusable workflow
> [`db-tenant-check.yml`](.github/workflows/db-tenant-check.yml) +
> [`scripts/db-tenant-check.py`](scripts/db-tenant-check.py).
> Cites rather than restates: the *what/who* is RFC 0005 (accepted, in force);
> this doc is the *how* a conforming app behaves.

**"DB tenant" here means**: an app (or service) holding a connection to the shared
PostgreSQL cluster `nucleus_db` and owning (or writing into) one or more of its
schemas. It is unrelated to *brand tenancy* (LCH/Biuman as Pháros brand tenants —
`brands/pharos_brand/BRAND.md`); the two vocabularies must not be mixed.

Current tenants: finance-lch · pharos-lis (lab-qc) · commercial-lch ·
admission-patient · cobol-migration (ETL). biuman-lis joins when `sports_lab`
onboards (RFC 0015 Phase 2). Out of scope: telemetry (MySQL), frozen pathology
(own Postgres).

---

## The contract

| # | Clause | Source of authority |
|---|---|---|
| **C1** | **Migrate as a deploy step, wired.** Schema changes apply only through the app's dedicated one-shot (`<app>-migrate` [→ `<app>-seed`] → app), each link `depends_on` the previous with `condition: service_completed_successfully`, actually exercised by the deploy — never parked behind a compose `profiles:` key, never a manual side-job. | nucleus-db ADR 0004; rfcs#8 ratification (`operations/plans/migrate-on-deploy-ratify-plan.md`) |
| **C2** | **No DDL/DML on app startup** in any non-dev environment. `alembic upgrade` / `init_db()` / `metadata.create_all()` / `CREATE SCHEMA` do not run in a lifespan or import path unless gated to dev and allowlisted in the manifest with a reason. | ADR 0004 ("never on app startup, never by hand") |
| **C3** | **TLS `verify-full` in prod.** The prod DSN carries `sslmode=verify-full` + the nucleus-db CA (`sslrootcert` / bind-mounted cert). asyncpg apps build an `ssl.SSLContext` explicitly (asyncpg ignores libpq URL params) — reference implementation: admission-patient `backend/app/core/database.py`. | `nucleus-db/operations/tls-verify-full-cert-delivery.md` |
| **C4** | **URL-encoded DSN.** Passwords never interpolate into raw f-strings; use `sqlalchemy.URL.create()` (encodes automatically) or an opaque-secret DSN. | `operations/runbooks/app-prod-go-live.md` §DSN |
| **C5** | **Liveness + readiness.** A no-dependency liveness endpoint (`/` or `/health`) plus a readiness endpoint (`/ready`) that probes the DB (`SELECT 1`, 503 on failure). Canonical shape: lab-qc `backend/app/features/health/router.py`. | RFC 0015 §Phase 1 |
| **C6** | **Pool + retry baseline.** Engines set `pool_pre_ping`; long-lived writers add `pool_recycle` and a transient-`OperationalError` retry (reference: cobol-migration `services/etl/db.py`). *Prose-only until the Phase 3 kit ships; not yet machine-checked.* | RFC 0015 §Phase 3 |
| **C7** | **Schema ownership + soft references.** Own schemas per RFC 0005 §2.1; cross-schema access is `SELECT`-only via explicit grant (`nucleus-db/operations/grants/grant-matrix.md`); cross-domain references are soft UUID columns, never hard FKs. | RFC 0005 §2.1, :497-503 |

**Schema shells:** today apps' `env.py` still runs `CREATE SCHEMA IF NOT EXISTS`
(reported informationally by the gate). Under **C-lite** (RFC 0015 Phase 2) the
nucleus-db steward pre-creates each shell + database-level grants and apps drop
that statement. New onboardings (commercial `crm`, biuman `sports_lab`) start
steward-owned; landed schemas retrofit later.

---

## Enforcement — `db-tenant-check`

Each tenant repo carries a `.db-tenant.yml` manifest (its declared shape) and a
thin caller workflow; the check itself lives here and evolves centrally.

| Check | Asserts | Clause |
|---|---|---|
| T1 | manifest valid, referenced paths exist | — |
| T2 | migrate one-shot chain wired (`service_completed_successfully`, no `profiles:`) | C1 |
| T3 | no startup-DDL patterns outside alembic roots (allowlist = file + reason) | C2 |
| T4 | `sslmode` + CA wiring present (or documented opaque-secret DSN) | C3 |
| T5 | no raw f-string DSN password interpolation | C4 |
| T6 | liveness + readiness routes present, readiness has a DB probe | C5 |
| T7 | *info only:* `CREATE SCHEMA` in `env.py` → Phase 2 target | — |

The checks are deliberate **text-level heuristics** — cheap, deterministic,
stdlib-only (no PyPI on the merge path, same rule as `plan_lint.py`). They catch
the drift classes that actually occurred; independent DDL review (RFC 0015
Phase 4) covers judgment.

### Manifest

```yaml
app: <name>
profile: alembic-app | dml-only | pre-onboarding
schemas: [<owned schemas>]
backend_dir: backend                      # repo-root-relative
deploy_compose: docker-compose.deploy.yml
deploy_chain: [<app>-migrate, <app>-backend]   # order = dependency order
alembic_roots: [backend/alembic]
health:
  liveness: /
  readiness: /ready
startup_ddl_allow:                        # optional; every entry needs a reason
  - file: backend/app/main.py
    reason: "gated behind DEV_MODE (ADR 0004)"
dsn_allow: []                             # optional, same shape
# dml-only extras:
# dsn_style: opaque-secret
# dsn_env: NUCLEUS_DB_DSN
```

Strict YAML subset (scalars, inline/block lists, one-level maps, lists of flat
maps); unquoted `#` starts a comment — quote values containing `#`. The parser
fails loudly on anything else: misparse never passes silently.

**Profiles:** `alembic-app` = full T1–T7 · `dml-only` = owns zero DDL (ETL;
T2 informational, T3 widened to all DDL statements) · `pre-onboarding` = not on
nucleus-db yet (T1 + informational row only).

### Adoption (caller)

```yaml
# .github/workflows/db-tenant-check.yml  (standalone file — not in app ci.yml)
name: db-tenant-check
on:
  pull_request:
  workflow_dispatch:
jobs:
  db-tenant-check:
    uses: Interval-Col/.github/.github/workflows/db-tenant-check.yml@main
    with:
      enforce: true    # drift blocks merges — enforced org-wide since 2026-07-08
```

### Rollout — enforced since 2026-07-08

RFC 0015 OQ4 planned a warn cycle; it was **superseded by decision 2026-07-08**
(all six adopters green on day one): `db-tenant-check / db-tenant-check` is a
**required status check on `develop` + `main` in every tenant repo**, and
`enforce: true` rode the convergence PRs in the two drifting repos
(commercial-lch, cobol-migration ETL) so no lane was ever blocked. The
conformance dashboard lives at `operations/ops/db-tenant/DASHBOARD.md`.

**Standing rule — new apps comply from day one.** Any app entering the shared
cluster adopts the manifest + caller with `enforce: true` in its very first PR,
and its onboarding starts with the steward-created schema shell (C-lite, RFC
0015 Phase 2). There are no warn cycles for new tenants.

**False-positive escape hatches** (why enforcing early is safe): an allowlist
entry with a written reason in the repo's own manifest (reviewed like any code
change), and the checker itself lives in this repo — a fix merged here `@main`
heals every tenant at once, no re-adoption needed.

---

## References

RFC 0015 (contract) · RFC 0005 (platform, §2.1 ownership) · nucleus-db ADR 0004
(migrate-as-deploy-step) · `operations/guides/base-compartida-nucleus-db.md`
(conceptual explainer) · `BRANCHING-AND-DEPLOY.md` §"Pre-deploy migration gate"
(the reserved seam this gate lands in) · RFC 0012 (per-repo manifest + shared CI
mechanism — the structural template).
