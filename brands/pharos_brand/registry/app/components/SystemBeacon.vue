<script setup lang="ts">
// Live system-health beacon — "vigilamos lo invisible" made literal. Reads the
// shared poller (useHealthBeacon) and renders the accent-INDEPENDENT status palette
// (RFC 0008 Q4), NOT the brand accent, so it never shifts when a sub-brand re-accents.
// 'ok' is the calm rest/all-clear state (steady); 'drift'/'out' pulse. When the backend
// reports subsystems, the beacon becomes a popover with the per-subsystem breakdown
// (structure + status only — never PHI).
//
// PRESENTATION is its own brand knob (spec f6e8c984, "Beacon de estado · presentación").
// Six registers: three that are READ, in the topbar (dot / dot+label / pill), two that are
// pure light on the canvas with no words at all (a standing bar in the bottom-right corner,
// a lit rail along the bottom edge), and off. The APP picks the register — never the state:
//
//     runtimeConfig.public.beaconMode  →  <html data-beacon>  →  this component
//
// Config is the source, because it is identical on the server and the client — so an SSR app
// hydrates clean (3 of the 4 consuming apps render on the server; reading the DOM at setup
// would tear). The attribute is the published contract, mirrored by beacon-mode.client.ts,
// and flipping it live — devtools, QA, NUXT_PUBLIC_BEACON_MODE — is honoured with no rebuild.
//
// The component mounts TWICE — place="topbar" and place="canvas" — and each mount renders only
// the registers that belong to it, so the knob moves the beacon between the topbar and the
// canvas without the layout ever branching on the mode.
//
// FAIL-SAFE, and load-bearing. The re-sync bot refreshes components but NEVER layouts (those
// are app-owned scaffold), so an app can end up carrying a canvas register with no canvas
// mount — that is, no beacon at all. The topbar mount detects exactly that and falls back to
// dot+label. Same reason an unconfigured app resolves to 'dot-label' (the beacon this shell
// has always had) and not the family's 'bar': absence of config must never mean absence of
// beacon.
//
// Colour is never the only channel: every register carries the state in `title` and in an
// aria-live region, and every pulse is disabled under prefers-reduced-motion.
//
// Every rendered root carries `data-pg-beacon` (the live register) and `data-pg-place`, joining
// the shell's data-pg-* contract (data-pg-sidebar / data-pg-topbar / data-pg-content). That is
// what lets a contract test assert WHICH register is live — the failure this component is built
// to survive (a beacon that quietly renders nowhere) is invisible to a test that can only ask
// "is some beacon present?".
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import type { BeaconStatus } from '~/composables/useHealthBeacon'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'

const props = withDefaults(defineProps<{ place?: 'topbar' | 'canvas' }>(), { place: 'topbar' })
const place = computed(() => props.place)

const MODES = ['dot', 'dot-label', 'pill', 'bar', 'rail', 'none'] as const
type BeaconMode = (typeof MODES)[number]

const FALLBACK: BeaconMode = 'dot-label'
const READ_MODES: BeaconMode[] = ['dot', 'dot-label', 'pill'] // topbar, and they carry words
const CANVAS_MODES: BeaconMode[] = ['bar', 'rail'] // canvas, and they carry none

const asMode = (v: unknown): BeaconMode =>
  (MODES as readonly string[]).includes(String(v)) ? (String(v) as BeaconMode) : FALLBACK

const mode = ref<BeaconMode>(asMode((useRuntimeConfig().public as Record<string, unknown>).beaconMode))

// A canvas register has nowhere to render without a place="canvas" mount. Both mounts of the
// component share this flag, so the topbar mount can tell whether it is alone in the shell.
const canvasMounted = useState<boolean>('pharos:beacon-canvas-mounted', () => false)
const settled = ref(false)
let observer: MutationObserver | null = null

onMounted(async () => {
  if (props.place === 'canvas') canvasMounted.value = true

  const readAttr = () => {
    const attr = document.documentElement.dataset.beacon
    if (attr) mode.value = asMode(attr)
  }
  readAttr()
  observer = new MutationObserver(readAttr)
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-beacon'] })

  // Let every mount register itself before the topbar concludes it is alone — otherwise the
  // healthy case would flash dot+label for a tick on its way to the bar.
  await nextTick()
  settled.value = true
})

onUnmounted(() => {
  observer?.disconnect()
  if (props.place === 'canvas') canvasMounted.value = false
})

const effective = computed<BeaconMode>(() =>
  settled.value && CANVAS_MODES.includes(mode.value) && !canvasMounted.value ? FALLBACK : mode.value,
)

