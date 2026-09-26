#!/usr/bin/env node
// =============================================================================
// check-registry-fresh.mjs — copy-in FRESHNESS gate (RFC 0016 / RFC 0008).
//
// The staleness sibling of check-registry-drift (Lock 3):
//   • Lock 3 (drift)     — app's file vs the app's OWN manifest → "did someone
//                          hand-edit a copied primitive?" (no registry needed).
//   • THIS  (freshness)  — app's manifest vs the registry's CURRENT source →
//                          "has the registry moved ahead of what the app synced?"
//
// Runs in the CONSUMING APP's CI. Because Interval-Col/.github is PUBLIC, the
// app's workflow checks it out (no token) and passes the registry app dir as
// argv[2]; this compares each manifest entry's synced sha256 against the current
// registry file's sha256 and fails on any that moved (STALE) or vanished.
//
// Fix = re-run scripts/sync-pharos-registry.sh (or merge the re-sync bot's PR),
// which refreshes both the copy AND the manifest.
//
// Self-contained (node:fs + node:crypto). REPO_ROOT (the dir containing app/) =
// resolve(HERE, '..'); registry app dir = argv[2] (REQUIRED). Skips cleanly with
// no manifest (an app that hasn't adopted the drift/freshness gates yet).
// =============================================================================
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = resolve(HERE, '..')
const manifestPath = resolve(REPO_ROOT, 'app', 'assets', 'pharos-registry.sha256')

const registryApp = process.argv[2]
if (!registryApp) {
  console.error('[registry-fresh] usage: check-registry-fresh.mjs <registry-app-dir>')
  console.error('  (checkout Interval-Col/.github and point at brands/pharos_brand/registry/app)')
  process.exit(2)
}
if (!existsSync(manifestPath)) {
  console.log('[registry-fresh] no pharos-registry.sha256 manifest — skip '
    + '(run scripts/sync-pharos-registry.sh to adopt the registry gates).')
  process.exit(0)
}
if (!existsSync(registryApp)) {
  console.error(`[registry-fresh] registry app dir not found: ${registryApp}`)
  process.exit(2)
}

const lines = readFileSync(manifestPath, 'utf8')
  .split('\n').map(l => l.trim()).filter(Boolean)

const stale = []
const vanished = []

// ── 🔴 LA TERCERA PREGUNTA, desde 2026-09-26 ───────────────────────────────────
// Hasta hoy este portón recorría SÓLO las líneas del manifiesto, así que un archivo que la
// app adoptó y que dejó de estar listado no lo miraba nadie: ni este check ni el de drift.
//
// Medido en pharos-lis#516: una sincronización corrida contra una copia vieja del script
// borró la entrada de `plugins/health-beacon.client.ts`, y los DOS portones siguieron en
// verde — sólo contaron 123 archivos en vez de 124. Ninguno distinguía «está sincronizado»
// de «no se está mirando», así que un manifiesto que encoge era invisible. Eso deshizo en
// silencio el arreglo del día anterior.
//
// Un archivo adoptado (existe en el registry Y en la app) sólo puede faltar del manifiesto
// por dos razones legítimas, y las dos son explícitas:
//   · está en `registry/scaffold.txt` — se entrega una vez y después es de la app;
//   · lleva la marca `pharos-registry:keep` — una primitiva que esa app afinó a propósito.
// Cualquier otra ausencia es el manifiesto encogiendo, y eso se detiene.
const KEEP_MARKER = 'pharos-registry:keep'
const scaffoldPath = resolve(registryApp, '..', 'scaffold.txt')
if (!existsSync(scaffoldPath)) {
  // Fallar cerrado: sin la lista no se puede distinguir un andamiaje legítimo de una entrada
  // borrada, y el veredicto benigno es justamente el caro de equivocar.
  console.error(`[registry-fresh] falta la lista de andamiaje: ${scaffoldPath}`)
  console.error('  Sin ella no se puede juzgar qué ausencia del manifiesto es legítima.')
  process.exit(2)
}
const scaffold = new Set(
  readFileSync(scaffoldPath, 'utf8')
    .split('\n').map(l => l.trim())
    .filter(l => l && !l.startsWith('#')),
)

/** Todo archivo del registry, como ruta relativa a su dir `app/`. */
function registryFiles(dir, base = dir) {
  const out = []
  for (const e of readdirSync(dir)) {
    const full = join(dir, e)
    if (statSync(full).isDirectory()) out.push(...registryFiles(full, base))
    else out.push(full.slice(base.length + 1))
  }
  return out
}

const listado = new Set(lines.map(l => l.split(/\s+/).slice(1).join(' ')).filter(Boolean))
const sinEntrada = []
for (const rel of registryFiles(registryApp)) {
  if (listado.has(rel) || scaffold.has(rel)) continue
  const copia = resolve(REPO_ROOT, 'app', rel)
  if (!existsSync(copia)) continue                       // no adoptado por esta app
  if (readFileSync(copia, 'utf8').includes(KEEP_MARKER)) continue
  sinEntrada.push(rel)
}

for (const line of lines) {
  const [synced, ...relParts] = line.split(/\s+/)
  const rel = relParts.join(' ')
  if (!synced || !rel) continue
  const src = join(registryApp, rel)
  if (!existsSync(src)) {
    vanished.push(rel)
    continue
  }
  const current = createHash('sha256').update(readFileSync(src)).digest('hex')
  if (current !== synced) stale.push(rel)
}

if (stale.length || vanished.length || sinEntrada.length) {
  console.error('[registry-fresh] this app is BEHIND the registry:')
  for (const rel of stale) console.error(`  STALE     app/${rel}  (registry moved ahead)`)
  for (const rel of vanished) console.error(`  REMOVED   app/${rel}  (no longer in the registry)`)
  for (const rel of sinEntrada) {
    console.error(`  UNTRACKED app/${rel}  (adopted from the registry but MISSING from the manifest)`)
  }
  console.error('')
  console.error('  Re-run scripts/sync-pharos-registry.sh (or merge the re-sync bot PR) to'
    + ' refresh the copies + manifest. Per-app adaptations marked `pharos-registry:keep`'
    + ' and the files listed in registry/scaffold.txt are excluded from the manifest on'
    + ' purpose and never flagged.')
  if (sinEntrada.length) {
    console.error('')
    console.error('  UNTRACKED means the manifest SHRANK: the file is still copied into the app'
      + ' and still in the registry, but nothing compares them any more. That is the blind spot'
      + ' this gate exists to prevent, so it fails rather than counting one file less.')
  }
  process.exit(1)
}

console.log(`[registry-fresh] OK — ${lines.length} adopted file(s) match the registry HEAD`
  + ` (${scaffold.size} scaffold path(s) excluded by registry/scaffold.txt).`)
