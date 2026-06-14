---
status: superseded
superseded-by: brand-playground-build-plan.md (all content merged there 2026-06-14)
created: 2026-06-14
owner: gczuluaga
---

> **This plan has been merged into `brand-playground-build-plan.md` and is archived.**
> All phases, bug fixes (T4/T5/T6/T7), and the §9 acceptance checklist from this file
> now live in the build plan as Phases 10–15 and §13–15. Do not run this file —
> run the merged build plan instead.

# Pháros brand playground — tweaks plan (auto-runnable)

## 0. What this is + how to run it

Three operator-requested tweaks to the **existing** local app at
`/Users/gczuluaga/dev/pharos-playground/` (built by
`brand-playground-build-plan.md`):

1. **Marca panel → fixed in-view, resizable** — convert the `Sheet` overlay
   drawer into a panel pinned on the **right** of the content, side-by-side with
   the preview, with a **draggable resizer** + persisted width (the finance-lch
   `FacturaDrawerPanel` / `CausacionPanel` pattern).
2. **Topbar + sidebar → finance-lch look** — keep the vendored shadcn `Sidebar`
   (`collapsible="icon"`, the RFC reference shell) but restyle the **topbar** to
   finance-lch's pattern: real Pháros **logo SVG** + vertical divider + a
   **popover "parent-only" breadcrumb** + a right-side cluster (org name +
   theme toggle). On the **`.dark`-class substrate, NO cobol, shadcn tokens**.
3. **Richer fonts** — an **8-family monospace picker** + an **off-by-default
   "data font" toggle** that, when on, applies a separate data font (default
   JetBrains Mono) with `tabular-nums`/`slashed-zero` to all cifras — the live
   demonstration of the brand-book "JetBrains-for-data" split vs Q5's "one mono."

**Also fixes a latent bug** found while planning: the v1 font picker is a no-op.
`@theme inline { --font-mono: <literal stack> }` bakes the literal value into the
`.font-mono` utility, so the store's runtime `--font-mono` override never renders.
Phase 1 fixes this with a `*-stack` indirection so the picker (and the new data
axis) actually re-render the font. (Verified 2026-06-14: setting `--font-mono`
on `<html>` does not change the computed `font-family` of a `.font-mono` element.)

**How to auto-run with Sonnet:** open a Claude session (Sonnet, auto-accept
edits is fine) and paste:

> Execute the plan at `/Users/gczuluaga/dev/.github/plans/brand-playground-tweaks-plan.md`
> exactly, phase by phase, against the existing app at
> `/Users/gczuluaga/dev/pharos-playground/`. After each phase run its verification.
> At the end run `pnpm dev`, drive the page, and confirm the §9 acceptance
> checklist. Do not deviate from the embedded file contents — they encode locked
> RFC 0008 decisions. Don't push.

## 1. Locked invariants — DO NOT DRIFT (RFC 0008-cocreation-prep)

These were settled before this plan; nothing here may violate them:

- **Theming = `.dark` CLASS** on `<html>`, **light/dark only, NO cobol** (Q7).
  Do NOT introduce `[data-theme]` or a 3-way toggle even though finance-lch's
  real shell uses them — they are explicitly dropped.
- **Tokens = LEAN shadcn contract + accent-INDEPENDENT status palette** (Q4).
  Brand accent → `--primary` (+ `--ring`, `--sidebar-primary`, `--sidebar-ring`,
  `--chart-1`) only. Status `--status-*` tokens NEVER move with the accent. Use
  `--sidebar-*` / shadcn tokens for chrome — NOT finance-lch's `--nav-*`.
- **Shell = shadcn `Sidebar collapsible="icon"`** (lab-qc is the RFC shell
  reference; we keep it and only restyle the topbar). **NO page `<h1>`** — the
  breadcrumb's bold last segment is the title. **UI copy in Spanish** (neutral
  Colombian; no exclamations, no emojis — brand voice).
- **3-family system stays: Fraunces (display) · Inter (sans) · IBM Plex Mono
  (default mono)** (Q5). The richer mono set + data-font toggle are **playground
  exploration** — the sanctioned way to validate the mono "before final lock"
  and to let the team SEE the brand-book data-font split. The **default state
  must still be Q5**: mono = IBM Plex Mono, data font OFF (so one mono is used
  for everything until someone flips the toggle).
- **Charts = @unovis, `--chart-1..5`** (Q11), client-only. Unchanged.
- **Pilot-light red `#E4002B` is shared and never re-tinted** (brand book) — the
  logo SVGs already encode this; do not recolor them.