const topbar = computed(() => props.place === 'topbar')
const canvas = computed(() => props.place === 'canvas')
const isRead = computed(() => topbar.value && READ_MODES.includes(effective.value))
const isPill = computed(() => effective.value === 'pill')

const MAP: Record<BeaconStatus, { label: string; dot: string; text: string; chip: string }> = {
  ok: { label: 'En orden', dot: 'bg-status-success', text: 'text-status-success', chip: 'bg-status-success-bg' },
  drift: { label: 'Derivando', dot: 'bg-status-warning', text: 'text-status-warning', chip: 'bg-status-warning-bg' },
  out: { label: 'Fuera de rango', dot: 'bg-status-error', text: 'text-status-error', chip: 'bg-status-error-bg' },
}

const state = useHealthBeacon()
const s = computed(() => MAP[state.value.status] ?? MAP.ok)
const alert = computed(() => state.value.status !== 'ok')
const hasSubsystems = computed(() => state.value.subsystems.length > 0)
const label = computed(() => `Sistema: ${s.value.label}`)
const checkedLabel = computed(() =>
  state.value.checkedAt
    ? new Date(state.value.checkedAt).toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
    : '—',
)

// The three topbar registers are one face with the words dialled up or down: the dot alone, the
// dot with its label, or the whole chip tinted with the status token (the pill).
const faceClass = computed(() => [
  'hidden items-center lg:inline-flex',
  isPill.value ? ['gap-1.5 rounded-full px-2.5 py-1', s.value.chip, s.value.text] : 'gap-2',
])
</script>

