# Laboratorio Clínico Hematológico — Brand & Design Specification
> **For AI coding assistants (Copilot, Cursor, Claude Code)**  
> Load this file as context before generating any UI code, components, copy, or styles.  
> This spec is the authoritative source for the **LCH brand identity, palette, and voice**.

> **⚠️ Read first — LCH is now a TENANT of the Pháros product family.**
> The **product/app design system** is the Pháros registry at
> `brands/pharos_brand/registry/` (token contract: `registry/tokens.css`). Build product
> UI from those tokens, not from the UI-implementation snippets below. This brand book
> remains the **LCH identity + palette source of truth** that Pháros draws from — Pháros
> `BRAND.md` §3.2 cites it. The narrative, archetypes, voice, color values, and logo
> intent here are canonical; the Tailwind/font/component **mechanics** in this file are
> kept for reference and are annotated where superseded by the registry.

---

## 1. Brand Identity

### 1.1 Who They Are
**Laboratorio Clínico Hematológico SAS** is a specialized diagnostic medicine organization based in Colombia (`lch.co`). Their core belief: technology is only valuable when it serves life. The human being is the sole protagonist of everything they do.

### 1.2 Brand Archetypes
| Archetype | Expression |
|-----------|-----------|
| **Caregiver** | Technology, development, and knowledge at the service of life. Empathy is a raw material. |
| **Creator** | Innovation, science, and technology applied to real needs and continuous improvement in medicine. |
| **Sage** | Veracity, experience, and deep knowledge in processes, protocols, and the medical team. |

### 1.3 Values
- **Vidas, no clientes** — Every person who needs results is a life, not a transaction.
- **Empatía** — Warm, human, transparent, and close communication at every touchpoint.

### 1.4 Tone of Voice
- Bilingual: Spanish primary, English secondary — both in a **technical but familiar** register.
- Simple, everyday words. No jargon for its own sake.
- Emotional messages that reflect the team's empathy toward patients.
- Speaks naturally about life situations. Avoids cold clinical detachment.
- **Never all-caps for headlines** — associated with shouting; use weight contrast instead.
- Brand name in running text: always title case (`Laboratorio Clínico Hematológico`), with heavier weight than surrounding text.

### 1.5 Tagline & Copy
| Usage | Text |
|-------|------|
| **Tagline** | Medicina Diagnóstica Especializada |
| **Mantra** | Nuestra pasión radica en leer en el tejido la vida y la información, y usar la tecnología para ver lo invisible y proyectarlo a favor de la medicina. |
| **Copy lines** | "La humanidad la llevamos en la sangre" · "Nuestra pasión nos permite ver lo invisible" · "En el tejido se puede leer más información de lo que una historia puede contar." |

---

## 2. Color System

> All hex values are for digital/screen use. Pantone references included for brand alignment checks.

### 2.1 Primary Palette — Corporate Communication

| Token Name | Hex | RGB | Pantone | Usage |
|---|---|---|---|---|
| `--color-brand-red` | `#E4002B` | 228, 0, 43 | 185 C | Primary brand, CTAs, main buttons, highlights |
| `--color-brand-red-dark` | `#A6192E` | 166, 26, 46 | 187 C | Hover states, button pressed, shadows |
| `--color-brand-orange` | `#FF8200` | 255, 130, 0 | 151 C | Warning states, accent badges |
| `--color-brand-lilac` | `#D986BA` | 217, 134, 186 | 673 C | Soft accents, tags, secondary highlights |
| `--color-brand-pink-soft` | `#FC9BB3` | 252, 155, 179 | 183 C | Hover backgrounds, light tints |

> **Logo-specific colors** (use only for logo rendering):
> - Logo red: `#E40046` (PANTONE 192 CP)
> - Logo burgundy: `#782F40` (PANTONE 195 C)

### 2.2 Secondary Palette — System Complement

| Token Name | Hex | RGB | Pantone | Usage |
|---|---|---|---|---|
| `--color-navy` | `#003A70` | 0, 58, 112 | 654 C | Dark backgrounds, data-dense surfaces, navy text |
| `--color-blue` | `#326295` | 50, 98, 149 | 653 C | Secondary interactive, links, medium accents |
| `--color-teal` | `#A0D1CA` | 160, 209, 202 | 7464 C | Success states, soft highlights, decorative |
| `--color-blush` | `#F4CDD4` | 244, 205, 212 | 7422 C | Soft backgrounds, card surfaces, empty states |
| `--color-yellow` | `#FBD872` | 251, 216, 114 | 1215 C | Financial data accents, warnings, badges |

