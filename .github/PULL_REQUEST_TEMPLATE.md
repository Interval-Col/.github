<!--
  Org-default PR template — lives in Interval-Col/.github.

  This applies to any repo in the org that does NOT define its own
  .github/PULL_REQUEST_TEMPLATE.md. Repos with code (finance-lch,
  lab-qc, …) ship their own with stack-specific test-plan rows; this is
  the fallback for the rest.

  Required by the org's branching-and-deploy policy
  (BRANCHING-AND-DEPLOY.md → "PR description").

  PR TITLE must follow Conventional Commits:
    <type>(<scope>)?: <short summary>
  The merge-commit subject is set to this PR title (repos merge via
  merge-commit with the PR-title message), so a bad PR title = a bad git
  log entry forever. CI (commitlint) blocks non-conforming titles.
-->

## Why

<!-- What problem does this solve? Link the plan / issue / discussion if
     any. One paragraph max. -->

## What changed

<!-- The SHAPE of the change — readers should not need to read the diff
     to understand it. Call out anything subtle. -->

## Test plan

<!-- What was verified, and how?
     - Commands you ran (tests, linters, build) and their results.
     - Manual-verification steps / screenshots for UI changes.
     - Docs-only change → note "docs-only; links resolve; no secrets";
       the `gitleaks` check must be green.
     - If something can't be auto-tested, say so explicitly. -->

## Rollout / rollback notes

<!-- Anything that affects deploys:
     - New env vars (added to .env.example?), migrations, feature flags.
     - How to roll back if it breaks.
     - Docs-only change → "revert is harmless." -->

## Related

<!-- Links to plans/*.md, RFCs, prior PRs, issues, discussions. -->
