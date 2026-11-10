#!/usr/bin/env python3
"""Flag dependencies declared with a dist-tag (`latest`, `next`, `*`…) instead of a version range.

A dist-tag is not a version: the lockfile holds it only until someone runs `pnpm add` or the
lockfile is rewritten, and then the package manager resolves «the newest one today» — a new
major included, with nobody having asked for it. The Nuxt starter template ships
`"vue": "latest"` and `"vue-router": "latest"`, so every app born from it inherits the trap.

Scans every tracked `package.json` (never `node_modules`), only in `dependencies` and
`devDependencies`. `peerDependencies` is left alone: a library may legitimately accept `*`.
Protocols are fine (`workspace:`, `file:`, `link:`, `npm:` aliases, git and http URLs).

Usage: npm_version_tags_check.py <repo-root> [--enforce]
  Without --enforce it only annotates (warning mode); with it, it exits 1 on a finding.
"""

import json
import pathlib
import re
import subprocess
import sys

SECCIONES = ("dependencies", "devDependencies")
PROTOCOLO = re.compile(r"^(workspace:|file:|link:|portal:|patch:|npm:|github:|git(\+\w+)?:|https?:|catalog:)")
# A bare word (`latest`, `next`, `beta`, `canary`…) is a dist-tag; `*`, `x` and "" mean «anything».
ETIQUETA = re.compile(r"^(\*|x|X|[A-Za-z][\w.-]*)$")


def es_etiqueta(valor) -> bool:
    if not isinstance(valor, str):
        return False
    v = valor.strip()
    if v == "":
        return True
    if PROTOCOLO.match(v) or "/" in v:  # `owner/repo` is a GitHub shorthand, not a tag
        return False
    return bool(ETIQUETA.match(v))


def package_jsons(raiz: pathlib.Path) -> list[pathlib.Path]:
    try:
        out = subprocess.run(["git", "-C", str(raiz), "ls-files", "*package.json"],
                             capture_output=True, text=True, check=True).stdout.split()
        archivos = [raiz / p for p in out]
    except (OSError, subprocess.CalledProcessError):  # not a git checkout: walk the tree
        archivos = list(raiz.rglob("package.json"))
    return sorted(p for p in archivos if "node_modules" not in p.parts and p.name == "package.json")


def hallazgos(raiz: pathlib.Path) -> list[tuple[str, str, str, str]]:
    out = []
    for p in package_jsons(raiz):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # a broken package.json is another check's business
        for sec in SECCIONES:
            for dep, valor in (data.get(sec) or {}).items():
                if es_etiqueta(valor):
                    out.append((str(p.relative_to(raiz)), sec, dep, valor))
    return out


def main(argv: list[str]) -> int:
    raiz = pathlib.Path(argv[1] if len(argv) > 1 and not argv[1].startswith("--") else ".")
    enforce = "--enforce" in argv
    encontrados = hallazgos(raiz)
    nivel = "error" if enforce else "warning"
    for ruta, sec, dep, valor in encontrados:
        print(f"::{nivel} file={ruta}::{sec}.{dep} = \"{valor}\" es una etiqueta, no una versión. "
              f"Usa el rango de la versión que ya tiene el lockfile (p. ej. \"^3.5.35\").")
    if encontrados:
        print(f"{len(encontrados)} dependencia(s) con etiqueta en vez de versión"
              + ("" if enforce else " (modo aviso: no falla el check)."))
    else:
        print("Sin etiquetas: todas las dependencias declaran un rango de versión.")
    return 1 if (encontrados and enforce) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
