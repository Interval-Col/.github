---
status: superseded
superseded-by: brand-playground-build-plan.md (all content merged there 2026-06-14)
created: 2026-06-14
updated: 2026-06-15
owner: gczuluaga
implementation: gczuluaga
language: English body; Spanish "Resumen" + decision/criteria glosses.
relates-to: RFC 0008 Q4/Q5/Q6/Q7/Q9/Q11
---

# Pháros brand playground — tweaks plan · Plan de ajustes al playground de marca

> **This plan has been merged into `brand-playground-build-plan.md` and is archived.**
> All phases, fixes (T4/T5/T6/T7), and the §9 acceptance checklist from this file
> now live in the build plan as Phases 10–15 and §13–15. Do not run this file —
> run the merged build plan instead.

> **Resumen (ES).** Tres ajustes pedidos por el operador sobre la app local del
> playground de marca Pháros (`/Users/gczuluaga/dev/pharos-playground/`): (1)
> convertir el panel "Marca" de un cajón superpuesto a un panel fijo a la derecha,
> redimensionable y con ancho persistido; (2) restilizar la barra superior al
> patrón de finance-lch (logo Pháros + divisor + breadcrumb con popover + cluster
> derecho con toggle de tema), sobre el sustrato `.dark`/tokens shadcn; (3) fuentes
> más ricas — un selector de 8 monoespaciadas + un interruptor de "fuente de datos"
> apagado por defecto. De paso se corrige un bug latente: el selector de fuentes v1
> no hacía nada. **Este plan ya está fusionado en el build plan y archivado — no se
> ejecuta.**

Three operator-requested tweaks to the **existing** local app at
`/Users/gczuluaga/dev/pharos-playground/` (built by
`brand-playground-build-plan.md`), plus a latent-bug fix found while planning. The
plan is auto-runnable phase-by-phase; it encodes locked RFC 0008 co-creation
decisions so an agent does not drift. It is now **superseded** — its content lives
in the merged build plan.

---

## How to use this plan · Cómo usar este plan

**EN.** This plan is written to be executed with AI-agent assistance — that is
expected and encouraged. The plan, not the agent, makes the technical decisions.
Your job has three parts: **execute** the tasks, **verify** each one against its
Done-when list, and **escalate** the decisions the plan marks for a human.

Read each task fully — including its **Why** and **Done-when** — *before* you start
it. A task is not finished because an agent said so; it is finished when every
Done-when line is literally true and you have checked it yourself.

If a task or its **Why** doesn't make sense, that is a gap in *this plan*, not a
failing in you — stop and ask gczuluaga. A question costs minutes; a
misunderstanding shipped costs days.

**If the English here slows you down:** every section opens with a Spanish
**Resumen**, and your AI agent will translate or explain any part of this plan in
Spanish if you ask it — that is a completely legitimate thing to do. Don't let the
language be the reason a task stalls.

**ES.** Este plan está escrito para ejecutarse con ayuda de agentes de IA — eso se
espera y se fomenta. Las decisiones técnicas las toma el plan, no el agente. Tu
trabajo tiene tres partes: **ejecutar** las tareas, **verificar** cada una contra su
lista *Done-when*, y **escalar** las decisiones que el plan marca para un humano.

Lee cada tarea completa — incluyendo su **Why** y su **Done-when** — *antes* de
empezarla. Una tarea no está terminada porque un agente lo diga; está terminada
cuando cada línea *Done-when* es literalmente cierta y tú mismo la verificaste.

Si una tarea o su **Why** no te quedan claras, eso es un vacío de *este plan*, no una
falla tuya — pregúntale a gczuluaga. Y si el inglés te frena: cada sección tiene un
**Resumen** en español, y tu agente de IA te traduce o explica cualquier parte en
español si se lo pides — hazlo sin problema.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| 💡 **Heuristic** | A short engineering or working lesson. Worth 30 seconds. *(ES: heurística — lección breve.)* |
| 🛑 **HUMAN DECISION** | A choice the plan deliberately does not make. **Do not let an agent pick it.** Escalate to gczuluaga. *(ES: decisión humana — no la toma un agente; escala a gczuluaga.)* |
| ✅ **Done-when** | The Definition of Done. The phase is verified only when every line is literally true. *(ES: terminado-cuando — definición de "hecho".)* |
| 🚦 **Checkpoint** | Stop. Show gczuluaga the named evidence and answer the questions before continuing. **Mandatory stop — including in auto mode** (see Working rules). *(ES: punto de control — alto obligatorio, también en modo auto.)* |

> **On the checkpoints.** Each 🚦 lists evidence to show and questions to answer.
> The questions are **not a test of you** — they test whether the plan explained
> things well enough. gczuluaga may also ask any of them at any time. *(ES: las
> preguntas del checkpoint no son un examen tuyo — prueban si el plan explicó bien;
> gczuluaga puede preguntarlas en cualquier momento.)*

## Working rules · Reglas de trabajo

These apply to every phase.

- **Commit and push after every slice.** When a task group or a phase is done and
  its Done-when checks pass, commit and push to GitHub **immediately**. Work that
  lives only on your laptop cannot be seen, reviewed, helped with, or recovered.
  *(ES: haz commit y push a GitHub apenas termines — el trabajo que solo vive en tu
  laptop no existe para el equipo.)* — **Note for this plan:** the playground is
  local-only; **don't push** (see §2). The "commit and push" rule still governs the
  message/branch shape; the push target simply doesn't exist yet.
- **Merge mode — merge-commit everywhere.** Org standard is merge-commit; **squash
  is disabled** ("Allow squash merging" off). Do not squash. *(ES: modo de merge =
  merge-commit en todos lados; squash desactivado.)*
