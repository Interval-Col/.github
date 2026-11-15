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


OK = "# x\n\n## Tronco y ramas\n\n- Tronco: `develop`.\n\n## Reglas que obligan a este repo\n\n- RFC 0001.\n"
SIN_DEVELOP = lambda raiz: False  # noqa: E731
CON_DEVELOP = lambda raiz: True  # noqa: E731


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
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK, "@AGENTS.md\n"))[0], "conformant")

    def test_shim_con_comentario_debajo(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK, "@AGENTS.md\n\n<!-- por qué -->\n"))[0], "conformant")

    def test_sin_agents(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, None, "@AGENTS.md\n"))[0], "missing")

    def test_sin_claude(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK, None))[0], "missing")

    def test_claude_sin_la_linea(self):
        with tempfile.TemporaryDirectory() as t:
            estado, motivos = c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK, "# instrucciones viejas\nver AGENTS.md\n"))
            self.assertEqual(estado, "missing")
            self.assertIn("@AGENTS.md", motivos[0])

    def test_la_linea_tiene_que_estar_sola(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK, "lee @AGENTS.md antes\n"))[0], "missing")

    def test_sobre_presupuesto(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK + "x\n" * 200, "@AGENTS.md\n"))[0], "over-budget")

    def test_justo_en_el_presupuesto(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(remoto=SIN_DEVELOP, raiz=repo(t, OK + "x\n" * (200 - OK.count("\n")), "@AGENTS.md\n"))[0], "conformant")


    def test_shim_con_instrucciones_viejas(self):
        with tempfile.TemporaryDirectory() as t:
            estado, motivos = c.revisar(repo(t, OK, "@AGENTS.md\n\n# Viejo\n- usa pnpm\n"), SIN_DEVELOP)
            self.assertEqual(estado, "impure-shim")
            self.assertIn("2 línea", motivos[0])

    def test_plantilla_de_claude_es_pura(self):
        plantilla = pathlib.Path(__file__).parent.parent / "templates" / "CLAUDE.md"
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(c.revisar(repo(t, OK, plantilla.read_text()), SIN_DEVELOP)[0], "conformant")

    def test_plantilla_de_agents_trae_las_secciones(self):
        plantilla = (pathlib.Path(__file__).parent.parent / "templates" / "AGENTS.md").read_text()
        self.assertIsNotNone(c.seccion(plantilla, c.SECCION_TRONCO))
        self.assertIsNotNone(c.seccion(plantilla, c.SECCION_REGLAS))

    def test_sin_tronco_nombrado(self):
        with tempfile.TemporaryDirectory() as t:
            agents = OK.replace("- Tronco: `develop`.", "- Ramas cortas.")
            estado, motivos = c.revisar(repo(t, agents, "@AGENTS.md\n"), SIN_DEVELOP)
            self.assertEqual(estado, "missing")
            self.assertIn("tronco", motivos[0])

    def test_tronco_main_con_develop_en_el_remoto(self):
        with tempfile.TemporaryDirectory() as t:
            agents = OK.replace("`develop`", "**`main`** (rama por defecto)")
            estado, motivos = c.revisar(repo(t, agents, "@AGENTS.md\n"), CON_DEVELOP)
            self.assertEqual(estado, "missing")
            self.assertIn("promotes", motivos[0])

    def test_tronco_main_sin_develop_es_legitimo(self):
        with tempfile.TemporaryDirectory() as t:
            agents = OK.replace("`develop`", "`main`")
            self.assertEqual(c.revisar(repo(t, agents, "@AGENTS.md\n"), SIN_DEVELOP)[0], "conformant")

    def test_tronco_main_sin_poder_preguntar_no_falla(self):
        with tempfile.TemporaryDirectory() as t:
            agents = OK.replace("`develop`", "`main`")
            self.assertEqual(c.revisar(repo(t, agents, "@AGENTS.md\n"), lambda r: None)[0], "conformant")

    def test_secciones_en_ingles(self):
        with tempfile.TemporaryDirectory() as t:
            agents = "# x\n\n## Trunk and branches\n\n- Trunk: `main`.\n\n## Rules that bind this repo\n"
            self.assertEqual(c.revisar(repo(t, agents, "@AGENTS.md\n"), SIN_DEVELOP)[0], "conformant")

    def test_sin_seccion_de_reglas(self):
        with tempfile.TemporaryDirectory() as t:
            agents = OK.split("## Reglas")[0]
            estado, motivos = c.revisar(repo(t, agents, "@AGENTS.md\n"), SIN_DEVELOP)
            self.assertEqual(estado, "missing")
            self.assertIn("Reglas que obligan", motivos[0])


class Modos(unittest.TestCase):
    def correr(self, raiz, *flags):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            codigo = c.main([str(raiz), *flags], remoto=SIN_DEVELOP)
        return codigo, out.getvalue()

    def test_aviso_nunca_falla_y_dice_por_que(self):
        # Desde la promoción, el aviso solo existe porque el caller pasó `enforce: false`.
        with tempfile.TemporaryDirectory() as t:
            codigo, out = self.correr(repo(t))
            self.assertEqual(codigo, 0)
            self.assertIn("enforce: false", out)
            self.assertIn("::warning", out)

    def test_obligatorio_falla_si_no_conforma(self):
        with tempfile.TemporaryDirectory() as t:
            codigo, out = self.correr(repo(t), "--enforce")
            self.assertEqual(codigo, 1)
            self.assertIn("::error", out)

    def test_obligatorio_pasa_si_conforma(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.correr(repo(t, OK, "@AGENTS.md\n"), "--enforce")[0], 0)


if __name__ == "__main__":
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
