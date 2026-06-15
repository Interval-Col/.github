#!/usr/bin/env bash
# =============================================================================
# sync-pharos-registry.sh — copy the shared Pháros design-system foundation into
# a consuming app (RFC 0008 Q3: copy-in registry, NOT a runtime package).
#
# Skeleton. Phase 1 will extend this to also sync the shadcn-vue component set
# once the component library is built (it is intentionally not built yet — see
# brands/pharos_brand/registry/README.md "Decided vs open").
#
# Usage:
#   scripts/sync-pharos-registry.sh <path-to-app-repo>
#
# Copies:
#   brands/pharos_brand/registry/tokens.css  ->  <app>/app/assets/css/pharos-tokens.css
#
# The app then `@import`s pharos-tokens.css from its main.css and themes its
# sub-brand by overriding only the accent slots (--primary/--accent/--ring/
# --sidebar-primary). See registry/README.md.
# =============================================================================
set -euo pipefail

REGISTRY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../brands/pharos_brand/registry" && pwd)"
APP_DIR="${1:?usage: sync-pharos-registry.sh <path-to-app-repo>}"

if [[ ! -d "$APP_DIR" ]]; then
  echo "error: app dir not found: $APP_DIR" >&2
  exit 1
fi

DEST_CSS_DIR="$APP_DIR/app/assets/css"
mkdir -p "$DEST_CSS_DIR"
cp "$REGISTRY_DIR/tokens.css" "$DEST_CSS_DIR/pharos-tokens.css"
echo "synced tokens.css -> $DEST_CSS_DIR/pharos-tokens.css"

echo
echo "Next steps in the app:"
echo "  1. @import \"./pharos-tokens.css\";  in app/assets/css/main.css"
echo "  2. Load Fraunces + Inter + IBM Plex Mono (see registry/frontend-standards.md)"
echo "  3. Override ONLY the accent slots for this sub-brand"
echo "  4. Toggle light/dark with the shadcn .dark class"
echo
echo "TODO (Phase 1): sync the shadcn-vue component set once built."
