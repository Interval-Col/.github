"""chat-contract-check H11: a corpus-backed chat is registered and verified.

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import importlib.util
import os
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("ccc", REPO / "scripts/chat-contract-check.py")
ccc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ccc)

REGISTRY = textwrap.dedent("""\
    version: 1
    audiences: [publico, staff, servicio-al-cliente, ti, liderazgo]
    kbs:
      - id: kb-a
        repo: kb-a
        image: kb-a-site
        roots: [guias]
        url: site
        default_status: vigente
        audiences: [staff]
    consumers:
      - kb: kb-a
        app: live-app
        repo: live-app
        environments: [development]
        audiences: [staff]
        mode: wait
      - kb: kb-a
        app: future-app
        repo: future-app
        environments: [development]
        audiences: [staff]
        mode: planned
    """)

CALLER = """jobs:
  corpus-verify:
    uses: Interval-Col/.github/.github/workflows/corpus-verify.yml@main
"""


class H11Test(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.registry = self.root / "corpus-registry.yml"
        self.registry.write_text(REGISTRY, encoding="utf-8")
        self.wf = self.root / ".github/workflows"
        self.wf.mkdir(parents=True)
        self.embedder_ref = self.root / "org_kb_embedder.py"
        self.embedder_ref.write_text("# the org's embedder\n", encoding="utf-8")
        self.cwd = os.getcwd()
        os.chdir(self.root)

    def conformant(self, embedder_text="# the org's embedder\n"):
        (self.wf / "ci-cd.yml").write_text(CALLER, encoding="utf-8")
        (self.root / "ask.py").write_text("", encoding="utf-8")
        (self.root / "kb_embedder.py").write_text(embedder_text, encoding="utf-8")
        return dict(rag="on", corpus_app="live-app", ask_module="ask.py",
                    embedder="kb_embedder.py")

    def tearDown(self):
        os.chdir(self.cwd)
        self._tmp.cleanup()

    def h11(self, **manifest):
        results = []
        ccc.check_h11(manifest, results, registry_path=str(self.registry),
                      embedder_ref=str(self.embedder_ref))
        [(cid, status, detail)] = results
        self.assertEqual(cid, "H11")
        return status, detail

    def test_rag_off_is_info(self):
        self.assertEqual(self.h11(rag="off")[0], "INFO")

    def test_app_owned_corpus_is_info(self):
        self.assertEqual(self.h11(rag="on", corpus_app="none")[0], "INFO")

    def test_missing_corpus_app_warns(self):
        status, detail = self.h11(rag="on")
        self.assertEqual(status, "WARN")
        self.assertIn("corpus_app", detail)

    def test_unregistered_app_warns(self):
        status, detail = self.h11(rag="on", corpus_app="ghost")
        self.assertEqual(status, "WARN")
        self.assertIn("not a consumer", detail)

    def test_only_planned_edges_is_info(self):
        self.assertEqual(self.h11(rag="on", corpus_app="future-app")[0], "INFO")

    def test_live_edge_without_verify_or_ask_module_warns_with_both_reasons(self):
        status, detail = self.h11(rag="on", corpus_app="live-app")
        self.assertEqual(status, "WARN")
        self.assertIn("corpus-verify.yml", detail)
        self.assertIn("ask_module", detail)

    def test_conformant_app_passes(self):
        status, detail = self.h11(**self.conformant())
        self.assertEqual(status, "PASS", detail)

    def test_a_drifted_embedder_fails_even_unenforced(self):
        # One hotfix in the app's copy and nothing else would ever notice.
        status, detail = self.h11(**self.conformant("# the org's embedder\n# hotfix\n"))
        self.assertEqual(status, "FAIL")
        self.assertIn("NOT byte-identical", detail)

    def test_no_embedder_declared_warns(self):
        m = self.conformant()
        del m["embedder"]
        status, detail = self.h11(**m)
        self.assertEqual(status, "WARN")
        self.assertIn("embedder", detail)

    def test_a_commented_out_call_does_not_count(self):
        m = self.conformant()
        (self.wf / "ci-cd.yml").write_text(
            "jobs:\n  # corpus-verify:\n  #   uses: Interval-Col/.github/.github/workflows/"
            "corpus-verify.yml@main\n", encoding="utf-8")
        status, detail = self.h11(**m)
        self.assertEqual(status, "WARN")
        self.assertIn("corpus-verify.yml", detail)

    def test_enforced_flips_to_fail(self):
        try:
            ccc.H11_ENFORCED = True
            self.assertEqual(self.h11(rag="on")[0], "FAIL")
        finally:
            ccc.H11_ENFORCED = False

    def test_unreachable_registry_warns_instead_of_guessing(self):
        self.registry.unlink()
        status, detail = self.h11(rag="on", corpus_app="live-app")
        self.assertEqual(status, "WARN")
        self.assertIn("not reachable", detail)

    def test_the_real_registry_knows_the_rag_apps(self):
        results = []
        ccc.check_h11({"rag": "on", "corpus_app": "admission-patient"}, results)
        self.assertNotIn("not a consumer", results[0][2])


if __name__ == "__main__":
    unittest.main()