- **Commit messages — Conventional Commits, scope required.**
  `type(scope): description` — e.g. `feat(playground): panel de marca fijo y
  redimensionable`. `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The
  `(scope)` is **mandatory**. Branch names mirror it: `type/scope-short-description`.
  Note: `hotfix` is valid as **both** a branch type and a commit type; `ci` is part
  of the canonical set (added org-wide). *(ES: Conventional Commits; el `(scope)` es
  obligatorio; la rama refleja el commit; `hotfix` sirve como rama y como commit;
  `ci` ya es parte del set canónico.)*
- **Review the frontend yourself, in the browser.** A phase that touches the UI is
  **not verified** because the backend endpoint returned `200` — it is verified when
  you have opened the app, clicked through what you built, and seen it work the way a
  real user would use it. *(ES: revisa el frontend tú mismo, en el navegador — un
  `200` del backend no es una funcionalidad que sirve.)*
- **Which AI tool:** Claude **Sonnet** by default; **Opus** when a task is hard or
  you are stuck; **Copilot** for inline autocomplete and quick questions — not for
  executing a whole task. *(ES: Sonnet por defecto; Opus cuando es difícil o te
  atascas; Copilot para autocompletar.)*
- **You can tell your agent to skip the Why boxes — we won't stop you.** But the 🚦
  checkpoint questions are asked by a person, and that you cannot outsource. Reading
  as you go is the cheap way to be ready. *(ES: puedes pedirle a tu agente que se
  salte las explicaciones — pero las preguntas del checkpoint las hace una persona;
  eso no se delega.)*
- **Auto mode is slice-bounded.** Auto mode (running without clarifying questions
  between turns) is allowed for the duration of **one slice** — a single numbered
  task, or one phase when the plan groups tasks that way. At the end of every slice,
  the agent **STOPS**, surfaces what landed (Done-when items verified, files
  touched, what's next), and waits for explicit human acknowledgement before
  starting the next slice. At 🚦 Checkpoints the stop is stronger — the human walks
  the evidence with the agent. Auto mode is **never** "execute the whole plan
  unattended." *(ES: el modo auto va por slice, no por plan entero. Al final de cada
  slice, el agente **PARA**, te muestra qué cerró (Done-when, archivos tocados, qué
  viene) y espera tu visto bueno antes del siguiente slice. En los 🚦 el alto es más
  fuerte — recorres la evidencia con el agente. Auto **nunca** significa "ejecuta el
  plan completo solo".)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que vas a ver muchas veces en este
> plan, con su traducción y una línea de qué significan. Si te encuentras un término
> del plan que no está aquí y no lo entiendes, pregúntale a tu agente — no es una
> falla tuya, es un vacío de esta tabla.

| English | Español | Means |
|---|---|---|
| token contract | contrato de tokens | the registry's `tokens.css` — the shared set of CSS variables (shadcn-vue vars + the accent-independent status palette) every Pháros surface copies in |
| accent | acento | the one brand colour a sub-brand overrides — `--primary`/`--accent`/`--ring`/`--sidebar-primary` only; everything else stays shared |
| status palette | paleta de estado | the accent-**independent** `--success`/`--warning`/`--error`/`--info` (+ foregrounds) that never moves when the accent changes (RFC 0008 Q4) |
| resizer / handle | redimensionador / asa | the 6px draggable divider between the preview and the Marca panel; its width persists |
| stack var | variable de stack de fuente | an overridable `--font-*-stack` CSS var the utility reads, so a runtime font override actually renders |
| data font | fuente de datos | a separate face applied only to cifras when the toggle is ON, with `tabular-nums`/`slashed-zero` |
| FOUC guard | guarda anti-FOUC | the inline script that sets `.dark` before paint so the theme doesn't flash on reload |
| Done-when | terminado-cuando | the literal checkable list that means the task is verified |
| commit + push | hacer commit y push | save to git locally **and** send to GitHub — both verbs (here: local-only, no push) |
| slice | rebanada / unidad de trabajo | a small piece of work (one task or one phase) that can ship on its own |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es para después /
> lo decide un humano. Si un agente sugiere construir algo de esta lista, no lo
> hagas.

Explicitly out of scope — not for this plan:

- **Resolving the data-font question.** The brand-book "data font" exploration and
  the canonical 3-family lock (Fraunces · Inter · IBM Plex Mono) are reconciled in
  Decisions, not here — the playground only *shows* options so a human can decide.
- **Pushing anywhere.** Still local-only; the future home is the registry sync
  (RFC 0008 Q3), not this app.
- **`[data-theme]` / cobol / CRT theme / 3-way toggle.** Light + dark only via the
  shadcn `.dark` class; the cobol theme is dropped.
- **Inventing non-ERP sub-brand accents.** They are 🛑 OPEN (→ @SKuger01 / brand
  playground); never invent them.

---

## 1. Locked invariants — DO NOT DRIFT (RFC 0008 co-creation)

> **Resumen (ES) — §1: invariantes bloqueadas.** Reglas decididas antes de este
> plan; nada aquí puede violarlas. Tema = clase `.dark` (claro/oscuro, sin cobol).
> Tokens = contrato shadcn + paleta de estado independiente del acento. Shell =
> `Sidebar collapsible="icon"`. Fuentes = Fraunces · Inter · IBM Plex Mono. El
> acento solo mueve `--primary`/`--accent`/`--ring`/`--sidebar-primary`. ERP · Timón
> = navy LCH bloqueado; los demás acentos están abiertos (TBD). Distribución =
> copia vía script de registry, no paquete npm. Un tenant nunca antepone su nombre
> al de la app.

These were settled before this plan; nothing here may violate them. The
**source of truth** is the registry at
`/Users/gczuluaga/dev/.github/brands/pharos_brand/registry/`; its token contract is
`registry/tokens.css`.

- **Design system tenancy.** Pháros is the umbrella **product design system**; LCH
  and Biuman are **tenants** of it. A tenant **never prefixes an app name** (it is
  `Pháros · Timón`, never "LCH Pháros"). Maker credit = *Interval · The Human Tech
  Co.* (footer only).
- **Theming = `.dark` CLASS** on `<html>`, **light/dark only, NO cobol** (Q7). Do
  NOT introduce `[data-theme]` or a 3-way toggle even though finance-lch's real
  shell uses them — they are explicitly dropped.
- **Tokens = shadcn-vue contract + accent-INDEPENDENT status palette** (Q4). The
  status palette is `--success` / `--warning` / `--error` / `--info` (+ their
  `*-foreground`) and NEVER moves with the accent. Brand accent → `--primary` (+
  `--accent`, `--ring`, `--sidebar-primary`, `--sidebar-ring`, `--chart-1`) only.
  Use `--sidebar-*` / shadcn tokens for chrome — NOT finance-lch's `--nav-*`. Legacy
  names collapse: `--text-secondary`/`--text-muted` → `--muted-foreground`;
  `--text-brand` → `--primary`; `--nav-*` → `--sidebar-*`.
  - 💡 **Heuristic.** Where this plan's *embedded code* (built before the contract
    was finalized) writes `--status-*`, treat that as the playground's historical
    naming; the canonical contract name is the status palette above. The divergence
    is logged in Decisions, not silently rewritten in the archived code. *(ES: el
    código embebido usa `--status-*`; el nombre canónico es la paleta de estado; la
    diferencia queda registrada en Decisiones, no se reescribe el código archivado.)*
- **Shell = shadcn `Sidebar collapsible="icon"`** (lab-qc is the RFC shell
  reference; we keep it and only restyle the topbar). **NO page `<h1>`** — the
  breadcrumb's bold last segment is the title. **UI copy in Spanish** (neutral
  Colombian; no exclamations, no emojis — brand voice).
- **3-family system stays: Fraunces (display/wordmark) · Inter (sans UI) · IBM Plex
  Mono (data + labels)** (Q5). JetBrains Mono and Apax are **NOT used in product
  UI** (Apax stays an LCH brand-identity asset only). The richer mono set + data-font
  toggle in this plan are **playground exploration** — the sanctioned way to validate
  the mono before final lock and to let the team SEE the brand-book data-font split.
  The **default state must still be Q5**: mono = IBM Plex Mono, data font OFF (so one
  mono is used for everything until someone flips the toggle).
- **Accent rule.** A sub-brand overrides ONLY `--primary`/`--accent`/`--ring`/
  `--sidebar-primary`. **ERP · Timón = LCH Navy `#003A70`** (+ teal `#A0D1CA`
  success) — **LOCKED**. Non-ERP accents (LIS clínico, LIS deportivo, Admisiones,
  CRM, Archivo) are **OPEN → TBD** (RFC 0008 Q1/Q6, @SKuger01 / brand playground);
  **never invent them**.
- **Charts = @unovis, `--chart-1..5`** (Q11), client-only. Unchanged.
- **Pilot-light red `#E4002B` is shared and never re-tinted** (brand book) — the
  logo SVGs already encode this; do not recolor them.
- **Distribution = copy-in via `scripts/sync-pharos-registry.sh`** (NOT an npm
  package — RFC 0008 Q3).
- Keep the v1 build fixes intact: `reka-ui@2.9.6`, the `typescript` devDep +
  `tsConfig.paths['reka-ui']`, `striptags` dep + `optimizeDeps.include`,
  `build.transpile` for @unovis, the FOUC guard script.

## 2. Prerequisites · Prerrequisitos

> **Resumen (ES) — §2: prerrequisitos.** La app ya construida según el build plan y
> arrancando en `http://localhost:3000`. `node >= 22`, `pnpm@10+`. Los componentes
> shadcn-vue vendorizados están presentes. Rama local; **no hacer push**.

- App already built per `brand-playground-build-plan.md` and booting on
  `http://localhost:3000`. `node >= 22`, `pnpm@10+`.
- Vendored shadcn-vue components present (confirmed): `popover`, `switch`, `select`,
  `label`, `badge`, `button`, `separator`, `sidebar`, `card`, `table`, `tabs`,
  `dialog`, `sheet` (sheet becomes unused after Phase 4 — leave it vendored,
  harmless).
- Default branch is `main` of the fresh local repo; **don't push** (local-only).

---

## Phase 1 — Fonts foundation (fix the latent bug + register families)

