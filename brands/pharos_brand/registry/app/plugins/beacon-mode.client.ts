// Publishes the app's chosen beacon register onto <html data-beacon> (spec f6e8c984,
// "Beacon de estado · presentación"). The app picks the register, never the state:
//
//     runtimeConfig.public.beaconMode  →  <html data-beacon>  →  SystemBeacon.vue
//
// SystemBeacon reads the SAME config directly, so it renders correctly with or without this
// plugin — the attribute is the published contract, not the wiring. What the plugin buys:
//   • the DOM tells the truth about which register is live (QA, CSS, screenshots, support);
//   • flipping it is a live operation — set `NUXT_PUBLIC_BEACON_MODE` per environment and
//     redeploy, or poke the attribute in devtools; SystemBeacon observes it. No rebuild.
//
// The register is a BRAND decision, not a health signal — `<html data-status>` (written by
// the health poller in useHealthBeacon) is what carries ok/drift/out. Keep them apart.
//
// Registers, and where each one renders:
//   dot · dot-label · pill   → the topbar (they carry words)
//   bar · rail               → the canvas (pure light, no words) — these REQUIRE the layout's
//                              <SystemBeacon place="canvas" /> mount; without it SystemBeacon
//                              falls back to dot-label rather than leave the app with no beacon.
//   none                     → nothing but the logo's pilot light (state still announced).
//
// Unset/unknown → 'dot-label', the beacon this shell has always had. Absence of config must
// never mean absence of beacon.
const MODES = ['dot', 'dot-label', 'pill', 'bar', 'rail', 'none']
const FALLBACK = 'dot-label'

export default defineNuxtPlugin(() => {
  const pub = useRuntimeConfig().public as Record<string, unknown>
  const configured = String(pub.beaconMode ?? '')
  document.documentElement.dataset.beacon = MODES.includes(configured) ? configured : FALLBACK
})
