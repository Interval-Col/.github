#!/usr/bin/env node
/**
 * CI gate: forbid Tailwind palette utilities (text-green-600,
 * bg-amber-100, border-blue-500, etc.) in app code outside vendored
 * shadcn primitives. Use semantic tokens instead.
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * Why: every time a status pill or hover state lands with a raw palette
 * color, dark-mode and brand-theming break. The semantic tokens
 * defined in app/assets/css/main.css (--success, --warning,
 * --destructive, --primary, --muted, --accent, --foreground, --border,
 * etc.) shift correctly between themes; the raw palette doesn't.
 *
 * Banned class root + palette combinations:
 *   {prop}-{color}-{shade}
 *
 *   prop  ∈ text bg border ring outline fill stroke from to via
 *           placeholder caret accent decoration divide shadow
 *   color ∈ slate gray zinc neutral stone red orange amber yellow
 *           lime green emerald teal cyan sky blue indigo violet
 *           purple fuchsia pink rose
 *   shade ∈ 50, 100, 200, … 950
 *
 * Mapping table (most common cases) — use these substitutions:
 *
 *   Raw                          → Semantic
 *   ─────────────────────────────┼──────────────────────────────────
 *   bg-green-100  text-green-800 │ bg-success/15 text-success
 *   bg-red-100    text-red-800   │ bg-destructive/15 text-destructive
 *   bg-amber-100  text-amber-800 │ bg-warning/15 text-warning
 *   bg-blue-100   text-blue-800  │ bg-primary/15 text-primary
 *   text-green-600               │ text-success
 *   text-red-600                 │ text-destructive
 *   text-amber-600 / yellow-*    │ text-warning
 *   text-blue-600                │ text-primary
 *
 * What this gate ignores:
 *   - app/components/ui/         vendored shadcn primitives may use
 *                                palette references in their default
 *                                variant maps (we keep them verbatim
 *                                so future scaffolds don't drift)
 *   - app/lib/api/generated/     openapi-ts output (none here, kept for parity)
 *   - lines containing `lint-allow-palette` (escape-hatch)
 *
 * Ported from finance-lch/frontend/scripts (RFC 0008 §6 design gates).
 */
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = resolve(__dirname, '..')
const SCAN_ROOT = join(REPO_ROOT, 'app')

const IGNORE_PATH_FRAGMENTS = [
  'app/components/ui/',
  'app/lib/api/generated/',
]

const SCAN_EXTS = new Set(['.vue', '.ts'])

const PROPS = 'text|bg|border|ring|outline|fill|stroke|from|to|via|placeholder|caret|accent|decoration|divide|shadow'
const COLORS = 'slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose'
// `\b` boundaries on both sides; allow optional `dark:` / `hover:` /
// `focus-visible:` etc. modifier prefixes (caught by the `\b` itself
// because `:` is a non-word char).
const PALETTE_RE = new RegExp(`\\b(?:${PROPS})-(?:${COLORS})-\\d{2,3}\\b`, 'g')
const ESCAPE_HATCH = /lint-allow-palette/

function* walk(root) {
  let entries
  try { entries = readdirSync(root) } catch { return }
  for (const name of entries) {
    if (name.startsWith('.')) continue
    const full = join(root, name)
    const s = statSync(full)
    if (s.isDirectory()) {
      yield* walk(full)
    } else if (s.isFile()) {
      const ext = name.slice(name.lastIndexOf('.'))
      if (SCAN_EXTS.has(ext)) yield full
    }
  }
}

function shouldIgnore(rel) {
  for (const frag of IGNORE_PATH_FRAGMENTS) {
    if (rel.startsWith(frag)) return true
  }
  return false
}

const offenders = []

for (const file of walk(SCAN_ROOT)) {
  const rel = relative(REPO_ROOT, file)
  if (shouldIgnore(rel)) continue
  const text = readFileSync(file, 'utf8')
  const lines = text.split('\n')

  // Block-scoped escape hatch: a `lint-allow-palette` comment exempts
  // its own line plus every following non-blank line up to the next
  // blank line. So putting the marker once above an array literal or
  // class map ignores the whole block, not just the comment line.
  let inAllowBlock = false
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (line.trim() === '') {
      inAllowBlock = false
      continue
    }
    if (ESCAPE_HATCH.test(line)) {
      inAllowBlock = true
      continue
    }
    if (inAllowBlock) continue
    PALETTE_RE.lastIndex = 0
    const m = line.match(PALETTE_RE)
    if (!m) continue
    offenders.push({ rel, lineNumber: i + 1, content: line.trim(), matches: m })
  }
}

if (offenders.length) {
  console.error()
  console.error(`[no-palette-colors] ${offenders.length} site(s) use raw Tailwind palette utilities outside app/components/ui/:`)
  for (const o of offenders) {
    console.error(`  - ${o.rel}:${o.lineNumber}  [${o.matches.join(', ')}]  ${o.content.slice(0, 80)}${o.content.length > 80 ? '…' : ''}`)
  }
  console.error()
  console.error('Replace with semantic tokens (bg-success, text-destructive, bg-warning, text-primary, …). See the mapping table at the top of this script.')
  process.exit(1)
}

console.log(`[no-palette-colors] OK — 0 raw palette utilities outside app/components/ui/`)