> **Resumen (ES) — Fase 1: cimiento de fuentes.** Arregla el bug latente (el
> selector de fuentes v1 no hace nada porque `@theme inline` hornea el stack literal)
> y registra todas las familias seleccionables. Va primero porque sin la indirección
> `*-stack` ningún cambio de fuente se renderiza.
>
> En orden, las tareas:
>
> 1. **1.1** — Registrar todas las familias en `nuxt.config.ts` (`fonts.families`).
> 2. **1.2** — Enrutar las fuentes por variables `*-stack` sobre-escribibles en `main.css`.

**The bug:** the v1 font picker is a no-op. `@theme inline { --font-mono: <literal
stack> }` bakes the literal value into the `.font-mono` utility, so the store's
runtime `--font-mono` override never renders. This phase fixes it with a `*-stack`
indirection so the picker (and the new data axis) actually re-render the font.
(Verified 2026-06-14: setting `--font-mono` on `<html>` does not change the computed
`font-family` of a `.font-mono` element.)

- [x] **1.1** — `nuxt.config.ts` — register all selectable families.
      Replace the entire `fonts.families` array body with this (all
      `provider: 'google'`, verified on Google Fonts 2026-06-14). `families:`
      appears once in the file; replace the whole `[ ... ]` body and leave every
      other key unchanged.

      ```ts
        fonts: {
          families: [
            { name: 'Fraunces',         weights: [400, 500],      provider: 'google' },
            { name: 'Inter',            weights: [400, 500, 600], provider: 'google' },
            // monospace picker (8)
            { name: 'IBM Plex Mono',    weights: [400, 500],      provider: 'google' },
            { name: 'JetBrains Mono',   weights: [400, 500],      provider: 'google' },
            { name: 'Source Code Pro',  weights: [400, 500],      provider: 'google' },
            { name: 'Fira Code',        weights: [400, 500],      provider: 'google' },
            { name: 'Roboto Mono',      weights: [400, 500],      provider: 'google' },
            { name: 'Red Hat Mono',     weights: [400, 500],      provider: 'google' },
            { name: 'Spline Sans Mono', weights: [400, 500],      provider: 'google' },
            { name: 'Martian Mono',     weights: [400, 500],      provider: 'google' },
            // extra data-font candidates
            { name: 'DM Mono',          weights: [400, 500],      provider: 'google' },
            { name: 'IBM Plex Sans',    weights: [400, 500, 600], provider: 'google' },
          ],
        },
      ```

      (@nuxt/fonts emits `@font-face` for all; the browser only fetches the family
      the active CSS var actually uses, so eager registration is fine.)
  - **Why:** registering JetBrains Mono / DM Mono / etc. here is what lets the
    *exploration* selectors paint real candidate faces. Per §1 these are exploration
    only — the canonical product set is Fraunces · Inter · IBM Plex Mono.