### 2.3 Neutral / Base Colors

| Token Name | Hex | RGB | Pantone | Usage |
|---|---|---|---|---|
| `--color-black` | `#000000` | 0, 0, 0 | — | Body text, max contrast |
| `--color-gray-dark` | `#888B8D` | 136, 139, 141 | Gray 8C | Muted text, labels, disabled states |
| `--color-gray-mid` | `#C8C9C7` | 200, 201, 199 | Gray 8C (30%) | Borders, dividers, subtle separators |
| `--color-white` | `#FFFFFF` | 255, 255, 255 | — | Backgrounds, cards, text on dark |

### 2.4 Semantic Aliases

| Alias | Value | Purpose |
|---|---|---|
| `--color-text-primary` | `#000000` | Default body text |
| `--color-text-secondary` | `#888B8D` | Labels, captions, metadata |
| `--color-text-muted` | `#C8C9C7` | Placeholders, disabled text |
| `--color-text-on-dark` | `#FFFFFF` | Text on dark/red backgrounds |
| `--color-bg-page` | `#FFFFFF` | Page background |
| `--color-bg-surface` | `#F4CDD4` | Card / panel background (soft) |
| `--color-bg-dark` | `#003A70` | Dark sidebar, dark header |
| `--color-interactive` | `#E4002B` | Buttons, links, primary actions |
| `--color-interactive-hover` | `#A6192E` | Hover/focus state for interactive |
| `--color-success` | `#A0D1CA` | Positive outcomes, completed states |
| `--color-warning` | `#FBD872` | Warnings, financial alerts |
| `--color-error` | `#E4002B` | Errors, critical states |
| `--color-border` | `#C8C9C7` | Default borders |
| `--color-border-focus` | `#E4002B` | Focus ring on inputs |

### 2.5 Color Contrast Reference (from brand manual)

| Foreground | Background | Contrast |
|---|---|---|
| White | Brand Red `#E4002B` | **High** ✅ |
| White | Navy `#003A70` | **High** ✅ |
| Black | White | **High** ✅ |
| Brand Red | White | **High** ✅ |
| Navy | Teal `#A0D1CA` | **Medium** ⚠️ |
| White | Teal | **Low** ❌ — avoid small text |
| White | Yellow `#FBD872` | **Low** ❌ — avoid |
| Black | Yellow `#FBD872` | **High** ✅ |

### 2.6 Tailwind Config Extension

> **⚠️ Legacy / illustrative (Tailwind v3).** This `tailwind.config.js (module.exports)`
> block is kept to document the palette mapping only. The live product system is
> **Tailwind v4, CSS-first**, with tokens defined in the Pháros registry
> (`brands/pharos_brand/registry/tokens.css`) — there is no JS config to extend. Use the
> registry tokens; do not reintroduce a v3 config. The hex values below remain the
> canonical LCH palette source.

```js
// tailwind.config.js  — LEGACY (Tailwind v3); superseded by registry tokens.css (v4 CSS-first)
module.exports = {
  theme: {
    extend: {
      colors: {
        lch: {
          red:       '#E4002B',
          'red-dark':'#A6192E',
          orange:    '#FF8200',
          lilac:     '#D986BA',
          pink:      '#FC9BB3',
          navy:      '#003A70',
          blue:      '#326295',
          teal:      '#A0D1CA',
          blush:     '#F4CDD4',
          yellow:    '#FBD872',
          black:     '#000000',
          'gray-dark':'#888B8D',
          'gray-mid': '#C8C9C7',
          white:     '#FFFFFF',
          // logo only
          'logo-red':      '#E40046',
          'logo-burgundy': '#782F40',
        }
      }
    }
  }
}
```

### 2.7 CSS Custom Properties

