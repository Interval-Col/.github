// Starts the single live system-health beacon poller (client only).
//
// Default source = the app's own backend liveness (/health) — RFC 0008
// §System-health beacon. This ships the beacon live with NO per-app blocker;
// richer LIS signals (analyzer connectivity, pending-validation backlog,
// cobolql facade) are an optional later enrichment (owner + backend), with no
// FE or contract change. The composable maps {status:"healthy"} → 'ok' and any
// unreachable/error → 'drift'.
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const base = String(config.public.apiBase ?? '')
  startHealthBeacon(`${base}/health`)
})