- Keep the v1 build fixes intact: `reka-ui@2.9.6`, the `typescript` devDep +
  `tsConfig.paths['reka-ui']`, `striptags` dep + `optimizeDeps.include`,
  `build.transpile` for @unovis, the FOUC guard script.

## 2. Prerequisites

- App already built per `brand-playground-build-plan.md` and booting on
  `http://localhost:3000`. `node >= 22`, `pnpm@10+`.
- Vendored shadcn-vue components present (confirmed): `popover`, `switch`,
  `select`, `label`, `badge`, `button`, `separator`, `sidebar`, `card`, `table`,
  `tabs`, `dialog`, `sheet` (sheet becomes unused after Phase 4 — leave it
  vendored, harmless).
- Default branch is `master`/`main` of the fresh local repo; **don't push**.

---

## 3. Phase 1 — Fonts foundation (fix the latent bug + register families)

### 3a. `nuxt.config.ts` — register all selectable families

Replace the entire `fonts.families` array body with this (all `provider: 'google'`,
verified on Google Fonts 2026-06-14). `families:` appears once in the file; replace
the whole `[ ... ]` body and leave every other key unchanged.

```ts
  fonts: {
    families: [
      { name: 'Fraunces',         weights: [400, 500],      provider: 'google' },
      { name: 'Inter',            weights: [400, 500, 600], provider: 'google' },
      // monospace picker (8)
      { name: 'IBM Plex Mono',    weights: [400, 500],      provider: 'google' },
      { name: 'JetBrains Mono',   weights: [400, 500],      provider: 'google' },
      { name: 'Source Code Pro',  weights: [400, 500],      provider: 'google' },
      { name: 'Fira Code',        weights: [400, 500],      provider: 'google' },
      { name: 'Roboto Mono',      weights: [400, 500],      provider: 'google' },
      { name: 'Red Hat Mono',     weights: [400, 500],      provider: 'google' },
      { name: 'Spline Sans Mono', weights: [400, 500],      provider: 'google' },
      { name: 'Martian Mono',     weights: [400, 500],      provider: 'google' },
      // extra data-font candidates
      { name: 'DM Mono',          weights: [400, 500],      provider: 'google' },
      { name: 'IBM Plex Sans',    weights: [400, 500, 600], provider: 'google' },
    ],
  },
```

(@nuxt/fonts emits `@font-face` for all; the browser only fetches the family the
active CSS var actually uses, so eager registration is fine.)

### 3b. `app/assets/css/main.css` — route fonts through overridable `*-stack` vars

**The bug:** runtime overrides only work if the utility reads `var(...)`. Mirror
how the color tokens work (`--color-primary: var(--primary)`).

**Edit 1 — add four stack vars to the `:root` block** (put them right after the
`--chart-5` line, before the closing `}` of `:root`):

```css
  /* font stacks — overridable at runtime (the mono + data picker write these) */
  --font-mono-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-data-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
```

