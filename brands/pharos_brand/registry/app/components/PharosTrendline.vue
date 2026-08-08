<script setup lang="ts">
// The Pháros trendline — the FINANCIAL half of the trend pair.
//
// Same engine as `PharosSparkline` (`~/lib/sparkline.ts`: ordering, domain,
// segmentation, gap handling, downsample, the spoken sentence). Different
// grammar, and the difference is not taste — the two surfaces are looking at
// different kinds of quantity:
//
//                    PharosSparkline (clínico)      PharosTrendline (financiero)
//   Each point       a DISCRETE EVENT — a specimen  a CONTINUOUS quantity sampled
//                    drawn on a date                daily
//   The question     "is it in range, did it move?" "which way is this going?"
//   Marks            carry meaning: "you were       false precision — a single day
//                    measured these four times"     is noise (weekends, batch billing)
//   Smoothing        FORBIDDEN — it would invent    expected, and why a moving
//                    measurements that never were   average exists upstream
//   Colour           a clinical judgement: reserved a DIRECTION: green is "went up",
//                    for the last mark, opt-in      and it asserts nothing further
//
// That last row is why this component exists rather than a `variant` prop on the
// other one. `PharosSparkline`'s header says a finance trend "has no such
// judgement to reinforce, and colouring it would assert one". The rule was
// right; it was being applied to the wrong object. On a revenue card there IS
// no judgement — up is up. Two components, so neither has to carry the other's
// caveats.
//
// ── Colour comes from `--trend-*`, never `--status-*` ───────────────────────
// Separate tokens on purpose. Re-accenting the CLINICAL palette must not move
// what "went up" means in Ingresos. They start in the same hue families and are
// free to diverge; both are defined per theme and measured ≥3:1 against their
// own background (unlike `--chart-*`, declared once and therefore legible in
// only one theme).
//
// Direction is never colour ALONE: the caller is expected to show the delta as
// text and an arrow beside this mark, exactly as the KPI card already does.
//
// ── What it does NOT own ────────────────────────────────────────────────────
// Smoothing (the app's — it is a presentation choice about ITS noise), the
// number shown as the headline, the drill-down chart, and any fetch. It plots
// the array it is given, once.
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import type { SparkDomain, SparkPoint } from '~/lib/sparkline'
import { computeGeometry, downsample, orderPoints, trendSummary } from '~/lib/sparkline'

const props = withDefaults(defineProps<{
  /** Series, oldest first — order is not trusted, it is sorted. Already numeric.
   *  A `null` is a period with no reading and breaks the line; on a financial
   *  series a real zero is a ZERO, not a gap, and must be passed as `0`. */
  points?: SparkPoint[]
  /** Names what is plotted, for the accessible summary. */
  label: string
  unit?: string | null
  /** Direction of travel. Drives the whole mark's colour — line and fill —
   *  because that IS the message here. `null` renders the neutral tone. */
  direction?: 'up' | 'down' | 'flat' | null
  /**
   * Vertical scale. Defaults to `[0, null]` — floor at zero, top follows the
   * data — because these are counts and currency, non-negative by construction,
   * and "how big is this against nothing" is the honest financial read. Without
   * a floor, orders wobbling 180→210 would fill the box and read as a surge.
   */
  domain?: SparkDomain | null
  /** A target or goal to compare against, drawn as a recessive hairline. */
  referenceLine?: number | null
  /** Fixed height in px. Width is fluid — see `hostWidth`. */
  height?: number
  /** Fallback width before the host has been measured, and on the server. */
  width?: number
  maxMarks?: number
  /** Area under the line. On by default: it is what gives a KPI card's trend its
   *  visual weight at this size, and there is no reference band competing for it. */
  fill?: boolean
  /** Per-reading dots. OFF by default — see the table above: a smoothed daily
   *  series has no discrete events to mark, and dots would claim precision the
   *  smoothing already removed. */
  showMarks?: boolean
  interactive?: boolean
  formatValue?: (value: number) => string
  labelSuffix?: string
}>(), {
  points: () => [],
  unit: null,
  direction: null,
  domain: () => [0, null],
  referenceLine: null,
  height: 32,
  width: 160,
  maxMarks: 60,
  fill: true,
  showMarks: false,
  interactive: false,
  formatValue: undefined,
  labelSuffix: '',
})

const emit = defineEmits<{ select: [] }>()

const PAD = 3

/**
 * FLUID WIDTH, measured from the host.
 *
 * A KPI card lives in a responsive grid — its width changes with the breakpoint
 * and with the viewport, and the mark has always filled it. A fixed pixel width
 * would leave dead space on a wide card and would be the single most visible
 * regression of adopting a shared component. `PharosSparkline` is fixed-width
 * because a table cell is; a card is not.
 *
 * SSR-safe: `width` is the server-rendered fallback, and the observer only ever
 * runs in the browser.
 */
