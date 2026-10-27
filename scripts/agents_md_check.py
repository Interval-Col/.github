#!/usr/bin/env python3
"""Contrato de cada repo: AGENTS.md en la raíz + CLAUDE.md que lo importa (RFC 0039 D4).

Lo corre el workflow reutilizable `.github/workflows/agents-md-check.yml` sobre la
raíz del repo que lo llama. Reporta uno de tres estados:

- `missing`     — falta AGENTS.md, falta CLAUDE.md, CLAUDE.md no tiene la línea
                  `@AGENTS.md` (sin ella Claude Code nunca carga AGENTS.md: el mapa
                  de ~/dev apaga su lectura nativa), o a AGENTS.md le falta una
                  sección obligatoria: «Tronco y ramas» con el tronco nombrado, y
                  «Reglas que obligan a este repo» (RFC 0039 D4);
- `impure-shim` — CLAUDE.md trae algo más que `@AGENTS.md` y comentarios: esas
                  instrucciones viejas siguen cargando y contradicen a AGENTS.md;
- `over-budget` — AGENTS.md pasa de MAX_LINEAS líneas;
- `conformant`  — todo en orden.

Si AGENTS.md declara `main`/`master` como tronco y el remoto tiene una rama
`develop`, también es `missing`: así se salió pharos-telephony del estándar
(2026-08-10 → 2026-10-24, 34 PRs directo a `main`). Sin acceso al remoto, esa
comprobación se salta.

Nació en modo aviso, con fecha de promoción (RFC 0029): hasta FECHA_PROMOCION solo
anotaba. Desde esa fecha el workflow reutilizable pasa `--enforce` por defecto y el
check es obligatorio (tarea 3.9 del plan del arnés).

Uso: agents_md_check.py [raíz] [--enforce]   → sale 1 solo con --enforce y sin conformar.
"""
import pathlib
import re
import subprocess
import sys

MAX_LINEAS = 200
FECHA_PROMOCION = "2026-11-10"


SECCION_TRONCO = re.compile(r"^##\s+(Tronco y ramas|Trunk and branches)\s*$", re.M | re.I)
SECCION_REGLAS = re.compile(r"^##\s+(Reglas que obligan a este repo|Rules that bind this repo)\s*$",
                            re.M | re.I)
LINEA_TRONCO = re.compile(r"^\s*-\s*(?:Tronco|Trunk)\b[^\n`]*`(develop|main|master)`", re.M | re.I)


def seccion(texto, cabecera):
    """Cuerpo de la sección `## …` que casa con `cabecera`, o None."""
    m = cabecera.search(texto)
    if not m:
        return None
    sigue = re.search(r"^## ", texto[m.end():], re.M)
    return texto[m.end(): m.end() + sigue.start()] if sigue else texto[m.end():]


def tiene_develop(raiz):
    """True/False si el remoto `origin` tiene `develop`; None si no se pudo preguntar."""
    try:
        r = subprocess.run(["git", "-C", str(raiz), "ls-remote", "--heads", "origin", "develop"],
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return bool(r.stdout.strip()) if r.returncode == 0 else None


def revisar(raiz, remoto=tiene_develop):
    """(estado, motivos) del repo en `raiz`."""
    raiz = pathlib.Path(raiz)
    agents, claude = raiz / "AGENTS.md", raiz / "CLAUDE.md"
    motivos = []
    texto_claude = claude.read_text(encoding="utf-8", errors="replace") if claude.is_file() else None
    if not agents.is_file():
        motivos.append("falta AGENTS.md en la raíz")
    if texto_claude is None:
        motivos.append("falta CLAUDE.md en la raíz (el puente con la línea `@AGENTS.md`)")
    elif not re.search(r"^\s*@AGENTS\.md\s*$", texto_claude, re.M):
        motivos.append("CLAUDE.md no tiene una línea `@AGENTS.md`: Claude Code nunca carga AGENTS.md")
    if agents.is_file():
        texto = agents.read_text(encoding="utf-8", errors="replace")
        tronco = seccion(texto, SECCION_TRONCO)
        m = LINEA_TRONCO.search(tronco) if tronco is not None else None
        if m is None:
            motivos.append("AGENTS.md no nombra su tronco: falta «## Tronco y ramas» con una línea "
                           "«- Tronco: `develop`» (o `main`). Sin ella un PR sin `--base` cae en la "
                           "rama por defecto")
        elif m.group(1).lower() != "develop" and remoto(raiz):
            motivos.append(f"AGENTS.md declara `{m.group(1)}` como tronco, pero el remoto tiene "
                           "`develop`: en la org el trabajo entra a `develop` y a `main` solo llegan "
                           "promotes")
        if seccion(texto, SECCION_REGLAS) is None:
            motivos.append("falta la sección «## Reglas que obligan a este repo» (RFC 0039 D4): una "
                           "línea por cada RFC aceptada que nombra al repo")
    if motivos:
        return "missing", motivos
    sobra = re.sub(r"<!--.*?-->", "", texto_claude, flags=re.S)
    sobra = [l for l in sobra.splitlines() if l.strip() and l.strip() != "@AGENTS.md"]
    if sobra:
        return "impure-shim", [f"CLAUDE.md trae {len(sobra)} línea(s) además de `@AGENTS.md`: "
                               "siguen cargando en cada sesión. Muévelas a AGENTS.md"]
    n = len(texto.splitlines())
    if n > MAX_LINEAS:
        return "over-budget", [f"AGENTS.md tiene {n} líneas; el presupuesto es {MAX_LINEAS} "
                               "(el detalle va en docs/, enlazado)"]
    return "conformant", []


def main(argv, remoto=tiene_develop):
    enforce = "--enforce" in argv
    args = [a for a in argv if not a.startswith("--")]
    estado, motivos = revisar(args[0] if args else ".", remoto)
    modo = "obligatorio" if enforce else f"aviso (se vuelve obligatorio el {FECHA_PROMOCION})"
    print(f"agents-md-check: {estado} · modo {modo}")
    for m in motivos:
        nivel = "error" if enforce else "warning"
        print(f"::{nivel} title=agents-md-check ({estado})::{m}")
    return 1 if enforce and estado != "conformant" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
