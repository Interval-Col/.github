#!/usr/bin/env node
/**
 * CI gate: forbid raw HTML form/data primitives in `app/pages/**` and
 * `app/layouts/**`. Use the shadcn-vue equivalents from `~/components/ui/*`:
 *   <button>   → <Button>    · <table>  → <Table> (+ TableHeader/Row/Head/Body/Cell/Empty)
 *   <input>    → <Input>     · <select> → <Select> (+ Trigger/Value/Content/Item)
 *   <textarea> → <Textarea>
 *
 * CANONICAL REGISTRY COPY — source of truth for this gate script.
 * Distributed to consuming apps via scripts/sync-pharos-registry.sh.
 * Do NOT edit the per-app copy; edit here and re-sync.
 *
 * Documented INLINE exceptions (matched in code below):
 *   - <input type="file">  — shadcn-vue has no file-input primitive; use a
 *                            native element with Tailwind `file:` utilities.
 *   - reka-ui combobox slotted <input> — the headless API requires it.
 *
 * File-level ALLOWLIST: each entry is a DOCUMENTED exception (org policy —
 * ENGINEERING_STANDARDS.md "Allowlists are intentional"). Keep it tiny and
 * justified; prefer migrating the file.
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

// Banned tags. Match opening-tag-with-attributes or self-closing forms;
// avoid PascalCase components (<Button>) by requiring lowercase + a
// non-letter afterwards. The `$` arm covers multi-line opening tags.
const BANNED_TAG_RE = /<(button|table|input|select|textarea)(\s|>|\/|$)/
const FILE_INPUT_TYPE_RE = /\btype\s*=\s*["']file["']/

// Documented file-level exceptions (keep tiny + justified).
const ALLOWLIST = new Set([
  // app-specific exceptions go here
])

// The opening <input ...> tag may wrap across many lines before its
// `type="file"` attribute appears; scan a window until the tag closes.
function isFileInput(lines, startIndex) {
  for (let i = startIndex; i < Math.min(startIndex + 20, lines.length); i++) {
    if (FILE_INPUT_TYPE_RE.test(lines[i])) return true
    if (/>/.test(lines[i]) && i > startIndex) return false
  }
  return false
}

function* walk(root) {
  let entries
  try { entries = readdirSync(root) } catch { return }
  for (const name of entries) {
    const full = join(root, name)
    const s = statSync(full)
    if (s.isDirectory()) yield* walk(full)
    else if (s.isFile() && full.endsWith('.vue')) yield full
  }
}

const offenders = []
for (const root of SCAN_ROOTS) {
  for (const file of walk(root)) {
    const rel = relative(REPO_ROOT, file)
    if (ALLOWLIST.has(rel)) continue
    const text = readFileSync(file, 'utf8')

    // Only scan the <template>; script blocks may mention tag names in
    // strings, types, or comments.
    const templateMatch = text.match(/<template>([\s\S]*?)<\/template>/m)
    if (!templateMatch) continue
    const lines = templateMatch[1].split('\n')
    const startLine = (text.slice(0, templateMatch.index).match(/\n/g) ?? []).length + 2

    const hits = []
    for (let i = 0; i < lines.length; i++) {
      const m = lines[i].match(BANNED_TAG_RE)
      if (!m) continue
      if (m[1] === 'input' && isFileInput(lines, i)) continue
      hits.push({ lineNumber: startLine + i, content: lines[i].trim() })
    }
    if (hits.length) offenders.push({ rel, hits })
  }
}

if (offenders.length) {
  console.error()
  const total = offenders.reduce((n, o) => n + o.hits.length, 0)
  console.error(`[no-raw-html] ${offenders.length} file(s) / ${total} site(s) use raw HTML primitives in app/pages or app/layouts:`)
  for (const o of offenders) {
    for (const h of o.hits) {
      console.error(`  - ${o.rel}:${h.lineNumber}  ${h.content.slice(0, 100)}${h.content.length > 100 ? '…' : ''}`)
    }
  }
  console.error()
  console.error('Replace with the matching ~/components/ui/* primitive (<Button>, <Input>, <Select>, …).')
  process.exit(1)
}

console.log('[no-raw-html] OK — no raw HTML primitives in pages/layouts (no exceptions)')
