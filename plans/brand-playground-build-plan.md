---
status: in-progress
created: 2026-06-13
owner: gczuluaga
tracking-issue: Interval-Col/.github#27
intent: auto-runnable by a Sonnet coding agent
relates-to: RFC 0008 Q5 (brand playground), Q4 (token contract), Q7 (theming), Q11 (charts)
---

# Pháros brand playground — local build plan (auto-runnable)

## 0. What this is + how to run it

A **local-only Nuxt app** that renders the shared Pháros app-shell + a component
gallery + sample charts, with a **control panel** that live-switches **accent
(per sub-brand) · theme (light/dark) · font** — so the team can *see* the design
system re-theme before locking the open brand decisions. It's the **code-first
Figma replacement** RFC 0008 implies, and the surface that validates Q6 accents,
Q7 themes, the Q5 mono pick, and the Q11 chart palette.

**How to auto-run with Sonnet:** open a Claude session (Sonnet, auto-accept
edits is fine — this is mechanical) and paste:

> Execute the plan at `/Users/gczuluaga/dev/.github/plans/brand-playground-build-plan.md`
> exactly, phase by phase. Build the app at `/Users/gczuluaga/dev/pharos-playground/`.
> After each phase run its verification step. At the end, run `pnpm dev`, drive the
> page, and confirm the §10 acceptance checklist. Do not deviate from the embedded
> file contents — they encode locked RFC 0008 decisions. Don't push.

## 1. Locked decisions this playground MUST embody (do not drift)

- **Stack:** Nuxt 4 + Vue 3 + TypeScript, **Tailwind v4 CSS-first** (NO
  `tailwind.config.*`; config lives in `app/assets/css/main.css`), **shadcn-vue**
  (new-york / zinc / lucide), pnpm, Node ≥ 22.
- **Theming = `.dark` CLASS** on `<html>` (Q7) — **light/dark only, NO cobol**.
- **Token contract = LEAN** (Q4): shadcn vars as the base **+ one
  accent-INDEPENDENT status palette** (success/warning/error/info, each fg+bg).
  The status palette MUST NOT change when the accent changes — the playground
  proves this.
- **Brand accent maps to `--primary`** (+ `--ring`, `--sidebar-primary`,
  `--chart-1`) — NOT to shadcn's `--accent` (that stays the neutral hover bg).
- **3 fonts** (Q5): Fraunces (display/wordmark) · Inter (sans UI) · IBM Plex
  Mono (mono). Load JetBrains Mono too **only** as a selectable alternative so
  the team can A/B the mono pick.
- **Charts = @unovis** (Q11), colored from `--chart-1..5`; client-only.
- **Shell = lab-qc pattern** (Q-ref): shadcn `Sidebar collapsible="icon"` +
  sticky topbar + breadcrumb. **NO page `<h1>`** — the breadcrumb's bold last
  segment is the title. **UI copy in Spanish** (neutral Colombian).

## 2. Target & prerequisites

- Build dir: **`/Users/gczuluaga/dev/pharos-playground/`** (fresh; `git init`,
  no remote — future home is the `pharos-ui` registry).
- `node >= 22`, `pnpm` (use `pnpm@10`+). Verify: `node -v && pnpm -v`.

## 3. Phase 0 — Scaffold

```bash
cd /Users/gczuluaga/dev
pnpm create nuxt@latest pharos-playground   # choose: no extra modules, pnpm
cd pharos-playground
git init -q

# Tailwind v4 (CSS-first) + shadcn-nuxt + supporting deps
pnpm add -D tailwindcss @tailwindcss/vite tw-animate-css
pnpm dlx nuxi@latest module add shadcn-nuxt
pnpm add @pinia/nuxt pinia @nuxt/fonts
pnpm add @vueuse/core lucide-vue-next class-variance-authority clsx tailwind-merge reka-ui
pnpm add @unovis/vue@1.6.5 @unovis/ts@1.6.5

pnpm dlx nuxi prepare   # MUST run before shadcn-vue init (generates .nuxt types)
```

