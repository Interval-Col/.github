#!/usr/bin/env node
/**
 * CI gate: forbid `<style scoped>` blocks in `app/pages/**` and
 * `app/layouts/**`.
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * NO EXCEPTIONS. Pages/layouts must use Tailwind utilities + shadcn-vue
 * primitives. Scoped styles are allowed only in `app/components/**`. Do not
 * introduce an allowlist; migrate the file instead.
 *
 * Ported from finance-lch/frontend/scripts (RFC 0008 §6 design gates).
 */
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = resolve(__dirname, '..')
const SCAN_ROOTS = [
  join(REPO_ROOT, 'app', 'pages'),
  join(REPO_ROOT, 'app', 'layouts'),
]

const RE = /<style\s+(?:[^>]*\s+)?scoped(?:\s|>)/i

function* walk(root) {
  let entries
  try {
    entries = readdirSync(root)
  } catch {
    return
  }
  for (const name of entries) {
    const full = join(root, name)
    const s = statSync(full)
    if (s.isDirectory()) {
      yield* walk(full)
    } else if (s.isFile() && full.endsWith('.vue')) {
      yield full
    }
  }
}

const offenders = []
for (const root of SCAN_ROOTS) {
  for (const file of walk(root)) {
    if (RE.test(readFileSync(file, 'utf8'))) {
      offenders.push(relative(REPO_ROOT, file))
    }
  }
}

if (offenders.length) {
  console.error()
  console.error(
    `[no-scoped-pages] ${offenders.length} file(s) use <style scoped> in pages/layouts:`,
  )
  for (const f of offenders) console.error(`  - ${f}`)
  console.error()
  console.error(
    'Use Tailwind utilities + shadcn-vue primitives instead (scoped styles are allowed only in app/components/**).',
  )
  process.exit(1)
}

console.log('[no-scoped-pages] OK — no <style scoped> in pages/layouts (no exceptions)')
