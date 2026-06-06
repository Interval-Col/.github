#!/usr/bin/env bash
#
# Pre-push branch-name linter — policy hook #4 (docs repos) / #5 (repos
# with code). Byte-for-byte the reusable copy from finance-lch / lab-qc.
#
# Rejects branches whose name doesn't match `<type>/<short-kebab-slug>`
# per the org's branching-and-deploy policy
# (BRANCHING-AND-DEPLOY.md → "Branch naming").
#
# Allowed `<type>` set: feat, fix, refactor, test, chore, docs, hotfix.
# Slug must be lowercase kebab-case (a-z, 0-9, hyphen), 2-60 chars.
#
# `main` and `develop` are exempt — pushing to those is governed by
# branch protection, not by name lint.

set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"

if [[ -z "$branch" || "$branch" == "HEAD" ]]; then
  echo "branch-name-lint: skipping (detached HEAD)"
  exit 0
fi

case "$branch" in
  main|master|develop)
    exit 0
    ;;
esac

pattern='^(feat|fix|refactor|test|chore|docs|hotfix)/[a-z0-9][a-z0-9-]{1,59}[a-z0-9]$'

if [[ ! "$branch" =~ $pattern ]]; then
  cat >&2 <<EOF
branch-name-lint: rejecting "$branch".

Branch names must match:
  <type>/<short-kebab-slug>

Allowed types: feat, fix, refactor, test, chore, docs, hotfix.
Slug: lowercase kebab-case (a-z, 0-9, hyphen), 3-61 chars, no trailing hyphen.

Examples:
  feat/sso-mock
  fix/login-redirect
  docs/branching-policy-compliance
  chore/github-chrome
  hotfix/iam-startup-guard

Rename with:  git branch -m <new-name>

(See: https://github.com/Interval-Col/.github/blob/main/BRANCHING-AND-DEPLOY.md#branch-naming)
EOF
  exit 1
fi

exit 0