**Pin reference** (match these majors; from the finance-lch/lab-qc real trees):
`nuxt ^4` · `vue ^3.5` · `typescript ^5.5` · `tailwindcss ^4` · `@tailwindcss/vite ^4`
· `tw-animate-css ^1.4` · `shadcn-nuxt ^2.6` · `shadcn-vue ^2.6` · `reka-ui ^2.9`
· `class-variance-authority ^0.7` · `clsx ^2.1` · `tailwind-merge ^3.5` ·
`lucide-vue-next ^1` · `@vueuse/core ^14` · `pinia ^3` · `@pinia/nuxt ^0.11` ·
`@nuxt/fonts` (latest) · `@unovis/vue 1.6.5` + `@unovis/ts 1.6.5` (lockstep).

**Verify P0:** `pnpm dev` boots the default Nuxt page at http://localhost:3000.
Stop it before continuing.

## 4. Phase 1 — Token contract: `app/assets/css/main.css`

Overwrite `app/assets/css/main.css` with **exactly** this (it encodes Q4/Q5/Q7).
Note: brand accent → `--primary`; status palette is its own block and is
**identical in structure** across light/dark (accent-independent).

```css
/* Pháros brand playground — LEAN token contract (RFC 0008 Q4/Q5/Q7) */
@import "tailwindcss";
@import "tw-animate-css";
@custom-variant dark (&:is(.dark *));

/* ---- Brand primitives -> Tailwind color utilities (bg-lch-navy, etc.) ---- */
@theme {
  --color-lch-navy: #003A70;
  --color-lch-blue: #326295;
  --color-lch-teal: #A0D1CA;
  --color-lch-pink: #F4CDD4;
  --color-lch-yellow: #FBD872;
  --color-lch-burgundy: #782F40;
  --color-lch-red: #E4002B;
}

/* ---- LIGHT: shadcn contract + accent-independent status + charts ---- */
:root {
  color-scheme: light;
  --radius: 0.5rem;

  --background: #ffffff;
  --foreground: #1a1d21;
  --card: #ffffff;
  --card-foreground: #1a1d21;
  --popover: #ffffff;
  --popover-foreground: #1a1d21;
  --primary: #003A70;          /* brand accent (ERP=Navy default) — overridden at runtime */
  --primary-foreground: #ffffff;
  --secondary: #eeeeed;
  --secondary-foreground: #1a1d21;
  --muted: #f7f7f6;
  --muted-foreground: #6b6e70;
  --accent: #eeeeed;           /* shadcn neutral hover bg — NOT the brand accent */
  --accent-foreground: #1a1d21;
  --destructive: #8b1a2b;
  --destructive-foreground: #ffffff;
  --border: #e2e2e1;
  --input: #e2e2e1;
  --ring: #003A70;             /* focus ring follows the brand accent */

  --sidebar: #f7f7f6;
  --sidebar-foreground: #1a1d21;
  --sidebar-primary: #003A70;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #eeeeed;
  --sidebar-accent-foreground: #1a1d21;
  --sidebar-border: #e2e2e1;
  --sidebar-ring: #003A70;

  /* ACCENT-INDEPENDENT STATUS PALETTE — never moves when the accent changes */
  --status-success: #1b6b5a; --status-success-bg: #e8f5f1;
  --status-warning: #7a5d00; --status-warning-bg: #fef6dc;
  --status-error:   #8b1a2b; --status-error-bg:   #fceaee;
  --status-info:    #003a70; --status-info-bg:    #e4edf7;

  /* numbered chart palette (brand-derived) */
  --chart-1: #003A70;
  --chart-2: #A0D1CA;
  --chart-3: #326295;
  --chart-4: #FBD872;
  --chart-5: #782F40;
}

/* ---- DARK overrides (.dark class) ---- */
.dark {
  color-scheme: dark;
  --background: #0f2744;
  --foreground: #e8eef5;
  --card: #13233d;
  --card-foreground: #e8eef5;
  --popover: #13233d;
  --popover-foreground: #e8eef5;
  --primary: #A0D1CA;          /* ERP accent shifts to teal in dark */
  --primary-foreground: #06121f;
  --secondary: #1c3454;
  --secondary-foreground: #e8eef5;
  --muted: #16283f;
  --muted-foreground: #9bb0c6;
  --accent: #1c3454;
  --accent-foreground: #e8eef5;
  --destructive: #f4a0b0;
  --destructive-foreground: #2a0a10;
  --border: #243a5a;
  --input: #243a5a;
  --ring: #A0D1CA;

  --sidebar: #0c1f38;
  --sidebar-foreground: #e8eef5;
  --sidebar-primary: #A0D1CA;
  --sidebar-primary-foreground: #06121f;
  --sidebar-accent: #1c3454;
  --sidebar-accent-foreground: #e8eef5;
  --sidebar-border: #243a5a;
  --sidebar-ring: #A0D1CA;

  --status-success: #4cd1b0; --status-success-bg: #0c2a24;
  --status-warning: #e6c34d; --status-warning-bg: #2e2606;
  --status-error:   #f4a0b0; --status-error-bg:   #2a0a10;
  --status-info:    #7fb0e6; --status-info-bg:    #0a1f38;

  --chart-1: #5b9bd5;
  --chart-2: #A0D1CA;
  --chart-3: #8fb3d9;
  --chart-4: #FBD872;
  --chart-5: #c98a9b;
}

/* ---- map runtime vars -> Tailwind v4 utilities ---- */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);

  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --color-status-success: var(--status-success);
  --color-status-success-bg: var(--status-success-bg);
  --color-status-warning: var(--status-warning);
  --color-status-warning-bg: var(--status-warning-bg);
  --color-status-error: var(--status-error);
  --color-status-error-bg: var(--status-error-bg);
  --color-status-info: var(--status-info);
  --color-status-info-bg: var(--status-info-bg);

  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);

  /* 3-family font system (Q5) */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", "JetBrains Mono", monospace;
  --font-heading: "Fraunces", "Times New Roman", serif;

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground font-sans; }
}
```