(`--font-data-stack` defaults to the **mono** stack — data-font OFF = one mono,
per Q5. Sans/heading stay static, so they don't need stack vars.)

**Edit 2 — in the `@theme inline` block, replace the comment + 3 font lines.**
Find this exact 4-line block (the radius vars just below it stay intact):

```css
  /* 3-family font system (Q5) */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", "JetBrains Mono", monospace;
  --font-heading: "Fraunces", "Times New Roman", serif;
```

Replace it with these 5 lines (routes mono/data through the overridable vars):

```css
  /* 3-family system (Q5) + an overridable data slot (playground exploration) */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: var(--font-mono-stack);
  --font-data: var(--font-data-stack);
  --font-heading: "Fraunces", "Times New Roman", serif;
```

This makes `.font-mono` → `font-family: var(--font-mono-stack)` and creates a new
`.font-data` → `font-family: var(--font-data-stack)` utility, both runtime-overridable.

**Verify P1:** `pnpm dev` boots clean. In the browser console:
`getComputedStyle(document.querySelector('.font-mono')).fontFamily` includes IBM
Plex Mono; then `document.documentElement.style.setProperty('--font-mono-stack','"JetBrains Mono", monospace')`
→ the same query now reports JetBrains Mono (i.e. the override **renders**, unlike
before). Deterministic fallback if the webfont hasn't painted yet:
`getComputedStyle(document.documentElement).getPropertyValue('--font-mono-stack')`
reflects the override (the var write is deterministic even pre-paint). Stop the server.

---

## 4. Phase 2 — Store: richer fonts + data axis (`app/stores/playground.ts`)

Overwrite the file with **exactly** this. Changes vs v1: 8 `MONO_FONTS`, new
`DATA_FONTS`, `dataFontEnabled`/`dataFontId` state, `apply()` writes
`--font-mono-stack` + `--font-data-stack` (NOT `--font-mono`/`--font-data`), light
pref persistence. `SUB_BRANDS` is unchanged (ERP locked; rest placeholders for
SKuger). Theme state stays (the topbar toggle calls `toggleTheme`).

```ts
import { defineStore } from 'pinia'

export interface SubBrand {
  id: string
  name: string
  light: { accent: string; foreground: string }
  dark: { accent: string; foreground: string }
  locked: boolean
}

// ERP name + accent LOCKED (RFC 0008 Q1/Q6). Rest are PLACEHOLDERS for SKuger.
export const SUB_BRANDS: SubBrand[] = [
  { id: 'erp',         name: 'Pháros · Timón (ERP)',       light: { accent: '#003A70', foreground: '#ffffff' }, dark: { accent: '#A0D1CA', foreground: '#06121f' }, locked: true },
  { id: 'lis-clinico', name: 'LIS clínico — ? (LCH)',      light: { accent: '#782F40', foreground: '#ffffff' }, dark: { accent: '#d59aa8', foreground: '#2a0a12' }, locked: false },
  { id: 'lis-deport',  name: 'LIS deportivo — ? (Biuman)', light: { accent: '#326295', foreground: '#ffffff' }, dark: { accent: '#8fb3d9', foreground: '#06121f' }, locked: false },
  { id: 'admisiones',  name: 'Admisiones — ?',             light: { accent: '#1b6b5a', foreground: '#ffffff' }, dark: { accent: '#4cd1b0', foreground: '#06121f' }, locked: false },
  { id: 'crm',         name: 'CRM — ? (¿Gente?)',          light: { accent: '#7a5d00', foreground: '#ffffff' }, dark: { accent: '#e6c34d', foreground: '#2e2606' }, locked: false },
]

// 8 monos verified on Google Fonts. Q5 default = IBM Plex Mono; the rest explore
// the pick before final lock (the playground is the sanctioned validation surface).
export const MONO_FONTS = [
  { id: 'ibm',       label: 'IBM Plex Mono (Q5 default)', stack: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'jetbrains', label: 'JetBrains Mono',             stack: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'source',    label: 'Source Code Pro',            stack: '"Source Code Pro", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'fira',      label: 'Fira Code',                  stack: '"Fira Code", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'roboto',    label: 'Roboto Mono',                stack: '"Roboto Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'redhat',    label: 'Red Hat Mono',               stack: '"Red Hat Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'spline',    label: 'Spline Sans Mono',           stack: '"Spline Sans Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'martian',   label: 'Martian Mono',               stack: '"Martian Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
]

// Data-font candidates — only applied when dataFontEnabled. Brand book mandates
// JetBrains Mono + tabular-nums for cifras (BRAND.md §4.4); Inter/Plex Sans are
// the proportional-with-tabular-figures alternatives.
export const DATA_FONTS = [
  { id: 'jetbrains', label: 'JetBrains Mono (brand book — exploración)', stack: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'ibm-mono',  label: 'IBM Plex Mono',               stack: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'dm-mono',   label: 'DM Mono',                     stack: '"DM Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'inter',     label: 'Inter (tabular)',             stack: '"Inter", system-ui, sans-serif' },
  { id: 'ibm-sans',  label: 'IBM Plex Sans (tabular)',     stack: '"IBM Plex Sans", system-ui, sans-serif' },
]

const PREFS_KEY = 'pharos-pg-prefs'

export const usePlayground = defineStore('playground', () => {
  const theme = ref<'light' | 'dark'>('light')
  const subBrandId = ref('erp')
  const customAccent = ref<string | null>(null)
  const monoId = ref('ibm')
  const dataFontEnabled = ref(false)
  const dataFontId = ref('jetbrains')

  const subBrand = computed(() => SUB_BRANDS.find(s => s.id === subBrandId.value) ?? SUB_BRANDS[0])

  function apply() {
    if (!import.meta.client) return
    const el = document.documentElement
    el.classList.toggle('dark', theme.value === 'dark')
    const tone = theme.value === 'dark' ? subBrand.value.dark : subBrand.value.light
    const accent = customAccent.value ?? tone.accent
    const fg = customAccent.value ? '#ffffff' : tone.foreground
    // brand accent -> --primary + ring + sidebar-primary + chart-1 (NOT shadcn --accent, NOT status)
    for (const v of ['--primary', '--ring', '--sidebar-primary', '--sidebar-ring', '--chart-1']) {
      el.style.setProperty(v, accent)
    }
    el.style.setProperty('--primary-foreground', fg)
    el.style.setProperty('--sidebar-primary-foreground', fg)
    // fonts — write the *-stack vars the utilities read (Phase 1 indirection)
    const mono = MONO_FONTS.find(m => m.id === monoId.value) ?? MONO_FONTS[0]
    el.style.setProperty('--font-mono-stack', mono.stack)
    const data = DATA_FONTS.find(d => d.id === dataFontId.value) ?? DATA_FONTS[0]
    // OFF => data cells fall back to the single mono (Q5 "one mono")
    el.style.setProperty('--font-data-stack', dataFontEnabled.value ? data.stack : mono.stack)
    // persist
    localStorage.setItem('pharos-pg-theme', theme.value)
    localStorage.setItem(PREFS_KEY, JSON.stringify({
      subBrandId: subBrandId.value,
      monoId: monoId.value,
      dataFontEnabled: dataFontEnabled.value,
      dataFontId: dataFontId.value,
    }))
  }

  function setSubBrand(id: string) { subBrandId.value = id; customAccent.value = null; apply() }
  function setCustomAccent(hex: string) { customAccent.value = hex; apply() }
  function clearCustomAccent() { customAccent.value = null; apply() }
  function toggleTheme() { theme.value = theme.value === 'dark' ? 'light' : 'dark'; apply() }
  function setMono(id: string) { monoId.value = id; apply() }
  function setDataFont(id: string) { dataFontId.value = id; apply() }
  function setDataFontEnabled(on: boolean) { dataFontEnabled.value = on; apply() }

  function init() {
    if (import.meta.client) {
      theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
      try {
        const p = JSON.parse(localStorage.getItem(PREFS_KEY) ?? '{}')
        if (p.subBrandId) subBrandId.value = p.subBrandId
        if (p.monoId) monoId.value = p.monoId
        if (typeof p.dataFontEnabled === 'boolean') dataFontEnabled.value = p.dataFontEnabled
        if (p.dataFontId) dataFontId.value = p.dataFontId
      } catch { /* ignore malformed prefs */ }
    }
    apply()
  }

  return {
    theme, subBrandId, customAccent, monoId, dataFontEnabled, dataFontId, subBrand,
    setSubBrand, setCustomAccent, clearCustomAccent, toggleTheme,
    setMono, setDataFont, setDataFontEnabled, init, apply,
  }
})
```

**Verify P2:** `pnpm dev` still boots clean; optionally run `pnpm exec nuxi typecheck`
for the store (the `typescript` devDep is present). Note a clean boot alone does NOT
prove the store compiles — no page imports it until Phase 5, which is where the real
proof lands (the panel imports `MONO_FONTS`/`DATA_FONTS`). No visual change yet. Stop the server.

---

## 5. Phase 3 — Real Pháros logo (`public/logos/` + `AppLogo.vue`)

### 5a. Copy the brand SVGs into `public/`

```bash
cd /Users/gczuluaga/dev/pharos-playground
mkdir -p public/logos
cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-navbar-light.svg public/logos/
cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-navbar-dark.svg  public/logos/
cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-icon-light.svg   public/logos/
cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-icon-dark.svg    public/logos/
```

### 5b. `app/components/AppLogo.vue` (new)

Theme-swap with pure CSS (`.dark` class on `<html>`) — no JS, snapshot-safe. The
light/dark SVGs already carry the correct (never-recolored) wordmark + pilot dot.

```vue
<script setup lang="ts">
withDefaults(defineProps<{ variant?: 'navbar' | 'icon' }>(), { variant: 'navbar' })
</script>

<template>
  <span class="inline-flex items-center" aria-label="Pháros">
    <img :src="`/logos/pharos-${variant}-light.svg`" alt="Pháros"
         class="block h-7 w-auto dark:hidden" />
    <img :src="`/logos/pharos-${variant}-dark.svg`" alt="Pháros"
         class="hidden h-7 w-auto dark:block" />
  </span>
</template>
```

**Verify P3:** `ls public/logos` shows 4 SVGs; component compiles (used in Phase 4).

---

## 6. Phase 4 — Layout: finance-lch topbar + resizable Marca grid (`app/layouts/default.vue`)

Overwrite with **exactly** this. It keeps the shadcn `Sidebar collapsible="icon"`,
restyles the topbar to finance-lch's pattern (logo + divider + popover breadcrumb
+ right cluster with theme toggle), and hosts the now-block `<PlaygroundPanel>` in
a 3-track grid (`preview | resizer | panel`) with a draggable resizer + persisted
width. The preview region is a `<div>` (NOT `<main>` — `SidebarInset` is already a
`<main>`; do not nest).

