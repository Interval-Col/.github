"""changes_classify: only documentation skips the heavy jobs — and doubt runs them.

    python3 -m unittest discover -s tests/corpus -v
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import changes_classify as cc  # noqa: E402


class ClassifyTest(unittest.TestCase):
    def test_a_plan_only_change_is_docs(self):
        self.assertFalse(cc.classify(["plans/nerea-con-conocimiento-plan.md"]))

    def test_markdown_anywhere_is_docs(self):
        self.assertFalse(cc.classify([
            "README.md", "CLAUDE.md", "backend/README.md", "lab-qc/docs/STANDARDS.md",
            ".github/copilot-instructions.md",
        ]))

    def test_docs_and_plans_folders_at_any_depth_are_docs(self):
        self.assertFalse(cc.classify(["docs/diagram.svg", "apps/lch-web/plans/x.png", "LICENSE"]))

    def test_one_code_file_makes_it_code(self):
        self.assertTrue(cc.classify(["plans/x.md", "backend/app/chat/embed_kb.py"]))

    def test_workflows_and_config_are_code(self):
        for path in (".github/workflows/ci.yml", "docker-compose.deploy.yml", "pyproject.toml",
                     "frontend/package.json", ".chat-contract.yml"):
            self.assertTrue(cc.classify([path]), path)

    def test_lookalikes_are_code(self):
        # A folder merely NAMED like docs, or an .md-ish extension, is not docs.
        for path in ("backend/app/docs_router.py", "frontend/app/plans.vue", "notes.mdx",
                     "app/templates/report.md.j2"):
            self.assertTrue(cc.classify([path]), path)

    def test_empty_list_fails_open(self):
        self.assertTrue(cc.classify([]))
        self.assertTrue(cc.classify(["", "  "]))

    def test_code_regex_claims_docs_back(self):
        code_re = re.compile(r"^content/")
        self.assertTrue(cc.classify(["content/guia.md"], code_re))
        self.assertFalse(cc.classify(["plans/x.md"], code_re))


class WorkflowShapeTest(unittest.TestCase):
    """The workflow can't run here; these pin its fail-open properties."""

    wf = (REPO / ".github/workflows/changes.yml").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in wf.splitlines() if not ln.lstrip().startswith("#"))

    def test_is_reusable_with_a_code_output(self):
        self.assertIn("workflow_call:", self.code)
        self.assertIn("value: ${{ jobs.changes.outputs.code }}", self.code)

    def test_never_uses_trigger_path_filters(self):
        # A required check behind paths-ignore waits forever.
        self.assertNotIn("paths-ignore", self.code)

    def test_renames_classify_both_paths(self):
        # Codex on #246: `src/x.py` → `docs/x.py` must not read as docs-only.
        self.assertEqual(self.code.count(".previous_filename // empty"), 2)
        self.assertTrue(cc.classify(["docs/module.py", "src/module.py"]))

    def test_a_pr_listing_cut_short_fails_open(self):
        self.assertIn(".changed_files", self.code)
        self.assertIn('"$listed" -lt "$total"', self.code)

    def test_since_last_success_diffs_against_the_last_green_run(self):
        # A docs push that cancels a code deploy must not skip it.
        self.assertIn("since_last_success:", self.code)
        self.assertIn("status=success", self.code)

    def test_events_without_a_diff_run_everything(self):
        self.assertIn("*) ok=false", self.code)
        self.assertIn("-ge 300", self.code)


if __name__ == "__main__":
    unittest.main()
