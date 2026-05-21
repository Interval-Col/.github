# Pháros — Brand Book
> Visual identity manual and design system for the LCH Quality Control module.
> Strategy and meaning live in `BACKBONE.md`. This document defines how Pháros *looks*, *sounds*, and *behaves* in code.

For AI coding assistants: this file is authoritative for all UI, copy, and component generation in any Pháros repository. When in doubt about strategy or tone, consult `BACKBONE.md`.

---

## 1. Brand at a Glance

```
NAME              Pháros
PARENT            Laboratorio Clínico Hematológico
PURPOSE           Internal quality control module
TAGLINE           Control de Calidad
MANTRA            Vigilamos lo invisible para que la verdad pueda verse.
LANGUAGE          Spanish primary · English secondary
TONE              Technically precise · humanly warm · never alarmist
```

---

## 2. Logo

### 2.1 Anatomy
The Pháros mark is a **typography-led wordmark** with one symbolic element:

- **Wordmark**: "Pháros" set in Fraunces (variable serif, optical size 144), regular weight, in LCH burgundy `#782F40`.
- **Pilot light**: a small red dot floating above the P, in LCH brand red `#E4002B`. It functions as an indicator light — quietly referencing the lighthouse without depicting one.
- **Sublabel** (when used): "CONTROL DE CALIDAD" in Helvetica Neue, 9px, wide-tracked at 0.32em letter-spacing, muted gray `#888B8D`.

### 2.2 Versions

| File | Use case |
|---|---|
| `pharos-horizontal-light.svg` | Main pages, white/light backgrounds |
| `pharos-horizontal-dark.svg` | Dark headers, sidebars |
| `pharos-navbar-light.svg` | Top navbar, light theme |
| `pharos-navbar-dark.svg` | Top navbar, dark theme |
| `pharos-icon-light.svg` | Favicon, app icon (P + dot only) |
| `pharos-icon-dark.svg` | Favicon on dark surfaces |

Files live at `/public/assets/logos/` in each Pháros project, or are pulled from the org `.github/brands/Pháros/logos/` repo.

### 2.3 Clear space
Minimum clear space on all sides = the height of the lowercase "h" in the wordmark.

### 2.4 Minimum sizes
- Horizontal: 140px wide minimum (digital) · 4cm (print)
- Navbar: 110px wide minimum
- Icon: 24px square minimum

### 2.5 Don'ts
- Never separate the pilot-light dot from the wordmark.
- Never recolor the dot to anything other than `#E4002B`.
- Never recolor the wordmark to anything other than `#782F40` (light bg) or `#FFFFFF` (dark bg).
- Never use a different typeface for the wordmark.
- Never add effects: shadow, glow, gradient, outline, italic.
- Never tilt, stretch, or distort.
- Never place on backgrounds where contrast falls below WCAG AA.

---

## 3. Color System

Pháros uses a **deliberately restrained subset** of the LCH palette. Restraint is part of the brand — Pháros earns trust by not being visually loud.

### 3.1 Primary

| Token | Hex | Role |
|---|---|---|
| `--pharos-burgundy` | `#782F40` | Wordmark, headers, primary text on light bg |
| `--pharos-red` | `#E4002B` | Pilot light, critical alerts, focus states |

### 3.2 Inherited from LCH (used sparingly)

| Token | Hex | When to use |
|---|---|---|
| `--lch-navy` | `#003A70` | Data charts, dark UI surfaces, secondary headings |
| `--lch-teal` | `#A0D1CA` | Success states, "in control" indicators |
| `--lch-yellow` | `#FBD872` | Warning states, drift indicators |
| `--lch-blush` | `#F4CDD4` | Soft surface backgrounds (rarely) |

### 3.3 Neutrals

| Token | Hex | Role |
|---|---|---|
| `--neutral-black` | `#000000` | Body text, max emphasis |
| `--neutral-gray-dark` | `#888B8D` | Secondary text, labels, captions |
| `--neutral-gray-mid` | `#C8C9C7` | Borders, dividers |
| `--neutral-gray-light` | `#F5F5F4` | Surface backgrounds, off-white card fills |
| `--neutral-white` | `#FFFFFF` | Page background, text on dark |

### 3.4 Semantic aliases for QC states

QC is the core domain of Pháros — these states have specific meanings:

| Token | Hex | QC meaning |
|---|---|---|
| `--qc-in-control` | `#A0D1CA` | Process within acceptable range |
| `--qc-drift` | `#FBD872` | Trending toward limits — attention needed |
| `--qc-out-of-control` | `#E4002B` | Outside acceptable range — action required |
| `--qc-pending` | `#C8C9C7` | Awaiting evaluation |
| `--qc-resolved` | `#326295` | Issue acknowledged and corrected |

