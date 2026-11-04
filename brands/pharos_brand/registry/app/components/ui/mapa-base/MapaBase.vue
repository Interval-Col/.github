<script setup lang="ts">
// MapaBase — the ONE map renderer of the Pháros apps (RFC 0043 R1). MapLibre GL JS 6 from npm,
// bundled by the app's build: no CDN, no third-party tile, style, glyph or sprite (R2).
//
// ── What it draws ─────────────────────────────────────────────────────────────
// • The background token, and — only when `origen` is given — a self-served PMTiles basemap
//   (`@protomaps/basemaps` layers, light or dark by the `.dark` class). Every URL in `origen`
//   must be the app's own origin; an external one throws (lib/mapa.ts `estilo`).
// • Data layers, aggregates only (R4): `coropletas` (polygons coloured by a number), `calor`
//   (a density surface over weighted points) and `puntos` (marked places).
// • ALWAYS a table with the same figures as the choropleth (R4, accessibility). It is in the DOM
//   in both views; the «Tabla» toggle only makes it visible.
//
// ── What it does NOT own, on purpose ──────────────────────────────────────────
// • Fetching. It draws the collections it is given; the app's backend serves them (RFC 0013).
// • Suppression and rounding. A figure that reaches this component is already publishable.
// • Number semantics. `formato` turns a value into text; the default is plain `es-CO`.
//
// ── Colour ────────────────────────────────────────────────────────────────────
// Read from the tokens at runtime (`--background`, `--chart-2`, `--border`, `--primary`,
// `--foreground`), so it follows `.dark` and any `.theme-*` with no hex here. A MutationObserver
// on <html class> re-applies the style when the theme flips.
import 'maplibre-gl/dist/maplibre-gl.css'
// MapLibre 6 starts its worker from a URL relative to its own module, and a bundler that
// pre-bundles the package (Vite's optimizeDeps) moves the module and breaks that URL: the canvas
// appears and nothing is ever drawn («Worker failed to load»). `?worker&url` makes the app's build
// bundle the worker (with its shared chunk) and hand back its URL, so no consuming app has to
// touch its Vite config.
import urlTrabajador from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { PROP_ID, PROP_VALOR, conAlfa, cortes, estilo, expresionRelleno, filasTabla, normalizarCoropletas, rampa, valorDe } from '@/lib/mapa'
import type { CapaCalor, CapaCoropletas, CapaPuntos, Limites, Lonlat, MapaBaseOrigen } from './types'

const props = withDefaults(defineProps<{
  /** Accessible name of the map (required: a map without a name is a blank box to a screen reader). */
  etiqueta: string
  centro?: Lonlat
  zoom?: number
  /** Self-served basemap. Omit it and the map is the background token plus the data layers. */
  origen?: MapaBaseOrigen | null
  /** Font stack for labels; must exist under `origen.glyphs`. */
  fuente?: string
  coropletas?: CapaCoropletas | null
  calor?: CapaCalor | null
  puntos?: CapaPuntos | null
  /** The view to fit. From bounds back to null, the map returns to `centro` and `zoom`. */
  encuadre?: Limites | null
  /** The id of the zone to outline. */
  resaltado?: string | null
  /** Header of the value column in the table companion. */
  nombreValor?: string
  formato?: (v: number) => string
}>(), {
  centro: () => [-75.57, 6.24],
  zoom: 11,
  origen: null,
  fuente: 'Noto Sans Regular',
  coropletas: null,
  calor: null,
  puntos: null,
  encuadre: null,
  resaltado: null,
  nombreValor: 'Valor',
  formato: (v: number) => new Intl.NumberFormat('es-CO', { maximumFractionDigits: 1 }).format(v),
})

const emit = defineEmits<{ seleccionar: [id: string] }>()