```vue
<script setup lang="ts">
import { Sun, Moon, LayoutGrid, BarChart3, ChevronDown } from 'lucide-vue-next'
import AppLogo from '~/components/AppLogo.vue'
import PlaygroundPanel from '~/components/PlaygroundPanel.vue'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'

const route = useRoute()
const pg = usePlayground()

const nav = [
  { label: 'Componentes', to: '/', icon: LayoutGrid },
  { label: 'Gráficas', to: '/graficas', icon: BarChart3 },
]
const crumbLeaf = computed(() => nav.find(n => n.to === route.path)?.label ?? 'Componentes')

// ── resizable Marca panel (finance-lch Factura/Causación pattern) ──
const PANEL_KEY = 'pharos-pg-panel-pct'
const DEFAULT_PCT = 26
const panelPct = ref(DEFAULT_PCT)
const gridRef = ref<HTMLElement | null>(null)
let dragging = false

function onMove(e: PointerEvent) {
  if (!dragging || !gridRef.value) return
  const r = gridRef.value.getBoundingClientRect()
  // panel is on the RIGHT: its width % = (right edge - cursor) / total width
  panelPct.value = Math.min(50, Math.max(18, ((r.right - e.clientX) / r.width) * 100))
}
function endResize() {
  if (!dragging) return
  dragging = false
  window.removeEventListener('pointermove', onMove)
  window.removeEventListener('pointerup', endResize)
  localStorage.setItem(PANEL_KEY, String(Math.round(panelPct.value)))
}
function startResize(e: PointerEvent) {
  dragging = true
  ;(e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId)
  window.addEventListener('pointermove', onMove)
  window.addEventListener('pointerup', endResize)
}
function resetPanel() {
  panelPct.value = DEFAULT_PCT
  localStorage.setItem(PANEL_KEY, String(DEFAULT_PCT))
}

onMounted(() => {
  pg.init()
  const saved = Number(localStorage.getItem(PANEL_KEY))
  if (saved >= 18 && saved <= 50) panelPct.value = saved
})
</script>

<template>
  <SidebarProvider>
    <Sidebar collapsible="icon">
      <SidebarHeader class="h-14 justify-center px-3">
        <AppLogo variant="icon" />
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Diseño</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem v-for="item in nav" :key="item.to">
                <SidebarMenuButton :is-active="route.path === item.to" as-child>
                  <NuxtLink :to="item.to">
                    <component :is="item.icon" />
                    <span>{{ item.label }}</span>
                  </NuxtLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>

    <SidebarInset class="flex h-svh flex-col overflow-hidden">
      <!-- topbar: finance-lch pattern on the .dark/shadcn substrate -->
      <header class="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-card px-4">
        <SidebarTrigger />
        <span class="h-5 w-px shrink-0 bg-border" />
        <AppLogo class="hidden md:inline-flex" />
        <span class="hidden h-5 w-px shrink-0 bg-border md:block" />
        <nav aria-label="Breadcrumb" class="text-sm">
          <ol class="flex items-center gap-1.5">
            <li>
              <Popover>
                <PopoverTrigger class="inline-flex items-center gap-1 text-muted-foreground transition-colors hover:text-foreground">
                  Diseño
                  <ChevronDown class="size-3.5" />
                </PopoverTrigger>
                <PopoverContent align="start" :side-offset="6" class="w-56 p-1.5">
                  <NuxtLink v-for="item in nav" :key="item.to" :to="item.to"
                    class="block rounded-md px-2 py-1.5 text-sm transition-colors hover:bg-accent"
                    :class="route.path === item.to ? 'font-semibold text-foreground' : 'text-muted-foreground'">
                    {{ item.label }}
                  </NuxtLink>
                </PopoverContent>
              </Popover>
            </li>
            <li aria-hidden="true"><span class="text-muted-foreground">/</span></li>
            <li><span class="font-semibold text-foreground" aria-current="page">{{ crumbLeaf }}</span></li>
          </ol>
        </nav>
        <div class="ml-auto flex items-center gap-3">
          <span class="hidden whitespace-nowrap text-sm text-muted-foreground lg:inline">Laboratorio Clínico Hematológico</span>
          <span class="hidden h-5 w-px shrink-0 bg-border lg:block" />
          <button type="button" aria-label="Cambiar tema"
            class="inline-flex size-9 items-center justify-center rounded-full border border-border bg-muted text-foreground transition-colors hover:bg-accent"
            @click="pg.toggleTheme()">
            <Moon v-if="pg.theme === 'light'" class="size-[18px]" />
            <Sun v-else class="size-[18px]" />
          </button>
        </div>
      </header>

      <!-- content: preview | draggable resizer | fixed Marca panel -->
      <div ref="gridRef" class="grid min-h-0 flex-1 overflow-hidden"
        :style="`grid-template-columns: minmax(0,1fr) 6px ${panelPct}%`">
        <div class="min-w-0 overflow-y-auto p-6">
          <NuxtPage />
        </div>
        <div role="separator" aria-orientation="vertical" aria-label="Redimensionar panel"
          class="relative cursor-col-resize touch-none select-none bg-border transition-colors hover:bg-primary"
          @pointerdown="startResize" @dblclick="resetPanel">
          <span class="pointer-events-none absolute left-1/2 top-1/2 h-7 w-0.5 -translate-x-1/2 -translate-y-1/2 rounded bg-muted-foreground/40" />
        </div>
        <PlaygroundPanel class="min-w-0 overflow-y-auto border-l border-border bg-card" />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
```

