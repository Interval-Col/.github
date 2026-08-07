// Pure geometry + prose for `PharosSparkline.vue`. No Vue, no DOM, no SVG —
// every function here is a plain input→output map, so a unit test can pin the
// behaviour that actually matters clinically without mounting anything.
//
// WHY THIS MODULE EXISTS SEPARATELY, and it is the load-bearing reason the
// estate standardises on hand-drawn SVG rather than a charting library: the
// two @unovis sparklines this replaces have geometry that CANNOT be asserted
// in this estate's test runner. happy-dom has no layout engine, so @unovis's
// scales resolve to 0/NaN and every geometric assertion is vacuous. A shared
// component whose drawing no consumer can verify is worse than four unshared
// ones. Here the drawing IS these functions, and they are testable.
//
// ── The rule this module enforces above all others ──────────────────────────
// VALUES ARRIVE ALREADY PARSED. `SparkPoint.value` is a `number`, never a
// string. Nothing in this file calls Number(), parseFloat() or toFixed().
//
// That is not fastidiousness. Both string-parsing sparklines in this estate
// are wrong in opposite directions: the legacy release screen does
// `parseFloat('12,5') === 12` and PLOTS THE TRUNCATED VALUE as fact, and the
// modern one does `Number('12,5') === NaN` and SILENTLY DROPS the point while
// its aria-label goes on to announce a measurement count that no longer
// matches what was drawn. A Colombian lab reports decimal commas. Owning the
// parse here would standardise one of those bugs across every app at once, so
// the boundary is drawn before it: the app parses, in its own locale, against
// its own wire contract, and hands over numbers.

/** One measurement event. `at` orders the series; `value` is already numeric. */
export interface SparkPoint {
  /** Any Date-parseable stamp, or a raw epoch. Used ONLY for ordering. */
  at: string | number
  value: number
  /**
   * Set when the instrument reported a LIMIT rather than a measurement
   * (`<0.5`, `>100`). `value` is then the limit itself and the true value lies
   * beyond it, in this direction.
   */
  censoring?: 'below' | 'above' | null
}

/** The analyte's reference range. Drawn as a band; anchors or widens the scale. */
export interface SparkBounds { low: number, high: number }

export type SparkScale
  /** Domain anchored to `bounds`, widened only to contain excursions. */
  = 'bounds'
  /** Domain spans the data, widened to keep `bounds` on canvas. */
  | 'data'

export interface SparkGeometry {
  domain: [number, number]
  points: Array<{ x: number, y: number, value: number, censoring: 'below' | 'above' | null, isLast: boolean }>
  linePath: string
  /** Band rect in chart space, or null when there is no drawable range. */
  band: { y: number, height: number } | null
}

/** Fraction of the domain reserved so a censored arrowhead is never clipped. */
const ARROW_HEADROOM = 0.12

/**
 * Chronological order by PARSED STAMP, not array index.
 *
 * The legacy sparkline plotted by index and would silently mis-order the trend
 * whenever the upstream response was not already ascending — a chart that reads
 * as a fall when the truth is a rise. Backends here do sort server-side; this
 * is defence in depth, and it costs one comparison.
 *
 * Points that are non-finite, or whose stamp will not parse, are dropped: there
 * is no honest place to draw them.
 */
export function orderPoints(points: readonly SparkPoint[]): SparkPoint[] {
  return points
    .map(p => ({ p, t: typeof p.at === 'number' ? p.at : Date.parse(String(p.at)) }))
    .filter(({ p, t }) => Number.isFinite(t) && Number.isFinite(p.value))
    .sort((a, b) => a.t - b.t)
    .map(({ p }) => p)
}

/**
 * Evenly-spaced index downsample that ALWAYS keeps the first and last point.
 * A no-op below the cap. Never mutates the input.
 */
export function downsample<T>(points: readonly T[], cap: number): T[] {
  if (cap <= 0) return []
  if (points.length <= cap) return [...points]
  if (cap === 1) return [points[points.length - 1]!]
  const step = (points.length - 1) / (cap - 1)
  const out: T[] = []
  for (let i = 0; i < cap; i++) out.push(points[Math.round(i * step)]!)
  return out
}

/**
 * The vertical domain — the one clinically load-bearing choice in a sparkline.
 *
 * `'bounds'` anchors the scale to the reference range and widens it only for
 * real excursions. Autoscaling to the series' own spread makes any wobble fill
 * the box: VCM 88→91→90, entirely inside an 80–100 range, renders as a dramatic
 * climb. On a screen where someone decides whether a result is safe to
 * authorise, that chart lies. Anchored, the same drift is a flat line inside the
 * band and a genuine excursion visibly breaks out of it — the eye reads
 * inside/outside first and trend second.
 *
 * `'data'` spans the readings and widens to keep the band on canvas. Correct
 * when the shape itself is the message and every reading may sit far outside the
 * range — scaling to the data alone would push the band off-canvas exactly when
 * it matters most.
 *
 * With no bounds, both degrade to the data's own range: relative shape is all
 * the data can honestly support.
 *
 * A FLAT series is a real and common result. It gets a symmetric window rather
 * than a zero-height domain, so it renders as the flat line it is instead of
 * dividing by zero — which is precisely how the legacy component erased trends.
 */