```css
/* globals.css or assets/styles/tokens.css */
:root {
  /* Brand */
  --color-brand-red:       #E4002B;
  --color-brand-red-dark:  #A6192E;
  --color-brand-orange:    #FF8200;
  --color-brand-lilac:     #D986BA;
  --color-brand-pink-soft: #FC9BB3;

  /* Secondary */
  --color-navy:   #003A70;
  --color-blue:   #326295;
  --color-teal:   #A0D1CA;
  --color-blush:  #F4CDD4;
  --color-yellow: #FBD872;

  /* Neutrals */
  --color-black:    #000000;
  --color-gray-dark:#888B8D;
  --color-gray-mid: #C8C9C7;
  --color-white:    #FFFFFF;

  /* Semantic */
  --color-text-primary:        #000000;
  --color-text-secondary:      #888B8D;
  --color-text-muted:          #C8C9C7;
  --color-text-on-dark:        #FFFFFF;
  --color-bg-page:             #FFFFFF;
  --color-bg-surface:          #F4CDD4;
  --color-bg-dark:             #003A70;
  --color-interactive:         #E4002B;
  --color-interactive-hover:   #A6192E;
  --color-success:             #A0D1CA;
  --color-warning:             #FBD872;
  --color-error:               #E4002B;
  --color-border:              #C8C9C7;
  --color-border-focus:        #E4002B;
}
```

---

## 3. Typography

### 3.1 Primary Brand Font — Apax
The official typeface is **Apax** (Optimo foundry, Geneva). It is a custom-modified font for the brand — rounded terminals inspired by organic forms of the human body. Friendly, balanced, elegant.

> ⚠️ Apax is a **commercial font** and must be licensed separately. Do not use freely available fonts as substitutes in production without brand approval. For development and prototyping, use the system-ui fallback stack below.

**Available weights:** Thin · Regular · Medium · Bold (+ Italic variants for each)

```css
font-family: 'Apax', 'Inter', 'DM Sans', system-ui, -apple-system, sans-serif;
```

**Fallback for dev (Apax not available):** `Inter` or `DM Sans` from Google Fonts — both share the same humanist, rounded character.

### 3.2 Typography Rules
- **Paragraphs**: always left-aligned.
- **Line height**: 1.6× font size. E.g., `font-size: 10pt → line-height: 16pt`.
- **Brand name in body text**: always `Laboratorio Clínico Hematológico` in title case, with one weight heavier than surrounding text.
- **Headlines**: use weight contrast (`thin` vs `medium/bold`) instead of ALL CAPS.
- **Italic**: only use Apax's built-in italic variants. Never artificially oblique.
- **No distortion** of type: no stretching, no skewing.

### 3.3 Type Scale (Tailwind)

> **⚠️ Legacy / illustrative (Tailwind v3).** This `fontSize` config is reference only.
> The live product system is **Tailwind v4 CSS-first** and takes its type scale from the
> Pháros registry (`brands/pharos_brand/registry/tokens.css` + `frontend-standards.md`).
> Do not reintroduce a v3 `fontSize` block.

```js
// tailwind.config.js — extend fontSize  — LEGACY (Tailwind v3); superseded by registry (v4 CSS-first)
fontSize: {
  'xs':   ['0.75rem',  { lineHeight: '1.2rem' }],
  'sm':   ['0.875rem', { lineHeight: '1.4rem' }],
  'base': ['1rem',     { lineHeight: '1.6rem' }],
  'lg':   ['1.125rem', { lineHeight: '1.8rem' }],
  'xl':   ['1.25rem',  { lineHeight: '2rem'   }],
  '2xl':  ['1.5rem',   { lineHeight: '2.4rem' }],
  '3xl':  ['1.875rem', { lineHeight: '3rem'   }],
  '4xl':  ['2.25rem',  { lineHeight: '3.6rem' }],
  '5xl':  ['3rem',     { lineHeight: '4.8rem' }],
}
```

### 3.4 Monospaced / Data Font

> **⚠️ Product UI font standard differs.** Across the **Pháros product family** the data +
> label font is **IBM Plex Mono** (the family triad is **Fraunces** display/wordmark +
> **Inter** sans UI + **IBM Plex Mono** data/labels). **JetBrains Mono** (and **Apax**)
> remain **LCH brand-identity references only** — they are *not* product-UI fonts. The
> survey of mono options below is kept for brand context; for product code, use IBM Plex
> Mono per the registry.

Used for: numerical data, results, lab values, financial figures, code, timestamps, tabular data.

#### ✅ Recommended — On-brand & harmonious with Apax

| Font | Personality | Why it works | Google Fonts |
|---|---|---|---|
| **JetBrains Mono** | Rounded, humanist, warm | Rounded terminals match Apax's organic forms. Perfectly tabular numerals. Best overall fit. | `JetBrains+Mono` |
| **IBM Plex Mono** | Warm, technical, trustworthy | Clinical-scientific feel. Aligns with the lab context. Excellent legibility at small sizes. | `IBM+Plex+Mono` |
| **DM Mono** | Friendly, distinctive, geometric | Pairs naturally with DM Sans (Apax fallback). Approachable and slightly playful. | `DM+Mono` |

