#!/usr/bin/env node
// =============================================================================
// check-font-allowlist.mjs — Layer-D brand-compliance gate (RFC 0008 Q5).
//
// Asserts that only the FOUR sanctioned Pháros families are referenced as fonts:
//   Fraunces · DM Sans · IBM Plex Mono · JetBrains Mono
// plus generic CSS keywords + common system fallbacks. Fails on a stray family
// (Inter, Segoe UI, Helvetica Neue, VT323, Apax, Tahoma, …) loaded or named
// anywhere under app/ or in nuxt.config — the drift a static rule can't see.
//
// Scans for: `font-family:` declarations, Tailwind `font-['X']` arbitrary values,
// `--font-*:` token stacks, @font-face families, and @nuxt/fonts `{ name: 'X' }`.
// Self-contained (node:fs only); REPO_ROOT = the dir containing app/ (argv[2] override).
// =============================================================================
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = process.argv[2] ? resolve(process.argv[2]) : resolve(HERE, '..')
const APP_DIR = join(REPO_ROOT, 'app')

const BRAND = new Set(['fraunces', 'dm sans', 'ibm plex mono', 'jetbrains mono'])
// Generic CSS keywords + universally-acceptable system fallbacks (never flagged).
const FALLBACK_OK = new Set([
  'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-monospace',
  'ui-sans-serif', 'ui-serif', 'inherit', 'initial', 'unset', 'revert',
  '-apple-system', 'blinkmacsystemfont', 'georgia', 'times new roman', 'times',
  'sfmono-regular', 'sf mono', 'menlo', 'monaco', 'consolas', 'courier new', 'courier',
  'liberation mono', 'dejavu sans mono', 'emoji', 'math', 'fangsong',
])

const SCAN_EXTS = new Set(['.vue', '.ts', '.js', '.mjs', '.css'])
const IGNORE_DIRS = new Set(['node_modules', '.nuxt', '.output', 'dist', 'generated', '.git'])

function walk(dir) {
  const out = []
  if (!existsSync(dir)) return out
  for (const name of readdirSync(dir)) {
    if (IGNORE_DIRS.has(name)) continue
    const p = join(dir, name)
    const st = statSync(p)
    if (st.isDirectory()) out.push(...walk(p))
    else if (SCAN_EXTS.has(p.slice(p.lastIndexOf('.')))) out.push(p)
  }
  return out
}

const files = walk(APP_DIR)
for (const cfg of ['nuxt.config.ts', 'nuxt.config.js', 'nuxt.config.mjs']) {
  const p = join(REPO_ROOT, cfg)
  if (existsSync(p)) files.push(p)
}

// Normalize one family token: strip quotes/whitespace, lowercase. Drop var()/empty.
function norm(raw) {
  const t = raw.trim().replace(/^['"]|['"]$/g, '').trim().toLowerCase()
  if (!t || t.startsWith('var(') || t.startsWith('--')) return null
  return t
}

// Pull family names out of one comma-separated font list.
function familiesFrom(list) {
  return list
    .replace(/var\(/gi, '') // unwrap var(--token, fallback…) → --token, fallback…
    .replace(/\)/g, '')
    .split(',')
    .map(norm)
    .filter(f => f && !BRAND.has(f) && !FALLBACK_OK.has(f))
}

const violations = []
const RULES = [
  /font-family\s*:\s*([^;}{]+)[;}]/gi, // CSS / inline style / @font-face
  /font-\[(['"]?)([^\]]+?)\1\]/gi, // Tailwind arbitrary: font-['Segoe UI']
  /--font-[a-z-]+\s*:\s*([^;]+);/gi, // token stacks
]
// @nuxt/fonts families read `{ name: 'X', weights/provider… }`. A bare `name:`
// is NOT a font on its own — it also matches i18n locales, Pinia store ids,
// route/component names — so only treat it as a family when a font-declaration
// sibling key (weights/provider/subsets/style/…) sits nearby.
const FONT_NAME_RE = /\bname\s*:\s*['"]([^'"]+)['"]/gi
const FONT_CTX_RE = /\b(?:weights?|provider|subsets|styles?|fallbacks|display|src)\s*:/i
const FONT_CTX_WINDOW = 200

for (const file of files) {
  const text = readFileSync(file, 'utf8')
  const lines = text.split('\n')
  for (const re of RULES) {
    re.lastIndex = 0
    let m
    while ((m = re.exec(text)) !== null) {
      const list = m[2] ?? m[1] // font-[] uses group 2; the rest group 1
      const bad = familiesFrom(list)
      if (bad.length) {
        const line = text.slice(0, m.index).split('\n').length
        for (const fam of bad) {
          violations.push({ file: relative(REPO_ROOT, file), line, fam, ctx: lines[line - 1]?.trim().slice(0, 90) })
        }
      }
    }
  }
  // @nuxt/fonts family names — only when guarded by a nearby font-declaration key.
  FONT_NAME_RE.lastIndex = 0
  let mn
  while ((mn = FONT_NAME_RE.exec(text)) !== null) {
    const around = text.slice(Math.max(0, mn.index - FONT_CTX_WINDOW), mn.index + FONT_CTX_WINDOW)
    if (!FONT_CTX_RE.test(around)) continue // not a @nuxt/fonts family entry
    const bad = familiesFrom(mn[1])
    if (!bad.length) continue
    const line = text.slice(0, mn.index).split('\n').length
    for (const fam of bad) {
      violations.push({ file: relative(REPO_ROOT, file), line, fam, ctx: lines[line - 1]?.trim().slice(0, 90) })
    }
  }
}

if (violations.length) {
  console.error(`[font-allowlist] ${violations.length} non-sanctioned font reference(s):`)
  for (const v of violations) {
    console.error(`  ✗ ${v.file}:${v.line}  "${v.fam}"`)
    if (v.ctx) console.error(`      ${v.ctx}`)
  }
  console.error('\nAllowed: Fraunces · DM Sans · IBM Plex Mono · JetBrains Mono (+ generic/system fallbacks).')
  console.error('Use a --font-* contract token (font-display/sans/mono/data). If a fallback is genuinely needed, add it to FALLBACK_OK.')
  process.exit(1)
}
console.log(`[font-allowlist] OK — only sanctioned families referenced (scanned ${files.length} file(s)).`)
