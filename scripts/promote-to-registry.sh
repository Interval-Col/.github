#!/usr/bin/env bash
# =============================================================================
# promote-to-registry.sh — promote a primitive prototyped in the design-studio
# playground INTO the Pháros registry. The inverse of sync-pharos-registry.sh:
#
#     sync-pharos-registry.sh   registry/app/**  ──>  a consuming app's app/**
#     promote-to-registry.sh    design-studio app/**  ──>  registry/app/**
#
# This is the missing last-mile of the RFC 0008 co-creation loop: design-studio
# CONSUMES the registry (copy-in) and exports spec/*.md via regen-spec, but has
# no path to push a ratified composed SFC/composable back into registry/app/.
#
# MANUAL-ASSISTED v1 (decided 2026-06-28): this script STAGES the copy and shows
# the diff. It NEVER commits, pushes, or opens a PR — you review the working tree
# and open the registry PR yourself (@gczuluaga is the sole registry approver).
#
# Usage:
#   scripts/promote-to-registry.sh [--dry-run] <design-studio-dir> <path-under-app>...
#
#   <design-studio-dir>  The design-studio checkout (the dir that CONTAINS app/).
#                        REQUIRED.
#   <path-under-app>     One or more paths UNDER app/, each a file or a directory:
#                        components/ui/SearchableSelect.vue
#                        components/EntityLookup            (a directory)
#                        composables/useFlow.ts
#                        REQUIRED (at least one).
#   --dry-run            Print what WOULD be promoted (with diffs); write nothing.
#
# Examples:
#   scripts/promote-to-registry.sh --dry-run ../design-studio composables/useFlow.ts
#   scripts/promote-to-registry.sh ../design-studio components/ui/SearchableSelect.vue
# =============================================================================
set -euo pipefail

REGISTRY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../brands/pharos_brand/registry" && pwd)"

# ── Argument parsing ─────────────────────────────────────────────────────────
DRY_RUN=false
POSITIONAL=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    -h|--help) sed -n '2,40p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) POSITIONAL+=("$arg") ;;
  esac
done

