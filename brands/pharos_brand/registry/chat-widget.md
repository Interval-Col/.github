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
| `PharosChatAvatar` | `app/components/PharosChatAvatar.vue` | the assistant's mark — 11 glyphs (nautical-robot marks + plain nautical marks), all **inline SVG, zero deps** (the playground's copy imports lucide; the registry deliberately does not push an icon library onto adopters) |

**Deps (per adopting app):** `pnpm add marked dompurify` (+ `pnpm add -D @types/dompurify`).
`marked` renders the assistant's markdown; `DOMPurify` sanitizes it before
`v-html` — both are load-bearing for the XSS boundary, never drop one.

**Tokens:** the widget uses the token contract only (`--popover`, `--primary`,
`--muted`, `--foreground`, `--border`, `--status-error*`, `--font-mono`, …) — no
hex, no legacy `--text-*`/`--bg-surface` vars — so it re-accents cleanly under any
sub-brand `.theme-*`. If a target app predates the token contract, sync
`pharos-tokens.css` first (`check-token-drift` covers it).

## Per-app config (CH7 extension points)

| Prop | Type | finance-lch | biuman-lis | Notes |
|---|---|---|---|---|
| `send` | `(payload) => Promise<ChatReply>` | `(p) => helpApi.chat(p)` | `(p) => kbChatApi.chat(p)` | **required**; app-owned transport (Bearer / 401→SSO bounce stay app-side, like `createPharosAdminApi`) |
| `brandName` | `string` | `'Pháros ERP'` | `'Biuman'` | shown in the greeting |
| `title` | `string` | `'Asistente de ayuda'` | `'Asistente de ayuda'` | panel aria-label; also the heading when the assistant has no name |
| `starters` | `string[]` | factura / causación / datos maestros | KB-derived | opening chips; `[]` = none |
| `storageKey` | `string` | `'finance-lch-help-chat-history'` | `'biuman-lis-kb-chat-history'` | **must be unique per app** so histories never collide |
| `placeholder` | `string` | (default) | (default) | textarea placeholder |

## Presentation (RFC 0017 — `registry/spec/chat.md` is the source of these values)

These are **brand decisions, not per-app taste.** The playground (`design-studio`) decides them and
writes `registry/spec/chat.md`; apps pass the decided values through. Don't fork them per app —
that's the third variant this widget exists to prevent.

Every one defaults to the **pre-2026-07-13 behaviour**, so an app that re-syncs without touching its
mount renders exactly what it rendered before.

| Prop | Type | Default | Decided | Notes |
|---|---|---|---|---|
| `trigger` | `'floating' \| 'topbar'` | `floating` | **`topbar`** | `floating` = fixed bubble, bottom-right. `topbar` = an **in-flow** button — ⚠️ **requires mounting the component inside the app's topbar** (see below) |
| `form` | `'corner' \| 'sheet'` | `corner` | **`corner`** | `corner` = card, bottom-right. `sheet` = full-height right-hand drawer + backdrop |
| `assistantName` | `string` | `''` | **`'Nerea'`** | proper name; `''` = unnamed (heading falls back to `title`, greeting stays generic) |
| `avatar` | `string` | `''` | **`'nereid-holgada-orejas'`** | a `PharosChatAvatar` id; `''` = the plain speech-bubble mark |
| `avatarBg` | `'circulo' \| 'solo'` | `circulo` | **`solo`** | mark on a round chip, or bare |
| `statusLine` | `boolean` | `false` | **`true`** | «En línea» under the name + a dot on the topbar button. **Cosmetic — it does not probe the backend** |
| `citations` | `boolean` | `true` | **`true`** | render corpus-source chips on grounded replies (CH5) |

The `ChatMessage` / `ChatReply` shapes are exported from the component and match
the chat-contract wire format (`{ reply, sources?, blocked?, reason? }`).

### Built-in dialog behaviours (not knobs — always on, 2026-07-14)

- **Topbar toggle** — the launcher stays mounted while the panel is open (`aria-expanded` +
  active style); a second click closes. With `form: sheet` the full-height drawer physically
  covers it — the full open/close cycle is a `corner` benefit.
