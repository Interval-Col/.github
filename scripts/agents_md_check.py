#!/usr/bin/env python3
"""Contrato de cada repo: AGENTS.md en la raíz + CLAUDE.md que lo importa (RFC 0039 D4).

Lo corre el workflow reutilizable `.github/workflows/agents-md-check.yml` sobre la
raíz del repo que lo llama. Reporta uno de tres estados:

- `missing`     — falta AGENTS.md, falta CLAUDE.md, o CLAUDE.md no tiene la línea
                  `@AGENTS.md` (sin ella Claude Code nunca carga AGENTS.md: el mapa
                  de ~/dev apaga su lectura nativa);
- `over-budget` — AGENTS.md pasa de MAX_LINEAS líneas;
- `conformant`  — todo en orden.

Nace en modo aviso, con fecha de promoción (RFC 0029): hasta FECHA_PROMOCION solo
anota; desde ahí, cada repo que llama al check pasa `enforce: true` y el check se
marca obligatorio (tarea 3.9 del plan del arnés).

Uso: agents_md_check.py [raíz] [--enforce]   → sale 1 solo con --enforce y sin conformar.
"""
import pathlib
import re
import sys

MAX_LINEAS = 200
FECHA_PROMOCION = "2026-11-10"


def revisar(raiz):
    """(estado, motivos) del repo en `raiz`."""
    raiz = pathlib.Path(raiz)
    agents, claude = raiz / "AGENTS.md", raiz / "CLAUDE.md"
    motivos = []
    if not agents.is_file():
        motivos.append("falta AGENTS.md en la raíz")
    if not claude.is_file():
        motivos.append("falta CLAUDE.md en la raíz (el puente con la línea `@AGENTS.md`)")
    elif not re.search(r"^\s*@AGENTS\.md\s*$", claude.read_text(encoding="utf-8", errors="replace"), re.M):
        motivos.append("CLAUDE.md no tiene una línea `@AGENTS.md`: Claude Code nunca carga AGENTS.md")
    if motivos:
        return "missing", motivos
    n = len(agents.read_text(encoding="utf-8", errors="replace").splitlines())
    if n > MAX_LINEAS:
        return "over-budget", [f"AGENTS.md tiene {n} líneas; el presupuesto es {MAX_LINEAS} "
                               "(el detalle va en docs/, enlazado)"]
    return "conformant", []


def main(argv):
    enforce = "--enforce" in argv
    args = [a for a in argv if not a.startswith("--")]
    estado, motivos = revisar(args[0] if args else ".")
    modo = "obligatorio" if enforce else f"aviso (se vuelve obligatorio el {FECHA_PROMOCION})"
    print(f"agents-md-check: {estado} · modo {modo}")
    for m in motivos:
        nivel = "error" if enforce else "warning"
        print(f"::{nivel} title=agents-md-check ({estado})::{m}")
    return 1 if enforce and estado != "conformant" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
