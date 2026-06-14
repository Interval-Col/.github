# Interval — Brand Book
> Visual identity manual and design system for **Interval — The Human Tech Co.**, the
> in-house software development house behind the LCH / Interval-Col product portfolio.
> This document defines how Interval *looks*, *sounds*, and *behaves* — in print, on
> screen, and in code.

For AI coding assistants: this file is authoritative for the **Interval house brand**
(the studio/company itself — landing pages, decks, repos, READMEs, internal tooling).
It is **not** the brand for the individual products. Products have their own books:
Pháros → `../pharos_brand/BRAND.md`, LCH → `../hematologico/LCH-BRAND.md`. See
§10 for how they relate.

Derived from the studio master `BRANDBOOK-INTERVAL nueva propuesta` (Adobe Illustrator,
Oct 2025) — the 81-page deck. The master `.ai`/`.pdf` are **not stored in this repo**
(too large); see §11 for what they are, where they live, and how to re-extract assets.

---

## 1. Brand at a Glance

```
NAME              Interval
DESCRIPTOR        The Human Tech Co.
ROLE              In-house software development house (the studio / parent brand)
YEAR              2023  ·  www.interval.com
LANGUAGE          Spanish primary · English for taglines/claims
MANIFESTO (ES)    La tecnología en pro de la libertad de tiempo y de la vida.
TAGLINES (EN)     Free time for smart ideas  ·  Pay attention to life
PHILOSOPHY        Wu Wei (Tao) — "no forzar": technology that gives time back
TONE              Calm · spacious · confident · human · quietly futuristic
LOOK              Black-first, high-contrast, generous negative space, one bold accent
```

The deck frames the brand around three words — **Backbone · Brand Wondering ·
The Anatomy of Magic** — and the Taoist idea of *Wu Wei* (acting without forcing).
The core belief: technology should *cover the fronts and optimize our time* so people
can spend that time **living, feeling, thinking** — "darle espacio a la mente de abrirse
y expandirse." That's the emotional center; everything visual serves that calm.

---

## 2. Concept / Backbone

Verbatim brand copy — preserve wording and Spanish; do not paraphrase in brand contexts.

> **Wu Wei** es un concepto proveniente del Tao que invita a "no actuar". A dejar que
> la vida pase mientras no hacemos, a parar por momentos y simplemente dejar que suceda.
> A tener espacios en blanco donde por sí sola la mente se exprese.

> Creemos que la tecnología debería tener la función de cubrir los frentes, de optimizar
> nuestros tiempos y de facilitarnos la vida… **Para poder usarla en vivir, en sentir,
> en pensar.** Inspirados por estos conceptos, usamos la tecnología en pro de la
> **libertad de tiempo y de la vida.**

Design implication: **white space is a brand asset, not empty space.** Layouts breathe.
Don't crowd. The "interval" — the gap, the pause, the space between — is the whole idea
and it shows up in the logotype, the icon, and the page composition.

---

## 3. Logo

### 3.1 Anatomy
The Interval mark is a **custom logotype** — the word *Interval* drawn (not typed) in a
segmented, geometric, mono-width construction where strokes are broken by deliberate
**gaps / intervals**. The letterforms read as built from timeline segments — the name
made visible. It is *not* one of the brand fonts; treat it as artwork.

- **Logotype**: "Interval", custom segmented letterforms. The leading **I** is a bare
  vertical bar with a small top notch that rhymes with the icon brackets.
- **Descriptor** (optional lockup): "THE HUMAN TECH CO." set small, uppercase,
  3 lines, in the brand mono/condensed face, locked to the right of the logotype.

### 3.2 Logo versions
| Version | Contents | Asset |
|---|---|---|
| **V1 — lockup** | Logotype + "THE HUMAN TECH CO." descriptor | `logos/interval-lockup-light.png` · `logos/interval-lockup-dark.png` |
| **V2 — wordmark** | Logotype alone | `logos/interval-wordmark-dark.png` |

