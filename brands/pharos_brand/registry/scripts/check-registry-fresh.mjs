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
import { readFileSync, existsSync } from 'node:fs'
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

if (stale.length || vanished.length) {
  console.error('[registry-fresh] this app is BEHIND the registry:')
  for (const rel of stale) console.error(`  STALE     app/${rel}  (registry moved ahead)`)
  for (const rel of vanished) console.error(`  REMOVED   app/${rel}  (no longer in the registry)`)
  console.error('')
  console.error('  Re-run scripts/sync-pharos-registry.sh (or merge the re-sync bot PR) to'
    + ' refresh the copies + manifest. Per-app adaptations marked `pharos-registry:keep`'
    + ' are excluded from the manifest and never flagged.')
  process.exit(1)
}

console.log(`[registry-fresh] OK — ${lines.length} adopted file(s) match the registry HEAD.`)
