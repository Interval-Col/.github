---
description: "Use when creating any Nuxt 4 component, page, composable, layout, or store for a Pháros product-family app. Covers Vue 3 Composition API conventions, Tailwind v4 usage on the Pháros token contract, file structure, SSR guidance, and TypeScript standards."
applyTo: "**/*.vue,**/*.ts"
---
# Pháros frontend standards (registry)

> The Nuxt 4 / Vue 3 / Tailwind v4 authoring conventions for any app in the
> **Pháros product family** (`Pháros · Timón` ERP, `Pháros LIS`, `Pháros Admisiones`,
> `Pháros CRM`, `Pháros Archivo`). This is the re-cut of the former
> `instructions/nuxt-standards`, bound to the registry token contract.
>
> **Source of truth for tokens:** [`tokens.css`](./tokens.css) (shadcn-vue vars +
> accent-independent status palette + the 4-font system + the sub-brand accent
> themes (`.theme-*`) + `.dark` theme).
> Distributed by **copy-in** via `scripts/sync-pharos-registry.sh`, **not** an npm
> package (RFC 0008 Q3). LCH and Biuman are **tenants** of this contract, not parents.

## Stack
- **Framework:** Nuxt 4 — `srcDir: app/` (the Nuxt 4 default); SSR por defecto (ver "Modo de renderizado")
- **UI:** Vue 3 Composition API (`<script setup lang="ts">`)
- **Estilos:** Tailwind v4 — configuración via CSS (`@theme` / `@theme inline` en `tokens.css`), no `tailwind.config.js`
- **Estado:** Pinia (`defineStore`)
- **Testing:** Vitest
- **Linting:** ESLint + Prettier

## Estructura de directorios (`app/` — Nuxt 4)
```
app/
├── assets/
│   └── css/
│       ├── tokens.css           ← contrato de tokens (copy-in del registry — NO editar a mano)
│       └── main.css             ← @import "tailwindcss"; @import "./tokens.css";
├── components/                  ← shadcn-vue + superficies Pháros (ver "Naming de componentes")
│   └── ui/                      ← primitivas shadcn-vue (Button, Card, Sidebar, …)
├── composables/
│   └── use{Nombre}.ts
├── pages/
├── layouts/
├── stores/
│   └── use{Nombre}Store.ts
├── types/
│   └── {dominio}.ts
└── app.vue
```
> El árbol vive bajo `app/`, no en un `frontend/` plano. `nuxt.config.ts`, `Dockerfile`
> y demás config quedan en la raíz del repo, fuera de `app/`.

## Convenciones de SFC (Vue 3)
```vue
<script setup lang="ts">
// 1. Imports externos
import { ref, computed } from 'vue'

// 2. Props y emits (siempre tipados)
const props = defineProps<{
  label: string
  value?: number
  variant?: 'primary' | 'secondary'
}>()

const emit = defineEmits<{
  change: [value: string]
  submit: []
}>()

// 3. Estado local
const isOpen = ref(false)

// 4. Computadas
const displayValue = computed(() => ...)

// 5. Funciones
function handleClick() { ... }
</script>

<template>
  <!-- Template -->
</template>

<style scoped>
/* Solo en componentes, y solo si las utilidades Tailwind no alcanzan. Ver "Estilos scoped". */
</style>
```

## Estilos scoped — dónde se permite `<style scoped>`
- **`app/pages/**` y `app/layouts/**`: solo utilidades Tailwind.** Un *gate* de CI
  prohíbe `<style scoped>` (y `<style>`) en páginas y layouts — si una utilidad no
  existe, componetiza el patrón en `app/components/` en vez de escribir CSS suelto.
- **`app/components/**`: `<style scoped>` permitido** como escape hatch puntual,
  cuando Tailwind no es suficiente (p. ej. un selector estructural que una utilidad
  no expresa). Aun así, prefiere utilidades primero.

