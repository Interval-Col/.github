# Biuman — Centro de Experiencia Deportiva — Brand & Design Specification
> **For AI coding assistants (Copilot, Cursor, Claude Code)**  
> Load this file as context before generating any UI code, components, copy, or styles for the **Biuman** tenant.  
> This spec is the authoritative source for the **Biuman brand identity, palette, and voice**.

> This document was compiled from the Biuman brand masters in `biuman_brand`
> (`Backbone-BIUMAN.pdf`, 23 pp concise strategy backbone; `Brandbook-BIUMAN.pdf`, 47 pp full brand
> book; the `FONTS/` directory; and the supplied logo files). It is the **tenant brand reference**
> for Biuman, the sibling of `hematologico/LCH-BRAND.md`. Values were extracted from the source PDFs;
> anything the masters did not state is marked **"no especificado en el material fuente."**

> **⚠️ Read first — Biuman is a TENANT of the Pháros product family.**
> Biuman is a clinic / sports-lab **tenant** of the Pháros product family — the **same structural
> role as Hematológico (LCH)**, *not* a Pháros sub-brand and *not* the maker (Interval). Per Pháros
> `BRAND.md` §10: *"LCH and Biuman are tenants, not parents — a tenant **never prefixes an app name**
> (it is `Pháros · Timón`, never \"LCH Pháros\"). Where a tenant must appear (e.g. a login footer),
> use a small `para [tenant]` / \"by [tenant]\" credit; the Pháros brand wins on its own screens."*
> Biuman maps onto the **Pháros LIS deportivo** surface (`Pháros LIS clínico (LCH) · deportivo (Biuman)`).
> The **product/app design system** is therefore the Pháros registry at `brands/pharos_brand/registry/`
> (token contract: `registry/tokens.css`) — **build product UI from those tokens, not from this file's
> palette/Tailwind snippets.** This brand book remains the **Biuman identity + palette source of truth**
> that Pháros draws from. The narrative, personality, voice, color values, and logo intent here are
> canonical; the mechanics (Tailwind/font/component snippets) are kept for reference only.

---

## 1. Brand Identity

### 1.1 Who They Are
**Biuman** is a **"Centro de Experiencia Deportiva"** (sports-experience center) operating under the
idea of **"La Ciencia del Movimiento"** (the Science of Movement). Its value proposition, stated
literally in the Backbone: *"Llevar al cuerpo humano a conquistar el movimiento a través del
conocimiento, la tecnología y la técnica."* (To take the human body to conquer movement through
knowledge, technology and technique.)

