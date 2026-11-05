# Pháros map — MapaBase (RFC 0043 · RFC 0008)

**El único renderizador de mapas de las apps Pháros** (RFC 0043 R1). MapLibre GL JS 6 desde npm,
empaquetado por el build de la app: **sin CDN y sin teselas, estilos, glifos ni sprites de
terceros** (R2). Pinta agregados (R4): coropletas, una superficie de calor y puntos, con los colores
de los tokens, y **siempre** trae una tabla con las mismas cifras.

> Es **presentación pura**. No hace fetch, no suprime ni redondea cifras: lo que llega a sus props ya
> es publicable. El backend de la app (RFC 0013) sirve las colecciones y, si hay mapa base, el
> archivo `.pmtiles` desde su propio origen.

## What's in the registry

| Entry | Path | What it is |
|---|---|---|
| `MapaBase` | `app/components/ui/mapa-base/MapaBase.vue` | el mapa (canvas de MapLibre, zoom con botones y teclado) + el conmutador Mapa / Tabla + la tabla R4, que **siempre** está en el DOM |
| tipos | `app/components/ui/mapa-base/types.ts` | `CapaCoropletas`, `CapaCalor`, `CapaPuntos`, `MapaBaseOrigen` |
| barrel | `app/components/ui/mapa-base/index.ts` | exporta componente + tipos |
| lógica pura | `app/lib/mapa.ts` | cortes de la escala, rampa desde tokens, filas de la tabla, el estilo de MapLibre y el guardia de URLs externas — funciones puras, probadas en `scripts/test_mapa_lib.mjs` |

Adopción: `scripts/sync-pharos-registry.sh <app-fe-dir> --add components/ui/mapa-base/MapaBase.vue`
trae también sus compañeros (tipos, barrel, `lib/mapa.ts`, `Button`, `Icon`).

**Deps (por app, con rango de versión y lockfile, nunca `latest`):**

```bash
pnpm add maplibre-gl@^6.16.0 pmtiles@^4.5.0 @protomaps/basemaps@^5.7.2
```

`pmtiles` y `@protomaps/basemaps` solo se cargan si hay mapa base (import dinámico).

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `etiqueta` | `string` | — (obligatoria) | nombre accesible del mapa y título de la tabla |
| `centro` | `[lon, lat]` | Valle de Aburrá | |
| `zoom` | `number` | `11` | |
| `origen` | `MapaBaseOrigen \| null` | `null` | `{ url, glyphs?, sprite? }` del **mismo origen** de la app. Sin él, el mapa es el token de fondo + las capas de datos. Una URL de otro origen **lanza** (R2) |
| `fuente` | `string` | `'Noto Sans Regular'` | pila de fuente para rótulos; tiene que existir bajo `origen.glyphs` |
| `coropletas` | `CapaCoropletas \| null` | `null` | polígonos coloreados por `valor`; `etiqueta` da la primera columna de la tabla; `pasos` (5) clases en escala raíz cuadrada |
| `calor` | `CapaCalor \| null` | `null` | puntos con `peso` opcional |
| `puntos` | `CapaPuntos \| null` | `null` | lugares marcados; rotulados solo si hay `glyphs` |
| `encuadre` | `Limites \| null` | `null` | `[[oeste, sur], [este, norte]]` a encuadrar; `limitesDe(colección)` lo calcula. Al volver a `null`, regresa a `centro` y `zoom` |
| `resaltado` | `string \| null` | `null` | id de la zona a contornear |
| `nombreValor` | `string` | `'Valor'` | encabezado de la columna de cifras |
| `formato` | `(v) => string` | `es-CO`, 1 decimal | texto de cada cifra en la tabla |

**Evento:** `seleccionar(id)` al hacer clic en una zona del mapa o en su fila de la tabla. El id
sale de `properties.id` (o del `id` de la feature).

## Reglas que el componente hace cumplir

