# The Pháros auth contract

> **Normative** org standard — RFC 0016 Phase 1 (`rfcs/0016-pharos-auth-contract.md`).
> Machine-checked subset enforced by the reusable workflow
> [`auth-contract-check.yml`](.github/workflows/auth-contract-check.yml) +
> [`scripts/auth-contract-check.py`](scripts/auth-contract-check.py).
> Cites rather than restates: the *what/who* is RFC 0012 (accepted — authz is local);
> this doc is the *how* a conforming auth module behaves. Sibling of the
> [nucleus-db tenant contract](db-tenant-contract.md).

**"Auth module" here means**: an app's self-serve role/capability administration —
a role×capability matrix, user→role assignment, and capability-gated route
enforcement, resolved **locally** from the app's own tables. It is unrelated to
*identity* (SSO/IAM issues the token and gates coarse frontend-route navigation;
`is_authorized` is deliberately not called for in-app capability checks — RFC 0012).

Current auth apps: finance-lch (source, live prod) · pharos-lis (lab-qc) ·
admission-patient. Greenfield adopters (no role layer yet): commercial-lch ·
biuman-lis. The three existing modules drifted independently — this contract is
the anti-drift baseline they converge to (RFC 0016).

---

## The contract

| # | Clause | Source of authority |
|---|---|---|
| **C1** | **Authorization is local; IAM is identity only.** The current user comes from IAM (`get_user_by_token`); *what they may do* is resolved in-process from the app's own role→capability tables. The SSO `is_authorized` endpoint is not called for in-app capability checks. | RFC 0012 (Access-as-Code, accepted) |
| **C2** | **The capability gate.** Every protected route is guarded by `require_capability(cap)` — a dependency that raises at import for an unknown capability id and returns **403** at request time. Role resolution: `resolve_role` (no/unknown role → least-privilege `viewer`) → `capabilities_for` (the admin role short-circuits to all-True). `require_role` is not a primary gate — only a *documented, allowlisted* migration shim. | RFC 0016; reference impl: finance-lch `backend/app/auth/deps.py` |
| **C3** | **The admin surface.** The seven `/auth/admin/*` endpoints exist with the contract verbs/paths: `GET/POST/PATCH/DELETE users`, `GET capabilities`, `GET roles`, `PUT roles/{role}/capabilities`. | RFC 0016; finance-lch `backend/app/auth/admin_router.py` |
| **C4** | **Runtime role registry.** Roles are DB-backed and administrable at runtime — create / rename / delete a role, `is_system` on built-ins — not a code-only closed set. (D4: on every app; a converging clone declares `custom_roles: off` until it lands.) | RFC 0016 D4; finance-lch `finance_roles` |
| **C5** | **Idempotent seeding as a deploy step, never on startup.** Default role→capability seeding is idempotent (seeds only a role with zero rows, so admin edits survive redeploys) and runs as a deploy-step one-shot / migrate job — **not** in a FastAPI lifespan or import path. Aligns with the nucleus-db tenant contract C2. | RFC 0016; db-tenant-contract C2 (ADR 0004) |
| **C6** | **Self-protection.** An admin cannot demote or delete their own role row; the admin role is reserved for the bootstrap user and rendered read-only. Recovery is re-seeding the bootstrap admin on next deploy. *Prose clause — not machine-checked.* | RFC 0016; finance-lch `admin_router.py` |
| **C7** | **The backend is the only gate; the FE mirrors it.** Frontend capability references (`requiresCap`, `can('…')`, menu gates) are a **subset** of the backend capability catalog; FE enforcement (`NUXT_PUBLIC_ENFORCE_CAPABILITIES`) is UX only. Backend `require_capability` is the security boundary regardless of the flag. | RFC 0016 D5 |
| **C8** | **Per-app catalog is the only variation.** The capability catalog, role vocabulary, admin-role name, and schema/table names are declared per app in the manifest; the machinery (C1–C7) does not vary. Schema: the `role` column is at least the standard width (drift: `String(20)` is one char from the wall). | RFC 0016 §2b (the seam) |
| **C9** | **The FE admin runs on the shared registry primitives.** The `/admin/roles` + `/admin/users` surface is built from the RFC 0008 copy-in registry primitives (`RoleCapabilityMatrix`, `UsersRoleTable`, `useCan`/`usePharosAuthStore`, `createPharosAdminApi`) — parameterized per app (`adminRoleName`, `defaultRole`, `customRolesEnabled`, API base), **never hand-rolled**. Adopted apps declare `fe_registry_adopted: on`; the role-label map is already API-driven, so nothing to hard-code. | RFC 0016 Phase 4; RFC 0008 registry; .github#110 |

---

## Enforcement — `auth-contract-check`

