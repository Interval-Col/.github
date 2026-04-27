---
description: "Use when creating components or pages for LCH Laboratorio — internal lab operations system (biuman-reports, lab-qc). Data-dense, technical, dark surfaces, precision-first design. Audience: lab technicians and pathologists."
---
# Design System — LCH Laboratorio

**Audiencia:** Técnicos de laboratorio, patólogos, bacteriólogos  
**Aplicaciones:** `biuman-reports`, `lab-qc`  
**Prioridades:** densidad de información, velocidad de lectura, precisión, dark/light ambivalent

---

## Paleta de colores — Laboratorio

```css
/* Sección Laboratorio */
--lab-primary:       var(--color-navy);         /* #003A70 — superficies principales */
--lab-secondary:     var(--color-blue);         /* #326295 — acciones secundarias */
--lab-accent:        var(--color-brand-red);    /* #E4002B — alertas críticas */
--lab-bg:            #F4F7FA;                   /* fondo de app */
--lab-surface:       #FFFFFF;                   /* superficies de tarjeta */
--lab-surface-dark:  var(--color-navy);         /* sidebars, headers */
--lab-text:          var(--color-text-primary); /* #000000 */
--lab-text-muted:    var(--color-text-secondary);
--lab-text-on-dark:  var(--color-white);        /* texto sobre navy */
--lab-border:        var(--color-border);       /* #C8C9C7 */
--lab-success:       var(--color-teal);         /* #A0D1CA — resultado normal */
--lab-warning:       var(--color-yellow);       /* #FBD872 — resultado fuera de rango */
--lab-critical:      var(--color-brand-red);    /* #E4002B — resultado crítico */
--lab-pending:       var(--color-brand-lilac);  /* #D986BA — en proceso */
```

### Tailwind v4 — Clases frecuentes
```
bg-lch-navy         → sidebar, header, superficies dark
text-white          → texto sobre navy
bg-lch-blue         → acciones secundarias, tabs activos
bg-lch-red          → alertas críticas, botón de urgencia
bg-[#F4F7FA]        → fondo de aplicación (layout bg)
text-lch-navy       → títulos sobre fondo claro
font-['JetBrains_Mono'] → todos los valores numéricos de laboratorio
tabular-nums        → alineación de cifras en tablas
```

---

## Tipografía — Laboratorio

```css
/* Valores y resultados: monoespaciado para tabular-nums */
--font-data: 'JetBrains Mono', 'IBM Plex Mono', monospace;

/* Etiquetas de columnas y encabezados de tabla */
--font-label: 'IBM Plex Mono', monospace;

/* Todo lo demás */
--font-brand: 'Apax', 'Inter', system-ui, sans-serif;

/* Tamaños en contexto de laboratorio */
/* Valor resultado grande */ font-size: 1.5rem — 2rem; font-weight: 500;
/* Valor en tabla */         font-size: 0.9rem; tabular-nums;
/* Rango de referencia */    font-size: 0.8rem; color: var(--lab-text-muted);
/* Etiqueta de examen */     font-size: 0.875rem; font-weight: 500; letter-spacing: 0.025em;
```

---

## Espaciado y layout

```
--lab-radius-card:   rounded-lg    /* 8px — más técnico/formal */
--lab-radius-badge:  rounded-full
--lab-shadow:        shadow-sm
--lab-sidebar-w:     256px          /* sidebar fijo */
--lab-table-row-h:   48px           /* altura mínima de fila de tabla */
--lab-card-p:        p-4 md:p-5
```

**Layout típico:** Sidebar navy fijo + área de contenido con header

---

## Componentes disponibles

### `LchLaboratorioResultTable` — Tabla de resultados
Props: `results: LabResult[]`, `showRanges?: boolean`, `highlightCritical?: boolean`

```vue
<LchLaboratorioResultTable
  :results="hemogramaResults"
  :show-ranges="true"
  :highlight-critical="true"
/>
```

