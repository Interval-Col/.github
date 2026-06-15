# Pháros — Brand Book
> Visual identity manual and design system for the **Pháros product family** — the software that replaces the COBOL LIS, built by Interval (LCH's in-house software house). Pháros began as LCH's Quality Control module; QC is now a set of surfaces *inside* Pháros LIS.
> Strategy and meaning live in `BACKBONE.md`. This document defines how Pháros *looks*, *sounds*, and *behaves* in code, and is the shared spec every sub-brand inherits.

For AI coding assistants: this file is authoritative for the **shared foundation** behind all UI, copy, and component generation in any Pháros repository. Each app's sub-brand (`sub-brands/*.md`) only records what it *adds to* or *overrides in* this foundation (accent colour, sub-name, icon tint). When in doubt about strategy or tone, consult `BACKBONE.md`.

---

## 1. Brand at a Glance

```
NAME              Pháros
TYPE              Umbrella brand for the software family (replaces the COBOL LIS)
BUILT BY          Interval · The Human Tech Co. — LCH's in-house software team
SERVES            LCH (Laboratorio Clínico Hematológico) · Biuman — the holding's labs
SEPARATOR         ·  (Pháros · <Sub-name>)
DESCRIPTOR        Control de Calidad — the QC/LIS surface (umbrella tagline TBD · RFC 0008)
MANTRA            Vigilamos lo invisible para que la verdad pueda verse.
LANGUAGE          Spanish primary · English secondary
TONE              Technically precise · humanly warm · never alarmist
```

> **Pháros is a family, not a module.** It is the umbrella over the apps Interval builds for the holding's labs — ERP (`Pháros · Timón`), LIS (clínico + deportivo), Admisiones, CRM, and the Archivo utility surface. It is **not** "the QC module of LCH": QC is now a set of surfaces *inside* Pháros LIS. See §10 for the full architecture and the shared-vs-differentiated split.

---

## 2. Logo

### 2.1 Anatomy
The Pháros mark is a **typography-led wordmark** with one symbolic element:

- **Wordmark**: "Pháros" set in Fraunces (variable serif, optical size 144), regular weight, in burgundy `#782F40`. The wordmark is the shared family constant — **never re-tinted to a sub-brand's accent**.
- **Pilot light**: a small red dot floating above the P, in red `#E4002B`. It functions as an indicator light — quietly referencing the lighthouse without depicting one. Also shared across the family, never re-tinted.
- **Separator + sub-name** (sub-brand lockup): `· <Sub-name>` after the wordmark — e.g. `Pháros · Timón`.
- **Sublabel** (when used): the sub-brand's functional descriptor in IBM Plex Mono, ~9px, wide-tracked at 0.18em letter-spacing, muted gray `#888B8D` — e.g. `ERP · FINANZAS Y OPERACIONES` (Timón). The shared horizontal mark carries **no** sublabel; descriptors live only in per-sub-brand lockups.

### 2.2 Versions

| File | Use case |
|---|---|
| `pharos-horizontal-light.svg` | Main pages, white/light backgrounds |
| `pharos-horizontal-dark.svg` | Dark headers, sidebars |
| `pharos-navbar-light.svg` | Top navbar, light theme |
| `pharos-navbar-dark.svg` | Top navbar, dark theme |
| `pharos-icon-light.svg` | Favicon, app icon (P + dot only) |
| `pharos-icon-dark.svg` | Favicon on dark surfaces |

Files live alongside this spec in `.github/brands/pharos_brand/`, and are copied into `/public/assets/logos/` in each Pháros project. Per-sub-brand lockups + accent-tinted icons live under `sub-brands/` once the names + accents lock (RFC 0008).

> The shared horizontal mark is the **Pháros wordmark + pilot dot** (no sublabel) — the pre-umbrella `CONTROL DE CALIDAD` sublabel + off-system Helvetica face were removed, the pilot dot was rescaled to the navbar's dot:P ratio (horizontal + icon), and the `@import` ampersand was XML-escaped across all six SVGs. Per-sub-brand lockups add the sub-name + descriptor (IBM Plex Mono, per §2.1) under `sub-brands/` once names lock. App chrome that still shows the old sublabel or an unaccented "Pharos" (e.g. lab-qc's `PharosLogo`) re-syncs with the full logo remake (RFC 0008 Implementation §).

### 2.3 Clear space
Minimum clear space on all sides = the height of the lowercase "h" in the wordmark.

### 2.4 Minimum sizes
- Horizontal: 140px wide minimum (digital) · 4cm (print)
- Navbar: 110px wide minimum
- Icon: 24px square minimum

### 2.5 Don'ts
- Never separate the pilot-light dot from the wordmark.
- Never recolor the dot to anything other than `#E4002B`.
- Never recolor the wordmark to anything other than `#782F40` (light bg) or `#FFFFFF` (dark bg) — not even to a sub-brand's accent.
- Never use a different typeface for the wordmark.
- Never add effects: shadow, glow, gradient, outline, italic.
- Never tilt, stretch, or distort.
- Never place on backgrounds where contrast falls below WCAG AA.

