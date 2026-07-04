# Surface — Portal Pacientes

> Per-surface design guidance on the Pháros token contract (`../tokens.css`).
> Patient-facing public results portal. Warm, accessible, clear, empathetic.

**Audiencia:** Pacientes externos (adultos, adultos mayores, padres con hijos) — sin
formación técnica.
**Sub-brand / superficie Pháros:** **Pháros LIS** — portal público de consulta de
resultados (la cara pública del LIS clínico).
**Prioridades:** accesibilidad, legibilidad, calidez humana, simplicidad radical.

> **Accent — Laboratorio (teal), LOCKED.** Pháros LIS hereda el acento **Laboratorio**
> (`.theme-clinico` en `tokens.css`: teal `#1B6B5A` light / `#4CD1B0` dark), aplicado
> añadiendo la clase al `<html>` (RFC 0008 — ACCEPTED 2026-06-17). Todo lo que hay
> abajo se expresa contra los slots semánticos, de modo que el portal hereda el acento
> Clínico sin reescritura; el tema sólo sobreescribe los slots de acento
> (`--primary/--ring/--sidebar-primary` + foregrounds), el resto se hereda.

---

## Colour — sólo tokens del contrato

Esta superficie no define paleta propia: consume el contrato compartido
(`../tokens.css`). No hay `--pp-*`, no hay `var(--color-*)` LCH, no hay hex crudos.

| Rol en el portal | Token (NO inventar valores) |
|---|---|
| Acción primaria / CTA / enlaces | `--primary` / `--primary-foreground` (acento Clínico / teal del sub-brand) |
| Superficie suave de tarjeta / sección | `--card`, `--secondary`, `--accent` (hover suave) |
| Fondo de página | `--background` |
| Texto principal | `--foreground` |
| Texto secundario / helpers / captions | `--muted-foreground` |
| Bordes de inputs y tarjetas | `--border` / `--input` |
| Resultado **Normal / OK** | `--status-success` / `--status-success-bg` |
| Resultado **a revisar** | `--status-warning` / `--status-warning-bg` |
| Resultado **crítico** / peligro / error | `--status-error` (= `--destructive`) / `--status-error-bg` |
| Información / resuelto | `--status-info` / `--status-info-bg` |

**Regla cromática clave (corrige el portal LCH):** el archivo anterior usaba el
**mismo rojo** para los CTAs primarios y para "crítico/peligro". Aquí se separan:

- **Acciones primarias → `--primary`** (el acento del sub-brand, Clínico / teal).
- **Crítico / peligro / destructivo → `--status-error` / `--destructive`.**
- El **rojo** (`--pharos-red` / `--status-error`) queda reservado para **error + el
  pilot-light de marca** — **nunca** es una acción primaria.

### Tailwind v4 — utilidades de uso frecuente
```
bg-background            → fondo de página
bg-card / bg-secondary   → fondos de sección y tarjeta suaves
bg-primary               → botones primarios, CTAs
text-primary             → links, acciones
text-foreground          → encabezados
text-muted-foreground    → texto secundario, helpers
border-border            → bordes de inputs y tarjetas
bg-status-success-bg  text-status-success   → estado "Normal/OK"
bg-status-warning-bg  text-status-warning   → estado "Revisar"
bg-status-error-bg    text-status-error     → estado "Crítico"
```
Sub-brand re-acentúa sólo `--primary/--accent/--ring/--sidebar-primary`; la paleta
de estado (status-success/warning/error/info) **no** se mueve.

---

## Tipografía

```css
/* UI sans (DM Sans) por defecto; display (Fraunces) para hero/encabezados grandes */
font-family: var(--font-sans);   /* DM Sans — system-ui fallback */
/* Hero / display */ font-family: var(--font-display); /* Fraunces */
/* Etiquetas / labels */ font-family: var(--font-mono); /* IBM Plex Mono */
/* Datos (valores de laboratorio / cifras) */ font-family: var(--font-data); /* JetBrains Mono, tabular-nums */
```