> Note: `app/app.vue` stays `<template><NuxtLayout><NuxtPage /></NuxtLayout></template>`.
> The theme toggle now lives in the topbar (finance-lch faithful); it is removed
> from the panel in Phase 5. The playground still live-switches theme (Q5 satisfied).
> The explicit `Popover` import is intentional and harmless (Nuxt auto-import would
> also resolve it); do NOT "fix" the apparent inconsistency by importing the other
> `ui/*` components — `Sidebar*`, `SidebarTrigger`, etc. all resolve via auto-import.

**Verify P4:** boots; topbar shows the Pháros logo + "Diseño ▾ / Componentes"
breadcrumb (the "Diseño" chip opens a popover listing both pages) + a round theme
toggle on the right; the Marca panel sits pinned on the right; dragging the 6px
divider resizes it and the width survives reload; double-click resets to 26%.

---

## 7. Phase 5 — Marca panel as a fixed block (`app/components/PlaygroundPanel.vue`)

Overwrite with **exactly** this. No more `Sheet`/trigger — it's a plain `<aside>`
the layout mounts inline. Theme control removed (now in topbar). Adds the **mono
picker (8)**, the **data-font toggle + picker**, keeps sub-brand + custom accent +
the Q4 status note. shadcn `ui/*` components are Nuxt auto-imported (no import
needed); only the store is imported.