- [x] **1.2** — `app/assets/css/main.css` — route fonts through overridable
      `*-stack` vars. Runtime overrides only work if the utility reads `var(...)`.
      Mirror how the color tokens work (`--color-primary: var(--primary)`).

      **Edit 1 — add two stack vars to the `:root` block** (put them right after the
      `--chart-5` line, before the closing `}` of `:root`):

      ```css
        /* font stacks — overridable at runtime (the mono + data picker write these) */
        --font-mono-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
        --font-data-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
      ```

      (`--font-data-stack` defaults to the **mono** stack — data-font OFF = one mono,
      per Q5. Sans/heading stay static, so they don't need stack vars.)

      **Edit 2 — in the `@theme inline` block, replace the comment + 3 font lines.**
      Find this exact 4-line block (the radius vars just below it stay intact):

      ```css
        /* 3-family font system (Q5) */
        --font-sans: "Inter", system-ui, sans-serif;
        --font-mono: "IBM Plex Mono", "JetBrains Mono", monospace;
        --font-heading: "Fraunces", "Times New Roman", serif;
      ```

      Replace it with these 5 lines (routes mono/data through the overridable vars):

      ```css
        /* 3-family system (Q5) + an overridable data slot (playground exploration) */
        --font-sans: "Inter", system-ui, sans-serif;
        --font-mono: var(--font-mono-stack);
        --font-data: var(--font-data-stack);
        --font-heading: "Fraunces", "Times New Roman", serif;
      ```

      This makes `.font-mono` → `font-family: var(--font-mono-stack)` and creates a
      new `.font-data` → `font-family: var(--font-data-stack)` utility, both
      runtime-overridable.
  - 💡 **Heuristic.** A runtime CSS-var override only renders if the utility reads
    `var(...)` — a literal value baked into `@theme inline` is frozen at build time.
    Mirror the working pattern (`--color-primary: var(--primary)`) before assuming a
    picker is "wired but flaky." *(ES: una sobre-escritura en tiempo de ejecución solo
    se ve si la utilidad lee `var(...)`; un valor literal en `@theme inline` queda
    congelado en build.)*

✅ **Done-when:**
- `pnpm dev` boots clean.
- In the browser console,
  `getComputedStyle(document.querySelector('.font-mono')).fontFamily` includes IBM
  Plex Mono; then
  `document.documentElement.style.setProperty('--font-mono-stack','"JetBrains Mono", monospace')`
  → the same query now reports JetBrains Mono (i.e. the override **renders**, unlike
  before).
- Deterministic fallback if the webfont hasn't painted yet:
  `getComputedStyle(document.documentElement).getPropertyValue('--font-mono-stack')`
  reflects the override (the var write is deterministic even pre-paint).
- Server stopped.
*(ES: arranca limpio; la sobre-escritura de `--font-mono-stack` ya se renderiza; el
valor de la variable refleja el override aun antes de pintar; servidor detenido.)*

🚦 **Checkpoint 1.** Show gczuluaga: the booted app and the two console reads (before
override = IBM Plex Mono, after override = JetBrains Mono). Questions:
1. Why did the v1 picker silently fail, and why does the `*-stack` indirection fix it
   when writing `--font-mono` directly did not? *(ES: ¿por qué fallaba el selector v1
   y por qué lo arregla la indirección `*-stack`?)*
2. Walk the `:root` / `@theme inline` edit live: point to where `.font-mono` now
   resolves to `var(--font-mono-stack)`. *(ES: muestra en vivo dónde `.font-mono`
   resuelve a `var(--font-mono-stack)`.)*

---

## Phase 2 — Store: richer fonts + data axis (`app/stores/playground.ts`)

> **Resumen (ES) — Fase 2: store.** Reescribe el store de Pinia: 8 monos, nuevo
> `DATA_FONTS`, estado `dataFontEnabled`/`dataFontId`, `apply()` escribe
> `--font-mono-stack` + `--font-data-stack` (no `--font-mono`/`--font-data`),
> persistencia de preferencias. `SUB_BRANDS` no cambia (ERP bloqueado; el resto son
> placeholders para @SKuger01). El estado de tema queda (el toggle de la topbar llama
> `toggleTheme`).
>
> En orden, las tareas:
>
> 1. **2.1** — Sobre-escribir `app/stores/playground.ts` con el contenido exacto.
>
> Decisión humana relacionada: los acentos no-ERP de `SUB_BRANDS` son TBD (@SKuger01).

🛑 **HUMAN DECISION — non-ERP sub-brand accents.** The `light/dark.accent` hexes for
`lis-clinico`, `lis-deport`, `admisiones`, and `crm` in `SUB_BRANDS` are
**placeholders only** — they are 🛑 OPEN (RFC 0008 Q1/Q6) and decided by @SKuger01 via
the brand playground. An agent must **not** treat them as final or invent new ones.
ERP · Timón (navy `#003A70` light / teal `#A0D1CA` dark) is the only LOCKED entry.
*(ES: los acentos no-ERP son placeholders; los decide @SKuger01; no los inventes.)*

- [x] **2.1** — Overwrite the file with **exactly** this. Changes vs v1: 8
      `MONO_FONTS`, new `DATA_FONTS`, `dataFontEnabled`/`dataFontId` state, `apply()`
      writes `--font-mono-stack` + `--font-data-stack` (NOT `--font-mono`/
      `--font-data`), light pref persistence.

      ```ts
      import { defineStore } from 'pinia'

      export interface SubBrand {
        id: string
        name: string
        light: { accent: string; foreground: string }
        dark: { accent: string; foreground: string }
        locked: boolean
      }

      // ERP name + accent LOCKED (RFC 0008 Q1/Q6). Rest are PLACEHOLDERS for SKuger.
      export const SUB_BRANDS: SubBrand[] = [
        { id: 'erp',         name: 'Pháros · Timón (ERP)',       light: { accent: '#003A70', foreground: '#ffffff' }, dark: { accent: '#A0D1CA', foreground: '#06121f' }, locked: true },
        { id: 'lis-clinico', name: 'LIS clínico — ? (LCH)',      light: { accent: '#782F40', foreground: '#ffffff' }, dark: { accent: '#d59aa8', foreground: '#2a0a12' }, locked: false },
        { id: 'lis-deport',  name: 'LIS deportivo — ? (Biuman)', light: { accent: '#326295', foreground: '#ffffff' }, dark: { accent: '#8fb3d9', foreground: '#06121f' }, locked: false },
        { id: 'admisiones',  name: 'Admisiones — ?',             light: { accent: '#1b6b5a', foreground: '#ffffff' }, dark: { accent: '#4cd1b0', foreground: '#06121f' }, locked: false },
        { id: 'crm',         name: 'CRM — ? (¿Gente?)',          light: { accent: '#7a5d00', foreground: '#ffffff' }, dark: { accent: '#e6c34d', foreground: '#2e2606' }, locked: false },
      ]

      // 8 monos verified on Google Fonts. Q5 default = IBM Plex Mono; the rest explore
      // the pick before final lock (the playground is the sanctioned validation surface).
      export const MONO_FONTS = [
        { id: 'ibm',       label: 'IBM Plex Mono (Q5 default)', stack: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'jetbrains', label: 'JetBrains Mono',             stack: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'source',    label: 'Source Code Pro',            stack: '"Source Code Pro", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'fira',      label: 'Fira Code',                  stack: '"Fira Code", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'roboto',    label: 'Roboto Mono',                stack: '"Roboto Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'redhat',    label: 'Red Hat Mono',               stack: '"Red Hat Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'spline',    label: 'Spline Sans Mono',           stack: '"Spline Sans Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'martian',   label: 'Martian Mono',               stack: '"Martian Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
      ]

      // Data-font candidates — only applied when dataFontEnabled. Brand book mandates
      // JetBrains Mono + tabular-nums for cifras (BRAND.md §4.4); Inter/Plex Sans are
      // the proportional-with-tabular-figures alternatives.
      export const DATA_FONTS = [
        { id: 'jetbrains', label: 'JetBrains Mono (brand book — exploración)', stack: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'ibm-mono',  label: 'IBM Plex Mono',               stack: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'dm-mono',   label: 'DM Mono',                     stack: '"DM Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
        { id: 'inter',     label: 'Inter (tabular)',             stack: '"Inter", system-ui, sans-serif' },
        { id: 'ibm-sans',  label: 'IBM Plex Sans (tabular)',     stack: '"IBM Plex Sans", system-ui, sans-serif' },
      ]

      const PREFS_KEY = 'pharos-pg-prefs'

      export const usePlayground = defineStore('playground', () => {
        const theme = ref<'light' | 'dark'>('light')
        const subBrandId = ref('erp')
        const customAccent = ref<string | null>(null)
        const monoId = ref('ibm')
        const dataFontEnabled = ref(false)
        const dataFontId = ref('jetbrains')

        const subBrand = computed(() => SUB_BRANDS.find(s => s.id === subBrandId.value) ?? SUB_BRANDS[0])

        function apply() {
          if (!import.meta.client) return
          const el = document.documentElement
          el.classList.toggle('dark', theme.value === 'dark')
          const tone = theme.value === 'dark' ? subBrand.value.dark : subBrand.value.light
          const accent = customAccent.value ?? tone.accent
          const fg = customAccent.value ? '#ffffff' : tone.foreground
          // brand accent -> --primary + ring + sidebar-primary + chart-1 (NOT shadcn --accent, NOT status)
          for (const v of ['--primary', '--ring', '--sidebar-primary', '--sidebar-ring', '--chart-1']) {
            el.style.setProperty(v, accent)
          }
          el.style.setProperty('--primary-foreground', fg)
          el.style.setProperty('--sidebar-primary-foreground', fg)
          // fonts — write the *-stack vars the utilities read (Phase 1 indirection)
          const mono = MONO_FONTS.find(m => m.id === monoId.value) ?? MONO_FONTS[0]
          el.style.setProperty('--font-mono-stack', mono.stack)
          const data = DATA_FONTS.find(d => d.id === dataFontId.value) ?? DATA_FONTS[0]
          // OFF => data cells fall back to the single mono (Q5 "one mono")
          el.style.setProperty('--font-data-stack', dataFontEnabled.value ? data.stack : mono.stack)
          // persist
          localStorage.setItem('pharos-pg-theme', theme.value)
          localStorage.setItem(PREFS_KEY, JSON.stringify({
            subBrandId: subBrandId.value,
            monoId: monoId.value,
            dataFontEnabled: dataFontEnabled.value,
            dataFontId: dataFontId.value,
          }))
        }

        function setSubBrand(id: string) { subBrandId.value = id; customAccent.value = null; apply() }
        function setCustomAccent(hex: string) { customAccent.value = hex; apply() }
        function clearCustomAccent() { customAccent.value = null; apply() }
        function toggleTheme() { theme.value = theme.value === 'dark' ? 'light' : 'dark'; apply() }
        function setMono(id: string) { monoId.value = id; apply() }
        function setDataFont(id: string) { dataFontId.value = id; apply() }
        function setDataFontEnabled(on: boolean) { dataFontEnabled.value = on; apply() }

        function init() {
          if (import.meta.client) {
            theme.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
            try {
              const p = JSON.parse(localStorage.getItem(PREFS_KEY) ?? '{}')
              if (p.subBrandId) subBrandId.value = p.subBrandId
              if (p.monoId) monoId.value = p.monoId
              if (typeof p.dataFontEnabled === 'boolean') dataFontEnabled.value = p.dataFontEnabled
              if (p.dataFontId) dataFontId.value = p.dataFontId
            } catch { /* ignore malformed prefs */ }
          }
          apply()
        }

        return {
          theme, subBrandId, customAccent, monoId, dataFontEnabled, dataFontId, subBrand,
          setSubBrand, setCustomAccent, clearCustomAccent, toggleTheme,
          setMono, setDataFont, setDataFontEnabled, init, apply,
        }
      })
      ```
  - **Why:** `apply()` writes the **`*-stack`** vars (Phase-1 indirection), never
    `--font-mono`/`--font-data` directly — those are frozen by `@theme inline`. The
    accent loop touches only `--primary`/`--ring`/`--sidebar-primary`/`--sidebar-ring`/
    `--chart-1`; it deliberately never touches the status palette or shadcn `--accent`.

✅ **Done-when:**
- `pnpm dev` still boots clean; optionally `pnpm exec nuxi typecheck` passes for the
  store (the `typescript` devDep is present).
- No visual change yet (no page imports the store until Phase 5 — a clean boot alone
  does **not** prove the store compiles; the real proof lands in Phase 5 when the
  panel imports `MONO_FONTS`/`DATA_FONTS`).
- Server stopped.
*(ES: arranca limpio; opcionalmente `nuxi typecheck`; aún sin cambio visual — la
prueba real llega en la Fase 5; servidor detenido.)*

---

## Phase 3 — Real Pháros logo (`public/logos/` + `AppLogo.vue`)

> **Resumen (ES) — Fase 3: logo Pháros real.** Copia los 4 SVG de marca a `public/`
> y crea `AppLogo.vue`, que intercambia claro/oscuro con CSS puro (clase `.dark`), sin
> JS. Los SVG ya traen el wordmark correcto + el punto piloto (rojo `#E4002B`, nunca
> recoloreado).
>
> En orden, las tareas:
>
> 1. **3.1** — Copiar los SVG de `brands/pharos_brand/` a `public/logos/`.
> 2. **3.2** — Crear `app/components/AppLogo.vue`.

- [x] **3.1** — Copy the brand SVGs into `public/`.

      ```bash
      cd /Users/gczuluaga/dev/pharos-playground
      mkdir -p public/logos
      cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-navbar-light.svg public/logos/
      cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-navbar-dark.svg  public/logos/
      cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-icon-light.svg   public/logos/
      cp /Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-icon-dark.svg    public/logos/
      ```
- [x] **3.2** — `app/components/AppLogo.vue` (new). Theme-swap with pure CSS (`.dark`
      class on `<html>`) — no JS, snapshot-safe. The light/dark SVGs already carry the
      correct (never-recolored) wordmark + pilot dot.

      ```vue
      <script setup lang="ts">
      withDefaults(defineProps<{ variant?: 'navbar' | 'icon' }>(), { variant: 'navbar' })
      </script>

      <template>
        <span class="inline-flex items-center" aria-label="Pháros">
          <img :src="`/logos/pharos-${variant}-light.svg`" alt="Pháros"
               class="block h-7 w-auto dark:hidden" />
          <img :src="`/logos/pharos-${variant}-dark.svg`" alt="Pháros"
               class="hidden h-7 w-auto dark:block" />
        </span>
      </template>
      ```
  - 💡 **Heuristic.** A pure-CSS `dark:hidden` / `dark:block` swap is snapshot-safe;
    a JS-driven swap can flash or desync from the FOUC guard. The pilot-light red is
    already baked into the SVGs — do not recolor it. *(ES: el intercambio por CSS es
    seguro para snapshots; no recolorees el rojo piloto.)*

✅ **Done-when:**
- `ls public/logos` shows 4 SVGs.
- The component compiles (it is used in Phase 4).
*(ES: `public/logos` tiene 4 SVG; el componente compila — se usa en la Fase 4.)*

---

## Phase 4 — Layout: finance-lch topbar + resizable Marca grid (`app/layouts/default.vue`)

> **Resumen (ES) — Fase 4: layout (primera UI real).** Reescribe el layout: conserva
> el `Sidebar collapsible="icon"` de shadcn, restiliza la topbar al patrón de
> finance-lch (logo + divisor + breadcrumb con popover + cluster derecho con toggle de
> tema) sobre el sustrato `.dark`/tokens shadcn, y aloja el `<PlaygroundPanel>` (ahora
> en bloque) en una grilla de 3 pistas (`preview | resizer | panel`) con
> redimensionador arrastrable y ancho persistido. La región de preview es un `<div>`
> (NO `<main>` — `SidebarInset` ya es `<main>`; no anidar).
>
> En orden, las tareas:
>
> 1. **4.1** — Sobre-escribir `app/layouts/default.vue` con el contenido exacto.

- [x] **4.1** — Overwrite with **exactly** this. It keeps the shadcn `Sidebar
      collapsible="icon"`, restyles the topbar to finance-lch's pattern (logo +
      divider + popover breadcrumb + right cluster with theme toggle), and hosts the
      now-block `<PlaygroundPanel>` in a 3-track grid (`preview | resizer | panel`)
      with a draggable resizer + persisted width. The preview region is a `<div>`
      (NOT `<main>` — `SidebarInset` is already a `<main>`; do not nest).

      ```vue
      <script setup lang="ts">
      import { Sun, Moon, LayoutGrid, BarChart3, ChevronDown } from 'lucide-vue-next'
      import AppLogo from '~/components/AppLogo.vue'
      import PlaygroundPanel from '~/components/PlaygroundPanel.vue'
      import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'

      const route = useRoute()
      const pg = usePlayground()

      const nav = [
        { label: 'Componentes', to: '/', icon: LayoutGrid },
        { label: 'Gráficas', to: '/graficas', icon: BarChart3 },
      ]
      const crumbLeaf = computed(() => nav.find(n => n.to === route.path)?.label ?? 'Componentes')

      // ── resizable Marca panel (finance-lch Factura/Causación pattern) ──
      const PANEL_KEY = 'pharos-pg-panel-pct'
      const DEFAULT_PCT = 26
      const panelPct = ref(DEFAULT_PCT)
      const gridRef = ref<HTMLElement | null>(null)
      let dragging = false

      function onMove(e: PointerEvent) {
        if (!dragging || !gridRef.value) return
        const r = gridRef.value.getBoundingClientRect()
        // panel is on the RIGHT: its width % = (right edge - cursor) / total width
        panelPct.value = Math.min(50, Math.max(18, ((r.right - e.clientX) / r.width) * 100))
      }
      function endResize() {
        if (!dragging) return
        dragging = false
        window.removeEventListener('pointermove', onMove)
        window.removeEventListener('pointerup', endResize)
        localStorage.setItem(PANEL_KEY, String(Math.round(panelPct.value)))
      }
      function startResize(e: PointerEvent) {
        dragging = true
        ;(e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId)
        window.addEventListener('pointermove', onMove)
        window.addEventListener('pointerup', endResize)
      }
      function resetPanel() {
        panelPct.value = DEFAULT_PCT
        localStorage.setItem(PANEL_KEY, String(DEFAULT_PCT))
      }

      onMounted(() => {
        pg.init()
        const saved = Number(localStorage.getItem(PANEL_KEY))
        if (saved >= 18 && saved <= 50) panelPct.value = saved
      })
      </script>

      <template>
        <SidebarProvider>
          <Sidebar collapsible="icon">
            <SidebarHeader class="h-14 justify-center px-3">
              <AppLogo variant="icon" />
            </SidebarHeader>
            <SidebarContent>
              <SidebarGroup>
                <SidebarGroupLabel>Diseño</SidebarGroupLabel>
                <SidebarGroupContent>
                  <SidebarMenu>
                    <SidebarMenuItem v-for="item in nav" :key="item.to">
                      <SidebarMenuButton :is-active="route.path === item.to" as-child>
                        <NuxtLink :to="item.to">
                          <component :is="item.icon" />
                          <span>{{ item.label }}</span>
                        </NuxtLink>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  </SidebarMenu>
                </SidebarGroupContent>
              </SidebarGroup>
            </SidebarContent>
          </Sidebar>

          <SidebarInset class="flex h-svh flex-col overflow-hidden">
            <!-- topbar: finance-lch pattern on the .dark/shadcn substrate -->
            <header class="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-card px-4">
              <SidebarTrigger />
              <span class="h-5 w-px shrink-0 bg-border" />
              <AppLogo class="hidden md:inline-flex" />
              <span class="hidden h-5 w-px shrink-0 bg-border md:block" />
              <nav aria-label="Breadcrumb" class="text-sm">
                <ol class="flex items-center gap-1.5">
                  <li>
                    <Popover>
                      <PopoverTrigger class="inline-flex items-center gap-1 text-muted-foreground transition-colors hover:text-foreground">
                        Diseño
                        <ChevronDown class="size-3.5" />
                      </PopoverTrigger>
                      <PopoverContent align="start" :side-offset="6" class="w-56 p-1.5">
                        <NuxtLink v-for="item in nav" :key="item.to" :to="item.to"
                          class="block rounded-md px-2 py-1.5 text-sm transition-colors hover:bg-accent"
                          :class="route.path === item.to ? 'font-semibold text-foreground' : 'text-muted-foreground'">
                          {{ item.label }}
                        </NuxtLink>
                      </PopoverContent>
                    </Popover>
                  </li>
                  <li aria-hidden="true"><span class="text-muted-foreground">/</span></li>
                  <li><span class="font-semibold text-foreground" aria-current="page">{{ crumbLeaf }}</span></li>
                </ol>
              </nav>
              <div class="ml-auto flex items-center gap-3">
                <span class="hidden whitespace-nowrap text-sm text-muted-foreground lg:inline">Laboratorio Clínico Hematológico</span>
                <span class="hidden h-5 w-px shrink-0 bg-border lg:block" />
                <button type="button" aria-label="Cambiar tema"
                  class="inline-flex size-9 items-center justify-center rounded-full border border-border bg-muted text-foreground transition-colors hover:bg-accent"
                  @click="pg.toggleTheme()">
                  <Moon v-if="pg.theme === 'light'" class="size-[18px]" />
                  <Sun v-else class="size-[18px]" />
                </button>
              </div>
            </header>

            <!-- content: preview | draggable resizer | fixed Marca panel -->
            <div ref="gridRef" class="grid min-h-0 flex-1 overflow-hidden"
              :style="`grid-template-columns: minmax(0,1fr) 6px ${panelPct}%`">
              <div class="min-w-0 overflow-y-auto p-6">
                <NuxtPage />
              </div>
              <div role="separator" aria-orientation="vertical" aria-label="Redimensionar panel"
                class="relative cursor-col-resize touch-none select-none bg-border transition-colors hover:bg-primary"
                @pointerdown="startResize" @dblclick="resetPanel">
                <span class="pointer-events-none absolute left-1/2 top-1/2 h-7 w-0.5 -translate-x-1/2 -translate-y-1/2 rounded bg-muted-foreground/40" />
              </div>
              <PlaygroundPanel class="min-w-0 overflow-y-auto border-l border-border bg-card" />
            </div>
          </SidebarInset>
        </SidebarProvider>
      </template>
      ```

      > Note: `app/app.vue` stays `<template><NuxtLayout><NuxtPage /></NuxtLayout></template>`.
      > The theme toggle now lives in the topbar (finance-lch faithful); it is removed
      > from the panel in Phase 5. The playground still live-switches theme (Q5
      > satisfied). The explicit `Popover` import is intentional and harmless (Nuxt
      > auto-import would also resolve it); do NOT "fix" the apparent inconsistency by
      > importing the other `ui/*` components — `Sidebar*`, `SidebarTrigger`, etc. all
      > resolve via auto-import.
  - **Why:** the resizer math reads from the **right** edge (`(r.right - e.clientX) /
    r.width`) because the panel is pinned right; clamped to 18–50%. We adopt
    finance-lch's *look/structure only* — never its `[data-theme]`/cobol/`--nav-*`
    (see §1).

