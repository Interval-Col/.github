# Surface — Calidad (Pháros LIS · QC)

**Audiencia:** Equipo de control de calidad, coordinador de calidad.
**Pertenece a:** `Pháros LIS` — superficie de **Calidad / Control de Calidad** (la antigua app `lab-qc`).
**Prioridades:** visualización de datos de control, gráficos Levey-Jennings, indicadores de desvío, reglas Westgard, trazabilidad de lote.

> Construye sobre el contrato de tokens del registro: [`../tokens.css`](../tokens.css).
> Convenciones de autoría (Nuxt 4 / Vue 3 / Tailwind v4): [`../frontend-standards.md`](../frontend-standards.md).
> Esta superficie hereda **todo** el contrato y solo se diferencia por su acento de sub-marca (ver abajo).

---

## Acento de sub-marca

`Pháros LIS` es una sub-marca **no-ERP**. Su acento **no está decidido** — es un ítem
abierto del playground de marca (RFC 0008 Q1/Q6, **@SKuger01**). Por tanto:

- **NO** inventes un acento concreto para esta superficie.
- Usa `--primary` / `--accent` / `--ring` / `--sidebar-primary` de forma **genérica**;
  el valor real lo fijará la sub-marca sobreescribiendo solo esos slots.
- Lo que **sí** es estable: la paleta de estado (`--success`/`--warning`/`--error`/`--info`),
  los neutrales, las constantes de marca y el radio — se heredan sin cambios.

> Si en algún momento esta superficie se reasignara a `Pháros · Timón` (ERP), el acento
> sería navy `#003A70` (LOCKED) — pero hoy **Calidad no es ERP**: acento **TBD**.

---

## Paleta de estado de control — la pieza central de esta superficie

El estado de control mapea **directamente** sobre la paleta de estado accent-independiente
del contrato. Nunca uses el acento de la sub-marca para comunicar estado, ni al revés.

| Estado de control QC | Token | Utilidad Tailwind | Significado |
|---|---|---|---|
| **En control** (in-control / positivo) | `--success` | `bg-success/20 border-success text-success-foreground` | dentro de límites |
| **Advertencia** (drift, regla 1-2s) | `--warning` | `bg-warning/30 border-warning text-warning-foreground` | desvío incipiente |
| **Fuera de control** (out-of-control, crítico) | `--error` / `--destructive` | `bg-error/10 border-error text-error` | regla 1-3s, R-4s violadas |
| **Resuelto / informativo** | `--info` | `bg-info/10 border-info text-info` | nota, resolución, contexto |

Reglas duras de color en esta superficie:

- **Nunca** uses literales hex (`text-[#...]`) ni los tokens LCH viejos
  (`var(--color-navy)`, `var(--color-brand-red)`, `--qc-*`). Todo va por tokens semánticos.
- El **rojo** (`--error`/`--destructive`) queda reservado para *fuera de control* y para
  el "pilot light" de marca — **nunca** para una acción primaria.
- Superficies y bordes neutros: `bg-card`, `bg-background`, `border-border`,
  `text-foreground`, `text-muted-foreground`. El antiguo `--qc-bg` teal y el
  `--qc-border` teal-suave desaparecen; el carácter "teal" lo aporta `--success`
  donde comunica *en control*, no como fondo decorativo.
- Tema **claro + oscuro** vía la clase `.dark` de shadcn. Los tokens ya resuelven
  ambos temas; no escribas valores oscuros a mano.

---

## Tipografía — Calidad

Tres familias del contrato (RFC 0008 Q5): **Fraunces** (display) · **Inter** (UI) ·
**IBM Plex Mono** (datos + etiquetas). **No** se usa JetBrains Mono ni Apax.

```
font-mono tabular-nums    → TODO valor estadístico (media x̄, SD σ, CV %, Z-score) y celdas de tabla QC
font-mono                 → etiquetas de regla Westgard (1-2s, 1-3s, R-4s, 2-2s…) y micro-labels
font-sans                 → texto de UI, controles, descripciones
font-display              → títulos de pantalla / encabezados de sección (uso moderado)
```

`tabular-nums` es **obligatorio** en cualquier número que pueda alinearse en columna
(tablas de registro, tarjetas de estadísticas, ejes). Los datos siempre `font-mono`.

---

## Componentes de la superficie

> Inventario portado de la guía LCH original. Los nombres pierden el prefijo de tenant
> (`Lch…`) — un tenant nunca prefija el nombre de la app/superficie. Implementación final
> como SFC shadcn-vue: pendiente del build de Fase 1 (ver registro README "Decided vs open").

### `CalidadEstadoIndicator` — Indicador de estado de control
Props: `estado: 'en-control' | 'advertencia' | 'fuera-control'`, `regla?: string`

```vue
<CalidadEstadoIndicator estado="en-control" />
<CalidadEstadoIndicator estado="advertencia" regla="1-2s" />
<CalidadEstadoIndicator estado="fuera-control" regla="1-3s" />
```

