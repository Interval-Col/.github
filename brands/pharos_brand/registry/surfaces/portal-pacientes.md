# Surface — Portal Pacientes

> Per-surface design guidance on the Pháros token contract (`../tokens.css`).
> Patient-facing public results portal. Warm, accessible, clear, empathetic.

**Audiencia:** Pacientes externos (adultos, adultos mayores, padres con hijos) — sin
formación técnica.
**Sub-brand / superficie Pháros:** **Pháros LIS** — portal público de consulta de
resultados (la cara pública del LIS clínico).
**Prioridades:** accesibilidad, legibilidad, calidez humana, simplicidad radical.

> **Accent — TBD.** Pháros LIS no es ERP · Timón, así que su acento todavía NO está
> fijado (RFC 0008 Q1/Q6 — @SKuger01 / brand playground). Use `--primary` de forma
> genérica; **nunca invente un acento concreto** para esta superficie. Todo lo que
> hay abajo se expresa contra los slots semánticos, de modo que cuando se cierre el
> acento de Pháros LIS la superficie lo herede sin reescritura.

---

## Colour — sólo tokens del contrato

Esta superficie no define paleta propia: consume el contrato compartido
(`../tokens.css`). No hay `--pp-*`, no hay `var(--color-*)` LCH, no hay hex crudos.

| Rol en el portal | Token (NO inventar valores) |
|---|---|
| Acción primaria / CTA / enlaces | `--primary` / `--primary-foreground` (acento TBD del sub-brand) |
| Superficie suave de tarjeta / sección | `--card`, `--secondary`, `--accent` (hover suave) |
| Fondo de página | `--background` |
| Texto principal | `--foreground` |
| Texto secundario / helpers / captions | `--muted-foreground` |
| Bordes de inputs y tarjetas | `--border` / `--input` |
| Resultado **Normal / OK** | `--success` / `--success-foreground` |
| Resultado **a revisar** | `--warning` / `--warning-foreground` |
| Resultado **crítico** / peligro / error | `--error` (= `--destructive`) / `--error-foreground` |
| Información / resuelto | `--info` / `--info-foreground` |

**Regla cromática clave (corrige el portal LCH):** el archivo anterior usaba el
**mismo rojo** para los CTAs primarios y para "crítico/peligro". Aquí se separan:

- **Acciones primarias → `--primary`** (el acento del sub-brand, TBD).
- **Crítico / peligro / destructivo → `--error` / `--destructive`.**
- El **rojo** (`--pharos-red` / `--error`) queda reservado para **error + el
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
bg-success/30  text-success-foreground   → estado "Normal/OK"
bg-warning/40  text-warning-foreground   → estado "Revisar"
bg-error/10    text-error                → estado "Crítico"
```
Sub-brand re-acentúa sólo `--primary/--accent/--ring/--sidebar-primary`; la paleta
de estado (success/warning/error/info) **no** se mueve.

---

## Tipografía

```css
/* UI sans (Inter) por defecto; display (Fraunces) para hero/encabezados grandes */
font-family: var(--font-sans);   /* Inter — system-ui fallback */
/* Hero / display */ font-family: var(--font-display); /* Fraunces */
/* Datos (valores de laboratorio) */ font-family: var(--font-mono); /* IBM Plex Mono */
```

| Nivel | Escala |
|---|---|
| Hero | `clamp(2rem, 5vw, 3.5rem)`, `font-display`, `font-weight: 700` |
| H1 | `2rem`, `font-weight: 600` |
| H2 | `1.5rem`, `font-weight: 600` |
| Body | `1rem`, `line-height: 1.8` (mayor espaciado para pacientes) |
| Caption | `0.875rem`, `text-muted-foreground` |
| Valor de laboratorio | `font-mono` + `tabular-nums`, `1.5rem`, `font-weight: 500` |

- **Datos / números → `font-mono` (IBM Plex Mono) + `tabular-nums`.** Sin JetBrains
  Mono, sin Apax.
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
<span class="bg-success/30 text-success-foreground text-xs font-medium px-3 py-1 rounded-full">Normal</span>
<!-- Revisar -->
<span class="bg-warning/40 text-warning-foreground text-xs font-medium px-3 py-1 rounded-full">Revisar</span>
<!-- Crítico -->
<span class="bg-error/10 text-error text-xs font-medium px-3 py-1 rounded-full">Crítico</span>
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
<div class="font-mono text-2xl font-medium text-foreground tabular-nums">
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
- Contraste mínimo AA: usar siempre los pares `*-foreground` del contrato
  (`--warning-foreground` sobre `--warning`, etc.). **Nunca** texto claro sobre
  `--warning` (amarillo).
- Focus ring visible: `focus:ring-2 focus:ring-ring`.
- `min-h-[48px]` en todos los elementos interactivos táctiles.

---

## Theming (.dark aware)
- Light + dark vía la clase **`.dark`** de shadcn (no `[data-theme]`, no tema CRT).
- No se hardcodean colores: todo resuelve contra los tokens, por lo que el portal
  se invierte correctamente en modo oscuro sin cambios de marcado. Verificar que los
  estados (success/warning/error/info) mantienen contraste con sus `*-foreground`
  tanto en claro como en oscuro.

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
- **Acento del sub-brand:** marcado **TBD** (RFC 0008 Q1/Q6, @SKuger01). Pháros LIS
  no es ERP · Timón; no se inventa acento — se usa `--primary` genérico.
- **CTA ≠ peligro (corregido):** el portal LCH usaba el mismo rojo (`--pp-primary` =
  `--color-brand-red`) para CTAs y para "crítico". Ahora **primario → `--primary`** y
  **crítico/peligro → `--error`/`--destructive`**; el rojo queda reservado para
  error + el pilot-light, nunca para una acción primaria.
- **Tokens:** eliminados todos los `--pp-*`, `var(--color-navy)`, `var(--color-brand-red)`,
  `var(--color-*)` LCH y hex crudos. Reemplazados por tokens semánticos shadcn +
  paleta de estado acento-independiente (`--success/--warning/--error/--info`).
  Mapeo: normal → `--success`, revisar → `--warning`, crítico → `--error`,
  info/resuelto → `--info`.
- **Tipografía:** valores de laboratorio pasan de `font-['JetBrains_Mono']` a
  `font-mono` (**IBM Plex Mono**) + `tabular-nums`. La fuente de marca Apax
  (`--font-brand`) se sustituye por `font-display` (**Fraunces**) para hero y
  `font-sans` (**Inter**) para UI. Sin JetBrains Mono, sin Apax.
- **Componentes:** prefijo `Lch…` → `PharosPortal…` (tenant no antepone su nombre);
  props/emits y patrones UX (búsqueda, tarjeta de resultado, descarga PDF, empty
  state, hero) se conservan.
- **Theming:** ahora `.dark`-aware vía la clase shadcn; sin tema CRT/`cobol`, sin
  `[data-theme]`.