const host = ref<HTMLElement | null>(null)
const hostWidth = ref<number | null>(null)
let observer: ResizeObserver | null = null

onMounted(() => {
  if (!host.value || typeof ResizeObserver === 'undefined') return
  observer = new ResizeObserver((entries) => {
    const w = entries[0]?.contentRect.width
    if (w && w > 0) hostWidth.value = w
  })
  observer.observe(host.value)
})
onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
})

const w = computed(() => Math.max(hostWidth.value ?? props.width, PAD * 2 + 1))

const ordered = computed(() => downsample(orderPoints(props.points), props.maxMarks))
const valued = computed(() => ordered.value.filter(p => p.value !== null).length)
const hasData = computed(() => valued.value >= 2)

const geo = computed(() =>
  computeGeometry(ordered.value, null, w.value, props.height, PAD, {
    domain: props.domain,
    referenceLine: props.referenceLine,
  }),
)

/**
 * The area under each segment, closed to the baseline.
 *
 * One filled path PER SEGMENT, matching the line: a gap must interrupt the fill
 * too, or the shading would bridge a period with no reading and quietly restore
 * the very thing segmentation exists to prevent.
 */
const areas = computed(() => {
  if (!props.fill) return []
  const base = props.height - PAD
  return geo.value.segments.map((d) => {
    const coords = [...d.matchAll(/[ML] ([\d.-]+) ([\d.-]+)/g)]
    if (coords.length < 2) return ''
    const first = coords[0]!
    const last = coords[coords.length - 1]!
    return `${d} L ${last[1]} ${base} L ${first[1]} ${base} Z`
  }).filter(Boolean)
})

const toneClass = computed(() => {
  switch (props.direction) {
    case 'up': return 'tone-up'
    case 'down': return 'tone-down'
    default: return 'tone-flat'
  }
})

const summary = computed(() =>
  trendSummary({
    label: props.label,
    points: ordered.value,
    bounds: null,
    unit: props.unit,
    formatValue: props.formatValue,
    labelSuffix: props.labelSuffix,
  }),
)

const activatable = computed(() => props.interactive && hasData.value)
const spokenLabel = computed(() =>
  activatable.value ? `${summary.value}. Abrir detalle.` : summary.value,
)
</script>

<template>
  <component
    :is="activatable ? 'button' : 'div'"
    :type="activatable ? 'button' : undefined"
    ref="host"
    class="pharos-trendline"
    :class="[toneClass, activatable ? 'is-activatable' : undefined]"
    :style="{ height: `${height}px` }"
    :role="activatable ? undefined : 'img'"
    :aria-label="activatable ? undefined : spokenLabel"
    @click="activatable && emit('select')"
  >
    <svg
      v-if="hasData"
      :width="w"
      :height="height"
      :viewBox="`0 0 ${w} ${height}`"
      :role="activatable ? 'img' : undefined"
      :aria-label="activatable ? spokenLabel : undefined"
      focusable="false"
      preserveAspectRatio="none"
    >
      <line
        v-if="geo.referenceLineY != null"
        x1="0"
        :x2="w"
        :y1="geo.referenceLineY"
        :y2="geo.referenceLineY"
        class="reference-line"
      />

      <path v-for="(d, i) in areas" :key="`a${i}`" :d="d" class="area" />

      <path
        v-for="(d, i) in geo.segments"
        :key="`l${i}`"
        :d="d"
        class="line"
        fill="none"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />

      <!-- Off by default. When a surface does want them, the last one is still
           the one that matters, so it keeps the size distinction. -->
      <template v-if="showMarks">
        <circle
          v-for="(m, i) in geo.points"
          :key="`m${i}`"
          :cx="m.x"
          :cy="m.y"
          :r="m.isLast ? 2.5 : 1.5"
          class="mark"
        />
      </template>
    </svg>

    <span v-else class="empty" :aria-hidden="activatable ? undefined : 'true'">—</span>
  </component>
</template>

<style scoped>
.pharos-trendline {
  display: block;
  position: relative;
  width: 100%;
  /* A grid child refuses to shrink below its content without this, which would
     make the card widen instead of the mark narrowing. */
  min-width: 0;
}

.is-activatable {
  cursor: pointer;
  border-radius: var(--radius-sm, 0.25rem);
}

.is-activatable:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

.tone-up { --tone: var(--trend-up); }
.tone-down { --tone: var(--trend-down); }
.tone-flat { --tone: var(--trend-flat); }

.line {
  stroke: var(--tone);
}

.area {
  fill: var(--tone);
  opacity: 0.12;
  stroke: none;
}

.mark {
  fill: var(--tone);
}

.reference-line {
  stroke: var(--muted-foreground);
  stroke-width: 1;
  opacity: 0.4;
}

.empty {
  color: var(--muted-foreground);
  font-size: 0.75rem;
}
</style>
