// useCan — the Pháros standard capability gate (RFC 0016 Phase 4, shared admin
// block). ONE definition of "does the current user hold capability X" for every
// Pháros app, so the gate can't drift app-to-app.
//
// A Pinia store holds the session (user + role + a {capability: bool} map) and
// exposes `can(cap) = permissions[cap] === true` — fail-CLOSED: an unknown or
// unloaded capability is "no", never "yes". This mirrors the backend contract
// (auth-contract.md C7): the FE gate is UX only; `require_capability` on the
// backend is the real boundary regardless.
//
// Auth transport is an APP-integration concern (same split as useAsyncState):
// the app owns its auth-aware fetcher (Bearer injection / 401→SSO bounce) and
// its session endpoint, and calls `load(fetcher, sessionUrl)` ONCE on mount.
// The store just holds the result and answers can().
//
//   // app plugin / layout, once:
//   const auth = usePharosAuthStore()
//   await auth.load((u) => apiFetch(u), `${base}/auth/session`)
//   // anywhere:
//   const { can } = useCan()
//   if (can('admin.manage_users')) { … }
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface PharosAuthUser {
  username: string
  [key: string]: unknown
}

export interface PharosSession {
  user: PharosAuthUser
  role: string
  permissions: Record<string, boolean>
}

/** App-supplied auth-aware fetcher (e.g. a wrapped $fetch). */
export type SessionFetcher = (url: string) => Promise<PharosSession>

/**
 * Shared session store. `id: 'pharosAuth'` is fixed so every app resolves the
 * same store — do NOT re-id it per app.
 */
export const usePharosAuthStore = defineStore('pharosAuth', () => {
  const user = ref<PharosAuthUser | null>(null)
  const role = ref<string | null>(null)
  const permissions = ref<Record<string, boolean>>({})
  const loaded = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Idempotent: loads the session once. The app passes its own auth-aware
   * fetcher + the fully-resolved session URL, so this composable stays free of
   * any per-app base/transport assumptions. Leaves the store empty (fail-closed)
   * on error — the UI then renders as if the user has no capabilities.
   */
  async function load(fetcher: SessionFetcher, sessionUrl: string): Promise<void> {
    if (loaded.value || loading.value) return
    loading.value = true
    error.value = null
    try {
      const data = await fetcher(sessionUrl)
      user.value = data.user
      role.value = data.role
      permissions.value = data.permissions
      loaded.value = true
    } catch (e) {
      error.value = 'No se pudo cargar la sesión.'
      console.error('[pharosAuth] session load failed', e)
    } finally {
      loading.value = false
    }
  }

  /** The single gate the rest of the app uses. Fail-closed. */
  function can(capability: string): boolean {
    return permissions.value?.[capability] === true
  }

  const isLoggedIn = computed(() => user.value !== null)

  return { user, role, permissions, loaded, loading, error, load, can, isLoggedIn }
})

/**
 * Convenience wrapper so pages/components read a single `can` without reaching
 * for the store id. Keep the store as the source of truth for `load()`.
 */
export function useCan() {
  const store = usePharosAuthStore()
  return {
    can: (capability: string) => store.can(capability),
    role: computed(() => store.role),
    isLoggedIn: computed(() => store.isLoggedIn),
  }
}
