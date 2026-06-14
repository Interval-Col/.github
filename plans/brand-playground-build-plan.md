---
status: active
created: 2026-06-13
updated: 2026-06-14
owner: gczuluaga
tracking-issue: Interval-Col/.github#27
intent: auto-runnable by a Sonnet coding agent — single source of truth (v1 build + v2 tweaks merged)
relates-to: RFC 0008 Q4/Q5/Q6/Q7/Q9/Q11
supersedes: brand-playground-tweaks-plan.md (merged here; that file is now archived)
---

# Pháros brand playground — complete build plan (v1 + v2 tweaks)

## 0. What this is + how to run it

A **local-only Nuxt 4 app** that renders the shared Pháros app-shell + a component
gallery + sample charts, with a **fixed right-side control panel** that live-switches
**accent (per sub-brand) · theme (light/dark) · mono font (8 families) · data font
(off/on)** — so the team can *see* the design system re-theme before locking the open
brand decisions. The **code-first validation surface** RFC 0008 implies for Q5 (mono
pick), Q6 (accent candidates), Q7 (themes), Q11 (charts), and the brand-book
JetBrains-for-data split.

**How to auto-run with Sonnet:** open a Claude session and paste:

> Execute the plan at `/Users/gczuluaga/dev/.github/plans/brand-playground-build-plan.md`
> exactly, phase by phase. Build at `/Users/gczuluaga/dev/pharos-playground/`.
> After each phase run its verification. At the end run `pnpm dev` and confirm the
> §11 acceptance checklist. Do not deviate from the embedded file contents — they
> encode locked RFC 0008 decisions. Don't push.

**Current state (2026-06-14):** the app is built and all phases below are complete.
Phases 0–9 produced v1; Phases 10–15 + bug-fixes produced the current v2 state.
A fresh run from Phase 0 reproduces the current app.

---

## 1. Locked invariants — DO NOT DRIFT (RFC 0008-cocreation-prep)

- **Theming = `.dark` CLASS** on `<html>`, light/dark only, **NO cobol** (Q7).
  Do NOT introduce `[data-theme]`. Theme toggle lives in the **topbar**, not the panel.
- **Token contract = LEAN shadcn + accent-INDEPENDENT status palette** (Q4).
  Brand accent → `--primary` (+ `--ring`, `--sidebar-primary`, `--sidebar-ring`,
  `--chart-1`) only. Status `--status-*` tokens NEVER move with the accent.
  Use `--sidebar-*` / shadcn tokens for chrome — NOT `--nav-*`.
- **Shell = shadcn `Sidebar collapsible="icon"`** (the RFC reference shell).
  **NO page `<h1>`** — the breadcrumb's bold leaf is the title.
  **UI copy in Spanish** (neutral Colombian; no exclamations, no emojis).
- **3-family font system (Q5):** Fraunces (display/wordmark) · Inter (sans UI) ·
  IBM Plex Mono (default mono). The richer picker is **playground exploration
  before final Q5 lock**. Default state MUST be Q5 (mono = IBM Plex Mono, data font OFF).
- **Charts = @unovis, `--chart-1..5`** (Q11), client-only (`.client.vue` + `ClientOnly`).
- **Pilot-light red `#E4002B` is never re-tinted** (brand book) — it lives in the SVGs.
- Keep v1 build fixes intact: `reka-ui@2.9.6` + `tsConfig.paths['reka-ui']`,
  `striptags` dep + `optimizeDeps.include`, `build.transpile` for @unovis, FOUC guard.
- `reka-ui` 2.9.6 Switch: use `modelValue`/`update:modelValue` — `:checked` does not exist.

## 2. Prerequisites

- Build dir: **`/Users/gczuluaga/dev/pharos-playground/`** (fresh).
- `node >= 22`, `pnpm@10+`.
- Brand SVGs: `/Users/gczuluaga/dev/.github/brands/pharos_brand/` (4 files: navbar/icon × light/dark).

---

## 3. Phase 0 — Scaffold

