# Pháros — surface guidance: Laboratorio

**Surface family:** Pháros LIS — superficies de laboratorio (resultados, muestras, QC)
**Sub-brand:** LIS clínico (tenant LCH) · LIS deportivo (tenant Biuman)
**Audiencia:** Técnicos de laboratorio, patólogos, bacteriólogos
**Apps de referencia:** `lab-qc`, `biuman-reports`
**Prioridades:** densidad de información, velocidad de lectura, precisión numérica, light + dark

> Esta guía porta la intención de `ds-lch-laboratorio` al **contrato del registro**
> (`../tokens.css`). No define colores propios: usa los tokens semánticos shadcn y
> la paleta de estado **independiente del acento** (`--success` / `--warning` /
> `--error` / `--info`). Las superficies de QC viven dentro de Pháros LIS (BRAND §3.4) —
> su rojo/ámbar es la expresión LIS de esa capa de estado, **no** un acento hermano.

---

## Acento (sub-brand)

El acento del **LIS clínico / deportivo está ABIERTO** — RFC 0008 Q1/Q6, pendiente de
`@SKuger01` / brand playground. **No inventar un acento.** Hasta que se cierre:

- Usa `--primary` / `--accent` / `--ring` / `--sidebar-primary` de forma **genérica**
  (heredados del contrato). Las acciones primarias y la navegación activa usan
  `--primary` — sea cual sea el valor que el sub-brand termine fijando.
- El **único** ERP con acento bloqueado es `Pháros · Timón` (navy `#003A70`). Esta
  superficie **no** es ERP, así que no asumas navy como su identidad.
- La paleta de estado, las constantes de marca y el radio se heredan sin cambios.

---

## Color por rol (mapa al contrato)

Nada de hex crudos, nada de `--lab-*` / `--qc-*`. Todo se expresa con tokens del contrato:

| Rol en laboratorio | Token | Notas |
|---|---|---|
| Superficie de app / fondo | `--background` | shell |
| Tarjeta / panel | `--card` / `--card-foreground` | |
| Texto principal | `--foreground` | |
| Texto secundario / unidades / rangos | `--muted-foreground` | (antes `--lab-text-muted`) |
| Acción primaria / nav activa | `--primary` | acento del sub-brand (TBD) |
| Acción / superficie de hover sutil | `--accent` / `--accent-foreground` | |
| Borde / divisores de tabla | `--border` | |
| **Resultado normal / en rango** | `--success` | teal — in control |
| **Resultado fuera de rango / en proceso** | `--warning` | ámbar — drift / pendiente |
| **Resultado crítico / muestra rechazada** | `--error` / `--destructive` | rojo — out of control |
| **Informativo / resuelto** | `--info` | azul |

Mapeo desde el archivo viejo:
`--lab-success → --success` · `--lab-warning → --warning` ·
`--lab-critical → --error/--destructive` · `--lab-pending`(lilac) **→ `--warning`**
(pendiente = drift en la paleta de estado; el lilac deja de ser un estado y queda
disponible como `--chart-5`). `resuelto/info → --info`.

> El rojo está reservado a **error/crítico** + la luz piloto de la marca. Nunca es
> una acción primaria.

---

## Tipografía

Tres familias del contrato (RFC 0008 Q5). **Sin JetBrains Mono. Sin Apax.**

```
font-display   → 'Fraunces'        — wordmark / display (raro en esta superficie)
font-sans      → 'Inter'           — toda la UI, etiquetas de examen, navegación
font-mono      → 'IBM Plex Mono'   — TODO dato numérico + etiquetas de columna
```

- **Todo valor numérico de laboratorio** usa `font-mono` + `tabular-nums` (alineación
  de cifras en tablas y celdas). Esto reemplaza el viejo `font-['JetBrains_Mono']` y
  `--font-data`.
