<script setup lang="ts">
// The Pháros sparkline — one inline trend mark, used identically on every
// surface that shows a measured series over time: analyte history on the
// release screen, the same analyte on the patient's results portal, positivity
// on an epidemiology report, a KPI on a finance card.
//
// It is CONTEXT for a value, never the value itself. The datum is the number
// beside it; this answers "is it moving, and against what?".
//
// ── Hand-drawn SVG, deliberately, and it is not a style preference ──────────
// The two implementations this replaces used @unovis. It is a good library and
// it stays the standard for real charts (RFC 0008 Q11) — but for a sparkline it
// buys nothing and costs two things. It cannot ship to `public-web` without
// putting a charting bundle on a patient-facing page whose entire design goal
// is calm and fast. And its geometry is UNASSERTABLE in this estate's tests:
// happy-dom has no layout engine, so the scales resolve to 0/NaN and every
// geometric assertion passes vacuously. A shared component whose drawing no
// consumer can verify is worse than four unshared ones. Here the drawing is
// `~/lib/sparkline.ts` — plain functions, pinned by real tests.
//
// ── What this component does NOT own, on purpose ────────────────────────────
// • Parsing. `points[].value` is a `number`. See the module header: owning the
//   parse would standardise a decimal-comma bug across every app at once.
// • Fetching. It plots the array it is given, once. A per-row mount must never
//   trigger a network call — on the release screen there is one of these per
//   analyte per order.
// • Number formatting. It never re-renders a reported value as text.
// • The drill-down dialog. Four consuming apps have four different dialog
//   mechanisms; owning it would drag a dialog dependency into the registry.
//   This emits `select` and the app opens whatever it already has.
// • Clinical policy. Floors, lag windows, maturity cut-offs, denominators and
//   the COBOL "0 means absent" rule are the app's, and they resolve to plain
//   numbers before they reach this boundary.
//
// ── Colour is never the only channel ────────────────────────────────────────
// `status` is OPT-IN and defaults OFF, because the two audiences disagree and
// both are right: the release screen tints the current mark to reinforce a
// judgement the technologist is making, and the patient portal refuses to,
// because a coloured mark on a patient's own result reads as a verdict the
// chart has no standing to deliver. When it IS on, it tints the LAST mark only
// — never the line, never the band — and size + surface ring carry the same
// distinction so it survives without colour. Measured 2026-07-18:
// `--status-warning` and `--status-success` sit ΔE 12.8 apart for normal
// vision, under the 15 floor, so hue alone is not a reliable channel when
// scanning a column of these.
//
// The series uses `--chart-2` and no other chart token. Measured against both
// backgrounds, it is the ONLY one of `--chart-1..5` clearing 3:1 in light AND
// dark (`--chart-1` is 1.68:1 on dark, `--chart-4` is 1.38:1 on light) — the
// chart tokens are declared once and never redefined in `.dark`. Until that is
// fixed in `tokens.css`, a second series colour has nowhere honest to come
// from, so this component draws one series and says so.
import { computed } from 'vue'
import type { SparkBounds, SparkPoint, SparkScale } from '~/lib/sparkline'
import { arrowPath, computeGeometry, downsample, orderPoints, trendSummary } from '~/lib/sparkline'

const props = withDefaults(defineProps<{
  /** Measurement events. Order does not matter — sorted by `at`. */
  points?: SparkPoint[]
  /** Reference range. Drawn as a band and anchors the scale. Omit when the analyte has none. */
  bounds?: SparkBounds | null
  /** `'bounds'` anchors the domain to the range (default, and the safer read on
   *  a clinical screen); `'data'` spans the readings. See `computeDomain`. */
  scale?: SparkScale
  /** Names what is plotted, for the accessible summary. Required — a sparkline
   *  with no text alternative is decoration. */
  label: string
  unit?: string | null
  width?: number
  height?: number
  /** Rendered-mark cap; a longer series is downsampled keeping first and last. */
  maxMarks?: number
  /** Opt-in status tint on the LAST mark only. `null` (default) draws it in the
   *  series colour — the correct choice on any patient-facing surface. */
  status?: 'critical' | 'abnormal' | 'normal' | null
  /** A lone measurement: `'show'` draws the single dot ("measured once" and
   *  "never measured" are different facts and the row should say which);
   *  `'hide'` renders the empty state instead. */
  singlePoint?: 'show' | 'hide'
  /** Makes the mark activatable and emits `select`. Off unless the app has
   *  somewhere to go — offering a click that opens nothing is a worse
   *  affordance than offering none. */
  interactive?: boolean
}>(), {
  points: () => [],
  bounds: null,
  scale: 'bounds',
  unit: null,
  width: 96,
  height: 28,
  maxMarks: 24,
  status: null,
  singlePoint: 'show',
  interactive: false,
})

const emit = defineEmits<{ select: [] }>()

