#!/usr/bin/env node
/**
 * CI gate: forbid color utilities that name a token which DOESN'T EXIST.
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * ── Why this gate exists ───────────────────────────────────────────────────
 * `check-no-palette-colors` catches a color that is REAL but WRONG
 * (`text-green-600`). This one catches the opposite and nastier case: a color
 * that is right in spirit and simply does not exist.
 *
 * Real occurrence (pharos-ti, 2026-08): an error banner shipped as
 * `text-status-danger`. The token is `--color-status-error`; `status-danger`
 * was never defined. Tailwind emits no class for an undefined token, so the
 * banner rendered with NO color at all — the error text came out the same
 * shade as body copy. Nothing threw. The build was green, every existing gate
 * was green, and the only symptom was a warning that didn't look like one.
 *
 * That is the failure mode worth a gate: not a crash, just a thing quietly
 * failing to be what it claims. A typo in a token name has no blast radius
 * anywhere except the pixels nobody looks at twice.
 *
 * ── How it decides, without drowning in false positives ────────────────────
 * We can't simply require every color utility to match a token — `bg-white`,
 * `border-2` and `text-center` are all perfectly legal Tailwind and none of
 * them are ours. So the rule keys on NAMESPACE OWNERSHIP:
 *
 *   A utility is checked only if its first name segment is a segment we own
 *   (i.e. some defined `--color-*` token starts with it). If it is, the FULL
 *   name must resolve to a defined token.
 *
 *   bg-status-danger  → `status` is ours → `status-danger` undefined → FAIL
 *   bg-status-error   → `status` is ours → defined                   → ok
 *   bg-chart-9        → `chart`  is ours → `chart-9` undefined       → FAIL
 *   bg-red-500        → `red`    not ours                            → ignored
 *   text-center       → `center` not ours                            → ignored
 *   border-2          → `2`      not ours                            → ignored
 *
 * The tokens are read from the app's synced CSS, so the gate tracks whatever
 * the registry currently defines. Add a token upstream and it becomes legal
 * here on the next sync — no allowlist to maintain by hand.
 *
 * ⚠️ Static analysis only. A class built at runtime (`text-status-${level}`)
 * is invisible to this gate — but it is equally invisible to Tailwind's own
 * scanner, which means it wouldn't render either. Keep color classes literal.
 *
 * Escape hatch: `lint-allow-token` on the offending line.
 */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = process.argv[2] ? resolve(process.argv[2]) : resolve(__dirname, '..')
const SCAN_ROOT = join(REPO_ROOT, 'app')
const CSS_ROOT = join(REPO_ROOT, 'app', 'assets', 'css')

const IGNORE_PATH_FRAGMENTS = [
  'app/lib/api/generated/',
]

const SCAN_EXTS = new Set(['.vue', '.ts'])

// ⚠️ Sin `shadow` ni `placeholder`, y por razones distintas:
//   • `shadow-*` resuelve contra `--shadow-*`, no `--color-*`. Incluirlo hacía
//     que un `shadow-soft` perfectamente definido se reportara como token
//     inexistente — un gate que grita por algo correcto se desactiva solo.
//   • `placeholder-<color>` es Tailwind v3; en v4 se escribe `placeholder:text-*`.
//     Dejarlo se comía cualquier clase propia que empezara por `placeholder-`
//     (`placeholder-table-wrapper`, medido en finance-lch).
const PROPS = 'text|bg|border|ring|outline|fill|stroke|from|to|via|caret|accent|decoration|divide'
// Optional variant prefixes (`dark:`, `hover:`, `group-hover:`, `md:`) and an
// optional `!` important marker; optional `/50` opacity modifier on the tail.
const USAGE_RE = new RegExp(
  `(?:^|[\\s"'\`{(\\[])(?:[a-z0-9:_-]+:)*!?(?:${PROPS})-([a-z][a-z0-9-]*)(?:/\\d{1,3})?(?=$|[\\s"'\`})\\]])`,
  'g',
)
const ESCAPE_HATCH = /lint-allow-token/
const PALETTE_RE = /^(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}$/
const TOKEN_DEF_RE = /--color-([a-z0-9-]+)\s*:/g

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

function stripStyleBlocks(src) {
  return src.replace(/<style\b[\s\S]*?<\/style>/gi, (block) => block.replace(/[^\n]/g, ' '))
}

function shouldIgnore(rel) {
  return IGNORE_PATH_FRAGMENTS.some((frag) => rel.startsWith(frag))
}

