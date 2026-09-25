#!/usr/bin/env python3
"""Genera `registry/prompts/sol_persona.py` desde `SOL.md` §6/§7.

🔴 **Por qué existe.** Hasta el 2026-09-20 ese fichero se mantenía «en sincronía a
mano» —lo dice su propio docstring— y la sincronía no ocurrió: quedó con el texto
anterior al fallo del 2026-09-08 («tratas a la persona de usted, siempre»)
mientras el canon ya decía que Sol tutea. Nadie lo notó porque H9 sólo verificaba
`persona: nerea`; para `sol` el checker respondía «app-owned, nothing to verify».

🔑 **La lección, que es la que este script encarna:** dos originales del mismo
texto siempre divergen. El markdown es la fuente; el `.py` es una proyección.

⚠️ Nerea tiene el suyo generado por `design-studio` (vista /nerea → «Exportar al
registry»). Ese pipeline está cableado a Nerea y parametrizarlo se defirió hasta
que existiera una tercera persona (regla de tres, RFC 0020). Este script es el
equivalente mínimo para Sol, con el **mismo formato y el mismo `persona-stamp`**,
para que H9 pueda tratar a las dos igual. El día que design-studio se parametrice,
esto se retira.

Uso:
    python3 scripts/generar-persona-sol.py            # escribe
    python3 scripts/generar-persona-sol.py --check     # sólo verifica (CI)
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import textwrap
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CANON = RAIZ / "brands" / "pharos_brand" / "SOL.md"
DESTINO = RAIZ / "brands" / "pharos_brand" / "registry" / "prompts" / "sol_persona.py"

#: Ancho del prompt. El de Nerea va a ~74; se iguala para que un diff entre los
#: dos ficheros muestre diferencias de CONTENIDO y no de envoltura.
ANCHO = 74


def _entre(md: str, abre: str, cierra: str) -> str:
    """El texto entre dos marcadores HTML del canon.

    🪤 Falla RUIDOSAMENTE si un marcador no está: un marcador renombrado daría
    un bloque vacío, y un prompt vacío es un asistente sin personaje — que es
    exactamente el fallo que nadie nota hasta que un paciente lo ve.
    """
    try:
        i = md.index(abre) + len(abre)
        j = md.index(cierra)
    except ValueError as exc:  # noqa: TRY003
        raise SystemExit(
            f"✗ No encontré el marcador {abre!r} o {cierra!r} en {CANON.name}. "
            "Si se renombraron, este script hay que actualizarlo — no se puede "
            "generar un personaje a medias."
        ) from exc
    bloque = md[i:j].strip()
    if not bloque:
        raise SystemExit(f"✗ El bloque entre {abre!r} y {cierra!r} está vacío.")
    return bloque


def _prompt(persona_md: str) -> str:
    """El blockquote del §6, convertido a texto llano y re-envuelto.

    El canon lo escribe como cita con negritas para que se lea en GitHub; el
    prompt no lleva markdown — un `**` dentro del system prompt es ruido que el
    modelo puede imitar.
    """
    plano = " ".join(linea.lstrip("> ").strip() for linea in persona_md.splitlines())
    plano = re.sub(r"\*\*(.+?)\*\*", r"\1", plano)
    return "\n".join(textwrap.wrap(" ".join(plano.split()), ANCHO))


def _copy(copys_md: str, clave: str) -> str:
    m = re.search(rf"\*\*{clave}:\*\*\s*«(.+?)»", copys_md, re.S)
    if not m:
        raise SystemExit(f"✗ No encontré el micro-copy {clave!r} en §7 de {CANON.name}.")
    return " ".join(m.group(1).split())


def _literal(texto: str) -> str:
    """Un literal de Python legible: una línea si cabe, concatenado si no."""
    if len(texto) <= 72:
        return '"' + texto.replace('"', '\\"') + '"'
    lineas = textwrap.wrap(texto, 70)
    cuerpo = "\n    ".join(f'"{l.replace(chr(34), chr(92) + chr(34))} "' for l in lineas)
    return "(\n    " + cuerpo.rstrip().rstrip('"').rstrip() + '"\n)'


def construir() -> str:
    md = CANON.read_text(encoding="utf-8")
    persona_md = _entre(md, "<!-- sol:persona -->", "<!-- /sol:persona -->")
    copys_md = _entre(md, "<!-- sol:copys -->", "<!-- /sol:copys -->")
    persona = _prompt(persona_md)
    stamp = hashlib.sha256((persona_md + copys_md).encode("utf-8")).hexdigest()[:8]
    saludo = _copy(copys_md, "Saludo")
    no_se = _copy(copys_md, "No sé")
    despedida = _copy(copys_md, "Despedida")

    return f'''"""Sol — bloque canónico de persona para el system prompt (chat-contract H9).

GENERADO desde brands/pharos_brand/SOL.md (§6 persona · §7 micro-copys) por
scripts/generar-persona-sol.py. NO editar a mano — regenerar.
persona-stamp: {stamp}

🔴 **Por qué esto se genera y ya no se escribe a mano.** Hasta el 2026-09-20 este
archivo se mantenía «en sincronía a mano», y la sincronía no ocurrió: quedó con el
texto anterior al fallo del 2026-09-08 —«tratas a la persona de usted, siempre»—
mientras el canon ya decía que Sol tutea. Nadie lo notó porque H9 sólo verificaba
`persona: nerea`; para `sol` el checker respondía «app-owned, nothing to verify».
⇒ Dos originales del mismo texto siempre divergen. Ahora hay uno.

Sol es la asistente de las superficies PÚBLICAS —paciente y cliente—; Nerea es la
de las superficies internas. Misma casa y mismos límites (SOL.md §4 hereda
NEREA.md §4 sin excepción); lo que cambia es el CORPUS y el encuadre, no el trato:
las dos tutean.

Cada app compone `SYSTEM_PROMPT = SOL_PERSONA + <bloque local>` — el personaje es
compartido, el corpus/rol es por app (CH7, RFC 0017). NO editar la copia
sincronizada en una app: se propaga con
`sync-pharos-registry.sh --persona-dir <backend-chat-dir>` y H9 exige que
coincida byte a byte con esta copia canónica.
"""

SOL_PERSONA = """\\
{persona}
"""

# Micro-copys canónicos (SOL.md §7), en tú. El «no sé» lleva [persona/canal] —
# cada app lo concreta a su realidad, nunca el tono.
SOL_SALUDO = {_literal(saludo)}
SOL_NO_SE = {_literal(no_se)}
SOL_DESPEDIDA = {_literal(despedida)}
'''


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="no escribe; falla si está desfasado")
    args = ap.parse_args()

    nuevo = construir()
    actual = DESTINO.read_text(encoding="utf-8") if DESTINO.exists() else ""
    if nuevo == actual:
        print(f"✓ {DESTINO.relative_to(RAIZ)} está al día con {CANON.name}")
        return 0
    if args.check:
        print(
            f"✗ {DESTINO.relative_to(RAIZ)} NO coincide con {CANON.name}.\n"
            "  Corre `python3 scripts/generar-persona-sol.py` y commitea el resultado.\n"
            "  🔑 Si editaste el .py a mano, ese cambio se pierde: la fuente es el markdown."
        )
        return 1
    DESTINO.write_text(nuevo, encoding="utf-8")
    print(f"✓ {DESTINO.relative_to(RAIZ)} regenerado desde {CANON.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