- **Nada externo por defecto.** Sin `origen` no hay fuentes, glifos ni sprites en el estilo. Con
  `origen`, toda URL debe ser relativa o del mismo origen de la página; otra cosa lanza un error que
  el componente muestra (`role="alert"`) en vez de cargarla.
- **Colores de los tokens.** `--background` → `--chart-2` para la rampa y el calor, `--border` para
  los bordes, `--primary` para los puntos, `--foreground` para los rótulos. Se leen en tiempo de
  ejecución y se re-aplican cuando cambia la clase de `<html>` (`.dark`, `.theme-*`).
- **La tabla R4 nunca falta.** Está en el DOM con las mismas cifras de las coropletas; mientras se
  ve el mapa queda oculta a la vista (`sr-only`), no a los lectores de pantalla. Una zona sin cifra
  sale transparente en el mapa y con «—» en la tabla: las dos leen el mismo valor limpio
  (`normalizarCoropletas`). `calor` y `puntos` no tienen fila propia: si una app muestra cifras solo
  por ahí, le debe a la persona su alternativa en texto.
- **Una sola parada de tabulación en el mapa**: el canvas de MapLibre (flechas desplazan, `+`/`-`
  acercan), con el nombre de `etiqueta`, y los botones de zoom. Las filas de la tabla solo entran al
  orden de tabulación cuando la tabla está a la vista.
- **El guardia de origen** decide con el parser de URL, el mismo con el que pide el navegador: una
  ruta con barras invertidas (que el navegador lee como `/`) también cuenta como externa. El mapa
  base compartido que describe la RFC 0043 R2 pasa si sale por el mismo dominio de la app.

## Trampas ya pagadas

- 🪤 **El worker de MapLibre 6 se pierde si el bundler pre-empaqueta el paquete** (`optimizeDeps` de
  Vite mueve el módulo y rompe su URL relativa): aparece el canvas y nunca se pinta nada. El
  componente importa el worker con `?worker&url` y llama `setWorkerUrl`; ninguna app tiene que tocar
  su configuración de Vite.
- 🪤 **`setStyle` con diff puede no emitir `style.load`**: las capas de datos (que no son parte del
  objeto de estilo) desaparecerían al cambiar una prop o el tema. El componente usa `diff: false`.
- **Las zonas van debajo de los rótulos del mapa base.** Coropletas y calor se insertan antes de la
  primera capa de texto del mapa base, para que los nombres de calles y barrios se lean encima del
  color. Las sedes y su nombre quedan arriba de todo. Sin `glyphs` no hay rótulos y todo va encima.
- 🪤 **Cambiar datos no reconstruye el estilo.** Solo se repintan las capas de datos, porque un
  `setStyle` volvería a procesar el mapa base en cada filtro. El estilo completo se rehace al cambiar
  `origen` o el tema.
- 🪤 **Una coropleta sin valores o toda en cero no tiene cortes**, y un `step` sin paradas es inválido:
  `expresionRelleno` devuelve entonces un solo color.
- 🪤 **Un token puede no ser un color que MapLibre entienda** (`color-mix(…)`, `oklch(…)`): el
  componente lo resuelve pintándolo en un píxel y leyéndolo como RGB. Leer `fillStyle` no basta,
  porque Chrome devuelve `oklab(…)`.
- 🪤 **El servidor que entrega el `.pmtiles` tiene que atender `Range`** (206 con
  `Content-Length`). El servidor de producción de Nitro, por ejemplo, no lo hace con los archivos de
  `public/`, y el mapa base no carga («HTTP Byte Serving»). El BFF de la app es quien lo sirve.
- 🪤 **Un WebGL en una pestaña de fondo pinta negro.** Para revisar el mapa, míralo en la pestaña
  activa antes de darlo por roto.
- 🪤 El portón `check-token-usage` confunde las claves de pintura de MapLibre (`text-color`,
  `fill-color`, `to-number`) con clases de Tailwind: esas líneas llevan `lint-allow-token`.
