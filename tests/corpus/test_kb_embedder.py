"""kb_embedder: the one embedder every Nerea uses (plan task 3.1).

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "brands/pharos_brand/registry/corpus"))

import kb_embedder as ke  # noqa: E402


def art(slug, audience="staff", status="vigente", body="texto", area="guias", h=""):
    a = {"slug": slug, "audience": audience, "status": status, "body_md": body, "area": area}
    if h:
        a["content_hash"] = h
    return a


class FakeStore:
    def __init__(self):
        self.replaced, self.pruned, self.foreign = [], [], []

    def replace(self, article, chunks, vectors):
        self.replaced.append(f"{article.kb}:{article.slug}")

    def prune(self, kb, keep):
        self.pruned.append((kb, sorted(keep)))
        return 0

    def prune_foreign(self, kbs):
        self.foreign.append(sorted(kbs))
        return 0


def ok_embed(texts):
    return [[0.0] for _ in texts], 5


class SelectTest(unittest.TestCase):
    def test_only_vigente_and_granted(self):
        idx = {"articles": [
            art("sac/portal", "servicio-al-cliente", h="sha256:x"),
            art("ti/portal", "ti"),
            art("lex", "staff", status="borrador"),
            art("jefes", "liderazgo"),
        ]}
        s = ke.select(idx, "lch-admin-kb", ["staff", "servicio-al-cliente"])
        self.assertEqual([a.slug for a in s.articles], ["sac/portal"])
        self.assertEqual(s.articles[0].content_hash, "sha256:x")
        self.assertEqual((s.total, s.skipped_status, s.skipped_audience), (4, 1, 2))

    def test_unknown_audience_is_skipped_missing_takes_area_fallback(self):
        idx = {"articles": [art("x", "ti-interno"), {"slug": "y", "status": "vigente",
                                                    "area": "comercial", "body_md": "b"},
                            {"slug": "z", "status": "vigente", "area": "guias", "body_md": "b"}]}
        s = ke.select(idx, "kb", ["staff", "liderazgo"])
        self.assertEqual([(a.slug, a.audience) for a in s.articles],
                         [("y", "liderazgo"), ("z", "staff")])

    def test_emails_are_scrubbed_but_hash_is_of_the_original(self):
        s = ke.select({"articles": [art("x", body="escribe a a@b.co")]}, "kb", ["staff"])
        self.assertNotIn("@", s.articles[0].body)
        self.assertEqual(s.articles[0].content_hash, ke.content_hash("escribe a a@b.co"))

    def test_metadata_shape(self):
        a = ke.Article("lch-admin-kb", "s", "area", "staff", "sha256:h", "b")
        self.assertEqual(ke.metadata(a, 3, "lch"), {
            "chunk_index": 3, "area": "area", "audience": "staff", "kb": "lch-admin-kb",
            "content_hash": "sha256:h", "tenant": "lch"})


class CorpusTest(unittest.TestCase):
    def test_parse_corpus(self):
        c = ke.parse_corpus('{"biuman-kb": {"url": "http://b", "audiences": ["staff"]}}')
        self.assertEqual(c, {"biuman-kb": {"url": "http://b", "audiences": ["staff"]}})
        self.assertEqual(ke.parse_corpus(""), {})
        with self.assertRaises(ValueError):
            ke.parse_corpus('{"kb": {"audiences": ["staff"]}}')
        with self.assertRaises(ValueError):
            ke.parse_corpus('{"kb": {"url": "u", "audiences": ["gerencia"]}}')

    def test_registry_corpus_command_feeds_parse_corpus(self):
        # What the deploy passes is exactly what the embedder reads.
        out = subprocess.run(
            [sys.executable, str(REPO / "scripts/corpus_registry.py"), "corpus",
             "--app", "admission-patient"], capture_output=True, text=True, check=True).stdout
        c = ke.parse_corpus(out)
        self.assertIn("biuman-kb", c)
        self.assertEqual(c["biuman-kb"]["url"], "http://biuman-kb-site")
        for spec in c.values():
            self.assertFalse(set(spec["audiences"]) & {"ti", "liderazgo", "publico"})

    def test_planned_edges_are_not_in_the_corpus(self):
        out = subprocess.run(
            [sys.executable, str(REPO / "scripts/corpus_registry.py"), "corpus",
             "--app", "pharos-ti"], capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), {})


class RetryTest(unittest.TestCase):
    def test_transient_is_retried_then_succeeds(self):
        calls = []

        def flaky(texts):
            calls.append(1)
            if len(calls) < 3:
                raise ke.Transient("502 upstream error")
            return [[0.0]], 1

        waits = []
        self.assertEqual(ke.embed_with_retry(flaky, ["t"], sleep=waits.append), ([[0.0]], 1))
        self.assertEqual(waits, [2.0, 4.0])

    def test_blocked_is_not_retried(self):
        calls = []

        def blocked(texts):
            calls.append(1)
            raise ke.Blocked("email")

        with self.assertRaises(ke.Blocked):
            ke.embed_with_retry(blocked, ["t"], sleep=lambda s: None)
        self.assertEqual(len(calls), 1)


class RunTest(unittest.TestCase):
    CORPUS = {"biuman-kb": {"url": "http://b", "audiences": ["staff", "servicio-al-cliente"]},
              "lch-admin-kb": {"url": "http://l", "audiences": ["staff", "servicio-al-cliente"]}}

    def fetch(self, indexes):
        def f(url):
            v = indexes[url]
            if isinstance(v, Exception):
                raise v
            return v
        return f

    def run_it(self, indexes, embed=ok_embed, corpus=None):
        store, out, err = FakeStore(), [], []
        code = ke.run(corpus or self.CORPUS, store, embed, log=out.append, err=err.append,
                      fetch=self.fetch(indexes), sleep=lambda s: None)
        return code, store, "\n".join(out), "\n".join(err)

    def test_clean_run(self):
        code, store, out, _ = self.run_it({
            "http://b": {"articles": [art("servicios/catalogo")]},
            "http://l": {"articles": [art("sac/portal", "servicio-al-cliente"), art("ti/x", "ti")]},
        })
        self.assertEqual(code, 0)
        self.assertEqual(store.replaced,
                         ["biuman-kb:servicios/catalogo", "lch-admin-kb:sac/portal"])
        self.assertEqual(store.pruned, [("biuman-kb", ["servicios/catalogo"]),
                                        ("lch-admin-kb", ["sac/portal"])])
        self.assertEqual(store.foreign, [["biuman-kb", "lch-admin-kb"]])
        self.assertIn("[done]", out)

    def test_a_502_that_recovers_does_not_redden_the_run(self):
        calls = []

        def once(texts):
            calls.append(1)
            if len(calls) == 1:
                raise ke.Transient("proxy returned 502: upstream error")
            return ok_embed(texts)

        code, store, out, _ = self.run_it({"http://b": {"articles": [art("a")]},
                                           "http://l": {"articles": [art("b")]}}, embed=once)
        self.assertEqual(code, 0)
        self.assertIn("[done]", out)

    def test_failed_source_keeps_rows_and_blocks_foreign_prune(self):
        code, store, out, err = self.run_it({
            "http://b": {"articles": [art("a")]},
            "http://l": urllib.error.URLError("down"),
        })
        self.assertEqual(code, 1)
        self.assertEqual([kb for kb, _ in store.pruned], ["biuman-kb"])
        self.assertEqual(store.foreign, [])
        self.assertIn("[partial]", err)
        self.assertNotIn("[done]", out)

    def test_failed_article_blocks_foreign_prune(self):
        def block_b(texts):
            if any("BLOCK" in t for t in texts):
                raise ke.Blocked("email")
            return ok_embed(texts)

        indexes = {"http://b": {"articles": [art("a"), art("b", body="BLOCK")]},
                   "http://l": {"articles": [art("c")]}}
        code, store, _, err = self.run_it(indexes, embed=block_b)
        self.assertEqual(code, 1)
        self.assertEqual(store.foreign, [])
        self.assertIn("biuman-kb:b", err)

    def test_empty_index_is_a_failed_source(self):
        code, _, _, err = self.run_it({"http://b": {"articles": []},
                                       "http://l": {"articles": [art("c")]}})
        self.assertEqual(code, 1)
        self.assertIn("zero articles", err)

    def test_no_corpus_embeds_nothing(self):
        store, err = FakeStore(), []
        self.assertEqual(ke.run({}, store, ok_embed, err=err.append), 2)
        self.assertEqual(store.replaced, [])

    def test_chunker_respects_size_and_overlap(self):
        text = ("Una frase. " * 400).strip()
        cs = ke.chunk(text)
        self.assertGreater(len(cs), 1)
        self.assertTrue(all(len(c) <= ke.TARGET_CHARS for c in cs))


class FetchTest(unittest.TestCase):
    def test_only_http_urls_are_fetched(self):
        with self.assertRaises(ValueError):
            ke.fetch_index("file:///etc/passwd")


class SyncTest(unittest.TestCase):
    def test_sync_script_knows_the_embedder(self):
        sh = (REPO / "scripts/sync-pharos-registry.sh").read_text(encoding="utf-8")
        self.assertIn("--embedder-dir", sh)
        self.assertIn("corpus/kb_embedder.py", sh)


if __name__ == "__main__":
    unittest.main()