// ── 1. What tokens actually exist ─────────────────────────────────────────
// Two layouts, on purpose. In a consuming app the tokens arrive as
// `app/assets/css/pharos-tokens.css`; in the registry itself the source is
// `tokens.css` at the root and `app/assets/css/` holds only the component and
// icon sheets. Read both so the gate is runnable in either place.
const defined = new Set()
const sources = []

const REGISTRY_TOKENS = join(REPO_ROOT, 'tokens.css')
if (existsSync(REGISTRY_TOKENS)) sources.push(REGISTRY_TOKENS)
if (existsSync(CSS_ROOT)) {
  for (const file of readdirSync(CSS_ROOT)) {
    if (file.endsWith('.css')) sources.push(join(CSS_ROOT, file))
  }
}

for (const src of sources) {
  const css = readFileSync(src, 'utf8')
  for (const m of css.matchAll(TOKEN_DEF_RE)) defined.add(m[1])
}

// A synced token sheet that yields nothing is a BROKEN SYNC, and passing on it
// would be the exact sin this gate exists to catch — a green check standing in
// for a check that never happened. Distinguish it from "no tokens anywhere",
// which just means there is nothing here to police.
const SYNCED_TOKENS = join(CSS_ROOT, 'pharos-tokens.css')
if (defined.size === 0) {
  if (existsSync(SYNCED_TOKENS)) {
    console.error('[token-usage] pharos-tokens.css is present but defines no --color-* tokens.')
    console.error('  That is a broken sync, not a design choice — refusing to pass vacuously.')
    process.exit(1)
  }
  console.log('[token-usage] no --color-* tokens found — skip (run scripts/sync-pharos-registry.sh first).')
  process.exit(0)
}

const ownedSegments = new Set([...defined].map((t) => t.split('-')[0]))

// ── 1b. The blind spot the ownership rule alone leaves ────────────────────
// The rule above only inspects a utility whose FIRST SEGMENT belongs to some
// defined token. That is what keeps `bg-red-500` and `text-center` out of the
// report, and it catches every typo INSIDE a family we own — `status-danger`
// (we own `status`), `chart-9`, `bg-brand` where only `brand-wash` exists.
//
// It cannot see a family where NOTHING is defined. Measured case, lab-qc:
// `bg-error-fill` / `text-error-ink`. A token cleanup renamed that whole
// family away; no `--color-error-*` survives, so `error` is not an owned
// segment, so the rule skipped both — and the error banner they style has
// been rendering with no background and no colour ever since.
//
// That is the worst possible shape for this gate: it would have certified the
// file as clean. So the second rule inverts the question — instead of "is
// this ours?", it asks "is this a name Tailwind actually recognises?" and
// flags whatever is neither a defined token nor real Tailwind vocabulary.
//
// The cost is the one thing the first rule avoids: this list needs a line
// added when someone reaches for a utility value nobody here has used yet.
// That trade is deliberate. The failure mode is loud and the fix is one line,
// versus a silent pass on a rename that already happened once.
const TW_KEYWORDS = new Set([
  // CSS-wide colour keywords. Tailwind ships these for every colour utility
  // and they resolve to real CSS — they are not tokens and never will be.
  'white', 'black', 'transparent', 'current', 'inherit', 'auto',
  // `border-none`, `outline-none`, `shadow-none`, `bg-none`, `fill-none`…
  'none',
  // sizes / scales — text-*, shadow-*
  'xs', 'sm', 'base', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl',
  '7xl', '8xl', '9xl', 'inner',
  // alignment + wrapping — text-*
  'left', 'center', 'right', 'justify', 'start', 'end',
  'wrap', 'nowrap', 'balance', 'pretty', 'ellipsis', 'clip',
  // line/border styles — border-*, divide-*, outline-*, decoration-*
  'solid', 'dashed', 'dotted', 'double', 'wavy', 'hidden', 'collapse',
  'separate', 'independent',
  // background behaviour — bg-*
  'fixed', 'local', 'scroll', 'cover', 'contain', 'repeat', 'no-repeat',
  'top', 'bottom', 'origin', 'clip',
  // misc keywords valid after several prefixes
  'inset', 'from-font', 'normal',
])
// Numeric scales (`border-2`, `ring-4`, `stroke-2`), side-prefixed values
// (`border-b-2`, `border-t`), fractions and percentages.
const NUMERIC_RE = /^\d+(\.\d+)?(\/\d+)?$/
const SIDE_RE = /^(x|y|s|e|t|r|b|l|offset)(-(.+))?$/
// SVG presentation attributes (`stroke-width="2"`) look like utilities to the
// scanner. They are attributes, not classes; skipping them is correct, not a
// concession.
const SVG_ATTRS = new Set(['width', 'linecap', 'linejoin', 'dasharray', 'dashoffset', 'opacity', 'rule', 'miterlimit'])