### 3.5 Tailwind config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        pharos: {
          burgundy: '#782F40',
          red:      '#E4002B',
        },
        // LCH inheritance (only what Pháros uses)
        lch: {
          navy:   '#003A70',
          teal:   '#A0D1CA',
          yellow: '#FBD872',
          blush:  '#F4CDD4',
        },
        qc: {
          'in-control':     '#A0D1CA',
          'drift':          '#FBD872',
          'out-of-control': '#E4002B',
          'pending':        '#C8C9C7',
          'resolved':       '#326295',
        }
      }
    }
  }
}
```

### 3.6 CSS custom properties

```css
:root {
  --pharos-burgundy: #782F40;
  --pharos-red:      #E4002B;
  --lch-navy:        #003A70;
  --lch-teal:        #A0D1CA;
  --lch-yellow:      #FBD872;
  --lch-blush:       #F4CDD4;
  --neutral-black:      #000000;
  --neutral-gray-dark:  #888B8D;
  --neutral-gray-mid:   #C8C9C7;
  --neutral-gray-light: #F5F5F4;
  --neutral-white:      #FFFFFF;
  --qc-in-control:     #A0D1CA;
  --qc-drift:          #FBD872;
  --qc-out-of-control: #E4002B;
  --qc-pending:        #C8C9C7;
  --qc-resolved:       #326295;
}
```

---

## 4. Typography

### 4.1 Fonts

| Role | Font | Loaded from | Fallback |
|---|---|---|---|
| Display / wordmark | **Fraunces** (variable, opsz 9–144) | Google Fonts | Times New Roman, serif |
| UI / body | **Inter** (variable) | Google Fonts | system-ui, sans-serif |
| Data / metrics | **JetBrains Mono** | Google Fonts | Courier New, monospace |
| Labels / table headers | **IBM Plex Mono** | Google Fonts | monospace |

### 4.2 Font loading (Nuxt 4)

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap'
        }
      ]
    }
  }
})
```

### 4.3 Type scale

| Use | Size | Line height | Font | Weight |
|---|---|---|---|---|
| Hero / page title | 48px | 1.1 | Fraunces | 400 |
| Section title | 32px | 1.2 | Fraunces | 400 |
| Subsection | 20px | 1.4 | Inter | 600 |
| Body | 15px | 1.6 | Inter | 400 |
| Body small | 13px | 1.5 | Inter | 400 |
| Label | 11px | 1.4 | IBM Plex Mono | 500 (uppercase, 0.18em tracking) |
| Data value | 22px | 1.0 | JetBrains Mono | 500 (tabular-nums) |
| Data value small | 14px | 1.0 | JetBrains Mono | 400 (tabular-nums) |

### 4.4 Typography rules
- Body text: always left-aligned. Never justified.
- Line height: 1.6× for body, 1.2× for headlines.
- Brand name in running text: always title case "Pháros", never ALL CAPS.
- LCH brand name in running text: full form, "Laboratorio Clínico Hematológico", title case.
- Data and numerical values: always JetBrains Mono with `tabular-nums` — columns must align in tables.
- Headlines: never ALL CAPS — use weight contrast instead.

---

## 5. Voice & Copy

### 5.1 Tone
- **Technically precise** — use the right word, not a rough approximation.
- **Humanly warm** — use full sentences, complete thoughts, no abrupt commands.
- **Calm** — never alarmist. Urgency comes from clarity, not from volume or color.
- **Bilingual-ready** — Spanish first, English second. Both in the same register.

### 5.2 Copy patterns

```
✅  Tres muestras fuera de rango en el último turno.
❌  ¡ALERTA! Anomalía detectada.

✅  El instrumento 3 está derivando hacia el límite superior.
❌  FALLA en instrumento 3.

✅  Todo en orden.
❌  ¡Excelente! ¡Sin problemas! 🎉

✅  Detener la corrida. La control falló.
❌  Por favor considera pausar el proceso si no es inconveniente.

✅  No encontramos el lote 2024-0341. Verifica el código.
❌  Lote inexistente. Error 404.
```

### 5.3 FastAPI response patterns

```python
# ✅ Pháros voice
{"message": "El control fuera de rango. Revisa el instrumento 3 antes de continuar."}

# ❌ Generic
{"detail": "Validation failed"}
```

### 5.4 Reusable slogans (from BACKBONE.md)
- *"La luz que verifica."*
- *"Cada resultado tiene un guardián."*
- *"Vigilancia serena, resultados confiables."*
- *"Lo invisible también se cuida."*

Use these for marketing surfaces, splash screens, empty states. Never for transactional UI copy.

---

## 6. Component Patterns

### 6.1 Primary button
```vue
<button class="bg-pharos-burgundy hover:bg-pharos-red text-white font-medium px-6 py-3 rounded-lg transition-colors">
  Aprobar control
</button>
```

### 6.2 Secondary button
```vue
<button class="border border-pharos-burgundy text-pharos-burgundy hover:bg-lch-blush/30 font-medium px-6 py-3 rounded-lg transition-colors">
  Ver detalles
</button>
```