✅ **Done-when:**
- Boots.
- Topbar shows the Pháros logo + "Diseño ▾ / Componentes" breadcrumb (the "Diseño"
  chip opens a popover listing both pages) + a round theme toggle on the right.
- The Marca panel sits pinned on the right; dragging the 6px divider resizes it and
  the width survives reload; double-click resets to 26%.
*(ES: arranca; topbar con logo + breadcrumb con popover + toggle redondo; el panel
fijo a la derecha se redimensiona, persiste al recargar y vuelve a 26% con doble
clic.)*

🚦 **Checkpoint 2.** (First real UI.) Show gczuluaga, live in the browser: the
restyled topbar, the popover breadcrumb opening, the theme toggle flipping
light↔dark, and the resizer dragging + surviving a reload + double-click reset.
Questions:
1. Why is the preview region a `<div>` and not a `<main>`, and what breaks if you
   nest a second `<main>` inside `SidebarInset`? *(ES: ¿por qué la preview es `<div>`
   y no `<main>`?)*
2. Walk the resizer math live: why does the panel width read from `r.right`, not
   `r.left`, and where is the width persisted/clamped? *(ES: recorre la matemática del
   redimensionador — por qué `r.right` y dónde se persiste/limita.)*

---

## Phase 5 — Marca panel as a fixed block (`app/components/PlaygroundPanel.vue`)