- **Width cycle** — a header button cycles 1× → 2× → 3× (`corner`: 380/760/1140px ·
  `sheet`: 22/44/66rem), always capped by the viewport `max-width`.
- **Copy message** — hover/keyboard-focus action on every turn; copies the raw markdown.
- **Regenerate** — on the last assistant reply; re-sends the same question through the
  app's `send` transport.
- **«Al final» pill** — appears when the user scrolls >160px away from the newest message.

### ⚠️ `trigger: 'topbar'` changes WHERE you mount the widget

With `floating`, the root is `position: fixed` and the mount point is irrelevant — anywhere in the
shell works. With `topbar`, the root becomes `display: contents`, so the button is laid out as a
**direct child of whatever contains it**. Mount it inside your topbar's action row, or the button
will appear wherever you happened to put the component.

```vue
<!-- app shell topbar -->
<header class="app-topbar">
  …
  <div class="topbar-actions">
    <NotificationsBell />
    <PharosHelpChat v-bind="chatProps" :send="(p) => helpApi.chat(p)" />  <!-- ← here -->
    <UserMenu />
  </div>
</header>
```

## Adoption

1. `scripts/sync-pharos-registry.sh --add components/PharosHelpChat.vue <app-fe-dir> [repo-root]`
   **and** `--add components/PharosChatAvatar.vue` — copies both into the app's `app/components/`
   and records them in the registry drift manifest (Lock 3, `check-registry-drift`).
   `PharosHelpChat` imports the avatar as a sibling (`./PharosChatAvatar.vue`), so syncing the chat
   without the avatar leaves a broken import.
2. `pnpm add marked dompurify && pnpm add -D @types/dompurify`. (No icon library — every glyph in
   `PharosChatAvatar` is inline SVG.)
3. Mount it **inside the app's topbar** (the decided `trigger: topbar` needs it — see above), wiring
   the app's transport and the decided presentation values:
   ```vue
   <!-- app/layouts/default.vue — inside the topbar's action row -->
   <script setup lang="ts">
   import PharosHelpChat from '~/components/PharosHelpChat.vue'
   import { helpApi } from '~/utils/api'   // the app's own chat endpoint client
   </script>
   <template>
     <header class="app-topbar">
       <div class="topbar-actions">
         <PharosHelpChat
           :send="(p) => helpApi.chat(p)"
           brand-name="Pháros ERP"
           :starters="['¿Cómo proceso una factura?', '¿Qué es la causación?']"
           storage-key="finance-lch-help-chat-history"
           trigger="topbar"
           form="corner"
           assistant-name="Nerea"
           avatar="nereid-holgada-orejas"
           avatar-bg="solo"
           status-line
         />
       </div>
     </header>
   </template>
   ```
   Omit the presentation props entirely and you get the old floating bubble + corner panel — which is
   exactly what a re-sync without a mount change should do.
4. Flip `fe_registry_widget: on` in `.chat-contract.yml`; the H8 check then holds
   the widget in place (a hand-rolled `HelpChat.vue` fails the gate).

> finance-lch's revival (RFC 0017 Phase 5, fin#140) re-mounts the widget in the
> app-shell layout it lost in commit `9caa87b`.
>
> **biuman-lis — el asistente NO va anidado dentro del panel «Conocimiento Biuman»** (revisa
> biuman-lis#31, que proponía lo contrario). Son dos superficies distintas: el **conocimiento**
> sale al sidebar como pestaña propia (consulta deliberada del corpus), y el **asistente** se abre
> desde un **botón en el topbar** hacia un **cajón lateral** (pregunta de paso). Decidido
> 2026-07-13.
>
> Eso fija `trigger: topbar` + `form: sheet` en `registry/spec/chat.md`, y **el componente ya los
> honra** (#126, 2026-07-13): las props de la tabla de arriba son reales. Ambas apps pueden adoptar
> el layout decidido re-sincronizando el widget + el avatar y montándolo dentro de su topbar.
