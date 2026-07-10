#!/usr/bin/env bash
# =============================================================================
# sync-pharos-registry.sh — copy the shared Pháros design-system foundation
# into a consuming app (RFC 0008 Q3: copy-in registry, NOT a runtime package).
#
# Syncs: tokens.css (+ .sha256 drift sidecar) · the 8 gate scripts (check-*.mjs)
#        · eslint.config.mjs template · pharos-lint-check.yml (its working-directory
#        + pnpm cache path auto-set to the app's FE subdir) · registry/app/**.
#
# Does NOT overwrite: the app's .pre-commit-config.yaml or main ci.yml (those
# carry org policy hooks and backend/test jobs — see pre-commit.snippet.yaml).
#
# Components: registry/app/** (the live beacon now; shell / AppLogo / ui primitives
# as they land) is mirrored into the consuming app's app/** at the same paths.
#
# Usage:
#   scripts/sync-pharos-registry.sh [--dry-run] <app-fe-dir> [repo-root]
#
#   <app-fe-dir>   The directory that CONTAINS app/ (e.g. frontend,
#                  lab-qc/frontend, or the repo root for single-app repos
#                  like admission-patient). REQUIRED.
#   [repo-root]    Where .github/workflows/ lives. Defaults to <app-fe-dir>
#                  (correct for single-app repos). Pass the repo root for
#                  monorepos (e.g. the checkout root when fe is under frontend/).
#   --dry-run      Print what WOULD be copied; write nothing.
# =============================================================================
set -euo pipefail

REGISTRY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../brands/pharos_brand/registry" && pwd)"

# ── Argument parsing ─────────────────────────────────────────────────────────
DRY_RUN=false
POSITIONAL=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) POSITIONAL+=("$arg") ;;
  esac
done

APP_FE_DIR="${POSITIONAL[0]:?usage: sync-pharos-registry.sh [--dry-run] <app-fe-dir> [repo-root]}"
REPO_ROOT="${POSITIONAL[1]:-$APP_FE_DIR}"

if [[ ! -d "$APP_FE_DIR" ]]; then
  echo "error: app-fe-dir not found: $APP_FE_DIR" >&2
  exit 1
fi
if [[ ! -d "$REPO_ROOT" ]]; then
  echo "error: repo-root not found: $REPO_ROOT" >&2
  exit 1
fi

# Resolve to absolute paths so the monorepo FE-subdir can be derived.
APP_FE_DIR="$(cd "$APP_FE_DIR" && pwd)"
REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"

# FE dir relative to the repo root — drives the copied workflow's
# working-directory + pnpm cache-dependency-path, so the CI works for monorepos
# (e.g. lab-qc/frontend, frontend) AND single-app repos (FE_REL=".") with NO
# manual patching that a re-sync would clobber.
if [[ "$APP_FE_DIR" == "$REPO_ROOT" ]]; then
  FE_REL="."