> **Resumen (ES) — Fase 5: panel "Marca" como bloque fijo.** Reescribe el panel: ya
> no es `Sheet`/trigger superpuesto, es un `<aside>` que el layout monta en línea.
> Quita el control de tema (ahora en la topbar). Agrega el selector de mono (8), el
> interruptor + selector de fuente de datos, y conserva sub-marca + acento
> personalizado + la nota Q4 (estado independiente del acento). Los `ui/*` son
> auto-importados por Nuxt; solo se importa el store.
>
> En orden, las tareas:
>
> 1. **5.1** — Sobre-escribir `app/components/PlaygroundPanel.vue` con el contenido exacto.

- [x] **5.1** — Overwrite with **exactly** this. No more `Sheet`/trigger — it's a
      plain `<aside>` the layout mounts inline. Theme control removed (now in topbar).
      Adds the **mono picker (8)**, the **data-font toggle + picker**, keeps
      sub-brand + custom accent + the Q4 status note. shadcn `ui/*` components are
      Nuxt auto-imported (no import needed); only the store is imported.

      ```vue
      <script setup lang="ts">
      import { SUB_BRANDS, MONO_FONTS, DATA_FONTS, usePlayground } from '~/stores/playground'
      const pg = usePlayground()
      </script>

      <template>
        <aside class="flex h-full flex-col gap-5 p-4">
          <header>
            <h2 class="font-heading text-base font-medium">Control de marca</h2>
            <p class="text-xs text-muted-foreground">Explora el sistema de diseño Pháros</p>
          </header>

          <!-- Sub-marca -->
          <section>
            <Label class="mb-2 block text-xs font-medium uppercase tracking-wide text-muted-foreground">Sub-marca</Label>
            <div class="flex flex-col gap-1.5">
              <button v-for="brand in SUB_BRANDS" :key="brand.id" type="button"
                class="flex items-center justify-between gap-2 rounded-md border px-3 py-2 text-left text-sm transition-colors hover:bg-accent"
                :class="pg.subBrandId === brand.id ? 'border-primary ring-1 ring-primary' : 'border-border'"
                @click="pg.setSubBrand(brand.id)">
                <span>{{ brand.name }}</span>
                <Badge :variant="brand.locked ? 'default' : 'secondary'" class="shrink-0 text-xs">
                  {{ brand.locked ? 'decidida' : 'propuesta' }}
                </Badge>
              </button>
            </div>
          </section>

          <Separator />

          <!-- Acento personalizado -->
          <section>
            <Label class="mb-2 block text-xs font-medium uppercase tracking-wide text-muted-foreground">Acento personalizado</Label>
            <div class="flex items-center gap-2">
              <input type="color"
                :value="pg.customAccent ?? (pg.theme === 'dark' ? pg.subBrand.dark.accent : pg.subBrand.light.accent)"
                class="h-8 w-10 cursor-pointer rounded border border-border bg-transparent"
                @input="pg.setCustomAccent(($event.target as HTMLInputElement).value)" />
              <Button variant="ghost" size="sm" @click="pg.clearCustomAccent()">Limpiar</Button>
            </div>
          </section>

          <Separator />

          <!-- Fuentes -->
          <section class="flex flex-col gap-3">
            <Label class="block text-xs font-medium uppercase tracking-wide text-muted-foreground">Fuentes</Label>

            <div class="flex flex-col gap-1.5">
              <Label class="text-xs text-muted-foreground">Mono</Label>
              <Select :model-value="pg.monoId" @update:model-value="pg.setMono($event as string)">
                <SelectTrigger class="w-full"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="f in MONO_FONTS" :key="f.id" :value="f.id">{{ f.label }}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div class="flex items-center justify-between gap-2 rounded-md border border-border px-3 py-2">
              <Label for="data-toggle" class="text-sm font-normal">Fuente de datos aparte</Label>
              <Switch id="data-toggle" :model-value="pg.dataFontEnabled"
                @update:model-value="pg.setDataFontEnabled($event)" />
            </div>

            <div class="flex flex-col gap-1.5" :class="pg.dataFontEnabled ? '' : 'pointer-events-none opacity-50'">
              <Label class="text-xs text-muted-foreground">Datos (cifras)</Label>
              <Select :model-value="pg.dataFontId" @update:model-value="pg.setDataFont($event as string)">
                <SelectTrigger class="w-full" :disabled="!pg.dataFontEnabled"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="f in DATA_FONTS" :key="f.id" :value="f.id">{{ f.label }}</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <p class="text-xs leading-relaxed text-muted-foreground">
              Apagado = un solo mono (RFC 0008 Q5). Encendido = fuente de datos aparte con
              <span class="font-data tabular-nums slashed-zero">tabular-nums</span> y cero con barra,
              como el brand book (JetBrains Mono para cifras).
            </p>
          </section>

          <Separator />

          <p class="text-xs leading-relaxed text-muted-foreground">
            Los colores de estado (éxito/alerta/error/info) <strong>NO cambian</strong> al
            cambiar el acento — son independientes de la marca (RFC 0008 Q4).
          </p>
        </aside>
      </template>
      ```

      > reka-ui 2.9.6 `Switch` uses `modelValue` / `update:modelValue` (verified
      > against `SwitchRootProps`) — the `:model-value`/`@update:model-value` binding
      > above is correct. Do NOT switch to `:checked`/`@update:checked`: that is not a
      > valid prop on this version and would silently fail to bind (the toggle renders
      > but never updates the store).
  - 💡 **Heuristic.** When a control "renders but does nothing," check the
    library's actual prop name for that version before reworking your wiring — reka-ui
    2.9.6 `Switch` is `modelValue`, not `checked`. A wrong-but-plausible prop binds to
    nothing and fails silently. *(ES: si un control "se ve pero no hace nada", revisa
    el nombre real del prop para esa versión antes de reescribir el cableado.)*

