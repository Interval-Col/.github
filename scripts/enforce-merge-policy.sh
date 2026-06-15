#!/usr/bin/env bash
# =============================================================================
# enforce-merge-policy.sh — bring LIVE GitHub repo settings in line with the org
# merge policy (BRANCHING-AND-DEPLOY.md → "Merge mode"): MERGE-COMMIT ONLY,
# squash + rebase disabled, branches auto-deleted on merge, and — on protected
# branches — "Require linear history" turned OFF (it contradicts merge-commit).
#
# The docs are the target state; this is the one-shot to make live repos match.
# Idempotent — safe to re-run. Requires the `gh` CLI authenticated with admin
# on the repos.
#
#   scripts/enforce-merge-policy.sh             # all GitHub repos in the list
#   scripts/enforce-merge-policy.sh lab-qc      # just one (or several) repos
#   DRY_RUN=1 scripts/enforce-merge-policy.sh   # print actions, change nothing
#
# Scope: GitHub (Interval-Col) only. Bitbucket repos (master-default) are not
# covered here.
# =============================================================================
set -euo pipefail

ORG="Interval-Col"
DRY_RUN="${DRY_RUN:-0}"

# GitHub repos per the workspace map (~/dev/CLAUDE.md). Update as the org grows.
REPOS=(
  .github infrastructure nucleus-db operations rfcs
  finance-lch lab-qc commercial-lch admission-patient
  biuman-lis biuman-reports cobol-migration legacy-repositories
)
[[ $# -gt 0 ]] && REPOS=("$@")

run() { if [[ "$DRY_RUN" == "1" ]]; then echo "  DRY: $*"; else "$@"; fi; }

for r in "${REPOS[@]}"; do
  echo "== ${ORG}/${r} =="

  # 1) Repo-level merge buttons: merge-commit only, auto-delete head branches.
  if run gh api -X PATCH "repos/${ORG}/${r}" \
        -F allow_merge_commit=true \
        -F allow_squash_merge=false \
        -F allow_rebase_merge=false \
        -F delete_branch_on_merge=true \
        --silent; then
    echo "  merge buttons → merge-commit only; auto-delete on merge"
  else
    echo "  !! could not patch repo settings (admin rights? repo exists?)"
  fi

  # 2) Drop "Require linear history" on protected branches (contradicts merge-commit).
  for b in main develop; do
    if gh api "repos/${ORG}/${r}/branches/${b}/protection" >/dev/null 2>&1; then
      if run gh api -X DELETE \
            "repos/${ORG}/${r}/branches/${b}/protection/required_linear_history" \
            >/dev/null 2>&1; then
        echo "  ${b}: linear-history requirement removed"
      else
        echo "  ${b}: no linear-history requirement to remove"
      fi
    fi
  done
done
echo "done."
