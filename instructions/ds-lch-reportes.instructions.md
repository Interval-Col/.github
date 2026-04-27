---
description: "Use when creating components or pages for LCH Reportes — the biuman-reports pathology report generation system. Clinical typography, structured sections, PDF-export ready, print-aware styles. Audience: pathologists and lab directors."
---
# Design System — LCH Reportes (biuman-reports)

**Audiencia:** Patólogos, biólogos, directores de laboratorio  
**Aplicación:** `biuman-reports`  
**Prioridades:** estructura documental, jerarquía tipográfica clara, diseño orientado a impresión/PDF, trazabilidad clínica

---

## Paleta de colores — Reportes

```css
/* Sección Reportes */
--rep-primary:       var(--color-navy);         /* #003A70 — encabezados, secciones clave */
--rep-secondary:     var(--color-brand-red);    /* #E4002B — acento de firma/validación */
--rep-accent:        var(--color-blue);         /* #326295 — links, referencias */
--rep-bg:            #FFFFFF;                   /* fondo de reporte — siempre blanco */
--rep-bg-header:     var(--color-navy);         /* encabezado del documento */
--rep-section-bg:    #F8FAFC;                   /* fondo de sección dentro del reporte */
--rep-text:          #111827;                   /* negro denso para máxima legibilidad */
--rep-text-muted:    var(--color-gray-dark);
--rep-border:        var(--color-border);
--rep-border-strong: var(--color-navy);
--rep-signature:     var(--color-brand-red);    /* #E4002B — firma digital validada */
```

### Tailwind v4 — Clases frecuentes
```
bg-white                 → fondo de documento
bg-lch-navy              → encabezado del reporte
text-white               → texto sobre navy
text-[#111827]           → texto cuerpo del reporte
font-['JetBrains_Mono']  → valores numéricos de laboratorio
font-['IBM_Plex_Mono']   → etiquetas de campos, metadata
border-lch-navy          → separadores de sección fuertes
border-lch-gray-mid      → separadores suaves entre campos
print:shadow-none        → eliminar sombras al imprimir
print:border-0           → eliminar bordes decorativos al imprimir
```

---

## Tipografía — Reportes

El reporte debe ser **legible tanto en pantalla como impreso**:

```css
/* Encabezado del reporte (nombre de examen) */
font-size: 1.25rem; font-weight: 700; color: var(--rep-primary);

/* Nombre del paciente */
font-size: 1rem; font-weight: 600;

/* Etiquetas de campo (Fecha, Médico, etc.) */
font-family: 'IBM Plex Mono'; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--rep-text-muted);

/* Valores de campo */
font-size: 0.9rem; font-weight: 400;

/* Valores numéricos del laboratorio en tablas */
font-family: 'JetBrains Mono'; font-size: 0.9rem; tabular-nums;

/* Nota clínica / interpretación */
font-size: 0.875rem; line-height: 1.75; font-style: italic;

/* Firma profesional */
font-size: 0.875rem; font-weight: 600; color: var(--rep-signature);
```

---

## Componentes disponibles

### `LchReportesDocHeader` — Encabezado del reporte
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
<LchReportesDocHeader
  :paciente="{ nombre: 'María García', documento: '1.234.567.890', fechaNacimiento: '15/04/1985', genero: 'F' }"
  examen="Hemograma Completo"
  fecha="27/04/2026"
  orden-medica="OM-2026-00123"
/>
```

```vue
<!-- Patrón del header -->
<header class="bg-lch-navy text-white px-8 py-6 rounded-t-lg">
  <div class="flex items-start justify-between">
    <LchLogo theme="dark" size="navbar" />
    <div class="text-right font-['IBM_Plex_Mono'] text-xs">
      <p class="text-lch-gray-mid uppercase tracking-wide">Reporte N°</p>
      <p class="text-white font-medium">{{ reporteId }}</p>
    </div>
  </div>
  <div class="mt-6 grid grid-cols-3 gap-4 border-t border-white/20 pt-4">
    <LchReportesCampo label="Paciente" :value="paciente.nombre" inverted />
    <LchReportesCampo label="Documento" :value="paciente.documento" inverted />
    <LchReportesCampo label="Fecha" :value="fecha" inverted />
  </div>