**Verify P1:** no build error after wiring `nuxt.config` (Phase 2); the page
background is white in light and dark-navy when `<html class="dark">`.

## 5. Phase 2 — `nuxt.config.ts` (Tailwind plugin + fonts + modules + FOUC guard)

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  modules: ['@pinia/nuxt', 'shadcn-nuxt', '@nuxt/fonts'],
  css: ['~/assets/css/main.css'],
  vite: { plugins: [tailwindcss()] },
  // @unovis touches the DOM at import; keep its ESM transpiled (still render client-only).
  build: { transpile: ['@unovis/vue', '@unovis/ts'] },
  shadcn: { prefix: '', componentDir: './app/components/ui' },
  fonts: {
    families: [
      { name: 'Fraunces',       weights: [400, 500],      provider: 'google' },
      { name: 'Inter',          weights: [400, 500, 600], provider: 'google' },
      { name: 'IBM Plex Mono',  weights: [400, 500],      provider: 'google' },
      { name: 'JetBrains Mono', weights: [400, 500],      provider: 'google' }, // A/B only
    ],
  },
  app: {
    head: {
      title: 'Pháros · Playground',
      // FOUC guard: paint .dark before hydration so there's no flash.
      script: [{
        innerHTML:
          "(function(){var t=localStorage.getItem('pharos-pg-theme');var d=t==='dark'||(t!=='light'&&window.matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d)})()",
        tagPosition: 'head',
      }],
    },
  },
  devServer: { port: 3000, host: '0.0.0.0' },
})
```

**Verify P2:** `pnpm dev` boots clean; `@nuxt/fonts` downloads the 4 families
(check Network or `.nuxt/cache/fonts`).

## 6. Phase 3 — shadcn-vue init + components

```bash
pnpm dlx shadcn-vue@latest init    # accept: new-york, zinc base, css app/assets/css/main.css, prefix "", lucide
# IMPORTANT: if init offers to overwrite main.css, DECLINE / then re-apply the Phase-1 file.
pnpm dlx shadcn-vue@latest add button badge input label select checkbox switch \
  dialog table tabs card separator tooltip sidebar breadcrumb popover sheet
