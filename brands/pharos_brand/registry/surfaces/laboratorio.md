# Pháros — surface guidance: Laboratorio

**Surface family:** Pháros LIS — superficies de laboratorio (resultados, muestras, QC)
**Sub-brand:** LIS clínico (tenant LCH) · LIS deportivo (tenant Biuman)
**Audiencia:** Técnicos de laboratorio, patólogos, bacteriólogos
**Apps de referencia:** `lab-qc`, `biuman-reports`
**Prioridades:** densidad de información, velocidad de lectura, precisión numérica, light + dark

> Esta guía porta la intención de `ds-lch-laboratorio` al **contrato del registro**
> (`../tokens.css`). No define colores propios: usa los tokens semánticos shadcn y
> la paleta de estado **independiente del acento** (`--status-success` / `--status-warning` /
> `--status-error` / `--status-info`). Las superficies de QC viven dentro de Pháros LIS (BRAND §3.4) —
> su rojo/ámbar es la expresión LIS de esa capa de estado, **no** un acento hermano.

---

## Acento (sub-brand)

Los acentos de sub-brand están **BLOQUEADOS** (RFC 0008 — ACCEPTED 2026-06-17). Esta
superficie pertenece al **LIS clínico** (tenant LCH), cuyo acento es **teal**
(`.theme-clinico`, `#1B6B5A` light / `#4CD1B0` dark); el **LIS deportivo** (tenant Biuman)
usa **azul** (`.theme-deportivo`, `#004F70` / `#16749C`). El tema vive como clase `.theme-*`
en `tokens.css`; la app añade su clase a `<html>`.

- Usa `--primary` / `--accent` / `--ring` / `--sidebar-primary` del contrato. Las acciones
  primarias y la navegación activa usan `--primary` — que el tema `.theme-clinico` /
  `.theme-deportivo` reapunta al acento del sub-brand.
- Un tema **solo** sobre-escribe los slots de acento (`--primary` / `--ring` /
  `--sidebar-primary` + sus foregrounds); el resto se hereda del contrato. Sin clase de
  tema, el neutro de familia es **LCH Navy `#003A70`** (Archivo).
- La paleta de estado, las constantes de marca y el radio se heredan sin cambios y **no**
  se mueven al re-acentuar.

---

## Color por rol (mapa al contrato)

Nada de hex crudos, nada de `--lab-*` / `--qc-*`. Todo se expresa con tokens del contrato:

| Rol en laboratorio | Token | Notas |
|---|---|---|
| Superficie de app / fondo | `--background` | shell |
| Tarjeta / panel | `--card` / `--card-foreground` | |
| Texto principal | `--foreground` | |
| Texto secundario / unidades / rangos | `--muted-foreground` | (antes `--lab-text-muted`) |
| Acción primaria / nav activa | `--primary` | acento del sub-brand (teal `.theme-clinico` / azul `.theme-deportivo`) |
| Acción / superficie de hover sutil | `--accent` / `--accent-foreground` | |
| Borde / divisores de tabla | `--border` | |
| **Resultado normal / en rango** | `--status-success` | verde — in control |
| **Resultado fuera de rango / en proceso** | `--status-warning` | ámbar — drift / pendiente |
| **Resultado crítico / muestra rechazada** | `--status-error` / `--destructive` | rojo — out of control |
| **Informativo / resuelto** | `--status-info` | azul |

Mapeo desde el archivo viejo:
`--lab-success → --status-success` · `--lab-warning → --status-warning` ·
`--lab-critical → --status-error/--destructive` · `--lab-pending`(lilac) **→ `--status-warning`**
(pendiente = drift en la paleta de estado; el lilac deja de ser un estado y queda
disponible como `--chart-5`). `resuelto/info → --status-info`.

> El rojo está reservado a **error/crítico** + la luz piloto de la marca. Nunca es
> una acción primaria.

---

## Tipografía

Cuatro familias del contrato (RFC 0008 — ACCEPTED 2026-06-17). **Sin Apax.**

```
font-display   → 'Fraunces'        — wordmark / display (raro en esta superficie)
font-sans      → 'DM Sans'         — toda la UI, navegación (la sans por defecto)
font-mono      → 'IBM Plex Mono'   — SOLO etiquetas / encabezados de columna
font-data      → 'JetBrains Mono'  — TODO dato numérico / cifras (tabular-nums)
```

- **Todo valor numérico de laboratorio** usa `font-data` (JetBrains Mono) + `tabular-nums`
  (alineación de cifras en tablas y celdas). JetBrains Mono **es** la cara de datos.