#### ⚙️ Functional — Neutral & reliable

| Font | Personality | Why it works | Google Fonts |
|---|---|---|---|
| **Roboto Mono** | Neutral, clinical, professional | Very readable in dense data tables. Medical/ERP systems vibe. | `Roboto+Mono` |
| **Fira Mono** | Clean, open, developer-grade | Excellent at small sizes. More "technical" feel, less warm. | `Fira+Mono` |
| **Inconsolata** | Elegant, narrow, efficient | Great for compact tables. More classical feel, less playful. | `Inconsolata` |

#### 🎨 Expressive — Different but harmonizable

| Font | Personality | Why to consider | Google Fonts |
|---|---|---|---|
| **Space Mono** | Geometric, bold, retro-tech | High contrast vs Apax — creates clear hierarchy between prose and data. | `Space+Mono` |
| **Courier Prime** | Classic, editorial, trustworthy | Evokes lab reports and clinical documents. Strong heritage feel. | `Courier+Prime` |
| **Source Code Pro** | Legible, system-like, versatile | Adobe's workhorse. Very safe for mixed content apps. | `Source+Code+Pro` |

#### 🏆 Recommendation for your Finanzas app
> **⚠️ Superseded for product UI.** The Pháros product standard is **IBM Plex Mono** as
> the single data + label font. The JetBrains-Mono-primary pairing below is a historical
> LCH recommendation, kept for reference only.

**Primary:** `JetBrains Mono` for all numeric/data output *(LCH brand reference; product UI uses IBM Plex Mono)*  
**Secondary:** `IBM Plex Mono` for labels, table headers, code  
Both available free on Google Fonts and NPM.

```css
/* Nuxt: add to nuxt.config.ts webfonts or load via CSS */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --font-brand: 'Apax', 'Inter', 'DM Sans', system-ui, sans-serif;
  --font-data:  'JetBrains Mono', 'IBM Plex Mono', 'Courier New', monospace;
  --font-label: 'IBM Plex Mono', 'JetBrains Mono', monospace;
}
```

```js
// Nuxt 4 — nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap'
        }
      ]
    }
  }
})
```

---

## 4. Logo Usage

### 4.1 Logo Structure
The logo has three elements:
1. **Symbol / Isotipo** — DNA double helix abstraction forming the letter "H". Two colors: red `#E40046` (right side / dominant) + burgundy `#782F40` (left side / shadow).
2. **Typografía nombre** — "Laboratorio Clínico" (small, regular weight) + "Hematológico" (large, medium weight). Custom-modified Apax.
3. **Descriptor** — "Medicina Diagnóstica Especializada" in regular weight, centered below isotipo.

### 4.2 Logo Versions

> **Reconciled to the actual committed assets** in `brands/hematologico/logos/`,
> renamed to a consistent kebab-case scheme and **verified against the rendered
> artwork** — the legacy `LOGO.png` / `Logo horizontal.png` filenames had the
> orientation backwards (`LOGO.png` was the horizontal lockup; `Logo horizontal.png`
> was the vertical/stacked one). Files marked **canonical** are the approved versions.
> Each canonical mark now also ships a `.svg` — see the SVG note below.

| File | Version | Canonical? | Use Case |
|---|---|---|---|
| `logo-horizontal-color.{svg,png}` | Horizontal lockup (icon + name + descriptor in a row) | ✅ canonical | Wide headers, navbars, side-by-side contexts. |
| `logo-vertical-color.{svg,png}` | Vertical / stacked lockup (icon over name over descriptor) | ✅ canonical | Square-ish contexts; primary on white. |
| `logo-white.{svg,png}` | All white (horizontal lockup) | ✅ canonical | Dark / red / navy backgrounds. |
| `logo-icon-color.{svg,png}` | Symbol / isotipo only (DNA-helix "H") | ✅ canonical | Favicon, avatar, small icon slots (≥32px). |
| `logo-white-alt.png` | All white (alt artboard export) | — | Variant; prefer `logo-white`. |
| `logo-alt-nuevo.png` | Full color (updated mark) | — | Legacy/transitional export; verify before use. |
| `logo-alt-1.png` | Full color (early export) | — | Legacy export; do not use for new UI. |
| `logo-koc.png` | Single-color / print variant | — | Legacy print variant; verify with brand mgmt. |

