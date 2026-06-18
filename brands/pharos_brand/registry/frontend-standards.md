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
> accent-independent status palette + the 4-font system + the 5 sub-brand accent
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
- Los **5 acentos de sub-marca están LOCKED** (RFC 0008 — ACCEPTED 2026-06-17),
  como clases `.theme-*` (light / dark):

  | Sub-marca | App | Clase | Acento (light / dark) |
  |---|---|---|---|
  | Números (ERP/finanzas) | Timón | `.theme-numeros` | ámbar `#7A5D00` / `#E6C34D` |
  | Clínico (LIS) | pharos-lis | `.theme-clinico` | teal `#1B6B5A` / `#4CD1B0` |
  | Deportivo (Biuman LIS) | biuman | `.theme-deportivo` | azul `#004F70` / `#16749C` |
  | Recepción (Admisiones) | admisiones | `.theme-recepcion` | rosa `#FFE0E6` (light+dark) |
  | Clientes (CRM) | crm | `.theme-clientes` | ámbar claro `#FFB86B` (light+dark) |

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
> La **biblioteca de componentes del registry** (los SFC shadcn-vue compartidos) es
> el follow-up de **Fase 1** (RFC 0008): hoy el registry distribuye tokens +
> convenciones + guía por superficie; los componentes se construyen en el brand
> playground. Hasta entonces, cada app mantiene sus SFC alineados a estas convenciones.

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
```vue
<Icon name="..." class="w-5 h-5 text-primary" />            <!-- sm: 20px -->
<Icon name="..." class="w-6 h-6 text-foreground" />         <!-- md: 24px -->
<Icon name="..." class="w-8 h-8 text-muted-foreground" />   <!-- lg: 32px -->
```
Siempre: stroke-based, rounded terminals. Colores solo de los roles semánticos del
contrato (`text-primary`, `text-status-success`, `text-muted-foreground`, …), nunca hex.

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
