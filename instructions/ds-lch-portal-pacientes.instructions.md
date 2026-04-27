---
description: "Use when creating components or pages for LCH Portal Pacientes — the public-facing patient results portal. Warm, accessible, clear, empathetic design. Audience: patients with no technical background."
---
# Design System — LCH Portal Pacientes

**Audiencia:** Pacientes externos (adultos, adultos mayores, padres con hijos)  
**Aplicación:** Portal público de consulta de resultados `lch.co`  
**Prioridades:** accesibilidad, legibilidad, calidez humana, simplicidad radical

---

## Paleta de colores — Portal Pacientes

```css
/* Sección Portal Pacientes */
--pp-primary:       var(--color-brand-red);    /* #E4002B — CTAs, enlaces */
--pp-primary-hover: var(--color-brand-red-dark); /* #A6192E — hover */
--pp-surface:       var(--color-blush);        /* #F4CDD4 — fondos suaves de tarjeta */
--pp-bg:            var(--color-bg-page);      /* #FFFFFF */
--pp-text:          var(--color-text-primary); /* #000000 */
--pp-text-muted:    var(--color-text-secondary);/* #888B8D */
--pp-border:        var(--color-border);       /* #C8C9C7 */
--pp-success:       var(--color-teal);         /* #A0D1CA — resultados normales */
--pp-warning:       var(--color-yellow);       /* #FBD872 — resultados a revisar */
--pp-danger:        var(--color-brand-red);    /* #E4002B — resultados críticos */
--pp-accent:        var(--color-brand-lilac);  /* #D986BA — detalles suaves */
```

### Tailwind v4 — Clases de uso frecuente
```
bg-lch-blush        → fondos de sección suaves
bg-lch-red          → botones primarios, CTAs
text-lch-red        → links, acciones
text-lch-navy       → encabezados importantes
text-lch-gray-dark  → texto secundario, helpers
border-lch-gray-mid → bordes de inputs y tarjetas
bg-lch-teal/30      → estado "Normal/OK"
bg-lch-yellow/40    → estado "Revisar"
bg-lch-red/10       → estado "Crítico"
```

---

## Tipografía — Portal Pacientes

```css
font-family: var(--font-brand);  /* Apax → fallback: Inter, DM Sans */

/* Escalas recomendadas */
/* Hero */       font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 700;
/* H1 */         font-size: 2rem; font-weight: 600;
/* H2 */         font-size: 1.5rem; font-weight: 600;
/* Body */       font-size: 1rem; line-height: 1.8;  /* mayor espaciado para pacientes */
/* Caption */    font-size: 0.875rem; color: var(--pp-text-muted);
/* Valores lab */ font-family: var(--font-data); font-size: 1.5rem; font-weight: 500;
```

**Regla clave:** Tamaños de fuente mínimo `text-base` (16px). Nunca menos para este portal.

---

## Espaciado y layout

```
--pp-radius-card:   rounded-xl    /* 12px — más amigable para pacientes */
--pp-radius-btn:    rounded-lg    /* 8px */
--pp-radius-badge:  rounded-full
--pp-shadow:        shadow-sm
--pp-shadow-hover:  shadow-md
--pp-section-py:    py-16
--pp-card-p:        p-6 md:p-8
```

---

## Componentes disponibles

### `LchPortalBusquedaResultados` — Búsqueda de resultados
Props: `documentType: string`, `documentNumber: string`  
Emits: `search(doc: { type: string, number: string })`

```vue
<LchPortalBusquedaResultados @search="handleSearch" />
```

### `LchPortalResultadoCard` — Tarjeta de resultado individual
Props: `examen: string`, `fecha: string`, `resultado: string | number`, `unidad?: string`, `estado: 'normal' | 'revisar' | 'critico'`, `referencia?: string`

```vue
<LchPortalResultadoCard
  examen="Glóbulos Rojos"
  fecha="15/04/2026"
  :resultado="4.8"
  unidad="10^6/μL"
  estado="normal"
  referencia="4.5 – 5.9"
/>
```

Estado visual:
```vue
<!-- Normal: teal suave -->
<span class="bg-lch-teal/30 text-lch-navy text-xs font-medium px-3 py-1 rounded-full">Normal</span>
<!-- Revisar: amarillo -->
<span class="bg-lch-yellow/40 text-lch-black text-xs font-medium px-3 py-1 rounded-full">Revisar</span>
<!-- Crítico: rojo suave -->
<span class="bg-lch-red/10 text-lch-red text-xs font-medium px-3 py-1 rounded-full">Crítico</span>
```

### `LchPortalDescargaBtn` — Botón de descarga PDF
Props: `resultadoId: string`, `loading?: boolean`

```vue
<LchPortalDescargaBtn resultado-id="123" />
```

### `LchPortalEmptyState` — Estado vacío / no encontrado
Props: `titulo?: string`, `mensaje?: string`

```vue
<LchPortalEmptyState
  titulo="No encontramos tu resultado"
  mensaje="Verifica tu número de documento o consulta con nuestro equipo."
/>
```

### `LchPortalHero` — Banner principal
Props: `title?: string`, `subtitle?: string`

---

## Patrones de código

### Botón primario (CTA)
```vue
<button class="bg-lch-red hover:bg-lch-red-dark text-white font-medium px-6 py-3 rounded-lg transition-colors duration-200 min-h-[48px]">
  Ver mis resultados
</button>
```

### Input de búsqueda
```vue
<input
  class="w-full border border-lch-gray-mid rounded-lg px-4 py-3 text-lch-black placeholder-lch-gray-dark
         focus:outline-none focus:ring-2 focus:ring-lch-red focus:border-lch-red transition text-base"
  placeholder="Número de documento"
  :aria-label="'Número de documento'"
/>
```

### Valor de resultado de laboratorio
```vue
<div class="font-['JetBrains_Mono'] text-2xl font-medium text-lch-navy tabular-nums">
  {{ resultado }}
</div>
<div class="font-sans text-sm text-lch-gray-dark">{{ unidad }}</div>
```

### Tarjeta de resultado
```vue
<div class="bg-white border border-lch-gray-mid rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
  <!-- contenido -->
</div>
```

---

## Accesibilidad obligatoria
- Todos los inputs con `aria-label` o `<label>` asociado
- Botones con texto claro — nunca solo ícono sin `aria-label`
- Contraste mínimo AA: blanco sobre `--lch-red` ✅, negro sobre amarillo ✅, **nunca** blanco sobre amarillo ❌
- Focus ring visible: `focus:ring-2 focus:ring-lch-red`
- `min-h-[48px]` en todos los elementos interactivos táctiles

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
