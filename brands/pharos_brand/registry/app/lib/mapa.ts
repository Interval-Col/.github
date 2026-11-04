// The pure half of MapaBase: breaks, colour ramp, the accessible table and the MapLibre style.
// Plain functions on plain data — no DOM, no MapLibre instance — so every consumer can pin them
// with real tests (the same reason `sparkline.ts` exists: a map canvas is unassertable in
// happy-dom, the logic behind it is not).
//
// Two rules this file enforces and the component relies on:
// 1. NOTHING EXTERNAL BY DEFAULT. The style references no tile, glyph or sprite URL unless the
//    caller passes one, and the caller passes its OWN origin (RFC 0043 R1/R2). Without a basemap
//    the map is the background token plus the data layers; without glyphs there are no text
//    labels on the canvas — the table companion carries every choropleth figure (R4). Heat and
//    points have no row of their own: a consumer showing figures only through them owes its own
//    text alternative.
// 2. COLOUR COMES FROM TOKENS. The ramp is mixed from the CSS custom properties the app already
//    ships (`--background` → `--chart-2`), read at runtime, so it follows `.dark` and any
//    `.theme-*` with no hex in the component.

export type Lonlat = [number, number]

export interface MapaFeature {
  type: 'Feature'
  id?: string | number
  properties: Record<string, unknown> | null
  geometry: { type: string; coordinates: unknown } | null
}

export interface MapaFeatureCollection {
  type: 'FeatureCollection'
  features: MapaFeature[]
}

export interface FilaTabla {
  id: string
  etiqueta: string
  valor: number | null
}

/** Numeric value of a feature's property, or null when absent or not a finite number. */
export function valorDe(f: MapaFeature, propiedad: string): number | null {
  const v = f.properties?.[propiedad]
  const n = typeof v === 'number' ? v : typeof v === 'string' && v.trim() !== '' ? Number(v) : NaN
  return Number.isFinite(n) ? n : null
}

/** The cleaned value and id `normalizarCoropletas` writes, for the map's paint and click. */
export const PROP_VALOR = '__valor'
export const PROP_ID = '__id'

/**
 * The choropleth's data as the map paints it: each feature carries the SAME value and id the table
 * shows (`valorDe`, and `filasTabla`'s id rule). Without this the two disagree: MapLibre's numeric
 * coercion reads `""` as 0 and paints a suppressed zone as «low» while the table says «—», and
 * a top-level `id` with no `properties.id` selects from its row but not from the map.
 */
export function normalizarCoropletas(fc: MapaFeatureCollection, valor: string): MapaFeatureCollection {
  return {
    type: 'FeatureCollection',
    features: fc.features.map((f, i) => ({
      ...f,
      properties: { ...f.properties, [PROP_VALOR]: valorDe(f, valor), [PROP_ID]: String(f.id ?? f.properties?.id ?? i) },
    })),
  }
}

/**
 * Class breaks for a choropleth: `pasos` classes on a square-root scale between the minimum and
 * the maximum, so one very dense zone does not flatten every other zone into the first class.
 * Returns the `pasos - 1` interior thresholds (ascending, de-duplicated). Empty input → [].
 */
export function cortes(valores: Array<number | null>, pasos = 5): number[] {
  const v = valores.filter((x): x is number => x !== null && Number.isFinite(x) && x >= 0)
  if (v.length === 0 || pasos < 2) return []
  const max = Math.max(...v)
  if (max === 0) return []
  const out: number[] = []
  for (let i = 1; i < pasos; i++) {
    const t = (i / pasos) ** 2 * max
    if (!out.length || t > out[out.length - 1]!) out.push(Number(t.toPrecision(6)))
  }
  return out
}

/** `#rgb`/`#rrggbb`/`rgb(a)(…)` → [r, g, b], or null. Only what getComputedStyle returns. */
export function rgb(color: string): [number, number, number] | null {
  const c = color.trim()
  const hex = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(c)
  if (hex) {
    const h = hex[1]!.length === 3 ? [...hex[1]!].map((x) => x + x).join('') : hex[1]!
    return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)) as [number, number, number]
  }
  const fn = /^rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)/i.exec(c)
  return fn ? [Number(fn[1]), Number(fn[2]), Number(fn[3])] : null
}

/**
 * `pasos` colours from `desde` (the background token) to `hasta` (the series token), linear in RGB.
 * The first step is a visible tint, never the background itself, so a zone with a value is never
 * mistaken for an empty one. Falls back to `hasta` repeated when a colour does not parse.
 */
export function rampa(desde: string, hasta: string, pasos = 5): string[] {
  const a = rgb(desde)
  const b = rgb(hasta)
  if (!a || !b || pasos < 1) return Array.from({ length: Math.max(pasos, 1) }, () => hasta)
  return Array.from({ length: pasos }, (_, i) => {
    const t = (i + 1) / pasos
    const [r, g, bl] = [0, 1, 2].map((k) => Math.round(a[k]! + (b[k]! - a[k]!) * t))
    return `rgb(${r}, ${g}, ${bl})`
  })
}

/** The same colour with alpha `a` (0–1): the transparent end of a ramp keeps its hue, so a
 * heat surface fades out instead of passing through grey. Returns the input when it does not parse. */
