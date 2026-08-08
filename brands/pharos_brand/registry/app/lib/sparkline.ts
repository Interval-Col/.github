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

/** One point in the series. `at` orders it; `value` is already numeric. */
export interface SparkPoint {
  /** Any Date-parseable stamp, or a raw epoch. Used ONLY for ordering. */
  at: string | number
  /**
   * The measured value — or `null` for a GAP: a period that was never read.
   *
   * `null` is not "zero" and not "missing from the array". It is a positive
   * assertion that this position in the series exists and has no reading, and
   * it BREAKS THE LINE: no mark is drawn, and the segments on either side are
   * not joined.
   *
   * This exists because the alternative shipped to production. A positivity
   * chart drew a flat line pinned to 0% across nine months that had never been
   * read, while the table two centimetres below it printed "—" for those same
   * periods. "Not read yet" rendered as "did not grow", on the screen that
   * exists to catch exactly that. Dropping the point instead of representing it
   * is the same lie by a different route: the line simply joins across the void.
   *
   * A non-finite NUMBER (`NaN`, `Infinity`) is a different thing — an
   * unparseable or invalid reading, not a declared gap — and is dropped by
   * `orderPoints`. Only an explicit `null` means "no reading here".
   */
  value: number | null
  /**
   * Set when the instrument reported a LIMIT rather than a measurement
   * (`<0.5`, `>100`). `value` is then the limit itself and the true value lies
   * beyond it, in this direction.
   */
  censoring?: 'below' | 'above' | null
}

/** A point that carries a reading — the narrowed form the geometry works in. */
type ValuedPoint = SparkPoint & { value: number }

const hasValue = (p: SparkPoint): p is ValuedPoint =>
  p.value !== null && Number.isFinite(p.value)

/** The analyte's reference range. Drawn as a band; anchors or widens the scale. */
export interface SparkBounds { low: number, high: number }

/**
 * An EXPLICIT vertical scale, overriding the computed one. `null` in a slot
 * leaves that end automatic.
 *
 * This exists because "the scale" and "the reference range" are two different
 * facts, and `bounds` conflates them. A positivity series is a percentage: 0 and
 * 100 are the natural limits of the quantity, not a range against which a
 * reading is judged. Passing them as `bounds` produced three wrong things at
 * once — the domain came back padded to −10…110 (meaningless for a percentage),
 * a `--muted` band covered 54% of the box, and the spoken sentence announced a
 * "rango de referencia 0–100 %" that nobody would ever be measured against.
 *
 * So: `domain` sets the scale and draws nothing; `bounds` draws a band and
 * anchors the scale. A surface can use either, both, or neither.
 *
 * An explicit end is used VERBATIM — never padded. A declared scale is a
 * statement about the quantity, and widening it would silently contradict that.
 * `[0, null]` is the common half-open case: floor at zero, let the top follow
 * the data.
 */
export type SparkDomain = [number | null, number | null]

export interface SparkGeometry {
  domain: [number, number]
  /** Only the points that carry a reading. Gaps produce no mark. */
  points: Array<{ x: number, y: number, value: number, censoring: 'below' | 'above' | null, isLast: boolean }>
  /**
   * ONE PATH PER CONTIGUOUS RUN of value-bearing points — never one path for
   * the whole series.
   *
   * The shape of the data is the guard, not a rendering flag. A gap simply ends
   * a segment, so there is nothing to interpolate across and no library
   * behaviour to argue with. A run of a single point yields no path at all: one
   * reading has nothing to connect, and its mark alone is the honest render.
   */
  segments: string[]
  /** Band rect in chart space, or null when there is no drawable range. */
  band: { y: number, height: number } | null
  /**
   * y of the single-value reference line, or null when none was asked for or it
   * falls outside the scale.
   *
   * A LINE, not a band, and the distinction is the point: a band says "anywhere
   * in here is the expected region", a line says "this one value is the thing to
   * compare against" — a target, a goal, the series' own long-run rate. Drawing
   * one as the other asserts something the data does not support.
   */
  referenceLineY: number | null
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
    // An unparseable stamp has no honest position, and a non-finite NUMBER is an
    // invalid reading — both go. An explicit `null` STAYS: it is a declared gap
    // and dropping it would let the line join across it.
    .filter(({ p, t }) => Number.isFinite(t) && (p.value === null || Number.isFinite(p.value)))
    .sort((a, b) => a.t - b.t)
    .map(({ p }) => p)
}