```vue
<script setup lang="ts">
import { SUB_BRANDS, MONO_FONTS, DATA_FONTS, usePlayground } from '~/stores/playground'
const pg = usePlayground()
</script>

<template>
  <aside class="flex h-full flex-col gap-5 p-4">
    <header>
      <h2 class="font-heading text-base font-medium">Control de marca</h2>
      <p class="text-xs text-muted-foreground">Explora el sistema de diseño Pháros</p>
    </header>

    <!-- Sub-marca -->
    <section>
      <Label class="mb-2 block text-xs font-medium uppercase tracking-wide text-muted-foreground">Sub-marca</Label>
      <div class="flex flex-col gap-1.5">
        <button v-for="brand in SUB_BRANDS" :key="brand.id" type="button"
          class="flex items-center justify-between gap-2 rounded-md border px-3 py-2 text-left text-sm transition-colors hover:bg-accent"
          :class="pg.subBrandId === brand.id ? 'border-primary ring-1 ring-primary' : 'border-border'"
          @click="pg.setSubBrand(brand.id)">
          <span>{{ brand.name }}</span>
          <Badge :variant="brand.locked ? 'default' : 'secondary'" class="shrink-0 text-xs">
            {{ brand.locked ? 'decidida' : 'propuesta' }}
          </Badge>
        </button>
      </div>
    </section>

    <Separator />

    <!-- Acento personalizado -->
    <section>
      <Label class="mb-2 block text-xs font-medium uppercase tracking-wide text-muted-foreground">Acento personalizado</Label>
      <div class="flex items-center gap-2">
        <input type="color"
          :value="pg.customAccent ?? (pg.theme === 'dark' ? pg.subBrand.dark.accent : pg.subBrand.light.accent)"
          class="h-8 w-10 cursor-pointer rounded border border-border bg-transparent"
          @input="pg.setCustomAccent(($event.target as HTMLInputElement).value)" />
        <Button variant="ghost" size="sm" @click="pg.clearCustomAccent()">Limpiar</Button>
      </div>
    </section>

    <Separator />

    <!-- Fuentes -->
    <section class="flex flex-col gap-3">
      <Label class="block text-xs font-medium uppercase tracking-wide text-muted-foreground">Fuentes</Label>

      <div class="flex flex-col gap-1.5">
        <Label class="text-xs text-muted-foreground">Mono</Label>
        <Select :model-value="pg.monoId" @update:model-value="pg.setMono($event as string)">
          <SelectTrigger class="w-full"><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem v-for="f in MONO_FONTS" :key="f.id" :value="f.id">{{ f.label }}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div class="flex items-center justify-between gap-2 rounded-md border border-border px-3 py-2">
        <Label for="data-toggle" class="text-sm font-normal">Fuente de datos aparte</Label>
        <Switch id="data-toggle" :model-value="pg.dataFontEnabled"
          @update:model-value="pg.setDataFontEnabled($event)" />
      </div>

      <div class="flex flex-col gap-1.5" :class="pg.dataFontEnabled ? '' : 'pointer-events-none opacity-50'">
        <Label class="text-xs text-muted-foreground">Datos (cifras)</Label>
        <Select :model-value="pg.dataFontId" @update:model-value="pg.setDataFont($event as string)">
          <SelectTrigger class="w-full" :disabled="!pg.dataFontEnabled"><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem v-for="f in DATA_FONTS" :key="f.id" :value="f.id">{{ f.label }}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <p class="text-xs leading-relaxed text-muted-foreground">
        Apagado = un solo mono (RFC 0008 Q5). Encendido = fuente de datos aparte con
        <span class="font-data tabular-nums slashed-zero">tabular-nums</span> y cero con barra,
        como el brand book (JetBrains Mono para cifras).
      </p>
    </section>

    <Separator />

    <p class="text-xs leading-relaxed text-muted-foreground">
      Los colores de estado (éxito/alerta/error/info) <strong>NO cambian</strong> al
      cambiar el acento — son independientes de la marca (RFC 0008 Q4).
    </p>
  </aside>
</template>
```