const contenedor = ref<HTMLDivElement | null>(null)
const vista = ref<'mapa' | 'tabla'>('mapa')
const error = ref<string | null>(null)
const mapa = shallowRef<import('maplibre-gl').Map | null>(null)
let observador: MutationObserver | null = null
// The mount awaits three chunks: leaving meanwhile must not build a map nobody will ever remove.
let desmontado = false
// Two restyles can overlap (each awaits): only the newest may reach the map.
let ultimoEstilo = 0
let protocoloPmtiles = false
// Layers can only change between a style's `style.load` and the next setStyle.
let estiloListo = false

const filas = computed(() =>
  props.coropletas ? filasTabla(props.coropletas.datos, props.coropletas.valor, props.coropletas.etiqueta) : [],
)

// A token's RAW value can be any CSS colour syntax (`color-mix(in oklab, …)`, `oklch(…)`), and
// MapLibre only parses hex/rgb/hsl/named (measured: a production theme broke the border layer).
// So the token is resolved the way the browser paints it: applied to a probe element, painted
// into one canvas pixel, and read back as RGB. (Reading `fillStyle` back is NOT enough: Chrome
// answers `oklab(…)` for an oklab input — measured in a production build.)
let sonda: HTMLSpanElement | null = null
let lienzo: CanvasRenderingContext2D | null = null
function token(nombre: string): string {
  if (!sonda) {
    sonda = document.createElement('span')
    sonda.style.display = 'none'
    document.body.appendChild(sonda)
  }
  sonda.style.color = ''
  sonda.style.color = `var(${nombre})`
  const calculado = getComputedStyle(sonda).color
  if (!lienzo) {
    const c = document.createElement('canvas')
    c.width = 1
    c.height = 1
    lienzo = c.getContext('2d', { willReadFrequently: true })
  }
  if (!lienzo || !calculado) return calculado
  lienzo.clearRect(0, 0, 1, 1)
  lienzo.fillStyle = calculado
  lienzo.fillRect(0, 0, 1, 1)
  const [r, g, b, a] = lienzo.getImageData(0, 0, 1, 1).data
  return a === 255 ? `rgb(${r}, ${g}, ${b})` : `rgba(${r}, ${g}, ${b}, ${(a! / 255).toFixed(3)})`
}

function oscuro(): boolean {
  return document.documentElement.classList.contains('dark')
}

async function construirEstilo() {
  let capasBase: unknown[] = []
  if (props.origen) {
    const { layers, namedFlavor } = await import('@protomaps/basemaps')
    // Without self-served glyphs the symbol layers would ask for fonts nobody serves: drop them.
    capasBase = layers('base', namedFlavor(oscuro() ? 'dark' : 'light'), { lang: 'es' })
      .filter((c: { type?: string }) => props.origen?.glyphs || c.type !== 'symbol')
  }
  return estilo({ fondo: token('--background') || 'white', origen: props.origen, capasBase, origenApp: location.origin })
}

const CAPAS = ['coropletas-relleno', 'coropletas-borde', 'coropletas-resaltado', 'calor', 'puntos', 'puntos-texto']
const FUENTES = ['coropletas', 'calor', 'puntos']

const filtroResaltado = () => ['==', ['get', PROP_ID], props.resaltado ?? ''] as never