<template>
  <!-- ══════ topbar — the registers that are READ ══════ -->

  <!-- With subsystems the face opens the per-subsystem breakdown. -->
  <Popover v-if="isRead && hasSubsystems">
    <PopoverTrigger
      class="outline-none"
      :class="faceClass"
      :title="label"
      :data-pg-beacon="effective"
      :data-pg-place="place"
      aria-live="polite"
    >
      <span class="relative flex" :class="isPill ? 'size-1.5' : 'size-2'">
        <span
          v-if="alert"
          aria-hidden="true"
          class="absolute inline-flex size-full animate-ping rounded-full opacity-60 motion-reduce:animate-none"
          :class="s.dot"
        />
        <span aria-hidden="true" class="relative inline-flex size-full rounded-full" :class="s.dot" />
      </span>
      <span
        v-if="effective !== 'dot'"
        class="font-mono uppercase"
        :class="isPill ? 'text-[10px] tracking-wider' : ['text-[11px] tracking-wide', s.text]"
      >
        {{ s.label }}
      </span>
      <span v-else class="sr-only">{{ label }}</span>
    </PopoverTrigger>
    <PopoverContent align="end" class="w-64 p-2">
      <div class="mb-1.5 flex items-center justify-between">
        <span class="font-mono text-[11px] uppercase tracking-wide" :class="s.text">{{ s.label }}</span>
        <span class="text-[11px] text-muted-foreground">{{ checkedLabel }}</span>
      </div>
      <ul class="flex flex-col gap-1">
        <li
          v-for="sub in state.subsystems"
          :key="sub.name"
          class="flex items-center justify-between gap-2 text-[0.8rem]"
        >
          <span class="truncate text-foreground">{{ sub.name }}</span>
          <span class="size-1.5 shrink-0 rounded-full" :class="(MAP[sub.status] ?? MAP.ok).dot" />
        </li>
      </ul>
    </PopoverContent>
  </Popover>

  <!-- No subsystems → the same face, with nothing to open. -->
  <span
    v-else-if="isRead"
    :class="faceClass"
    :title="label"
    :data-pg-beacon="effective"
    :data-pg-place="place"
    role="status"
    aria-live="polite"
  >
    <span class="relative flex" :class="isPill ? 'size-1.5' : 'size-2'">
      <span
        v-if="alert"
        aria-hidden="true"
        class="absolute inline-flex size-full animate-ping rounded-full opacity-60 motion-reduce:animate-none"
        :class="s.dot"
      />
      <span aria-hidden="true" class="relative inline-flex size-full rounded-full" :class="s.dot" />
    </span>
    <span
      v-if="effective !== 'dot'"
      class="font-mono uppercase"
      :class="isPill ? 'text-[10px] tracking-wider' : ['text-[11px] tracking-wide', s.text]"
    >
      {{ s.label }}
    </span>
    <span v-else class="sr-only">{{ label }}</span>
  </span>

  <!-- No beacon — the logo's pilot light is the only carrier left; the state is still announced. -->
  <span
    v-else-if="topbar && effective === 'none'"
    class="sr-only"
    :data-pg-beacon="effective"
    :data-pg-place="place"
    role="status"
    aria-live="polite"
  >
    {{ label }}
  </span>

  <!-- ══════ canvas — pure light, no words ══════ -->

  <!-- Bar — the lighthouse seen from the ship: a column of light in the app's bottom-right corner.
       It is seated ON the bottom edge, square-cut: a tower rising from the floor, not a pill
       floating near it, and it grows upward on hover (items-end). On alert it is the HALO that
       breathes, never the light itself — a beacon that dimmed when the system went out of range
       would be an alarm that goes quiet. The body stays solid; the blurred clone behind it swells.
       With subsystems the hover-grow is not just an affordance: the bar opens the same breakdown
       the topbar registers do, anchored to the corner (German, 2026-07-13). At rest it is still
       pure light — nothing is written on the canvas.
       Unlike the topbar registers this is NOT gated behind lg:. Those hide on small screens
       because words in a cramped topbar are what does not fit; six pixels of light in the corner
       cost no layout at all. Gating it would leave a reception tablet — the surface least able to
       afford a silent system — with no beacon whatsoever. -->
  <Popover v-else-if="canvas && effective === 'bar' && hasSubsystems">
    <PopoverTrigger
      class="group fixed bottom-0 right-0 z-30 flex items-end outline-none"
      :class="s.text"
      :title="label"
      :data-pg-beacon="effective"
      :data-pg-place="place"
    >
      <span
        class="relative flex h-8 w-1.5 transition-all duration-300 group-hover:h-11 group-hover:w-2.5 motion-reduce:transition-none"
      >
        <span
          v-if="alert"
          aria-hidden="true"
          class="absolute inset-x-[-3px] -top-2 bottom-0 animate-pulse blur-[6px] motion-reduce:animate-none"
          :class="s.dot"
        />
        <span aria-hidden="true" class="relative size-full shadow-[0_0_16px_currentColor]" :class="s.dot" />
      </span>
      <span class="sr-only" role="status" aria-live="polite">{{ label }}</span>
    </PopoverTrigger>
    <PopoverContent align="end" side="top" class="mb-1 mr-1 w-64 p-2">
      <div class="mb-1.5 flex items-center justify-between">
        <span class="font-mono text-[11px] uppercase tracking-wide" :class="s.text">{{ s.label }}</span>
        <span class="text-[11px] text-muted-foreground">{{ checkedLabel }}</span>
      </div>
      <ul class="flex flex-col gap-1">
        <li
          v-for="sub in state.subsystems"
          :key="sub.name"
          class="flex items-center justify-between gap-2 text-[0.8rem]"
        >
          <span class="truncate text-foreground">{{ sub.name }}</span>
          <span class="size-1.5 shrink-0 rounded-full" :class="(MAP[sub.status] ?? MAP.ok).dot" />
        </li>
      </ul>
    </PopoverContent>
  </Popover>

  <!-- Bar, with no subsystems to show → inert light, nothing to open. -->
  <span
    v-else-if="canvas && effective === 'bar'"
    class="group fixed bottom-0 right-0 z-30 flex items-end"
    :class="s.text"
    :title="label"
    :data-pg-beacon="effective"
    :data-pg-place="place"
  >
    <span
      class="relative flex h-8 w-1.5 transition-all duration-300 group-hover:h-11 group-hover:w-2.5 motion-reduce:transition-none"
    >
      <span
        v-if="alert"
        aria-hidden="true"
        class="absolute inset-x-[-3px] -top-2 bottom-0 animate-pulse blur-[6px] motion-reduce:animate-none"
        :class="s.dot"
      />
      <span aria-hidden="true" class="relative size-full shadow-[0_0_16px_currentColor]" :class="s.dot" />
    </span>
    <span class="sr-only" role="status" aria-live="polite">{{ label }}</span>
  </span>

  <!-- Rail — the horizon line: the whole bottom edge of the canvas is the beacon. Faint in calm,
       lit when it drifts; zero pixels of chrome stolen. Deliberately inert (a 3px full-bleed
       hairline is not a hit target) — an app that wants the breakdown picks a read register. -->
  <span
    v-else-if="canvas && effective === 'rail'"
    class="pointer-events-none absolute inset-x-0 bottom-0 z-30 block h-[3px]"
    :class="s.text"
    :data-pg-beacon="effective"
    :data-pg-place="place"
  >
    <span aria-hidden="true" class="block size-full" :class="[s.dot, alert ? 'opacity-90' : 'opacity-45']" />
    <span
      v-if="alert"
      aria-hidden="true"
      class="absolute inset-0 animate-pulse blur-[3px] motion-reduce:animate-none"
      :class="s.dot"
    />
    <span class="sr-only" role="status" aria-live="polite">{{ label }}</span>
  </span>
</template>