| Nivel | Escala |
|---|---|
| Hero | `clamp(2rem, 5vw, 3.5rem)`, `font-display`, `font-weight: 700` |
| H1 | `2rem`, `font-weight: 600` |
| H2 | `1.5rem`, `font-weight: 600` |
| Body | `1rem`, `line-height: 1.8` (mayor espaciado para pacientes) |
| Caption | `0.875rem`, `text-muted-foreground` |
| Valor de laboratorio | `font-data` + `tabular-nums`, `1.5rem`, `font-weight: 500` |

- **Datos / números / cifras → `font-data` (JetBrains Mono) + `tabular-nums`.**
  Las **etiquetas / labels** usan `font-mono` (IBM Plex Mono). Sin Apax.
- **Regla clave:** tamaño mínimo `text-base` (16px). Nunca menos en este portal.

---

## Espaciado y layout

```
Radio de tarjeta:   rounded-xl    /* más amigable para pacientes */
Radio de botón:     rounded-lg    /* = --radius (8px) */
Radio de badge:     rounded-full
Sombra:             shadow-sm  →  hover: shadow-md
Padding de sección: py-16
Padding de tarjeta: p-6 md:p-8
```

---

## Inventario de componentes

Nombres re-cortados a `Pháros LIS` (un tenant nunca antepone su nombre: `Pháros · …`,
no "LCH Pháros"). Los contratos de props/emits se conservan.

### `PharosPortalBusquedaResultados` — Búsqueda de resultados
Props: `documentType: string`, `documentNumber: string`
Emits: `search(doc: { type: string, number: string })`

```vue
<PharosPortalBusquedaResultados @search="handleSearch" />
```

### `PharosPortalResultadoCard` — Tarjeta de resultado individual
Props: `examen: string`, `fecha: string`, `resultado: string | number`,
`unidad?: string`, `estado: 'normal' | 'revisar' | 'critico'`, `referencia?: string`

```vue
<PharosPortalResultadoCard
  examen="Glóbulos Rojos"
  fecha="15/04/2026"
  :resultado="4.8"
  unidad="10^6/μL"
  estado="normal"
  referencia="4.5 – 5.9"
/>
```

Estado visual (paleta de estado, acento-independiente):
```vue
<!-- Normal -->
<span class="bg-status-success-bg text-status-success text-xs font-medium px-3 py-1 rounded-full">Normal</span>
<!-- Revisar -->
<span class="bg-status-warning-bg text-status-warning text-xs font-medium px-3 py-1 rounded-full">Revisar</span>
<!-- Crítico -->
<span class="bg-status-error-bg text-status-error text-xs font-medium px-3 py-1 rounded-full">Crítico</span>
```

### `PharosPortalDescargaBtn` — Botón de descarga PDF
Props: `resultadoId: string`, `loading?: boolean`

```vue
<PharosPortalDescargaBtn resultado-id="123" />
```

### `PharosPortalEmptyState` — Estado vacío / no encontrado
Props: `titulo?: string`, `mensaje?: string`

```vue
<PharosPortalEmptyState
  titulo="No encontramos tu resultado"
  mensaje="Verifica tu número de documento o consulta con nuestro equipo."
/>
```

### `PharosPortalHero` — Banner principal
Props: `title?: string`, `subtitle?: string`

---

## Patrones de código

### Botón primario (CTA) — usa el acento, no el rojo
```vue
<button class="bg-primary hover:bg-primary/90 text-primary-foreground font-medium px-6 py-3 rounded-lg transition-colors duration-200 min-h-[48px]">
  Ver mis resultados
</button>
```

### Botón destructivo / crítico — el ÚNICO botón que usa rojo
```vue
<button class="bg-destructive hover:bg-destructive/90 text-destructive-foreground font-medium px-6 py-3 rounded-lg transition-colors duration-200 min-h-[48px]">
  Eliminar
</button>
```