Each auth app carries an `.auth-contract.yml` manifest (its declared shape) and a
thin caller workflow; the check itself lives here and evolves centrally.

| Check | Asserts | Clause |
|---|---|---|
| A1 | manifest valid, referenced paths exist | — |
| A2 | the 7 `/auth/admin/*` endpoints present in the admin router | C3 |
| A3 | `require_capability` guards unknown capability ids (KeyError at import) | C2 |
| A4 | no seeding/`upgrade`/`create_all` on app startup outside a deploy step (allowlist = file + reason) | C5 |
| A5 | every FE capability reference is a subset of the backend catalog | C7 |
| A6 | auth tables present; `role` column width ≥ the standard minimum | C8 |
| A7 | *info/warn:* runtime role registry (create/rename/delete-role) present | C4 |
| A8 | *info/warn:* `require_role` used as a gate is allowlisted as a documented shim | C2 |
| A9 | *info until adopted:* with `fe_registry_adopted: on`, the FE admin pages reference the registry primitives (`RoleCapabilityMatrix`/`UsersRoleTable`) — a hand-rolled admin **FAILs** | C9 |

The checks are deliberate **text-level heuristics** — cheap, deterministic,
stdlib-only (no PyPI on the merge path, same rule as `db-tenant-check.py`). They
catch the drift classes that actually occurred across the three clones; the RFC
and human review cover judgment.

### Manifest

```yaml
app: <name>
profile: app | greenfield             # greenfield = no auth module yet (A1 + info only)
admin_role: admin                     # the reserved superuser role name (lab-qc: administrator)
backend_dir: backend                  # repo-root-relative
auth_dir: backend/app/auth
admin_router: backend/app/auth/admin_router.py
deps: backend/app/auth/deps.py
capabilities: backend/app/auth/capabilities.py
frontend_dir: frontend                # app-scoped in a monorepo (e.g. lab-qc/frontend)
auth_tables: [<app>_user_roles, <app>_role_capabilities, <app>_roles]
role_col_min: 32                       # required minimum width of the role column
custom_roles: on                       # C4; a converging clone may declare `off` until it lands
fe_registry_adopted: off               # C9; flip `on` once /admin uses the registry primitives (Phase 4)
startup_seed_allow:                    # optional; every entry needs a reason
  - file: backend/app/main.py
    reason: "dev-only, gated behind AUTH_MODE=mock"
require_role_allow:                    # optional; documented migration shims (C2)
  - file: backend/app/auth/deps.py
    reason: "lab-qc: require_role shim, Phase-3 router migration in flight"
```

Strict YAML subset (scalars, inline/block lists, one-level maps, lists of flat
maps); unquoted `#` starts a comment — quote values containing `#`. The parser
fails loudly on anything else: misparse never passes silently. (Same parser as
`db-tenant-check.py`.)

**Profiles:** `app` = has an auth module, full A1–A9 · `greenfield` = no auth
module on nucleus-db auth yet (A1 + an informational row; the full contract
applies at adoption, RFC 0016 Phase 4).

### Adoption (caller)

```yaml
# .github/workflows/auth-contract-check.yml  (standalone file — not in app ci.yml)
name: auth-contract-check
on:
  pull_request:
  workflow_dispatch:
jobs:
  auth-contract-check:
    uses: Interval-Col/.github/.github/workflows/auth-contract-check.yml@main
    with:
      enforce: false   # advisory during convergence; flip to true when green (RFC 0016 Phase 1)
```

### Rollout — advisory during convergence, then required

Unlike the DB gate (which was green on day one and flipped immediately, RFC 0015
OQ4), the three auth modules **start non-conformant by construction** — that is
the drift RFC 0016 exists to pay down. So callers adopt with `enforce: false`:
`auth-contract-check` annotates the drift and lands it on the dashboard without
blocking, each app converges under its own issue (finance-lch#101 epic), and
flips `enforce: true` + marks the check required once its first run is green.

**Standing rule — new apps comply from day one.** A greenfield adopter
(commercial-lch, biuman-lis) builds against the contract and adopts with
`enforce: true` in the PR that lands its auth module — no warn cycle.

**False-positive escape hatches** (why enforcing is safe once green): an
allowlist entry with a written reason in the app's own manifest (reviewed like
any code change), and the checker lives here — a fix merged `@main` heals every
app at once, no re-adoption.

---

## References

RFC 0016 (this contract) · RFC 0012 (Access-as-Code — authz is local; the
structural template) · RFC 0015 + [`db-tenant-contract.md`](db-tenant-contract.md)
(the sibling gate this mirrors) · RFC 0008 (design-system registry — the FE admin
primitives, RFC 0016 Phase 3) · finance-lch#101 (rollout epic) · finance-lch
`backend/app/auth/*` (the reference implementation the contract is drawn from).
