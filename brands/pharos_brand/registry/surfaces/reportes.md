---
description: "Use when creating components or pages for the Reportes surface — pathology report generation inside Pháros LIS (biuman-reports lineage). Clinical typography, structured documental sections, PDF-export ready, print-aware styles. Audience: pathologists and lab directors."
surface: reportes
app: Pháros LIS
accent: TBD (RFC 0008 Q1/Q6 — @SKuger01 / brand playground)
---
# Pháros — Surface: Reportes (generación de reportes de patología)

**Audiencia:** Patólogos, biólogos, directores de laboratorio
**App / surface:** **Pháros LIS** → Reportes (linaje `biuman-reports`; surface dentro de LIS, no sub-marca propia)
**Prioridades:** estructura documental, jerarquía tipográfica clara, diseño orientado a impresión/PDF, trazabilidad clínica

> Esta surface vive **dentro de Pháros LIS** (RFC 0004 §2 — QC y los surfaces de reporte se pliegan aquí). No es una sub-marca: hereda el contrato compartido (`registry/tokens.css`) sin alterarlo.

---

## Acento — TBD

La surface Reportes pertenece a **Pháros LIS**, cuyo acento aún **no está cerrado** (RFC 0008 Q1/Q6 — abierto para @SKuger01 / brand playground). Hasta que se resuelva:

- Usa `--primary` de forma **genérica** para encabezados, separadores de sección fuertes y la firma/validación profesional. NO inventes un acento concreto para esta surface.
- NUNCA codifiques navy `#003A70` ni ningún hex literal aquí: el navy está **bloqueado para ERP · Timón**, no para LIS/Reportes. Cuando el acento LIS se cierre, sólo cambia `--primary`/`--accent`/`--ring`/`--sidebar-primary`; esta surface no requiere edición.

> Rojo (`--pharos-red` / `--error` / `--destructive`) está **reservado** a estados de error y al pilot light — **nunca** a una acción primaria ni a un acento decorativo. El acento de firma/validación, que el archivo LCH original pintaba de rojo, ahora usa `--primary` (ver §Firma).

---

## Colores — Reportes (sobre el contrato shadcn + status palette)

Todo se expresa con tokens semánticos shadcn-vue y la **status palette acento-independiente** (`--success`/`--warning`/`--error`/`--info`). El documento de reporte es, por naturaleza, claro; pero todo es `.dark`-aware vía los tokens.

```
Rol documental                     Token / utilidad Tailwind v4
---------------------------------  --------------------------------------------
Fondo del documento                bg-card  (claro por contrato; .dark-aware)
Texto cuerpo del reporte           text-card-foreground
Encabezado del documento           bg-primary  text-primary-foreground
Encabezados / secciones clave      text-primary
Separadores de sección fuertes     border-primary  /  border-b-2 border-primary
Separadores suaves entre campos    border-border
Fondo de sección dentro del rep.   bg-muted
Etiquetas de campo / metadata      text-muted-foreground  (font-mono, uppercase)
Links / referencias                text-info
Firma / validación profesional     text-primary   (NO rojo)
```

### Status de resultado clínico (status palette, acento-independiente)

Para marcar resultados fuera de rango, banderas o estados de validación dentro de una tabla de resultados:

```
Estado del valor                   Token
---------------------------------  ----------------------------------
Dentro de rango / normal           --success
Limítrofe / a vigilar              --warning
Crítico / fuera de rango / pánico  --error  (= --destructive)
Informativo / nota de referencia   --info
```

Estos tokens **no se mueven** cuando LIS reciba su acento — son la capa de estado compartida (BRAND.md §3.4).

### Tailwind v4 — clases frecuentes

```
bg-card                  → fondo de documento (claro; .dark-aware)
bg-primary               → encabezado del reporte
text-primary-foreground  → texto sobre el encabezado
text-card-foreground     → texto cuerpo del reporte
font-mono tabular-nums   → valores numéricos de laboratorio (IBM Plex Mono)
font-mono                → etiquetas de campo, metadata
border-primary           → separadores de sección fuertes
border-border            → separadores suaves entre campos
text-error               → valor crítico / fuera de rango
print:shadow-none        → eliminar sombras al imprimir
print:border-0           → eliminar bordes decorativos al imprimir
```

---

## Tipografía — Reportes

El reporte debe ser **legible tanto en pantalla como impreso**. Datos y números → `font-mono` (IBM Plex Mono) + `tabular-nums`. (Sin JetBrains Mono, sin Apax.)