export function computeDomain(
  points: readonly SparkPoint[],
  bounds: SparkBounds | null,
  scale: SparkScale,
): [number, number] {
  const values = points.map(p => p.value)
  let lo = values.length ? Math.min(...values) : 0
  let hi = values.length ? Math.max(...values) : 1

  if (bounds && bounds.high > bounds.low) {
    if (scale === 'bounds') {
      lo = Math.min(lo, bounds.low)
      hi = Math.max(hi, bounds.high)
    }
    else {
      lo = Math.min(lo, bounds.low)
      hi = Math.max(hi, bounds.high)
    }
  }

  if (hi === lo) {
    const pad = Math.abs(hi) * 0.1 || 1
    return [lo - pad, hi + pad]
  }

  // Headroom only where a censored arrow actually needs to point.
  const span = hi - lo
  const needsLow = points.some(p => p.censoring === 'below')
  const needsHigh = points.some(p => p.censoring === 'above')
  const pad = span * 0.1
  return [
    lo - pad - (needsLow ? span * ARROW_HEADROOM : 0),
    hi + pad + (needsHigh ? span * ARROW_HEADROOM : 0),
  ]
}

/**
 * Full drawing geometry in one pass, so a censored point cannot be drawn as a
 * dot by one branch of a template and as an arrow by another.
 */
export function computeGeometry(
  points: readonly SparkPoint[],
  bounds: SparkBounds | null,
  scale: SparkScale,
  width: number,
  height: number,
  pad: number,
): SparkGeometry {
  const domain = computeDomain(points, bounds, scale)
  const [lo, hi] = domain
  const span = hi - lo

  const n = points.length - 1
  const x = (i: number) => (n <= 0 ? width / 2 : pad + (i / n) * (width - pad * 2))
  const y = (v: number) => pad + (1 - (v - lo) / span) * (height - pad * 2)

  const marks = points.map((p, i) => ({
    x: x(i),
    y: y(p.value),
    value: p.value,
    censoring: p.censoring ?? null,
    isLast: i === points.length - 1,
  }))

  const linePath = marks.length > 1
    ? marks.map((m, i) => `${i === 0 ? 'M' : 'L'} ${m.x.toFixed(2)} ${m.y.toFixed(2)}`).join(' ')
    : ''

  // `high > low` guard AND min/abs on the rect: an inverted or degenerate range
  // must produce no band, never a negative-height rect. One of the four
  // implementations this replaces omitted the min/abs and was one bad reference
  // row away from a rendering error.
  let band: SparkGeometry['band'] = null
  if (bounds && bounds.high > bounds.low) {
    const top = y(bounds.high)
    const bottom = y(bounds.low)
    band = { y: Math.min(top, bottom), height: Math.abs(bottom - top) }
  }

  return { domain, points: marks, linePath, band }
}

/**
 * The censored mark: a stem with an arrowhead pointing where the true value is.
 *
 * A `<path>`, never a `↓` text glyph — at this size a missing font glyph
 * degrades to a tofu box, which reads as an error rather than as a mark. The
 * stem points AWAY from the plotted point: the point is the limit, the direction
 * is where we cannot see.
 */
export function arrowPath(cx: number, cy: number, censoring: 'below' | 'above'): string {
  const sign = censoring === 'below' ? 1 : -1
  const tip = cy + sign * 7
  const head = cy + sign * 3
  return `M ${cx} ${cy - sign * 2} L ${cx} ${tip} M ${cx - 3} ${head} L ${cx} ${tip} L ${cx + 3} ${head}`
}

/**
 * The text alternative — the same facts a sighted reader takes from the shape.
 *
 * Always rendered, never gated behind the graphic. A sparkline with no summary
 * is decoration to a screen-reader user, and on a patient-facing surface that
 * audience is larger than on a staff tool. Censored readings are named, because
 * an arrow whose meaning lives only in its shape is not an accessible encoding.
 *
 * Kept as a pure function precisely so a test can pin the sentence. Spanish,
 * because every consuming surface in this estate is Spanish.
 */
export function trendSummary(input: {
  label: string
  points: readonly SparkPoint[]
  bounds: SparkBounds | null
  unit?: string | null
}): string {
  const { label, points, bounds, unit } = input
  if (!points.length) return `${label}: sin mediciones previas`

  const u = unit ? ` ${unit}` : ''
  const n = points.length
  const count = n === 1 ? '1 medición' : `${n} mediciones`
  const last = points[n - 1]!
  const first = points[0]!

  const latest = last.censoring
    ? `último valor ${last.censoring === 'below' ? 'menor que' : 'mayor que'} ${last.value}${u}`
    : `último valor ${last.value}${u}`

  let movement = ''
  if (n > 1 && !last.censoring && !first.censoring) {
    if (last.value > first.value) movement = ', en ascenso'
    else if (last.value < first.value) movement = ', en descenso'
    else movement = ', sin cambio'
  }

  const range = bounds && bounds.high > bounds.low
    ? `, rango de referencia ${bounds.low}–${bounds.high}${u}`
    : ', sin rango de referencia'

  const censored = points.filter(p => p.censoring).length
  const censoredNote = censored
    ? `. ${censored === 1 ? '1 lectura está' : `${censored} lecturas están`} fuera del límite de medición`
    : ''

  return `${label}: ${count}, ${latest}${movement}${range}${censoredNote}`
}
