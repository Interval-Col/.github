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
| `RoleCapabilityMatrix` | `components/ui/role-capability-matrix/` | role×area×capability grid + draft/dirty/save buffer + admin-role lock (extendable to extra roles via `lockedRoles`); create/rename/delete roles when `customRolesEnabled` |
| `UsersRoleTable` | `components/ui/users-role-table/` | assign / change / remove a user's role + self-protection |
| `useCan` / `usePharosAuthStore` | `composables/useCan.ts` | session store + `can(cap)` (fail-closed); FE gate is UX only (C7) |
| `createPharosAdminApi` | `lib/pharosAdminApi.ts` | the 10 `/auth/admin/*` calls, parameterized by API base |

## Per-app config (the only knobs — §2b extension points)

| Prop / arg | finance | lab-qc | admission |
|---|---|---|---|
| `adminRoleName` | `admin` | `administrator` | `admin` |
| `defaultRole` | `viewer` | `viewer` | `viewer` |
| `customRolesEnabled` | `true` | `false` | `false` |
| `lockedRoles` | — | — | — |
| API base (`createPharosAdminApi` 2nd arg) | `…/api/v1` | `…` (no prefix) | `…/queue/api/v1` |

The **role-label map is NOT a knob** — labels come from the API
(`PharosRoleCapabilities.label`); never hard-code them.

`lockedRoles` (default `[]`) hard-locks extra roles read-only — no toggling
their capabilities, and no rename/delete when `customRolesEnabled` — beyond
`adminRoleName`. It's for roles whose definition an RFC fixes, not this UI;
leaving them editable here would hand out a button to break that governance
constraint. None of finance/lab-qc/admission pass it (they're unaffected —
default `[]`). First consumer, **`pharos-ti`**: it locks both its superuser
and the RFC 0021 `audit` role (read-only, must never grow a second
capability):
```vue
<RoleCapabilityMatrix :api="admin" :locked-roles="['audit', 'platform_owner']" />
```

## Adoption

1. `scripts/sync-pharos-registry.sh <app-fe-dir> [repo-root]` — copies the
   primitives into the app's `app/**`.

   ⚠️ **«All Pháros apps have the shadcn base wrappers» was NOT true** — measured
   2026-08-20: `biuman-lis` had no `components/ui/badge`, so a `--add` of
   `RoleCapabilityMatrix` landed the component with a broken import, silently, and would
   have done so again on every routine re-sync. Two fixes, both live now:

   - **`badge` and `checkbox` ship FROM the registry** and travel as **companions** of
     `RoleCapabilityMatrix` — they were byte-identical across finance-lch, lab-qc and
     (checkbox) biuman-lis, so they were a shared primitive duplicated by hand. So are
     `lib/pharosAdminApi.ts` and the component's own `index.ts`: the sync now refuses to
     land the importer without them.
   - 🪤 **`components/ui/input` is a PREREQUISITE, not a companion.** It is the one
     primitive that **differs** in all three apps (each tuned it), so it stays app-owned
     and the registry cannot ship it. If the app lacks it the component will not compile:
     `pnpm dlx shadcn-vue@latest add input`. Same for `select` and `table` if a page needs
     them. `button` and `collapsible` already come from the registry.
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
