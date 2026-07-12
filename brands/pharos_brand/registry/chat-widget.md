# Pháros chat widget — PharosHelpChat (RFC 0017 Phase 4)

The shared FE for an app's **in-app AI assistant** — the floating launcher +
slide-up chat panel. ONE definition so it can't drift across apps
(finance-lch ↔ biuman-lis ↔ …). The **backend** half converges via the
[chat contract](../../../chat-contract.md); this is its FE half.

> This is the **widget** (transport-agnostic UI). The **product** decisions —
> what the assistant knows, how it retrieves — are per-app (chat-contract CH7);
> the gateway (`pharos-llm-proxy`) is shared (RFC 0017 Phase 2).

## What's in the registry (synced verbatim)

| Entry | Path | What it is |
|---|---|---|
| `PharosHelpChat` | `app/components/PharosHelpChat.vue` | launcher + panel; sessionStorage history, marked+DOMPurify rendering, es-CO usted copy, graceful outage/rate-limit states, corpus-source chips (CH5) |

**Deps (per adopting app):** `pnpm add marked dompurify` (+ `pnpm add -D @types/dompurify`).
`marked` renders the assistant's markdown; `DOMPurify` sanitizes it before
`v-html` — both are load-bearing for the XSS boundary, never drop one.

**Tokens:** the widget uses the token contract only (`--popover`, `--primary`,
`--muted`, `--foreground`, `--border`, `--status-error*`, `--font-mono`, …) — no
hex, no legacy `--text-*`/`--bg-surface` vars — so it re-accents cleanly under any
sub-brand `.theme-*`. If a target app predates the token contract, sync
`pharos-tokens.css` first (`check-token-drift` covers it).

## Per-app config (the only knobs — CH7 extension points)

| Prop | Type | finance-lch | biuman-lis | Notes |
|---|---|---|---|---|
| `send` | `(payload) => Promise<ChatReply>` | `(p) => helpApi.chat(p)` | `(p) => kbChatApi.chat(p)` | **required**; app-owned transport (Bearer / 401→SSO bounce stay app-side, like `createPharosAdminApi`) |
| `brandName` | `string` | `'Pháros ERP'` | `'Biuman'` | shown in the greeting |
| `title` | `string` | `'Asistente de ayuda'` | `'Asistente de ayuda'` | panel title + aria-label |
| `starters` | `string[]` | factura / causación / datos maestros | KB-derived | opening chips; `[]` = none |
| `storageKey` | `string` | `'finance-lch-help-chat-history'` | `'biuman-lis-kb-chat-history'` | **must be unique per app** so histories never collide |
| `placeholder` | `string` | (default) | (default) | textarea placeholder |

The `ChatMessage` / `ChatReply` shapes are exported from the component and match
the chat-contract wire format (`{ reply, sources?, blocked?, reason? }`).

## Adoption

1. `scripts/sync-pharos-registry.sh --add components/PharosHelpChat.vue <app-fe-dir> [repo-root]`
   — copies the widget into the app's `app/components/` and records it in the
   registry drift manifest (Lock 3, `check-registry-drift`).
2. `pnpm add marked dompurify && pnpm add -D @types/dompurify`.
3. Mount it once in the app shell (a layout), wiring the app's transport:
   ```vue
   <!-- app/layouts/default.vue (or the app-shell) -->
   <script setup lang="ts">
   import PharosHelpChat from '~/components/PharosHelpChat.vue'
   import { helpApi } from '~/utils/api'   // the app's own chat endpoint client
   </script>
   <template>
     <!-- …app shell… -->
     <PharosHelpChat
       :send="(p) => helpApi.chat(p)"
       brand-name="Pháros ERP"
       :starters="['¿Cómo proceso una factura?', '¿Qué es la causación?']"
       storage-key="finance-lch-help-chat-history"
     />
   </template>
   ```
4. Flip `fe_registry_widget: on` in `.chat-contract.yml`; the H8 check then holds
   the widget in place (a hand-rolled `HelpChat.vue` fails the gate).

> finance-lch's revival (RFC 0017 Phase 5, fin#140) re-mounts the widget in the
> app-shell layout it lost in commit `9caa87b`; biuman-lis adds it as a tab in the
> existing «Conocimiento Biuman» panel (biuman-lis#31).