- Etiquetas de columna / encabezados de tabla: `font-mono`, `uppercase`, `tracking-wide`,
  `text-muted-foreground` (antes `--font-label`).
- Etiqueta de examen: `font-sans`, `font-medium`, `text-sm`, `tracking-wide`.

Tamaños sugeridos (sin cambios de intención):
```
Valor de resultado grande   text-2xl font-medium tabular-nums   (~1.5–2rem)
Valor en tabla              text-sm tabular-nums
Rango de referencia         text-xs text-muted-foreground
```

---

## Espaciado y layout

```
Radio de tarjeta   rounded-lg     (--radius = 8px; modales rounded-xl)
Radio de badge     rounded-full
Sombra             shadow-sm
Sidebar fijo       w-64           (256px)
Alto de fila       ~48px          (densa pero legible)
Padding de tarjeta p-4 md:p-5
```

**Layout típico:** app-shell shadcn `Sidebar` (tokens `--sidebar-*`) + área de
contenido con header. El sidebar usa `--sidebar` / `--sidebar-foreground`; el ítem
activo, `--sidebar-primary`. (Reemplaza el viejo "sidebar navy fijo" — el color del
sidebar ya no es navy hardcodeado, sale del contrato/acento.)

Todo es **`.dark`-aware**: las superficies, bordes y la paleta de estado tienen su
variante en `.dark` dentro del contrato; no escribas colores claros/oscuros a mano.

---

## Inventario de componentes / superficies

> Nombres re-cortados al contrato (sin el prefijo `LchLaboratorio`). El sub-brand es
> un tenant; un tenant **nunca** prefija el nombre. Estos son los SFC shadcn-vue que
> la fase de componentes (RFC 0008, Phase-1) materializará; aquí va su intención.

### Tabla de resultados — `ResultTable`
Props: `results: LabResult[]`, `showRanges?: boolean`, `highlightCritical?: boolean`

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

Patrón de fila densa:
```vue
<tr class="border-b border-border hover:bg-accent transition-colors">
  <td class="px-4 py-3 text-sm font-medium text-foreground">{{ examen }}</td>
  <td class="px-4 py-3 font-mono text-sm tabular-nums">{{ valor }}</td>
  <td class="px-4 py-3 text-xs text-muted-foreground">{{ unidad }}</td>
  <td class="px-4 py-3 text-xs text-muted-foreground">{{ min }} – {{ max }}</td>
  <td class="px-4 py-3"><EstadoBadge :estado="estado" /></td>
</tr>
```

### Valor numérico de resultado
```vue
<div
  class="font-mono text-2xl font-medium tabular-nums"
  :class="{
    'text-error': resultado.estado === 'critico',
    'text-warning-foreground': resultado.estado === 'alto' || resultado.estado === 'bajo',
    'text-foreground': resultado.estado === 'normal',
  }"
>
  {{ resultado.valor }}
</div>
<div class="font-mono text-xs text-muted-foreground uppercase tracking-wide">
  {{ resultado.unidad }}
</div>
```

### Badge de estado — `EstadoBadge`
Props: `estado: 'pendiente' | 'procesando' | 'listo' | 'critico' | 'rechazado'`

Estado → token de la paleta de estado (independiente del acento):
```vue
<!-- listo / en control → success -->
<span class="bg-success/30 text-success-foreground px-3 py-1 rounded-full text-xs font-medium">Listo</span>
<!-- pendiente / procesando (drift) → warning -->
<span class="bg-warning/40 text-warning-foreground px-3 py-1 rounded-full text-xs font-medium">Pendiente</span>
<!-- critico → error -->
<span class="bg-error/10 text-error px-3 py-1 rounded-full text-xs font-medium">Crítico</span>
<!-- rechazado → error (variante outline) -->
<span class="bg-error/10 text-error px-3 py-1 rounded-full text-xs font-medium">Rechazado</span>
```

### KPI de laboratorio — `MetricCard`
Props: `label: string`, `valor: string | number`, `unidad?: string`, `delta?: number`