/**
 * Evenly-spaced index downsample that always keeps the first and last
 * value-bearing point. A no-op below the cap. Never mutates the input.
 *
 * ⚠️ GAPS ARE NEVER DROPPED, and the cap yields to that. Sampling that removed
 * a gap would rejoin the line across it — reintroducing, at the last step of
 * the pipeline, exactly the defect gap representation exists to prevent. So the
 * sampling budget is spent on value-bearing points and every gap survives; a
 * gap-heavy series can therefore come back slightly longer than `cap`.
 *
 * A caller that aggregates rather than samples (pooling buckets, recomputing a
 * rate per group) must do that BEFORE calling in, and hand over an array
 * already at or under `cap` so this is a guaranteed passthrough — index
 * sampling would otherwise discard real observations and could erase a genuine
 * spike.
 */
export function downsample(points: readonly SparkPoint[], cap: number): SparkPoint[] {
  if (cap <= 0) return []
  if (points.length <= cap) return [...points]

  const valuedIdx: number[] = []
  const gapIdx: number[] = []
  points.forEach((p, i) => (hasValue(p) ? valuedIdx : gapIdx).push(i))

  if (valuedIdx.length === 0) return [...points]

  const budget = Math.max(1, cap - gapIdx.length)
  const keep = new Set<number>(gapIdx)

  if (budget === 1 || valuedIdx.length <= budget) {
    if (valuedIdx.length <= budget) valuedIdx.forEach(i => keep.add(i))
    else keep.add(valuedIdx[valuedIdx.length - 1]!)
  } else {
    const step = (valuedIdx.length - 1) / (budget - 1)
    for (let k = 0; k < budget; k++) keep.add(valuedIdx[Math.round(k * step)]!)
  }

  return points.filter((_, i) => keep.has(i))
}

/**
 * The vertical domain — the one clinically load-bearing choice in a sparkline,
 * and DELIBERATELY NOT CONFIGURABLE.
 *
 * The rule: a valid reference range ANCHORS the scale, widened only to contain
 * real excursions. With no range, the domain falls back to the data's own
 * spread, because relative shape is then all the data can honestly support.
 *
 * There is no autoscale knob, and its absence is the point. Autoscaling to the
 * series' own spread makes any wobble fill the box: VCM 88→91→90, entirely
 * inside an 80–100 range, renders as a dramatic climb. On a screen where
 * someone decides whether a result is safe to authorise, that chart lies.
 * Anchored, the same drift is a flat line inside the band and a genuine
 * excursion visibly breaks out of it — the eye reads inside/outside first and
 * trend second.
 *
 * Both consuming apps independently arrived at anchoring and each wrote down
 * the same reasoning (`AnalyteSparkline.vue`, `microPositividad.ts` — the
 * latter for positivity, where "20→23→21% autoescalada se lee como un
 * acantilado epidemiológico"). No real surface wants "I have a range and I
 * choose to ignore it", so offering that as a prop only left the misleading
 * chart one keystroke away.
 *
 * A FLAT series is a real and common result. It gets a symmetric window rather
 * than a zero-height domain, so it renders as the flat line it is instead of
 * dividing by zero — which is precisely how the legacy component erased trends.
 */
export function computeDomain(
  points: readonly SparkPoint[],
  bounds: SparkBounds | null,
  domain?: SparkDomain | null,
): [number, number] {
  // Gaps carry no value and must not pull the domain — a `null` treated as 0
  // would drag the floor down and flatten every real reading against it.
  const values = points.filter(hasValue).map(p => p.value)
  let lo = values.length ? Math.min(...values) : 0
  let hi = values.length ? Math.max(...values) : 1

  if (bounds && bounds.high > bounds.low) {
    lo = Math.min(lo, bounds.low)
    hi = Math.max(hi, bounds.high)
  }

  if (hi === lo) {
    const pad = Math.abs(hi) * 0.1 || 1
    return [lo - pad, hi + pad]
  }

  // Headroom only where a censored arrow actually needs to point.
  const span = hi - lo
  const needsLow = points.some(p => hasValue(p) && p.censoring === 'below')
  const needsHigh = points.some(p => hasValue(p) && p.censoring === 'above')
  const pad = span * 0.1
  return applyExplicitDomain(
    [
      lo - pad - (needsLow ? span * ARROW_HEADROOM : 0),
      hi + pad + (needsHigh ? span * ARROW_HEADROOM : 0),
    ],
    domain,
  )
}

/**
 * An explicitly declared end replaces the computed one, VERBATIM — no padding,
 * no headroom. Declaring a scale is a statement about the quantity; widening it
 * would silently contradict the statement.
 *
 * A declaration that inverts or flattens the scale is ignored rather than
 * obeyed: a zero-or-negative span divides by zero downstream and would erase the
 * series, which is worse than quietly falling back to the computed scale.
 */