## Modo de renderizado (SSR / CSR)

- **SSR por defecto.** Nunca pongas `ssr: false` global en
  `nuxt.config.ts`.
- Una página individual puede optar por CSR con
  `definePageMeta({ ssr: false })` **solo** cuando: está detrás de
  autenticación (sin valor SEO) **y** carga todos sus datos en
  `onMounted` vía `apiFetch` cliente — el render del servidor
  produciría únicamente un esqueleto vacío. Acompaña el
  `definePageMeta` con un comentario de una línea explicando el
  motivo.
- **Código compartido SSR-safe** (stores, composables, plugins): no
  uses `typeof window` / `typeof localStorage` para detectar el
  servidor — Node 22+ expone un global `localStorage` y ese chequeo
  falla (`.getItem()` lanza error). Usa `import.meta.client` /
  `import.meta.server`. Para estado de Pinia persistido solo en
  cliente, envuelve el `ref` en `skipHydrate()`.

## Tailwind v4 — Configuración y tokens
La configuración es **CSS-first**: no hay `tailwind.config.js`. El contrato de
tokens vive en [`tokens.css`](./tokens.css) y se expone a las utilidades de
Tailwind v4 vía `@theme inline`. **No** edites `tokens.css` a mano en el app:
llega por copy-in desde el registry.

```css
/* app/assets/css/main.css */
@import "tailwindcss";
@import "./tokens.css";   /* contrato de tokens del registry (shadcn vars + status) */
```

El contrato define los slots semánticos shadcn-vue y una **paleta de estado
independiente del acento** (`--status-success` / `--status-warning` /
`--status-error` / `--status-info`, cada uno con su `-foreground` y una superficie
`-bg` para tintes de fondo). Es **independiente del acento**: nunca se desplaza
cuando una sub-marca re-acentúa. Usa **siempre** estos roles semánticos en las
utilidades, nunca hex sueltos:

```vue
<!-- ✅ Roles semánticos del contrato -->
<div class="bg-card text-card-foreground border border-border rounded-lg">…</div>
<button class="bg-primary text-primary-foreground">Guardar</button>
<span class="text-status-success bg-status-success-bg">En control</span>
<span class="text-status-warning bg-status-warning-bg">Pendiente</span>
<span class="text-status-error bg-status-error-bg">Fuera de control</span>
<p class="text-muted-foreground">Texto secundario</p>

<!-- ❌ Hex/colores sueltos o utilidades de marca legadas -->
<div class="bg-[#003A70] text-[#888B8D]">…</div>
```

### Theming (light + dark) y acento por sub-marca
- **Light + dark únicamente**, conmutados por la clase shadcn **`.dark`** en el
  elemento raíz. No hay tema `cobol`/CRT ni `[data-theme]`.
- Una **sub-marca** se diferencia overrideando **solo** los slots de acento
  —`--primary`, `--ring`, `--sidebar-primary` y sus foregrounds— vía una clase
  `.theme-*` que vive en `tokens.css`; el app añade su clase al `<html>`. El resto
  del contrato (paleta de estado, neutros, constantes de marca, radius) se hereda
  sin cambios.
- Los **acentos de sub-marca están LOCKED** (5 por RFC 0008 — ACCEPTED 2026-06-17;
  `.theme-ti` por RFC 0004 rev. 2026-07-03), como clases `.theme-*` (light / dark):

  | Sub-marca | App | Clase | Acento (light / dark) |
  |---|---|---|---|
  | Números (ERP/finanzas) | Timón | `.theme-numeros` | ámbar `#7A5D00` / `#E6C34D` |
  | Laboratorio (LIS) | pharos-lis | `.theme-clinico` | teal `#1B6B5A` / `#4CD1B0` |
  | Movimiento (Biuman LIS) | biuman | `.theme-deportivo` | azul `#004F70` / `#16749C` |
  | Pacientes (Admisiones) | admisiones | `.theme-recepcion` | rosa funcional `#ff3d63` / `#ff6b85` (pastel `#FFE0E6` = solo `--brand-wash`) |
  | Clientes (CRM) | crm | `.theme-clientes` | ámbar funcional `#e37600` / `#f59e3c` (pastel `#FFB86B` = solo `--brand-wash`) |
  | Tecnología (TI · plataforma — nombre provisional, RFC 0004 rev.) | pharos-ti | `.theme-ti` | navy profundo `#002A52` / `#7FB0E6` |

  > El **ERP (Números)** pasó de navy a **ámbar `#7A5D00`** (RFC 0008 Q6); el navy
  > queda superado como acento de ERP.