✅ **Done-when:**
- Panel renders inline (no overlay/backdrop).
- Switching **Mono** visibly changes the typography + table cifras (the Phase-1 fix
  made this real).
- Toggling **Fuente de datos aparte** ON enables the data Select and re-renders the
  cifras in the data font; OFF returns them to the mono.
- Sub-brand + accent + Limpiar behave as before.
- Status pills do NOT move on accent change.
*(ES: panel en línea, sin overlay; el mono cambia la tipografía y las cifras; el
toggle de datos habilita su Select y re-renderiza las cifras; las pastillas de estado
no se mueven al cambiar el acento.)*

🚦 **Checkpoint 3.** (Core loop — the live re-theme.) Show gczuluaga, live: switching
Mono changes both the sample and the table cifras; toggling the data font ON/OFF;
changing the accent and confirming the status pills stay put. Questions:
1. Why does flipping the accent leave the status palette unchanged — where in the
   store is that boundary enforced? *(ES: ¿por qué el acento no mueve la paleta de
   estado y dónde se hace cumplir eso en el store?)*
2. Walk a Mono switch end-to-end: store → `--font-mono-stack` → `.font-mono`/`.font-data`
   utility → painted cifras. *(ES: recorre un cambio de mono de extremo a extremo.)*

---

## Phase 6 — Gallery: route cifras through the data font (`app/pages/index.vue`)

> **Resumen (ES) — Fase 6: galería.** Dos ediciones pequeñas para que el eje de
> fuente de datos sea visible donde viven los números: la celda numérica de la tabla
> financiera y la tarjeta de tipografía (una línea mono + una línea de datos). Deja
> las muestras de Fraunces e Inter como están.
>
> En orden, las tareas:
>
> 1. **6.1** — Editar la celda numérica de la tabla (reemplazo de SUBcadena).
> 2. **6.2** — Reemplazar la muestra de tipografía mono por una línea mono + una de datos.

- [x] **6.1** — Tabla financiera numeric cell. A **SUBSTRING** replace only — the
      find-text is part of a longer `<TableCell>` line that also carries a
      `:class="row.monto < 0 ? 'text-status-error' : ''"` color binding; do NOT touch
      that binding.

      - find: `class="text-right font-mono tabular-nums"`
      - replace: `class="text-right font-data tabular-nums slashed-zero lining-nums"`
- [x] **6.2** — Tipografía card. Replace the single mono sample `<p>` (the only
      `<p class="font-mono` in the file) with a mono line **and** a data line so both
      faces are visible.

      - find (verbatim, including the 8 leading spaces):

      ```vue
              <p class="font-mono text-sm tabular-nums">IBM Plex Mono · 0123456789 · $1.234.567 · ─── monoespaciado</p>
      ```

      - replace with:

      ```vue
              <p class="font-mono text-sm">Mono · IBM Plex Mono · etiquetas · ABCDEF · {} [] =&gt;</p>
              <p class="font-data tabular-nums slashed-zero lining-nums text-sm">Datos · 0123456789 · $1.234.567 · 0 con barra (cero/letra O)</p>
      ```

      (Leave the Fraunces `font-heading` and Inter `font-sans` sample lines as they
      are.)
  - **Why:** routing the numeric cell + the data sample line through `.font-data`
    (not `.font-mono`) is what makes the OFF=one-mono / ON=separate-data-font axis
    actually visible. With the toggle OFF both faces resolve to the same mono.

✅ **Done-when:**
- The table's Monto column and the new "Datos" line change font when the data
  toggle/picker change.
- With the toggle OFF they match the selected mono.
*(ES: la columna Monto y la línea "Datos" cambian con el toggle/selector de datos; con
el toggle apagado coinciden con el mono elegido.)*

---

## §9 — Run & acceptance checklist · Ejecución y checklist de aceptación

> **Resumen (ES) — §9.** Arranca la app, recórrela y confirma TODO el checklist.
> Captura las 5 capturas de evidencia. §9a fija el guard de determinismo de snapshots
> (Q9): siempre desde un estado neutralizado, nunca el último que dejó un humano.

```bash
cd /Users/gczuluaga/dev/pharos-playground && pnpm dev   # http://localhost:3000
```

✅ **Done-when (acceptance).** Drive the page and confirm ALL of:

- [ ] **Topbar (finance-lch look):** Pháros **logo SVG** (swaps light/dark with the
      theme) + vertical divider + **"Diseño ▾ / Componentes"** breadcrumb where the
      "Diseño" chip opens a **popover** listing both pages; right side shows the org
      name + a round **theme toggle**. **No page `<h1>`.**
- [ ] **Sidebar** is still the shadcn `Sidebar collapsible="icon"`; the topbar
      `SidebarTrigger` collapses it to the icon rail and back.
- [ ] **Marca panel is fixed in-view on the right** (no overlay/backdrop), pinned
      full-height with its own scroll; **dragging the 6px divider resizes it**, width
      **persists across reload**, double-click resets to 26%.
- [ ] **Theme toggle** (topbar) flips the whole UI light ↔ dark (`.dark` on `<html>`),
      no FOUC on reload. **No cobol option anywhere.**
- [ ] **Sub-brand switch** recolors buttons, sidebar active state, focus ring, and
      chart series 1 (`--primary` propagates); **status pills do NOT move** (Q4).
- [ ] **Custom accent** live-retints; "Limpiar" restores the preset.
- [ ] **Mono picker (8 families)** visibly changes the typography sample AND the table
      cifras — i.e. the Phase-1 indirection works (this was broken in v1).
- [ ] **Data-font toggle:** OFF → cifras use the selected mono (one mono, Q5); ON →
      cifras switch to the chosen data font (default JetBrains Mono) with
      `tabular-nums`/`slashed-zero`. The data Select is disabled while OFF.
- [ ] **Charts** (`/graficas`) render and recolor on accent change; breadcrumb leaf
      reads "Gráficas".
- [ ] No console errors; **`pnpm build` succeeds** (SSR-safe — charts stay
      `.client`/`ClientOnly`; the resizer + font logic are client-guarded).

Capture screenshots as evidence: (1) light + ERP, (2) dark + ERP, (3) light + a
placeholder sub-brand, (4) data-font toggle ON showing JetBrains cifras vs OFF, (5)
the panel resized narrow + wide.

