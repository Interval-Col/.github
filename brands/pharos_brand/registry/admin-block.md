# Pháros admin block — roles/users (RFC 0016 Phase 4)

The shared FE for an app's **self-serve role/capability administration** — the
`/admin/roles` + `/admin/users` surface. ONE definition so it can't drift across
apps (finance-lch ↔ lab-qc ↔ admission-patient ↔ …). Enforced by
[`auth-contract.md`](../../../auth-contract.md) **C9 / check A9**: once an app
declares `fe_registry_adopted: on`, its admin pages must use these primitives —
a hand-rolled admin fails the gate.

> This is the **functional** layer (matrix logic, gate, API client). The
> **visual** admin surface guidance lives in [`surfaces/administracion.md`](surfaces/administracion.md).

## What's in the registry (synced verbatim)

| Entry | Path | What it is |
|---|---|---|
| `RoleCapabilityMatrix` | `components/ui/role-capability-matrix/` | role×area×capability grid + draft/dirty/save buffer + admin-role lock; create/rename/delete roles when `customRolesEnabled` |
| `UsersRoleTable` | `components/ui/users-role-table/` | assign / change / remove a user's role + self-protection |
| `useCan` / `usePharosAuthStore` | `composables/useCan.ts` | session store + `can(cap)` (fail-closed); FE gate is UX only (C7) |
| `createPharosAdminApi` | `lib/pharosAdminApi.ts` | the 10 `/auth/admin/*` calls, parameterized by API base |

## Per-app config (the only knobs — §2b extension points)

| Prop / arg | finance | lab-qc | admission |
|---|---|---|---|
| `adminRoleName` | `admin` | `administrator` | `admin` |
| `defaultRole` | `viewer` | `viewer` | `viewer` |
| `customRolesEnabled` | `true` | `false` | `false` |
| API base (`createPharosAdminApi` 2nd arg) | `…/api/v1` | `…` (no prefix) | `…/queue/api/v1` |

The **role-label map is NOT a knob** — labels come from the API
(`PharosRoleCapabilities.label`); never hard-code them.

## Adoption

1. `scripts/sync-pharos-registry.sh <app-fe-dir> [repo-root]` — copies the
   primitives into the app's `app/**`. Ensure the app has the shadcn base
   wrappers the primitives import (`badge checkbox input select table` — all
   Pháros apps do; add with `pnpm dlx shadcn-vue@latest add …` if missing).
2. Load the session once (app plugin/layout), passing the app's auth-aware fetcher:
   ```ts
   const cfg = useRuntimeConfig()
   const auth = usePharosAuthStore()
   await auth.load((u) => apiFetch(u), `${cfg.public.apiBase}/api/v1/auth/session`)
   ```
3. Re-point the app-owned thin pages onto the primitives:
   ```vue
   <!-- app/pages/admin/roles.vue — app-owned shell, ~10 lines -->
   <script setup lang="ts">
   import { RoleCapabilityMatrix } from '~/components/ui/role-capability-matrix'
   import { createPharosAdminApi } from '~/lib/pharosAdminApi'
   import { apiFetch } from '~/utils/apiFetch'
   definePageMeta({ requiresCap: 'admin.manage_role_capabilities' })
   const cfg = useRuntimeConfig()
   const admin = createPharosAdminApi((url, init) => apiFetch(url, init), `${cfg.public.apiBase}/api/v1`)
   </script>
   <template>
     <RoleCapabilityMatrix :api="admin" :custom-roles-enabled="true" />
   </template>
   ```
   (`users.vue` wires `UsersRoleTable` the same way, `requiresCap: 'admin.manage_users'`.)
4. Flip `fe_registry_adopted: on` in `.auth-contract.yml`, verify in-browser as
   each role, then the A9 gate holds it in place.