- **Default/neutral (sin clase) = LCH Navy `#003A70`** — la familia-neutral / `Archivo`.
  Una clase `.theme-*` sobre-escribe **solo** los slots de acento; lo demás se hereda
  del neutro navy.

## Fuentes
Cuatro familias, vía las variables del contrato:
- **`--font-display`** → **Fraunces** (display / wordmark — clase `font-display`)
- **`--font-sans`** → **DM Sans** (UI sans — texto de interfaz por defecto — clase `font-sans`)
- **`--font-mono`** → **IBM Plex Mono** (**labels / etiquetas** únicamente — clase `font-mono`)
- **`--font-data`** → **JetBrains Mono** (**datos / cifras / figuras**, `tabular-nums` — clase `font-data`)

```vue
<h1 class="font-display">Tablero</h1>
<p class="font-sans">Texto de interfaz</p>
<span class="font-mono">RES-CTRL</span>                  <!-- labels / etiquetas / códigos -->
<span class="font-data tabular-nums">1.234,56</span>     <!-- datos / cifras / figuras -->
```
> Las **cifras / datos** usan `font-data` (**JetBrains Mono**) con `tabular-nums`;
> `font-mono` (**IBM Plex Mono**) es solo para **labels**. **Apax** no se usa en UI de
> producto (es un activo de identidad de marca **LCH** únicamente, no del contrato
> Pháros). Carga las cuatro familias en el app (self-host preferido) y deja que
> `--font-sans` sea el default.

## Naming de componentes
- Sin el esquema legado `Lch` + prefijo de sección. Usa primitivas **shadcn-vue**
  en `app/components/ui/` (`Button.vue`, `Card.vue`, `Sidebar.vue`, …) y compón
  componentes de superficie Pháros encima, en PascalCase descriptivo por dominio:
  `KpiCard.vue`, `ResultTable.vue`, `OrderQueue.vue`.
- Composables: `usePatientResults.ts`, `useLabMetrics.ts`
- Stores: `useFinanceStore.ts`, `useLaboratoryStore.ts`
- Tipos: `patient.ts`, `labResult.ts`, `invoice.ts`
> La **biblioteca de componentes del registry** (Fase 1, RFC 0008) ya está **publicada**:
> los primitivos compartidos viven en `registry/app/components/` + `registry/app/composables/`
> y se distribuyen copy-in vía `sync-pharos-registry.sh`. Ver «Biblioteca de componentes
> (Fase 1)» abajo. Las apps consumen estos primitivos en vez de re-implementarlos.

## API — Integración con FastAPI
```ts
// Usar useFetch de Nuxt — camelCase en FE, snake_case en BE
const { data } = await useFetch<PatientResult[]>('/api/results', {
  transform: (res) => res.map(normalizeResult)
})

// Fechas: ISO 8601 en API, DD/MM/YYYY para display
const displayDate = new Date(result.createdAt)
  .toLocaleDateString('es-CO', { day:'2-digit', month:'2-digit', year:'numeric' })
```

### Origin: same-origin by default (no CORS)