STUDIO_DIR="${POSITIONAL[0]:?usage: promote-to-registry.sh [--dry-run] <design-studio-dir> <path-under-app>...}"
REL_PATHS=("${POSITIONAL[@]:1}")
if [[ ${#REL_PATHS[@]} -eq 0 ]]; then
  echo "error: give at least one <path-under-app> (e.g. composables/useFlow.ts)" >&2
  exit 1
fi
if [[ ! -d "$STUDIO_DIR/app" ]]; then
  echo "error: no app/ dir under design-studio-dir: $STUDIO_DIR" >&2
  exit 1
fi
STUDIO_APP="$(cd "$STUDIO_DIR/app" && pwd)"

# ── Helpers ──────────────────────────────────────────────────────────────────
# Print a unified diff of an incoming source against the current registry copy
# (or mark it NEW), so a human can review before promoting.
show_diff() {
  local src="$1" dest="$2"
  if [[ -f "$dest" ]]; then
    if diff -q "$dest" "$src" >/dev/null 2>&1; then
      echo "  = unchanged: app/${src#"$STUDIO_APP/"}"
    else
      echo "  ~ CHANGED:   app/${src#"$STUDIO_APP/"}"
      diff -u "$dest" "$src" | sed 's/^/      /' || true
    fi
  else
    echo "  + NEW:       app/${src#"$STUDIO_APP/"}"
  fi
}

copy_file() {
  local src="$1" dest="$2"
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[dry-run] would promote: $src -> $dest"
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "promoted: app/${src#"$STUDIO_APP/"} -> registry/app/${dest#"$REGISTRY_DIR/app/"}"
  fi
}

# Flag imports that reference playground-only modules — these do NOT exist in a
# consuming app and would break after sync. We SURFACE them (manual-assisted);
# we never auto-rewrite. Tune the pattern as the playground's layout evolves.
# Matches both explicit playground import paths AND the bare auto-imported
# `usePlayground()` store accessor (Nuxt auto-imports have no import line).
PORTABILITY_PATTERN='(stores/playground|/playground|lib/spec|~/stores|@/stores|\.\./stores|usePlayground)'
PORTABILITY_HITS=()
portability_scan() {
  local src="$1"
  local hits
  hits="$(grep -nE "$PORTABILITY_PATTERN" "$src" 2>/dev/null || true)"
  if [[ -n "$hits" ]]; then
    PORTABILITY_HITS+=("app/${src#"$STUDIO_APP/"}:")
    while IFS= read -r line; do PORTABILITY_HITS+=("    $line"); done <<< "$hits"
  fi
}

# ── Collect source files ─────────────────────────────────────────────────────
SRC_FILES=()
for rel in "${REL_PATHS[@]}"; do
  rel="${rel#app/}"            # tolerate a leading app/ in the argument
  src="$STUDIO_APP/$rel"
  if [[ -f "$src" ]]; then
    SRC_FILES+=("$src")
  elif [[ -d "$src" ]]; then
    while IFS= read -r f; do SRC_FILES+=("$f"); done < <(find "$src" -type f | sort)
  else
    echo "error: not found under design-studio app/: $rel" >&2
    exit 1
  fi
done

if [[ ${#SRC_FILES[@]} -eq 0 ]]; then
  echo "error: no files resolved from the given paths." >&2
  exit 1
fi

# ── Review (diffs) ───────────────────────────────────────────────────────────
echo "─────────────────────────────────────────────────────────────────────────"
echo "Promoting from: $STUDIO_APP"
echo "            to: $REGISTRY_DIR/app"
echo "         files: ${#SRC_FILES[@]}"
echo "─────────────────────────────────────────────────────────────────────────"
echo "Review:"
for src in "${SRC_FILES[@]}"; do
  rel="${src#"$STUDIO_APP/"}"
  show_diff "$src" "$REGISTRY_DIR/app/$rel"
  portability_scan "$src"
done

# ── Portability warnings ─────────────────────────────────────────────────────
if [[ ${#PORTABILITY_HITS[@]} -gt 0 ]]; then
  echo
  echo "⚠️  PORTABILITY — these reference playground-only modules that will NOT"
  echo "    exist in a consuming app. Refactor them out before promoting:"
  printf '    %s\n' "${PORTABILITY_HITS[@]}"
fi

# ── Copy ─────────────────────────────────────────────────────────────────────
echo
for src in "${SRC_FILES[@]}"; do
  rel="${src#"$STUDIO_APP/"}"
  copy_file "$src" "$REGISTRY_DIR/app/$rel"
done

# ── Manual-assisted footer (NO commit, NO PR) ────────────────────────────────
echo
echo "─────────────────────────────────────────────────────────────────────────"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "dry-run: nothing written. Re-run without --dry-run to stage the copy."
else
  echo "Staged into the registry working tree. NOT committed — review + open the PR:"
  echo
  echo "  1. Review the diff:        git -C \"$REGISTRY_DIR\" diff -- app"
  echo "  2. Verify it still syncs:  scripts/sync-pharos-registry.sh --dry-run <an-app-fe-dir>"
  echo "  3. Branch + commit ONLY the registry files you promoted:"
  echo "       git switch -c feat/pharos-ui-<primitive>"
  echo "       git add brands/pharos_brand/registry/app/<paths>"
  echo "       git commit -m \"feat(pharos-ui): promote <primitive> to the registry\""
  echo "  4. Open a registry PR for @gczuluaga (sole registry approver)."
  echo
  echo "  Add the matching adoption gate (registry/scripts/check-*.mjs) in WARN mode"
  echo "  and a surface doc (registry/surfaces/*.md) in the same PR — see the plan."
fi
echo "─────────────────────────────────────────────────────────────────────────"
