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
| `PharosChatAvatar` | `app/components/PharosChatAvatar.vue` | the assistant's mark — 12 glyphs (`sol` for the public assistant, nautical-robot marks + plain nautical marks), all **inline SVG, zero deps** (the playground's copy imports lucide; the registry deliberately does not push an icon library onto adopters) |

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
| `statusLine` | `boolean` | `false` | **`true`** | live status under the name + a presence dot on the topbar button. **Real, not decorative** — see below |
| `citations` | `boolean` | `true` | **`true`** | render corpus-source chips on grounded replies (CH5) |
| `probe` | `() => Promise<ChatHealth>` | — | — | app-owned readiness probe → `GET {base}/v1/chat/health` (chat-contract **CH8**). Same ownership split as `send` |
| `assistantRole` | `string` | `''` | — | el PAPEL, bajo el nombre («Asistente virtual»). `''` = no se pinta. ⚠️ Se llama así y no `role` porque `role` es un atributo ARIA |
| `privacyTitle` | `string` | `'Sin datos de pacientes.'` | — | encabezado del aviso de PHI, en sus dos sitios |
| `privacyBody` | `string` | (el de siempre, en usted) | — | cuerpo del aviso. **El trato cambia por superficie**: Nerea trata de usted, Sol tutea |

### Por qué el aviso de PHI y el papel son props (2026-09-20)

🔴 **El encabezado es `assistantName || title`**, así que una app que pasa las dos cosas
—nombre propio Y papel— **pierde el papel en silencio**. Medido en `lch-web`: pasaba
`assistant-name="Sol"` y `:title="$t('sol.papel')"`, el panel decía «Sol» a secas, y el
canon §4.1 («nunca finge ser humana») quedaba delegado a que el paciente preguntara.
`assistantRole` lo pinta debajo; sin él, el encabezado es exactamente el de antes.

🔑 **Y el aviso de PHI estaba cableado en usted, con vocabulario de personal:** «No escriba
nombres… Pregunte por cómo funciona **la aplicación**». Eso es correcto para Nerea
(`NEREA.md` §3: trata de usted) y equivocado para Sol (`SOL.md` §6: tutea, fallo del
2026-09-08) — y en `lch.co` no hay ninguna aplicación, hay un laboratorio, y quien pregunta
**es** el paciente. Un texto cableado obliga a una de las dos a hablar como la otra.

### El copy de error: gana el servidor (2026-09-20)

No es un prop, es una regla. Ante un **4xx**, si el backend de la app mandó un mensaje
(`detail` o `message`), **ese se pinta**; el texto cableado queda de respaldo para las apps
que no mandan ninguno.

🔴 El widget estaba tirando un texto mejor que el suyo: ante un 429 el backend de Sol
responde «Has hecho muchas preguntas seguidas. Intenta más tarde, **o llama al
604 444 42 00**» —con su tuteo y con una salida— y el widget lo reemplazaba por «Ha
alcanzado el límite de consultas. Intente más tarde.»

⚠️ **Sólo 4xx.** El cuerpo de un 5xx puede traer una traza o un mensaje de framework; ahí el
texto cableado es lo correcto. El mensaje se recorta a 300 caracteres, se descarta si empieza
por `<`, `{` o `[`, y se pinta con `{{ }}`, que Vue escapa.

### The status indicator (`statusLine` + `probe`)

It used to render a hard-coded green «En línea» whether or not anything worked. That is
worse than showing nothing: a user without the chat capability saw «En línea», asked a real
question, and got a 403 — the indicator sent them to open a ticket for a permission.

It now reports one of five states, from two sources, freshest-wins: the `probe` (on mount,
and on open once the last result is older than 60 s) and what actually happened on the last
send. A real reply is the strongest evidence there is, so traffic outranks a stale probe.

| state | word | when |
|---|---|---|
| `en-linea` | «en línea» | probe healthy, or a reply came back |
| `desconocido` | «sin verificar» | no probe wired and nothing sent yet |
| `sin-permiso` | «sin permiso» | `allowed: false`, or a 403 |
| `limitado` | «límite alcanzado» | a 429 |
| `no-disponible` | «no disponible» | chat off, proxy down, or a 5xx |

Each state carries its own **word, glyph and dot shape** — never colour alone (the dot is
10 px, and success/warning are a known confusable pair in this palette).

**`probe` is optional only during rollout.** Without it the status cannot know anything
until the first message is sent, which is precisely too late. `chat-contract-check` **H10**
warns while the per-app routes land and is designed to be flipped to a hard FAIL
(`H10_ENFORCED` in `scripts/chat-contract-check.py`) once every chat app carries one — so
the fallback cannot quietly become the permanent state.

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
- **PHI notice** — a warning block in the empty state (*«Sin datos de pacientes.»*) plus a
  compact persistent reminder above the input. **Always on, not a prop, not dismissible.**

### Why the PHI notice is not configurable

The proxy's outbound gate stops a patient identifier from *leaving* the organisation. This
addresses the step before that — not typing it in the first place — which is strictly
stronger, because it does not depend on a regex being right.

Three deliberate choices:

- **Not a prop.** Every Pháros app sits on a PHI-adjacent estate; making it opt-in invites
  someone to opt out of the one control that costs nothing.
- **Not dismissible.** A notice you can close stops existing for exactly the person who most
  needs it.
- **In two places.** The empty-state block disappears with the first message — precisely when
  the user starts typing freely — so the rule also lives permanently beside the input.

It uses `--status-warning` rather than `--status-error`: nothing has gone wrong, it is an
instruction. Icon + text + surface, never colour alone.

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