</header>
```

### `LchReportesCampo` — Campo etiqueta/valor del reporte
Props: `label: string`, `value: string`, `inverted?: boolean` (para fondo dark)

```vue
<LchReportesCampo label="Médico solicitante" value="Dr. Juan Pérez" />
```

```vue
<div>
  <p class="font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide"
     :class="inverted ? 'text-lch-gray-mid' : 'text-lch-gray-dark'">
    {{ label }}
  </p>
  <p class="text-sm font-medium mt-0.5"
     :class="inverted ? 'text-white' : 'text-[#111827]'">
    {{ value }}
  </p>
</div>
```

### `LchReportesResultSection` — Sección de resultados
Props: `titulo: string`, `results: LabResult[]`

```vue
<LchReportesResultSection titulo="Serie Roja" :results="serieRoja" />
```

```vue
<section class="mt-6">
  <h2 class="text-lch-navy font-semibold text-base border-b-2 border-lch-navy pb-1 mb-3">
    {{ titulo }}
  </h2>
  <table class="w-full text-sm">
    <thead>
      <tr class="bg-[#F8FAFC]">
        <th class="px-3 py-2 text-left font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide text-lch-gray-dark">Parámetro</th>
        <th class="px-3 py-2 text-right font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide text-lch-gray-dark">Resultado</th>
        <th class="px-3 py-2 text-center font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide text-lch-gray-dark">Unidad</th>
        <th class="px-3 py-2 text-center font-['IBM_Plex_Mono'] text-xs uppercase tracking-wide text-lch-gray-dark">Rango Ref.</th>
      </tr>
    </thead>
  </table>
</section>
```

### `LchReportesFirma` — Firma y validación profesional
Props: `nombre: string`, `titulo: string`, `registro: string`, `fechaValidacion: string`

```vue
<LchReportesFirma
  nombre="Dra. Ana Martínez"
  titulo="Bacterióloga - Patóloga Clínica"
  registro="T.P. 12345"
  fecha-validacion="27/04/2026 14:32"
/>
```

```vue
<div class="border-t border-lch-gray-mid pt-6 mt-8 flex items-end gap-6">
  <div>
    <div class="h-12 border-b-2 border-lch-red w-48 mb-1"></div>
    <p class="text-lch-red font-semibold text-sm">{{ nombre }}</p>
    <p class="text-lch-gray-dark text-xs font-['IBM_Plex_Mono']">{{ titulo }}</p>
    <p class="text-lch-gray-dark text-xs font-['IBM_Plex_Mono']">{{ registro }}</p>
  </div>
  <div class="ml-auto text-right">
    <p class="font-['IBM_Plex_Mono'] text-xs text-lch-gray-dark uppercase tracking-wide">Validado electrónicamente</p>
    <p class="font-['JetBrains_Mono'] text-xs text-lch-navy">{{ fechaValidacion }}</p>
  </div>
</div>
```

### `LchReportesInterpretacion` — Nota de interpretación clínica
Props: `texto: string`, `autor?: string`

```vue
<LchReportesInterpretacion texto="Los valores se encuentran dentro de los rangos de referencia..." />
```

---

## Estilos de impresión / PDF

```vue
<!-- Contenedor del documento listo para imprimir -->
<div class="bg-white shadow-lg rounded-lg max-w-[800px] mx-auto my-8 print:shadow-none print:rounded-none print:my-0 print:max-w-none">
  <!-- contenido del reporte -->
</div>
```

```css
@media print {
  .sidebar { display: none; }
  .no-print { display: none; }
  body { font-size: 11pt; }
}
```

---

## Rutas de destino
```
components/Reportes/LchReportesDocHeader.vue
components/Reportes/LchReportesCampo.vue
components/Reportes/LchReportesResultSection.vue
components/Reportes/LchReportesFirma.vue
components/Reportes/LchReportesInterpretacion.vue
pages/reportes/[id].vue
pages/reportes/index.vue
```
