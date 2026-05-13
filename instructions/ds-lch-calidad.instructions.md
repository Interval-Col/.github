---
description: "Use when creating components or pages for LCH Calidad — the lab-qc quality control application. Scientific precision, control charts, deviation indicators, teal-accented. Audience: quality control team."
---
# Design System — LCH Calidad (lab-qc)

**Audiencia:** Equipo de control de calidad, coordinador de calidad  
**Aplicación:** `lab-qc`  
**Prioridades:** visualización de datos de control, gráficos Levey-Jennings, indicadores de desvío, trazabilidad

---

## Paleta de colores — Calidad

```css
/* Sección Calidad */
--qc-primary:       var(--color-navy);         /* #003A70 — superficies principales */
--qc-secondary:     var(--color-teal);         /* #A0D1CA — acento dominante en QC */
--qc-accent:        var(--color-blue);         /* #326295 — acciones interactivas */
--qc-in-control:    var(--color-teal);         /* #A0D1CA — dentro de control */
--qc-warning:       var(--color-yellow);       /* #FBD872 — regla de advertencia (1-2s) */
--qc-out-control:   var(--color-brand-red);    /* #E4002B — fuera de control */
--qc-bg:            #F0F7F7;                   /* fondo levemente teal */
--qc-surface:       #FFFFFF;
--qc-text:          var(--color-text-primary);
--qc-text-muted:    var(--color-text-secondary);
--qc-border:        #C5DCDC;                   /* borde teal-suave */
```

### Tailwind v4 — Clases frecuentes
```
bg-lch-teal/20         → fondos de sección "en control"
border-lch-teal        → bordes de tarjetas QC
text-lch-teal          → etiquetas de estado "en control"
bg-lch-yellow/40       → fondo de advertencia QC
text-lch-red           → fuera de control, alerta
bg-lch-navy            → headers, sidebar
font-['JetBrains_Mono'] → valores de media, SD, CV
tabular-nums           → siempre en tablas de QC
```

---

## Tipografía — Calidad

```css
/* Valores estadísticos (media, SD, CV, Z-score) */
font-family: 'JetBrains Mono'; font-size: 1.125rem; font-weight: 500; tabular-nums;

/* Etiquetas de reglas QC (1-2s, 1-3s, R-4s...) */
font-family: 'IBM Plex Mono'; font-size: 0.75rem; font-weight: 500;

/* Títulos de analito/instrumento */
font-family: var(--font-brand); font-size: 1rem; font-weight: 600;
```

---

## Componentes disponibles

### `LchCalidadEstadoIndicator` — Indicador de estado de control
Props: `estado: 'en-control' | 'advertencia' | 'fuera-control'`, `regla?: string`

```vue
<LchCalidadEstadoIndicator estado="en-control" />
<LchCalidadEstadoIndicator estado="advertencia" regla="1-2s" />
<LchCalidadEstadoIndicator estado="fuera-control" regla="1-3s" />
```

```vue
<!-- En control → teal -->
<div class="flex items-center gap-2 bg-lch-teal/20 border border-lch-teal px-3 py-2 rounded-lg">
  <span class="w-2.5 h-2.5 rounded-full bg-lch-teal"></span>
  <span class="text-lch-navy text-sm font-medium">En control</span>
</div>
<!-- Advertencia → amarillo + regla -->
<div class="flex items-center gap-2 bg-lch-yellow/30 border border-lch-yellow px-3 py-2 rounded-lg">
  <span class="w-2.5 h-2.5 rounded-full bg-lch-yellow"></span>
  <span class="text-lch-black text-sm font-medium">Advertencia</span>
  <span class="font-['IBM_Plex_Mono'] text-xs text-lch-gray-dark ml-1">{{ regla }}</span>
</div>
<!-- Fuera de control → rojo -->
<div class="flex items-center gap-2 bg-lch-red/10 border border-lch-red px-3 py-2 rounded-lg">
  <span class="w-2.5 h-2.5 rounded-full bg-lch-red animate-pulse"></span>
  <span class="text-lch-red text-sm font-medium">Fuera de control</span>
  <span class="font-['IBM_Plex_Mono'] text-xs text-lch-red ml-1">{{ regla }}</span>
</div>
```

### `LchCalidadEstadisticasCard` — Estadísticas del lote QC
Props: `analito: string`, `nivel: string`, `media: number`, `sd: number`, `cv: number`, `n: number`

```vue
<LchCalidadEstadisticasCard
  analito="Glucosa"
  nivel="Nivel 1"
  :media="95.4"
  :sd="2.1"
  :cv="2.2"
  :n="30"
/>
```

```vue
<!-- Patrón interno -->
<div class="grid grid-cols-4 gap-4 p-4">
  <div v-for="stat in [{ label: 'media (x̄)', value: media }, { label: 'SD (σ)', value: sd }, { label: 'CV (%)', value: cv }, { label: 'N', value: n }]">
    <p class="font-['IBM_Plex_Mono'] text-xs text-lch-gray-dark uppercase tracking-wide">{{ stat.label }}</p>
    <p class="font-['JetBrains_Mono'] text-xl font-medium text-lch-navy tabular-nums">{{ stat.value }}</p>
  </div>
</div>
```

### `LchCalidadReglaTag` — Etiqueta de regla Westgard
Props: `regla: string`, `violada?: boolean`

```vue
<LchCalidadReglaTag regla="1-2s" />
<LchCalidadReglaTag regla="1-3s" :violada="true" />
<LchCalidadReglaTag regla="R-4s" :violada="true" />
```

```vue
<span class="font-['IBM_Plex_Mono'] text-xs px-2 py-0.5 rounded"
      :class="violada ? 'bg-lch-red/10 text-lch-red font-semibold' : 'bg-lch-gray-mid/30 text-lch-gray-dark'">
  {{ regla }}
</span>
```

### `LchCalidadRegistroTable` — Tabla de registro de controles
Props: `registros: QcRegistro[]`

```ts
interface QcRegistro {
  fecha: string
  valor: number
  z: number          // z-score
  operador: string
  instrumento: string
  reglaViolada?: string
}
```

### `LchCalidadResumenDashboard` — Resumen de estado de todos los analitos
Muestra grid de analitos con su estado de control actual.

---

## Patrones de código

### Fila de tabla QC con resaltado
```vue
<tr class="border-b border-lch-gray-mid"
    :class="{
      'bg-lch-red/5':    registro.reglaViolada,
      'bg-lch-yellow/10': Math.abs(registro.z) > 2 && !registro.reglaViolada,
      'hover:bg-lch-blush/20': !registro.reglaViolada
    }">
  <td class="px-4 py-3 font-['JetBrains_Mono'] text-sm tabular-nums">{{ registro.valor }}</td>
  <td class="px-4 py-3 font-['JetBrains_Mono'] text-sm tabular-nums"
      :class="{ 'text-lch-red font-semibold': Math.abs(registro.z) > 3, 'text-lch-navy': Math.abs(registro.z) <= 3 }">
    {{ registro.z.toFixed(2) }}
  </td>
  <td class="px-4 py-3">
    <LchCalidadReglaTag v-if="registro.reglaViolada" :regla="registro.reglaViolada" :violada="true" />
  </td>
</tr>
```

---

## Rutas de destino
```
components/Calidad/LchCalidadEstadoIndicator.vue
components/Calidad/LchCalidadEstadisticasCard.vue
components/Calidad/LchCalidadReglaTag.vue
components/Calidad/LchCalidadRegistroTable.vue
components/Calidad/LchCalidadResumenDashboard.vue
pages/calidad/dashboard.vue
pages/calidad/registros/[analito].vue
```
