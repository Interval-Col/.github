#!/usr/bin/env python3
"""Tests for web_app_conformance.py — synthetic repos only."""

import pathlib
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import web_app_conformance as w  # noqa: E402

fallas = 0


def repo(archivos: dict[str, str]) -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp())
    for nombre, contenido in archivos.items():
        p = d / nombre
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contenido)
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(d), "add", "-A"], check=True)
    return d


def caso(nombre: str, archivos: dict[str, str], esperado: int, ignorar: list[str] | None = None) -> None:
    global fallas
    got = len(w.revisar(repo(archivos), ignorar or []))
    if got == esperado:
        print(f"ok    {nombre}")
    else:
        print(f"FALLA {nombre}: esperaba {esperado} hallazgo(s), salieron {got}")
        fallas += 1


NUXT = {"frontend/nuxt.config.ts": "export default defineNuxtConfig({})\n"}

caso("app Nuxt sin recursos externos: conforme", {**NUXT, "frontend/app/app.vue": "<template><div/></template>\n"}, 0)
caso("sin nuxt.config: un hallazgo", {"app/index.html": "<html><body></body></html>\n"}, 1)
caso("página que carga su librería de un CDN: dos hallazgos (sin Nuxt + script externo)",
     {"app/index.html": '<script src="https://cdn.example.org/lib.js"></script>\n'}, 2)
caso("hoja de estilos y fuente externas en un .vue",
     {**NUXT, "frontend/app/a.vue": '<link rel="stylesheet" href="https://fonts.example.com/x.css">\n<style>@import url("https://cdn.example.org/y.css");</style>\n'}, 2)
caso("URL sin esquema (//cdn…) también cuenta",
     {**NUXT, "frontend/app/a.vue": '<script src="//cdn.example.org/lib.js"></script>\n'}, 1)
caso("script del propio origen (ruta relativa): conforme",
     {**NUXT, "frontend/public/x.html": '<script src="/assets/lib.js"></script>\n'}, 0)
caso("excepción con motivo en la línea: se salta",
     {**NUXT, "frontend/app/a.vue": '<link href="https://sso.example.org/login"> <!-- conformance-allow: navegación al login, no un recurso -->\n'}, 0)
caso("--ignore deja fuera un prototipo local",
     {**NUXT, "app/index.html": '<script src="https://cdn.example.org/lib.js"></script>\n'}, 0, ignorar=["app/*"])
caso("node_modules nunca se mira",
     {**NUXT, "node_modules/pkg/index.html": '<script src="https://cdn.example.org/lib.js"></script>\n'}, 0)
caso("un enlace <a href> externo no es un recurso",
     {**NUXT, "frontend/app/a.vue": '<a href="https://example.org">sitio</a>\n'}, 0)

caso("docs/ queda fuera por defecto (una presentación no es la app)",
     {**NUXT, "apps/x/docs/slides.html": '<script src="https://cdn.example.org/lib.js"></script>\n'}, 0)

print(f"fallas={fallas}")
sys.exit(1 if fallas else 0)
