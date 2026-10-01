"""corpus_verify: fresh by content hash, absent when it must be, answers that cite.

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import corpus_verify as cv  # noqa: E402


def art(slug, status="vigente", audience="staff", h=None, questions=()):
    return {"slug": slug, "status": status, "audience": audience,
            "content_hash": h or f"sha256:{slug}", "verificacion": list(questions)}


INDEX = {"version": 5, "kb": "kb-a", "articles": [
    art("guias/a"),
    art("guias/b"),
    art("guias/borrador", status="borrador"),
    art("guias/jefes", audience="liderazgo"),
]}


def statuses(results):
    return {c: s for c, s, _ in results}


class EvaluateKbTest(unittest.TestCase):
    def test_passing_corpus(self):
        stored = [("guias/a", "sha256:guias/a", 3), ("guias/b", "sha256:guias/b", 2)]
        r = cv.evaluate_kb("kb-a", INDEX, ["staff"], stored, floor=1)
        self.assertEqual(statuses(r), {"V1": "PASS", "V2": "PASS", "V3": "PASS"}, r)

    def test_edited_article_with_old_chunks_is_stale(self):
        # Same slug, old hash: a slug check would pass this.
        stored = [("guias/a", "sha256:OLD", 3), ("guias/b", "sha256:guias/b", 2)]
        r = cv.evaluate_kb("kb-a", INDEX, ["staff"], stored, floor=1)
        self.assertEqual(statuses(r)["V2"], "FAIL")
        self.assertIn("stale 1: guias/a", dict((c, d) for c, _, d in r)["V2"])

    def test_half_replaced_article_is_stale(self):
        stored = [("guias/a", "sha256:guias/a", 2), ("guias/a", "sha256:OLD", 1),
                  ("guias/b", "sha256:guias/b", 2)]
        self.assertEqual(statuses(cv.evaluate_kb("kb-a", INDEX, ["staff"], stored, 1))["V2"],
                         "FAIL")

    def test_missing_article_fails_v2(self):
        stored = [("guias/a", "sha256:guias/a", 3)]
        r = cv.evaluate_kb("kb-a", INDEX, ["staff"], stored, floor=1)
        self.assertEqual(statuses(r)["V2"], "FAIL")

    def test_draft_removed_and_ungranted_articles_must_be_absent(self):
        stored = [("guias/a", "sha256:guias/a", 3), ("guias/b", "sha256:guias/b", 2),
                  ("guias/borrador", "sha256:guias/borrador", 1),   # not vigente
                  ("guias/jefes", "sha256:guias/jefes", 1),         # outside the grant
                  ("guias/retirado", "sha256:x", 4)]                # gone from the KB
        r = cv.evaluate_kb("kb-a", INDEX, ["staff"], stored, floor=1)
        self.assertEqual(statuses(r)["V3"], "FAIL")
        detail = dict((c, d) for c, _, d in r)["V3"]
        for slug in ("guias/borrador", "guias/jefes", "guias/retirado"):
            self.assertIn(slug, detail)

    def test_granting_liderazgo_makes_it_servable(self):
        stored = [("guias/a", "sha256:guias/a", 1), ("guias/b", "sha256:guias/b", 1),
                  ("guias/jefes", "sha256:guias/jefes", 1)]
        r = cv.evaluate_kb("kb-a", INDEX, ["staff", "liderazgo"], stored, floor=1)
        self.assertEqual(statuses(r), {"V1": "PASS", "V2": "PASS", "V3": "PASS"})

    def test_empty_corpus_fails_the_floor(self):
        r = cv.evaluate_kb("kb-a", INDEX, ["staff"], [], floor=1)
        self.assertEqual(statuses(r)["V1"], "FAIL")

    def test_nothing_servable_means_floor_zero(self):
        r = cv.evaluate_kb("kb-a", INDEX, ["ti"], [], floor=5)
        self.assertEqual(statuses(r), {"V1": "PASS", "V2": "PASS", "V3": "PASS"})

    def test_pre_v5_index_fails_plainly(self):
        r = cv.evaluate_kb("kb-a", {"version": 4, "articles": []}, ["staff"], [], 1)
        self.assertEqual(r[0][1], "FAIL")
        self.assertIn("v5", r[0][2])


class AnswerTest(unittest.TestCase):
    Q = {"pregunta": "¿Cuánto dura el bloqueo?", "debe_citar": "guias/a",
         "debe_decir": "5 minutos"}

    def test_cites_and_says(self):
        ok, _ = cv.check_answer(self.Q, "El bloqueo dura 5 MINUTOS.", ["kb-a:guias/a"])
        self.assertTrue(ok)

    def test_accents_and_case_do_not_matter(self):
        q = dict(self.Q, debe_decir="Servicio al Cliente")
        ok, _ = cv.check_answer(q, "escríbele a servicio al cliénte", ["guias/a"])
        self.assertTrue(ok)

    def test_right_fact_without_citation_fails(self):
        ok, detail = cv.check_answer(self.Q, "Dura 5 minutos.", ["guias/otra"])
        self.assertFalse(ok)
        self.assertIn("did not cite", detail)

    def test_twin_guides_pass_on_either_citation(self):
        q = dict(self.Q, debe_citar=["sac/ingreso", "mesa/ingreso"], debe_decir="5 por hora")
        for cited in (["lch-admin-kb:sac/ingreso"], ["lch-admin-kb:mesa/ingreso"]):
            ok, _ = cv.check_answer(q, "Hasta 5 por hora.", cited)
            self.assertTrue(ok, cited)

    def test_twin_guides_still_fail_when_neither_is_cited(self):
        q = dict(self.Q, debe_citar=["sac/ingreso", "mesa/ingreso"], debe_decir="5 por hora")
        ok, detail = cv.check_answer(q, "Hasta 5 por hora.", ["lch-admin-kb:otra/guia"])
        self.assertFalse(ok)
        self.assertIn("any of `sac/ingreso`, `mesa/ingreso`", detail)

    def test_a_suffix_is_not_a_citation(self):
        # `endswith(":" + slug)` must not let «x/sac/ingreso» count for «sac/ingreso».
        q = dict(self.Q, debe_citar=["sac/ingreso"], debe_decir="")
        ok, _ = cv.check_answer(q, "", ["lch-admin-kb:x/sac/ingreso"])
        self.assertFalse(ok)

    def test_citation_with_wrong_fact_fails(self):
        # The error the plan names: the guide said 5 minutes, an answer said an hour.
        ok, detail = cv.check_answer(self.Q, "Dura hasta una hora.", ["guias/a"])
        self.assertFalse(ok)
        self.assertIn("5 minutos", detail)

    def test_the_fact_in_other_words_passes(self):
        # Measured on Admisiones: right answer, not the literal phrase.
        q = dict(self.Q, debe_decir="5 por hora")
        ok, _ = cv.check_answer(q, "Puede pedir hasta 5 códigos de recuperación por hora.",
                                ["guias/a"])
        self.assertTrue(ok)

    def test_another_form_of_the_same_verb_says_it(self):
        # Pháros TI, 2026-09-30: guide «escala de inmediato», Nerea «debes escalar
        # de inmediato». Right answer; the check must not demand the wording.
        q = dict(self.Q, debe_decir="escala")
        for reply in ("Debes escalar de inmediato.", "Escálalo de inmediato.", "Escala ya."):
            ok, _ = cv.check_answer(q, reply, ["guias/a"])
            self.assertTrue(ok, reply)

    def test_singular_and_plural_are_the_same_word(self):
        q = dict(self.Q, debe_decir="5 minutos")
        self.assertTrue(cv.check_answer(q, "Queda bloqueada 5 minuto más.", ["guias/a"])[0])

    def test_a_longer_different_word_is_not_the_same_word(self):
        # «hora» is not «horario»: 3 letters apart, a different word.
        q = dict(self.Q, debe_decir="por hora")
        self.assertFalse(cv.check_answer(q, "Según el horario de la sede.", ["guias/a"])[0])
        self.assertFalse(cv.same_word("hora", "horario"))
        self.assertFalse(cv.same_word("pie", "pies"))  # < 4 letters: exact only

    def test_a_missing_word_of_the_fact_still_fails(self):
        q = dict(self.Q, debe_decir="5 por hora")
        ok, _ = cv.check_answer(q, "Puede pedir 5 códigos por día.", ["guias/a"])
        self.assertFalse(ok)

    def test_numbers_keep_their_punctuation(self):
        # Codex on #254: the unit or the decimals are part of the fact.
        self.assertFalse(cv.says("5%", "El plazo es 5 minutos"))
        self.assertFalse(cv.says("1.5", "entre 1 y 5 días"))
        self.assertFalse(cv.says("10-15", "10 o 15 minutos"))
        self.assertTrue(cv.says("10-15", "tarda 10-15 minutos"))
        self.assertTrue(cv.says("5%", "sube un 5% al año"))

    def test_a_suffix_is_not_a_citation(self):
        self.assertFalse(cv.cites(["otras/guias/a"], "guias/a"))


class VerifyTest(unittest.TestCase):
    """The whole run, with the DB, the index fetch and the ask module faked."""

    def cfg(self, **kw):
        base = {"app": "app-a", "grants": {"kb-a": ["staff"]}, "sources": {"kb-a": "http://kb"},
                "table": "t", "db": "env:X", "ask_module": "app.chat.ask", "floor": 1}
        base.update(kw)
        return base

    def run_verify(self, rows, index, answers=None, **kw):
        answers = list(answers or [])
        with mock.patch.object(cv, "_connect", return_value=lambda sql: rows), \
             mock.patch.object(cv, "_fetch_index", return_value=index), \
             mock.patch.object(cv, "_ask", side_effect=lambda *a: answers.pop(0)):
            return cv.verify(self.cfg(**kw))

    def test_passing_run_next_to_a_failing_one(self):
        q = {"pregunta": "¿Cuánto dura el bloqueo?", "debe_citar": "guias/a",
             "debe_decir": "5 minutos"}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 3)]

        good = self.run_verify(rows, index, [("Dura 5 minutos.", ["kb-a:guias/a"])])
        self.assertTrue(all(s == "PASS" for _, s, _ in good), good)

        # A question the corpus cannot answer: three tries, all wrong → red.
        bad = self.run_verify(rows, index, [("No está en mi material.", [])] * 3)
        self.assertEqual([s for c, s, _ in bad if c == "V4"], ["FAIL"])

    def test_retry_absorbs_one_flaky_answer(self):
        q = {"pregunta": "p", "debe_citar": "guias/a", "debe_decir": ""}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 3)]
        r = self.run_verify(rows, index, [("x", []), ("y", ["guias/a"])])
        self.assertEqual([s for c, s, _ in r if c == "V4"], ["PASS"])

    def test_a_pass_after_a_retry_says_so(self):
        q = {"pregunta": "p", "debe_citar": "guias/a", "debe_decir": ""}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 3)]
        r = self.run_verify(rows, index, [("x", []), ("y", ["guias/a"])])
        (detail,) = [d for c, s, d in r if c == "V4" and s == "PASS"]
        self.assertIn("on attempt 2 of 3", detail)

    def test_three_attempts_before_a_fail_and_the_reply_is_shown(self):
        # 2026-10-01: one question failed twice in a row, then passed on a re-run.
        q = {"pregunta": "p", "debe_citar": "guias/a", "debe_decir": "escala"}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 3)]
        wrong = ("Revisa la conexión | y vuelve a intentar. " * 20, ["guias/a"])
        r = self.run_verify(rows, index, [wrong, wrong, ("Debes escalar ya.", ["guias/a"])])
        self.assertEqual([s for c, s, _ in r if c == "V4"], ["PASS"])
        r = self.run_verify(rows, index, [wrong, wrong, wrong])
        (detail,) = [d for c, s, d in r if c == "V4" and s == "FAIL"]
        self.assertIn("last reply: «Revisa la conexión / y vuelve", detail)
        self.assertLess(len(detail), 400)   # one line in the summary table, not the reply

    def test_unattributed_chunks_fail(self):
        index = {"version": 5, "articles": [art("guias/a")]}
        rows = [(None, "guias/a", None, 89)]    # today's lab-qc and Admisiones shape
        r = self.run_verify(rows, index)
        details = " ".join(d for _, s, d in r if s == "FAIL")
        self.assertIn("no `metadata.kb`", details)
        self.assertIn("missing 1", details)

    def test_chunks_from_an_ungranted_kb_fail(self):
        index = {"version": 5, "articles": [art("guias/a")]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 1), ("kb-z", "x", "h", 2)]
        r = self.run_verify(rows, index)
        self.assertTrue(any("not granted" in d for _, s, d in r if s == "FAIL"))

    def test_questions_without_an_ask_module_fail(self):
        q = {"pregunta": "p", "debe_citar": "guias/a", "debe_decir": ""}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        rows = [("kb-a", "guias/a", "sha256:guias/a", 1)]
        r = self.run_verify(rows, index, ask_module=None)
        self.assertEqual([s for c, s, _ in r if c == "V4"], ["FAIL"])

    def test_questions_are_asked_with_the_union_of_grants(self):
        q = {"pregunta": "p", "debe_citar": "guias/a", "debe_decir": ""}
        index = {"version": 5, "articles": [art("guias/a", questions=[q])]}
        seen = []
        rows = [("kb-a", "guias/a", "sha256:guias/a", 1)]
        with mock.patch.object(cv, "_connect", return_value=lambda sql: rows), \
             mock.patch.object(cv, "_fetch_index", return_value=index), \
             mock.patch.object(cv, "_ask", side_effect=lambda m, qq, a: seen.append(a)
                               or ("ok", ["guias/a"])):
            cv.verify(self.cfg(grants={"kb-a": ["staff", "ti"], "kb-b": ["servicio-al-cliente"]},
                               sources={"kb-a": "http://a", "kb-b": "http://b"}))
        self.assertEqual(seen[0], ["servicio-al-cliente", "staff", "ti"])

    def test_main_exit_code_and_marker(self):
        cfg = base64.b64encode(json.dumps(self.cfg()).encode()).decode()
        with mock.patch.dict("os.environ", {"CORPUS_VERIFY_CONFIG": cfg}), \
             mock.patch.object(cv, "verify", return_value=[("V1", "FAIL", "x")]), \
             mock.patch("builtins.print") as p:
            self.assertEqual(cv.main(), 1)
        self.assertTrue(any("CORPUS-VERIFY" in str(c) for c in p.call_args_list))


class WorkflowShapeTest(unittest.TestCase):
    """The workflow can't run here; these pin the properties that matter."""

    wf = (REPO / ".github/workflows/corpus-verify.yml").read_text(encoding="utf-8")

    def test_is_reusable_and_scoped_to_an_environment(self):
        self.assertIn("workflow_call:", self.wf)
        self.assertIn("environment: ${{ inputs.environment }}", self.wf)

    def test_environment_and_ssh_secret_names_have_no_default(self):
        # The org-level PROD_HOST trap: nothing may default to a secret name.
        for name in ("environment", "ssh_host_secret", "ssh_user_secret", "ssh_key_secret"):
            block = self.wf.split(f"      {name}:\n", 1)[1].split("\n      ", 3)
            self.assertIn("required: true", "\n".join(block[:3]), name)
        self.assertNotIn("PROD_HOST", "\n".join(
            ln for ln in self.wf.splitlines() if not ln.lstrip().startswith("#")))

    def test_can_wait_for_the_detached_embed(self):
        self.assertIn("wait_for:", self.wf)
        self.assertIn("docker wait $WAIT_FOR", self.wf)

    def _run_wait_step(self, ssh_stdout: str, ssh_exit: int, wf: str | None = None) -> int:
        """Run the real «Wait for the embed» shell with a fake `ssh` on PATH."""
        import os
        import subprocess
        import tempfile
        import textwrap

        step = (wf or self.wf).split("- name: Wait for the embed to finish", 1)[1]
        script = textwrap.dedent(step.split("run: |\n", 1)[1].split("\n\n      - name:", 1)[0])
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "ssh"
            fake.write_text(f"#!/bin/sh\nprintf '%s' '{ssh_stdout}'\nexit {ssh_exit}\n")
            fake.chmod(0o755)
            env = {**os.environ, "PATH": f"{tmp}:{os.environ['PATH']}",
                   "TARGET": "u@h", "WAIT_FOR": "app-embed-kb"}
            return subprocess.run(["bash", "-c", script], env=env,
                                  capture_output=True, text=True).returncode

    def test_an_embed_that_never_ran_is_red(self):
        # No such container (a failed pull after the old one-shot was removed), a
        # timeout, or no host: V1–V3 would pass on the OLD corpus (Fable, 2026-10-01).
        self.assertEqual(self._run_wait_step("", 1), 1)

    def test_a_finished_embed_goes_on_whatever_its_exit_code(self):
        self.assertEqual(self._run_wait_step("0", 0), 0)
        self.assertEqual(self._run_wait_step("1", 0), 0)

    def test_planned_edges_are_not_granted(self):
        self.assertIn('g["mode"] != "planned"', self.wf)

    def test_runs_the_script_and_requires_its_marker(self):
        self.assertIn(".corpus-org/scripts/corpus_verify.py", self.wf)
        self.assertIn("CORPUS-VERIFY", self.wf)
        self.assertTrue((REPO / "scripts/corpus_verify.py").exists())


if __name__ == "__main__":
    unittest.main()
