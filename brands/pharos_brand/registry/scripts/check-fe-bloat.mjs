#!/usr/bin/env node
/**
 * CI gate: forbid frontend dependency bloat. Two DETERMINISTIC rules (zero
 * false-positives). Dead-dep detection (knip) and a bundle-size budget are
 * tracked as fast-follows — see Interval-Col/.github#70.
 *
 *   1. no-iconify-monolith — the full `@iconify/json` package (~400 MB, every
 *      icon collection) must NOT be a dependency. Install only the
 *      per-collection `@iconify-json/<prefix>` packages you actually use;
 *      `@iconify/tailwind` resolves those before the monolith, so output is
 *      identical and the install footprint drops sharply.
 *   2. one-lib-per-category — at most ONE library from each "same-purpose"
 *      category may be installed (e.g. one Lucide-for-Vue package; one
 *      Radix/Reka headless-UI package). Two libraries doing the same job
 *      bloat both the install and the bundle.
 *
 * Why this gate exists: admission-patient shipped with @iconify/json (399 MB),
 * duplicate icon libs (lucide-vue-next + @lucide/vue) and a legacy + successor
 * UI lib (radix-vue + reka-ui). This gate stops that pattern from recurring in
 * any Pháros app.
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * Dep-level ALLOWLIST: each entry is a DOCUMENTED exception (org policy —
 * ENGINEERING_STANDARDS.md "Allowlists are intentional"). Keep it tiny and
 * justified (e.g. a dated migration window); prefer removing the dependency.
 *
 * Authored for RFC 0008 §6 design/standards gates.
 */
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = resolve(__dirname, '..')
const PKG = join(REPO_ROOT, 'package.json')

// Monolith packages that must never be installed → use the per-collection
// alternative instead. Map value is the fix advice printed on failure.
const BANNED_DEPS = new Map([
  [
    '@iconify/json',
    'Install only the per-collection @iconify-json/<prefix> packages you use; @iconify/tailwind resolves them before the monolith.',
  ],
])

// "Same purpose" categories: at most ONE library per category may be present.
const CATEGORIES = [
  { name: 'Lucide icons (Vue)', libs: ['lucide-vue-next', '@lucide/vue'] },
  { name: 'Radix/Reka headless UI', libs: ['reka-ui', 'radix-vue'] },
]

// Documented exceptions (keep tiny + justified). Each entry is a dep name that
// is allowed despite a rule — add a one-line comment with the removal plan.
const ALLOWLIST = new Set([
  // '@lucide/vue',  // example: mid-migration to lucide-vue-next, remove by <date>
])

if (!existsSync(PKG)) {
  console.log('[fe-bloat] no package.json at repo root — skip.')
  process.exit(0)
}

const pkg = JSON.parse(readFileSync(PKG, 'utf8'))
const deps = { ...pkg.dependencies, ...pkg.devDependencies, ...pkg.optionalDependencies }
const has = (name) => Object.prototype.hasOwnProperty.call(deps, name) && !ALLOWLIST.has(name)

const violations = []

// Rule 1 — no banned monoliths.
for (const [dep, advice] of BANNED_DEPS) {
  if (has(dep)) violations.push({ rule: 'no-iconify-monolith', msg: `"${dep}" is banned. ${advice}` })
}

// Rule 2 — one library per category.
for (const cat of CATEGORIES) {
  const present = cat.libs.filter(has)
  if (present.length > 1) {
    violations.push({
      rule: 'one-lib-per-category',
      msg: `category "${cat.name}": found ${present.length} (${present.join(', ')}). Keep one; migrate the rest.`,
    })
  }
}

if (violations.length) {
  console.error()
  console.error(`[fe-bloat] ${violations.length} violation(s) in package.json:`)
  for (const v of violations) console.error(`  - [${v.rule}] ${v.msg}`)
  console.error()
  console.error('Fix package.json (or add a tiny, justified ALLOWLIST entry with a removal note).')
  process.exit(1)
}

console.log('[fe-bloat] OK — no monolith deps, one library per category.')