```css
/* Encabezado del reporte (nombre de examen) */
font-size: 1.25rem; font-weight: 700; color: var(--primary);

/* Nombre del paciente */
font-size: 1rem; font-weight: 600;

/* Etiquetas de campo (Fecha, Médico, etc.) */
font-family: var(--font-mono); font-size: 0.75rem;
text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted-foreground);

/* Valores de campo */
font-size: 0.9rem; font-weight: 400;

/* Valores numéricos del laboratorio en tablas */
font-family: var(--font-mono); font-size: 0.9rem; font-variant-numeric: tabular-nums;

/* Nota clínica / interpretación */
font-size: 0.875rem; line-height: 1.75; font-style: italic;

/* Firma profesional */
font-size: 0.875rem; font-weight: 600; color: var(--primary);
```

---

## Componentes disponibles

### `ReportesDocHeader` — Encabezado del reporte
Props: `paciente: PacienteInfo`, `examen: string`, `fecha: string`, `ordenMedica?: string`

```ts
interface PacienteInfo {
  nombre: string
  documento: string
  fechaNacimiento: string
  genero: 'M' | 'F' | 'otro'
  eps?: string
}
```

```vue
<ReportesDocHeader
  :paciente="{ nombre: 'María García', documento: '1.234.567.890', fechaNacimiento: '15/04/1985', genero: 'F' }"
  examen="Hemograma Completo"
  fecha="27/04/2026"
  orden-medica="OM-2026-00123"
/>
```

```vue
<!-- Patrón del header (acento = --primary, genérico hasta cerrar el acento LIS) -->
<header class="bg-primary text-primary-foreground px-8 py-6 rounded-t-lg">
  <div class="flex items-start justify-between">
    <PharosLogo theme="dark" size="navbar" />
    <div class="text-right font-mono text-xs">
      <p class="text-primary-foreground/70 uppercase tracking-wide">Reporte N°</p>
      <p class="text-primary-foreground font-medium tabular-nums">{{ reporteId }}</p>
    </div>
  </div>
  <div class="mt-6 grid grid-cols-3 gap-4 border-t border-primary-foreground/20 pt-4">
    <ReportesCampo label="Paciente" :value="paciente.nombre" inverted />
    <ReportesCampo label="Documento" :value="paciente.documento" inverted />
    <ReportesCampo label="Fecha" :value="fecha" inverted />
  </div>
</header>
```

### `ReportesCampo` — Campo etiqueta/valor del reporte
Props: `label: string`, `value: string`, `inverted?: boolean` (para encabezado sobre `--primary`)

```vue
<ReportesCampo label="Médico solicitante" value="Dr. Juan Pérez" />
```

```vue
<div>
  <p class="font-mono text-xs uppercase tracking-wide"
     :class="inverted ? 'text-primary-foreground/70' : 'text-muted-foreground'">
    {{ label }}
  </p>
  <p class="text-sm font-medium mt-0.5"
     :class="inverted ? 'text-primary-foreground' : 'text-card-foreground'">
    {{ value }}
  </p>
</div>
```

### `ReportesResultSection` — Sección de resultados
Props: `titulo: string`, `results: LabResult[]`

```vue
<ReportesResultSection titulo="Serie Roja" :results="serieRoja" />
```

```vue
<section class="mt-6">
  <h2 class="text-primary font-semibold text-base border-b-2 border-primary pb-1 mb-3">
    {{ titulo }}
  </h2>
  <table class="w-full text-sm">
    <thead>
      <tr class="bg-muted">
        <th class="px-3 py-2 text-left  font-mono text-xs uppercase tracking-wide text-muted-foreground">Parámetro</th>
        <th class="px-3 py-2 text-right font-mono text-xs uppercase tracking-wide text-muted-foreground">Resultado</th>
        <th class="px-3 py-2 text-center font-mono text-xs uppercase tracking-wide text-muted-foreground">Unidad</th>
        <th class="px-3 py-2 text-center font-mono text-xs uppercase tracking-wide text-muted-foreground">Rango Ref.</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="r in results" :key="r.parametro" class="border-b border-border">
        <td class="px-3 py-2">{{ r.parametro }}</td>
        <!-- valor numérico: font-mono + tabular-nums; fuera de rango -> text-error -->
        <td class="px-3 py-2 text-right font-mono tabular-nums"
            :class="r.fueraDeRango ? 'text-error font-semibold' : 'text-card-foreground'">
          {{ r.valor }}
        </td>
        <td class="px-3 py-2 text-center font-mono tabular-nums text-muted-foreground">{{ r.unidad }}</td>
        <td class="px-3 py-2 text-center font-mono tabular-nums text-muted-foreground">{{ r.rangoRef }}</td>
      </tr>
    </tbody>
  </table>
</section>
```

### `ReportesFirma` — Firma y validación profesional
Props: `nombre: string`, `titulo: string`, `registro: string`, `fechaValidacion: string`

