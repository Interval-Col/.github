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
// ⚠️ COMMENTS ARE STRIPPED FIRST, and this line is load-bearing.
//
// The block regex below matches a body as `[^}]*` — everything up to the first
// closing brace. A `}` inside a CSS COMMENT therefore ends the block early, and
// every token declared after it becomes invisible to this gate. That is not
// hypothetical: `--radius`'s own comment reads
// `rounded-{sm,md,lg,xl} derived in @theme inline`, and its `}` truncated
// `:root` roughly a third of the way in. Everything below — the ENTIRE
// `--status-*` palette, all five `--chart-*`, the sidebar surfaces — was
// silently skipped in the light theme.
//
// And it failed OPEN. The checks below used to `continue` on a missing token, so
// the gate printed "OK — all text pairs meet WCAG AA" while never having read the
// pairs it exists to verify. A green gate that checked nothing is worse than no
// gate: it is the reason nobody looked.
//
// Stripping comments fixes the parse, but it does not fix the failure mode — it
// only removes today's trigger. Any future edit that puts a token out of this
// gate's reach (a new nested block, a token moved to another file, a renamed
// custom property) would go silently unchecked again. So a TEXT pair whose
// tokens cannot be resolved is now counted as a FAILURE, not skipped: the gate
// fails closed on its own blind spots.
const css = readFileSync(tokensPath, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '')
const blocks = {} // selector -> { token: '#hex' }   (only values this parser can read)
const declared = {} // selector -> Set(token)        (EVERY declaration, whatever the value)
const blockRe = /([.:][a-zA-Z0-9_.\- ]+?)\s*\{([^}]*)\}/g
const HEX = /(#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b)/
let m
while ((m = blockRe.exec(css)) !== null) {
  const selector = m[1].trim()
  const body = m[2]
  const map = (blocks[selector] ??= {})
  const seen = (declared[selector] ??= new Set())
  const declRe = /(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);/g
  let d
  while ((d = declRe.exec(body)) !== null) {
    // Track the NAME separately from the value. Only hex is measurable, but a
    // token written as `var(--pharos-red)` or `oklch(...)` is still DECLARED —
    // and those are legitimate encodings this file's own comments invite. If
    // the two cases are collapsed, "the gate cannot read this form" becomes
    // indistinguishable from "this token does not exist", and the fail-closed
    // rule below turns a routine re-encode into a red build for the whole team
    // with a message that blames the wrong thing.
    seen.add(d[1])
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

const union = (...sets) => new Set(sets.flatMap(s => [...(s ?? [])]))
const dRoot = declared[':root'] ?? new Set()
const dDark = declared['.dark'] ?? new Set()

// Build the contexts to check: base light/dark + each sub-brand theme light/dark.
// `names` mirrors `tokens` but carries EVERY declaration, readable or not.
const contexts = [
  { name: 'light', tokens: root, names: dRoot },
  { name: 'dark', tokens: merge(root, dark), names: union(dRoot, dDark) },
]
for (const t of themes) {
  const light = blocks[`.theme-${t}`] ?? {}
  const darkT = blocks[`.dark.theme-${t}`] ?? blocks[`.theme-${t}.dark`] ?? {}
  const dLight = declared[`.theme-${t}`] ?? new Set()
  const dDarkT = declared[`.dark.theme-${t}`] ?? declared[`.theme-${t}.dark`] ?? new Set()
  contexts.push({
    name: `theme-${t} (light)`,
    tokens: merge(root, light),
    names: union(dRoot, dLight),
  })
  contexts.push({
    name: `theme-${t} (dark)`,
    tokens: merge(root, dark, light, darkT),
    names: union(dRoot, dDark, dLight, dDarkT),
  })
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

  // `--destructive` is not decoration here: it is the surface a CRITICAL analyte
  // result is announced on (`AnalyteResultCell.vue` renders the out-of-range chip
  // as `bg-destructive` with `--destructive-foreground` text). That makes it a
  // clinical signal carrying text, so it owes the same AA 4.5:1 as the four
  // `--status-*` roles — and until now no pair in this file measured it.
  ['--destructive-foreground', '--destructive'],
]
const UI_PAIRS = [
  ['--ring', '--background'],
  ['--primary', '--background'],

  // Trend tokens — a sparkline stroke IS a non-text graphical object, so 3:1 is
  // the bar it has to clear in BOTH themes.
  ['--trend-up', '--background'],
  ['--trend-down', '--background'],
  ['--trend-flat', '--background'],

  // Chart tokens. Registered here deliberately, KNOWING several will warn: they
  // are declared once and never redefined in .dark, so measured against each
  // theme's own background only --chart-2 clears 3:1 in both (--chart-1 is
  // 1.68:1 on dark, --chart-4 is 1.38:1 on light). That is why every chart in
  // the estate hard-codes --chart-2 and never touches the other four — it reads
  // as taste until something measures it, and until now nothing did: this file
  // named no --chart-* pair at all.
  //
  // A warning, not a failure, on purpose. The fix is a palette decision (RFC
  // 0008 Q4 says the chart ramp is brand-fixed), not something a component
  // author can make. Surfacing it is the point.
  ['--chart-1', '--background'],
  ['--chart-2', '--background'],
  ['--chart-3', '--background'],
  ['--chart-4', '--background'],
  ['--chart-5', '--background'],
]

let failures = 0
let warnings = 0
let missing = 0
let unreadable = 0
const r2 = n => (Math.round(n * 100) / 100).toFixed(2)

// Split the two ways a pair can go unmeasured, because they are different
// events with different owners:
//
//   MISSING    — the token is declared nowhere this gate can see. That is the
//                fail-open hole this file exists to close: a pair silently not
//                checked while the gate printed OK. Hard failure.
//   UNREADABLE — the token IS declared, in a form this parser cannot resolve
//                (`var(...)`, `oklch(...)`, `hsl(...)`). That is a gap in the
//                GATE, not a defect in the palette, and those encodings are
//                sanctioned by this very token file. Failing the build on it
//                would turn a routine re-encode into a red pipeline for
//                everyone, blaming the palette for the parser's limits.
//                Loud warning, exit 0.
function classify(ctx, ...tokenNames) {
  const missingNames = tokenNames.filter(n => !ctx.tokens[n] && !ctx.names.has(n))
  const unreadableNames = tokenNames.filter(n => !ctx.tokens[n] && ctx.names.has(n))
  return { missingNames, unreadableNames }
}

for (const ctx of contexts) {
  const tk = ctx.tokens
  const lines = []
  for (const [fg, bg] of TEXT_PAIRS) {
    const { missingNames, unreadableNames } = classify(ctx, fg, bg)
    if (missingNames.length) {
      missing++
      lines.push(`  ✗ MISSING  ${fg} on ${bg}  — ${missingNames.join(' + ')} declared nowhere`)
      continue
    }
    if (unreadableNames.length) {
      unreadable++
      lines.push(
        `  ⚠ UNREADABLE  ${fg} on ${bg}  — ${unreadableNames.join(' + ')} declared as a non-hex value`,
      )
      continue
    }
    const cr = ratio(tk[fg], tk[bg])
    if (cr < AA_TEXT) {
      failures++
      lines.push(`  ✗ FAIL  ${fg} on ${bg}  ${r2(cr)}:1  (< AA ${AA_TEXT}) ${tk[fg]}/${tk[bg]}`)
    }
  }
  for (const [el, bg] of UI_PAIRS) {
    // UI pairs carry warn semantics throughout, so both unmeasured cases warn
    // here — but they are still named apart, and never folded into the
    // "below 3:1" tally, which would claim a measurement that never happened.
    const { missingNames, unreadableNames } = classify(ctx, el, bg)
    if (missingNames.length || unreadableNames.length) {
      unreadable++
      const why = missingNames.length
        ? `${missingNames.join(' + ')} declared nowhere`
        : `${unreadableNames.join(' + ')} declared as a non-hex value`
      lines.push(`  ⚠ UNMEASURED  ${el} on ${bg}  — ${why}`)
      continue
    }
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
if (unreadable) {
  console.log(
    `[contrast] ${unreadable} pair(s) UNMEASURED — a token is declared but not as a hex literal ` +
      `(var()/oklch()/hsl()), which this parser cannot resolve. That is a limit of THIS GATE, not ` +
      `a palette defect: resolve the value here or teach the parser. Not a build failure.`,
  )
}
if (missing) {
  console.error(
    `[contrast] ${missing} TEXT pair(s) MISSING — the token is declared NOWHERE this gate can see, ` +
      `so the pair went unchecked while the gate would otherwise print OK. That silent pass is the ` +
      `hole this check exists to close.`,
  )
}
if (failures) {
  console.error(`[contrast] ${failures} TEXT-contrast FAILURE(S) below AA ${AA_TEXT}:1 — fix a foreground/tint.`)
}
if (failures || missing) process.exit(1)
console.log(
  `[contrast] OK — ${TEXT_PAIRS.length - unreadable > 0 ? 'all ' : ''}text pairs resolved and meet ` +
    `WCAG AA ${AA_TEXT}:1 across ${contexts.length} context(s)` +
    `${unreadable ? `, except ${unreadable} left unmeasured above` : ''}.`,
)
