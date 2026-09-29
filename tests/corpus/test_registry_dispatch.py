"""registry_dispatch: a registry change reaches exactly the consumers it touched.

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import registry_dispatch as rd  # noqa: E402
from corpus_lib import load_registry  # noqa: E402
from test_kb_dispatch import VERIFY_GREEN, FakeClock, FakeHttp  # noqa: E402

BASE = textwrap.dedent("""\
    version: 1
    audiences: [publico, staff, servicio-al-cliente, ti, liderazgo]
    kbs:
      - id: kb-a
        repo: kb-a
        image: kb-a-site
        roots: [guias]
        url: site
        default_status: vigente
        audiences: [staff, liderazgo, servicio-al-cliente]
      - id: kb-b
        repo: kb-b
        image: kb-b-site
        roots: [guias]
        url: site
        default_status: vigente
        audiences: [staff]
    consumers:
      - kb: kb-a
        app: app-one
        repo: repo-one
        environments: [development]
        audiences: [staff]
        mode: wait
      - kb: kb-b
        app: app-one
        repo: repo-one
        environments: [development]
        audiences: [staff]
        mode: wait
      - kb: kb-a
        app: app-two
        repo: repo-two
        environments: [development, production]
        audiences: [staff, liderazgo]
        mode: notify
      - kb: kb-b
        app: app-three
        repo: repo-three
        environments: [development]
        audiences: [staff]
        mode: planned
    """)


def reg(text: str = BASE) -> dict:
    return load_registry(text)


def edit(old: str, new: str, text: str = BASE) -> dict:
    assert text.count(old) == 1, old
    return reg(text.replace(old, new))


def repos(consumers) -> list[str]:
    return [c["repo"] for c in consumers]


class TouchedTest(unittest.TestCase):
    def test_no_change_touches_no_one(self):
        self.assertEqual(rd.touched(reg(), reg()), [])

    def test_widening_a_grant_touches_only_that_repo(self):
        # The motivating case: lab-qc + liderazgo loaded nothing until a publish.
        after = edit("    audiences: [staff, liderazgo]\n    mode: notify",
                     "    audiences: [staff, liderazgo, servicio-al-cliente]\n"
                     "    mode: notify")
        self.assertEqual(repos(rd.touched(reg(), after)), ["repo-two"])

    def test_narrowing_a_grant_touches_it(self):
        after = edit("    audiences: [staff, liderazgo]\n    mode: notify",
                     "    audiences: [staff]\n    mode: notify")
        self.assertEqual(repos(rd.touched(reg(), after)), ["repo-two"])

    def test_audience_order_is_not_a_change(self):
        after = edit("audiences: [staff, liderazgo]\n    mode: notify",
                     "audiences: [liderazgo, staff]\n    mode: notify")
        self.assertEqual(rd.touched(reg(), after), [])

    def test_an_environment_change_touches_it(self):
        # Grants are per environment now: moving an edge to prod changes a deploy.
        after = edit("    environments: [development, production]\n",
                     "    environments: [development]\n")
        self.assertEqual(repos(rd.touched(reg(), after)), ["repo-two"])

    def test_a_kb_image_change_touches_every_live_consumer_of_that_kb(self):
        after = edit("image: kb-b-site", "image: kb-b-site-v2")
        self.assertEqual(repos(rd.touched(reg(), after)), ["repo-one"])  # three is planned

    def test_planned_edges_are_ignored_both_ways(self):
        after = edit("    audiences: [staff]\n    mode: planned",
                     "    audiences: [staff, ti]\n    mode: planned")
        self.assertEqual(rd.touched(reg(), after), [])

    def test_going_live_touches_it_with_its_mode(self):
        after = edit("mode: planned", "mode: wait")
        self.assertEqual(rd.touched(reg(), after),
                         [{"repo": "repo-three", "app": "app-three", "mode": "wait"}])

    def test_losing_the_last_live_edge_keeps_the_mode_it_had(self):
        # A revocation needs proof the app redeployed (Codex, #256): a consumer
        # that waited still waits; one that only listened still only listens.
        after = edit("    audiences: [staff, liderazgo]\n    mode: notify",
                     "    audiences: [staff, liderazgo]\n    mode: planned")
        self.assertEqual(rd.touched(reg(), after),
                         [{"repo": "repo-two", "app": "app-two", "mode": "notify"}])
        waited = BASE.replace("    audiences: [staff]\n    mode: wait\n  - kb: kb-b\n"
                              "    app: app-one", "    audiences: [staff]\n    mode: planned\n"
                              "  - kb: kb-b\n    app: app-one")
        gone = waited.replace("    audiences: [staff]\n    mode: wait\n  - kb: kb-a\n"
                              "    app: app-two", "    audiences: [staff]\n    mode: planned\n"
                              "  - kb: kb-a\n    app: app-two")
        self.assertNotIn("repo-one", rd.live_edges(reg(gone)))  # BOTH edges went planned
        self.assertEqual(rd.touched(reg(), reg(gone))[0],
                         {"repo": "repo-one", "app": "app-one", "mode": "wait"})

    def test_a_mode_change_alone_is_not_a_change(self):
        # wait → notify changes how the publisher listens, not what the app loads.
        kb_b_one = ("  - kb: kb-b\n    app: app-one\n    repo: repo-one\n"
                    "    environments: [development]\n    audiences: [staff]\n    mode: ")
        after = edit(kb_b_one + "wait", kb_b_one + "notify")
        self.assertEqual(rd.touched(reg(), after), [])

    def test_a_repo_waits_if_any_of_its_live_edges_waits(self):
        # repo-one's kb-b edge changes AND turns notify; its kb-a edge still waits.
        kb_b_one = ("  - kb: kb-b\n    app: app-one\n    repo: repo-one\n"
                    "    environments: [development]\n    audiences: [staff")
        after = edit(kb_b_one + "]\n    mode: wait", kb_b_one + ", ti]\n    mode: notify",
                     BASE.replace("audiences: [staff]\n    url", "audiences: [staff, ti]\n    url"))
        [c] = rd.touched(reg(), after)
        self.assertEqual((c["repo"], c["mode"]), ("repo-one", "wait"))

    def test_an_unusable_before_touches_every_live_consumer(self):
        self.assertEqual(repos(rd.touched(None, reg())), ["repo-one", "repo-two"])


class ChangedKbsTest(unittest.TestCase):
    """The `kbs:` block acts at the KB's build, not at the consumer (Fable, 1.6)."""

    def test_a_build_time_field_names_the_kb(self):
        after = edit("image: kb-b-site\n    roots: [guias]",
                     "image: kb-b-site\n    roots: [guias, procesos]")
        self.assertEqual(rd.changed_kbs(reg(), after), ["kb-b"])
        self.assertEqual(rd.touched(reg(), after), [])  # no consumer grant changed

    def test_an_image_change_is_the_consumers_business_not_a_stale_index(self):
        self.assertEqual(rd.changed_kbs(reg(), edit("image: kb-b-site", "image: kb-b2")), [])

    def test_nothing_is_stale_without_a_before(self):
        self.assertEqual(rd.changed_kbs(None, reg()), [])