```

`app/lib/utils.ts` (created by init; confirm it contains):
```ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

**Verify P3:** `ls app/components/ui` shows the added components;
`pnpm dev` still boots; re-confirm `main.css` is still the Phase-1 content (init
sometimes rewrites the `:root`/`.dark` blocks — if so, restore Phase 1).

## 7. Phase 4 — Theming engine: `app/stores/playground.ts`

The playground's brain. Writes brand-accent + font overrides as inline CSS vars
on `<html>` (inline beats the stylesheet, and overriding on `documentElement`
re-themes every shadcn component). Status palette is deliberately untouched.

```ts
import { defineStore } from 'pinia'

export interface SubBrand {
  id: string
  name: string            // user-facing lockup
  /* accent + its readable foreground, per theme */
  light: { accent: string; foreground: string }
  dark: { accent: string; foreground: string }
  locked: boolean         // true = decided (ERP); false = placeholder to explore
}

// ERP is LOCKED (RFC 0008 Q1/Q6). The rest are PLACEHOLDERS for the SKuger session.
export const SUB_BRANDS: SubBrand[] = [
  { id: 'erp',          name: 'Pháros · Timón (ERP)',        light: { accent: '#003A70', foreground: '#ffffff' }, dark: { accent: '#A0D1CA', foreground: '#06121f' }, locked: true },
  { id: 'lis-clinico',  name: 'LIS clínico — ? (LCH)',       light: { accent: '#782F40', foreground: '#ffffff' }, dark: { accent: '#d59aa8', foreground: '#2a0a12' }, locked: false },
  { id: 'lis-deport',   name: 'LIS deportivo — ? (Biuman)',  light: { accent: '#326295', foreground: '#ffffff' }, dark: { accent: '#8fb3d9', foreground: '#06121f' }, locked: false },
  { id: 'admisiones',   name: 'Admisiones — ?',              light: { accent: '#1b6b5a', foreground: '#ffffff' }, dark: { accent: '#4cd1b0', foreground: '#06121f' }, locked: false },
  { id: 'crm',          name: 'CRM — ? (¿Gente?)',           light: { accent: '#7a5d00', foreground: '#ffffff' }, dark: { accent: '#e6c34d', foreground: '#2e2606' }, locked: false },
]

export const MONO_FONTS = [
  { id: 'ibm',     label: 'IBM Plex Mono (decidida)', stack: '"IBM Plex Mono", monospace' },
  { id: 'jetbrains', label: 'JetBrains Mono (A/B)',   stack: '"JetBrains Mono", monospace' },
]

export const usePlayground = defineStore('playground', () => {
  const theme = ref<'light' | 'dark'>('light')
  const subBrandId = ref('erp')
  const customAccent = ref<string | null>(null) // overrides preset accent if set
  const monoId = ref('ibm')

  const subBrand = computed(() => SUB_BRANDS.find(s => s.id === subBrandId.value) ?? SUB_BRANDS[0])

  function apply() {
    if (!import.meta.client) return
    const el = document.documentElement
    el.classList.toggle('dark', theme.value === 'dark')
    const tone = theme.value === 'dark' ? subBrand.value.dark : subBrand.value.light
    const accent = customAccent.value ?? tone.accent
    const fg = customAccent.value ? '#ffffff' : tone.foreground
    // brand accent -> --primary + ring + sidebar-primary + chart-1 (NOT shadcn --accent)
    for (const v of ['--primary', '--ring', '--sidebar-primary', '--sidebar-ring', '--chart-1']) {
      el.style.setProperty(v, accent)
    }
    el.style.setProperty('--primary-foreground', fg)
    el.style.setProperty('--sidebar-primary-foreground', fg)
    // font (mono A/B)
    const mono = MONO_FONTS.find(m => m.id === monoId.value) ?? MONO_FONTS[0]
    el.style.setProperty('--font-mono', mono.stack)
    localStorage.setItem('pharos-pg-theme', theme.value)
  }

  function setSubBrand(id: string) { subBrandId.value = id; customAccent.value = null; apply() }
  function setCustomAccent(hex: string) { customAccent.value = hex; apply() }
  function clearCustomAccent() { customAccent.value = null; apply() }
  function toggleTheme() { theme.value = theme.value === 'dark' ? 'light' : 'dark'; apply() }
  function setMono(id: string) { monoId.value = id; apply() }

  function init() {
    // sync to whatever the FOUC guard already painted
    if (import.meta.client) theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
    apply()
  }

  return { theme, subBrandId, customAccent, monoId, subBrand, setSubBrand, setCustomAccent, clearCustomAccent, toggleTheme, setMono, init, apply }
})
```