Use V1 where there's room and you want the full positioning; V2 in tight or small
contexts. (Brand book p.003: *"dos versiones, con posibilidad de variar de acuerdo al
espacio destinado para su uso."*)

### 3.3 Icon / símbolo — the interval brackets `[ ]`
The brand icon is a pair of **bracket marks** `[` `]` (each with a small outer-corner
notch) framing empty space. The **negative space between them *is* the interval** — the
purest expression of the idea. Three uses (p.004):
- **V1** — brackets framing "THE HUMAN TECH CO."
- **V2** — brackets framing a claim, e.g. "PAY ATTENTION TO LIFE"
- **V3** — brackets alone (the minimal app/avatar icon) → `logos/interval-icon.png`

You may set short brand phrases *inside* the brackets. Keep the framed content centered
with even breathing room.

### 3.4 Minimum sizes (p.005)
Respect minimum reproduction sizes so the gaps stay legible:

| Variant | Print (min) | Digital (min) |
|---|---|---|
| 1 | 2.7 cm | 270 px |
| 2 | 1.0 cm | 100 px |
| 3 | 1.7 cm | 170 px |
| 4 | 1.2 cm | 120 px |
| 5 | 0.5 cm | 50 px |

### 3.5 Clear space — "Espacio vital" (p.005)
Maintain generous clear space; **keep boundaries from other marks** ("mantener límites
con otras marcas"). Use the height of the logotype's cap (or the bracket height for the
icon) as the minimum margin on all sides. When in doubt, give it more room — space is on-brand.

### 3.6 Don'ts
- Don't re-type "Interval" in a system font and call it the logo — the logotype is custom artwork.
- Don't close, fill, or "fix" the gaps in the letterforms or brackets — the gaps are the point.
- Don't recolor the mark outside the palette (black, white, or a single accent).
- Don't crowd it, add effects, outline, or place on busy imagery without enough contrast.
- Don't stretch, rotate, or rebuild the brackets at arbitrary proportions.

---

## 4. Color (p.006)

Five colors. **Hex/RGB are authoritative for digital and code.** CMYK/Pantone are
reproduced exactly as printed in the brand book — the book itself warns that on-screen
tones vary and to **confirm with a Pantonera before printing**.

| Role | Name | HEX | RGB | CMYK (per book) | Pantone |
|---|---|---|---|---|---|
| Ink / base | Process Black | `#121010` | 18 / 16 / 16 | 79 / 71 / 61 / 89 | Process Black C |
| Surface | White | `#FFFFFF` | 255 / 255 / 255 | 0 / 0 / 0 / 0 | — |
| Neutral | Cool Gray | `#C6C6C6` | 198 / 198 / 198 | 26 / 19 / 20 / 2 | Cool Gray 6 C |
| **Primary accent** | UT Naranja | `#FF8010` | 255 / 128 / 16 | 0 / 90 / 61 / 0 | UT Naranja |
| Secondary accent | Persian Indigo | `#261277` | 38 / 18 / 119 | 100 / 22 / 100 / 8 | Persian Indigo |

> Note: the CMYK figures for the two accents look transposed/atypical for these hues in
> the source deck — **trust the HEX/RGB for anything digital** and verify CMYK with the
> print provider (as the book instructs) before any litho run.

**Usage intent**
- `#121010` is the **default canvas** — Interval is a black-first brand. White is the
  primary type/logo color on it.
- `#FFFFFF` for light layouts and as the reverse logo color.
- `#C6C6C6` for secondary text, rules, captions, UI chrome.
- `#FF8010` (**UT Naranja**) is the **signature accent** — one bold pop per composition.
  Use sparingly: a single highlight, link, key word, or interactive state.
- `#261277` (**Persian Indigo**) is the supporting accent / second data color.
- Keep the look monochrome + **one** accent at a time; the orange should feel rare.

---

## 5. Typography (p.008)

Two brand fonts plus the custom logotype:

| Use | Typeface | Notes |
|---|---|---|
| Display / headlines / claims | **Pragmatica Cond** | Condensed grotesque; UPPERCASE, wide tracking for headlines and taglines |
| Secondary / body / labels / descriptor | **Avenue X Regular** | Clean grotesque; the "THE HUMAN TECH CO." descriptor and supporting copy |
| Logotype only | *custom "Interval" artwork* | Not a font — never substitute |

Full charset confirmed for both (incl. Ñ): `ABCDEFGHIJKLMNÑOPQRSTWXYZ 1234567890`.

**Setting conventions seen in the book**
- Headlines/taglines: Pragmatica Cond, all-caps, **wide letter-spacing**, lots of space around.
- Labels/section tags ("VERSIÓN 1", "PALETA", "FONTS"): all-caps, very wide tracking.
- Body: sentence case, comfortable leading.

**Digital fallback stack** (when the licensed fonts aren't embedded — e.g. web/app):
```
Display : "Pragmatica Cond", "Oswald", "Roboto Condensed", system-ui, sans-serif;
Text    : "Avenue X", "Inter", "Helvetica Neue", Arial, sans-serif;
```
> The licensed font files are **not** included here (licensing). Source them from the
> studio / foundry for production. The stacks above are visually-close open fallbacks.

---

## 6. Voice & messaging

- **Bilingual rhythm:** Spanish for the manifesto and body; punchy **English** for the
  signature claims.
- **Signature claims** (use verbatim):
  - `Free time for smart ideas`
  - `Pay attention to life`
  - `The Human Tech Co.`
  - ES manifesto: `La tecnología en pro de la libertad de tiempo y de la vida.`
- **Tone:** calm, spacious, human, quietly confident. Not hypey, not loud, no exclamation
  storms, no emojis in formal brand copy. Let silence/space carry weight.
- **Don't:** over-explain, stack buzzwords, or fill every gap with text. The pause is the brand.

---

## 7. Design / code tokens

Starter tokens for any Interval-branded surface (site, deck-to-web, internal tool). These
are the **house** tokens — products keep their own (Pháros etc.).

```css
:root {
  /* palette */
  --interval-black:  #121010;  /* base canvas (black-first) */
  --interval-white:  #ffffff;
  --interval-gray:   #c6c6c6;  /* secondary text, rules, chrome */
  --interval-orange: #ff8010;  /* UT Naranja — primary accent, use sparingly */
  --interval-indigo: #261277;  /* Persian Indigo — secondary accent */

  /* semantic (dark-first default) */
  --bg:        var(--interval-black);
  --fg:        var(--interval-white);
  --muted:     var(--interval-gray);
  --accent:    var(--interval-orange);
  --accent-2:  var(--interval-indigo);

  /* type */
  --font-display: "Pragmatica Cond", "Oswald", "Roboto Condensed", system-ui, sans-serif;
  --font-text:    "Avenue X", "Inter", "Helvetica Neue", Arial, sans-serif;

  /* space is a brand asset — bias generous */
  --space-page: clamp(2rem, 6vw, 6rem);
}
```
Conventions: black-first canvas; one accent per view; headlines uppercase + wide tracking
(`letter-spacing: 0.06em–0.12em`); never close the logotype/bracket gaps.

---

## 8. Assets in this folder

```
interval/
├─ INTERVAL-BRAND.md          ← this file (authoritative spec)
├─ logos/
│  ├─ interval-lockup-light.png   logotype + descriptor, white on black (dark surfaces)
│  ├─ interval-lockup-dark.png    logotype + descriptor, black on white (light surfaces)
│  ├─ interval-wordmark-dark.png  logotype only, black on white
│  ├─ interval-icon.png           the interval brackets [ ] (app/avatar icon)
│  └─ vector/                     true vector (SVG) extracted from the master PDF
│     ├─ interval-lockup-light.svg   (cover artboard — lockup, paths)
│     ├─ interval-wordmarks.svg      (logo-versions artboard — both V1 & V2)
│     └─ interval-icon.svg           (icon artboard — brackets)
└─ reference/                  full-page renders from the deck (human reference)
   ├─ 01-cover.png   04-logo-intro.png   06-logo-versions.png
   └─ 08-icon-v1-v2.png   09-icon-v3.png   24-color-palette.png   68-typography.png
```
> The editable **master `.ai`/`.pdf` are deliberately kept out of this repo** (≈57 MB).
> See §11 for what they are and where they're stored.
> The `vector/*.svg` are full-artboard exports (they include the artboard's labels/rules).
> The custom logotype inside them is real vector paths — open in a vector editor to pull
> a clean, transparent, recolorable mark. For production-grade isolated exports, use the
> `.ai` master in Illustrator.

---

## 9. Quick rules (TL;DR for builders)

1. **Black-first.** Default canvas `#121010`, white type/logo on it.
2. **One accent.** `#FF8010` orange, used rarely for a single highlight; `#261277` indigo supports.
3. **Space is sacred.** Generous margins; don't crowd; the gap/interval is the idea.
4. **Logo = artwork.** Use the provided files; never re-type it; never close the gaps.
5. **Type:** Pragmatica Cond (display, uppercase, wide tracking) + Avenue X (text).
6. **Voice:** calm, human, bilingual — ES manifesto + EN claims, verbatim.

---

## 10. Relationship to the org & sub-brands

**Interval** (this brand) is the **software development house** — the studio/parent
identity. It is distinct from, and the umbrella over, the product and tenant brands:

| Brand | Book | Role |
|---|---|---|
| **Interval** | *this file* | The dev house / company brand (decks, site, repos, internal tooling) |
| **Pháros** | `../pharos_brand/BRAND.md` | Product portfolio replacing the COBOL LIS (Fraunces + LCH palette) |
| **LCH** (Laboratorio Clínico Hematológico) | `../hematologico/LCH-BRAND.md` | The clinical lab client/tenant |
| **Biuman** | — | Second clinic tenant |

These do **not** share a palette or type system — Interval is black/orange/indigo with
Pragmatica Cond; Pháros is burgundy/red with Fraunces; LCH has its own (APAX font).
**Keep them separate.** Use Interval branding only for the house itself, not inside the
products. When a surface is ambiguous (e.g. an internal admin tool built by Interval for
an LCH product), the *product* brand wins on its own screens; Interval branding is for
"made by / about the studio" contexts.

---

## 11. Source & provenance

### 11.1 Master files (stored OUTSIDE this repo)
The editable masters are intentionally **not committed** here — they're ~57 MB and would
bloat the org `.github` repo (whose entire `.git` is ~3 MB). They are maintained in a
separate asset store:

| File | What it is | Size |
|---|---|---|
| `BRANDBOOK-INTERVAL nueva propuesta.ai` | Editable Adobe Illustrator master (81 artboards) | ~35 MB |
| `BRANDBOOK-INTERVAL nueva propuesta.pdf` | Flattened brand book (81 pages, 960×540 deck) | ~24 MB |

- **Provenance:** studio "nueva propuesta", Adobe Illustrator 29.5, Oct 2025.
- **Location:** _‹set when filed — e.g. brand drive / DAM / git-LFS asset repo›_.
  (TODO: update this line with the canonical path once the team places them.)
- For pixel-perfect, isolated, transparent logo exports, open the `.ai` in Illustrator
  and export the individual artboards.

### 11.2 How the committed assets were derived
This spec and everything in `logos/` + `reference/` was extracted from the master PDF
with `poppler` (`brew install poppler`):

```bash
F="BRANDBOOK-INTERVAL nueva propuesta.pdf"
pdftotext -layout "$F" out.txt                                   # text layer: hex, copy, fonts
pdftoppm  -png -r 150 -f 24 -l 24 "$F" page24                    # render a page (e.g. palette p.24)
pdftoppm  -png -r 300 -f 1 -l 1 -x 1150 -y 950 -W 1950 -H 430 \  # crop a logo region (px @ DPI)
          "$F" lockup-light
pdftocairo -svg -f 1 -l 1 "$F" lockup.svg                        # page → true vector SVG (logotype = paths)
```

The custom "Interval" logotype is **outlined vector** in the master (not a font), so the
`pdftocairo -svg` exports under `logos/vector/` carry the real letterform paths.

### 11.3 Section map
Page references (p.00x) map to the deck's own section markers: 002 Logo · 003 Icon ·
004 Sizes · 005 Clear space · 006 Color · 007 Applications · 008 Typography · 009 Resources.
