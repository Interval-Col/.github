---
description: "Use when creating components or pages for LCH Finanzas — the finance-lch application. Professional, precise, data-heavy. Audience: administrative and financial team."
---
# Design System — LCH Finanzas

**Audiencia:** Equipo administrativo y financiero  
**Aplicación:** `finance-lch`  
**Prioridades:** precisión numérica, densidad de datos, tablas, KPIs, exportación

---

## Paleta de colores — Finanzas

```css
/* Sección Finanzas */
--fin-primary:       var(--color-navy);         /* #003A70 — superficies, headers */
--fin-secondary:     var(--color-blue);         /* #326295 — acciones secundarias */
--fin-positive:      #00843D;                   /* verde — ingresos, positivos */
--fin-negative:      var(--color-brand-red);    /* #E4002B — gastos, negativos */
--fin-neutral:       var(--color-gray-dark);    /* #888B8D */
--fin-accent:        var(--color-yellow);       /* #FBD872 — alertas, pendientes */
--fin-bg:            #F4F7FA;
--fin-surface:       #FFFFFF;
--fin-text:          var(--color-text-primary);
--fin-text-muted:    var(--color-text-secondary);
--fin-border:        var(--color-border);
```

### Tailwind v4 — Clases frecuentes
```
font-['JetBrains_Mono']   → TODOS los valores monetarios y cifras
tabular-nums               → SIEMPRE en columnas numéricas
text-[#00843D]             → valores positivos/ingresos
text-lch-red               → valores negativos/gastos
bg-lch-yellow/40           → alertas de pendientes
bg-lch-navy                → headers, sidebar, encabezados de tabla
text-white                 → texto sobre navy
```

---

## Tipografía — Finanzas

**Regla fundamental:** Todos los valores monetarios usan `font-['JetBrains_Mono']` con `tabular-nums`. **Sin excepciones.**

```css
/* Montos grandes (KPI) */  font-size: 2rem; font-weight: 600; letter-spacing: -0.02em;
/* Celdas de tabla */        font-size: 0.875rem; font-weight: 400;
/* Encabezados de columna */ font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;
/* Etiquetas */              font-family: 'IBM Plex Mono'; font-size: 0.75rem;
```

---

## Formato de valores monetarios

```ts
// Siempre formatear con Intl.NumberFormat
const formatCurrency = (amount: number, currency = 'COP') =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency }).format(amount)

// Fechas: DD/MM/YYYY para display
const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('es-CO', { day:'2-digit', month:'2-digit', year:'numeric' })
```

---

## Componentes disponibles

### `LchFinanzasKpiCard` — Indicador financiero principal
Props: `label: string`, `amount: number`, `currency?: string`, `trend?: 'up' | 'down' | 'flat'`, `delta?: number`, `periodo?: string`

```vue
<LchFinanzasKpiCard
  label="Ingresos del mes"
  :amount="48500000"
  currency="COP"
  trend="up"
  :delta="12.5"
  periodo="Abril 2026"
/>
```

```vue
<!-- Patrón interno de KpiCard -->
<div class="bg-white border border-lch-gray-mid rounded-lg p-5 shadow-sm">
  <p class="font-['IBM_Plex_Mono'] text-xs text-lch-gray-dark uppercase tracking-wide">{{ label }}</p>
  <p class="font-['JetBrains_Mono'] text-3xl font-semibold text-lch-navy tabular-nums mt-2">
    {{ formatCurrency(amount) }}
  </p>
  <div class="flex items-center gap-1 mt-2">
    <Icon :name="trend === 'up' ? 'arrow-up' : 'arrow-down'"
          class="w-4 h-4"
          :class="{ 'text-[#00843D]': trend === 'up', 'text-lch-red': trend === 'down' }" />
    <span class="font-['JetBrains_Mono'] text-sm"
          :class="{ 'text-[#00843D]': trend === 'up', 'text-lch-red': trend === 'down' }">
      {{ delta }}%
    </span>
  </div>
</div>
```

### `LchFinanzasDataTable` — Tabla financiera
Props: `columns: TableColumn[]`, `data: Record<string, any>[]`, `totals?: Record<string, number>`, `loading?: boolean`

```ts
interface TableColumn {
  key: string
  label: string
  type: 'text' | 'currency' | 'date' | 'status' | 'badge'
  align?: 'left' | 'right' | 'center'
}
```

```vue
<LchFinanzasDataTable
  :columns="[
    { key: 'fecha', label: 'Fecha', type: 'date' },
    { key: 'concepto', label: 'Concepto', type: 'text' },
    { key: 'monto', label: 'Monto', type: 'currency', align: 'right' },
    { key: 'estado', label: 'Estado', type: 'badge' }
  ]"
  :data="facturas"
  :totals="{ monto: totalMes }"
/>
```

### `LchFinanzasEstadoBadge` — Estado de transacción
Props: `estado: 'pagado' | 'pendiente' | 'vencido' | 'anulado'`

```vue
<!-- pagado → teal -->
<span class="bg-lch-teal/30 text-lch-navy px-3 py-1 rounded-full text-xs font-medium">Pagado</span>
<!-- pendiente → amarillo -->
<span class="bg-lch-yellow/40 text-lch-black px-3 py-1 rounded-full text-xs font-medium">Pendiente</span>
<!-- vencido → rojo -->
<span class="bg-lch-red/10 text-lch-red px-3 py-1 rounded-full text-xs font-medium">Vencido</span>
<!-- anulado → gray -->
<span class="bg-lch-gray-mid/40 text-lch-gray-dark px-3 py-1 rounded-full text-xs font-medium">Anulado</span>
```

### `LchFinanzasCurrencyInput` — Input de monto
Props: `currency?: string`, `min?: number`, `max?: number`, `label?: string`

```vue
<LchFinanzasCurrencyInput currency="COP" :min="0" label="Monto de factura" />
```

### `LchFinanzasExportBtn` — Botón de exportación
Props: `format: 'pdf' | 'excel' | 'csv'`, `loading?: boolean`

---

## Patrones de código

### Encabezado de tabla financiera
```vue
<thead class="bg-lch-navy text-white">
  <tr>
    <th class="px-4 py-3 text-left font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide">
      Concepto
    </th>
    <th class="px-4 py-3 text-right font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide">
      Monto (COP)
    </th>
  </tr>
</thead>
```

### Celda de monto positivo/negativo
```vue
<td class="px-4 py-3 text-right font-['JetBrains_Mono'] text-sm tabular-nums"
    :class="{ 'text-[#00843D]': amount > 0, 'text-lch-red': amount < 0 }">
  {{ formatCurrency(amount) }}
</td>
```

### Fila de totales
```vue
<tfoot class="border-t-2 border-lch-navy bg-lch-blush/30">
  <tr>
    <td class="px-4 py-3 font-semibold text-lch-navy">Total</td>
    <td class="px-4 py-3 text-right font-['JetBrains_Mono'] font-semibold text-lch-navy tabular-nums">
      {{ formatCurrency(total) }}
    </td>
  </tr>
</tfoot>
```

---

## Rutas de destino
```
components/Finanzas/LchFinanzasKpiCard.vue
components/Finanzas/LchFinanzasDataTable.vue
components/Finanzas/LchFinanzasEstadoBadge.vue
components/Finanzas/LchFinanzasCurrencyInput.vue
components/Finanzas/LchFinanzasExportBtn.vue
pages/finanzas/dashboard.vue
pages/finanzas/facturas.vue
pages/finanzas/reportes.vue
```