> **SVG status (stopgap).** The four canonical `.svg` files exist but currently
> **embed the raster PNG as a base64 data URI** — they render anywhere (`<img src>`,
> CSS background) but are **not true vectors**. **TODO:** replace with hand-authored
> vector exports of the canonical four + a true single-color red/black mono lockup.
> (The gitleaks allowlist exempts `brands/**/logos/*.svg` so the embedded blob doesn't
> trip the entropy rule — see `.gitleaks.toml`.)

### 4.3 Clear Space
Minimum clear space = **2× the height of the letter "H" in "Hematológico"** on all sides. In special cases minimum is 1× (requires brand management approval).

### 4.4 Minimum Sizes

| Format | Vertical | Horizontal |
|---|---|---|
| **Digital** | 103 × 85 px | 153 × 43 px |
| **Print** | 3.6 × 2.9 cm | 5.4 × 1.5 cm |

### 4.5 Responsive Reduction (web components)

```
Viewport ≥ 1024px  →  Full logo: symbol + "Laboratorio Clínico Hematológico" + descriptor
Viewport 640–1023px →  Reduced: symbol + "Laboratorio Clínico Hematológico" (no descriptor)
Viewport < 640px   →  Icon only: symbol
```

### 4.6 Avatar / Social Media
- Square or circular: symbol with 1/4 height padding.
- Only two approved versions: symbol in brand colors on white, OR white symbol on `#E4002B`.

### 4.7 ❌ Logo Don'ts
Never: rotate, tilt, stretch, distort, outline, add drop shadows, change individual colors, use different typography, place on low-contrast backgrounds, combine with other graphics inside the clear space, reproduce in ALL CAPS wordmark, break letter spacing.

### 4.8 Vue Component Usage

> **Filenames map to the kebab-case canonical assets** (see §4.2). The `.svg` files are
> raster-embedded stopgaps today (§4.2 SVG status) but resolve fine via `<img src>`;
> swap to true vectors when they land — no code change needed.

```vue
<!-- Use as <LchLogo> with theme prop -->
<template>
  <img
    :src="logoSrc"
    :alt="'Laboratorio Clínico Hematológico'"
    :height="height"
    class="object-contain"
  />
</template>

<script setup>
const props = defineProps({
  theme: { type: String, default: 'light' },   // 'light' | 'dark'
  size: { type: String, default: 'default' },   // 'default' | 'navbar' | 'icon'
})

// Maps to the canonical kebab-case assets in brands/hematologico/logos/.
const logoSrc = computed(() => {
  if (props.size === 'icon') return '/assets/logos/logo-icon-color.svg'       // symbol only
  if (props.theme === 'dark') return '/assets/logos/logo-white.svg'           // white, for dark/red/navy bg
  // light theme: horizontal lockup for navbar, vertical (stacked) otherwise
  return props.size === 'navbar'
    ? '/assets/logos/logo-horizontal-color.svg'
    : '/assets/logos/logo-vertical-color.svg'
})

const height = computed(() => ({
  icon: 32, navbar: 36, default: 48
})[props.size])
</script>
```

---

## 5. Iconography System

Icons are built with **rounded terminals** — matching the curved endings of the Apax typeface. This rounded stroke ending is the governing rule for all icons.

- Stroke-based, not filled (unless filled version is part of official set)
- Consistent stroke weight across all icons
- Available for: wayfinding, medical specialties, UX interface actions
- Colors: use brand palette only. Never arbitrary colors.

```vue
<!-- Tailwind icon sizing convention -->
<Icon name="..." class="w-5 h-5 text-lch-red" />         <!-- sm: 20px -->
<Icon name="..." class="w-6 h-6 text-lch-navy" />        <!-- md: 24px -->
<Icon name="..." class="w-8 h-8 text-lch-gray-dark" />   <!-- lg: 32px -->
```

---

## 6. Photography & Imagery Guidelines

### 6.1 Style
- **Everyday life**: natural, candid moments. Transmit calm, happiness, security.
- **People**: Latin ethnicity matching the Colombian context. Natural body language — no poses.
- **Lab environments**: team in action, professional but warm.
- **Children**: freshness, joy, future-oriented communication.
- **Details**: macro shots of lab objects or biological textures as metaphors.

### 6.2 Color Treatment
- **Mass market segments**: warm yellow or blue tonal direction, high saturation.
- **Premium segments**: desaturated, gray-toned.
- **Monochrome**: tint with `#E4002B` as base color OR black-and-white with red color accents on focal elements.

