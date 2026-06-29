// Starts the single live system-health beacon poller (client only).
//
// Default source = the app's own backend liveness (/health) — RFC 0008
// §System-health beacon. This ships the beacon live with NO per-app blocker;
// richer LIS signals (analyzer connectivity, pending-validation backlog,
// cobolql facade) are an optional later enrichment (owner + backend), with no
// FE or contract change. The composable maps {status:"healthy"} → 'ok' and any
// unreachable/error → 'drift'.
//
// Health URL resolution (config, not a per-app file fork):
//   • An app MAY set `public.healthBeaconUrl` to an explicit, fully-qualified
//     liveness URL. Use this when the bare `apiBase/health` is NOT reachable —
//     e.g. behind a shared reverse proxy that only forwards a versioned path
//     (admission-patient: the proxy forwards `…/queue/api/v1/health`, not the
//     unversioned `…/queue/api/health`, which 404s + spams CORS).
//   • Otherwise the default is the app's own backend liveness at `apiBase/health`.
//   • If neither is configured, the beacon stays quiet (no errant fetch).
// Reads are cast through the public-config bag so apps need only declare the
// key(s) they actually use (not every app has `apiBase`, nor `healthBeaconUrl`).
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const pub = config.public as Record<string, unknown>
  const explicit = String(pub.healthBeaconUrl ?? '')
  const apiBase = String(pub.apiBase ?? '')
  const url = explicit || (apiBase ? `${apiBase}/health` : '')
  if (!url) return
  startHealthBeacon(url)
})