> reka-ui 2.9.6 `Switch` uses `modelValue` / `update:modelValue` (verified against
> `SwitchRootProps`) — the `:model-value`/`@update:model-value` binding above is
> correct. Do NOT switch to `:checked`/`@update:checked`: that is not a valid prop
> on this version and would silently fail to bind (the toggle renders but never
> updates the store).

**Verify P5:** panel renders inline (no overlay/backdrop). Switching **Mono**
visibly changes the typography + table cifras (the Phase-1 fix made this real).
Toggling **Fuente de datos aparte** ON enables the data Select and re-renders the
cifras in the data font; OFF returns them to the mono. Sub-brand + accent +
Limpiar behave as before. Status pills do NOT move on accent change.

---

## 8. Phase 6 — Gallery: route cifras through the data font (`app/pages/index.vue`)

Two small edits so the data-font axis is visible where numbers live.

**Edit 1 — Tabla financiera numeric cell.** A **SUBSTRING** replace only — the
find-text is part of a longer `<TableCell>` line that also carries a
`:class="row.monto < 0 ? 'text-status-error' : ''"` color binding; do NOT touch that
binding.

- find: `class="text-right font-mono tabular-nums"`
- replace: `class="text-right font-data tabular-nums slashed-zero lining-nums"`

**Edit 2 — Tipografía card.** Replace the single mono sample `<p>` (the only
`<p class="font-mono` in the file) with a mono line **and** a data line so both
faces are visible.

- find (verbatim, including the 8 leading spaces):

```vue
        <p class="font-mono text-sm tabular-nums">IBM Plex Mono · 0123456789 · $1.234.567 · ─── monoespaciado</p>
```

- replace with:

