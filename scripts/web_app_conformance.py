#!/usr/bin/env python3
"""Minimal conformance of a deployable web app with the org frontend standard.

A repo that calls the `web-app-conformance` workflow declares itself a deployable web app.
Three things are measured, from ENGINEERING_STANDARDS.md:

1. **The frontend is Nuxt.** At least one tracked `nuxt.config.ts` (or `.js`/`.mjs`) exists.
   A hand-written HTML page served as the app is not the standard, however small.
2. **No third-party assets at runtime.** No tracked `.html`, `.vue` or `nuxt.config.*` loads a
   script, stylesheet or font from an absolute `http(s)://` URL. Assets come from the app's own
   origin (bundled by the build, or served by its own backend). A third-party CDN at runtime
   is a supply-chain dependency that no lockfile pins and no review sees.
3. **The layout is `frontend/` + `backend/`.** Each `nuxt.config.*` sits in a folder named
   `frontend` and each FastAPI entrypoint (`app/main.py`) under one named `backend`, at the root
   or nested in a monorepo (`<app>/frontend`). Names that vary per repo break every tool and
   document that assumes them.

Why it exists: until it, nothing measured the frontend standard, so a green CI said nothing about
it — a repo born after the standards were written inherits none of them by itself.

Exceptions: a line carrying `conformance-allow:` followed by a reason is skipped (for example a
link to the SSO login page, which is navigation, not an asset). `--ignore <glob>` skips paths
that are not served (local prototypes, fixtures); repeat it as needed. `docs/` is skipped
by default: documentation is not served as the app. Tracked files only,
never `node_modules`.

Usage: web_app_conformance.py <repo-root> [--enforce] [--ignore <glob> ...]
  Without --enforce it only annotates (warning mode); with it, it exits 1 on a finding.
"""

import fnmatch
import pathlib
import re
import subprocess
import sys

NUXT_CONFIG = re.compile(r"(^|/)nuxt\.config\.(ts|js|mjs)$")
MIRADOS = re.compile(r"\.(html|vue)$|(^|/)nuxt\.config\.(ts|js|mjs)$")
# <script src="https://…">, <link href="https://…"> (stylesheets, fonts, preloads),
# @import url("https://…") and @import "https://…".
EXTERNO = re.compile(
    r"""<script\b[^>]*\bsrc\s*=\s*["']?(https?:)?//"""
    r"""|<link\b[^>]*\bhref\s*=\s*["']?(https?:)?//"""
    r"""|@import\s+(url\(\s*)?["']?(https?:)?//""",
    re.IGNORECASE,
)
PERMISO = "conformance-allow:"
ENTRADA_BACKEND = re.compile(r"(^|/)app/main\.py$")
# Documentation is not served as the app (slides, guides): skipped by default.
IGNORADOS_POR_DEFECTO = ("docs/*", "*/docs/*")


def archivos(raiz: pathlib.Path) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(raiz), "ls-files"], capture_output=True, text=True, check=True)
        nombres = out.stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        nombres = [str(p.relative_to(raiz)) for p in raiz.rglob("*") if p.is_file()]
    return [n for n in nombres if "node_modules/" not in n]


def ignorado(ruta: str, patrones: list[str]) -> bool:
    return any(fnmatch.fnmatch(ruta, p) for p in patrones)


def revisar(raiz: pathlib.Path, ignorar: list[str]) -> list[str]:
    hallazgos: list[str] = []
    patrones = [*IGNORADOS_POR_DEFECTO, *ignorar]
    nombres = [n for n in archivos(raiz) if not ignorado(n, patrones)]
    if not any(NUXT_CONFIG.search(n) for n in nombres):
        hallazgos.append(
            "::sin-nuxt:: no tracked nuxt.config.* — a deployable web app is Nuxt "
            "(ENGINEERING_STANDARDS.md § Frontend)"
        )
    for n in nombres:
        if NUXT_CONFIG.search(n) and pathlib.PurePosixPath(n).parent.name != "frontend":
            hallazgos.append(f"{n}:1: the frontend lives in a folder named frontend/ (ENGINEERING_STANDARDS.md)")
        if ENTRADA_BACKEND.search(n) and pathlib.PurePosixPath(n).parent.parent.name != "backend":
            hallazgos.append(f"{n}:1: the backend lives in a folder named backend/ (ENGINEERING_STANDARDS.md)")
    for n in nombres:
        if not MIRADOS.search(n):
            continue
        try:
            lineas = (raiz / n).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, linea in enumerate(lineas, 1):
            if PERMISO in linea:
                continue
            if EXTERNO.search(linea):
                hallazgos.append(f"{n}:{i}: third-party asset at runtime (script/stylesheet/font from an absolute URL)")
    return hallazgos


def main(argv: list[str]) -> int:
    args = argv[1:]
    enforce = "--enforce" in args
    ignorar: list[str] = []
    resto: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--ignore" and i + 1 < len(args):
            ignorar.append(args[i + 1])
            i += 2
            continue
        if args[i] != "--enforce":
            resto.append(args[i])
        i += 1
    raiz = pathlib.Path(resto[0] if resto else ".").resolve()
    hallazgos = revisar(raiz, ignorar)
    nivel = "error" if enforce else "warning"
    for h in hallazgos:
        if h.startswith("::sin-nuxt::"):
            print(f"::{nivel} title=web-app-conformance::{h.removeprefix('::sin-nuxt:: ')}")
        else:
            ruta, _, resto_h = h.partition(":")
            linea, _, msg = resto_h.partition(":")
            print(f"::{nivel} file={ruta},line={linea},title=web-app-conformance::{msg.strip()}")
    if not hallazgos:
        print("Conforme: frontend en Nuxt, estructura frontend/ + backend/ y sin recursos de terceros en tiempo de ejecución.")
        return 0
    print(f"{len(hallazgos)} hallazgo(s) de conformidad del frontend.")
    return 1 if enforce else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
