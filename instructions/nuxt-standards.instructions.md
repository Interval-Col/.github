---
description: "Use when creating any Nuxt 4 component, page, composable, layout, or store for Interval-Col / LCH projects. Covers Vue 3 Composition API conventions, Tailwind v4 usage, file structure, and TypeScript standards."
applyTo: "**/*.vue,**/*.ts"
---
# Estándares Nuxt 4 — Interval-Col / LCH

## Stack
- **Framework:** Nuxt 4 — SSR por defecto (ver "Modo de renderizado")
- **UI:** Vue 3 Composition API (`<script setup lang="ts">`)
- **Estilos:** Tailwind v4 — configuración via CSS (`@theme`), no `tailwind.config.js`
- **Estado:** Pinia (`defineStore`)
- **Testing:** Vitest
- **Linting:** ESLint + Prettier

## Estructura de directorios frontend
```
frontend/
├── assets/
│   └── css/
│       └── tokens.css          ← CSS variables globales LCH
├── components/
│   ├── Lch/                    ← Componentes de marca compartida (logo, etc.)
│   ├── PortalPacientes/        ← Sección pacientes
│   ├── Laboratorio/            ← Sección lab
│   ├── Finanzas/               ← Sección finanzas
│   ├── Calidad/                ← Sección calidad
│   ├── Reportes/               ← Sección reportes
│   └── Administracion/         ← Sección admin
├── composables/
│   └── use{Nombre}.ts
├── pages/
├── layouts/
├── stores/
│   └── use{Nombre}Store.ts
├── types/
│   └── {dominio}.ts
└── Dockerfile
```

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
/* Solo si Tailwind no es suficiente */
</style>
```

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

## Tailwind v4 — Configuración
```css
/* assets/css/tokens.css */
@import "tailwindcss";

@theme {
  /* Colores LCH */
  --color-lch-red:       #E4002B;
  --color-lch-red-dark:  #A6192E;
  --color-lch-orange:    #FF8200;
  --color-lch-lilac:     #D986BA;
  --color-lch-pink:      #FC9BB3;
  --color-lch-navy:      #003A70;
  --color-lch-blue:      #326295;
  --color-lch-teal:      #A0D1CA;
  --color-lch-blush:     #F4CDD4;
  --color-lch-yellow:    #FBD872;
  --color-lch-black:     #000000;
  --color-lch-gray-dark: #888B8D;
  --color-lch-gray-mid:  #C8C9C7;
  --color-lch-white:     #FFFFFF;

  /* Fuentes */
  --font-brand: 'Apax', 'Inter', 'DM Sans', system-ui, sans-serif;
  --font-data:  'JetBrains Mono', 'IBM Plex Mono', monospace;
  --font-label: 'IBM Plex Mono', 'JetBrains Mono', monospace;
}
```

## Naming de componentes
- PascalCase con prefijo de sección: `LchFinanzasKpiCard.vue`, `LchLaboratorioResultTable.vue`
- Composables: `usePatientResults.ts`, `useLabMetrics.ts`
- Stores: `useFinanzasStore.ts`, `useLaboratorioStore.ts`
- Tipos: `patient.ts`, `labResult.ts`, `invoice.ts`

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
// ✅ Tono LCH — empático, claro
throw createError({ statusCode: 404, message: 'No encontramos tu resultado. Verifica tu número de documento.' })
// ❌ Frío / genérico
throw createError({ statusCode: 404, message: 'Record not found' })
```

## Layout y grid
- Max content width: `max-w-[1280px] mx-auto`
- Grid: `grid grid-cols-12 gap-6` desktop, `gap-4` mobile
- Padding de sección: `py-16 px-4 md:px-6`
- Cards: `rounded-lg` (8px), modals: `rounded-xl` (12px), badges: `rounded-full`
- Sombras: `shadow-sm` default, `shadow-md` on hover

## Iconos
```vue
<Icon name="..." class="w-5 h-5 text-lch-red" />    <!-- sm: 20px -->
<Icon name="..." class="w-6 h-6 text-lch-navy" />   <!-- md: 24px -->
<Icon name="..." class="w-8 h-8 text-lch-gray-dark" /> <!-- lg: 32px -->
```
Siempre: stroke-based, rounded terminals. Colores solo de la paleta LCH.

## Commits (Conventional Commits)
```
feat(portal-pacientes): add result search component
fix(finanzas): correct currency formatting on KPI card
refactor(laboratorio): extract useLabResults composable
```