### 6.3 Illustration
- Flat-style, brand palette (reds, pinks, blush, purple).
- Used for innovation content, educational materials, UX empty states.
- Schematic/metaphorical — helps simplify complex medical concepts.

---

## 7. Component Patterns (Nuxt 4 / Vue / Tailwind)

### 7.1 Primary Button
```vue
<button class="bg-lch-red hover:bg-lch-red-dark text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200">
  Solicitar examen
</button>
```

### 7.2 Secondary Button
```vue
<button class="border border-lch-red text-lch-red hover:bg-lch-blush font-medium px-6 py-3 rounded-lg transition-colors duration-200">
  Ver resultados
</button>
```

### 7.3 Data / Metric Display
```vue
<div class="font-['JetBrains_Mono'] text-2xl font-medium text-lch-navy tabular-nums">
  {{ value }}
</div>
<div class="font-sans text-sm text-lch-gray-dark tracking-wide uppercase">
  {{ label }}
</div>
```

### 7.4 Status Badge
```vue
<!-- Success -->
<span class="bg-lch-teal/30 text-lch-navy text-xs font-medium px-3 py-1 rounded-full">Normal</span>
<!-- Warning -->
<span class="bg-lch-yellow/40 text-lch-black text-xs font-medium px-3 py-1 rounded-full">Revisar</span>
<!-- Error -->
<span class="bg-lch-red/10 text-lch-red text-xs font-medium px-3 py-1 rounded-full">Crítico</span>
```

### 7.5 Card Surface
```vue
<div class="bg-white border border-lch-gray-mid rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
  <!-- content -->
</div>
```

### 7.6 Input Field
```vue
<input
  class="w-full border border-lch-gray-mid rounded-lg px-4 py-3 text-lch-black placeholder-lch-gray-dark
         focus:outline-none focus:ring-2 focus:ring-lch-red focus:border-lch-red transition"
  placeholder="Nombre del paciente"
/>
```

---

## 8. Layout Principles

- **Grid**: 12-column, 24px gutters on desktop, 16px on mobile.
- **Max content width**: 1280px.
- **Spacing scale**: base 4px (Tailwind default — `p-1 = 4px, p-2 = 8px...`).
- **Border radius**: `rounded-lg` (8px) for cards and inputs, `rounded-xl` (12px) for modals, `rounded-full` for badges/avatars.
- **Shadows**: subtle (`shadow-sm`) by default. `shadow-md` on hover. Never heavy drop shadows on logo or icons.
- **Text alignment**: always left-aligned for body text. Center only for hero headlines and empty states.

---

## 9. FastAPI (Python Backend) — Naming & Copy

When generating API responses, error messages, or user-facing strings in FastAPI:

- Use Spanish as default language for all user-facing messages.
- Tone: calm, reassuring, never alarming. Match brand voice.
- HTTP error messages example:
  ```python
  # ✅ Brand-aligned
  {"message": "No encontramos tu resultado. Verifica tu número de documento."}
  # ❌ Cold / generic
  {"detail": "Record not found"}
  ```
- Field names in API: `snake_case` in Python, converted to `camelCase` in Vue via Nuxt's `useFetch` composable.
- Date formats: `DD/MM/YYYY` for display, ISO 8601 for API interchange.

---

## 10. Quick Reference Card

```
BRAND NAME   Laboratorio Clínico Hematológico
TAGLINE      Medicina Diagnóstica Especializada
URL          lch.co

BRAND/UI RED #E4002B  (buttons, CTAs, highlights)
DARK RED     #A6192E  (hover, pressed)
NAVY         #003A70  (dark surfaces, data)
TEAL         #A0D1CA  (success, soft accents)
YELLOW       #FBD872  (financial, warnings)
BLUSH        #F4CDD4  (soft backgrounds)
GRAY DARK    #888B8D  (secondary text)

LOGO-ONLY RED #E40046 (logo rendering only — NOT a UI color)

BRAND FONT   Apax (Optimo) → LCH brand-identity asset only; product UI sans = Inter
DATA FONT    Product UI = IBM Plex Mono  (JetBrains Mono = LCH brand reference, not product UI)
LABEL FONT   IBM Plex Mono

LOGO COLORS  #E40046 (logo-only red) + #782F40 (burgundy)
LOGO MIN     103×85px vertical / 153×43px horizontal
CLEAR SPACE  2× height of "H" in "Hematológico"
```

---

*Brand concept and identity by Backbone Brand Wondering. Visual identity manual by Ah/Studio. Medellín, Colombia, 2019. This specification compiled for digital development use, 2026.*
