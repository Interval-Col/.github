"""Tests for the corpus chain: registry, mini-YAML and the v5 KB index builder.

    python3 -m unittest discover -s tests/corpus -v

Stdlib only (unittest), like the scripts under test.
"""

from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import corpus_lib  # noqa: E402
import kb_index  # noqa: E402
from corpus_lib import ParseError, RegistryError, load_registry, parse_yaml  # noqa: E402

REAL_REGISTRY = (REPO / "corpus-registry.yml").read_text(encoding="utf-8")

MINIMAL = textwrap.dedent("""\
    version: 1
    audiences: [publico, staff, servicio-al-cliente, ti, liderazgo]
    kbs:
      - id: kb-a
        repo: kb-a
        image: kb-a-site
        roots: [guias, comercial]
        recursive: true
        skip: [borrame, guias/viejo]
        url: site
        default_status: vigente
        liderazgo_areas: [comercial]
        audiences: [publico, staff, ti, liderazgo]
    consumers:
      - kb: kb-a
        app: app-a
        repo: app-a
        environments: [development]
        audiences: [staff, ti]
        mode: wait
    """)


def _kb(text: str = MINIMAL) -> dict:
    return load_registry(text)["kbs"]["kb-a"]


# ── mini-YAML ─────────────────────────────────────────────────────────


class ParseYamlTest(unittest.TestCase):
    def test_inline_lists_inside_list_items(self):
        out = parse_yaml("rows:\n  - id: x\n    audiences: [staff, ti]\n")
        self.assertEqual(out["rows"], [{"id": "x", "audiences": ["staff", "ti"]}])

    def test_hyphenated_keys_and_comments(self):
        out = parse_yaml('vigente-desde: 2026-09-27  # comment\nfuente: "a#b"\n')
        self.assertEqual(out, {"vigente-desde": "2026-09-27", "fuente": "a#b"})

    def test_hash_inside_a_value_is_not_a_comment(self):
        self.assertEqual(parse_yaml("fuente: public-web#1176\n")["fuente"], "public-web#1176")

    def test_deeper_nesting_is_an_error_not_a_guess(self):
        with self.assertRaises(ParseError):
            parse_yaml("a:\n  b:\n    c: 1\n")


# ── registry ──────────────────────────────────────────────────────────


class RegistryTest(unittest.TestCase):
    def test_the_real_registry_is_valid(self):
        reg = load_registry(REAL_REGISTRY)
        self.assertEqual(set(reg["kbs"]), {"biuman-kb", "lch-kb", "lch-admin-kb"})

    def test_d1_is_the_real_registrys_vocabulary(self):
        self.assertEqual(tuple(parse_yaml(REAL_REGISTRY)["audiences"]), corpus_lib.AUDIENCES)

    def test_no_real_consumer_mixes_publico_with_internal_tiers(self):
        for c in load_registry(REAL_REGISTRY)["consumers"]:
            if "publico" in c["audiences"]:
                self.assertEqual(c["audiences"], ["publico"], c)

    def test_a_changed_vocabulary_fails(self):
        bad = MINIMAL.replace("servicio-al-cliente, ti, ", "")
        with self.assertRaisesRegex(RegistryError, "D1"):
            load_registry(bad)

    def test_unknown_kb_bad_mode_and_mixed_public_grant_are_all_reported(self):
        bad = MINIMAL + (
            "  - kb: nope\n"
            "    app: app-b\n"
            "    repo: app-b\n"
            "    environments: [development]\n"
            "    audiences: [publico, staff]\n"
            "    mode: sometimes\n"
        )
        with self.assertRaises(RegistryError) as ctx:
            load_registry(bad)
        msg = str(ctx.exception)
        self.assertIn("unknown kb `nope`", msg)
        self.assertIn("mode must be one of", msg)
        self.assertIn("`publico` cannot share a grant", msg)

    def test_consumer_audience_outside_d1_fails(self):
        with self.assertRaisesRegex(RegistryError, "outside D1"):
            load_registry(MINIMAL.replace("audiences: [staff, ti]", "audiences: [staff, gerencia]"))

    def test_consumers_of_filters_by_mode(self):
        reg = load_registry(REAL_REGISTRY)
        waits = corpus_lib.consumers_of(reg, "biuman-kb", ("wait",))
        self.assertEqual([c["app"] for c in waits], ["admission-patient"])
        # lch-admin-kb → Admisiones went live on 2026-09-28, → Pháros TI on 2026-09-29.
        active = corpus_lib.consumers_of(reg, "lch-admin-kb", ("wait", "notify"))
        self.assertEqual([c["app"] for c in active], ["admission-patient", "pharos-ti"])


