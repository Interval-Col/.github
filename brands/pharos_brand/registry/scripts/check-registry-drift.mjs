#!/usr/bin/env node
// =============================================================================
// check-registry-drift.mjs — Layer-D copy-in integrity gate (RFC 0008 / RFC 0016
// Lock 3). The registry-wide generalization of check-token-drift.
//
// Guards EVERY copied-in registry file (not just tokens.css): asserts each
// synced `app/**` file still byte-matches the registry source it was copied
// from — so an app can't silently hand-edit a shared primitive (e.g. the RFC
// 0016 admin block) and fork it. sync-pharos-registry.sh drops a manifest
// (`app/assets/pharos-registry.sha256`: `<sha256>  <relpath-under-app>` per
// line, one per synced file, EXCLUDING the app-owned presets it skips); this
// re-hashes each listed file and compares.
//
// Semantics: detects LOCAL edits since the last sync (drift), NOT staleness
// vs the current registry — re-running the sync refreshes both copy + manifest.
//
// Self-contained (node:fs + node:crypto). REPO_ROOT = the dir containing app/
// (argv[2] override). No-ops cleanly where no manifest exists (the registry
// itself, or an app synced before Lock 3 landed).
// =============================================================================
import { readFileSync, existsSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = process.argv[2] ? resolve(process.argv[2]) : resolve(HERE, '..')
const manifestPath = resolve(REPO_ROOT, 'app', 'assets', 'pharos-registry.sha256')

if (!existsSync(manifestPath)) {
  console.log('[registry-drift] no pharos-registry.sha256 manifest — skip '
    + '(run scripts/sync-pharos-registry.sh to adopt Lock 3).')
  process.exit(0)
}

const lines = readFileSync(manifestPath, 'utf8')
  .split('\n')
  .map(l => l.trim())
  .filter(Boolean)

const missing = []
const drifted = []

for (const line of lines) {
  const [want, ...relParts] = line.split(/\s+/)
  const rel = relParts.join(' ')
  if (!want || !rel) continue
  const file = resolve(REPO_ROOT, 'app', rel)
  if (!existsSync(file)) {
    missing.push(rel)
    continue
  }
  const got = createHash('sha256').update(readFileSync(file)).digest('hex')
  if (got !== want) drifted.push(rel)
}

if (missing.length || drifted.length) {
  console.error('[registry-drift] copied-in registry files diverge from the contract:')
  for (const rel of drifted) console.error(`  DRIFTED  app/${rel}`)
  for (const rel of missing) console.error(`  MISSING  app/${rel}`)
  console.error('')
  console.error('  Do NOT hand-edit synced registry files. Land the change in the'
    + ' registry (Interval-Col/.github) and re-run sync-pharos-registry.sh to'
    + ' refresh the copy + manifest.')
  process.exit(1)
}

console.log(`[registry-drift] OK — ${lines.length} synced registry file(s) match the contract.`)