**Verify P4:** unit-free — covered by P9 runtime checks.

## 8. Phase 5 — App-shell: `app/layouts/default.vue`

Mirror lab-qc: `SidebarProvider` > `Sidebar collapsible="icon"` + `SidebarInset`
with a sticky topbar (logo text + breadcrumb + the control-panel trigger). NO
`<h1>`. Sample nav with two sections so the breadcrumb has something to show.

Key structure (assemble with the vendored sidebar components; this is the
skeleton — keep it faithful, Spanish labels):

```vue
<script setup lang="ts">
import { Palette, LayoutGrid, BarChart3 } from 'lucide-vue-next'
import PlaygroundPanel from '~/components/PlaygroundPanel.vue'
const route = useRoute()
const nav = [
  { label: 'Componentes', to: '/', icon: LayoutGrid },
  { label: 'Gráficas', to: '/graficas', icon: BarChart3 },
]
const crumbLeaf = computed(() => nav.find(n => n.to === route.path)?.label ?? 'Componentes')
const pg = usePlayground()
onMounted(() => pg.init())
</script>

<template>
  <SidebarProvider>
    <Sidebar collapsible="icon">
      <SidebarHeader><SidebarTrigger class="ml-auto" /></SidebarHeader>
      <SidebarContent>
        <SidebarGroup><SidebarGroupContent><SidebarMenu>
          <SidebarMenuItem v-for="item in nav" :key="item.to">
            <SidebarMenuButton :is-active="route.path === item.to" as-child>
              <NuxtLink :to="item.to"><component :is="item.icon" /><span>{{ item.label }}</span></NuxtLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu></SidebarGroupContent></SidebarGroup>
      </SidebarContent>
    </Sidebar>

    <SidebarInset>
      <header class="sticky top-0 z-30 flex h-14 items-center gap-3 border-b border-border bg-card px-4">
        <span class="font-heading text-lg font-medium">Pháros</span>
        <span class="text-muted-foreground">·</span>
        <nav aria-label="Breadcrumb" class="text-sm">
          <span class="text-muted-foreground">Diseño</span>
          <span class="mx-1.5 text-muted-foreground">/</span>
          <span class="font-semibold text-foreground" aria-current="page">{{ crumbLeaf }}</span>
        </nav>
        <div class="ml-auto"><PlaygroundPanel /></div>
      </header>
      <main class="w-full max-w-[1280px] p-6"><NuxtPage /></main>
    </SidebarInset>
  </SidebarProvider>
</template>
```

Create `app/app.vue` = `<template><NuxtLayout><NuxtPage /></NuxtLayout></template>`.

**Verify P5:** shell renders with a collapsible icon-rail sidebar + topbar
breadcrumb; no `<h1>` anywhere.

## 9. Phase 6 — Control panel: `app/components/PlaygroundPanel.vue`