> El acento de firma/validación usa **`--primary`** (acción/identidad), no rojo. El rojo queda reservado para error + pilot light.

```vue
<ReportesFirma
  nombre="Dra. Ana Martínez"
  titulo="Bacterióloga - Patóloga Clínica"
  registro="T.P. 12345"
  fecha-validacion="27/04/2026 14:32"
/>
```

```vue
<div class="border-t border-border pt-6 mt-8 flex items-end gap-6">
  <div>
    <div class="h-12 border-b-2 border-primary w-48 mb-1"></div>
    <p class="text-primary font-semibold text-sm">{{ nombre }}</p>
    <p class="text-muted-foreground text-xs font-mono">{{ titulo }}</p>
    <p class="text-muted-foreground text-xs font-mono">{{ registro }}</p>
  </div>
  <div class="ml-auto text-right">
    <p class="font-mono text-xs text-muted-foreground uppercase tracking-wide">Validado electrónicamente</p>
    <p class="font-mono text-xs text-primary tabular-nums">{{ fechaValidacion }}</p>
  </div>
</div>
```

### `ReportesInterpretacion` — Nota de interpretación clínica
Props: `texto: string`, `autor?: string`

```vue
<ReportesInterpretacion texto="Los valores se encuentran dentro de los rangos de referencia..." />
```

---

## Estilos de impresión / PDF

El driver de esta surface: el reporte debe salir limpio en papel/PDF. El contenedor usa `bg-card` (claro por contrato) y elimina chrome decorativo al imprimir.

```vue
<!-- Contenedor del documento listo para imprimir -->
<div class="bg-card text-card-foreground shadow-lg rounded-lg max-w-[800px] mx-auto my-8
            print:shadow-none print:rounded-none print:my-0 print:max-w-none print:bg-white print:text-black">
  <!-- contenido del reporte -->
</div>
```

```css
@media print {
  .sidebar { display: none; }     /* shadcn Sidebar (app-shell) — fuera al imprimir */
  .no-print { display: none; }
  body { font-size: 11pt; }
}
```

> Nota de impresión + `.dark`: el reporte en pantalla es `.dark`-aware vía los tokens, pero al imprimir se fuerza fondo blanco / texto negro (`print:bg-white print:text-black`) — el PDF clínico siempre sale en claro, sea cual sea el tema de la app.

---

## Rutas de destino
```
components/Reportes/ReportesDocHeader.vue
components/Reportes/ReportesCampo.vue
components/Reportes/ReportesResultSection.vue
components/Reportes/ReportesFirma.vue
components/Reportes/ReportesInterpretacion.vue
pages/reportes/[id].vue
pages/reportes/index.vue
```

---

## Ported from `ds-lch-reportes`; what changed

- **Surface placement.** Mapeada a **Pháros LIS → Reportes** (RFC 0004 §2: QC y reportes se pliegan dentro de LIS). El linaje `biuman-reports` se preserva como origen, pero no es una sub-marca.
- **Acento = TBD.** LIS no tiene acento cerrado (RFC 0008 Q1/Q6 — @SKuger01). Se usa `--primary` genérico; se eliminó todo `var(--color-navy)` / `--rep-*` y todo hex literal (`text-[#111827]`, `#F8FAFC`, `#FFFFFF`). El navy `#003A70` está bloqueado para ERP · Timón, **no** para esta surface.
- **Firma ya no es roja.** El archivo LCH usaba `--color-brand-red` para la firma/validación. Corregido: firma y validación usan `--primary`. El rojo (`--error`/`--destructive`/`--pharos-red`) queda reservado a estados de error + pilot light.
- **Fuente de datos.** Valores de laboratorio pasan de `JetBrains Mono` a `font-mono` (**IBM Plex Mono**) + `tabular-nums`. JetBrains Mono y Apax no se usan en UI de producto.
- **Status palette.** Resultados fuera de rango / crítico → `--error`; limítrofe → `--warning`; normal → `--success`; nota informativa / links → `--info`. Capa de estado acento-independiente (BRAND.md §3.4).
- **Tokens colapsados.** `--rep-text-muted` → `--muted-foreground`; `--rep-section-bg` → `bg-muted`; `bg-white` → `bg-card`; separadores fuertes → `border-primary`.
- **Theming.** `.dark`-aware vía tokens shadcn (clase `.dark`, sin `[data-theme]`, sin tema `cobol`/CRT). La impresión fuerza claro independientemente del tema.
- **Logo.** `LchLogo` → `PharosLogo` (el wordmark Pháros es constante de familia, nunca se re-tinta al acento).
- **Componentes.** Prefijo `Lch*` retirado de la API de componentes (un tenant nunca prefija; ver BRAND.md §10).
