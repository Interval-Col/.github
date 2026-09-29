"""kb_dispatch: a 204 is not a verdict — the publisher waits for the consumer's run.

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import kb_dispatch  # noqa: E402

NOW = datetime.now(timezone.utc)
LATER = (NOW + timedelta(seconds=5)).strftime("%Y-%m-%dT%H:%M:%SZ")


class FakeHttp:
    """Scripted GitHub: dispatch codes per repo, and a run sequence per repo."""

    def __init__(self, dispatch=None, runs=None, list_code=200, jobs=None):
        self.dispatch = dispatch or {}
        self.runs = runs or {}          # repo -> list of run dicts returned in order
        self.list_code = list_code
        self.jobs = jobs or {}          # repo -> jobs of its run (default: verify green)
        self.calls: list[tuple[str, str]] = []

    def request(self, method, url, body=None):
        self.calls.append((method, url))
        repo = url.split("/repos/Interval-Col/")[1].split("/")[0]
        if url.endswith("/dispatches"):
            self.last_payload = body
            return self.dispatch.get(repo, 204), {}
        seq = self.runs.get(repo, [])
        if url.endswith("/jobs?per_page=100"):
            return 200, {"jobs": self.jobs.get(repo, [VERIFY_GREEN])}
        if "/actions/runs?" in url:
            if self.list_code != 200:
                return self.list_code, {"message": "Resource not accessible by integration"}
            return 200, {"workflow_runs": seq[:1]}
        # GET one run: advance the scripted sequence
        if len(seq) > 1:
            seq.pop(0)
        return 200, seq[0]


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def clock(self):
        return self.t

    def sleep(self, s):
        self.t += s


CID = kb_dispatch.correlation_id("biuman-kb", "a" * 40)
TITLE = f"kb-updated · biuman-kb · {CID}"
VERIFY_GREEN = {"name": "corpus-verify / corpus-verify", "conclusion": "success"}


def run(state, conclusion=None, title=TITLE):
    return {"id": 7, "status": state, "conclusion": conclusion, "created_at": LATER,
            "display_title": title, "html_url": "https://github.com/x/runs/7"}


def consumer(repo, mode="wait"):
    return {"repo": repo, "app": repo, "mode": mode}


def publish(http, consumers, timeout_s=600):
    fc = FakeClock()
    return kb_dispatch.publish(http, "Interval-Col", "biuman-kb", "a" * 40, consumers,
                               timeout_s, 30, clock=fc.clock, sleep=fc.sleep)


class PublishTest(unittest.TestCase):
    def test_green_consumer_run_is_success(self):
        http = FakeHttp(runs={"app-a": [run("queued"), run("in_progress"),
                                        run("completed", "success")]})
        [o] = publish(http, [consumer("app-a")])
        self.assertTrue(o.ok, o.detail)
        self.assertIn("corpus-verify `success`", o.detail)

    def test_green_run_with_verify_skipped_fails(self):
        # ADMISSION_DEPLOY_ENABLED off ⇒ deploy and corpus-verify skipped, run green.
        http = FakeHttp(runs={"app-a": [run("completed", "success")]},
                        jobs={"app-a": [{"name": "corpus-verify / corpus-verify",
                                         "conclusion": "skipped"}]})
        [o] = publish(http, [consumer("app-a")])
        self.assertFalse(o.ok)
        self.assertIn("`skipped`", o.detail)

    def test_green_run_with_no_verify_job_fails(self):
        # lab-qc today: a deploy, no corpus-verify at all.
        http = FakeHttp(runs={"app-a": [run("completed", "success")]},
                        jobs={"app-a": [{"name": "Deploy Backend", "conclusion": "success"}]})
        [o] = publish(http, [consumer("app-a")])
        self.assertFalse(o.ok)
        self.assertIn("no such job", o.detail)

    def test_red_consumer_run_fails_the_publish(self):
        # The Admisiones month: dispatch accepted, run red.
        http = FakeHttp(runs={"app-a": [run("completed", "failure")]})
        [o] = publish(http, [consumer("app-a")])
        self.assertFalse(o.ok)
        self.assertIn("failure", o.detail)

    def test_accepted_dispatch_with_no_run_times_out_red(self):
        http = FakeHttp(runs={"app-a": []})
        [o] = publish(http, [consumer("app-a")], timeout_s=120)
        self.assertFalse(o.ok)
        self.assertIn("no run titled with", o.detail)

    def test_refused_dispatch_fails_even_for_notify(self):
        http = FakeHttp(dispatch={"app-a": 404})
        [o] = publish(http, [consumer("app-a", "notify")])
        self.assertFalse(o.ok)
        self.assertIn("HTTP 404", o.detail)

    def test_notify_is_ok_on_204_but_warns(self):
        [o] = publish(FakeHttp(), [consumer("app-a", "notify")])
        self.assertTrue(o.ok)
        self.assertTrue(any("notify-only" in w for w in o.warnings))

    def test_missing_actions_read_is_named(self):
        http = FakeHttp(list_code=403)
        [o] = publish(http, [consumer("app-a")])
        self.assertFalse(o.ok)
        self.assertIn("actions: read", o.detail)

    def test_correlation_id_match_has_no_warning(self):
        http = FakeHttp(runs={"app-a": [run("completed", "success")]})
        [o] = publish(http, [consumer("app-a")])
        self.assertTrue(o.ok)
        self.assertEqual(o.warnings, [])
        self.assertEqual(http.last_payload["client_payload"]["correlation_id"], CID)

    def test_a_run_without_the_id_is_never_taken(self):
        # The time fallback bound two publishes to each other's runs; now an
        # untitled run — even a green one — is someone else's.
        http = FakeHttp(runs={"app-a": [run("completed", "success", title="CI/CD")]})
        [o] = publish(http, [consumer("app-a")], timeout_s=120)
        self.assertFalse(o.ok)
        self.assertIn("run-name", o.detail)

    def test_every_consumer_is_dispatched_before_anyone_is_waited_on(self):
        http = FakeHttp(runs={"app-a": [run("completed", "success")],
                              "app-b": [run("completed", "success")]})
        publish(http, [consumer("app-a"), consumer("app-b")])
        dispatches = [i for i, (m, u) in enumerate(http.calls) if u.endswith("/dispatches")]
        first_wait = next(i for i, (m, u) in enumerate(http.calls) if "/actions/runs" in u)
        self.assertEqual(dispatches, [0, 1])
        self.assertLess(max(dispatches), first_wait)

    def test_payload_carries_source_and_sha(self):
        http = FakeHttp(runs={"app-a": [run("completed", "success")]})
        publish(http, [consumer("app-a")])
        payload = http.last_payload
        self.assertEqual(payload["event_type"], "kb-updated")
        self.assertEqual(payload["client_payload"]["source"], "biuman-kb")
        self.assertEqual(payload["client_payload"]["sha"], "a" * 40)


class WorkflowShapeTest(unittest.TestCase):
    """The workflow can't run here; these pin the properties that matter."""

    wf = (REPO / ".github/workflows/kb-publish.yml").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in wf.splitlines() if not ln.lstrip().startswith("#"))

    def test_is_reusable(self):
        self.assertIn("workflow_call:", self.wf)

    def test_scripts_it_calls_exist(self):
        for script in ("kb_index.py", "corpus_registry.py", "kb_dispatch.py"):
            self.assertIn(f".corpus-org/scripts/{script}", self.wf)
            self.assertTrue((REPO / "scripts" / script).exists(), script)

    def test_nothing_fails_open(self):
        # The old legs had `continue-on-error: true` on the token mint.
        self.assertFalse("continue-on-error" in self.code, "a step fails open")

    def test_a_manual_dispatch_on_main_publishes_like_a_push(self):
        # lch-kb republishes on demand (e.g. to force a corpus refresh).
        self.assertEqual(self.code.count("github.event_name == 'workflow_dispatch'"), 3)

    def test_latest_moves_only_while_the_commit_is_the_tip(self):
        # Concurrency order is arbitrary (Codex, #255): the freshness check is the guard.
        self.assertIn('git ls-remote origin "$REF"', self.code)
        self.assertIn('"$tip" != "$SHA"', self.code)
        self.assertIn("needs.build.outputs.superseded != 'true'", self.code)

    def test_no_hardcoded_consumer_list(self):
        for repo in ("admission-patient", "biuman-lis", "pharos-lis"):
            self.assertFalse(repo in self.code, f"hardcoded consumer {repo}")


if __name__ == "__main__":
    unittest.main()