else
  FE_REL="${APP_FE_DIR#"$REPO_ROOT/"}"
  if [[ "$FE_REL" == /* || "$FE_REL" == "$APP_FE_DIR" ]]; then
    echo "error: app-fe-dir ($APP_FE_DIR) is not inside repo-root ($REPO_ROOT)" >&2
    exit 1
  fi
fi

# ── Copy helper ──────────────────────────────────────────────────────────────
copy_file() {
  local src="$1"
  local dest="$2"
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "[dry-run] would copy: $src -> $dest"
  else
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    echo "synced: $src -> $dest"
  fi
}

# ── 1. tokens.css ────────────────────────────────────────────────────────────
copy_file \
  "$REGISTRY_DIR/tokens.css" \
  "$APP_FE_DIR/app/assets/css/pharos-tokens.css"

# ── 1b. token-drift sidecar — sha256 of the registry source (check-token-drift) ─
TOKENS_SHA_DEST="$APP_FE_DIR/app/assets/css/pharos-tokens.css.sha256"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] would write: $TOKENS_SHA_DEST"
else
  ( cd "$REGISTRY_DIR" && shasum -a 256 tokens.css | awk '{print $1}' ) > "$TOKENS_SHA_DEST"
  echo "wrote:  $TOKENS_SHA_DEST"
fi

# ── 2. Gate scripts ──────────────────────────────────────────────────────────
for script in "$REGISTRY_DIR/scripts"/check-*.mjs; do
  copy_file "$script" "$APP_FE_DIR/scripts/$(basename "$script")"
done

# ── 3. ESLint config template ────────────────────────────────────────────────
copy_file \
  "$REGISTRY_DIR/eslint.config.mjs" \
  "$APP_FE_DIR/eslint.config.mjs"

# ── 4. Dedicated lint-check workflow (working-directory parameterized per app) ─
# Single-app repos keep the template's `.`; monorepos get FE_REL substituted in,
# so the copied CI runs in the right dir + caches the right lockfile.
WORKFLOW_SRC="$REGISTRY_DIR/.github/workflows/pharos-lint-check.yml"
WORKFLOW_DEST="$REPO_ROOT/.github/workflows/pharos-lint-check.yml"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] would copy: $WORKFLOW_SRC -> $WORKFLOW_DEST (working-directory=$FE_REL)"
elif [[ "$FE_REL" == "." ]]; then
  mkdir -p "$(dirname "$WORKFLOW_DEST")"
  cp "$WORKFLOW_SRC" "$WORKFLOW_DEST"
  echo "synced: $WORKFLOW_SRC -> $WORKFLOW_DEST (working-directory=.)"
else
  mkdir -p "$(dirname "$WORKFLOW_DEST")"
  sed -e "s#working-directory: \.#working-directory: $FE_REL#g" \
      -e "s#cache-dependency-path: pnpm-lock\.yaml#cache-dependency-path: $FE_REL/pnpm-lock.yaml#g" \
      "$WORKFLOW_SRC" > "$WORKFLOW_DEST"
  echo "synced: $WORKFLOW_SRC -> $WORKFLOW_DEST (working-directory=$FE_REL)"
fi

# ── 4b. Component tree — beacon (+ shell / lockup / ui primitives as they land) ─
# Mirrors registry/app/** into the consuming app's app/** at the same paths.
#
# EXCEPTION — app-owned PRESETS. The EntityLookup presets (PatientLookup /
# PhysicianLookup) are SCAFFOLDS: each consuming app wires their `searchFn` to its
# OWN endpoints, so they MUST diverge from the registry's mock versions. The
# registry copy is a starting point an app copies ONCE; re-syncing it would CLOBBER
# the app's real-endpoint wiring. So the sync SKIPS them — they are app-owned after
# first adoption. (The primitives they build on — EntityLookup, ScopedSearchInput —
# ARE synced verbatim.) If a preset's reusable shell needs changing, make it
# prop-driven in the registry instead.
SYNC_SKIP_RELPATHS=(
  "components/ui/entity-lookup/PatientLookup.vue"
  "components/ui/entity-lookup/PhysicianLookup.vue"
)
if [[ -d "$REGISTRY_DIR/app" ]]; then
  while IFS= read -r src; do
    rel="${src#"$REGISTRY_DIR/app/"}"
    skip=false
    for skip_rel in "${SYNC_SKIP_RELPATHS[@]}"; do
      [[ "$rel" == "$skip_rel" ]] && { skip=true; break; }
    done
    if [[ "$skip" == "true" ]]; then
      echo "skip (app-owned preset): $rel"
      continue
    fi
    copy_file "$src" "$APP_FE_DIR/app/$rel"
  done < <(find "$REGISTRY_DIR/app" -type f)
fi

# ── 4c. Registry drift manifest (check-registry-drift / RFC 0016 Lock 3) ──────
# sha256 of every synced registry file so an app can't silently hand-edit a
# copied primitive. Excludes the app-owned presets (meant to diverge).
MANIFEST_DEST="$APP_FE_DIR/app/assets/pharos-registry.sha256"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] would write registry drift manifest: $MANIFEST_DEST"
elif [[ -d "$REGISTRY_DIR/app" ]]; then
  mkdir -p "$(dirname "$MANIFEST_DEST")"
  : > "$MANIFEST_DEST"
  while IFS= read -r src; do
    rel="${src#"$REGISTRY_DIR/app/"}"
    skip=false
    for skip_rel in "${SYNC_SKIP_RELPATHS[@]}"; do
      [[ "$rel" == "$skip_rel" ]] && { skip=true; break; }
    done
    [[ "$skip" == "true" ]] && continue
    printf '%s  %s\n' "$(shasum -a 256 "$src" | awk '{print $1}')" "$rel" >> "$MANIFEST_DEST"
  done < <(find "$REGISTRY_DIR/app" -type f | sort)
  echo "wrote:  $MANIFEST_DEST ($(grep -c . "$MANIFEST_DEST") entries)"
fi

# ── 5. Pre-commit: never overwrite — print merge instructions ─────────────────
echo
echo "─────────────────────────────────────────────────────────────────────────"
echo "pre-commit: DO NOT overwrite the app's .pre-commit-config.yaml."
echo "  Merge the block from:"
echo "    $REGISTRY_DIR/pre-commit.snippet.yaml"
echo "  into: $REPO_ROOT/.pre-commit-config.yaml"
echo "─────────────────────────────────────────────────────────────────────────"

# ── 6. Manual follow-ups ──────────────────────────────────────────────────────
echo
echo "Manual follow-ups required in the app:"
echo
echo "  a) Import the registry CSS in app/assets/css/main.css:"
echo "       @import \"./pharos-tokens.css\";       /* token contract */"
echo "       @import \"./pharos-components.css\";   /* component layer (pilot light, …) */"
echo "       @import \"./pharos-icons.css\";        /* <Icon> safelist + @iconify plugin */"
echo
echo "  a2) Component-library adoption deps (per primitive used):"
echo "       <Icon>      → pnpm add -D @iconify-json/lucide @iconify-json/material-symbols @iconify/tailwind"
echo "       <DatePicker>→ pnpm add @internationalized/date"
echo "       (per-collection icon pkgs only — never @iconify/json; check-fe-bloat-safe)"
echo
echo "  b) Load the four Pháros fonts (via @nuxt/fonts or a CDN link):"
echo "       Fraunces · DM Sans · IBM Plex Mono · JetBrains Mono"
echo "     See registry/frontend-standards.md for the @nuxt/fonts config."
echo
echo "  c) Add the sub-brand theme class to <html> in app.vue / nuxt.config:"
echo "       .theme-numeros | .theme-clinico | .theme-deportivo | .theme-recepcion | .theme-clientes | .theme-ti"
echo "     (Default/neutral = no class — LCH Navy.)"
echo
echo "  d) Ensure package.json has the lint-check script. Add if missing:"
echo "       \"lint-check\": \"eslint . --max-warnings 0 && node scripts/check-no-scoped-pages.mjs && node scripts/check-no-raw-html.mjs && node scripts/check-no-hex-colors.mjs && node scripts/check-no-palette-colors.mjs && node scripts/check-token-drift.mjs && node scripts/check-registry-drift.mjs && node scripts/check-contrast.mjs && node scripts/check-font-allowlist.mjs && node scripts/check-fe-bloat.mjs\""
echo
echo "  e) Install ESLint + generate Nuxt types:"
echo "       pnpm add -D @nuxt/eslint"
echo "     Ensure nuxt prepare runs before lint (postinstall hook recommended):"
echo "       \"postinstall\": \"nuxt prepare\""
echo "     The eslint.config.mjs template imports from ./.nuxt/eslint.config.mjs"
echo "     which is generated by nuxt prepare."
echo