**A frontend talks to its backend same-origin: same host, through the proxy.** The
reverse-proxy publishes the pair under a single host — `/<app>` → frontend container,
`/<app>/api` → backend container — so the browser sees **one origin** and there is **no
CORS**. nginx matches by longest prefix: `/<app>/api/...` goes to the backend, everything
else to the frontend.

- **The FE API base is RELATIVE** (`NUXT_PUBLIC_API_BASE` = `/<app>` when the app is
  served under a path prefix), **never** an absolute URL to another host. An absolute base
  forces cross-origin → needless CORS, an extra preflight round-trip, and more attack
  surface.
- **Mind SSR** (see the SSR/CSR rendering-mode section above): a relative base only
  resolves in the browser. If a page fetches on the server (`useFetch` / `useAsyncData`
  with `server: true`), a relative path has no host — keep those fetches client-side, or
  provide an internal absolute base for the server side only.

**Cross-origin (a separate API host + CORS) is justified ONLY** when the backend is a
*shared gateway* consumed by **multiple** distinct frontends/origins (auth/SSO, a catalog
service, etc.). A 1:1 frontend↔backend pair is **not** one — it goes same-origin.

**If CORS is genuinely required, two non-negotiable rules:**
1. **The environment-variable name must exactly match the backend's `Settings` field.** If
   the code reads `FOO_ORIGINS` but the deploy sets `BAR_ORIGINS`, the variable is silently
   ignored, the backend falls back to its default, and **CORS breaks in production even
   though it looks configured.** Always check both sides.
2. **Never `allow_origins=["*"]` together with `allow_credentials=True`** — that is "any
   origin, with credentials." List explicit origins instead.

> Migration in progress of the 1:1 pairs still on cross-origin → same-origin. Tracking +
> step-by-step guide (internal): `Interval-Col/operations#29`.

## Mensajes de error — Voz de marca
```ts
// ✅ Tono Pháros — empático, claro, en la voz del usuario
throw createError({ statusCode: 404, message: 'No encontramos tu resultado. Verifica tu número de documento.' })
// ❌ Frío / genérico
throw createError({ statusCode: 404, message: 'Record not found' })
```

## Layout y grid
- Max content width: `max-w-[1280px] mx-auto`
- Grid: `grid grid-cols-12 gap-6` desktop, `gap-4` mobile
- Padding de sección: `py-16 px-4 md:px-6`
- Cards: `rounded-lg` (8px, = `--radius`), modals: `rounded-xl` (12px), badges: `rounded-full`
- Sombras: `shadow-sm` default, `shadow-md` on hover
- App-shell: el `Sidebar` de shadcn-vue es la referencia (usa los slots `bg-sidebar`,
  `text-sidebar-foreground`, `bg-sidebar-primary`, …).

## Iconos
Un solo tag **`<Icon>`** (`app/components/ui/icon/Icon.vue`) sobre `@iconify/tailwind`.
Acepta una **clave del registro curado** (`app/components/ui/icon/icons.ts`, ~94 claves:
Lucide como set principal + un subconjunto clínico de Material Symbols) **o** un id crudo
`prefix:name`.
```vue
<Icon name="search" />                       <!-- size 4 = 16px (inline, por defecto) -->
<Icon name="patient" :size="5" />            <!-- size 5 = 20px (botones / nav) -->
<Icon name="calendar" :size="6" class="text-primary" />  <!-- size 6 = 24px (encabezados) -->
<Icon name="stethoscope" label="Médico" />   <!-- significativo: role="img" + aria-label -->
```
- **Escala** `size` = 4 / 5 / 6 → 16 / 20 / 24 px (BRAND.md §8).
- **Color** solo por roles semánticos del contrato (`text-primary`, `text-status-success`,
  `text-muted-foreground`, …), nunca hex. Siempre stroke-based, terminaciones redondeadas.