Biuman is **backed by the Hematológico's medical experience** — it is the **sports-lab sibling** of LCH
inside the holding. The Brandbook lockups use the descriptors **"Centro de Experiencia Deportiva"** and
**"Ciencia del Movimiento."** (The supplied horizontal-lockup PNG also carries a **"LABORATORIO
DEPORTIVO"** descriptor that does *not* match the Brandbook's documented descriptor set — see §4.2.)

> **Taxonomy note.** Neither the Backbone nor the Brandbook states Biuman's relationship to Pháros /
> Interval — that placement comes from the org brand taxonomy (Pháros `BRAND.md` §10), where Biuman is a
> clinic/sports-lab **tenant** of the Pháros family, the same role as LCH.

### 1.2 Brand Archetypes
The Backbone defines Biuman's personality (the **"SER"**) through three archetypes:

| Archetype | Spanish name | Expression |
|-----------|--------------|-----------|
| **Sage** | SABIO | Science, experience and knowledge at the service of the human body and its movement. |
| **Explorer** | EXPLORADOR | Seeking the body's limits — resistance, regeneration and development; the power of movement. |
| **Ruler** | GOBERNANTE | The elite group that needs deep, precise information and is always willing to go further. |

**Brand spirit (the "Alma"):** break inertia and move — *romper límites, miedos, paradigmas y lograrlo
todo* (break limits, fears, paradigms and achieve it all).

### 1.3 Values
- **Acompañamiento Médico** *(medical accompaniment)* — the stated **valor agregado** (non-traditional
  added value): all of the Hematológico's experience plus a high-level medical team at the service of
  understanding sport, the human body and the science of movement.
- **Precisión, tecnología y confiabilidad** *(precision, technology, reliability)* — backing both
  methods and results.
- **Conocimiento + tecnología + técnica** *(knowledge + technology + technique)* — the means by which
  the body conquers movement.
- **Romper la inercia y moverse** *(break inertia and move)* — the governing law of the brand concept,
  derived from the "Big Bang" metaphor; *un paso adelante, un metro más, un juego más, una cima más,
  una meta más.*

### 1.4 Tone of Voice
- **Bilingual.** Speaks **English and Spanish**, fluidly and in combination. **Spanish is prioritized**
  for precise, technical, relevant information about technologies/tools (more elaborate). **English** is
  used as brand / campaign / strategic-positioning support (more punchy and *contundente*).
- **Register:** casual, neutral and powerful — everyday words delivered as a statement / declaration.
  Mixes **technical + precise** language with **inspiring + challenging** language.
- **Direct, athlete-to-athlete.** Communication is *de atleta a atleta*, *certera y eficaz* (accurate
  and effective). Inspirational, épico and científico at once; short, accumulative, ascending phrases
  (*"un metro más, un juego más, una cima más"*).
- **Avoid:** colloquialisms, overly informal slang, or over-elaborate language.
- **Talks about:** the human body; technology serving health & wellbeing; the importance of habits and
  good practices; tips to improve athletes' quality of life; relevant product recommendations; trends &
  news; Biuman products/services; athletes' conquests & challenges; brand philosophy & beliefs.

### 1.5 Tagline & Copy
| Usage | Text |
|-------|------|
| **Tagline (ES)** | La ciencia del movimiento. |
| **Concept / claim (EN)** | Humans Conquering Movement. |
| **Descriptors** | "Centro de Experiencia Deportiva" · "Ciencia del Movimiento" · (logo artwork only; see §4.2 discrepancy) "Laboratorio Deportivo" |
| **Mantra** | El deporte es la conquista del hombre sobre el movimiento. Un baile entre la gravedad y la voluntad, la biología y la determinación, el instinto y la conciencia. |
| **Concept line** | El lugar donde la ciencia se rinde al deporte y la tecnología se pone al servicio del cuerpo humano. |
| **Conceptual triad** | MOVEMENT — HUMANS — GOD (with HUMANS at the center; Brandbook p.37) |
| **Campaign / section headers** | "MEET YOUR FAN." · "TALK TO ME." · "MOVEMENT HUMANS GOD" · "HUMANS CONQUERING MOVEMENT" · "CIENCIA DEL MOVIMIENTO" |
| **URL** | WWW.BIUMAN.COM |

**Target audience ("MEET YOUR FAN").** High-performance athletes (professional or amateur) who want to
know their current physical state and their progress; value information; seek tech & tools to expand
capacity/performance; continuously improve technique, resistance and metrics; invest consciously in
health & wellbeing; and aim to keep improving and achieve more athletic goals. Aspirational / ally
brands cited (sensorial): On Running, Nike, Savvy, Garmin, Strava.

---

## 2. Color System

> Biuman runs a **high-contrast monochrome system: black + white + neutral grey.** The Backbone states
> the *receta visual* color recipe literally as **"blanco, negro, gris."** The values below are the
> **formal palette ("TONOS")** printed in the Brandbook (pp. 22–23), which is the authoritative source —
> it carries real CMYK and Pantone specs. The Brandbook's own palette note (p.22) warns that on-screen
> tones vary by device calibration and against print, and recommends confirming with a Pantonera and the
> print provider before producing.

### 2.1 Primary Palette — Corporate Communication (Brandbook "TONOS", pp. 22–23)

| Token Name | Hex | CMYK | Pantone | Role |
|---|---|---|---|---|
| `--color-biuman-light` | `#F0EEED` | 10 / 7 / 5 / 0 | Cool Gray C | Light / off-white neutral surface (tile 1 of 3). |
| `--color-biuman-black` | `#1B1B1B` | 65 / 66 / 68 / 82 | Black C | Near-black — primary text & dark surfaces; the brand's signature dark ground (tile 2 of 3). |
| `--color-biuman-grey` | `#A4A9A6` | 35 / 23 / 19 / 2 | 429 C | Greenish mid-grey — neutral accent; the monochrome logo color on light/medium grounds (tile 3 of 3). |

> The palette is intentionally only these **three tones** plus pure white/black for type and contrast.
> There is **no brand-red / no chromatic accent** equivalent to LCH's red.

### 2.2 Secondary Palette — System Complement
**no especificado en el material fuente.** Biuman ships no secondary chromatic palette — the system is the
three neutral tones above. The orange / salmon ("naranja / salmón") that appears in the Backbone moodboard
(p.16) is a **photographic / texture accent only** (salmon-flesh macro texture), **not** a defined palette
swatch — treat it as imagery color, not a brand color.

### 2.3 Neutral / Base Colors

| Token Name | Hex | CMYK | Pantone | Role |
|---|---|---|---|---|
| `--color-black` | `#000000` | — | — | Pure black; used in the Backbone "blanco, negro, gris" recipe and on dramatic dark surfaces. |
| `--color-white` | `#FFFFFF` | — | — | Logo/wordmark color and typography on grey & black grounds; light ground. |
| `--color-near-black` | `#1B1B1B` | 65 / 66 / 68 / 82 | Black C | Formal "dark tone" of the Brandbook palette (see §2.1). |

> The Backbone's signature surface (cover and section pages) is a cool-warm grey sampled at ~`#A3A9A6` /
> `#A5ABA8`, which corroborates the formal `#A4A9A6` (Pantone 429 C) in §2.1; the Backbone itself printed
> no CMYK/Pantone spec for it.

### 2.4 Semantic Aliases

> ⚠️ Biuman's masters define **no semantic-state palette** (success/warning/error). The aliases below are
> a structural mapping of the available neutral tones for tenant-themed UI parity; **for product UI use the
> Pháros registry semantic tokens, not these.** State colors are **no especificado en el material fuente.**

| Alias | Value | Purpose |
|---|---|---|
| `--color-text-primary` | `#1B1B1B` | Default body text (near-black). |
| `--color-text-secondary` | `#A4A9A6` | Labels, captions, metadata (mid-grey). |
| `--color-text-on-dark` | `#FFFFFF` / `#F0EEED` | Text on dark/black backgrounds. |
| `--color-bg-page` | `#F0EEED` | Light page background (off-white). |
| `--color-bg-dark` | `#1B1B1B` | Dark sidebar / header / hero ground. |
| `--color-border` | `#A4A9A6` | Default borders / dividers. |
| `--color-success` | no especificado en el material fuente | — |
| `--color-warning` | no especificado en el material fuente | — |
| `--color-error` | no especificado en el material fuente | — |

### 2.5 Color Contrast Reference

> The Brandbook does **not** print a contrast matrix — **no especificado en el material fuente** beyond the
> high-contrast B/W intent. The ratios below are **computed** (WCAG 2.x relative-luminance) from the three
> formal tones for implementation guidance only.

| Foreground | Background | Contrast (estimado) | Rating |
|---|---|---|---|
| White `#FFFFFF` | Near-black `#1B1B1B` | **17.22 : 1** | AAA ✅ |
| Near-black `#1B1B1B` | Off-white `#F0EEED` | **14.89 : 1** | AAA ✅ |
| Near-black `#1B1B1B` | Mid-grey `#A4A9A6` | **7.22 : 1** | AA / AAA (≥18 px) ✅ — prefer for larger type |
| White `#FFFFFF` | Mid-grey `#A4A9A6` | **2.39 : 1** | Fails AA ❌ — avoid for text |

### 2.6 Tailwind Config Extension

> **⚠️ Legacy / illustrative.** Kept to document the palette mapping only. The live product system is the
> **Pháros registry** (Tailwind v4, CSS-first; `brands/pharos_brand/registry/tokens.css`). Use the registry
> tokens; the hex values below remain the canonical Biuman palette source.

```js
// tailwind.config.js — LEGACY / reference only; superseded by Pháros registry tokens.css (v4 CSS-first)
module.exports = {
  theme: {
    extend: {
      colors: {
        biuman: {
          light: '#F0EEED',  // Cool Gray C
          black: '#1B1B1B',  // Black C
          grey:  '#A4A9A6',  // Pantone 429 C
          white: '#FFFFFF',
          pure:  '#000000',
        }
      }
    }
  }
}
```

### 2.7 CSS Custom Properties

```css
/* globals.css or assets/styles/tokens.css — Biuman tenant identity palette */
:root {
  --color-biuman-light: #F0EEED; /* Cool Gray C  | CMYK 10 7 5 0   */
  --color-biuman-black: #1B1B1B; /* Black C      | CMYK 65 66 68 82 */
  --color-biuman-grey:  #A4A9A6; /* Pantone 429 C| CMYK 35 23 19 2  */
  --color-white:        #FFFFFF;
  --color-black:        #000000;

  /* Semantic (neutral-only; state colors not specified by Biuman masters) */
  --color-text-primary:   #1B1B1B;
  --color-text-secondary: #A4A9A6;
  --color-text-on-dark:   #FFFFFF;
  --color-bg-page:        #F0EEED;
  --color-bg-dark:        #1B1B1B;
  --color-border:         #A4A9A6;
}
```

---

## 3. Typography

### 3.1 Primary Brand Font — Pragmática Ext
The official typeface is **Pragmática Ext** (Pragmatica Extended) — an extended-width, geometric/grotesque
sans with **rounded terminals** and uniform monoline strokes. It is used for the wordmark, headings, body
and the brand character set shown in the Brandbook (section 008, TIPOGRAFÍA DE MARCA). The **`Biuman`
wordmark** is set in this family — rounded, geometric lowercase letterforms (the dotted `i`, the curved
stems of `u`).

> ⚠️ Pragmática Ext is a **licensed commercial font** and must be licensed separately. Do not substitute
> freely available fonts in production without brand approval. The five OTF master weights are stored in
> `biuman_brand/FONTS/`. For development/prototyping, use the
> system-ui fallback stack below.

**Available weights (5 OTF masters, on-disk filenames verified):**

| Weight | OTF master filename (verified on disk) |
|---|---|
| ExtraLight | `Pragmatica Ext ExtraLight Reg.otf` |
| Light | `Pragmatica Ext Light Reg.otf` |
| Book / Regular | `Pragmatica Ext Book Reg.otf` |
| Medium | `Pragmatica Ext Medium Reg.otf` |
| ExtraBold | `Pragmatica Ext ExtraBold Reg.otf` |

> The Backbone source deck cited PostScript names `PragmaticaExtExtraLight-Reg`, `PragmaticaExtLight-Reg`,
> `PragmaticaExtBook-Reg`, `PragmaticaExtMedium-Reg`, `PragmaticaExtExtraBold-Reg` — **per the source deck;
> not re-verified against font metadata.** Reference the verified filenames above when loading the faces.
> No italic variants are present.

```css
font-family: 'Pragmatica Ext', system-ui, -apple-system, sans-serif;
```

**Fallback for dev (Pragmática Ext not available):** use any extended geometric grotesque (or `system-ui`)
as a development convenience. **No fallback is specified by the Biuman masters** — fallback choice is an
implementation decision, not a brand spec.

### 3.2 Typography Rules
- The **descriptor / tagline** lock-ups are set in **uppercase**, three lines, left-aligned, mixing
  **Regular + Bold** weights to emphasize key words (e.g. `CIENCIA` and `MOVIMIENTO` bold, `DEL` regular).
- The **wordmark** is **lowercase** `Biuman` in the rounded display cut of the family.
- **Brand name in running text:** the wordmark is the lowercase **`Biuman`**. How the brand name should be
  cased/weighted inside body copy (e.g. capitalized "Biuman" vs. all-lowercase) is **no especificado en el
  material fuente** — default to capitalized **"Biuman"** in prose for readability, reserving the
  all-lowercase treatment for the wordmark/logo itself.
- High-contrast layout: large section titles, generous negative space, section numbering (001–009).
- Detailed paragraph-level rules (alignment, line-height, type scale, min sizes) are **no especificado en
  el material fuente** — the Brandbook type section (008) shows the character set but not numeric paragraph
  specs in the pages reviewed.

### 3.3 Type Scale (Tailwind)

> **⚠️ Legacy / illustrative.** Biuman's masters define no numeric type scale — **no especificado en el
> material fuente.** For product UI, take the type scale from the **Pháros registry**
> (`brands/pharos_brand/registry/tokens.css` + `frontend-standards.md`). No Biuman-specific scale is reproduced here.

### 3.4 Monospaced / Data Font

> **⚠️ Product UI font standard.** Across the **Pháros product family** the data + label font is
> **IBM Plex Mono** (per the Pháros registry, *not* a Biuman spec). Biuman's masters do **not** specify a
> monospaced/data typeface (**no especificado en el material fuente**). The Brandbook only documents
> **Pragmática Ext** as the single brand typeface. For product code/data, use IBM Plex Mono per the
> registry; the Biuman fitness-app mockups (Brandbook p.45 — "DATA", "WORK TIME", "ENERGY LEVEL") render
> their metric UI in the brand sans, with no separate data face called out.

---

## 4. Logo Usage

### 4.1 Logo Structure
The Biuman identity has two core elements:
1. **Logotipo / wordmark** — `Biuman` in **lowercase**, drawn in the rounded-terminal geometric brand
   typeface (Pragmática Ext style); uniform monoline strokes, the `i` carries a dot.
2. **Isotipo / símbolo (monograma "B")** — a geometric capital **B** built from a vertical bar plus
   right-angle (rectangular) bowl strokes, with an inset rectangular counterform/cut. The Brandbook
   labels it **"V.1 / ÍCONO"** and shows its construction on a **3×3 module grid** (p.20) and
   conceptually over **a superimposed circle + square** (p.37, with the MOVEMENT / HUMANS / GOD labels).

A thin **vertical divider bar** separates the wordmark from its descriptor in the lock-up versions.

**Logo color treatments (Brandbook applications, pp. 25–31).** Three treatments are defined, applicable to
wordmark + descriptor, wordmark only, and the isotipo `B`:

| Treatment | Color | Background |
|---|---|---|
| **Positivo** | Black `#1B1B1B` | Light / off-white / white. |
| **Negativo** | White / off-white `#F0EEED` | Near-black `#1B1B1B`. |
| **Monocromático** | Greenish mid-grey `#A4A9A6` (Pantone 429 C) | Light & medium grounds. |

### 4.2 Logo Versions

> The Brandbook (section 002, "Versiones de Logo") defines **four interchangeable versions** chosen by the
> space available, plus the standalone **isotipo**. The committed PNG assets in
> `brands/biuman/logos/` are renamed to a consistent kebab-case scheme (mirroring the LCH `logos/` scheme)
> and reconciled to the rendered artwork.

**Brandbook-defined versions:**

| # | Version | Composition |
|---|---|---|
| **V.1** | Wordmark + bar + descriptor | `Biuman` + vertical bar + `HUMANS / CONQUERING / MOVEMENT` (CONQUERING & MOVEMENT bold, HUMANS regular). |
| **V.2** | Wordmark + bar + descriptor | `Biuman` + vertical bar + `CIENCIA / DEL / MOVIMIENTO` (CIENCIA & MOVIMIENTO bold, DEL regular). |
| **V.3** | Wordmark + bar + descriptor | `Biuman` + vertical bar + `CENTRO DE / EXPERIENCIA / MOVIMIENTO` (EXPERIENCIA & MOVIMIENTO bold, CENTRO DE regular). |
| **V.4** | Wordmark only | `Biuman` alone, no descriptor. |
| **ÍCONO V.1** | Isotipo only | The geometric `B` monogram. |

**Committed PNG assets (mapped to `brands/biuman/logos/`):**

| File (renamed) | Source master | Dims / alpha | Version | Canonical? | Use Case |
|---|---|---|---|---|---|
| `logo-horizontal.png` | `Biuman logo.png` | 1413×567, alpha ✓ | Horizontal lockup: `Biuman` + bar + `LABORATORIO / DEPORTIVO` | ✅ canonical | Wide headers, navbars, side-by-side contexts. |
| `logo-icon.png` | `logoB.png` | 485×560, alpha ✓ | Isotipo / `B` monogram only | ✅ canonical | Favicon, avatar, small icon slots; transparent contexts. |
| `logo-icon-square.png` | `logoF.png` | 200×200, **no alpha** | Square icon — small `B` on off-white | — | Favicon-style flattened variant; prefer `logo-icon.png` where transparency is needed. |
| `logo-avatar-white.png` | `Logo.png` | 283×283, alpha ✓ | White `Biuman` wordmark on near-black circle | ✅ canonical (avatar) | Social avatar / dark-circle inverse mark. |

> **Descriptor discrepancy — flagged.** The supplied horizontal-lockup PNG reads **"LABORATORIO
> DEPORTIVO"**, whereas the Brandbook's four documented versions use **HUMANS CONQUERING MOVEMENT /
> CIENCIA DEL MOVIMIENTO / CENTRO DE EXPERIENCIA MOVIMIENTO**. Treat the PNG's "LABORATORIO DEPORTIVO" as
> a later applied descriptor; confirm the approved descriptor set with brand management before shipping a
> lockup (see Open Questions).

> **SVG status (stopgap).** True vector `.svg` exports are **missing** — the only vector masters are the
> Adobe Illustrator `.ai` files (`LOGO BM.ai`, `LogoB.ai`), which are **not committed** (heavy binaries,
> reference only). **TODO:** author real `.svg` exports of the canonical marks from the `.ai` masters.
> Mind the gitleaks allowlist pattern `brands/**/logos/*.svg` if base64-embedded SVGs are ever added.

### 4.3 Clear Space
**"Espacio vital"** (Brandbook section 005, pp. 17–20): the protection area is built from the **isotipo
`B` used as the measuring module** — a respect area equal to **1 `B`** around the lock-up, on a reticule;
in the Backbone construction the `B` is also placed at the corners around the logotype. Rule stated
verbatim: **"Mantener límites con otras marcas."** (Keep boundaries with other brands.)

### 4.4 Minimum Sizes (Brandbook section 004, "Tamaños de Marca")

| Element | Print | Digital |
|---|---|---|
| Versions 1, 2 & 3 (wordmark + descriptor) | 9.5 cm | 280 px |
| Version 4 (wordmark only) | 2 cm | 60 px |
| Ícono / isotipo (V.1) | 0.7 cm | 20 px |

### 4.5 Responsive Reduction (web components)

```
Viewport ≥ 1024px  →  Full lockup: wordmark "Biuman" + bar + descriptor (V.1/V.2/V.3)
Viewport 640–1023px →  Reduced: wordmark "Biuman" only (V.4)
Viewport < 640px   →  Icon only: isotipo "B"
```

> Breakpoint mapping is an implementation convention aligned to the documented min-sizes; the masters
> specify the **min sizes** (§4.4), not breakpoints — **breakpoints no especificado en el material fuente.**

### 4.6 Avatar / Social Media
- Approved avatar variant from the masters: the **white `Biuman` wordmark on a near-black circle**
  (`logo-avatar-white.png`).
- For icon/avatar slots, use the **isotipo `B`** (`logo-icon.png`) with padding.
- Padding ratio for square/circular avatars: **no especificado en el material fuente** (LCH uses ¼-height;
  Biuman masters don't state a value).

### 4.7 ❌ Logo Don'ts
Explicit do's-and-don'ts pages were **not present** in the masters reviewed — **no especificado en el
material fuente.** The one stated rule is **"Mantener límites con otras marcas"** (keep clear space from
other brands). Pending an official misuse sheet, apply the conservative defaults: never rotate, tilt,
stretch, distort, recolor outside the `#1B1B1B` / `#FFFFFF` / `#A4A9A6` system, add shadows/outlines,
break the wordmark/descriptor spacing, or place on low-contrast backgrounds.

### 4.8 Vue Component Usage

> Filenames map to the kebab-case canonical assets (§4.2). `.svg` exports do not exist yet (§4.2 SVG
> status) — these reference the committed PNGs; swap to true vectors when authored (no code change needed
> beyond the extension).

```vue
<!-- Use as <BiumanLogo> with theme/size props -->
<template>
  <img
    :src="logoSrc"
    :alt="'Biuman — Centro de Experiencia Deportiva'"
    :height="height"
    class="object-contain"
  />
</template>

<script setup>
const props = defineProps({
  theme: { type: String, default: 'light' },  // 'light' | 'dark'
  size:  { type: String, default: 'default' }, // 'default' | 'navbar' | 'icon' | 'avatar'
})

// Maps to the canonical kebab-case assets in brands/biuman/logos/.
const logoSrc = computed(() => {
  if (props.size === 'icon')   return '/assets/logos/biuman/logo-icon.png'         // isotipo B
  if (props.size === 'avatar') return '/assets/logos/biuman/logo-avatar-white.png' // white-on-dark circle
  // light/dark themes both use the horizontal lockup; recolor handled by the asset/treatment
  return '/assets/logos/biuman/logo-horizontal.png'
})

const height = computed(() => ({
  icon: 24, avatar: 40, navbar: 36, default: 48
})[props.size])
</script>
```

---

## 5. Iconography System

**no especificado en el material fuente.** The masters reviewed do not include a dedicated iconography
system / icon set. The closest stated direction is the geometric, rounded-terminal construction language
of the typeface and the `B` isotipo (built on a circle + square, 3×3 grid). For product UI iconography,
follow the **Pháros registry** icon standard; if a Biuman-themed icon set is later authored, match the
**rounded-terminal, geometric, monoline** character of Pragmática Ext and the `B` mark.

---

## 6. Photography & Imagery Guidelines

### 6.1 Style
The Backbone states the **"Receta Visual"** explicitly: **Fotografía, tipografía, superposición gráfica**
(graphic overlay), **editorial, texturas en movimiento** (textures in motion). Overall style: **minimal,
tech, inspirador** — scientific-meets-athletic.
- **Casting:** *deportistas reales* (real athletes), professionals and amateurs.
- **Scenarios:** tech / specialized (gym, club, track, court, lab), natural / open nature, urban.
- **Theme:** *"El poder inspirador del movimiento, la conquista del cuerpo humano."*
- **Subjects (Brandbook applications):** human body in motion and sport — basketball, cycling, swimming,
  running, gymnastic/inverted athletic figures.
- **Graphic resources:** water / rippled-surface textures on black & grey grounds; anatomical / x-ray and
  biological textures; the base geometric forms (circle + square) used in symbol construction; the
  large-format `B` monogram used as a compositional element.

### 6.2 Color Treatment
- **High-contrast black & white**, desaturated / monochrome treatment over **grey-greige** grounds — the
  imagery color recipe is stated as **"blanco, negro, gris."**
- Photography is combined with flat neutral backgrounds and the typography/lock-up in white, preserving
  the minimal language.
- The salmon-flesh macro texture seen in the Backbone moodboard is a **photographic texture accent**, not
  a palette color (see §2.2).

### 6.3 Illustration
**no especificado en el material fuente** as a distinct illustration style. The graphic-language elements
that stand in for illustration are the **geometric construction forms (circle + square)**, the
**large-format `B` monogram**, and **texturas en movimiento** (water/anatomical textures) used as overlays.

---

## 7. Component Patterns (Nuxt 4 / Vue / Tailwind)

> **⚠️ Reference only.** Product UI must be built from the **Pháros registry** tokens/components, themed for
> the Biuman tenant. These snippets illustrate the monochrome Biuman identity palette, not the product
> contract. Biuman defines no semantic-state colors, so badges below borrow only the neutral tones.

### 7.1 Primary Button
```vue
<button class="bg-biuman-black hover:bg-black text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200">
  Empezar
</button>
```

### 7.2 Secondary Button
```vue
<button class="border border-biuman-black text-biuman-black hover:bg-biuman-light font-medium px-6 py-3 rounded-lg transition-colors duration-200">
  Ver datos
</button>
```

### 7.3 Data / Metric Display
```vue
<!-- Biuman defines no dedicated data font; product UI uses IBM Plex Mono per the Pháros registry -->
<div class="text-2xl font-medium text-biuman-black tabular-nums">
  {{ value }}
</div>
<div class="text-sm text-biuman-grey tracking-wide uppercase">
  {{ label }}
</div>
```

### 7.4 Status Badge
```vue
<!-- Neutral-only; Biuman has no brand state colors — use Pháros registry semantic tokens for real states -->
<span class="bg-biuman-grey/30 text-biuman-black text-xs font-medium px-3 py-1 rounded-full">{{ status }}</span>
```

### 7.5 Card Surface
```vue
<div class="bg-white border border-biuman-grey rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
  <!-- content -->
</div>
```

### 7.6 Input Field
```vue
<input
  class="w-full border border-biuman-grey rounded-lg px-4 py-3 text-biuman-black placeholder-biuman-grey
         focus:outline-none focus:ring-2 focus:ring-biuman-black focus:border-biuman-black transition"
  placeholder="Nombre del atleta"
/>
```

---

## 8. Layout Principles

- **High contrast + generous negative space** is the governing layout trait of the brand book (large
  section titles, numbering 001–009, descriptors in the lower-right corner).
- **Monochrome surfaces:** off-white `#F0EEED`, mid-grey `#A4A9A6`, near-black `#1B1B1B`, white.
- Numeric grid / spacing / radius specs are **no especificado en el material fuente** — for product UI use
  the **Pháros registry** layout tokens (spacing/radius/flatness). LCH-style defaults (12-col grid, 4px
  spacing scale, `rounded-lg` cards) may be used as a development convenience only.

---

## 9. FastAPI (Python Backend) — Naming & Copy

When generating API responses, error messages, or user-facing strings for Biuman surfaces:
- **Spanish is the default** user-facing language (English reserved for brand/campaign lines).
- Tone: direct, *de atleta a atleta*, *certera y eficaz* — performance-oriented, inspiring but precise;
  avoid slang and over-elaboration.
- Example:
  ```python
  # ✅ Brand-aligned (direct, athlete-facing)
  {"message": "No encontramos tus datos. Verifica tu número de documento."}
  # ❌ Cold / generic
  {"detail": "Record not found"}
  ```
- Field names: `snake_case` in Python → `camelCase` in Vue via Nuxt `useFetch`.
- Date formats: `DD/MM/YYYY` for display, ISO 8601 for API interchange.

---

## 10. Quick Reference Card

```
BRAND NAME    Biuman — Centro de Experiencia Deportiva
              ("Laboratorio Deportivo" appears on logo artwork only — see §4.2 discrepancy)
TENANT OF     Pháros product family → Pháros LIS deportivo  (sibling of LCH; not a sub-brand, not the maker)
TAGLINE (ES)  La ciencia del movimiento.
CLAIM (EN)    Humans Conquering Movement.
URL           www.biuman.com

PALETTE (3 tones, monochrome — no chromatic accent)
 LIGHT        #F0EEED   CMYK 10/7/5/0     Cool Gray C   (off-white surface)
 BLACK        #1B1B1B   CMYK 65/66/68/82  Black C       (text / dark ground)
 GREY         #A4A9A6   CMYK 35/23/19/2   Pantone 429 C (neutral accent / mono logo)
 + pure #FFFFFF / #000000 for contrast

BRAND FONT    Pragmática Ext (5 OTF weights: ExtraLight·Light·Book·Medium·ExtraBold) — licensed
DATA FONT     Product UI = IBM Plex Mono (Pháros registry); Biuman defines none

LOGO          wordmark "Biuman" (lowercase) + isotipo "B" monogram
LOGO COLORS   positivo #1B1B1B · negativo #F0EEED/white · mono #A4A9A6 (429 C)
LOGO MIN      V1/V2/V3 9.5cm·280px · V4 2cm·60px · ícono 0.7cm·20px
CLEAR SPACE   1 × the isotipo "B" module around the lockup ("Mantener límites con otras marcas")
```

---

## Appendix — Masters & Assets

**Brand masters (heavy — reference only, do NOT commit to git):**
- `biuman_brand/Brandbook-BIUMAN.pdf` — full brand book (47 pp; Adobe Illustrator
  25.4, 2023-06-08). Sections seen: 001 Versiones de Logo · 002 Versiones · 003 Ícono de Marca ·
  004 Tamaños de Marca · 005 Planimetría / Espacio Vital · 006 Color de Marca · 007 Aplicaciones ·
  008 Tipografía de Marca · 009 Recursos Visuales de Marca. **Authoritative source for palette & logo specs.**
- `biuman_brand/Backbone-BIUMAN.pdf` — concise strategy backbone ("Brand Wondering",
  23 pp; MDE, 2023/01/06). **Authoritative source for positioning, personality/archetypes, values, voice.**
- `biuman_brand/LOGO BM.ai` (1.3 MB) and `LogoB.ai` (1.3 MB) — editable Adobe
  Illustrator vector masters. **The only true vectors; do NOT commit — point here for vector exports.**
- `biuman_brand/FONTS/` — the five **Pragmática Ext** OTF weights (see §3.1).

**Logo PNGs (light — safe to copy into `brands/biuman/logos/`, all <30 KB):**
- `Biuman logo.png` → `logo-horizontal.png` (horizontal lockup)
- `logoB.png` → `logo-icon.png` (isotipo `B`, transparent)
- `logoF.png` → `logo-icon-square.png` (flattened square icon, no alpha)
- `Logo.png` → `logo-avatar-white.png` (white wordmark on dark circle)

> True `.svg` vectors are **missing** (§4.2 SVG status). TODO: author SVG exports from the `.ai` masters.

> **Section-numbering note vs LCH.** This file mirrors `hematologico/LCH-BRAND.md` §§1–10. The §4 logo
> subsections preserve LCH numbering (4.7 = Don'ts, 4.8 = Vue Component); the logo color-usage table is
> folded into §4.1 rather than added as an extra subsection. "Masters & Assets" is kept as an **unnumbered
> appendix** so the Quick Reference Card stays at the canonical §10 slot.

---

*Brand concept and strategy ("Backbone — Brand Wondering / The Anatomy Of Magic") and visual identity
manual produced in Medellín (MDE), 2023. Biuman is a tenant of the Pháros product family (maker: Interval ·
The Human Tech Co.; see `pharos_brand/BRAND.md` §10). This specification compiled from the Biuman masters
for digital development use, 2026.*