function isRecognized(name) {
  if (defined.has(name)) return true
  if (TW_KEYWORDS.has(name) || SVG_ATTRS.has(name)) return true
  if (NUMERIC_RE.test(name)) return true
  if (PALETTE_RE.test(name)) return true
  // `border-b-primary` → side `b`, colour `primary`. Recurse on the remainder
  // so a side-prefixed colour is judged by the colour, which is the part that
  // can be wrong.
  const side = SIDE_RE.exec(name)
  if (side) return side[3] === undefined || isRecognized(side[3])
  return false
}

// ── 2. Did-you-mean, so the failure is actionable ─────────────────────────
function distance(a, b) {
  const prev = Array.from({ length: b.length + 1 }, (_, i) => i)
  for (let i = 1; i <= a.length; i++) {
    let corner = prev[0]
    prev[0] = i
    for (let j = 1; j <= b.length; j++) {
      const up = prev[j]
      prev[j] = Math.min(
        prev[j] + 1,
        prev[j - 1] + 1,
        corner + (a[i - 1] === b[j - 1] ? 0 : 1),
      )
      corner = up
    }
  }
  return prev[b.length]
}

function suggest(bad) {
  const seg = bad.split('-')[0]
  const pool = [...defined].filter((t) => t.split('-')[0] === seg)
  return pool
    .map((t) => ({ t, d: distance(bad, t) }))
    .sort((a, b) => a.d - b.d)
    .slice(0, 3)
    .map((x) => x.t)
}

// ── 3. Scan ───────────────────────────────────────────────────────────────
const offenders = []
for (const file of walk(SCAN_ROOT)) {
  const rel = relative(REPO_ROOT, file)
  if (shouldIgnore(rel)) continue
  // Un `<style>` es CSS, no clases. `transition: color .15s, border-color .15s`
  // hacía saltar 'color' nueve veces en finance-lch. Se blanquea en vez de
  // borrarse para que los números de línea sigan siendo ciertos.
  const lines = stripStyleBlocks(readFileSync(file, 'utf8')).split('\n')
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (ESCAPE_HATCH.test(line)) continue
    for (const m of line.matchAll(USAGE_RE)) {
      const name = m[1]
      if (defined.has(name)) continue
      // Rule 1 — a typo INSIDE a family we own. High confidence, and we can
      // usually say what was meant.
      if (ownedSegments.has(name.split('-')[0])) {
        offenders.push({ rel, lineNumber: i + 1, name, content: line.trim(), rule: 'own' })
        continue
      }
      // Rule 2 — a name that is neither ours nor Tailwind's. Catches a family
      // renamed out of existence, which rule 1 structurally cannot see.
      if (!isRecognized(name)) {
        offenders.push({ rel, lineNumber: i + 1, name, content: line.trim(), rule: 'unknown' })
      }
    }
  }
}

if (offenders.length) {
  console.error()
  console.error(`[token-usage] ${offenders.length} utility(ies) name a token that does not exist:`)
  for (const o of offenders) {
    console.error(`  - ${o.rel}:${o.lineNumber}  '${o.name}' is not a defined --color-* token`)
    if (o.rule === 'own') {
      const near = suggest(o.name)
      if (near.length) console.error(`      did you mean: ${near.join(', ')}?`)
    } else {
      console.error(`      nothing in this family is defined — a renamed-away token, or a typo.`)
      console.error(`      If it IS valid Tailwind, add it to TW_KEYWORDS at the top of this script.`)
    }
    console.error(`      ${o.content.slice(0, 90)}${o.content.length > 90 ? '…' : ''}`)
  }
  console.error()
  console.error('These render with NO color at all — Tailwind emits nothing for an undefined token,')
  console.error('so the element silently inherits body styling. Nothing crashes; it just stops meaning')
  console.error('what it says. Fix the name, or define the token in the registry and re-sync.')
  process.exit(1)
}

console.log(`[token-usage] OK — every color utility resolves to one of ${defined.size} defined --color-* tokens`)