- **a11y**: decorativo por defecto (`aria-hidden`); pasa `label` para iconos significativos.
- El wrapper construye la clase `icon-[…]` en runtime, así que el registro curado se
  **fuerza** vía `app/assets/css/pharos-icons.css` (el safelist `@source`, sincronizado con
  `icons.ts`). La app adopta con una línea en su `main.css`: `@import "./pharos-icons.css";`
  + las deps per-collection (`@iconify-json/lucide`, `@iconify-json/material-symbols`,
  `@iconify/tailwind`) — todas seguras para `check-fe-bloat` (no el monolito `@iconify/json`).

## Biblioteca de componentes (Fase 1)
Primitivos compartidos Pháros, en `registry/app/components/ui/**` + `registry/app/composables/**`,
distribuidos copy-in (`sync-pharos-registry.sh`). Úsalos en vez de re-implementar. Cada app
añade las **deps de adopción** indicadas (todas seguras para `check-fe-bloat`).

| Primitivo | Ruta | Para qué | Deps de adopción |
|---|---|---|---|
| **SearchableSelect** | `ui/searchable-select` | Desplegable con filtro al teclear (estático o `searchFn` async); maneja valor vacío sin sentinel | — |
| **EntityLookup** (+ `ScopedSearchInput`, `PatientLookup`, `PhysicianLookup`) | `ui/entity-lookup`, `ui/scoped-search` | Búsqueda de persona con chips de filtro guiados (cédula con tipo de doc, nombre, orden…) → resultados → selección | — |
| **PageHeader** | `ui/page-header` | Encabezado de contenido (título/descripción/`#actions`/`#toolbar`); título `<h2>`, breadcrumb-as-title | — |
| **Icon** | `ui/icon` | Un solo tag de icono sobre `@iconify/tailwind` + registro curado (~94) | `@iconify-json/lucide`, `@iconify-json/material-symbols`, `@iconify/tailwind`, `@import "./pharos-icons.css"` |
| **FlowSteps** | `ui/flow-steps` | Indicador de pasos para flujos multi-paso (estado por paso) | — |
| **FormField** | `ui/form-field` | Wrapper de campo (label + control + error/hint/required); **agnóstico de validación** | — |
| **DatePicker** | `ui/date-picker` | Fecha es-CO: campo segmentado `dd/mm/aaaa` + calendario; `v-model` ISO; rellenable por escaneo de cédula | `@internationalized/date` |
| **useFlow** | `composables/useFlow.ts` | Back-stack + estado de diálogo (pasos como config; `goBack` real preserva datos) | — |
| **useAsyncState** | `composables/useAsyncState.ts` | Envoltura de fetch (`data/status/loading/error/isEmpty/refresh`); AbortController + guard de respuesta stale; `isEmpty` explícito | — |

> Decisiones parqueadas para la sesión de co-creación (refinamientos; copy-in es barato de
> revisar): FormField atado-a-vee-validate vs agnóstico · ruteo chips→backend de EntityLookup ·
> migración del estado persistido de `useProcessState`→`useFlow` · tipo del modelo de DatePicker.

## Higiene de dependencias — gate `check-fe-bloat`
Una compuerta de CI (`scripts/check-fe-bloat.mjs`, sincronizada del registry y
encadenada en `lint-check`) previene el bloat de dependencias que vimos en
admission-patient (íconos y librerías duplicadas). Reglas **deterministas** (cero
falsos positivos):

- **Sin monolito de íconos.** `@iconify/json` (~400 MB, todas las colecciones) está
  prohibido. Instala solo los paquetes per-collection `@iconify-json/<prefix>` que
  de verdad usas; `@iconify/tailwind` los resuelve **antes** que el monolito, así que
  el CSS generado es idéntico y la instalación baja muchísimo (399 MB → solo lo usado).
- **Una sola librería por categoría.** A lo sumo una librería por propósito (p. ej.
  una de Lucide-para-Vue: `lucide-vue-next` *o* `@lucide/vue`; una de Radix/Reka
  headless-UI: `reka-ui` *o* `radix-vue`). Dos libs que hacen lo mismo inflan
  instalación y bundle.

