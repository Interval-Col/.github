# Baldosas de app — los iconos del hub del SSO

La imagen que cada app muestra en el hub de `apps.hematologico.com`. No son los
glifos de la UI: son PNG de 960×960 que viven en la columna `application.image`
de la base del SSO, en base64.

> ⚠️ **Existían sólo en esa base.** Si el SSO se restaura de cero, se pierden y no
> hay de dónde sacarlas. Esta carpeta es su respaldo y, sobre todo, la primera vez
> que el contrato de construcción queda escrito.

## El contrato

**Medido, no inventado.** Se dedujo de las baldosas que ya estaban en producción
—SSO ids 59 «Números», 62 «Pharos · LIS», 66 «Pharos · TI»— y los tres acentos
medidos coinciden **al píxel** con los de [`../sub-brands/README.md`](../sub-brands/README.md).

| | |
|---|---|
| Lienzo | 960×960, fondo **blanco opaco** |
| Chip | 472×472 en (244, 108), radio 108 |
| Relleno del chip | el acento de la sub-marca al **12,5 % sobre blanco** |
| Glifo | lucide 24×24 · stroke = acento a plena fuerza · width 2 · caps y joins redondos |
| Posición del glifo | centrado en (480, 344), extensión vertical **270 px** |
| Pie | punto piloto `#E4002B` + wordmark «Pháros» en Fraunces burgundy `#782F40` |

El 12,5 % sale de las tres medidas, no de una preferencia: ámbar `#7A5D00` → chip
`#EEEBDF`, teal `#1B6B5A` → `#E2ECEA`, navy `#002A52` → `#DFE4E9`. La misma
fórmula en las tres.

## Por qué el pie se copia en vez de tipografiarse

[`_wordmark-strip.png`](_wordmark-strip.png) son los **píxeles reales** de una
baldosa existente (`y ≥ 600`). Re-componer «Pháros» con Fraunces dependería de
que la fuente esté instalada y de que el motor la rasterice igual; copiando la
franja, el pie es idéntico **por construcción** en cualquier máquina.

Se verificó que esa franja es la misma en las baldosas 59, 65 y 66 — es una
constante de familia, no una decisión por app.

## Generar una

```bash
pip install cairosvg pillow
./gen-app-icon.py movimiento.png "#004F70" sailboat
```

El script **auto-ajusta** la caja del glifo hasta clavar los 270 px de extensión
vertical, así que no hay que calcular escalas a mano: se le da el acento y el
nombre del glifo.

⚠️ Los trazos se copian de `node_modules/lucide-vue-next/dist/esm/icons/<nombre>.js`,
**nunca de memoria**. Para un glifo que lucide no traiga, ver
[`../registry/app/lib/custom-glyphs.ts`](../registry/app/lib/custom-glyphs.ts).

## Subirla al SSO

`PUT /auth/v1/apps/update_app` con la imagen en base64.

🔴 **Ese endpoint reescribe también el `scope` de la app.** Hay que leer primero
con `GET /auth/v1/apps/get_app` y reenviar `route`, `method` e `is_api_route`
**tal cual**; si se omiten, se le corrompe a la app su ruta de entrada.

## Qué hay

| Archivo | Sub-marca | Acento |
|---|---|---|
| [`movimiento.png`](movimiento.png) · [`.svg`](movimiento.svg) | Pháros · Movimiento (Biuman) | `#004F70` |

Las demás baldosas Pháros que ya están en el SSO —Números, LIS, Clientes, TI,
Playgrounds— **todavía no están respaldadas aquí**. Conviene traerlas.

## Una discrepancia sin resolver

La baldosa **«Clientes»** (id 65) lleva un **ancla** en rosa `#ff3d63`. Según
[`../sub-brands/README.md`](../sub-brands/README.md) eso es **Admisiones / Pacientes**
(Muelle → `Anchor`); CRM / Clientes debería ser **Catalejo → `Telescope`** en ámbar
`#e37600`. O el app del SSO llamado «Clientes» es en realidad Admisiones, o se
cruzó el glifo. Queda anotado, sin tocar.
