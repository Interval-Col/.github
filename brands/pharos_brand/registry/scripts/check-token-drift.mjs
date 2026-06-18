#!/usr/bin/env node
// =============================================================================
// check-token-drift.mjs — Layer-D brand-compliance gate (RFC 0008).
//
// Guards the copy-in: asserts the app's synced `app/assets/css/pharos-tokens.css`
// still matches the authoritative registry source — so an app can't silently fork
// the token contract by hand-editing its copy. The sync (sync-pharos-registry.sh)
// drops a `pharos-tokens.css.sha256` sidecar (the registry source's hash); this
// recomputes the copy's hash and compares.
//
// Self-contained (node:fs + node:crypto). REPO_ROOT = the dir containing app/
// (argv[2] override). No-ops cleanly where no synced tokens exist (e.g. the registry).
// =============================================================================
import { readFileSync, existsSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = process.argv[2] ? resolve(process.argv[2]) : resolve(HERE, '..')
const tokens = resolve(REPO_ROOT, 'app', 'assets', 'css', 'pharos-tokens.css')
const sidecar = `${tokens}.sha256`

if (!existsSync(tokens)) {
  console.log('[token-drift] no synced pharos-tokens.css — skip (run scripts/sync-pharos-registry.sh first).')
  process.exit(0)
}
if (!existsSync(sidecar)) {
  console.error('[token-drift] pharos-tokens.css present but no .sha256 sidecar — re-run sync-pharos-registry.sh.')
  process.exit(1)
}

const want = readFileSync(sidecar, 'utf8').trim().split(/\s+/)[0]
const got = createHash('sha256').update(readFileSync(tokens)).digest('hex')

if (got !== want) {
  console.error('[token-drift] pharos-tokens.css has DRIFTED from the registry contract.')
  console.error(`  expected ${want}`)
  console.error(`  found    ${got}`)
  console.error('  Do NOT hand-edit pharos-tokens.css. Re-run the sync to refresh, or land the change in the registry.')
  process.exit(1)
}
console.log('[token-drift] OK — pharos-tokens.css matches the registry contract.')