Excepciones: `ALLOWLIST` dentro del script (mínima y justificada, con fecha de
retiro). Fast-follow ([Interval-Col/.github#70]): deps muertas vía `knip` y un
presupuesto de tamaño de bundle (chequeo post-build).

[Interval-Col/.github#70]: https://github.com/Interval-Col/.github/issues/70

## Gráficos y datos masivos (analítica)
Para superficies con muchos datos (series de un *fact table* grande, p. ej. la media
móvil de QC). La cota del **lado de datos** —agregación en SQL, `statement_timeout`,
índice por predicado— vive en las normas de backend/datos del app (en lab-qc,
`docs/STANDARDS.md` → "Analytics & big-data queries"). Lado **frontend**:

- **Botón explícito de construir/aplicar, no fetch por cambio.** Las consultas
  costosas se disparan con un botón ("Generar"), no en cada cambio de control. El
  botón refleja estado *dirty* (variant `default`/primario cuando hay cambios sin
  aplicar; apagado/`outline` cuando el gráfico está al día). Colapsa N fetches
  reactivos en 1 deliberado.
- **`AbortController` + guard de respuesta obsoleta en todo fetch.** Cancela la
  solicitud en curso al reconstruir/desmontar y descarta respuestas superadas (un
  `requestId` que invalida las tardías). Evita el *pile-up* y que una respuesta lenta
  pise a una nueva.
- **Separar controles de *vista* de los de *consulta*.** Lo que es transformación
  puramente cliente (tamaño de ventana de suavizado, zoom, orden) se recalcula en el
  cliente y **no** vuelve a consultar. Los ejes y el título quedan **acoplados a los
  datos construidos**, no a los inputs en vivo: cambiar una fecha marca el botón como
  pendiente, pero el eje no se mueve hasta reconstruir.
- **Tope de marcas renderizadas.** @unovis dibuja un nodo SVG por punto (sin
  decimación). Agrega/submuestrea antes de renderizar —idealmente del lado servidor,
  ≤ unos cientos de puntos— para no congelar el hilo principal.
- **El *loading* no borra un gráfico ya dibujado.** Muestra el spinner sólo en la
  primera carga; en recargas deja el gráfico visible. Usa `:key` (identidad de los
  datos: rango + tamaño de la serie) para forzar un re-montaje limpio al cambiar el
  dataset, de modo que el *crosshair* de @unovis no lea datos obsoletos/vacíos y
  rompa en hover.
- **Múltiples vistas como toggles de cliente.** Cuando una distribución admite más de
  una lectura honesta, ofrécelas como un toggle que re-renderiza en el cliente (sin
  refetch): p. ej. *cajas por día* (box-whisker), *bandas* (áreas) y *puntos*
  (resultados individuales). Para cubetas discretas (una por día) prefiere siluetas
  por día sobre rellenos continuos: el relleno insinúa una interpolación entre días
  que no existe. Los puntos individuales se muestran sólo hasta un tope; superado,
  degrada a la dispersión agregada (el tope vive en las normas de datos del app).
- **Leyenda obligatoria en gráficos multi-marca.** Un gráfico con más de un tipo de
  marca (línea + puntos + banda/caja) necesita leyenda; que se adapte al modo activo.

Impl de referencia: pharos-lis `analytics/media-movil` (PRs #27, #29, #30).

## Commits (Conventional Commits)
Tipos canónicos (idénticos en branches y commits): **`feat`, `fix`, `refactor`,
`test`, `chore`, `docs`, `hotfix`, `ci`**. Merge-commit en todos lados (squash
deshabilitado).
```
feat(lis): add result search component
fix(finance): correct currency formatting on KPI card
refactor(laboratory): extract useLabResults composable
ci(admisiones): add scoped-style gate for pages/layouts
```
