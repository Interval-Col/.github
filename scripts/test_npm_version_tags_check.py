#!/usr/bin/env python3
"""Pruebas de npm_version_tags_check.py. Corre con: python3 scripts/test_npm_version_tags_check.py"""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import npm_version_tags_check as c  # noqa: E402


def repo(tmp, archivos):
    r = pathlib.Path(tmp)
    for ruta, contenido in archivos.items():
        p = r / ruta
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(contenido))
    return r


class Etiquetas(unittest.TestCase):
    def test_etiquetas(self):
        for v in ("latest", "next", "beta", "canary", "*", "x", ""):
            self.assertTrue(c.es_etiqueta(v), v)

    def test_versiones_y_protocolos(self):
        for v in ("^3.5.35", "~5.0.7", "3.5.35", ">=4.2.0", "1.x", "workspace:*", "file:../lib",
                  "npm:vue@^3", "github:vuejs/core", "git+ssh://git@x/y.git", "https://x/y.tgz",
                  "vuejs/core#main", "catalog:"):
            self.assertFalse(c.es_etiqueta(v), v)


class Repo(unittest.TestCase):
    def correr(self, raiz, *flags):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = c.main(["x", str(raiz), *flags])
        return code, buf.getvalue()

    def test_aviso_no_falla(self):
        with tempfile.TemporaryDirectory() as t:
            r = repo(t, {"package.json": {"dependencies": {"vue": "latest"}}})
            code, out = self.correr(r)
            self.assertEqual(code, 0)
            self.assertIn("::warning", out)

    def test_enforce_falla(self):
        with tempfile.TemporaryDirectory() as t:
            r = repo(t, {"app/package.json": {"devDependencies": {"@nuxt/devtools": "latest"}}})
            code, out = self.correr(r, "--enforce")
            self.assertEqual(code, 1)
            self.assertIn("::error file=app/package.json", out)

    def test_limpio(self):
        with tempfile.TemporaryDirectory() as t:
            r = repo(t, {"package.json": {"dependencies": {"vue": "^3.5.35"}, "peerDependencies": {"vue": "*"}}})
            code, out = self.correr(r, "--enforce")
            self.assertEqual(code, 0)
            self.assertIn("Sin etiquetas", out)

    def test_ignora_node_modules(self):
        with tempfile.TemporaryDirectory() as t:
            r = repo(t, {"node_modules/x/package.json": {"dependencies": {"y": "latest"}},
                         "package.json": {"dependencies": {"vue": "^3.5.35"}}})
            self.assertEqual(c.hallazgos(r), [])


if __name__ == "__main__":
    unittest.main()
