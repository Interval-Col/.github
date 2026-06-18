// useHealthBeacon — the shared live system-health beacon (RFC 0008 §System-health
// beacon). A single client-side poller hits the app's own backend health endpoint on
// a calm cadence, maps the result to ok | drift | out, mirrors it onto
// <html data-status> (which drives the .pharos-pilot animation on the logo), and
// exposes reactive state any component can read via useHealthBeacon().
//
// Failure mode (non-negotiable): unreachable / error / timeout → 'drift' (degraded,
// never alarmist); it never throws and never crashes the shell.
//
// PHI guardrail: the endpoint returns structure + aggregate status ONLY (subsystem
// names + states), never patient/row values — read-only. (Backend contract.)
//
// Registry-promotable: this composable is generic. The default health source (the
// app's backend liveness) is wired in app/plugins/health-beacon.client.ts.

export type BeaconStatus = 'ok' | 'drift' | 'out'

export interface BeaconSubsystem {
  name: string
  status: BeaconStatus
}

export interface BeaconState {
  status: BeaconStatus
  checkedAt: string | null
  subsystems: BeaconSubsystem[]
}

const STATE_KEY = 'pharos:health-beacon'
let started = false

function normalizeStatus(raw: unknown): BeaconStatus {
  if (raw === 'ok' || raw === 'drift' || raw === 'out') return raw
  if (typeof raw === 'string') {
    const s = raw.toLowerCase()
    if (['healthy', 'ready', 'up', 'ok', 'pass', 'green'].includes(s)) return 'ok'
    if (['degraded', 'warn', 'warning', 'drift', 'yellow'].includes(s)) return 'drift'
    if (['down', 'fail', 'error', 'out', 'red', 'unhealthy'].includes(s)) return 'out'
  }
  return 'ok' // a 2xx with an unrecognized shape = assume up
}

function parseSubsystems(raw: unknown): BeaconSubsystem[] {
  if (!Array.isArray(raw)) return []
  return raw
    .filter(
      (s): s is Record<string, unknown> =>
        !!s && typeof s === 'object' && typeof (s as Record<string, unknown>).name === 'string',
    )
    .map(s => ({ name: String(s.name), status: normalizeStatus(s.status) }))
}

/** Read the shared, reactive beacon state. Safe to call from any component. */
export function useHealthBeacon() {
  return useState<BeaconState>(STATE_KEY, () => ({
    status: 'ok',
    checkedAt: null,
    subsystems: [],
  }))
}

/**
 * Start the single client-side health poller. Idempotent — only the first call wires
 * the interval, so it is safe to call from a plugin and read from many components.
 */
export function startHealthBeacon(
  url: string,
  opts: { intervalMs?: number; timeoutMs?: number } = {},
) {
  if (!import.meta.client || started) return
  started = true

  const intervalMs = opts.intervalMs ?? 45_000 // calm cadence (BRAND §6.6 — humane)
  const timeoutMs = opts.timeoutMs ?? 8_000
  const state = useHealthBeacon()

  const set = (status: BeaconStatus, subsystems: BeaconSubsystem[] = []) => {
    state.value = { status, checkedAt: new Date().toISOString(), subsystems }
    document.documentElement.dataset.status = status // → .pharos-pilot pulse
  }

  const poll = async () => {
    const ctrl = new AbortController()
    const timer = window.setTimeout(() => ctrl.abort(), timeoutMs)
    try {
      const res = await fetch(url, { signal: ctrl.signal, headers: { accept: 'application/json' } })
      if (!res.ok) {
        set('drift') // reachable but unhealthy → degraded, not alarmist
        return
      }
      let body: unknown = null
      try {
        body = await res.json()
      } catch {
        /* non-JSON 2xx = up */
      }
      const record = body && typeof body === 'object' ? (body as Record<string, unknown>) : null
      set(
        record && 'status' in record ? normalizeStatus(record.status) : 'ok',
        record ? parseSubsystems(record.subsystems) : [],
      )
    } catch {
      set('drift') // unreachable / timeout → degraded; never crash the shell
    } finally {
      window.clearTimeout(timer)
    }
  }

  void poll()
  window.setInterval(() => void poll(), intervalMs)
  // Be calm but current: refresh when the user returns to the tab.
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) void poll()
  })
}
