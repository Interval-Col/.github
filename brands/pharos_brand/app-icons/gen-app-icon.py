#!/usr/bin/env python3
"""Genera la baldosa de una app Pháros (la imagen del hub del SSO).

El contrato de abajo NO se invento: se MIDIO sobre las baldosas que ya estaban
en produccion (SSO ids 59 «Números», 62 «Pharos - LIS», 66 «Pharos - TI»), y los
tres acentos medidos coinciden al pixel con los de `../sub-brands/README.md`.

  lienzo   960x960, fondo blanco opaco
  chip     472x472 en (244,108), radio 108
  relleno  el acento de la sub-marca al 12,5 % sobre blanco
  glifo    lucide 24x24 — stroke = acento a plena fuerza, width 2, caps y joins
           redondos; centrado en (480,344); extension vertical 270 px, que es la
           que tienen ShipWheel (ERP) y Radar (LIS)
  pie      punto piloto + wordmark «Pháros» — constante de familia

POR QUE EL PIE SE COPIA Y NO SE TIPOGRAFIA: `_wordmark-strip.png` son los pixeles
reales de una baldosa existente. Re-componer «Pháros» con Fraunces dependeria de
que la fuente este instalada y de que el motor la rasterice igual; copiando la
franja, el pie es identico por construccion en cualquier maquina. Se verifico que
esa franja es la misma en las baldosas 59, 65 y 66.

Uso:
    pip install cairosvg pillow
    ./gen-app-icon.py movimiento.png "#004F70" sailboat

El glifo se pasa por nombre y se lee de lucide; para uno que lucide no traiga,
ver `../registry/app/lib/custom-glyphs.ts`.
"""
import io, json, os, re, sys
import cairosvg
from PIL import Image

CHIP_X, CHIP_Y, CHIP_W, CHIP_R = 244, 108, 472, 108
CX, CY, TARGET_H = 480, 344, 270
STRIP = os.path.join(os.path.dirname(__file__), '_wordmark-strip.png')
STRIP_Y = 600

# Trazos lucide usados hasta ahora. Anadir aqui al crear una baldosa nueva
# (copiar de node_modules/lucide-vue-next/dist/esm/icons/<nombre>.js, NO de memoria).
GLYPHS = {
    'sailboat': [
        "M10 2v15",
        "M7 22a4 4 0 0 1-4-4 1 1 0 0 1 1-1h16a1 1 0 0 1 1 1 4 4 0 0 1-4 4z",
        "M9.159 2.46a1 1 0 0 1 1.521-.193l9.977 8.98A1 1 0 0 1 20 13H4a1 1 0 0 1-.824-1.567z",
    ],
}

def wash(hexc, a=0.125):
    c = hexc.lstrip('#'); rgb = [int(c[i:i+2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(255 - a * (255 - v)) for v in rgb)

def _svg(paths, accent, box):
    d = '\n    '.join(f'<path d="{p}"/>' for p in paths)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="960" viewBox="0 0 960 960">
  <rect width="960" height="960" fill="#FFFFFF"/>
  <rect x="{CHIP_X}" y="{CHIP_Y}" width="{CHIP_W}" height="{CHIP_W}" rx="{CHIP_R}" ry="{CHIP_R}" fill="{wash(accent)}"/>
  <g transform="translate({CX - box/2},{CY - box/2}) scale({box/24.0})"
     fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    {d}
  </g>
</svg>'''

def _render(paths, accent, box):
    png = cairosvg.svg2png(bytestring=_svg(paths, accent, box).encode(),
                           output_width=960, output_height=960)
    return Image.open(io.BytesIO(png)).convert('RGB')

def _bbox(im, accent):
    c = accent.lstrip('#'); acc = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
    px = im.load()
    pts = [(x, y) for x in range(CHIP_X, CHIP_X+CHIP_W)
                  for y in range(CHIP_Y, CHIP_Y+CHIP_W) if px[x, y] == acc]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), max(xs), min(ys), max(ys)

def build(out, accent, glyph):
    paths = GLYPHS[glyph]
    box = 294.0
    for _ in range(12):                       # ajusta la caja hasta clavar TARGET_H
        im = _render(paths, accent, box)
        x0, x1, y0, y1 = _bbox(im, accent)
        h = y1 - y0 + 1
        if abs(h - TARGET_H) <= 1:
            break
        box *= TARGET_H / h
    im.paste(Image.open(STRIP).convert('RGB'), (0, STRIP_Y))
    im.save(out)
    open(os.path.splitext(out)[0] + '.svg', 'w').write(_svg(paths, accent, box))
    print(f"{out}  acento {accent}  wash {wash(accent)}  caja {box:.1f}px")
    print(f"  glifo x {x0}..{x1} ({x1-x0+1})  y {y0}..{y1} ({y1-y0+1})   (ERP y LIS: y 209..478)")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2], sys.argv[3])