```bash
cd /Users/gczuluaga/dev
pnpm create nuxt@latest pharos-playground   # minimal, pnpm
cd pharos-playground
git init -q

pnpm add -D tailwindcss @tailwindcss/vite tw-animate-css
pnpm dlx nuxi@latest module add shadcn-nuxt
pnpm add @pinia/nuxt pinia @nuxt/fonts
pnpm add @vueuse/core lucide-vue-next class-variance-authority clsx tailwind-merge
pnpm add reka-ui@2.9.6        # pin — 2.9.10 breaks Vue SFC type inference
pnpm add -D typescript        # ensures TS ≥5.5 for reka-ui resolution
pnpm add @unovis/vue@1.6.5 @unovis/ts@1.6.5
pnpm add striptags            # @unovis/ts CJS dep — explicit for Vite 7 pre-bundle

pnpm dlx nuxi prepare   # generates .nuxt types before shadcn init
```

**Verify P0:** `pnpm dev` boots the default Nuxt page.

---

## 4. Phase 1 — Token contract: `app/assets/css/main.css`

Write **exactly** this. The `--font-mono-stack`/`--font-data-stack` in `:root` are
the vars the font picker writes at runtime. `@theme inline` routes utilities through
them so runtime overrides render (the `var()` indirection — without it, `@theme inline`
bakes literal font names at build time and runtime `setProperty` has no effect).
The `.fonts-preload` class lists all 10 picker fonts in a `font-family` property so
`@nuxt/fonts` generates `@font-face` for each; the class is never applied.

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

  /* font stacks — overridable at runtime (the picker writes --font-*-stack) */
  --font-mono-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-data-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
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

  /* 3-family system (Q5) + an overridable data slot (playground exploration) */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: var(--font-mono-stack);
  --font-data: var(--font-data-stack);
  --font-heading: "Fraunces", "Times New Roman", serif;

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

/* font-picker preload — never applied; @nuxt/fonts scans font-family for @font-face gen */
.fonts-preload {
  font-family: "JetBrains Mono", "Source Code Pro", "Fira Code", "Roboto Mono",
               "Red Hat Mono", "Spline Sans Mono", "Martian Mono", "DM Mono",
               "IBM Plex Sans", ui-monospace, monospace;
}

@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground font-sans; }
}
```

**Verify P1:** CSS parses clean; the `var()` indirection means `.font-mono` and
`.font-data` utilities resolve at runtime so `setProperty('--font-mono-stack', ...)` on
`<html>` immediately changes the computed font-family of `.font-mono` elements.

---

## 5. Phase 2 — `nuxt.config.ts`

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  modules: ['@pinia/nuxt', 'shadcn-nuxt', '@nuxt/fonts'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: { include: ['striptags'] },
  },
  // @unovis touches the DOM at import; keep its ESM transpiled (still render client-only).
  build: { transpile: ['@unovis/vue', '@unovis/ts'] },
  shadcn: { prefix: '', componentDir: './app/components/ui' },
  fonts: {
    families: [
      { name: 'Fraunces',         weights: [400, 500],      provider: 'google' },
      { name: 'Inter',            weights: [400, 500, 600], provider: 'google' },
      // monospace picker (8) — global:true forces @font-face even if not in static CSS
      { name: 'IBM Plex Mono',    weights: [400, 500],      provider: 'google', global: true },
      { name: 'JetBrains Mono',   weights: [400, 500],      provider: 'google', global: true },
      { name: 'Source Code Pro',  weights: [400, 500],      provider: 'google', global: true },
      { name: 'Fira Code',        weights: [400, 500],      provider: 'google', global: true },
      { name: 'Roboto Mono',      weights: [400, 500],      provider: 'google', global: true },
      { name: 'Red Hat Mono',     weights: [400, 500],      provider: 'google', global: true },
      { name: 'Spline Sans Mono', weights: [400, 500],      provider: 'google', global: true },
      { name: 'Martian Mono',     weights: [400, 500],      provider: 'google', global: true },
      // data-font candidates
      { name: 'DM Mono',          weights: [400, 500],      provider: 'google', global: true },
      { name: 'IBM Plex Sans',    weights: [400, 500, 600], provider: 'google', global: true },
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
  typescript: {
    tsConfig: {
      compilerOptions: {
        paths: {
          'reka-ui': ['./node_modules/reka-ui/dist/index.d.ts'],
        },
      },
    },
  },
})
```