```vue
<!-- En control → success -->
<div class="flex items-center gap-2 rounded-lg border border-success bg-success/20 px-3 py-2">
  <span class="h-2.5 w-2.5 rounded-full bg-success"></span>
  <span class="text-sm font-medium text-foreground">En control</span>
</div>

<!-- Advertencia → warning + regla -->
<div class="flex items-center gap-2 rounded-lg border border-warning bg-warning/30 px-3 py-2">
  <span class="h-2.5 w-2.5 rounded-full bg-warning"></span>
  <span class="text-sm font-medium text-foreground">Advertencia</span>
  <span class="ml-1 font-mono text-xs text-muted-foreground">{{ regla }}</span>
</div>

<!-- Fuera de control → error (la única regla que parpadea) -->
<div class="flex items-center gap-2 rounded-lg border border-error bg-error/10 px-3 py-2">
  <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-error"></span>
  <span class="text-sm font-medium text-error">Fuera de control</span>
  <span class="ml-1 font-mono text-xs text-error">{{ regla }}</span>
</div>
```

### `CalidadEstadisticasCard` — Estadísticas del lote QC
Props: `analito: string`, `nivel: string`, `media: number`, `sd: number`, `cv: number`, `n: number`

```vue
<CalidadEstadisticasCard
  analito="Glucosa"
  nivel="Nivel 1"
  :media="95.4"
  :sd="2.1"
  :cv="2.2"
  :n="30"
/>
```

```vue
<!-- Patrón interno: números en font-mono + tabular-nums; superficie en card -->
<div class="grid grid-cols-4 gap-4 rounded-lg border border-border bg-card p-4">
  <div v-for="stat in [
    { label: 'media (x̄)', value: media },
    { label: 'SD (σ)',     value: sd },
    { label: 'CV (%)',     value: cv },
    { label: 'N',          value: n },
  ]" :key="stat.label">
    <p class="font-mono text-xs uppercase tracking-wide text-muted-foreground">{{ stat.label }}</p>
    <p class="font-mono text-xl font-medium tabular-nums text-foreground">{{ stat.value }}</p>
  </div>
</div>
```

### `CalidadReglaTag` — Etiqueta de regla Westgard
Props: `regla: string`, `violada?: boolean`

```vue
<CalidadReglaTag regla="1-2s" />
<CalidadReglaTag regla="1-3s" :violada="true" />
<CalidadReglaTag regla="R-4s" :violada="true" />
```

```vue
<span
  class="rounded px-2 py-0.5 font-mono text-xs"
  :class="violada
    ? 'bg-error/10 text-error font-semibold'
    : 'bg-muted text-muted-foreground'">
  {{ regla }}
</span>
```

### `CalidadRegistroTable` — Tabla de registro de controles
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

### `CalidadResumenDashboard` — Resumen de estado de todos los analitos
Grid de analitos con su estado de control actual (cada celda = `CalidadEstadoIndicator`).
Para series temporales / Levey-Jennings, usa los tokens de gráfico del contrato
(`--chart-1..5`), no colores ad hoc.

---

## Patrones de código

### Fila de tabla QC con resaltado por estado
El resaltado de fila comunica **estado**, así que va por la paleta de estado — nunca por el acento.

```vue
<tr
  class="border-b border-border"
  :class="{
    'bg-error/5':   registro.reglaViolada,
    'bg-warning/10': Math.abs(registro.z) > 2 && !registro.reglaViolada,
    'hover:bg-accent': !registro.reglaViolada,
  }">
  <td class="px-4 py-3 font-mono text-sm tabular-nums text-foreground">{{ registro.valor }}</td>
  <td
    class="px-4 py-3 font-mono text-sm tabular-nums"
    :class="Math.abs(registro.z) > 3 ? 'font-semibold text-error' : 'text-foreground'">
    {{ registro.z.toFixed(2) }}
  </td>
  <td class="px-4 py-3">
    <CalidadReglaTag v-if="registro.reglaViolada" :regla="registro.reglaViolada" :violada="true" />
  </td>
</tr>
```

---

## Rutas de destino (en el app consumidor)

```
components/Calidad/CalidadEstadoIndicator.vue
components/Calidad/CalidadEstadisticasCard.vue
components/Calidad/CalidadReglaTag.vue
components/Calidad/CalidadRegistroTable.vue
components/Calidad/CalidadResumenDashboard.vue
pages/calidad/dashboard.vue
pages/calidad/registros/[analito].vue
```

---

## Portado desde `ds-lch-calidad`; qué cambió

- **Tokens de estado, no colores de marca.** En control → `--success`; advertencia/drift
  → `--warning`; fuera de control/crítico → `--error`/`--destructive`; resuelto/info →
  `--info`. Se eliminaron todos los `--qc-*`, `var(--color-navy)`, `var(--color-brand-red)`,
  los fondos `--qc-bg`/`--qc-border` teal y todos los literales hex / clases `text-[#...]` /
  `bg-lch-*` / `text-lch-*`.
- **Acento desacoplado del estado.** El acento de la sub-marca queda como `--primary`
  genérico y marcado **TBD** (RFC 0008 Q6, @SKuger01); ya no se hornea navy/teal como
  "color QC". El rojo se reserva para *fuera de control* + pilot light, nunca para acción.
- **Tipografía al contrato de 3 familias.** Todos los valores estadísticos y celdas pasan
  a `font-mono` (IBM Plex Mono) + `tabular-nums`. Se eliminó **JetBrains Mono**; las
  etiquetas de regla Westgard siguen en `font-mono`. Sin Apax.
- **Theming.** Claro + oscuro vía la clase `.dark` de shadcn; sin tema `cobol`/CRT, sin
  `[data-theme]`. Los tokens resuelven ambos temas.
- **Tenancy / naming.** Componentes pierden el prefijo `Lch…`; la superficie pertenece a
  `Pháros LIS` (un tenant nunca prefija el nombre). Maker = Interval · The Human Tech Co.
  (solo crédito de footer).