---

## 3. Color System

Pháros uses a **deliberately restrained subset** of the LCH palette. Restraint is part of the brand — Pháros earns trust by not being visually loud.

### 3.1 Family constant — the shared mark

| Token | Hex | Role |
|---|---|---|
| `--pharos-burgundy` | `#782F40` | Wordmark, headers, primary text on light bg — the shared mark, never re-tinted per app |
| `--pharos-red` | `#E4002B` | Pilot light, critical/error — the family constant |

These two are the visual signature shared across **every** sub-brand. A sub-brand's **accent** (one colour from the family palette below) is a *separate* colour for primary actions and active nav — it does **not** replace the burgundy wordmark or the red pilot light.

### 3.2 Family palette — each sub-brand draws ONE accent

The curated family palette is the **LCH colour set** (see `../hematologico/LCH-BRAND.md`); each sub-brand picks exactly one accent from it, so siblings stay siblings by construction.

| Token | Hex | When to use |
|---|---|---|
| `--lch-navy` | `#003A70` | **ERP (Timón) accent.** Data charts, dark UI surfaces, secondary headings |
| `--lch-teal` | `#A0D1CA` | Success states, "in control" indicators; ERP "en cuadre / conciliado" |
| `--lch-yellow` | `#FBD872` | Warning states, drift indicators |
| `--lch-blush` | `#F4CDD4` | Soft surface backgrounds (rarely) |

> Only **ERP = LCH Navy `#003A70`** is accent-locked; the other sub-brand accents are open (RFC 0008 Q6). A sub-brand records its accent in `sub-brands/*.md`; it never redefines the burgundy/red family constant.

### 3.3 Neutrals

| Token | Hex | Role |
|---|---|---|
| `--neutral-black` | `#000000` | Body text, max emphasis |
| `--neutral-gray-dark` | `#888B8D` | Secondary text, labels, captions |
| `--neutral-gray-mid` | `#C8C9C7` | Borders, dividers |
| `--neutral-gray-light` | `#F5F5F4` | Surface backgrounds, off-white card fills |
| `--neutral-white` | `#FFFFFF` | Page background, text on dark |

### 3.4 QC state palette (inside Pháros LIS)

QC folded into **Pháros LIS** (RFC 0004 §2). Its burgundy/red survives as a **state palette** — a recognizable status language for QC surfaces inside LIS, **not** a sibling accent and **not** the LIS sub-brand's accent. These are the LIS expression of the accent-**independent** status layer (success/warning/error/info), so they never shift when a sub-brand re-accents:

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

### 3.7 Theming & token contract

- **Light + dark only.** Every Pháros app ships exactly two themes, toggled by the shadcn **`.dark` class** on the root element (not a `[data-theme]` attribute). The former finance-lch `cobol`/terminal theme is **dropped** — a CRT-glow theme contradicts the calm / flatness spine (RFC 0008 Q7).
- **Token contract.** The shared contract is **shadcn-vue vars** + an accent-**independent** status palette (success / warning / error / info). The names are shared; the *values* are themed — a sub-brand is a small theme overriding only the accent (`--primary` / `--accent`), e.g. ERP → navy `#003A70`. QC's burgundy/red (§3.4) lives in that status layer for LIS.

---

## 4. Typography

### 4.1 Fonts

| Role | Font | Loaded from | Fallback |
|---|---|---|---|
| Display / wordmark | **Fraunces** (variable, opsz 9–144) | Google Fonts | Times New Roman, serif |
| UI / body | **Inter** (variable) | Google Fonts | system-ui, sans-serif |
| Data, metrics, labels, table headers | **IBM Plex Mono** | Google Fonts | monospace |

> Three families, shared across the whole family — **no per-app fonts** (type is the strongest cohesion lever, RFC 0008 Q5). Consolidated from four: the second mono (JetBrains Mono) is dropped; IBM Plex Mono now serves both data values and labels.

### 4.2 Font loading (Nuxt 4)

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap'
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
| Data value | 22px | 1.0 | IBM Plex Mono | 500 (tabular-nums) |
| Data value small | 14px | 1.0 | IBM Plex Mono | 400 (tabular-nums) |

### 4.4 Typography rules
- Body text: always left-aligned. Never justified.
- Line height: 1.6× for body, 1.2× for headlines.
- Brand name in running text: always title case "Pháros", never ALL CAPS.
- Sub-brand in running text: `Pháros · Timón` (with the `·` separator).
- Tenant brand name in running text: full form, "Laboratorio Clínico Hematológico", title case.
- Data and numerical values: always IBM Plex Mono with `tabular-nums` — columns must align in tables.
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

> Primary actions and active nav use the **sub-brand accent** (shadcn `--primary`, e.g. ERP = navy `#003A70`) — **not** the burgundy/red mark, which is the shared family constant. Some examples below are QC/LIS surfaces (state badges, CV cards); the patterns generalize across the family.

### 6.1 Primary button
```vue
<button class="bg-primary hover:bg-primary/90 text-primary-foreground font-medium px-6 py-3 rounded-lg transition-colors">
  Aprobar control
</button>
```

