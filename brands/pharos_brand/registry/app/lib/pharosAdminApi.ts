// pharosAdminApi — the Pháros admin (roles/users) API client, as ONE shared
// factory (RFC 0016 Phase 4). The 10 `/auth/admin/*` calls the RoleCapabilityMatrix
// + UsersRoleTable primitives drive, parameterized by the app's API base — the
// "API base currently hard-coded per app" that RFC 0016 Phase 4 addresses.
//
// The app injects its own auth-aware fetcher (Bearer / 401→SSO bounce) + the
// resolved base (`${apiBase}${mountPrefix}`, e.g. finance `…/api/v1`, lab-qc
// `…` (no prefix), admission `…/queue/api/v1`). Transport stays app-owned; the
// call surface + the DTO shapes are the shared contract that must not drift.
//
//   const admin = createPharosAdminApi((url, init) => apiFetch(url, init),
//                                      `${cfg.public.apiBase}/api/v1`)
//   const roles = await admin.listRoles()

/** Minimal fetcher contract — a wrapped $fetch the app already owns. */
export type AdminFetcher = <T>(url: string, init?: {
  method?: string
  body?: unknown
}) => Promise<T>

// ── DTOs (the shared shapes the admin surface returns/accepts) ────────────────

export interface PharosCapability {
  id: string
  area: string
  label: string
}

export interface PharosRoleCapabilities {
  role: string
  label: string
  description: string
  capabilities: string[]
  is_system: boolean
  is_admin: boolean
}

export interface PharosUserRole {
  id: number
  username: string
  role: string
  notes: string | null
  updated_at: string
}

export interface CreateUserIn {
  username: string
  role: string
  notes?: string | null
}
export interface UpdateUserIn {
  role?: string
  notes?: string | null
}
export interface SetRoleCapabilitiesIn {
  capabilities: string[]
}
export interface CreateRoleIn {
  name: string
  label: string
  description?: string
}
export interface EditRoleIn {
  label: string
  description?: string
}

export interface PharosAdminApi {
  listUsers(): Promise<PharosUserRole[]>
  createUser(body: CreateUserIn): Promise<PharosUserRole>
  updateUser(username: string, body: UpdateUserIn): Promise<PharosUserRole>
  deleteUser(username: string): Promise<void>
  listCapabilities(): Promise<PharosCapability[]>
  listRoles(): Promise<PharosRoleCapabilities[]>
  setRoleCapabilities(role: string, body: SetRoleCapabilitiesIn): Promise<PharosRoleCapabilities>
  createRole(body: CreateRoleIn): Promise<PharosRoleCapabilities>
  editRole(name: string, body: EditRoleIn): Promise<PharosRoleCapabilities>
  deleteRole(name: string): Promise<void>
}

/**
 * Build the admin client. `base` is the fully-resolved prefix up to (not
 * including) `/auth/admin` — the ONE per-app knob. `enc` guards usernames/role
 * slugs that reach the path.
 */
export function createPharosAdminApi(fetcher: AdminFetcher, base: string): PharosAdminApi {
  const at = (path: string) => `${base}${path}`
  const enc = encodeURIComponent
  return {
    listUsers: () => fetcher(at('/auth/admin/users')),
    createUser: (body) => fetcher(at('/auth/admin/users'), { method: 'POST', body }),
    updateUser: (username, body) =>
      fetcher(at(`/auth/admin/users/${enc(username)}`), { method: 'PATCH', body }),
    deleteUser: (username) =>
      fetcher(at(`/auth/admin/users/${enc(username)}`), { method: 'DELETE' }),
    listCapabilities: () => fetcher(at('/auth/admin/capabilities')),
    listRoles: () => fetcher(at('/auth/admin/roles')),
    setRoleCapabilities: (role, body) =>
      fetcher(at(`/auth/admin/roles/${enc(role)}/capabilities`), { method: 'PUT', body }),
    createRole: (body) => fetcher(at('/auth/admin/roles'), { method: 'POST', body }),
    editRole: (name, body) =>
      fetcher(at(`/auth/admin/roles/${enc(name)}`), { method: 'PATCH', body }),
    deleteRole: (name) => fetcher(at(`/auth/admin/roles/${enc(name)}`), { method: 'DELETE' }),
  }
}