> **@nuxt/fonts + picker fonts note:** `@nuxt/fonts` only generates `@font-face` for
> fonts it detects in CSS. Without `global: true` AND the `.fonts-preload` class,
> picker fonts would fall back to system fonts. Both are required for reliable
> `@font-face` generation across dev cold-starts. A **cold restart** (with cleared
> `.nuxt/` and font cache) is required after these changes take effect.

**Verify P2:** after a cold start (`rm -rf .nuxt && pnpm dev`), the browser shows
`@font-face` rules for all 10 picker fonts (check via DevTools → Sources, or
`document.fonts` in console).

---

## 6. Phase 3 — shadcn-vue init + components

```bash
pnpm dlx shadcn-vue@latest init    # new-york, zinc, app/assets/css/main.css, prefix "", lucide
# IMPORTANT: if init offers to overwrite main.css → DECLINE; then restore Phase 1 CSS exactly.
pnpm dlx shadcn-vue@latest add button badge input label select checkbox switch \
  dialog table tabs card separator tooltip sidebar breadcrumb popover sheet
```

`app/lib/utils.ts` (created by init):
```ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

If `shadcn-vue add` injects a Google Fonts `@import url(...)` into `main.css`, remove
it — @nuxt/fonts owns font loading.

**Verify P3:** `ls app/components/ui` shows the added components. `main.css` still
has the Phase-1 content.

---

## 7. Phase 4 — Store: `app/stores/playground.ts`

Writes brand-accent + font overrides as inline CSS vars on `<html>`. Status palette
is deliberately untouched (accent-independence proof, Q4).

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

// 8 monos verified on Google Fonts. Q5 default = IBM Plex Mono.
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

// Pull the primary family ("Martian Mono") out of a stack string and ask the browser
// to fetch it (400 + 500). Fire-and-forget: the page repaints when the face arrives.
// REQUIRED — without this, dynamically switching --font-*-stack never triggers
// @nuxt/fonts' lazy @font-face, so picked fonts silently fall back to system mono and
// the picker looks dead. (See trap T8.)
function ensureFontLoaded(stack: string) {
  if (!import.meta.client || !document.fonts?.load) return
  const family = stack.match(/"([^"]+)"/)?.[1]
  if (!family) return
  document.fonts.load(`400 1rem "${family}"`).catch(() => {})
  document.fonts.load(`500 1rem "${family}"`).catch(() => {})
}

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
    // fonts — write the *-stack vars the utilities read (var() indirection, Phase 1)
    const mono = MONO_FONTS.find(m => m.id === monoId.value) ?? MONO_FONTS[0]
    el.style.setProperty('--font-mono-stack', mono.stack)
    const data = DATA_FONTS.find(d => d.id === dataFontId.value) ?? DATA_FONTS[0]
    // OFF => data cells fall back to the single mono (Q5 "one mono")
    el.style.setProperty('--font-data-stack', dataFontEnabled.value ? data.stack : mono.stack)
    // force the lazy @font-face fetch so the picker visibly swaps (trap T8) — without
    // this the var() swap renders as the system fallback and the picker looks dead.
    ensureFontLoaded(mono.stack)
    if (dataFontEnabled.value) ensureFontLoaded(data.stack)
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

---

## 8. Phase 5 — `AppLogo.vue` (inline SVG) + `SidebarLogo.vue`

### 5a. The brand SVG files are NOT usable via `<img>` — inline instead

The brand source SVGs (`/Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-*.svg`)
render their wordmark as `<text>` styled by an **external** Google-Fonts `@import`. When
an SVG is loaded through `<img src>` it runs in **secure static mode** — external
resources are blocked and the file fails to decode entirely (`naturalWidth === 0`),
which the browser paints as a **broken-image glyph + the `alt` text**. That broken
glyph beside the alt text is exactly what reads as "the logo appears twice." (Trap T6.)

So do NOT use `<img src>` for these. Render the mark **inline** instead, where it uses
the page's real Fraunces (already loaded by @nuxt/fonts) and adapts to the theme via
`currentColor`. Copying the `public/logos/*.svg` files is optional (harmless if present;
not referenced by the component below).

### 5b. `app/components/AppLogo.vue` — inline SVG (verified)

One element per variant, theme-adaptive via `currentColor` on the wordmark; the
pilot-light dot keeps the literal brand red `#E4002B` (never re-tinted — brand book).
No `<img>`, no external font import, no light/dark file swap.

```vue
<script setup lang="ts">
// Inline SVG (NOT <img src>): the brand SVG files render their wordmark via an external
// Google-Fonts @import, which is blocked when an SVG loads through <img> (secure static
// mode) — there it fails to decode entirely (naturalWidth 0 → broken-image glyph + alt
// text, which read as "two logos"). Inlining lets the wordmark use the page's real
// Fraunces (already loaded by @nuxt/fonts) and adapt to the theme via currentColor.
// The pilot-light dot keeps the literal brand red #E4002B (never re-tinted — brand book).
withDefaults(defineProps<{ variant?: 'navbar' | 'icon' }>(), { variant: 'navbar' })
</script>

<template>
  <!-- navbar: pilot-light dot + "Pháros" wordmark -->
  <svg v-if="variant === 'navbar'" class="h-7 w-auto text-sidebar-foreground"
       viewBox="0 0 220 60" role="img" aria-label="Pháros" fill="none">
    <circle cx="22" cy="14" r="3.5" fill="#E4002B" />
    <text x="10" y="44" font-family="Fraunces, 'Times New Roman', serif"
          font-size="36" letter-spacing="-0.4" fill="currentColor">Pháros</text>
  </svg>

  <!-- icon (collapsed rail): pilot-light dot + "P" -->
  <svg v-else class="h-7 w-7 text-sidebar-foreground"
       viewBox="0 0 64 64" role="img" aria-label="Pháros" fill="none">
    <circle cx="29" cy="14" r="4.5" fill="#E4002B" />
    <text x="14" y="56" font-family="Fraunces, 'Times New Roman', serif"
          font-size="56" letter-spacing="-0.5" fill="currentColor">P</text>
  </svg>
</template>
```

### 5c. `app/components/SidebarLogo.vue`

`useSidebar()` must be called from inside a component rendered inside `<SidebarProvider>`
(not from the layout script setup that owns the `<SidebarProvider>`). This component
bridges that boundary.

```vue
<script setup lang="ts">
import { useSidebar } from '~/components/ui/sidebar'
const { state } = useSidebar()
</script>

<template>
  <AppLogo :variant="state === 'expanded' ? 'navbar' : 'icon'" />
</template>
```

**Logo rule:** the logo appears EXACTLY ONCE — in the sidebar header via `<SidebarLogo />`.
It is NOT repeated in the topbar. When the sidebar expands, the full navbar wordmark
shows; when collapsed to the icon rail, the icon variant shows. Both remain at a fixed
x position (the sidebar header, which doesn't shift horizontally with the content area).

---

## 9. Phase 6 — Layout: `app/layouts/default.vue`

Finance-lch topbar pattern on the `.dark`/shadcn substrate. The sidebar header holds
the logo via `<SidebarLogo>`. The content area is a 3-track CSS grid:
`preview | 6px-resizer | Marca-panel`, mimicking finance-lch's
`FacturaDrawerPanel`/`CausacionPanel` pattern for the resizable right panel.

Note: `SidebarInset` is already a `<main>`; do NOT nest a `<main>` inside it.
`<NuxtPage>` goes inside a `<div>` with `overflow-y-auto`.

```vue
<script setup lang="ts">
import { Sun, Moon, LayoutGrid, BarChart3, ChevronDown } from 'lucide-vue-next'
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
        <SidebarLogo />
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

Create `app/app.vue`:
```vue
<template><NuxtLayout><NuxtPage /></NuxtLayout></template>
```

**Verify P6:** topbar shows `[trigger] | [Diseño ▾ / Componentes] ... [org] [theme btn]`.
Pháros logo appears once, in the sidebar header. Dragging the 6px divider resizes the panel;
width persists across reload; double-click resets to 26%. Theme toggle in topbar works.
No `<h1>` anywhere.

---

## 10. Phase 7 — Marca panel: `app/components/PlaygroundPanel.vue`

Plain `<aside>` (NOT a Sheet/overlay) — the layout mounts it inline as the third
grid track. Theme control is in the topbar; the panel has sub-brand, accent, fonts.

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

---

## 11. Phase 8 — Component gallery: `app/pages/index.vue`

Use `font-data` (not `font-mono`) on all cifras so the data-font axis is visible.
Status pills use status tokens; they must NOT recolor on accent change.

Key lines to get right:

```vue
<!-- Table numeric cell — font-data + tabular features: -->
<TableCell class="text-right font-data tabular-nums slashed-zero lining-nums" :class="row.monto < 0 ? 'text-status-error' : ''">

<!-- Typography card — two samples: -->
<p class="font-mono text-sm">Mono · IBM Plex Mono · etiquetas · ABCDEF · {} [] =></p>
<p class="font-data tabular-nums slashed-zero lining-nums text-sm">Datos · 0123456789 · $1.234.567 · 0 con barra (cero/letra O)</p>
```

Full `app/pages/index.vue` structure (cards in order): Botones · Insignias y estados ·
Formulario · Tabla financiera · Pestañas · Diálogo · Tipografía. All headings Spanish.

---

## 12. Phase 9 — Charts: `app/pages/graficas.vue` + `app/components/PgCharts.client.vue`

`PgCharts.client.vue` uses `@unovis/vue` VisXYContainer/VisLine/VisDonut. Colors come
from `var(--chart-N)`. The `.client` suffix keeps it off SSR; `build.transpile` is set.

```vue
<!-- graficas.vue -->
<template>
  <ClientOnly>
    <PgCharts />
    <template #fallback><div class="h-72 animate-pulse rounded-md bg-muted" /></template>
  </ClientOnly>
</template>
```

(Keep `PgCharts.client.vue` identical to the v1 implementation — @unovis + chart data unchanged.)

---

## 13. Known issues, traps, and fixes (discovered during build)

### T1 — `reka-ui` TypeScript resolution
`tsc` error: `Failed to resolve import source "reka-ui"`. Fix: `pnpm add -D typescript`
(ensures TS ≥5.5) + add `typescript.tsConfig.compilerOptions.paths['reka-ui']` in
`nuxt.config.ts` (Phase 2 already includes this).

### T2 — `striptags` CJS/ESM conflict
`@unovis/ts` imports `striptags` (CJS); Vite 7 doesn't auto-wrap it unless it's a
direct dep. Fix: `pnpm add striptags` + `vite.optimizeDeps.include: ['striptags']`
(Phase 2 already includes both).

### T3 — `shadcn-vue add` injects Google Fonts CDN
The CLI may inject `@import url('https://fonts.googleapis.com/...')` and a duplicate
`@layer base {}` block into `main.css`. After running `shadcn-vue add`, verify
`main.css` still matches Phase 1 exactly; restore if not.

> **Font picker — three layered traps (T4 → T5 → T8).** The picker only renders
> correctly with ALL THREE fixes. T4 makes the CSS var override take effect; T5 makes
> the `@font-face` rules exist; T8 makes the browser actually FETCH the face on switch.
> Missing any one → the picker silently falls back to the system mono and "does nothing."

### T4 — `@theme inline` bakes font literals (necessary, not sufficient)
`@theme inline { --font-mono: "IBM Plex Mono", ... }` bakes the literal into the
`.font-mono` utility at build time. Runtime `setProperty('--font-mono', ...)` on `<html>`
has NO effect because the utility uses the baked literal, not the var. Fix: route
through `var(--font-mono-stack)` so the utility reads the overridable var (Phase 1).
Verified: after the fix, setting `--font-mono-stack` changes
`getComputedStyle(el).fontFamily` for `.font-mono` elements. **But the glyphs still
won't change until T8 — the computed family updates while the face is unfetched.**

### T5 — `@nuxt/fonts` misses picker fonts without `global:true` + preload class
`@nuxt/fonts` only generates `@font-face` for fonts it detects in CSS. With the
`var()` indirection (T4 fix), no font names appear in the Tailwind utility CSS —
only in the JS store. Fix: (a) add `global: true` to every picker family in
`nuxt.config.ts`, AND (b) add a `.fonts-preload` CSS class listing all picker font
names in a `font-family` property (Phase 1 CSS). Both are required; either alone
is insufficient. After this change, a **cold restart** (`rm -rf .nuxt && pnpm dev`)
is required to regenerate the font cache. Verified: all 10 picker `@font-face`
families are present in the document.

### T8 — @nuxt/fonts faces don't auto-fetch on a dynamic font-family change (the real "picker does nothing")
This is the bug the user actually saw. Even with T4 + T5 done, selecting a font in the
picker changed the computed `font-family` but **did not change the rendered glyphs** —
every option kept rendering as the system mono. Runtime evidence:
`document.fonts.check('1rem "Martian Mono"')` was **false** right after the picker set
the var, and the rendered text width was unchanged; yet an explicit
`document.fonts.load('1rem "Martian Mono"')` returned the face and made the same text
render **72.8px wider** (Martian's wider advance). So the faces are valid and DO render
distinctly — the browser's lazy `@font-face` loader simply doesn't re-fire when a
`var()`-indirected `font-family` changes on already-laid-out text.
**Fix:** the store's `apply()` calls `ensureFontLoaded(stack)` — extract the primary
family from the stack and `document.fonts.load()` it (400 + 500) to force the fetch
(Phase 4). Fire-and-forget; the page repaints when the face arrives. Verified: after
the fix, picking Martian Mono changes the rendered width 436.81 → 509.61px and
`document.fonts.check` → true.

### T6 — Brand SVGs can't be used via `<img>` (the real "logo appears twice")
The brand SVG files render their wordmark as `<text>` styled by an **external**
Google-Fonts `@import` inside `<style>`. Loaded through `<img src>`, an SVG runs in
**secure static mode** (external resources blocked) and **fails to decode entirely** —
runtime evidence: `img.complete === true` but `img.naturalWidth === 0`. The browser
paints that as a **broken-image glyph + the `alt="Pháros"` text**, which reads as "the
logo appears twice." (HTTP 200 + valid markup + correct MIME — so curl/network checks
look fine; only `naturalWidth` and a screenshot reveal it.) **Fix:** render the mark as
**inline SVG** in `AppLogo.vue` (Phase 5) — uses the page's real Fraunces and adapts via
`currentColor`; no `<img>`, no external import, no light/dark file swap. Verified: 0
leftover `<img alt="Pháros">`, exactly 1 visible `<svg aria-label="Pháros">` with
rendered `<text>`. The single-instance + fixed-on-collapse rule (one `<SidebarLogo>` in
the sidebar header, never in the topbar) still holds — verified the logo stays at x=12
and swaps navbar↔icon on collapse.

### T7 — `useSidebar()` cannot be called in the layout's script setup
`useSidebar()` uses Vue `inject()` and must be called from within a component that's
a descendant of `<SidebarProvider>`. The layout script setup runs for the component
that owns `<SidebarProvider>` in its template — calling `useSidebar()` there would fail.
Fix: `SidebarLogo.vue` is a separate component, rendered inside `<Sidebar>` (which is
inside `<SidebarProvider>`), so its script setup can safely call `useSidebar()`.

---

## 14. Q9 snapshot determinism (required guard for Playwright)

Before each snapshot, seed/clear localStorage to canonical state:

```js
await page.addInitScript(() => {
  localStorage.removeItem('pharos-pg-panel-pct')    // -> DEFAULT_PCT (26)
  localStorage.removeItem('pharos-pg-prefs')        // -> ERP / IBM Plex Mono / data-font OFF
  localStorage.setItem('pharos-pg-theme', 'light')  // set explicitly per snapshot variant
})
```

The panel's default width (26%) is the canonical snapshot width. Mono/data-font/accent
are likewise set explicitly per snapshot variant, never inherited from a prior session.

---

## 15. Run & acceptance checklist (§11)

```bash
cd /Users/gczuluaga/dev/pharos-playground
rm -rf .nuxt                # cold start so @nuxt/fonts regenerates with all families
pnpm dev                    # http://localhost:3000
```

Drive the page and confirm ALL of:

- [ ] **Logo** renders as a real **inline-SVG Fraunces wordmark** (NOT a broken image —
      `img.naturalWidth` must be >0, or better, there are 0 `<img alt="Pháros">` and exactly
      1 visible `<svg aria-label="Pháros">`). Appears exactly once — in the sidebar header,
      never the topbar. Wordmark recolors with the theme (via `currentColor`); pilot-light dot
      stays `#E4002B`. Shows full "Pháros" expanded, switches to "P" icon when collapsed,
      and stays at a fixed left position (x≈12) — does not shift with sidebar state. (T6)
- [ ] **Topbar (finance-lch pattern):** `[SidebarTrigger] | [Diseño ▾ / Componentes]` breadcrumb
      where "Diseño" chip opens a popover listing both pages; right side shows org name +
      round theme toggle. **No `<h1>` anywhere.**
- [ ] **Sidebar** stays the shadcn `Sidebar collapsible="icon"`; trigger collapses to icon rail.
- [ ] **Marca panel fixed in-view on the right** (no overlay). Dragging the 6px divider
      resizes it; width persists across reload; double-click resets to 26%.
- [ ] **Theme toggle** (topbar) flips light ↔ dark (`.dark` on `<html>`), no FOUC. No cobol.
- [ ] **Sub-brand switch** recolors buttons, sidebar active, focus ring, chart-1 (`--primary`
      propagates); **status pills do NOT move** (Q4 proof).
- [ ] **Custom accent** live-retints; "Limpiar" restores preset.
- [ ] **Mono picker (8 families)** visibly changes the typography sample AND the table cifras.
      The font must actually RENDER differently — measure rendered text width, not just the
      computed CSS var (T8: a changed `font-family` whose face is unfetched looks identical).
      Use Martian Mono for an obvious test: rendered width jumps ~+70px and
      `document.fonts.check('1rem "Martian Mono"')` becomes true. Requires `ensureFontLoaded`
      in `apply()` (T8) on top of T4 + T5.
- [ ] **Data-font toggle:** OFF → cifras use the selected mono (one mono, Q5); ON → cifras
      switch to the chosen data font (default JetBrains Mono) with `tabular-nums`/`slashed-zero`.
      The data Select is disabled while OFF.
- [ ] **Charts** (`/graficas`) render; breadcrumb leaf reads "Gráficas"; recolor on accent change.
- [ ] No console errors; **`pnpm build` succeeds** (charts stay `.client`/`ClientOnly`).

Screenshots: (1) light+ERP, (2) dark+ERP, (3) light+placeholder accent,
(4) data-font toggle ON/OFF, (5) panel resized.

---

## 16. Out of scope / notes

- The brand-book "data font" (JetBrains Mono for cifras) and Q5's "one mono" genuinely
  conflict. This playground does NOT resolve it — it makes both visible so SKuger can
  decide. Default stays Q5 (one mono, toggle off).
- finance-lch's real shell uses `[data-theme]` + cobol + `--nav-*`. We deliberately
  adopt only its **look/structure** on the locked `.dark`/shadcn substrate.
- Still local-only. Future home: `pharos-ui` shadcn-vue registry (RFC 0008 Q3).
  The resizable-panel + font-token work seeds it.
- The `sheet` component stays vendored (harmless) even though `PlaygroundPanel`
  no longer uses it — leave it for future use.