function applyExplicitDomain(auto: [number, number], domain?: SparkDomain | null): [number, number] {
  if (!domain) return auto
  const lo = domain[0] != null && Number.isFinite(domain[0]) ? domain[0] : auto[0]
  const hi = domain[1] != null && Number.isFinite(domain[1]) ? domain[1] : auto[1]
  return hi > lo ? [lo, hi] : auto
}

/**
 * Full drawing geometry in one pass, so a censored point cannot be drawn as a
 * dot by one branch of a template and as an arrow by another.
 */
export function computeGeometry(
  points: readonly SparkPoint[],
  bounds: SparkBounds | null,
  width: number,
  height: number,
  pad: number,
  opts?: { domain?: SparkDomain | null, referenceLine?: number | null },
): SparkGeometry {
  const domain = computeDomain(points, bounds, opts?.domain)
  const [lo, hi] = domain
  const span = hi - lo

  // ORDINAL x spacing — every reading gets equal width, regardless of the gap
  // between draws. A deliberate limit, not an oversight.
  //
  // Time-proportional spacing would make the slope encode rate of change, which
  // is more information — but in a 96px inline mark it degenerates: three
  // readings from this week plus one from five years ago collapse the recent
  // three into two pixels, and the mark stops answering anything at all.
  //
  // So the division of labour is: THIS answers "is it moving, and where does it
  // sit against the range" — sequence and level. The drill-down chart, which has
  // room for a real time axis, answers "how fast". The elapsed span is stated in
  // `trendSummary()` so the time context is said out loud rather than implied by
  // a slope that does not carry it.
  const n = points.length - 1
  const x = (i: number) => (n <= 0 ? width / 2 : pad + (i / n) * (width - pad * 2))
  const y = (v: number) => pad + (1 - (v - lo) / span) * (height - pad * 2)

  // A gap OCCUPIES ITS SLOT on the x axis — it is skipped as a mark, never as a
  // position. Compacting the array first would slide the later readings
  // leftward and silently shorten the period the chart claims to cover.
  //
  // `isLast` is the last point WITH A VALUE, not the last array entry. With
  // gaps representable, a series can end in one — and the emphasised mark is
  // the "latest reading", so anchoring it to the array's end would put the
  // large dot in the void.
  const lastValuedIndex = (() => {
    for (let i = points.length - 1; i >= 0; i--) if (hasValue(points[i]!)) return i
    return -1
  })()

  const marks: SparkGeometry['points'] = []
  const segments: string[] = []
  let run: string[] = []

  points.forEach((p, i) => {
    if (!hasValue(p)) {
      // The gap ends the current run. Two or more points make a drawable
      // segment; a lone reading is carried by its mark alone.
      if (run.length > 1) segments.push(run.join(' '))
      run = []
      return
    }
    const px = x(i)
    const py = y(p.value)
    marks.push({
      x: px,
      y: py,
      value: p.value,
      censoring: p.censoring ?? null,
      isLast: i === lastValuedIndex,
    })
    run.push(`${run.length === 0 ? 'M' : 'L'} ${px.toFixed(2)} ${py.toFixed(2)}`)
  })
  if (run.length > 1) segments.push(run.join(' '))

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

  // Clamped OUT rather than clamped IN: a reference that falls off the declared
  // scale is not drawn at all. Pinning it to the edge would put a line where no
  // line belongs and invite reading it as "just at the limit".
  const ref = opts?.referenceLine
  const referenceLineY = ref != null && Number.isFinite(ref) && ref >= lo && ref <= hi
    ? y(ref)
    : null

  return { domain, points: marks, segments, band, referenceLineY }
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
  /** The declared scale, when there is one. Named in the sentence because it is
   *  part of what the picture encodes: "flat at 20%" and "flat at 0%" look
   *  identical without knowing the scale is pinned to 0–100. */
  domain?: SparkDomain | null
  unit?: string | null
  /**
   * How a value becomes text IN THE SPOKEN SENTENCE. Defaults to `String`,
   * which prints a POINT decimal separator.
   *
   * That default is wrong for every Colombian clinical surface in this estate
   * and the prop exists because the demo caught it: the screen showed
   * "13,9 g/dL" while the screen reader announced "13.9 g/dL" — the same
   * mismatched separator that already corrupted a reported result here once.
   * The component refuses to own formatting (see the module header), so the
   * app passes the SAME formatter it uses for the value printed beside the
   * chart, and the two can never drift apart.
   */
  formatValue?: (value: number) => string
  /**
   * App-owned facts appended to the sentence.
   *
   * The standard can describe the SHAPE it drew — how many readings, over what
   * span, where they sit against a range. It cannot know what the surface means:
   * that this hairline is the exam's own long-run positivity, that the series is
   * suppressed because the volume floor was not met, what the number represents.
   * Those are the app's, and without a way to say them the spoken label is
   * strictly poorer than the picture. Kept as a plain string because the standard
   * has no business parsing domain prose.
   */
  labelSuffix?: string
}): string {
  const { label, bounds, unit } = input
  const fmt = input.formatValue ?? String

  // Counts and the "latest value" are over READINGS ONLY. A gap is a period
  // with no reading; counting it would announce measurements that never
  // happened, and reading "the last value" off it would announce nothing at
  // all. The gaps are named separately, at the end, as their own fact.
  const points = input.points.filter(hasValue)
  const gaps = input.points.length - points.length
  if (!points.length) {
    const extra = input.labelSuffix?.trim() ? `. ${input.labelSuffix.trim().replace(/\.$/, '')}` : ''
    return `${label}: sin mediciones previas${extra}`
  }

  const u = unit ? ` ${unit}` : ''
  const n = points.length
  const last = points[n - 1]!
  const first = points[0]!

  // The elapsed span, said out loud. The mark itself spaces readings ORDINALLY
  // (see computeGeometry), so its slope carries direction but not rate — and a
  // reader who cannot see the mark at all would otherwise get even less. Six
  // readings over six months and six over six years are different clinical
  // pictures; naming the span is what keeps the sentence from implying the
  // wrong one.
  const count = n === 1 ? '1 medición' : `${n} mediciones`
  const spanText = n > 1 ? ` a lo largo de ${elapsedText(first.at, last.at)}` : ''

  const latest = last.censoring
    ? `último valor ${last.censoring === 'below' ? 'menor que' : 'mayor que'} ${fmt(last.value)}${u}`
    : `último valor ${fmt(last.value)}${u}`

  let movement = ''
  if (n > 1 && !last.censoring && !first.censoring) {
    if (last.value > first.value) movement = ', en ascenso'
    else if (last.value < first.value) movement = ', en descenso'
    else movement = ', sin cambio'
  }

  // A reference RANGE and a declared SCALE are different facts, and the sentence
  // says whichever it actually has. A fixed scale is not a range to be judged
  // against — but staying silent about it loses what a sighted reader gets for
  // free from the box: "plana en 20%" and "plana en 0%" are the same picture
  // until you know the scale is pinned.
  const d = input.domain
  const scaleFixed = d && d[0] != null && d[1] != null && d[1] > d[0]
  const range = bounds && bounds.high > bounds.low
    ? `, rango de referencia ${fmt(bounds.low)}–${fmt(bounds.high)}${u}`
    : scaleFixed
      ? `, escala fija ${fmt(d![0]!)} a ${fmt(d![1]!)}${u}`
      : ', sin rango de referencia'

  const censored = points.filter(p => p.censoring).length
  const censoredNote = censored
    ? `. ${censored === 1 ? '1 lectura está' : `${censored} lecturas están`} fuera del límite de medición`
    : ''

  // Said out loud, because it is the fact the broken line encodes visually — and
  // a reader who cannot see the break would otherwise be told a continuous
  // trend that does not exist.
  const gapNote = gaps
    ? `. ${gaps === 1 ? '1 periodo sin lectura' : `${gaps} periodos sin lectura`}, la línea se parte ahí`
    : ''

  const extra = input.labelSuffix?.trim() ? `. ${input.labelSuffix.trim().replace(/\.$/, '')}` : ''
  return `${label}: ${count}${spanText}, ${latest}${movement}${range}${censoredNote}${gapNote}${extra}`
}

/**
 * Elapsed time between two stamps, in the coarsest unit that still says
 * something useful. Prose, not a date — no locale, no separator, nothing that
 * can drift from what the screen shows.
 */
function elapsedText(from: string | number, to: string | number): string {
  const a = typeof from === 'number' ? from : Date.parse(String(from))
  const b = typeof to === 'number' ? to : Date.parse(String(to))
  if (!Number.isFinite(a) || !Number.isFinite(b)) return 'un periodo desconocido'

  const days = Math.round(Math.abs(b - a) / 86_400_000)
  if (days < 1) return 'el mismo día'
  if (days === 1) return '1 día'
  if (days < 45) return `${days} días`

  const months = Math.round(days / 30.44)
  if (months < 24) return months === 1 ? '1 mes' : `${months} meses`

  const years = Math.round(days / 365.25)
  return years === 1 ? '1 año' : `${years} años`
}