- Etiquetas de columna / encabezados de tabla: `font-mono` (IBM Plex Mono), `uppercase`,
  `tracking-wide`, `text-muted-foreground` (antes `--font-label`). IBM Plex Mono es solo
  para etiquetas, **no** para cifras.
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
  <td class="px-4 py-3 font-data text-sm tabular-nums">{{ valor }}</td>
  <td class="px-4 py-3 text-xs text-muted-foreground">{{ unidad }}</td>
  <td class="px-4 py-3 text-xs text-muted-foreground">{{ min }} – {{ max }}</td>
  <td class="px-4 py-3"><EstadoBadge :estado="estado" /></td>
</tr>
```

### Valor numérico de resultado
```vue
<div
  class="font-data text-2xl font-medium tabular-nums"
  :class="{
    'text-status-error': resultado.estado === 'critico',
    'text-status-warning': resultado.estado === 'alto' || resultado.estado === 'bajo',
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
<span class="bg-status-success-bg text-status-success px-3 py-1 rounded-full text-xs font-medium">Listo</span>
<!-- pendiente / procesando (drift) → warning -->
<span class="bg-status-warning-bg text-status-warning px-3 py-1 rounded-full text-xs font-medium">Pendiente</span>
<!-- critico → error -->
<span class="bg-status-error-bg text-status-error px-3 py-1 rounded-full text-xs font-medium">Crítico</span>
<!-- rechazado → error (variante outline) -->
<span class="bg-status-error-bg text-status-error px-3 py-1 rounded-full text-xs font-medium">Rechazado</span>
```

### KPI de laboratorio — `MetricCard`
Props: `label: string`, `valor: string | number`, `unidad?: string`, `delta?: number`

El valor usa `font-data tabular-nums`. El `delta` colorea con la paleta de estado:
mejora → `text-status-success`, deterioro → `text-status-error`, neutro → `text-muted-foreground`
(nunca un verde/rojo crudo).

### Carta de control QC — `QcControlChart`
Superficie de QC dentro de LIS (BRAND §3.4). Gráfica de control (Levey-Jennings) con:
- Series y puntos vía `--chart-1..5` (numerados, RFC 0008 Q11; charts con `@unovis`).
- Bandas / estado del proceso con la paleta de estado:
  in-control → `--status-success` · drift → `--status-warning` · out-of-control → `--status-error` ·
  resuelto → `--status-info` · pendiente de evaluación → `--muted` / `--muted-foreground`.

### Navegación interna — `Sidebar`
Props: `items: NavItem[]`, `activeRoute: string`. App-shell shadcn `Sidebar`
(tokens `--sidebar-*`); ítem activo en `--sidebar-primary`.

### Panel de filtros — `Filtros`
Props: `filters: FilterConfig[]`.

---

## Patrones de UX del dominio

### Alerta clínica crítica
```vue
<div class="border-l-4 border-status-error bg-status-error-bg px-4 py-3 rounded-r-lg">
  <p class="text-status-error font-medium text-sm">Valor crítico — Requiere atención inmediata</p>
  <p class="text-foreground text-sm mt-1">{{ mensaje }}</p>
</div>
```

### Resaltado de resultado en/fuera de rango
- En rango → texto `--foreground`, badge `--status-success`.
- Fuera de rango (alto/bajo) → badge `--status-warning`; no uses rojo para "fuera de rango"
  no crítico (rojo es solo crítico).
- Crítico → texto y borde `--status-error`.

### Estado de muestra (flujo)
`pendiente`/`procesando` (drift, `--status-warning`) → `listo` (in control, `--status-success`) →
`critico` (`--status-error`) | `rechazado` (`--status-error`). Resoluciones / notas informativas → `--status-info`.

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
- **Estados.** `normal/en rango → --status-success` · `fuera de rango/pendiente → --status-warning`
  · `crítico/rechazado → --status-error/--destructive` · `info/resuelto → --status-info`. El
  `pending` lilac dejó de ser un color de estado (pasa a `--chart-5`). Cada estado lleva un
  surface tint `-bg` y es **independiente del acento** (no se mueve al re-acentuar).
- **Fuentes.** `Apax` eliminada. Datos numéricos / cifras → `font-data` (JetBrains Mono) +
  `tabular-nums`. Etiquetas / encabezados de columna → `font-mono` (IBM Plex Mono). UI →
  `font-sans` (DM Sans). Display → `font-display` (Fraunces).
- **Acento.** Antes el navy era la identidad de la superficie; ahora el acento del
  LIS está **bloqueado** (RFC 0008 — ACCEPTED 2026-06-17): clínico **teal** (`.theme-clinico`),
  deportivo **azul** (`.theme-deportivo`). Se usa `--primary` y el tema lo reapunta; el neutro
  de familia sin clase es Navy `#003A70`. El sidebar sale de `--sidebar-*`, no de navy.
- **Componentes.** Sin prefijo `LchLaboratorio` (tenancy: un tenant no prefija el
  nombre de app). Añadido `QcControlChart` para reflejar que QC vive dentro de LIS.
- **Theming.** `.dark`-aware vía la clase shadcn `.dark`; sin tema `cobol`/CRT,
  sin `[data-theme]`.