### Input de búsqueda
```vue
<input
  class="w-full border border-input rounded-lg px-4 py-3 bg-background text-foreground placeholder:text-muted-foreground
         focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring transition text-base"
  placeholder="Número de documento"
  :aria-label="'Número de documento'"
/>
```

### Valor de resultado de laboratorio
```vue
<div class="font-data text-2xl font-medium text-foreground tabular-nums">
  {{ resultado }}
</div>
<div class="font-sans text-sm text-muted-foreground">{{ unidad }}</div>
```

### Tarjeta de resultado
```vue
<div class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
  <!-- contenido -->
</div>
```

---

## Accesibilidad obligatoria
- Todos los inputs con `aria-label` o `<label>` asociado.
- Botones con texto claro — nunca sólo ícono sin `aria-label`.
- Contraste mínimo AA: usar siempre los pares de estado del contrato
  (`--status-warning` sobre `--status-warning-bg`, etc.). **Nunca** texto claro sobre
  el tinte de advertencia (`--status-warning-bg`, amarillo).
- Focus ring visible: `focus:ring-2 focus:ring-ring`.
- `min-h-[48px]` en todos los elementos interactivos táctiles.

---

## Theming (.dark aware)
- Light + dark vía la clase **`.dark`** de shadcn (no `[data-theme]`, no tema CRT).
- No se hardcodean colores: todo resuelve contra los tokens, por lo que el portal
  se invierte correctamente en modo oscuro sin cambios de marcado. Verificar que los
  estados (status-success/warning/error/info) mantienen contraste con sus tintes
  `-bg` tanto en claro como en oscuro.

---

## Tono de los textos en UI (voz de marca)
```
✅ "No encontramos tu resultado. Verifica tu número de documento."
✅ "Tus resultados están listos"
✅ "Descarga tu informe completo"
❌ "Error 404 — Record not found"
❌ "Consulta inválida"
❌ "DESCARGAR RESULTADO"  ← no ALL CAPS
```

---

## Ported from `ds-lch-portal-pacientes`; what changed
- **Acento del sub-brand:** **Clínico (teal), LOCKED** (RFC 0008 — ACCEPTED
  2026-06-17). Pháros LIS hereda `.theme-clinico` (teal `#1B6B5A` light / `#4CD1B0`
  dark); la superficie consume `--primary` y recibe el acento por la clase de tema.
- **CTA ≠ peligro (corregido):** el portal LCH usaba el mismo rojo (`--pp-primary` =
  `--color-brand-red`) para CTAs y para "crítico". Ahora **primario → `--primary`** y
  **crítico/peligro → `--status-error`/`--destructive`**; el rojo queda reservado para
  error + el pilot-light, nunca para una acción primaria.
- **Tokens:** eliminados todos los `--pp-*`, `var(--color-navy)`, `var(--color-brand-red)`,
  `var(--color-*)` LCH y hex crudos. Reemplazados por tokens semánticos shadcn +
  paleta de estado acento-independiente
  (`--status-success/--status-warning/--status-error/--status-info`, cada uno con su
  tinte `-bg`). Mapeo: normal → `--status-success`, revisar → `--status-warning`,
  crítico → `--status-error`, info/resuelto → `--status-info`.
- **Tipografía:** valores de laboratorio usan `font-data` (**JetBrains Mono**) +
  `tabular-nums` para cifras; las etiquetas usan `font-mono` (**IBM Plex Mono**). La
  fuente de marca Apax (`--font-brand`) se sustituye por `font-display` (**Fraunces**)
  para hero y `font-sans` (**DM Sans**) para UI. Sin Apax.
- **Componentes:** prefijo `Lch…` → `PharosPortal…` (tenant no antepone su nombre);
  props/emits y patrones UX (búsqueda, tarjeta de resultado, descarga PDF, empty
  state, hero) se conservan.
- **Theming:** ahora `.dark`-aware vía la clase shadcn; sin tema CRT/`cobol`, sin
  `[data-theme]`.