🚦 **Checkpoint 4.** (Exit.) Walk the full acceptance checklist with gczuluaga and
present the 5 screenshots. This checkpoint's Done-when **blocks archiving the plan**
until Checkpoints 1–3 have each been walked. Questions:
1. Which of the locked invariants (§1) would have been easiest to drift, and what in
   the plan prevented it? *(ES: ¿cuál invariante era el más fácil de violar y qué lo
   evitó?)*
2. Walk one screenshot pair (data-font ON vs OFF) and explain what a viewer is meant
   to conclude about the brand-book "JetBrains-for-data" question. *(ES: explica con
   el par de capturas qué debe concluir el lector sobre la pregunta del brand book.)*

### §9a — Q9 snapshot determinism (required guard)

RFC 0008 Q9 wants Playwright visual-regression snapshots of this playground across
themes/accents. The resizable panel and the persisted prefs make state sticky, so
snapshots MUST run from a neutralized state — never whatever a human last left:

- Before each snapshot, seed/clear localStorage so the panel + brand are at canonical
  defaults, e.g. a Playwright `addInitScript`:

  ```js
  await page.addInitScript(() => {
    localStorage.removeItem('pharos-pg-panel-pct')    // -> DEFAULT_PCT (26)
    localStorage.removeItem('pharos-pg-prefs')        // -> ERP / IBM Plex Mono / data-font OFF
    localStorage.setItem('pharos-pg-theme', 'light')  // set explicitly per snapshot variant
  })
  ```

- The panel's **default width (26%) is the canonical snapshot width**; dragging the
  resizer is a manual-exploration affordance only and is NOT part of the snapshot
  matrix. Mono/data-font/accent are likewise set explicitly per snapshot variant,
  never inherited from a prior session. This keeps the fixed panel deterministic
  across themes/accents per Q9.

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions logged below for
> traceability.

**Open:**

- 🛑 **Non-ERP sub-brand accents** — `lis-clinico` / `lis-deport` / `admisiones` /
  `crm` (and `archivo`) accents are placeholders in `SUB_BRANDS`. Pending: @SKuger01
  decides via the brand playground (RFC 0008 Q1/Q6). Each = ONE accent overriding
  `--primary`/`--accent`/`--ring`/`--sidebar-primary` only; the status palette + mark
  constants stay fixed. **Never invent them.**
- 🛑 **Brand-book "data font" vs the one-mono lock** — the brand-book JetBrains-for-data
  split and the canonical 3-family lock (IBM Plex Mono for data + labels; JetBrains
  Mono NOT in product UI) conflict. This plan does **not** resolve it — it makes the
  playground show both so @SKuger01 can decide. Default stays one mono (IBM Plex
  Mono), data-font toggle OFF.

**Resolved during planning / by canonical decisions (2026-06-15):**

- **Design-system tenancy + naming** — Pháros is the umbrella product design system;
  LCH & Biuman are tenants; a tenant never prefixes an app name (`Pháros · Timón`).
  Maker credit = *Interval · The Human Tech Co.* (footer only).
- **Token contract source of truth** — the registry at
  `/Users/gczuluaga/dev/.github/brands/pharos_brand/registry/`, contract file
  `registry/tokens.css` (shadcn-vue vars + accent-independent `--success`/`--warning`/
  `--error`/`--info`). Legacy names collapse: `--text-secondary`/`--text-muted` →
  `--muted-foreground`; `--text-brand` → `--primary`; `--nav-*` → `--sidebar-*`.
- **Status palette naming reconciliation** — the canonical status tokens are
  `--success`/`--warning`/`--error`/`--info` (+ foregrounds). This plan's embedded
  code (built earlier) uses `--status-*`/`text-status-error`; that is the playground's
  historical naming and is **not** rewritten in the archived code, only logged here so
  a reader maps it to the canonical contract.
- **Fonts** — Fraunces (display/wordmark) · Inter (sans UI) · IBM Plex Mono (data +
  labels). JetBrains Mono and Apax are NOT used in product UI (Apax stays an LCH
  brand-identity asset only). The richer mono set + data-font toggle here are
  exploration; the default state is the canonical 3-family lock.
- **Theming** — shadcn `.dark` class, light + dark only. No cobol/CRT theme. No
  `[data-theme]`. *(2026-06-13.)*
- **Accent overrides** — a sub-brand overrides ONLY `--primary`/`--accent`/`--ring`/
  `--sidebar-primary`. ERP · Timón = LCH Navy `#003A70` (+ teal `#A0D1CA` success) —
  LOCKED. *(RFC 0008 Q1/Q6.)*
- **Distribution** — copy-in via `scripts/sync-pharos-registry.sh`, NOT an npm package
  (RFC 0008 Q3).
- **Merge mode** — merge-commit everywhere; squash disabled org-wide. *(2026-06-15.)*
- **Commit/branch type vocabulary** — the canonical set is `feat`, `fix`, `refactor`,
  `test`, `chore`, `docs`, `hotfix`, `ci` (`ci` added org-wide; `hotfix` valid as both
  a branch type and a commit type). *(2026-06-15.)*
- **Plan superseded** — all phases, fixes (T4/T5/T6/T7), and the §9 acceptance
  checklist merged into `brand-playground-build-plan.md` (Phases 10–15 and §13–15);
  this file is archived and not run. *(2026-06-14.)*

## Risks · Riesgos

> **Resumen (ES).** Qué puede salir mal y dónde mitigarlo: el bug del selector de
> fuentes (Fase 1), el binding equivocado del `Switch` (Fase 5), drift hacia
> `[data-theme]`/cobol/`--nav-*` (§1), inventar acentos no-ERP, y snapshots no
> deterministas por estado pegajoso (§9a).

- **Font picker silently a no-op** → a "wired" picker that never re-renders. **Mitigation:**
  Phase 1's `*-stack` indirection + the Done-when console read that proves the
  override renders before building any picker UI.
- **`Switch` bound with the wrong prop** → the toggle renders but never updates the
  store. **Mitigation:** Phase 5 pins `:model-value`/`@update:model-value` for
  reka-ui 2.9.6 and forbids `:checked`/`@update:checked`.
- **Drift toward finance-lch's `[data-theme]`/cobol/`--nav-*`** → violates the locked
  substrate. **Mitigation:** §1 invariants + the Phase 4 note adopting *look/structure
  only*; Checkpoint 4 question 1 audits it.
- **Inventing non-ERP accents** → ships unsanctioned brand colours. **Mitigation:**
  the 🛑 in Phase 2 + the Open decision; placeholders are visibly badged "propuesta."
- **Non-deterministic Playwright snapshots** → flaky visual regression from sticky
  panel width / persisted prefs. **Mitigation:** §9a's `addInitScript` neutraliser +
  the canonical 26% snapshot width.
- **Embedded `--status-*` naming mistaken for the contract** → a reader copies the old
  token names into a real surface. **Mitigation:** the Decisions reconciliation entry
  maps `--status-*` → the canonical status palette; the registry `tokens.css` is the
  source of truth.

## References

- `plans/brand-playground-build-plan.md` — the merged build plan that supersedes this
  file (Phases 10–15, §13–15). **Run that, not this.**
- `brands/pharos_brand/registry/tokens.css` — the token contract (source of truth).
- `brands/pharos_brand/registry/` — registry root (README, frontend-standards,
  surfaces).
- `scripts/sync-pharos-registry.sh` — copy-in distribution (RFC 0008 Q3).
- `brands/pharos_brand/BRAND.md` — brand book (mark constants, data-font split).
- RFC 0008 (Pháros design system + co-creation) — Q1/Q4/Q5/Q6/Q7/Q9/Q11.
- finance-lch — `FacturaDrawerPanel` / `CausacionPanel` (the resizable-panel pattern);
  topbar look reference. lab-qc — the shadcn `Sidebar collapsible="icon"` shell
  reference.
- `templates/plan-template.md` — the canonical plan shape this file conforms to.
