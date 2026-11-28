# Pháros — guía de superficie: Búsqueda

**Qué es:** el estándar de búsqueda de todas las apps Pháros (épico `Interval-Col/design-studio#124`,
plan `design-studio/plans/estandar-de-busqueda-plan.md`). Se prototipó en el Playground de
design-studio con datos sintéticos y German lo aprobó vista por vista; la primera vista es
Liberación (2026-11-27). La enmienda a la RFC 0008 que lo ratifica está en `Interval-Col/rfcs#312`.

---

## La regla

Un campo de texto **filtra lo que ya está en pantalla** o **le pregunta al servidor**. Nunca las
dos cosas, y nunca cambia de una a otra sin avisar. Si una pantalla necesita las dos, lleva dos
controles con dos verbos: «Filtrar» y «Buscar».

## Cuándo pregunta, según lo que cuesta

| Fuente | Cuándo busca | Pieza |
|---|---|---|
| Lo que ya está en pantalla | Al teclear, con «Mostrando X de Y». Cero llamadas | `ListFilter` + `useSearchText` · `MultiSelectBuscable` |
| Servidor barato y sin datos de pacientes | Al teclear: 300 ms, mínimo 2 letras (D3) | `useDebouncedQuery` · `SearchableSelect` |
| Costoso, con datos de pacientes o el LIS | Sólo con «Buscar» o Enter: un solo submit | `Buscador` · `BuscadorEnLinea` + `useBuscador` |
| Barra que carga una bandeja | Todo con un botón («Cargar bandeja») | `DateRange` · `DateRangeCompacto` |

## Las piezas

- **`components/ui/list-filter/`** — `ListFilter` (prop `compacto` para una barra de una línea) y
  `ListFilterVacio`. Nunca llama al servidor.
- **`components/ui/buscador/`** — `Buscador` (pinta resultados) y `BuscadorEnLinea` (una línea; la
  pantalla pinta los resultados). Modos Orden · Documento · Nombre en pestañas (D1). Documento =
  tipo + número, sin tipo por defecto (D8). Nombre = tres campos, palabra completa o 3 letras, y
  eco obligatorio de la llave 3+3+3 (D4). Resultados enmascarados hasta revelar (D20).
- **`composables/useBuscador.ts`** — el motor: borrador ≠ aplicada, un envío a la vez, guarda de
  respuestas viejas, estados (error ≠ sin resultados; truncado = sin filas y pide afinar).
- **`components/ui/date-range/`** — `DateRange` y `DateRangeCompacto` (un botón con el rango). Atajos
  en `America/Bogota`, sin ventana máxima (D21): sólo avisa si es amplio.
- **`components/ui/multi-select/MultiSelectBuscable.vue`** — escoger varias con búsqueda por texto y
  por varias claves; cada opción dice por qué coincidió. Ancho fijo (`anchoClase`).
- **`lib/busqueda/`** — tipos, plegado, llave de nombre (porte exacto de `name_key()` de lab-qc),
  enmascarado, tipos de documento, estados, textos con «tú», examen por claves.

## Datos de pacientes (no negociable)

- Los identificadores viajan **sólo en el cuerpo de un POST**: nunca en la ruta, el query, la
  historia, el almacenamiento del navegador, la consola ni un access log (también entre servicios).
- **Buscar nunca crea** (D15): traer a alguien del LIS es un acto aparte, con nombre y confirmación.
- `useBuscador` recuerda la última búsqueda **en memoria** para volver atrás: vence a los 10 min y
  la app **llama a `olvidarBusquedas()` al cerrar sesión o cambiar de usuario**.
- Datos nuevos del servidor llegan enmascarados aunque antes se hubiera revelado.

## Al adoptar

- `scripts/sync-pharos-registry.sh --add <ruta> <app-fe-dir>` por cada pieza; el bot de resync
  sólo refresca lo que la app ya tiene.
- Dependen de primitivas shadcn que cada app tiene local (`input`, `label`, `tabs`, `button`,
  `checkbox`, `popover`) y de `ui/icon`.
- `BuscadorEnLinea` crece con el espacio de la barra por container query: pon `@container` en la
  barra que lo contiene. Sin él se queda en 15rem.
- Una barra fija debe usar el relleno de SU contenedor con scroll (en el Playground, `-top-6`).
- El portón `check-search-contract` (aviso → falla por app al migrar, D12) es la tarea 3.2 del plan;
  todavía no existe.