The actual "playground." A `Sheet` (drawer) opened from a topbar button, with:
**theme toggle**, **sub-brand selector** (radio list of `SUB_BRANDS`, locked one
badged "decidida"), a **custom-accent color input**, and the **mono A/B select**.

Spec (use `~/components/ui/{sheet,button,select,label,separator,badge}` +
`lucide` Palette/Sun/Moon):
- Trigger: `<Button variant="outline" size="sm">` with a Palette icon + "Marca".
- Theme: a Sun/Moon toggle button calling `pg.toggleTheme()`.
- Sub-brand: one clickable row per `SUB_BRANDS`; active = ring in `--primary`;
  show a `<Badge>` "decidida" when `locked`, else "propuesta". Click →
  `pg.setSubBrand(id)`.
- Custom accent: `<input type="color">` bound to call `pg.setCustomAccent($event)`
  + a "Limpiar" button → `pg.clearCustomAccent()`.
- Mono: a `<Select>` over `MONO_FONTS` → `pg.setMono(id)`.
- Footer note (Spanish): "Los colores de estado (éxito/alerta/error/info) NO
  cambian al cambiar el acento — son independientes de la marca (RFC 0008 Q4)."

**Verify P6:** changing sub-brand recolors buttons/sidebar/active states +
chart-1; toggling theme flips light/dark; the status pills (Phase 7) stay put.

## 10. Phase 7 — Component gallery: `app/pages/index.vue`

A single scrollable page showing the components so theme/accent changes are
visible. Sections (each in a `Card`), Spanish headings:
- **Botones**: Button variants — default, secondary, outline, ghost, destructive,
  + sizes + a disabled + one with a lucide icon.
- **Badges / estados**: `Badge` variants AND the **accent-independent status
  pills** built from the status tokens, e.g.
  `<span class="rounded-full px-2 py-0.5 text-xs bg-status-success-bg text-status-success">Conciliado</span>`
  for success/warning/error/info (these are the ones that must NOT move on
  re-accent — the live proof of Q4).
- **Formulario**: Input + Label + Select + Checkbox + Switch in a small form.
- **Tabla**: a `Table` with ~5 rows of fake finance data (montos with
  `font-mono tabular-nums`), one row `data-state="selected"`.
- **Tabs**: a `Tabs` with 2–3 panels.
- **Diálogo**: a `Dialog` triggered by a button.
- **Tipografía**: a block showing `font-heading` (Fraunces) heading, `font-sans`
  (Inter) body, `font-mono` sample numbers — so the font selector is visible.

**Verify P7:** all sections render; status pills use the status tokens (not
`--primary`).

## 11. Phase 8 — Charts: `app/pages/graficas.vue` + `app/components/PgCharts.client.vue`

`PgCharts.client.vue` = the verbatim @unovis component below (the `.client`
suffix keeps it off SSR; `build.transpile` is already set in Phase 2). Colors
come straight from `var(--chart-N)`.