El valor usa `font-mono tabular-nums`. El `delta` colorea con la paleta de estado:
mejora → `text-success`, deterioro → `text-error`, neutro → `text-muted-foreground`
(nunca un verde/rojo crudo).

### Carta de control QC — `QcControlChart`
Superficie de QC dentro de LIS (BRAND §3.4). Gráfica de control (Levey-Jennings) con:
- Series y puntos vía `--chart-1..5` (numerados, RFC 0008 Q11; charts con `@unovis`).
- Bandas / estado del proceso con la paleta de estado:
  in-control → `--success` · drift → `--warning` · out-of-control → `--error` ·
  resuelto → `--info` · pendiente de evaluación → `--muted` / `--muted-foreground`.

### Navegación interna — `Sidebar`
Props: `items: NavItem[]`, `activeRoute: string`. App-shell shadcn `Sidebar`
(tokens `--sidebar-*`); ítem activo en `--sidebar-primary`.

### Panel de filtros — `Filtros`
Props: `filters: FilterConfig[]`.

---

## Patrones de UX del dominio

### Alerta clínica crítica
```vue
<div class="border-l-4 border-error bg-error/5 px-4 py-3 rounded-r-lg">
  <p class="text-error font-medium text-sm">Valor crítico — Requiere atención inmediata</p>
  <p class="text-foreground text-sm mt-1">{{ mensaje }}</p>
</div>
```

### Resaltado de resultado en/fuera de rango
- En rango → texto `--foreground`, badge `--success`.
- Fuera de rango (alto/bajo) → badge `--warning`; no uses rojo para "fuera de rango"
  no crítico (rojo es solo crítico).
- Crítico → texto y borde `--error`.

### Estado de muestra (flujo)
`pendiente`/`procesando` (drift, `--warning`) → `listo` (in control, `--success`) →
`critico` (`--error`) | `rechazado` (`--error`). Resoluciones / notas informativas → `--info`.

---

## Rutas de destino (en la app consumidora)

```
components/laboratorio/ResultTable.vue
components/laboratorio/EstadoBadge.vue
components/laboratorio/MetricCard.vue
components/laboratorio/QcControlChart.vue
components/laboratorio/Sidebar.vue
pages/laboratorio/resultados.vue
pages/laboratorio/muestras.vue
```

---

## Ported from `ds-lch-laboratorio`; what changed

- **Tokens.** Eliminados `--lab-*` y todo hex crudo / `var(--color-navy)` /
  `var(--color-brand-red)`. Reexpresado sobre tokens shadcn (`--background`,
  `--card`, `--foreground`, `--muted-foreground`, `--border`, `--primary`, `--accent`)
  + paleta de estado independiente del acento.
- **Estados.** `normal/en rango → --success` · `fuera de rango/pendiente → --warning`
  · `crítico/rechazado → --error/--destructive` · `info/resuelto → --info`. El
  `pending` lilac dejó de ser un color de estado (pasa a `--chart-5`).
- **Fuentes.** `JetBrains Mono` y `Apax` eliminadas. Datos numéricos + etiquetas de
  columna → `font-mono` (IBM Plex Mono) + `tabular-nums`. UI → `font-sans` (Inter).
- **Acento.** Antes el navy era la identidad de la superficie; ahora el acento del
  LIS está **TBD** (RFC 0008 Q1/Q6, `@SKuger01`). Se usa `--primary` genérico; no se
  inventa navy ni ningún otro acento. El sidebar sale de `--sidebar-*`, no de navy.
- **Componentes.** Sin prefijo `LchLaboratorio` (tenancy: un tenant no prefija el
  nombre de app). Añadido `QcControlChart` para reflejar que QC vive dentro de LIS.
- **Theming.** `.dark`-aware vía la clase shadcn `.dark`; sin tema `cobol`/CRT,
  sin `[data-theme]`.