### 6.2 Secondary button
```vue
<button class="border border-primary text-primary hover:bg-primary/10 font-medium px-6 py-3 rounded-lg transition-colors">
  Ver detalles
</button>
```

### 6.3 QC state badge (Pháros LIS surface)
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
  <div class="font-['IBM_Plex_Mono'] text-3xl font-medium text-primary tabular-nums">
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
              focus:outline-none focus:ring-2 focus:ring-ring focus:border-primary transition" />
```

### 6.6 Pilot-light status indicator
The signature Pháros UI element — a pulsing dot that shows live system health, in the family-constant red (`--pharos-red`), shared across every sub-brand.

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
- **Focus on the work** — instruments, process, and the people doing it, shown with the same calm respect. The family is a Caregiver at heart; on patient- and staff-facing surfaces (Admisiones, CRM) people belong in frame.
- **No people-in-lab-coats clichés** — show the actual work being done.

---

## 10. Architectural Position

Pháros is the **umbrella brand** for the holding's software family — built by **Interval · The Human Tech Co.** (LCH's in-house software team) and run by the holding's labs (LCH · Biuman). The relationship is:

```
Laboratorio Clínico Hematológico (LCH) — the lab business
   └── Interval · The Human Tech Co. — LCH's in-house software team (the maker)
            │ builds
            ▼
         Pháros — the product family (umbrella)
            ├── Pháros · Timón      ERP          accent: LCH Navy #003A70
            ├── Pháros LIS          clínico (LCH) · deportivo (Biuman)   ← QC surfaces fold in here
            ├── Pháros Admisiones    ← Caja surfaces fold in here
            ├── Pháros CRM
            └── Pháros Archivo      utility · neutral accent · no evocative name

Run by (tenants):  LCH · Biuman   (Biuman = sports-lab sibling in the holding)
nucleus-db — shared infrastructure, never branded
```

- **QC and Caja are not siblings** — they are persona-scoped surfaces *inside* Pháros LIS and Pháros Admisiones (RFC 0004 §2), not nodes in the tree.
- **Pháros Archivo** is a utility tier (shared shell + a neutral family accent, no evocative sub-name).
- **`nucleus-db`** is infrastructure users never see — never branded.
- Only **ERP = `Pháros · Timón`** is name-locked; the other evocative sub-names are open (RFC 0008 Q1). Functional names (ERP / LIS / Admisiones / CRM) stay in RFC 0004 as the architecture vocabulary.

**Shared vs differentiated.** Every sub-brand inherits the shared Pháros foundation unchanged — the type system, the app-shell/layout, spacing/radius/flatness, the mark + wordmark construction, the voice, the semantic-token contract *names*, and the design gates. A sub-brand differentiates on only three things: its **accent value**, its **sub-name + sublabel**, and its **app-icon tint**. Mechanically, a sub-brand is a *theme* of the shared contract.

**Tenant co-branding.** LCH and Biuman are tenants, not parents — a tenant **never prefixes an app name** (it is `Pháros · Timón`, never "LCH Pháros"). Where a tenant must appear (e.g. a login footer), use a small `para [tenant]` / "by [tenant]" credit; the Pháros brand wins on its own screens. (The exact co-brand lockup — peer sizing, placement — is a small open spec.)

---

## 11. Quick Reference Card

```
FAMILY            Pháros — umbrella for the software family (replaces the COBOL LIS)
BUILT BY          Interval · The Human Tech Co. (LCH's in-house team)
SERVES            LCH · Biuman (tenants)

LOGO              Wordmark "Pháros" + red pilot-light dot above the P (shared constant)
WORDMARK FONT     Fraunces (variable serif, 400 weight)
WORDMARK COLOR    #782F40 (burgundy) — never re-tinted per app
PILOT LIGHT       #E4002B (red) — the family constant
SEPARATOR         ·   (Pháros · <Sub-name>)

UI FONT           Inter
DATA + LABEL FONT IBM Plex Mono (tabular-nums for data; uppercase 0.18em for labels)

ERP ACCENT        #003A70 (LCH Navy) + #A0D1CA teal success   [Pháros · Timón]
QC STATE (LIS)    #A0D1CA in control · #FBD872 drift · #E4002B out of control

THEMES            light + dark only (.dark class); cobol dropped
VOICE             Spanish first · technical + warm · never alarmist
DESCRIPTOR        Control de Calidad — the QC/LIS surface (umbrella tagline TBD · RFC 0008)
MANTRA            Vigilamos lo invisible para que la verdad pueda verse.
```

---

*This brand book is the authoritative source for the shared Pháros visual and verbal identity in code. Per-app sub-brands live in `sub-brands/*.md` (first: `sub-brands/erp.md`, `Pháros · Timón`) and only record their accent, sub-name, and icon tint. For strategic and conceptual questions, see `BACKBONE.md`. For the maker (house) brand, see `../interval/INTERVAL-BRAND.md` (esp. §10); the family palette source is `../hematologico/LCH-BRAND.md`.*