```vue
<script setup lang="ts">
import { VisXYContainer, VisLine, VisAxis, VisCrosshair, VisTooltip, VisSingleContainer, VisDonut } from '@unovis/vue'
import { Line, Donut } from '@unovis/ts'

type Point = { month: string; ingresos: number; gastos: number }
const lineData: Point[] = [
  { month: 'Ene', ingresos: 120, gastos: 80 }, { month: 'Feb', ingresos: 150, gastos: 90 },
  { month: 'Mar', ingresos: 140, gastos: 110 }, { month: 'Abr', ingresos: 180, gastos: 100 },
  { month: 'May', ingresos: 210, gastos: 130 },
]
const x = (_d: Point, i: number) => i
const lineColors = ['var(--chart-1)', 'var(--chart-2)']
const xTickFormat = (i: number) => lineData[i]?.month ?? ''

type Slice = { label: string; value: number }
const donutData: Slice[] = [
  { label: 'Caja', value: 35 }, { label: 'Bancos', value: 25 }, { label: 'Cartera', value: 20 },
  { label: 'Inversiones', value: 12 }, { label: 'Otros', value: 8 },
]
const donutColor = (_d: Slice, i: number) => `var(--chart-${(i % 5) + 1})`
const total = donutData.reduce((s, d) => s + d.value, 0)
const lineTooltip = {
  [Line.selectors.point]: (d: Point) => `<div style="font-size:12px">${d.month}<br/>Ingresos: ${d.ingresos}<br/>Gastos: ${d.gastos}</div>`,
}
const donutTooltip = {
  [Donut.selectors.segment]: (d: { data: Slice }) => `<div style="font-size:12px"><strong>${d.data.label}</strong><br/>${d.data.value} (${Math.round((d.data.value / total) * 100)}%)</div>`,
}
</script>

<template>
  <div class="grid gap-8 md:grid-cols-2">
    <div class="rounded-lg border border-border p-4">
      <p class="mb-3 text-sm text-muted-foreground">Ingresos vs. gastos</p>
      <VisXYContainer :data="lineData" :height="280">
        <VisLine :x="x" :y="[(d:Point)=>d.ingresos, (d:Point)=>d.gastos]" :color="lineColors" />
        <VisAxis type="x" :tickFormat="xTickFormat" /><VisAxis type="y" />
        <VisCrosshair :color="lineColors" /><VisTooltip :triggers="lineTooltip" />
      </VisXYContainer>
    </div>
    <div class="rounded-lg border border-border p-4">
      <p class="mb-3 text-sm text-muted-foreground">Distribución de activos</p>
      <VisSingleContainer :data="donutData" :height="280">
        <VisDonut :value="(d:Slice)=>d.value" :color="donutColor" :arcWidth="40" :cornerRadius="4" :padAngle="0.02" :centralLabel="String(total)" centralSubLabel="Total" />
        <VisTooltip :triggers="donutTooltip" />
      </VisSingleContainer>
    </div>
  </div>
</template>
```

`app/pages/graficas.vue`:
```vue
<template>
  <ClientOnly>
    <PgCharts />
    <template #fallback><div class="h-72 animate-pulse rounded-md bg-muted" /></template>
  </ClientOnly>
</template>
```

**Verify P8:** `/graficas` shows a line + donut; switching sub-brand recolors
`--chart-1` (the first series / first donut segment).

## 12. Run & acceptance checklist (§10)

```bash
cd /Users/gczuluaga/dev/pharos-playground && pnpm dev   # http://localhost:3000
```

Drive the page and confirm ALL of:
- [ ] Shell renders: collapsible icon-rail sidebar + topbar breadcrumb, **no `<h1>`**.
- [ ] **Theme toggle** flips the whole UI light ↔ dark (`.dark` class on `<html>`), no FOUC on reload.
- [ ] **Sub-brand switch** (ERP → a placeholder) recolors buttons, sidebar active state, focus ring, and chart series 1 — i.e. `--primary` propagates.
- [ ] **Status pills do NOT change** when you switch the accent (the Q4 proof) — only the brand accent moves.
- [ ] **Custom accent** color input live-retints; "Limpiar" restores the preset.
- [ ] **Mono A/B** select swaps IBM Plex Mono ↔ JetBrains Mono in the typography + table number samples.
- [ ] **Charts** render (`/graficas`), themed from `--chart-1..5`, and recolor on accent change.
- [ ] No console errors; `pnpm build` succeeds (SSR-safe because charts are `.client`/`ClientOnly`).

Capture a screenshot of light+ERP, dark+ERP, and light+one placeholder as evidence.

## 13. Notes / future
- This is local-only (no remote). Future home: the `pharos-ui` shadcn-vue
  registry (RFC 0008 Q3) — the token contract here is the seed for that registry.
- Placeholders (`SUB_BRANDS` non-ERP) are intentionally unnamed/un-accented —
  they're what the SKuger session fills in; the playground is where you'll *see*
  the candidates before locking (Q1/Q6).
- When @unovis charts graduate, they become the shared chart components (Q11).
```
