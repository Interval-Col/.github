// useAsyncState — the Pháros standard fetch/async-state envelope (RFC 0008
// component library, Phase 3). One uniform {data, status, loading, error,
// isEmpty} shape for every async read, honoring the org fetch contract
// (frontend-standards.md): an AbortController per call + a stale-response guard
// (a requestId that invalidates late responses) so a slow response never
// overwrites a newer one, and `isEmpty` is modeled EXPLICITLY — never conflated
// with `error`.
//
// Generic on purpose: the fetcher receives an AbortSignal and does the actual
// request. Auth (Bearer injection / 401→SSO bounce) and a generated typed
// client are APP-integration concerns layered on top of $fetch by the consuming
// app (admission-patient adds them in Phase 4) — NOT built into this envelope.
//
//   const { data, loading, error, isEmpty, refresh } = useAsyncState(
//     (signal) => $fetch('/api/pacientes', { signal }),
//     { default: [], immediate: true },
//   )
import { computed, shallowRef, ref } from 'vue'
import { tryOnScopeDispose } from '@vueuse/core'

export type AsyncStatus = 'idle' | 'pending' | 'success' | 'error'

export interface UseAsyncStateOptions<T> {
  /** Initial value before the first successful load. */
  default?: T
  /** Run execute() immediately on setup. Default false. */
  immediate?: boolean
  /** Reset data to `default` while a new execute() is in flight. Default false. */
  resetOnExecute?: boolean
}

/** Empty = null/undefined, [], '', or {} — modeled explicitly, separate from error. */
function computeEmpty(v: unknown): boolean {
  if (v == null) return true
  if (Array.isArray(v) || typeof v === 'string') return v.length === 0
  if (typeof v === 'object') return Object.keys(v as object).length === 0
  return false
}

/** Normalize any thrown value to a Spanish-safe message (FetchError {detail}/{message} aware). */
function normalizeError(e: unknown): string {
  if (e instanceof Error && e.message) return e.message
  if (typeof e === 'string') return e
  const any = e as { data?: { detail?: string, message?: string }, message?: string } | null
  return any?.data?.detail ?? any?.data?.message ?? any?.message ?? 'Error inesperado'
}

export function useAsyncState<T>(
  fetcher: (signal: AbortSignal) => Promise<T>,
  options: UseAsyncStateOptions<T> = {},
) {
  const def = (options.default ?? null) as T

  const data = shallowRef<T>(def)
  const status = ref<AsyncStatus>('idle')
  const error = ref<string | null>(null)

  const loading = computed(() => status.value === 'pending')
  // not empty while pending (avoids an empty-flash before data arrives)
  const isEmpty = computed(() => status.value !== 'pending' && computeEmpty(data.value))

  let controller: AbortController | null = null
  let requestId = 0

  async function execute(): Promise<T | undefined> {
    // cancel the in-flight request (and, via requestId, ignore its late response)
    controller?.abort()
    const local = new AbortController()
    controller = local
    const id = ++requestId

    status.value = 'pending'
    error.value = null
    if (options.resetOnExecute) data.value = def

    try {
      const result = await fetcher(local.signal)
      if (id !== requestId) return // superseded by a newer execute() — drop the stale result
      data.value = result
      status.value = 'success'
      return result
    }
    catch (e) {
      if (id !== requestId) return // stale failure — a newer call owns the state
      if (local.signal.aborted) return // aborted on purpose (refresh/dispose) — not an error
      error.value = normalizeError(e)
      status.value = 'error'
    }
  }

  /** Re-run; aborts any request still in flight first. */
  function refresh() {
    return execute()
  }

  // never let an in-flight request resolve into a torn-down scope
  tryOnScopeDispose(() => controller?.abort())

  if (options.immediate) void execute()

  return { data, status, loading, error, isEmpty, execute, refresh }
}
