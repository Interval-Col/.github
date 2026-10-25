#!/usr/bin/env python3
"""Pruebas de agents_md_check.py. Corre con: python3 scripts/test_agents_md_check.py"""
import contextlib
import io
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import agents_md_check as c  # noqa: E402


def repo(tmp, agents=None, claude=None):
    r = pathlib.Path(tmp)
    if agents is not None:
        (r / "AGENTS.md").write_text(agents)
    if claude is not None:
        (r / "CLAUDE.md").write_text(claude)
    return r


class Estados(unittest.TestCase):
    def test_conforme(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "# x\n", "@AGENTS.md\n"))[0], "conformant")

    def test_shim_con_comentario_debajo(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "# x\n", "@AGENTS.md\n\n<!-- por qué -->\n"))[0], "conformant")

    def test_sin_agents(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, None, "@AGENTS.md\n"))[0], "missing")

    def test_sin_claude(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "# x\n", None))[0], "missing")

    def test_claude_sin_la_linea(self):
        with tempfile.TemporaryDirectory() as t:
            estado, motivos = c.revisar(repo(t, "# x\n", "# instrucciones viejas\nver AGENTS.md\n"))
            self.assertEqual(estado, "missing")
            self.assertIn("@AGENTS.md", motivos[0])

    def test_la_linea_tiene_que_estar_sola(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "# x\n", "lee @AGENTS.md antes\n"))[0], "missing")

    def test_sobre_presupuesto(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "x\n" * 201, "@AGENTS.md\n"))[0], "over-budget")

    def test_justo_en_el_presupuesto(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, "x\n" * 200, "@AGENTS.md\n"))[0], "conformant")


class Modos(unittest.TestCase):
    def correr(self, raiz, *flags):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            codigo = c.main([str(raiz), *flags])
        return codigo, out.getvalue()

    def test_aviso_nunca_falla_y_dice_la_fecha(self):
        with tempfile.TemporaryDirectory() as t:
            codigo, out = self.correr(repo(t))
            self.assertEqual(codigo, 0)
            self.assertIn(c.FECHA_PROMOCION, out)
            self.assertIn("::warning", out)

    def test_obligatorio_falla_si_no_conforma(self):
        with tempfile.TemporaryDirectory() as t:
            codigo, out = self.correr(repo(t), "--enforce")
            self.assertEqual(codigo, 1)
            self.assertIn("::error", out)

    def test_obligatorio_pasa_si_conforma(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.correr(repo(t, "# x\n", "@AGENTS.md\n"), "--enforce")[0], 0)


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