function pintarDatos() {
  const m = mapa.value
  if (!m) return
  // Idempotent: `load` and a style reload can both land here; adding a source twice throws.
  for (const id of CAPAS) if (m.getLayer(id)) m.removeLayer(id)
  for (const id of FUENTES) if (m.getSource(id)) m.removeSource(id)
  const borde = token('--border')
  const serie = token('--chart-2')
  const primario = token('--primary')
  const fondo = token('--background')
  const texto = token('--foreground')

  if (props.coropletas) {
    const c = props.coropletas
    const pasos = c.pasos ?? 5
    const cortesV = cortes(c.datos.features.map((f) => valorDe(f, c.valor)), pasos)
    const colores = rampa(fondo, serie, cortesV.length + 1)
    m.addSource('coropletas', { type: 'geojson', data: normalizarCoropletas(c.datos, c.valor) as never, promoteId: PROP_ID })
    m.addLayer({ id: 'coropletas-relleno', type: 'fill', source: 'coropletas',
      paint: { 'fill-color': expresionRelleno(PROP_VALOR, cortesV, colores) as never, 'fill-opacity': 0.85 } })  // lint-allow-token: MapLibre paint/layout key, not a CSS class
    m.addLayer({ id: 'coropletas-borde', type: 'line', source: 'coropletas',
      paint: { 'line-color': borde, 'line-width': 0.6 } })
    m.addLayer({ id: 'coropletas-resaltado', type: 'line', source: 'coropletas', filter: filtroResaltado(),
      paint: { 'line-color': texto, 'line-width': 2.5 } })
  }
  if (props.calor) {
    const p = props.calor.peso
    m.addSource('calor', { type: 'geojson', data: props.calor.datos as never })
    m.addLayer({ id: 'calor', type: 'heatmap', source: 'calor', paint: {
      'heatmap-weight': (p ? ['to-number', ['get', p], 1] : 1) as never,  // lint-allow-token: MapLibre paint/layout key, not a CSS class
      'heatmap-color': ['interpolate', ['linear'], ['heatmap-density'],
        0, conAlfa(serie, 0), 0.3, conAlfa(serie, 0.35), 1, serie] as never,
      'heatmap-radius': ['interpolate', ['exponential', 2], ['zoom'], 9, 12, 14, 60] as never,
    } })
  }
  if (props.puntos) {
    m.addSource('puntos', { type: 'geojson', data: props.puntos.datos as never })
    m.addLayer({ id: 'puntos', type: 'circle', source: 'puntos',
      paint: { 'circle-radius': 6, 'circle-color': primario, 'circle-stroke-color': fondo, 'circle-stroke-width': 2 } })
    if (props.origen?.glyphs) {
      m.addLayer({ id: 'puntos-texto', type: 'symbol', source: 'puntos', layout: {
        'text-field': ['get', props.puntos.etiqueta] as never, 'text-font': [props.fuente],  // lint-allow-token: MapLibre paint/layout key, not a CSS class
        'text-size': 12, 'text-offset': [0, 1.2], 'text-anchor': 'top' },  // lint-allow-token: MapLibre paint/layout key, not a CSS class
      paint: { 'text-color': texto, 'text-halo-color': fondo, 'text-halo-width': 1.5 } })  // lint-allow-token: MapLibre paint/layout key, not a CSS class
    }
  }
}

async function aplicarEstilo() {
  const m = mapa.value
  if (!m) return
  try {
    const n = ++ultimoEstilo
    const s = await construirEstilo()
    if (n !== ultimoEstilo || mapa.value !== m) return
    estiloListo = false
    // diff: false — a diffed setStyle may not emit `style.load`, and the data layers (added by
    // pintarDatos, not part of the style object) would silently vanish (measured in the browser).
    m.setStyle(s as never, { diff: false })
  } catch (e) {
    error.value = (e as Error).message
  }
}

onMounted(async () => {
  if (!contenedor.value) return
  try {
    const maplibre = await import('maplibre-gl')
    maplibre.setWorkerUrl(urlTrabajador)
    if (props.origen && !protocoloPmtiles) {
      const { Protocol } = await import('pmtiles')
      maplibre.addProtocol('pmtiles', new Protocol().tile)
      protocoloPmtiles = true
    }
    const s = await construirEstilo()
    if (desmontado || !contenedor.value) return
    const m = new maplibre.Map({
      container: contenedor.value,
      style: s as never,
      locale: { 'NavigationControl.ZoomIn': 'Acercar', 'NavigationControl.ZoomOut': 'Alejar' },
      center: props.centro,
      zoom: props.zoom,
      attributionControl: props.origen ? { compact: true, customAttribution: '© OpenStreetMap' } : false,
    })
    m.addControl(new maplibre.NavigationControl({ showCompass: false }), 'top-right')
    // One tab stop, MapLibre's own canvas (arrows pan, +/- zoom), named like the region —
    // its default name is the English «Map».
    m.keyboard.enable()
    m.getCanvas().setAttribute('aria-label', props.etiqueta)
    // On every style, the first one included. A listener per restyle (`once`) loses the layers
    // when two restyles overlap; pintarDatos is idempotent, so firing more than once is harmless.
    m.on('style.load', () => {
      estiloListo = true
      pintarDatos()
    })
    m.on('click', 'coropletas-relleno', (ev) => {
      const f = ev.features?.[0]
      const id = f?.properties?.[PROP_ID]
      if (id !== undefined && id !== null) emit('seleccionar', String(id))
    })
    mapa.value = m
    encuadrar(false)
    observador = new MutationObserver(() => aplicarEstilo())
    observador.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  } catch (e) {
    error.value = (e as Error).message
  }
})

