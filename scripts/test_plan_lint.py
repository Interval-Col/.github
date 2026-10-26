"""Pruebas de plan_lint.py — por ahora, los avisos de la RFC 0040 (`talla`).

Correr: python3 scripts/test_plan_lint.py
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # no __pycache__ in the repo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_lint  # noqa: E402

FM = """---
status: active
owner: someone
created: 2026-10-26
updated: 2026-10-26
issue: Interval-Col/example#1
start: 2026-10-26
target: 2026-11-30
implementation: someone
{extra}
---

# Example plan · Plan de ejemplo

> **Resumen (ES).** Un plan de ejemplo.

{body}
"""

FICHA = "## Understanding · Entendimiento\n\nLa ficha.\n\n"
FASES_OK = "## Phase 1 — Build\n\n- [ ] **1.1** — x\n\n## Phase 2 — Delivery and stabilization · Entrega\n\n- [ ] **2.1** — y\n"
FASES_SIN_ENTREGA = "## Phase 1 — Build\n\n- [ ] **1.1** — x\n\n## Phase 2 — Polish\n\n- [ ] **2.1** — y\n"


def correr(extra, body, strict=False):
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "plans"))
        p = os.path.join(d, "plans", "ejemplo-plan.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(FM.format(extra=extra, body=body))
        out = io.StringIO()
        argv = sys.argv
        sys.argv = ["plan_lint.py"] + (["--strict"] if strict else []) + [p]
        try:
            with contextlib.redirect_stdout(out):
                code = plan_lint.main()
        finally:
            sys.argv = argv
        return code, out.getvalue()


class TallaRfc0040(unittest.TestCase):
    def test_sin_talla_no_mira(self):
        _, out = correr("", FASES_SIN_ENTREGA)
        self.assertNotIn("RFC 0040", out)

    def test_talla_s_no_pide_ficha(self):
        _, out = correr("talla: S", FASES_SIN_ENTREGA)
        self.assertNotIn("::notice", out)

    def test_talla_m_completo_no_avisa(self):
        _, out = correr("talla: M", FICHA + FASES_OK)
        self.assertNotIn("::notice", out)

    def test_talla_l_sin_ficha_avisa(self):
        _, out = correr("talla: L", FASES_OK)
        self.assertIn("no `## Understanding", out)

    def test_talla_m_sin_fase_de_entrega_avisa(self):
        _, out = correr("talla: M", FICHA + FASES_SIN_ENTREGA)
        self.assertIn("last phase is not delivery", out)

    def test_talla_invalida_avisa(self):
        _, out = correr("talla: XL", FICHA + FASES_OK)
        self.assertIn("sizes are S · M · L", out)

    def test_avisos_nunca_bloquean_en_strict(self):
        code, out = correr("talla: L", FASES_SIN_ENTREGA, strict=True)
        self.assertIn("::notice", out)
        self.assertEqual(code, 0, out)

    def test_avisos_no_cuentan_como_hallazgos(self):
        _, out = correr("talla: L", FASES_SIN_ENTREGA)
        self.assertIn("0 finding(s)", out)

    def test_encabezados_reales_del_estado(self):
        cuerpo = ("## Entendimiento · Understanding\n\nx\n\n### Phase 1 — Build\n\n"
                  "## 🚦 Fase 2 — Entrega y estabilización\n")
        _, out = correr("talla: M", cuerpo)
        self.assertNotIn("::notice", out)

    def test_fase_numerada_sin_entrega_avisa(self):
        _, out = correr("talla: L", FICHA + "## 1. Fase 0 — Base\n\n## 2. Fase 1 — Pulido\n")
        self.assertIn("last phase is not delivery", out)

    def test_cierre_con_otro_nombre_cuenta(self):
        _, out = correr("talla: M", FICHA + "## Phase 3 — Hypercare and handover\n")
        self.assertNotIn("::notice", out)

    def test_valor_entre_comillas(self):
        _, out = correr('talla: "M"', FICHA + FASES_OK)
        self.assertNotIn("::notice", out)

    def test_fase_dentro_de_un_bloque_de_codigo_no_cuenta(self):
        cuerpo = FICHA + FASES_OK + "\n```\n## Phase 9 — Example\n```\n"
        _, out = correr("talla: M", cuerpo)
        self.assertNotIn("::notice", out)

    def test_understanding_the_no_es_la_ficha(self):
        _, out = correr("talla: M", "## Understanding the legacy flow\n\n" + FASES_OK)
        self.assertIn("no `## Understanding", out)

    def test_excepcion_no_vuelve_hallazgo_el_aviso(self):
        code, out = correr("talla: L\nstandard-exception: framing doc in Spanish", FASES_SIN_ENTREGA, strict=True)
        self.assertIn("::notice", out)
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