class RepublishTest(unittest.TestCase):
    """A stale KB is rebuilt by running its build-site.yml on main (German, 2026-09-29)."""

    class Http:
        def __init__(self, code, body=None):
            self.code, self.body, self.calls = code, body or {}, []

        def request(self, method, url, body=None):
            self.calls.append((method, url, body))
            return self.code, self.body

    def test_204_queues_the_kbs_own_workflow_on_main(self):
        http = self.Http(204)
        ok, detail = rd.republish(http, "Interval-Col", "kb-b")
        self.assertTrue(ok, detail)
        [(method, url, body)] = http.calls
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/repos/Interval-Col/kb-b/actions/workflows/"
                                     "build-site.yml/dispatches"), url)
        self.assertEqual(body, {"ref": "main"})
        self.assertIn("kb-publish run", detail)

    def test_403_names_the_missing_permission(self):
        ok, detail = rd.republish(self.Http(403, {"message": "Resource not accessible"}),
                                  "Interval-Col", "kb-b")
        self.assertFalse(ok)
        self.assertIn("actions: write", detail)

    def test_404_is_red_too(self):
        # A KB without workflow_dispatch in build-site.yml answers 422/404.
        ok, detail = rd.republish(self.Http(422, {"message": "Workflow does not have "
                                                  "'workflow_dispatch' trigger"}),
                                  "Interval-Col", "kb-b")
        self.assertFalse(ok)
        self.assertIn("workflow_dispatch", detail)


class RunTest(unittest.TestCase):
    """The dispatch and the wait are kb_dispatch.publish(): same contract."""

    def publish(self, http, consumers):
        fc = FakeClock()
        return rd.kb_dispatch.publish(http, "Interval-Col", rd.SOURCE, "b" * 40, consumers,
                                      600, 30, clock=fc.clock, sleep=fc.sleep)

    def run_for(self, cid_title: bool = True, jobs=None):
        cid = rd.kb_dispatch.correlation_id(rd.SOURCE, "b" * 40)
        title = f"kb-updated · registry · {cid}" if cid_title else "CI/CD"
        run = {"id": 9, "status": "completed", "conclusion": "success",
               "display_title": title, "html_url": "u"}
        return FakeHttp(runs={"repo-one": [run]}, jobs={"repo-one": jobs or [VERIFY_GREEN]})

    def test_payload_says_the_registry_sent_it(self):
        http = self.run_for()
        [o] = self.publish(http, [{"repo": "repo-one", "app": "app-one", "mode": "wait"}])
        self.assertTrue(o.ok, o.detail)
        self.assertEqual(http.last_payload["client_payload"]["source"], "registry")

    def test_a_skipped_verify_is_red_here_too(self):
        http = self.run_for(jobs=[{"name": "corpus-verify / corpus-verify",
                                   "conclusion": "skipped"}])
        [o] = self.publish(http, [{"repo": "repo-one", "app": "app-one", "mode": "wait"}])
        self.assertFalse(o.ok)