const PAD = 5 // room for the surface ring on the end marker and the arrowhead

const ordered = computed(() => downsample(orderPoints(props.points), props.maxMarks))

const hasData = computed(() =>
  props.singlePoint === 'hide' ? ordered.value.length >= 2 : ordered.value.length >= 1,
)

const geo = computed(() =>
  computeGeometry(ordered.value, props.bounds, props.scale, props.width, props.height, PAD),
)

const summary = computed(() =>
  trendSummary({ label: props.label, points: ordered.value, bounds: props.bounds, unit: props.unit }),
)

const lastMarkClass = computed(() => {
  switch (props.status) {
    case 'critical': return 'mark-critical'
    case 'abnormal': return 'mark-abnormal'
    case 'normal': return 'mark-normal'
    default: return 'mark-series'
  }
})

const activatable = computed(() => props.interactive && hasData.value)

function arrowPathFor(m: { x: number, y: number, censoring: 'below' | 'above' | null }): string {
  return m.censoring ? arrowPath(m.x, m.y, m.censoring) : ''
}
</script>

<template>
  <component
    :is="activatable ? 'button' : 'div'"
    :type="activatable ? 'button' : undefined"
    class="pharos-sparkline"
    :class="activatable ? 'is-activatable' : undefined"
    :style="{ width: `${width}px`, height: `${height}px` }"
    :role="activatable ? undefined : 'img'"
    :aria-label="activatable ? undefined : summary"
    @click="activatable && emit('select')"
  >
    <svg
      v-if="hasData"
      :width="width"
      :height="height"
      :viewBox="`0 0 ${width} ${height}`"
      :role="activatable ? 'img' : undefined"
      :aria-label="activatable ? summary : undefined"
      focusable="false"
    >
      <!-- The reference band. Recessive and NEUTRAL on purpose: it is context,
           not a claim. Tinting it green would assert "this region is good" in a
           chart whose whole job is letting the reader judge that — and would
           spend a reserved status colour on decoration. -->
      <rect
        v-if="geo.band"
        x="0"
        :y="geo.band.y"
        :width="width"
        :height="geo.band.height"
        class="band"
      />

      <path
        v-if="geo.linePath"
        :d="geo.linePath"
        class="line"
        fill="none"
        stroke-width="1.75"
        stroke-linecap="round"
        stroke-linejoin="round"
      />

      <!-- One mark per reading. Lab results are DISCRETE EVENTS, not samples of
           a continuous function: a bare line implies the value passed smoothly
           through every point between draws, which is not what happened.

           A CENSORED reading is an ARROW, not a dot — plotted at the limit of
           measurement, with the arrow saying the true value lies beyond it. It
           is NOT an abnormality flag: same series colour as every other mark,
           because an instrument limit is a data point, not a judgement. -->
      <g v-for="(m, i) in geo.points" :key="i">
        <template v-if="m.censoring">
          <path
            :d="arrowPathFor(m)"
            class="mark-ring"
            :stroke-width="m.isLast ? 5 : 4"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            :d="arrowPathFor(m)"
            class="mark-series"
            :stroke-width="m.isLast ? 2.25 : 1.75"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </template>
        <template v-else>
          <circle :cx="m.x" :cy="m.y" :r="m.isLast ? 3.5 : 2.25" class="mark-ring-fill" />
          <circle
            :cx="m.x"
            :cy="m.y"
            :r="m.isLast ? 3.5 : 2.25"
            :class="m.isLast ? lastMarkClass : 'mark-historical'"
          />
        </template>
      </g>
    </svg>

    <!-- No history is a distinct state, not an empty chart: a blank plot area
         reads as "flat, nothing happening" when the truth is "never measured". -->
    <span v-else class="empty" :aria-hidden="activatable ? undefined : 'true'">—</span>
  </component>
</template>

<style scoped>
.pharos-sparkline {
  display: inline-flex;
  position: relative;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
}

.is-activatable {
  cursor: pointer;
  border-radius: var(--radius-sm, 0.25rem);
}

.is-activatable:hover {
  background-color: var(--accent);
}

.is-activatable:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

.band {
  fill: var(--muted);
}

.line {
  stroke: var(--chart-2);
}

/* Drawn beneath each mark in the surface colour, so a mark stays legible where
   it crosses the band edge or the line. */
.mark-ring-fill {
  fill: var(--background);
}

.mark-ring {
  stroke: var(--background);
}

.mark-series {
  fill: var(--chart-2);
  stroke: var(--chart-2);
}

.mark-historical {
  fill: var(--chart-2);
  opacity: 0.55;
}

.mark-critical {
  fill: var(--status-error);
}

.mark-abnormal {
  fill: var(--status-warning);
}

.mark-normal {
  fill: var(--status-success);
}

.empty {
  color: var(--muted-foreground);
  font-size: 0.75rem;
}
</style>