// New data repaints only the data layers: a full setStyle would reparse the basemap on every filter
// change. If a restyle is under way, its `style.load` paints the latest props anyway.
watch(() => [props.coropletas, props.calor, props.puntos], () => {
  if (estiloListo) pintarDatos()
})
watch(() => props.origen, () => aplicarEstilo())

watch(() => props.resaltado, () => {
  if (mapa.value?.getLayer('coropletas-resaltado')) mapa.value.setFilter('coropletas-resaltado', filtroResaltado())
})

function encuadrar(animar = true) {
  const m = mapa.value
  if (!m) return
  if (props.encuadre) m.fitBounds(props.encuadre, { padding: 40, maxZoom: 15, animate: animar })
  else if (animar) m.easeTo({ center: props.centro, zoom: props.zoom })
}
watch(() => props.encuadre, () => encuadrar())

onBeforeUnmount(() => {
  desmontado = true
  sonda?.remove()
  sonda = null
  observador?.disconnect()
  mapa.value?.remove()
  mapa.value = null
})
</script>

<template>
  <section class="flex flex-col gap-2" data-pg-mapa-base>
    <div class="flex items-center justify-end gap-1" role="group" aria-label="Vista del mapa">
      <Button size="sm" :variant="vista === 'mapa' ? 'secondary' : 'ghost'" :aria-pressed="vista === 'mapa'" @click="vista = 'mapa'">
        <Icon name="mapPin" /> Mapa
      </Button>
      <Button size="sm" :variant="vista === 'tabla' ? 'secondary' : 'ghost'" :aria-pressed="vista === 'tabla'" @click="vista = 'tabla'">
        <Icon name="table" /> Tabla
      </Button>
    </div>

    <p v-if="error" role="alert" class="rounded-md border border-destructive p-3 text-sm text-destructive">
      {{ error }}
    </p>

    <div
      v-show="vista === 'mapa'"
      ref="contenedor"
      class="relative h-96 w-full overflow-hidden rounded-md border border-border bg-background"
      role="region"
      :aria-label="etiqueta"
    />

    <!-- R4: the same figures as text. Always in the DOM; visually hidden while the map is shown. -->
    <div :class="vista === 'tabla' ? 'overflow-auto rounded-md border border-border' : 'sr-only'">
      <table class="w-full text-sm">
        <caption class="sr-only">{{ etiqueta }}</caption>
        <thead>
          <tr class="border-b border-border text-left text-muted-foreground">
            <th scope="col" class="px-3 py-2 font-medium">Zona</th>
            <th scope="col" class="px-3 py-2 text-right font-medium">{{ nombreValor }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in filas" :key="f.id" class="border-b border-border last:border-0">
            <th scope="row" class="px-3 py-1.5 text-left font-normal">
              <!-- Out of the tab order while the table is visually hidden: a focus nobody can see. Not
                   `inert`: screen readers still read the table in browse mode (R4). -->
              <button type="button" class="text-left hover:underline focus-visible:underline" :tabindex="vista === 'tabla' ? 0 : -1" @click="emit('seleccionar', f.id)">
                {{ f.etiqueta }}
              </button>
            </th>
            <td class="px-3 py-1.5 text-right tabular-nums">{{ f.valor === null ? '—' : formato(f.valor) }}</td>
          </tr>
          <tr v-if="!filas.length">
            <td colspan="2" class="px-3 py-3 text-center text-muted-foreground">Sin zonas para mostrar.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