class CliTest(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(REPO / "scripts/registry_dispatch.py"), *args],
                              capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})

    def test_plan_prints_the_touched_repos(self):
        with tempfile.TemporaryDirectory() as d:
            b, a = Path(d) / "b.yml", Path(d) / "a.yml"
            b.write_text(BASE, encoding="utf-8")
            a.write_text(BASE.replace("audiences: [staff, liderazgo]\n    mode: notify",
                                      "audiences: [staff]\n    mode: notify"), encoding="utf-8")
            r = self.cli("plan", "--before", str(b), "--after", str(a))
            self.assertEqual((r.returncode, r.stdout.strip()), (0, "repo-two"), r.stderr)

    def test_a_broken_before_touches_everyone_and_says_so(self):
        with tempfile.TemporaryDirectory() as d:
            b, a = Path(d) / "b.yml", Path(d) / "a.yml"
            b.write_text("version: [\n", encoding="utf-8")
            a.write_text(BASE, encoding="utf-8")
            r = self.cli("plan", "--before", str(b), "--after", str(a))
            self.assertEqual(r.stdout.strip(), "repo-one,repo-two")
            self.assertIn("unusable", r.stderr)

    def test_run_with_nothing_touched_is_green_without_a_token(self):
        with tempfile.TemporaryDirectory() as d:
            b = Path(d) / "b.yml"
            b.write_text(BASE, encoding="utf-8")
            r = self.cli("run", "--before", str(b), "--after", str(b), "--sha", "c" * 40)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("touches no live consumer", r.stdout)

    def test_run_that_touches_someone_without_a_token_is_red(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d) / "a.yml"
            a.write_text(BASE, encoding="utf-8")
            r = self.cli("run", "--after", str(a), "--sha", "c" * 40)
            self.assertEqual(r.returncode, 2)
            self.assertIn("GH_TOKEN", r.stderr)

    def stale_pair(self, d):
        b, a = Path(d) / "b.yml", Path(d) / "a.yml"
        b.write_text(BASE, encoding="utf-8")
        a.write_text(BASE.replace("image: kb-b-site\n    roots: [guias]",
                                  "image: kb-b-site\n    roots: [guias, procesos]"),
                     encoding="utf-8")
        return b, a

    def test_plan_mints_for_the_kb_to_republish(self):
        # No consumer grant changed, but the token must reach kb-b's repo.
        with tempfile.TemporaryDirectory() as d:
            b, a = self.stale_pair(d)
            r = self.cli("plan", "--before", str(b), "--after", str(a))
            self.assertEqual(r.stdout.strip(), "kb-b", r.stderr)

    def test_a_stale_kb_without_a_token_is_red(self):
        with tempfile.TemporaryDirectory() as d:
            b, a = self.stale_pair(d)
            r = self.cli("run", "--before", str(b), "--after", str(a), "--sha", "c" * 40)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("GH_TOKEN", r.stderr)

    def test_the_real_registry_plans(self):
        r = self.cli("plan", "--before", str(REPO / "corpus-registry.yml"),
                     "--after", str(REPO / "corpus-registry.yml"))
        self.assertEqual((r.returncode, r.stdout.strip()), (0, ""), r.stderr)


class WorkflowShapeTest(unittest.TestCase):
    wf = (REPO / ".github/workflows/corpus-registry-changed.yml").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in wf.splitlines() if not ln.lstrip().startswith("#"))

    def test_runs_on_a_registry_push_to_main(self):
        self.assertIn("branches: [main]", self.code)
        self.assertIn("paths: [corpus-registry.yml]", self.code)
        self.assertNotIn("pull_request", self.code)  # the bot key never reaches a PR

    def test_is_github_hosted(self):
        # Public repo: the org's runner groups refuse it, and self-hosted would be
        # the wrong place for a public repo's jobs anyway.
        self.assertNotIn("self-hosted", self.code)

    def test_nothing_fails_open(self):
        self.assertNotIn("continue-on-error", self.code)
        self.assertNotIn("|| true", self.code)

    def test_before_is_the_last_green_run_not_the_previous_push(self):
        # One pending run per group: diffing against event.before loses a change.
        self.assertIn("corpus-registry-changed.yml/runs?branch=main&status=success", self.code)
        self.assertIn("actions: read", self.code)

    def test_the_verdict_step_always_runs(self):
        # With no consumer touched it is still where a stale KB is republished.
        step = self.code.split("- name: Dispatch kb-updated")[1]
        self.assertNotIn("if:", step)

    def test_it_calls_the_script(self):
        self.assertIn("scripts/registry_dispatch.py plan", self.code)
        self.assertIn("scripts/registry_dispatch.py run", self.code)


if __name__ == "__main__":
    unittest.main()