export function conAlfa(color: string, a: number): string {
  const c = rgb(color)
  return c ? `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${a})` : color
}

/** The R4 table: one row per feature with a label, sorted by value (desc), nulls last. */
export function filasTabla(fc: MapaFeatureCollection | null | undefined, valor: string, etiqueta: string): FilaTabla[] {
  if (!fc) return []
  return fc.features
    .map((f, i) => ({
      id: String(f.id ?? f.properties?.id ?? i),
      etiqueta: String(f.properties?.[etiqueta] ?? '—'),
      valor: valorDe(f, valor),
    }))
    .sort((x, y) => (y.valor ?? -Infinity) - (x.valor ?? -Infinity) || x.etiqueta.localeCompare(y.etiqueta, 'es'))
}

export interface MapaBaseOrigen {
  /** Same-origin URL of a `.pmtiles` basemap (e.g. `/analitica/api/mapa/base.pmtiles`). */
  url: string
  /** Same-origin glyphs template, `…/{fontstack}/{range}.pbf`. Without it: no text labels. */
  glyphs?: string
  /** Same-origin sprite base URL. Without it: no icons. */
  sprite?: string
}

/**
 * True when a URL leaves the page's origin. Decided by the URL parser, the same one the browser
 * fetches with, and never by a pattern: the parser reads a backslash as a slash in http(s), so
 * `https:\\\\host/x` and `/\\host/x` leave the origin while looking relative to a regex. Without
 * `origenApp` (the page's `location.origin`), only what resolves against the page counts as its own.
 * A URL that cannot be parsed counts as external.
 */
export function esExterna(url: string | undefined, origenApp?: string): boolean {
  if (!url) return false
  const base = (origenApp || 'https://origen-propio.invalid').replace(/\/+$/, '')
  try {
    return new URL(url.trim(), `${base}/`).origin !== new URL(base).origin
  } catch {
    return true
  }
}

/**
 * The MapLibre style. `capasBase` are the basemap layers (from `@protomaps/basemaps`, computed by
 * the component only when a basemap is given). Refuses an external basemap, glyphs or sprite URL:
 * RFC 0043 R2 — the basemap is self-served — and the org frontend standard (no third-party asset
 * at runtime). Throws instead of silently loading it.
 */
export function estilo(opts: {
  fondo: string
  origen?: MapaBaseOrigen | null
  capasBase?: unknown[]
  /** The page's origin (`location.origin`): absolute URLs under it are the app's own. */
  origenApp?: string
}): Record<string, unknown> {
  const o = opts.origen ?? null
  for (const [nombre, u] of [['url', o?.url], ['glyphs', o?.glyphs], ['sprite', o?.sprite]] as const) {
    if (esExterna(u, opts.origenApp)) {
      throw new Error(`MapaBase: «${nombre}» apunta fuera del origen de la app (RFC 0043 R2): ${u}`)
    }
  }
  const s: Record<string, unknown> = {
    version: 8,
    sources: o ? { base: { type: 'vector', url: `pmtiles://${o.url}` } } : {},
    layers: [{ id: 'fondo', type: 'background', paint: { 'background-color': opts.fondo } }, ...(o ? opts.capasBase ?? [] : [])],
  }
  if (o?.glyphs) s.glyphs = o.glyphs
  if (o?.sprite) s.sprite = o.sprite
  return s
}

/** MapLibre `step` expression for a choropleth fill, from breaks and colours. Null values → transparent. */
export function expresionRelleno(propiedad: string, cortesV: number[], colores: string[]): unknown[] {
  const nulo = ['==', ['typeof', ['get', propiedad]], 'null']
  // Without breaks (no values, or all at zero) a `step` with no stops is invalid, and MapLibre rejects the layer.
  if (!cortesV.length) return ['case', nulo, 'rgba(0,0,0,0)', colores[0]]
  const paso: unknown[] = ['step', ['to-number', ['get', propiedad], 0], colores[0]]  // lint-allow-token: MapLibre paint/layout key, not a CSS class
  cortesV.forEach((c, i) => paso.push(c, colores[Math.min(i + 1, colores.length - 1)]))
  return ['case', nulo, 'rgba(0,0,0,0)', paso]
}

/** A map view's bounds, `[[west, south], [east, north]]`. */
export type Limites = [Lonlat, Lonlat]

/** The bounds of a collection's geometry, for `encuadre`. Null when it has no coordinates to fit. */
export function limitesDe(fc: MapaFeatureCollection | null | undefined): Limites | null {
  let [oeste, sur, este, norte] = [Infinity, Infinity, -Infinity, -Infinity]
  const visitar = (c: unknown): void => {
    if (!Array.isArray(c)) return
    if (typeof c[0] === 'number' && typeof c[1] === 'number') {
      oeste = Math.min(oeste, c[0])
      este = Math.max(este, c[0])
      sur = Math.min(sur, c[1])
      norte = Math.max(norte, c[1])
      return
    }
    c.forEach(visitar)
  }
  for (const f of fc?.features ?? []) visitar((f.geometry as { coordinates?: unknown } | null)?.coordinates)
  return oeste === Infinity ? null : [[oeste, sur], [este, norte]]
}
