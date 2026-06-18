#!/usr/bin/env node
// =============================================================================
// check-contrast.mjs — Layer-D brand-compliance gate (RFC 0008).
//
// Parses the Pháros token contract and asserts WCAG contrast on the pairs that
// carry meaning, in light + dark AND for every sub-brand `.theme-*`:
//
//   TEXT pairs (hard fail < AA 4.5:1) — readability:
//     background / foreground · primary / primary-foreground ·
//     sidebar / sidebar-foreground · sidebar-primary / sidebar-primary-foreground ·
//     each --status-X (as text) on its --status-X-bg surface.
//
//   UI pairs (warn < 3:1) — a non-text accent must be distinguishable from the
//   surface it sits on: ring / background, primary / background. The light
//   pastels (Recepción rosa, Clientes ámbar-claro) are expected to surface here —
//   that is the flag the plan asks for; threshold tuning is a human call (🟠).
//
// Self-contained (node:fs only). Resolves the token file from:
//   1. argv[2] (explicit path)
//   2. <script>/../tokens.css            (running inside the registry)
//   3. <repo>/app/assets/css/pharos-tokens.css  (running inside a consuming app)
// =============================================================================
import { readFileSync, existsSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const candidates = [
  process.argv[2],
  resolve(HERE, '..', 'tokens.css'),
  resolve(HERE, '..', 'app', 'assets', 'css', 'pharos-tokens.css'),
].filter(Boolean)
const tokensPath = candidates.find(p => existsSync(p))
if (!tokensPath) {
  console.error('[contrast] could not find a tokens file. Pass a path: check-contrast.mjs <tokens.css>')
  process.exit(1)
}

const AA_TEXT = 4.5 // normal text
const UI_MIN = 3.0 // non-text UI element vs adjacent surface (WCAG 1.4.11)

// ── WCAG relative luminance + contrast ratio ────────────────────────────────
function toLin(c) {
  const s = c / 255
  return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4
}
function luminance(hex) {
  const h = hex.replace('#', '')
  const full = h.length === 3 ? h.split('').map(c => c + c).join('') : h
  const r = parseInt(full.slice(0, 2), 16)
  const g = parseInt(full.slice(2, 4), 16)
  const b = parseInt(full.slice(4, 6), 16)
  return 0.2126 * toLin(r) + 0.7152 * toLin(g) + 0.0722 * toLin(b)
}
function ratio(h1, h2) {
  const a = luminance(h1)
  const b = luminance(h2)
  const hi = Math.max(a, b)
  const lo = Math.min(a, b)
  return (hi + 0.05) / (lo + 0.05)
}

// ── Parse `selector { --token: #hex; }` blocks (hex values only) ─────────────
const css = readFileSync(tokensPath, 'utf8')
const blocks = {} // selector -> { token: '#hex' }
const blockRe = /([.:][a-zA-Z0-9_.\- ]+?)\s*\{([^}]*)\}/g
const HEX = /(#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b)/
let m
while ((m = blockRe.exec(css)) !== null) {
  const selector = m[1].trim()
  const body = m[2]
  const map = (blocks[selector] ??= {})
  const declRe = /(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);/g
  let d
  while ((d = declRe.exec(body)) !== null) {
    const hx = d[2].match(HEX)
    if (hx) map[d[1]] = hx[1].toLowerCase()
  }
}

const root = blocks[':root'] ?? {}
const dark = blocks['.dark'] ?? {}
const themes = Object.keys(blocks)
  .filter(s => /^\.theme-[a-z0-9-]+$/.test(s))
  .map(s => s.replace('.theme-', ''))

const merge = (...maps) => Object.assign({}, ...maps)

// Build the contexts to check: base light/dark + each sub-brand theme light/dark.
const contexts = [
  { name: 'light', tokens: root },
  { name: 'dark', tokens: merge(root, dark) },
]
for (const t of themes) {
  const light = blocks[`.theme-${t}`] ?? {}
  const darkT = blocks[`.dark.theme-${t}`] ?? blocks[`.theme-${t}.dark`] ?? {}
  contexts.push({ name: `theme-${t} (light)`, tokens: merge(root, light) })
  contexts.push({ name: `theme-${t} (dark)`, tokens: merge(root, dark, light, darkT) })
}

const TEXT_PAIRS = [
  ['--foreground', '--background'],
  ['--primary-foreground', '--primary'],
  ['--sidebar-foreground', '--sidebar'],
  ['--sidebar-primary-foreground', '--sidebar-primary'],
  ['--card-foreground', '--card'],
  ['--muted-foreground', '--muted'],
  ['--status-success', '--status-success-bg'],
  ['--status-warning', '--status-warning-bg'],
  ['--status-error', '--status-error-bg'],
  ['--status-info', '--status-info-bg'],
]
const UI_PAIRS = [
  ['--ring', '--background'],
  ['--primary', '--background'],
]

let failures = 0
let warnings = 0
const r2 = n => (Math.round(n * 100) / 100).toFixed(2)

for (const ctx of contexts) {
  const tk = ctx.tokens
  const lines = []
  for (const [fg, bg] of TEXT_PAIRS) {
    if (!tk[fg] || !tk[bg]) continue
    const cr = ratio(tk[fg], tk[bg])
    if (cr < AA_TEXT) {
      failures++
      lines.push(`  ✗ FAIL  ${fg} on ${bg}  ${r2(cr)}:1  (< AA ${AA_TEXT}) ${tk[fg]}/${tk[bg]}`)
    }
  }
  for (const [el, bg] of UI_PAIRS) {
    if (!tk[el] || !tk[bg]) continue
    const cr = ratio(tk[el], tk[bg])
    if (cr < UI_MIN) {
      warnings++
      lines.push(`  ⚠ WARN  ${el} on ${bg}  ${r2(cr)}:1  (< UI ${UI_MIN}) ${tk[el]}/${tk[bg]}`)
    }
  }
  if (lines.length) {
    console.log(`\n[${ctx.name}]`)
    for (const l of lines) console.log(l)
  }
}

console.log(`\n[contrast] checked ${contexts.length} context(s) from ${tokensPath.split('/').slice(-2).join('/')}`)
if (warnings) {
  console.log(
    `[contrast] ${warnings} UI-contrast warning(s) — non-text accents below 3:1 (the light pastels). ` +
      `🟠 human call (RFC 0008): tune the tint darker or accept with a documented exception.`,
  )
}
if (failures) {
  console.error(`[contrast] ${failures} TEXT-contrast FAILURE(S) below AA ${AA_TEXT}:1 — fix a foreground/tint.`)
  process.exit(1)
}
console.log(`[contrast] OK — all text pairs meet WCAG AA ${AA_TEXT}:1.`)