Estructura de `LabResult`:
```ts
interface LabResult {
  examen: string
  valor: number | string
  unidad: string
  min?: number
  max?: number
  estado: 'normal' | 'bajo' | 'alto' | 'critico'
}
```

### `LchLaboratorioEstadoBadge` — Estado de muestra/examen
Props: `estado: 'pendiente' | 'procesando' | 'listo' | 'critico' | 'rechazado'`

```vue
<LchLaboratorioEstadoBadge estado="critico" />
<LchLaboratorioEstadoBadge estado="listo" />
<LchLaboratorioEstadoBadge estado="pendiente" />
```

Estado → colores:
```vue
<!-- listo → teal -->
<span class="bg-lch-teal/30 text-lch-navy px-3 py-1 rounded-full text-xs font-medium">Listo</span>
<!-- critico → rojo -->
<span class="bg-lch-red/10 text-lch-red px-3 py-1 rounded-full text-xs font-medium">Crítico</span>
<!-- pendiente → lilac -->
<span class="bg-lch-lilac/20 text-lch-navy px-3 py-1 rounded-full text-xs font-medium">Pendiente</span>
<!-- rechazado → naranja -->
<span class="bg-lch-orange/20 text-lch-black px-3 py-1 rounded-full text-xs font-medium">Rechazado</span>
```

### `LchLaboratorioMetricCard` — KPI de laboratorio
Props: `label: string`, `valor: string | number`, `unidad?: string`, `delta?: number`

```vue
<LchLaboratorioMetricCard label="Muestras hoy" :valor="142" />
<LchLaboratorioMetricCard label="Tiempo promedio" valor="23" unidad="min" :delta="-5" />
```

### `LchLaboratorioSidebar` — Navegación interna
Props: `items: NavItem[]`, `activeRoute: string`

### `LchLaboratorioFiltros` — Panel de filtros
Props: `filters: FilterConfig[]`

---

## Patrones de código

### Valor numérico de resultado
```vue
<div class="font-['JetBrains_Mono'] text-xl font-medium tabular-nums"
     :class="{ 'text-lch-red': resultado.estado === 'critico', 'text-lch-navy': resultado.estado === 'normal' }">
  {{ resultado.valor }}
</div>
<div class="font-['IBM_Plex_Mono'] text-xs text-lch-gray-dark uppercase tracking-wide">
  {{ resultado.unidad }}
</div>
```

### Fila de tabla (dense layout)
```vue
<tr class="border-b border-lch-gray-mid hover:bg-lch-blush/20 transition-colors">
  <td class="px-4 py-3 text-sm font-medium text-lch-navy">{{ examen }}</td>
  <td class="px-4 py-3 font-['JetBrains_Mono'] text-sm tabular-nums">{{ valor }}</td>
  <td class="px-4 py-3 text-xs text-lch-gray-dark">{{ unidad }}</td>
  <td class="px-4 py-3 text-xs text-lch-gray-dark">{{ min }} – {{ max }}</td>
  <td class="px-4 py-3"><LchLaboratorioEstadoBadge :estado="estado" /></td>
</tr>
```

### Header/Sidebar dark (navy)
```vue
<aside class="w-64 bg-lch-navy text-white min-h-screen flex flex-col">
  <div class="p-6">
    <LchLogo theme="dark" size="navbar" />
  </div>
  <!-- nav items -->
</aside>
```

### Alerta clínica crítica
```vue
<div class="border-l-4 border-lch-red bg-lch-red/5 px-4 py-3 rounded-r-lg">
  <p class="text-lch-red font-medium text-sm">Valor crítico — Requiere atención inmediata</p>
  <p class="text-lch-black text-sm mt-1">{{ mensaje }}</p>
</div>
```

---

## Rutas de destino
```
components/Laboratorio/LchLaboratorioResultTable.vue
components/Laboratorio/LchLaboratorioEstadoBadge.vue
components/Laboratorio/LchLaboratorioMetricCard.vue
components/Laboratorio/LchLaboratorioSidebar.vue
pages/laboratorio/resultados.vue
pages/laboratorio/muestras.vue
```
