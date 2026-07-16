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
ADD_LIST=()          # --add <relpath>: adopt a NEW registry file (else: refresh what you have)
PERSONA_DIR=""       # --persona-dir <backend-chat-dir>: refresh the Nerea persona fragment there
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)        DRY_RUN=true; shift ;;
    --add)            ADD_LIST+=("$2"); shift 2 ;;
    --add=*)          ADD_LIST+=("${1#--add=}"); shift ;;
    --persona-dir)    PERSONA_DIR="$2"; shift 2 ;;
    --persona-dir=*)  PERSONA_DIR="${1#--persona-dir=}"; shift ;;
    *)                POSITIONAL+=("$1"); shift ;;
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

# ── 4b. Component tree — "refresh what you have" (adoption-aware) ──────────────
# Mirrors registry/app/** into the app's app/**, but ONLY the files the app has
# already ADOPTED (present in app/) — plus any `--add <relpath>` — so a selective
# consumer isn't force-fed the whole registry. Three file categories:
#   • verbatim  → refreshed + recorded in the drift manifest (Lock 3).
#   • scaffold  → app-owned after first adoption (the EntityLookup presets, the
#                 AppLogo, the shell layout, the menu example, the health-beacon
#                 plugin). Never overwritten, never in the manifest.
#   • adapted   → a shared primitive an app deliberately tuned, marked in-file
#                 with `pharos-registry:keep`. Preserved (not overwritten),
#                 excluded from the manifest — the documented escape hatch (e.g.
#                 finance-lch's denser SearchableSelect anchor).
SCAFFOLD_SKIP_RELPATHS=(
  "components/ui/entity-lookup/PatientLookup.vue"
  "components/ui/entity-lookup/PhysicianLookup.vue"
  "components/AppLogo.vue"
  "layouts/default.vue"
  "navigation/menu.example.ts"
  "plugins/health-beacon.client.ts"
)
KEEP_MARKER="pharos-registry:keep"

is_scaffold() {
  local rel="$1" s
  for s in "${SCAFFOLD_SKIP_RELPATHS[@]}"; do [[ "$rel" == "$s" ]] && return 0; done
  return 1
}
is_added() {
  local rel="$1" a
  [[ ${#ADD_LIST[@]} -eq 0 ]] && return 1
  for a in "${ADD_LIST[@]}"; do [[ "$rel" == "$a" ]] && return 0; done
  return 1
}

# ── Companion files — "importer:sibling" ───────────────────────────────────────
# A registry component that imports a sibling must NEVER land without it: this sync is
# adoption-aware, so an app that adopted the importer but never `--add`'d the sibling would get the
# importer refreshed and the sibling silently skipped — a broken import, at the next routine sync,
# with no flag flipped by anyone. So the sibling FOLLOWS the importer: if the importer is present in
# the app (or is being --add'd this run), the sibling comes too, whether or not anyone remembered it.
COMPANIONS=(
  "components/PharosHelpChat.vue:components/PharosChatAvatar.vue"   # imports ./PharosChatAvatar.vue
)
is_companion_required() {
  local rel="$1" pair importer companion
  for pair in "${COMPANIONS[@]}"; do
    importer="${pair%%:*}"; companion="${pair##*:}"
    [[ "$rel" == "$companion" ]] || continue
    [[ -f "$APP_FE_DIR/app/$importer" ]] && return 0   # importer already adopted
    is_added "$importer" && return 0                   # importer being added right now
  done
  return 1
}

MANIFEST_DEST="$APP_FE_DIR/app/assets/pharos-registry.sha256"
MANIFEST_TMP="$(mktemp)"
if [[ -d "$REGISTRY_DIR/app" ]]; then
  while IFS= read -r src; do
    rel="${src#"$REGISTRY_DIR/app/"}"
    dest="$APP_FE_DIR/app/$rel"
    # scaffold → app-owned, never touched
    if is_scaffold "$rel"; then
      [[ -f "$dest" ]] && echo "skip (app-owned scaffold): $rel"
      continue
    fi
    # not adopted (absent), not explicitly --add'd, and not required by an adopted importer → leave out
    if [[ ! -f "$dest" ]] && ! is_added "$rel" && ! is_companion_required "$rel"; then
      continue
    fi
    # pulled in only because an adopted component imports it — say so, it wasn't asked for
    if [[ ! -f "$dest" ]] && ! is_added "$rel" && is_companion_required "$rel"; then
      echo "companion (required by an adopted component): $rel"
    fi
    # adopted-but-adapted → preserve the app's version, keep it out of the manifest
    if [[ -f "$dest" ]] && grep -qF "$KEEP_MARKER" "$dest" 2>/dev/null; then
      echo "keep (app adaptation, $KEEP_MARKER): $rel"
      continue
    fi
    # verbatim → refresh + record in the drift manifest
    copy_file "$src" "$dest"
    printf '%s  %s\n' "$(shasum -a 256 "$src" | awk '{print $1}')" "$rel" >> "$MANIFEST_TMP"
  done < <(find "$REGISTRY_DIR/app" -type f | sort)
fi

# ── 4c. Registry drift manifest (check-registry-drift / RFC 0016 Lock 3) ──────
# sha256 of every VERBATIM file this sync refreshed (scaffold + adapted excluded)
# so Lock 3 flags a hand-edit WITHOUT false MISSING on un-adopted files.
if [[ "$DRY_RUN" == "true" ]]; then
  echo "[dry-run] would write registry drift manifest: $MANIFEST_DEST ($(grep -c . "$MANIFEST_TMP" 2>/dev/null || echo 0) entries)"
  rm -f "$MANIFEST_TMP"
else
  mkdir -p "$(dirname "$MANIFEST_DEST")"
  sort "$MANIFEST_TMP" > "$MANIFEST_DEST"
  rm -f "$MANIFEST_TMP"
  echo "wrote:  $MANIFEST_DEST ($(grep -c . "$MANIFEST_DEST") entries)"
fi

# ── 4d. Nerea persona fragment (backend, chat-contract H9) ────────────────────
# The BE half of the persona: registry/prompts/nerea_persona.py is copied verbatim
# into the app's backend chat dir (--persona-dir). Enforcement is NOT Lock 3 (that
# manifest is FE-scoped): chat-contract-check H9 compares the app copy byte-for-byte
# against the registry canon when the manifest declares `persona: nerea`.
if [[ -n "$PERSONA_DIR" ]]; then
  if [[ ! -d "$PERSONA_DIR" ]]; then
    echo "error: --persona-dir not found: $PERSONA_DIR" >&2
    exit 1
  fi
  copy_file "$REGISTRY_DIR/prompts/nerea_persona.py" "$PERSONA_DIR/nerea_persona.py"
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