### 6.3 QC state badge
```vue
<!-- In control -->
<span class="bg-qc-in-control/30 text-pharos-burgundy text-xs font-medium px-3 py-1 rounded-full">
  En control
</span>

<!-- Drift -->
<span class="bg-qc-drift/40 text-neutral-black text-xs font-medium px-3 py-1 rounded-full">
  Derivando
</span>

<!-- Out of control -->
<span class="bg-qc-out-of-control/10 text-pharos-red text-xs font-medium px-3 py-1 rounded-full">
  Fuera de rango
</span>
```

### 6.4 Data card
```vue
<div class="bg-white border border-neutral-gray-mid rounded-xl p-6 hover:shadow-md transition-shadow">
  <div class="font-['IBM_Plex_Mono'] text-xs uppercase tracking-[0.18em] text-neutral-gray-dark mb-2">
    Coeficiente de variación
  </div>
  <div class="font-['JetBrains_Mono'] text-3xl font-medium text-pharos-burgundy tabular-nums">
    2.4%
  </div>
  <div class="text-sm text-neutral-gray-dark mt-1">
    Dentro de rango aceptable
  </div>
</div>
```

### 6.5 Input
```vue
<input class="w-full border border-neutral-gray-mid rounded-lg px-4 py-3
              text-neutral-black placeholder-neutral-gray-dark
              focus:outline-none focus:ring-2 focus:ring-pharos-red focus:border-pharos-red transition" />
```

### 6.6 Pilot-light status indicator
The signature Pháros UI element — a pulsing dot that shows live system health.

```vue
<div class="flex items-center gap-2">
  <span class="relative flex h-2 w-2">
    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-pharos-red opacity-50"></span>
    <span class="relative inline-flex rounded-full h-2 w-2 bg-pharos-red"></span>
  </span>
  <span class="text-xs text-neutral-gray-dark font-['IBM_Plex_Mono'] uppercase tracking-wider">
    Sistema activo
  </span>
</div>
```

---

## 7. Layout Principles

- **Grid**: 12 columns, 24px gutters on desktop, 16px on mobile.
- **Max content width**: 1280px.
- **Spacing scale**: 4px base (Tailwind default).
- **Border radius**: `rounded-lg` (8px) for inputs/cards, `rounded-xl` (12px) for modals/major surfaces, `rounded-full` for badges and pilot lights.
- **Shadows**: avoid by default. Pháros's calm comes from flatness. Use `shadow-sm` only on hover/focus.
- **Whitespace**: generous. Density should never exceed what a tired tech can read at a glance.

---

## 8. Iconography

- Use **Lucide** as the primary icon set.
- Stroke width: 1.5px (slightly thinner than default — matches Pháros's restraint).
- Default color: `text-neutral-gray-dark`.
- Sizes: 16px (inline), 20px (buttons/nav), 24px (section headers).
- Never use multi-color icons. Single stroke color only.

---

## 9. Photography & Imagery

Pháros rarely uses imagery. When it does:

- **Real lab environments**, not stock photos.
- **Calm color grade** — desaturated, no warm/cool extremes.
- **Focus on instruments and process**, not faces. Pháros is about the system, not the people running it.
- **No people-in-lab-coats clichés** — show the actual work being done.

---

## 10. Architectural Position

Pháros is a **sub-brand** of Laboratorio Clínico Hematológico. The relationship is:

```
Laboratorio Clínico Hematológico (master brand)
├── Finanzas              (operational module)
├── Pháros                (QC module — this brand)
└── [other modules...]
```

When Pháros and LCH appear together (e.g. login screens, footers, internal docs):
- LCH master logo dominates in size and position.
- Pháros sits below or beside, smaller, never competing.
- Format: `[LCH logo] | Pháros · Control de Calidad`.

When Pháros appears standalone (inside its own app, dashboard, navbar):
- Pháros can be the primary identity in that surface.
- A small "by Laboratorio Clínico Hematológico" credit appears in the footer.

---

## 11. Quick Reference Card

```
LOGO              Wordmark "Pháros" + red pilot-light dot above the P
WORDMARK FONT     Fraunces (variable serif, 400 weight)
WORDMARK COLOR    #782F40 (LCH burgundy)
PILOT LIGHT       #E4002B (LCH brand red)

UI FONT           Inter
DATA FONT         JetBrains Mono (with tabular-nums)
LABEL FONT        IBM Plex Mono (uppercase, 0.18em tracking)

QC GREEN          #A0D1CA (in control)
QC YELLOW         #FBD872 (drift)
QC RED            #E4002B (out of control)

VOICE             Spanish first · technical + warm · never alarmist
TAGLINE           Control de Calidad
MANTRA            Vigilamos lo invisible para que la verdad pueda verse.
PARENT            Laboratorio Clínico Hematológico
```

---

*This brand book is the authoritative source for Pháros visual and verbal identity in code. For strategic and conceptual questions, see `BACKBONE.md`. For master-brand inheritance details, see the LCH brand spec at the org level.*