```vue
        <p class="font-mono text-sm">Mono · IBM Plex Mono · etiquetas · ABCDEF · {} [] =&gt;</p>
        <p class="font-data tabular-nums slashed-zero lining-nums text-sm">Datos · 0123456789 · $1.234.567 · 0 con barra (cero/letra O)</p>
```

(Leave the Fraunces `font-heading` and Inter `font-sans` sample lines as they are.)

**Verify P6:** the table's Monto column and the new "Datos" line change font when
the data toggle/picker change; with the toggle OFF they match the selected mono.

---

## 9. Run & acceptance checklist

```bash
cd /Users/gczuluaga/dev/pharos-playground && pnpm dev   # http://localhost:3000
```

Drive the page and confirm ALL of:

- [ ] **Topbar (finance-lch look):** Pháros **logo SVG** (swaps light/dark with
      the theme) + vertical divider + **"Diseño ▾ / Componentes"** breadcrumb where
      the "Diseño" chip opens a **popover** listing both pages; right side shows the
      org name + a round **theme toggle**. **No page `<h1>`.**
- [ ] **Sidebar** is still the shadcn `Sidebar collapsible="icon"`; the topbar
      `SidebarTrigger` collapses it to the icon rail and back.
- [ ] **Marca panel is fixed in-view on the right** (no overlay/backdrop), pinned
      full-height with its own scroll; **dragging the 6px divider resizes it**,
      width **persists across reload**, double-click resets to 26%.
- [ ] **Theme toggle** (topbar) flips the whole UI light ↔ dark (`.dark` on
      `<html>`), no FOUC on reload. **No cobol option anywhere.**
- [ ] **Sub-brand switch** recolors buttons, sidebar active state, focus ring, and
      chart series 1 (`--primary` propagates); **status pills do NOT move** (Q4).
- [ ] **Custom accent** live-retints; "Limpiar" restores the preset.
- [ ] **Mono picker (8 families)** visibly changes the typography sample AND the
      table cifras — i.e. the Phase-1 indirection works (this was broken in v1).
- [ ] **Data-font toggle:** OFF → cifras use the selected mono (one mono, Q5);
      ON → cifras switch to the chosen data font (default JetBrains Mono) with
      `tabular-nums`/`slashed-zero`. The data Select is disabled while OFF.
- [ ] **Charts** (`/graficas`) render and recolor on accent change; breadcrumb
      leaf reads "Gráficas".
- [ ] No console errors; **`pnpm build` succeeds** (SSR-safe — charts stay
      `.client`/`ClientOnly`; the resizer + font logic are client-guarded).

Capture screenshots as evidence: (1) light + ERP, (2) dark + ERP, (3) light +
a placeholder sub-brand, (4) data-font toggle ON showing JetBrains cifras vs OFF,
(5) the panel resized narrow + wide.

### 9a. Q9 snapshot determinism (required guard)

RFC 0008 Q9 wants Playwright visual-regression snapshots of this playground across
themes/accents. The resizable panel and the persisted prefs make state sticky, so
snapshots MUST run from a neutralized state — never whatever a human last left:

- Before each snapshot, seed/clear localStorage so the panel + brand are at
  canonical defaults, e.g. a Playwright `addInitScript`:

  ```js
  await page.addInitScript(() => {
    localStorage.removeItem('pharos-pg-panel-pct')    // -> DEFAULT_PCT (26)
    localStorage.removeItem('pharos-pg-prefs')        // -> ERP / IBM Plex Mono / data-font OFF
    localStorage.setItem('pharos-pg-theme', 'light')  // set explicitly per snapshot variant
  })
  ```

- The panel's **default width (26%) is the canonical snapshot width**; dragging the
  resizer is a manual-exploration affordance only and is NOT part of the snapshot
  matrix. Mono/data-font/accent are likewise set explicitly per snapshot variant,
  never inherited from a prior session. This keeps the fixed panel deterministic
  across themes/accents per Q9.

## 10. Out of scope / notes

- The brand-book "data font" (JetBrains Mono) and Q5's "one mono" genuinely
  conflict; this plan does **not** resolve it — it makes the playground show both
  so SKuger can decide. Default stays Q5 (one mono, toggle off).
- finance-lch's real shell uses `[data-theme]` + cobol + `--nav-*`; we deliberately
  adopt only its **look/structure** on the locked `.dark`/shadcn-token substrate.
- Still local-only; don't push. Future home: the `pharos-ui` shadcn-vue registry
  (RFC 0008 Q3) — the resizable-panel + font-token work seeds it.
