#!/usr/bin/env node
// =============================================================================
// check-orphan-vars.mjs — Layer-D brand-compliance gate (RFC 0008).
//
// Falla si un componente usa una custom property CSS con VALOR ARBITRARIO
// —`shadow-[var(--x)]`, `bg-[var(--x)]`, `style="…var(--x)…"`— que NADIE declara
// en el CSS que este repo tiene a mano.
//
// 🔴 POR QUÉ EXISTE. `RoleCapabilityMatrix.vue` y `UsersRoleTable.vue` llegaron al
// registry desde finance-lch trayéndose `shadow-[var(--shadow-soft)]`. El token se
// quedó atrás: `tokens.css` no publica NI UN `--shadow-*`. Tailwind emite
// `box-shadow: var(--shadow-soft)`, la regla no resuelve, y la sombra
// simplemente no se pinta — sin error, sin warning, sin build roto. En lab-qc y
// pharos-ti el panel «Agregar usuario» se quedó sin sombra Y sin borde durante
// meses, en verde. Medido el 2026-08-21.
//
// Ningún gate lo veía, por dos capas de ceguera: `check-token-usage.mjs` sólo
// mira utilidades con NOMBRE de token (`bg-primary`), no valores arbitrarios, y
// encima excluye `shadow` a propósito. Este gate cubre justo ese hueco y por eso
// va aparte: meter `shadow` de vuelta en el otro reproduce su falso positivo.
//
// ── LO QUE CUENTA COMO «DECLARADO» ──
// Se leen las declaraciones de DOS sitios, no uno:
//   1. el CSS del repo (`tokens.css`, `app/assets/css/**`)
//   2. los propios .vue/.ts — un componente que fija su variable en un `:style`
//      la está declarando (`--sidebar-width`, `--tone`, `--skeleton-width`)
// Sin (2) el gate acusaría a shadcn de romper su propia mecánica.
//
// ⇒ El mismo script sirve corrido DENTRO del registry y DENTRO de una app, y da
// la respuesta correcta en cada uno: en el registry un token que sólo la app
// define ES un huérfano (el componente se copia a cinco apps, el token no); en
// la app, ese mismo token está declarado y pasa. Esa asimetría es el hallazgo.
//
// 🪤 TRAMPA DE MÉTODO, ya pagada. El regex ingenuo `--x\s*:` NO ve las claves con
// comilla de cierre (`'--sidebar-width': ancho`), porque la comilla se interpone
// antes de los dos puntos. Con esa versión `--sidebar-width` salía como huérfano
// y no lo es. Hay que permitir `'`, `"`, backtick o `]` antes del `:`.
//
// Escape hatch: `lint-allow-token` en la línea (misma convención que los demás).
// Self-contained (node:fs). REPO_ROOT = el dir que contiene app/ (argv[2]).
// =============================================================================
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs'
import { dirname, resolve, join, extname, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = process.argv[2] ? resolve(process.argv[2]) : resolve(HERE, '..')

// Prefijos que los aporta una librería, no el sistema de diseño.
const VENDOR_PREFIXES = ['--reka-', '--tw-', '--radix-', '--vaul-']

// Las variables de tema de Tailwind v4 las publica `tailwindcss/theme.css`, así que
// se leen de ahí — exactas, no por familia. ⚠️ NO se permite una familia entera
// (`--shadow-*`, `--color-*`): así se colaron `--shadow-soft` y `--color-yellow`,
// que se PARECEN a tokens de Tailwind y no existen (Tailwind trae `--shadow-sm` y
// `--color-yellow-500`, no esos). La precisión es el punto del gate.
const TAILWIND_SINGLETONS = [
  '--spacing',
  '--default-transition-duration',
  '--default-transition-timing-function',
  '--default-font-family',
  '--default-font-feature-settings',
  '--default-font-variation-settings',
  '--default-mono-font-family',
  '--default-mono-font-feature-settings',
  '--default-mono-font-variation-settings',
]

/** Busca `node_modules/tailwindcss/theme.css` subiendo desde REPO_ROOT (pnpm workspaces). */
function findTailwindTheme(start) {
  let dir = start
  for (let i = 0; i < 6; i++) {
    const c = resolve(dir, 'node_modules', 'tailwindcss', 'theme.css')
    if (existsSync(c)) return c
    const up = dirname(dir)
    if (up === dir) break
    dir = up
  }
  return null
}

// Un candidato con interpolación (`--status-${kind}`) no se puede resolver
// estáticamente. Se salta y se cuenta aparte: acusarlo sería un falso positivo,
// y callarlo del todo escondería que el gate no lo revisó.
const isDynamic = (name) => name.includes('$') || name.includes('{')

const SKIP_DIRS = new Set(['node_modules', '.git', '.nuxt', '.output', 'dist', 'coverage'])

function walk(dir, out = []) {
  if (!existsSync(dir)) return out
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue
    const p = join(dir, entry)
    if (statSync(p).isDirectory()) walk(p, out)
    else out.push(p)
  }
  return out
}

