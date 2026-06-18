#!/usr/bin/env node
// =============================================================================
// check-spec-drift.mjs — Layer-D gate for the GENERATED Pháros spec docs.
//
// The playground (design-studio) emits brands/pharos_brand/registry/spec/*.md via
// buildSpec(); each file carries a `<!-- spec-version: HASH -->` stamp. The
// registry shell + the apps IMPLEMENT a given version. `.implemented.json` is the
// ledger of which version is currently implemented per spec file.
//
// On every run we compare each spec's CURRENT stamp vs the IMPLEMENTED version:
//   • match            → OK (nothing pending)
//   • mismatch / new   → WARN "pending to implement" (the spec upgraded; the
//                        registry/apps haven't caught up). NON-BLOCKING — a
//                        visible backlog signal, like the contrast pastels.
// After you implement a spec change in the registry shell, bump `.implemented.json`
// to the new version to clear the pending flag. NEVER hand-edit spec/*.md — they
// are generated; re-export from the playground (Exportar spec) instead.
//
// Run from .github (registry-maintenance gate; NOT synced into apps).
// =============================================================================
import { readdirSync, readFileSync, existsSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const SPEC_DIR = resolve(HERE, '..', 'brands', 'pharos_brand', 'registry', 'spec')
const LEDGER = join(SPEC_DIR, '.implemented.json')

if (!existsSync(SPEC_DIR)) {
  console.log('[spec-drift] no registry/spec/ — skip (generate it from the playground first).')
  process.exit(0)
}

const VERSION_RE = /<!--\s*spec-version:\s*([0-9a-f]+)/i
const specs = readdirSync(SPEC_DIR).filter(f => f.endsWith('.md')).sort()
const implemented = existsSync(LEDGER) ? JSON.parse(readFileSync(LEDGER, 'utf8')) : {}

const pending = []
const missingStamp = []
for (const file of specs) {
  const m = readFileSync(join(SPEC_DIR, file), 'utf8').match(VERSION_RE)
  if (!m) { missingStamp.push(file); continue }
  const current = m[1]
  const impl = implemented[file]
  if (current !== impl) pending.push({ file, current, impl: impl ?? '(none)' })
}

if (missingStamp.length) {
  console.error(`[spec-drift] ${missingStamp.length} spec file(s) missing a spec-version stamp: ${missingStamp.join(', ')}`)
  console.error('  These are GENERATED — re-export from the playground (Exportar spec); do not hand-author.')
  process.exit(1)
}

if (pending.length) {
  console.log(`[spec-drift] ${pending.length} spec(s) PENDING implementation (the playground advanced; registry/apps haven't caught up):`)
  for (const p of pending) console.log(`  ⏳ spec/${p.file} — current ${p.current}, implemented ${p.impl}`)
  console.log('  → implement the change in the registry shell, then bump scripts/../registry/spec/.implemented.json. (Non-blocking backlog signal.)')
  process.exit(0)
}

console.log(`[spec-drift] OK — all ${specs.length} spec(s) implemented (versions match .implemented.json).`)