# ── v5 builder ────────────────────────────────────────────────────────


class BuildTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for area in ("guias", "comercial"):
            (self.root / area).mkdir()
        self.warnings: list[str] = []

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel: str, meta: str, body: str = "# Título\n\nCuerpo.\n") -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"---\n{textwrap.dedent(meta)}---\n{body}", encoding="utf-8")

    def build(self, kb: dict | None = None) -> dict:
        return kb_index.build(self.root, kb or _kb(), "abc123", warn=self.warnings.append)

    def by_slug(self, index: dict) -> dict:
        return {a["slug"]: a for a in index["articles"]}

    def test_a_bom_or_crlf_does_not_hide_the_frontmatter(self):
        # A draft saved by Notepad must stay a draft, not fall back to `vigente`.
        for name, raw in (("bom", "\ufeff---\ntitle: A\nstatus: borrador\n---\n# A\n\nx\n"),
                          ("crlf", "---\r\ntitle: A\r\nstatus: borrador\r\n---\r\n# A\r\n\r\nx\r\n")):
            (self.root / "guias" / f"{name}.md").write_bytes(raw.encode("utf-8"))
        idx = self.by_slug(self.build())
        self.assertEqual({a["status"] for a in idx.values()}, {"borrador"}, idx)

    def test_unknown_audience_fails_the_build(self):
        self.write("guias/a.md", "title: A\naudience: gerencia\n")
        with self.assertRaisesRegex(kb_index.KbError, "not in D1"):
            self.build()

    def test_audience_not_allowed_in_this_kb_fails(self):
        self.write("guias/a.md", "title: A\naudience: servicio-al-cliente\n")
        with self.assertRaisesRegex(kb_index.KbError, "not allowed in kb-a"):
            self.build()

    def test_every_problem_is_listed_not_just_the_first(self):
        self.write("guias/a.md", "audience: gerencia\n")
        self.write("guias/b.md", "audience: jefes\n")
        with self.assertRaises(kb_index.KbError) as ctx:
            self.build()
        self.assertIn("guias/a.md", str(ctx.exception))
        self.assertIn("guias/b.md", str(ctx.exception))

    def test_publico_on_a_draft_is_served_as_staff(self):
        self.write("guias/a.md", "audience: publico\nstatus: borrador\n")
        self.write("guias/b.md", "audience: publico\nstatus: vigente\n")
        idx = self.by_slug(self.build())
        self.assertEqual(idx["guias/a"]["audience"], "staff")
        self.assertEqual(idx["guias/b"]["audience"], "publico")
        self.assertEqual(len(self.warnings), 1)

    def test_default_audience_comes_from_the_area(self):
        self.write("guias/a.md", "title: A\n")
        self.write("comercial/b.md", "title: B\n")
        idx = self.by_slug(self.build())
        self.assertEqual(idx["guias/a"]["audience"], "staff")
        self.assertEqual(idx["comercial/b"]["audience"], "liderazgo")

    def test_ti_and_servicio_al_cliente_survive(self):
        kb = _kb(MINIMAL.replace("audiences: [publico, staff, ti, liderazgo]",
                                 "audiences: [staff, servicio-al-cliente, ti]"))
        self.write("guias/a.md", "audience: ti\n")
        self.write("guias/b.md", "audience: servicio-al-cliente\n")
        idx = self.by_slug(self.build(kb))
        self.assertEqual(idx["guias/a"]["audience"], "ti")
        self.assertEqual(idx["guias/b"]["audience"], "servicio-al-cliente")

    def test_verificacion_is_parsed_and_debe_citar_defaults_to_the_article(self):
        self.write("guias/a.md", textwrap.dedent("""\
            title: A
            verificacion:
              - pregunta: "¿Cuánto dura el bloqueo?"
                debe-decir: "5 minutos"
              - pregunta: "¿Dónde está la guía?"
                debe-citar: guias/otra
            """))
        [a] = self.build()["articles"]
        self.assertEqual(a["verificacion"], [
            {"pregunta": "¿Cuánto dura el bloqueo?", "debe_citar": "guias/a",
             "debe_decir": "5 minutos"},
            {"pregunta": "¿Dónde está la guía?", "debe_citar": "guias/otra", "debe_decir": ""},
        ])

    def test_verificacion_rejects_unknown_keys(self):
        self.write("guias/a.md", "verificacion:\n  - pregunta: x\n    debe-responder: y\n")
        with self.assertRaisesRegex(kb_index.KbError, "unknown key"):
            self.build()

    def test_content_hash_follows_the_body(self):
        self.write("guias/a.md", "title: A\n", "Uno.\n")
        h1 = self.build()["articles"][0]["content_hash"]
        self.write("guias/a.md", "title: A\n", "Dos.\n")
        h2 = self.build()["articles"][0]["content_hash"]
        self.assertTrue(h1.startswith("sha256:"))
        self.assertNotEqual(h1, h2)

    def test_links_outside_the_index_become_absolute(self):
        self.write("guias/a.md", "title: A\n", "[b](b.md) y [anexo](../anexos/x.md)\n")
        self.write("guias/b.md", "title: B\n")
        body = self.by_slug(self.build())["guias/a"]["body_md"]
        self.assertIn("[b](b.md)", body)
        self.assertIn("(https://github.com/Interval-Col/kb-a/blob/main/anexos/x.md)", body)

    def test_readme_skip_and_recursion(self):
        self.write("guias/README.md", "title: landing\n")
        self.write("guias/borrame.md", "title: x\n")
        self.write("guias/viejo.md", "title: x\n")
        self.write("guias/sub/hondo.md", "title: Hondo\n")
        self.assertEqual(list(self.by_slug(self.build())), ["guias/sub/hondo"])

    def test_an_empty_kb_is_a_failed_build(self):
        with self.assertRaisesRegex(kb_index.KbError, "zero articles"):
            self.build()

    def test_a_missing_root_fails(self):
        (self.root / "comercial").rmdir()
        with self.assertRaisesRegex(kb_index.KbError, "does not exist"):
            self.build()

    def test_index_envelope(self):
        self.write("guias/a.md", "title: A\n")
        idx = self.build()
        self.assertEqual(idx["version"], 5)
        self.assertEqual(idx["kb"], "kb-a")
        self.assertEqual(idx["source_commit"], "abc123")
        self.assertEqual(idx["audiences"], list(corpus_lib.AUDIENCES))
        self.assertEqual(idx["articles"][0]["url"], "/guias/a/")

    def test_compare_ignores_padding_and_reports_content(self):
        self.write("guias/a.md", "title: A\n")
        new = self.build()
        old = {"version": 2, "articles": [dict(new["articles"][0])]}
        old["articles"][0]["body_md"] = "\n" + old["articles"][0]["body_md"] + "\n"
        self.assertEqual(kb_index.compare(new, old), [])
        old["articles"][0]["title"] = "Otro"
        self.assertEqual(kb_index.compare(new, old), ["guias/a: `title` differs"])


if __name__ == "__main__":
    unittest.main()