const all = walk(resolve(REPO_ROOT, 'app'))
const rootCss = ['tokens.css', 'pharos-tokens.css']
  .map((f) => resolve(REPO_ROOT, f))
  .filter((f) => existsSync(f))

const cssFiles = [...all.filter((f) => extname(f) === '.css'), ...rootCss]
const codeFiles = all.filter((f) => ['.vue', '.ts'].includes(extname(f)))

if (!cssFiles.length && !codeFiles.length) {
  console.log('[orphan-vars] no hay app/ ni CSS de tokens — skip.')
  process.exit(0)
}

// ── 1 · lo DECLARADO ────────────────────────────────────────────────────────
// La clase de caracteres antes del `:` es la trampa de arriba: comilla simple,
// doble, backtick o `]` pueden interponerse cuando la declaración es una clave
// de objeto JS en vez de una línea de CSS.
const DECL = /(--[A-Za-z][A-Za-z0-9_-]*)\s*['"`\]]?\s*:/g
const declared = new Set()
for (const f of [...cssFiles, ...codeFiles]) {
  const src = readFileSync(f, 'utf8')
  for (const m of src.matchAll(DECL)) declared.add(m[1])
}

for (const k of TAILWIND_SINGLETONS) declared.add(k)
const twTheme = findTailwindTheme(REPO_ROOT)
if (twTheme) {
  for (const m of readFileSync(twTheme, 'utf8').matchAll(DECL)) declared.add(m[1])
}

// ── 2 · lo USADO con valor arbitrario ───────────────────────────────────────
const USE = /var\(\s*(--[A-Za-z][A-Za-z0-9_$-]*(?:\{[^}]*\})?[A-Za-z0-9_$-]*)/g
const orphans = []
let dynamicSkipped = 0

for (const f of codeFiles) {
  const src = readFileSync(f, 'utf8')
  const lines = src.split('\n')
  lines.forEach((line, i) => {
    if (line.includes('lint-allow-token')) return
    for (const m of line.matchAll(USE)) {
      const name = m[1]
      if (isDynamic(name)) { dynamicSkipped++; continue }
      if (VENDOR_PREFIXES.some((p) => name.startsWith(p))) continue
      // Un `var(--x, fallback)` NO es huérfano: el fallback es la declaración.
      const after = line.slice(m.index + m[0].length)
      if (/^\s*,/.test(after)) continue
      if (declared.has(name)) continue
      orphans.push({ file: relative(REPO_ROOT, f), line: i + 1, name, text: line.trim().slice(0, 110) })
    }
  })
}

const nota = dynamicSkipped ? ` · ${dynamicSkipped} con nombre dinámico, NO verificadas` : ''

if (!orphans.length) {
  const tw = twTheme ? 'tema de Tailwind leído' : '⚠️ sin tema de Tailwind (sólo los singletons)'
  console.log(`[orphan-vars] OK — ${declared.size} custom propert(ies) declaradas cubren todo var(--x) arbitrario · ${tw}${nota}.`)
  process.exit(0)
}

console.error(`\n[orphan-vars] ${orphans.length} uso(s) de una custom property que NADIE declara:`)
for (const o of orphans) console.error(`  - ${o.file}:${o.line}  ${o.name}\n      ${o.text}`)
console.error(`
La regla CSS no resuelve y el estilo NO SE APLICA — sin error, sin warning y con
el build en verde. Es la forma más silenciosa de romper una pantalla.

Tres salidas, en orden de preferencia:
  1. Usá la utilidad de Tailwind en vez del valor arbitrario (\`shadow-sm\` en vez
     de \`shadow-[var(--shadow-soft)]\`). Es lo que hacen 18 de los 20 usos de
     sombra del registry, y lo que manda \`frontend-standards.md\`.
  2. Dale un fallback al var: \`var(--x, <valor>)\`. Deja de ser huérfano porque
     el fallback ES la declaración.
  3. Declará el token en el CSS de este repo — pero si estás en el REGISTRY, eso
     agrega vocabulario al contrato y se propaga a las cinco apps: es una
     decisión de sistema de diseño, no un arreglo de paso.
${nota ? `\nY${nota.replace(' · ', ' ojo: ')} — un nombre construido en runtime este gate no lo puede verificar.\n` : ''}`)
process.exit(1)
