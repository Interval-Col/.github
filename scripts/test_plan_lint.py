"""Pruebas de plan_lint.py — por ahora, los avisos de la RFC 0040 (`talla`).

Correr: python3 scripts/test_plan_lint.py
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()
