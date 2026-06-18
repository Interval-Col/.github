#!/usr/bin/env node
/**
 * CI gate: forbid hardcoded hex color literals outside the design-token
 * source of truth.
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * The token hierarchy:
 *   1. Brand primitives in @theme {}        — `--color-pharos-burgundy`, etc.
 *   2. Semantic vars in :root / .dark       — `--background`, `--foreground`,
 *                                              `--primary`, `--success`, etc.
 *   3. Tailwind utilities in @theme inline  — `bg-background`, `text-success`,
 *                                              `border-border`, etc.
 *
 * All three layers live in `app/assets/css/main.css`. Every other file
 * — pages, layouts, components, composables, scripts — must consume the
 * Tailwind utility (preferred) or the CSS var (when reading at runtime).
 *
 * What this gate flags:
 *   - `#ff8200`, `#3a0a17` … : 6-digit hex literals
 *   - `#fff`, `#ffe`         : 3-digit hex literals
 *
 * Where the gate scans:
 *   - app/ (recursive) for .vue / .ts / .js / .mjs / .css files
 *
 * Where the gate ignores:
 *   - app/assets/css/         design-token source of truth
 *   - app/components/ui/      vendored shadcn-vue primitives — keep verbatim
 *   - app/lib/api/generated/  openapi-ts output (none here, kept for parity)
 *   - lines containing `lint-allow-hex` (escape-hatch comment for genuinely-
 *     necessary literals that don't belong in a token)
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
  'app/assets/',
  'app/components/ui/',
  'app/lib/api/generated/',
]

// Per-file allowlist — app-specific exceptions go here
const ALLOWLIST = new Set([
  // app-specific exceptions go here
])

const SCAN_EXTS = new Set(['.vue', '.ts', '.js', '.mjs', '.css'])
const HEX_RE = /#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b/g
const ESCAPE_HATCH = /lint-allow-hex/

// `var(--foo, #fallback)` is a legitimate CSS pattern: it provides a
// default for environments where the custom property hasn't been
// defined. Treat the `#fallback` arg as a token of last resort, not a
// raw color literal that needs migrating.
const VAR_FALLBACK_RE = /\bvar\s*\(\s*--[\w-]+\s*,\s*#[0-9a-fA-F]{3,6}\s*\)/g

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
const allowlistHits = new Map()

for (const file of walk(SCAN_ROOT)) {
  const rel = relative(REPO_ROOT, file)
  if (shouldIgnore(rel)) continue
  const text = readFileSync(file, 'utf8')
  const lines = text.split('\n')
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    if (ESCAPE_HATCH.test(line)) continue
    // Strip out `var(--foo, #fallback)` patterns first — those are
    // legitimate CSS custom-property fallbacks, not raw color literals.
    line = line.replace(VAR_FALLBACK_RE, '')
    HEX_RE.lastIndex = 0
    const m = line.match(HEX_RE)
    if (!m) continue
    if (ALLOWLIST.has(rel)) {
      allowlistHits.set(rel, (allowlistHits.get(rel) ?? 0) + m.length)
      continue
    }
    offenders.push({ rel, lineNumber: i + 1, content: line.trim(), matches: m })
  }
}

if (allowlistHits.size > 0) {
  console.log(`[no-hex-colors] ${allowlistHits.size} allowlisted file(s) still contain hex literals:`)
  for (const [rel, count] of allowlistHits) {
    console.log(`  - ${rel} (${count} hit${count === 1 ? '' : 's'})`)
  }
}

if (offenders.length) {
  console.error()
  console.error(`[no-hex-colors] ${offenders.length} site(s) with hardcoded hex colors outside app/assets/css/:`)
  for (const o of offenders) {
    console.error(`  - ${o.rel}:${o.lineNumber}  [${o.matches.join(', ')}]  ${o.content.slice(0, 80)}${o.content.length > 80 ? '…' : ''}`)
  }
  console.error()
  console.error('Move the value into a CSS custom property in app/assets/css/main.css and consume it via the Tailwind utility (e.g., bg-success) or getComputedStyle().getPropertyValue() for runtime reads. If the value is genuinely brand DATA (a swatch the playground lets you try on), add the file to the ALLOWLIST or the line gets a `lint-allow-hex` comment.')
  process.exit(1)
}

console.log(`[no-hex-colors] OK — 0 hex literals outside app/assets/css/`)
