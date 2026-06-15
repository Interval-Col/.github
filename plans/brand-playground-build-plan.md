---
status: active
created: 2026-06-13
updated: 2026-06-15
owner: gczuluaga
implementation: TBD
language: English body; Spanish "Resumen" + decision/criteria glosses.
tracking-issue: Interval-Col/.github#27
relates-to: RFC 0008 Q4/Q5/Q6/Q7/Q9/Q11
supersedes: brand-playground-tweaks-plan.md (merged here; that file is now archived)
---

# Pháros brand playground — complete build plan (v1 + v2 tweaks) · Playground de marca Pháros

> **Resumen (ES).** Una app **Nuxt 4 solo-local** que renderiza el app-shell
> compartido de Pháros + una galería de componentes + gráficas de ejemplo, con
> un **panel de control fijo a la derecha** que cambia en vivo
> **acento (por sub-marca) · tema (claro/oscuro) · fuente mono · fuente de
> datos**. Sirve para *ver* el sistema de diseño re-tematizarse antes de cerrar
> las decisiones de marca abiertas. Pháros es el sistema de diseño paraguas;
> LCH y Biuman son **tenants**. La fuente de la verdad es el registry en
> `/Users/gczuluaga/dev/.github/brands/pharos_brand/registry/` (contrato de
> tokens = `registry/tokens.css`). **Estado actual: la app ya está construida y
> todas las fases están completas.**

A **local-only Nuxt 4 app** that renders the shared Pháros app-shell + a component
gallery + sample charts, with a **fixed right-side control panel** that live-switches
**accent (per sub-brand) · theme (light/dark) · mono font (8 families) · data font
(off/on)** — so the team can *see* the design system re-theme before locking the open
brand decisions. The **code-first validation surface** RFC 0008 implies for Q5 (mono
pick), Q6 (accent candidates), Q7 (themes), Q11 (charts), and the brand-book
data-font split.

---

## How to use this plan · Cómo usar este plan

**EN.** This plan is written to be executed with AI-agent assistance —
that is expected and encouraged. The plan, not the agent, makes the
technical decisions. Your job has three parts: **execute** the tasks,
**verify** each one against its Done-when list, and **escalate** the
decisions the plan marks for a human.

Read each task fully — including its **Why** and **Done-when** — *before*
you start it. A task is not finished because an agent said so; it is
finished when every Done-when line is literally true and you have
checked it yourself.

If a task or its **Why** doesn't make sense, that is a gap in *this
plan*, not a failing in you — stop and ask gczuluaga. A question costs
minutes; a misunderstanding shipped costs days.

**If the English here slows you down:** every section opens with a
Spanish **Resumen**, and your AI agent will translate or explain any
part of this plan in Spanish if you ask it — that is a completely
legitimate thing to do. Don't let the language be the reason a task
stalls.

**ES.** Este plan está escrito para ejecutarse con ayuda de agentes de
IA — eso se espera y se fomenta. Las decisiones técnicas las toma el
plan, no el agente. Tu trabajo tiene tres partes: **ejecutar** las
tareas, **verificar** cada una contra su lista *Done-when*, y **escalar**
las decisiones que el plan marca para un humano.

Lee cada tarea completa — incluyendo su **Why** y su **Done-when** —
*antes* de empezarla. Una tarea no está terminada porque un agente lo
diga; está terminada cuando cada línea *Done-when* es literalmente cierta
y tú mismo la verificaste.

Si una tarea o su **Why** no te quedan claras, eso es un vacío de *este
plan*, no una falla tuya — pregúntale a gczuluaga. Y si el inglés te
frena: cada sección tiene un **Resumen** en español, y tu agente de IA
te traduce o explica cualquier parte en español si se lo pides — hazlo
sin problema.

> **How to auto-run with a coding agent.** Open a Claude session and paste:
>
> > Execute the plan at `/Users/gczuluaga/dev/.github/plans/brand-playground-build-plan.md`
> > exactly, phase by phase. Build at `/Users/gczuluaga/dev/pharos-playground/`.
> > After each phase run its verification. At the end run `pnpm dev` and confirm the
> > acceptance checklist. Do not deviate from the embedded file contents — they
> > encode locked RFC 0008 decisions. Don't push.
>
> **Current state (2026-06-15).** The app is built and all phases below are
> complete. Phases 0–9 produced v1; Phases 10–15 + bug-fixes produced the
> current v2 state. A fresh run from Phase 0 reproduces the current app.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| 💡 **Heuristic** | A short engineering or working lesson. Worth 30 seconds. *(ES: heurística — lección breve.)* |
| 🛑 **HUMAN DECISION** | A choice the plan deliberately does not make. **Do not let an agent pick it.** Escalate to gczuluaga. *(ES: decisión humana — no la toma un agente; escala a gczuluaga.)* |
| ✅ **Done-when** | The Definition of Done. The phase is verified only when every line is literally true. *(ES: terminado-cuando — definición de "hecho".)* |
| 🚦 **Checkpoint** | Stop. Show gczuluaga the named evidence and answer the questions before continuing. **Mandatory stop — including in auto mode** (see Working rules). *(ES: punto de control — alto obligatorio, también en modo auto.)* |

> **On the checkpoints.** Each 🚦 lists evidence to show and questions to
> answer. The questions are **not a test of you** — they test whether
> the plan explained things well enough. gczuluaga may also ask any of
> them at any time. *(ES: las preguntas del checkpoint no son un examen
> tuyo — prueban si el plan explicó bien; gczuluaga puede preguntarlas en
> cualquier momento.)*

## Working rules · Reglas de trabajo

These apply to every phase.

- **Commit and push after every slice.** When a task group or a phase is
  done and its Done-when checks pass, commit and push to GitHub
  **immediately**. Work that lives only on your laptop cannot be seen,
  reviewed, helped with, or recovered. *(ES: haz commit y push a GitHub
  apenas termines — el trabajo que solo vive en tu laptop no existe para
  el equipo.)*
- **Merge mode — merge-commit everywhere.** PRs are integrated with a
  **merge commit**; squash merging is **disabled** ("Allow squash merging"
  off). *(ES: el modo de integración es merge-commit en todos los repos;
  el squash está deshabilitado.)*
- **Commit messages — Conventional Commits, scope required.**
  `type(scope): description` — e.g. `feat(playground): add mono font picker`.
  `type` ∈ `feat | fix | refactor | test | chore | docs | hotfix | ci`. The
  `(scope)` is **mandatory**. Branch names mirror it:
  `type/scope-short-description` (`hotfix` is valid as both a branch type and a
  commit type; `ci` was added org-wide). *(ES: Conventional Commits; el
  `(scope)` es obligatorio; la rama refleja el commit.)*
- **Review the frontend yourself, in the browser.** A phase that touches
  the UI is **not verified** because the backend endpoint returned `200`
  — it is verified when you have opened the app, clicked through what
  you built, and seen it work the way a real user would use it. *(ES:
  revisa el frontend tú mismo, en el navegador — un `200` del backend no
  es una funcionalidad que sirve.)*
- **Which AI tool:** Claude **Sonnet** by default; **Opus** when a task
  is hard or you are stuck; **Copilot** for inline autocomplete and
  quick questions — not for executing a whole task. *(ES: Sonnet por
  defecto; Opus cuando es difícil o te atascas; Copilot para
  autocompletar.)*
- **You can tell your agent to skip the Why boxes — we won't stop you.**
  But the 🚦 checkpoint questions are asked by a person, and that you
  cannot outsource. Reading as you go is the cheap way to be ready.
  *(ES: puedes pedirle a tu agente que se salte las explicaciones — pero
  las preguntas del checkpoint las hace una persona; eso no se delega.)*
- **Auto mode is slice-bounded.** Auto mode (running without clarifying
  questions between turns) is allowed for the duration of **one
  slice** — a single numbered task, or one phase when the plan groups
  tasks that way. At the end of every slice, the agent **STOPS**,
  surfaces what landed (Done-when items verified, files touched,
  what's next), and waits for explicit human acknowledgement before
  starting the next slice. At 🚦 Checkpoints the stop is stronger —
  the human walks the evidence with the agent. Auto mode is **never**
  "execute the whole plan unattended." *(ES: el modo auto va por
  slice, no por plan entero. Al final de cada slice, el agente
  **PARA**, te muestra qué cerró (Done-when, archivos tocados, qué
  viene) y espera tu visto bueno antes del siguiente slice. En los
  🚦 el alto es más fuerte — recorres la evidencia con el agente.
  Auto **nunca** significa "ejecuta el plan completo solo".)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que vas a ver muchas
> veces en este plan, con su traducción y una línea de qué significan.
> Si te encuentras un término del plan que no está aquí y no lo
> entiendes, pregúntale a tu agente — no es una falla tuya, es un vacío
> de esta tabla.

| English | Español | Means |
|---|---|---|
| token contract | contrato de tokens | The canonical set of CSS variables every Pháros surface must expose; the source of truth is `registry/tokens.css` (shadcn-vue vars + an accent-independent status palette). |
| accent / sub-brand accent | acento / acento de sub-marca | The single brand color a sub-brand overrides; touches only `--primary` / `--accent` / `--ring` / `--sidebar-primary` (+ `--chart-1`). |
| status palette | paleta de estado | `--success` / `--warning` / `--error` / `--info` (+ foregrounds) — independent of the accent; **never** moves when the accent changes. |
| `@theme inline` | `@theme inline` | The Tailwind v4 block that routes utilities through `var()` so runtime CSS-var overrides actually render. |
| `@font-face` | `@font-face` | The CSS rule that registers a web font; `@nuxt/fonts` generates one per detected family. |
| FOUC guard | guard anti-FOUC | A tiny inline head script that paints `.dark` before hydration so there is no flash of unstyled content. |
| copy-in / sync | copiar-adentro / sincronizar | Distribution is by copying the registry into a repo via `scripts/sync-pharos-registry.sh`, **not** an npm package. |
| tenant | tenant / inquilino | A brand (LCH, Biuman) that consumes the Pháros design system; a tenant never prefixes an app name. |
| Done-when | terminado-cuando | The literal checkable list that means a phase is verified. |
| cold restart | reinicio en frío | `rm -rf .nuxt` then `pnpm dev` — clears the build + font cache so `@nuxt/fonts` regenerates. |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> v1+ / para después. Si un agente sugiere construir algo de esta lista,
> no lo hagas.

Explicitly out of scope — not for this plan:

- **Resolving the data-font conflict.** The brand-book "data font" (a mono for
  cifras) and Q5's "one mono" genuinely conflict. This playground does NOT
  resolve it — it makes both visible so the brand owner (@SKuger01) can decide.
  Default stays Q5 (one mono, toggle off).
- **A CRT / cobol theme or `[data-theme]` switching.** Theming is shadcn `.dark`
  class, light + dark only. finance-lch's real shell uses `[data-theme]` + cobol
  + `--nav-*`; we deliberately adopt only its **look/structure** on the locked
  `.dark`/shadcn substrate.
- **Packaging the registry as an npm package.** Distribution is copy-in via
  `scripts/sync-pharos-registry.sh`. The future home is the `pharos-ui`
  shadcn-vue registry (RFC 0008 Q3); the resizable-panel + font-token work seeds
  it but is not built here.
- **Deploying anywhere.** Still local-only.

---

## 1. Locked invariants — DO NOT DRIFT (RFC 0008 co-creation prep)

> **Resumen (ES).** Reglas que NO se pueden romper: tema por clase `.dark`
> (claro/oscuro), contrato de tokens magro shadcn-vue + paleta de estado
> independiente del acento, shell shadcn `Sidebar collapsible="icon"`, sistema de
> 3 fuentes (Fraunces + Inter + IBM Plex Mono), gráficas con @unovis, y rojo
> piloto `#E4002B` que nunca se re-tinta. La fuente de la verdad es el registry.

- **Design system = Pháros, the umbrella.** Pháros is the product design system;
  **LCH and Biuman are tenants**. The source of truth is the registry at
  `/Users/gczuluaga/dev/.github/brands/pharos_brand/registry/`; its token contract
  is `registry/tokens.css`. A tenant **never prefixes an app name** (it is
  `Pháros · Timón`, never "LCH Pháros"). Maker credit = *Interval · The Human Tech
  Co.* (footer credit only).
- **Theming = `.dark` CLASS** on `<html>`, light/dark only, **NO cobol / CRT** (Q7).
  Do NOT introduce `[data-theme]`. Theme toggle lives in the **topbar**, not the panel.
- **Token contract = shadcn-vue vars + accent-INDEPENDENT status palette** (Q4).
  The status tokens are `--success` / `--warning` / `--error` / `--info` (+ their
  foregrounds) and they **NEVER move with the accent**. Brand accent → `--primary`
  (+ `--accent`, `--ring`, `--sidebar-primary`, `--sidebar-ring`, `--chart-1`) only.
  Use `--sidebar-*` / shadcn tokens for chrome — NOT `--nav-*`. Legacy tokens
  collapse into the contract: `--text-secondary` / `--text-muted` →
  `--muted-foreground`; `--text-brand` → `--primary`; `--nav-*` → `--sidebar-*`.
- **Shell = shadcn `Sidebar collapsible="icon"`** (the RFC reference shell).
  **NO page `<h1>`** — the breadcrumb's bold leaf is the title.
  **UI copy in Spanish** (neutral Colombian; no exclamations, no emojis).
- **3-family font system (Q5):** Fraunces (display/wordmark) · Inter (sans UI) ·
  IBM Plex Mono (data + labels, default mono). **JetBrains Mono and Apax are NOT
  used in product UI** — Apax stays an LCH brand-identity asset only. The richer
  picker is **playground exploration before final Q5 lock**. Default state MUST be
  Q5 (mono = IBM Plex Mono, data font OFF).
- **Charts = @unovis, `--chart-1..5`** (Q11), client-only (`.client.vue` + `ClientOnly`).
- **Pilot-light red `#E4002B` is never re-tinted** (brand book) — it lives in the SVGs.
- Keep v1 build fixes intact: `reka-ui@2.9.6` + `tsConfig.paths['reka-ui']`,
  `striptags` dep + `optimizeDeps.include`, `build.transpile` for @unovis, FOUC guard.
- `reka-ui` 2.9.6 Switch: use `modelValue`/`update:modelValue` — `:checked` does not exist.

> 🚦 **Accent lock state (escalate before inventing any accent).** ERP ·
> Timón = LCH Navy `#003A70` (+ teal `#A0D1CA` for success) — **LOCKED**. All
> non-ERP accents (LIS clínico, LIS deportivo, Admisiones, CRM, Archivo) are
> **OPEN → TBD** (RFC 0008 Q1/Q6, owned by @SKuger01 via this playground). The
> placeholder hexes in the store are explicitly NOT decisions — **never invent
> an accent**. *(ES: solo el acento del ERP está cerrado; los demás están
> abiertos y son TBD — nunca inventes un acento, escala a @SKuger01.)*

## 2. Prerequisites · Prerrequisitos

> **Resumen (ES).** Lo que necesitas antes de empezar: el directorio de build, las
> versiones de Node/pnpm, y los SVG de marca.

- Build dir: **`/Users/gczuluaga/dev/pharos-playground/`** (fresh).
- `node >= 22`, `pnpm@10+`.
- Brand SVGs: `/Users/gczuluaga/dev/.github/brands/pharos_brand/` (navbar/icon × light/dark).

---

## Phase 0 — Scaffold · Andamiaje

> **Resumen (ES) — Fase 0: Andamiaje.**
>
> Crea el proyecto Nuxt 4 mínimo e instala todas las dependencias (Tailwind v4,
> shadcn-nuxt, Pinia, @nuxt/fonts, reka-ui pineado, @unovis, striptags).
>
> En orden, las tareas:
>
> 1. **0.1** — Crear el proyecto `pharos-playground` con `pnpm create nuxt` e `git init`.
> 2. **0.2** — Instalar dependencias dev y de runtime (versiones pineadas).
> 3. **0.3** — Correr `nuxi prepare` para generar tipos antes del init de shadcn.

- [x] **0.1** — Scaffold the project and init git.
- [x] **0.2** — Install dev + runtime dependencies (pinned versions matter).
  - **Why:** `reka-ui` is pinned to `2.9.6` because `2.9.10` breaks Vue SFC type
    inference; `striptags` must be a direct dep so Vite 7 pre-bundles the CJS dep
    that `@unovis/ts` imports; `typescript` is added explicitly to guarantee TS ≥5.5
    for reka-ui resolution.
- [x] **0.3** — `pnpm dlx nuxi prepare` to generate `.nuxt` types before shadcn init.

```bash
cd /Users/gczuluaga/dev
pnpm create nuxt@latest pharos-playground   # minimal, pnpm
cd pharos-playground
git init -q

pnpm add -D tailwindcss @tailwindcss/vite tw-animate-css
pnpm dlx nuxi@latest module add shadcn-nuxt
pnpm add @pinia/nuxt pinia @nuxt/fonts
pnpm add @vueuse/core lucide-vue-next class-variance-authority clsx tailwind-merge
pnpm add reka-ui@2.9.6        # pin — 2.9.10 breaks Vue SFC type inference
pnpm add -D typescript        # ensures TS ≥5.5 for reka-ui resolution
pnpm add @unovis/vue@1.6.5 @unovis/ts@1.6.5
pnpm add striptags            # @unovis/ts CJS dep — explicit for Vite 7 pre-bundle

pnpm dlx nuxi prepare   # generates .nuxt types before shadcn init
```

✅ **Done-when:** `pnpm dev` boots the default Nuxt page. *(ES: `pnpm dev`
arranca la página por defecto de Nuxt.)*

🚦 **Checkpoint 0.** Show gczuluaga: the booting default Nuxt page and the
`package.json` dependency list. Questions:
1. Why is `reka-ui` pinned to `2.9.6` rather than taking the latest? *(ES: ¿por
   qué se pinea `reka-ui` a `2.9.6` y no se toma la última?)*
2. Walk the dependency list live — which deps exist only to make a *transitive*
   dep build (`striptags`, `typescript`), and why? *(ES: recorre las dependencias
   en vivo — ¿cuáles existen solo para que compile una dependencia transitiva?)*

---

## Phase 1 — Token contract: `app/assets/css/main.css` · Contrato de tokens

> **Resumen (ES) — Fase 1: Contrato de tokens.**
>
> Escribe el CSS que define el contrato de tokens (shadcn-vue + paleta de estado
> independiente del acento + paleta de gráficas + stacks de fuentes overridables
> en runtime).
>
> En orden, las tareas:
>
> 1. **1.1** — Escribir `main.css` EXACTAMENTE como abajo (primitivas de marca, light, dark, `@theme inline`, preload de fuentes, base).

- [x] **1.1** — Write `app/assets/css/main.css` **exactly** as below.
  - **Why:** The `--font-mono-stack` / `--font-data-stack` in `:root` are the vars
    the font picker writes at runtime. `@theme inline` routes utilities through
    them so runtime overrides render (the `var()` indirection — without it,
    `@theme inline` bakes literal font names at build time and runtime
    `setProperty` has no effect). The `.fonts-preload` class lists all 10 picker
    fonts in a `font-family` property so `@nuxt/fonts` generates `@font-face` for
    each; the class is never applied.
  - 💡 **Heuristic.** A CSS variable only stays overridable at runtime if every
    consumer reads it through `var()`. The moment a Tailwind utility bakes the
    literal value at build time, `setProperty()` is a no-op — the indirection is
    the whole trick. *(ES: una variable CSS solo sigue siendo overridable en runtime
    si todos la leen vía `var()`; si una utilidad hornea el literal en build, el
    `setProperty()` no hace nada.)*

```css
/* Pháros brand playground — LEAN token contract (RFC 0008 Q4/Q5/Q7) */
@import "tailwindcss";
@import "tw-animate-css";
@custom-variant dark (&:is(.dark *));

/* ---- Brand primitives -> Tailwind color utilities (bg-lch-navy, etc.) ---- */
@theme {
  --color-lch-navy: #003A70;
  --color-lch-blue: #326295;
  --color-lch-teal: #A0D1CA;
  --color-lch-pink: #F4CDD4;
  --color-lch-yellow: #FBD872;
  --color-lch-burgundy: #782F40;
  --color-lch-red: #E4002B;
}

/* ---- LIGHT: shadcn contract + accent-independent status + charts ---- */
:root {
  color-scheme: light;
  --radius: 0.5rem;

  --background: #ffffff;
  --foreground: #1a1d21;
  --card: #ffffff;
  --card-foreground: #1a1d21;
  --popover: #ffffff;
  --popover-foreground: #1a1d21;
  --primary: #003A70;          /* brand accent (ERP=Navy default) — overridden at runtime */
  --primary-foreground: #ffffff;
  --secondary: #eeeeed;
  --secondary-foreground: #1a1d21;
  --muted: #f7f7f6;
  --muted-foreground: #6b6e70;
  --accent: #eeeeed;           /* shadcn neutral hover bg — NOT the brand accent */
  --accent-foreground: #1a1d21;
  --destructive: #8b1a2b;
  --destructive-foreground: #ffffff;
  --border: #e2e2e1;
  --input: #e2e2e1;
  --ring: #003A70;             /* focus ring follows the brand accent */

  --sidebar: #f7f7f6;
  --sidebar-foreground: #1a1d21;
  --sidebar-primary: #003A70;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #eeeeed;
  --sidebar-accent-foreground: #1a1d21;
  --sidebar-border: #e2e2e1;
  --sidebar-ring: #003A70;

  /* ACCENT-INDEPENDENT STATUS PALETTE — never moves when the accent changes */
  --success: #1b6b5a; --success-foreground: #e8f5f1;
  --warning: #7a5d00; --warning-foreground: #fef6dc;
  --error:   #8b1a2b; --error-foreground:   #fceaee;
  --info:    #003a70; --info-foreground:    #e4edf7;

  /* numbered chart palette (brand-derived) */
  --chart-1: #003A70;
  --chart-2: #A0D1CA;
  --chart-3: #326295;
  --chart-4: #FBD872;
  --chart-5: #782F40;

  /* font stacks — overridable at runtime (the picker writes --font-*-stack) */
  --font-mono-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --font-data-stack: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}

/* ---- DARK overrides (.dark class) ---- */
.dark {
  color-scheme: dark;
  --background: #0f2744;
  --foreground: #e8eef5;
  --card: #13233d;
  --card-foreground: #e8eef5;
  --popover: #13233d;
  --popover-foreground: #e8eef5;
  --primary: #A0D1CA;          /* ERP accent shifts to teal in dark */
  --primary-foreground: #06121f;
  --secondary: #1c3454;
  --secondary-foreground: #e8eef5;
  --muted: #16283f;
  --muted-foreground: #9bb0c6;
  --accent: #1c3454;
  --accent-foreground: #e8eef5;
  --destructive: #f4a0b0;
  --destructive-foreground: #2a0a10;
  --border: #243a5a;
  --input: #243a5a;
  --ring: #A0D1CA;

  --sidebar: #0c1f38;
  --sidebar-foreground: #e8eef5;
  --sidebar-primary: #A0D1CA;
  --sidebar-primary-foreground: #06121f;
  --sidebar-accent: #1c3454;
  --sidebar-accent-foreground: #e8eef5;
  --sidebar-border: #243a5a;
  --sidebar-ring: #A0D1CA;

  --success: #4cd1b0; --success-foreground: #0c2a24;
  --warning: #e6c34d; --warning-foreground: #2e2606;
  --error:   #f4a0b0; --error-foreground:   #2a0a10;
  --info:    #7fb0e6; --info-foreground:    #0a1f38;

  --chart-1: #5b9bd5;
  --chart-2: #A0D1CA;
  --chart-3: #8fb3d9;
  --chart-4: #FBD872;
  --chart-5: #c98a9b;
}

/* ---- map runtime vars -> Tailwind v4 utilities ---- */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);

  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-error: var(--error);
  --color-error-foreground: var(--error-foreground);
  --color-info: var(--info);
  --color-info-foreground: var(--info-foreground);

  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);

  /* 3-family system (Q5) + an overridable data slot (playground exploration) */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: var(--font-mono-stack);
  --font-data: var(--font-data-stack);
  --font-heading: "Fraunces", "Times New Roman", serif;

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

/* font-picker preload — never applied; @nuxt/fonts scans font-family for @font-face gen */
.fonts-preload {
  font-family: "JetBrains Mono", "Source Code Pro", "Fira Code", "Roboto Mono",
               "Red Hat Mono", "Spline Sans Mono", "Martian Mono", "DM Mono",
               "IBM Plex Sans", ui-monospace, monospace;
}

@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground font-sans; }
}
```

✅ **Done-when:** CSS parses clean; the `var()` indirection means `.font-mono`
and `.font-data` utilities resolve at runtime so `setProperty('--font-mono-stack',
…)` on `<html>` immediately changes the computed font-family of `.font-mono`
elements. *(ES: el CSS parsea sin errores; la indirección `var()` hace que cambiar
`--font-mono-stack` en `<html>` cambie de inmediato la `font-family` computada.)*

---

## Phase 2 — `nuxt.config.ts` · Configuración de Nuxt

> **Resumen (ES) — Fase 2: nuxt.config.ts.**
>
> Configura módulos, Tailwind v4 vía Vite, las 12 familias de fuentes
> (`@nuxt/fonts`), el guard anti-FOUC, el puerto, y el `paths` de TypeScript para
> `reka-ui`.
>
> En orden, las tareas:
>
> 1. **2.1** — Escribir `nuxt.config.ts` con módulos, Vite, fuentes, head/FOUC y typescript.

- [x] **2.1** — Write `nuxt.config.ts` as below.
  - 💡 **Heuristic.** `@nuxt/fonts` only generates `@font-face` for fonts it
    *detects in CSS*. With the `var()` indirection, picker font names never appear
    in the Tailwind utility CSS — so each picker family needs `global: true` AND
    the `.fonts-preload` class (Phase 1); both are required for reliable
    `@font-face` generation across dev cold-starts. A **cold restart** (cleared
    `.nuxt/` and font cache) is required after these changes take effect. *(ES:
    `@nuxt/fonts` solo genera `@font-face` para fuentes que detecta en el CSS; las
    del picker necesitan `global: true` y la clase `.fonts-preload`, y un reinicio
    en frío.)*

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },
  modules: ['@pinia/nuxt', 'shadcn-nuxt', '@nuxt/fonts'],
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: { include: ['striptags'] },
  },
  // @unovis touches the DOM at import; keep its ESM transpiled (still render client-only).
  build: { transpile: ['@unovis/vue', '@unovis/ts'] },
  shadcn: { prefix: '', componentDir: './app/components/ui' },
  fonts: {
    families: [
      { name: 'Fraunces',         weights: [400, 500],      provider: 'google' },
      { name: 'Inter',            weights: [400, 500, 600], provider: 'google' },
      // monospace picker (8) — global:true forces @font-face even if not in static CSS
      { name: 'IBM Plex Mono',    weights: [400, 500],      provider: 'google', global: true },
      { name: 'JetBrains Mono',   weights: [400, 500],      provider: 'google', global: true },
      { name: 'Source Code Pro',  weights: [400, 500],      provider: 'google', global: true },
      { name: 'Fira Code',        weights: [400, 500],      provider: 'google', global: true },
      { name: 'Roboto Mono',      weights: [400, 500],      provider: 'google', global: true },
      { name: 'Red Hat Mono',     weights: [400, 500],      provider: 'google', global: true },
      { name: 'Spline Sans Mono', weights: [400, 500],      provider: 'google', global: true },
      { name: 'Martian Mono',     weights: [400, 500],      provider: 'google', global: true },
      // data-font candidates
      { name: 'DM Mono',          weights: [400, 500],      provider: 'google', global: true },
      { name: 'IBM Plex Sans',    weights: [400, 500, 600], provider: 'google', global: true },
    ],
  },
  app: {
    head: {
      title: 'Pháros · Playground',
      // FOUC guard: paint .dark before hydration so there's no flash.
      script: [{
        innerHTML:
          "(function(){var t=localStorage.getItem('pharos-pg-theme');var d=t==='dark'||(t!=='light'&&window.matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d)})()",
        tagPosition: 'head',
      }],
    },
  },
  devServer: { port: 3000, host: '0.0.0.0' },
  typescript: {
    tsConfig: {
      compilerOptions: {
        paths: {
          'reka-ui': ['./node_modules/reka-ui/dist/index.d.ts'],
        },
      },
    },
  },
})
```

✅ **Done-when:** after a cold start (`rm -rf .nuxt && pnpm dev`), the browser
shows `@font-face` rules for all 10 picker fonts (check via DevTools → Sources, or
`document.fonts` in console). *(ES: tras un reinicio en frío, el navegador muestra
reglas `@font-face` para las 10 fuentes del picker.)*

---

## Phase 3 — shadcn-vue init + components · Init de shadcn-vue

> **Resumen (ES) — Fase 3: Init de shadcn-vue + componentes.**
>
> Inicializa shadcn-vue y agrega los componentes que usa el playground, cuidando
> de NO sobrescribir el `main.css` de la Fase 1.
>
> En orden, las tareas:
>
> 1. **3.1** — Correr `shadcn-vue init` (DECLINAR sobrescribir `main.css`).
> 2. **3.2** — Agregar los componentes y crear `app/lib/utils.ts`; remover cualquier `@import` de Google Fonts inyectado.

- [x] **3.1** — Run `shadcn-vue init` (new-york, zinc, prefix `""`, lucide). If
      init offers to overwrite `main.css` → **DECLINE**; then restore Phase 1 CSS
      exactly.
- [x] **3.2** — Add the components, create `app/lib/utils.ts`, and remove any
      injected Google Fonts `@import` from `main.css` (@nuxt/fonts owns fonts).

```bash
pnpm dlx shadcn-vue@latest init    # new-york, zinc, app/assets/css/main.css, prefix "", lucide
# IMPORTANT: if init offers to overwrite main.css → DECLINE; then restore Phase 1 CSS exactly.
pnpm dlx shadcn-vue@latest add button badge input label select checkbox switch \
  dialog table tabs card separator tooltip sidebar breadcrumb popover sheet
```

`app/lib/utils.ts` (created by init):
```ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

✅ **Done-when:** `ls app/components/ui` shows the added components, and
`main.css` still has the Phase-1 content (no injected `@import url(...)`, no
duplicate `@layer base`). *(ES: `ls app/components/ui` muestra los componentes y
`main.css` conserva el contenido de la Fase 1.)*

---

## Phase 4 — Store: `app/stores/playground.ts` · Estado del playground

> **Resumen (ES) — Fase 4: Store de Pinia.**
>
> El store escribe el acento de marca + overrides de fuente como variables CSS
> inline en `<html>`. La paleta de estado se deja intacta a propósito (prueba de
> independencia del acento, Q4). El ERP está LOCKED; el resto son placeholders.
>
> En orden, las tareas:
>
> 1. **4.1** — Escribir `app/stores/playground.ts` (sub-marcas, monos, fuentes de datos, `apply()`, `ensureFontLoaded`, persistencia, `init`).

🚦 **Accent placeholders are NOT decisions.** The non-ERP sub-brand hexes below are
**placeholders for @SKuger01**, marked `locked: false`. Only ERP · Timón (Navy
`#003A70` light / teal `#A0D1CA` dark) is locked. Do not promote any placeholder to
a decision without escalating (RFC 0008 Q1/Q6). *(ES: los hexes no-ERP son
placeholders para @SKuger01; solo el ERP está cerrado — no los conviertas en
decisión sin escalar.)*

- [x] **4.1** — Write `app/stores/playground.ts` as below.
  - **Why:** `apply()` writes the brand accent only to `--primary` / `--ring` /
    `--sidebar-primary` / `--sidebar-ring` / `--chart-1` — never the status tokens
    (that is the Q4 accent-independence proof). `ensureFontLoaded` is required
    because `@nuxt/fonts`' lazy `@font-face` does not re-fire on a `var()`-indirected
    `font-family` change (trap T8); without it, picked fonts silently fall back to
    system mono and the picker looks dead.

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

// 8 monos verified on Google Fonts. Q5 default = IBM Plex Mono.
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

// Data-font candidates — only applied when dataFontEnabled. The brand book mandates
// a mono + tabular-nums for cifras (BRAND.md §4.4); Inter/Plex Sans are the
// proportional-with-tabular-figures alternatives. NOTE: JetBrains Mono is a
// playground exploration candidate ONLY — it is NOT a product-UI font (see §1).
export const DATA_FONTS = [
  { id: 'jetbrains', label: 'JetBrains Mono (brand book — exploración)', stack: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'ibm-mono',  label: 'IBM Plex Mono',               stack: '"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'dm-mono',   label: 'DM Mono',                     stack: '"DM Mono", ui-monospace, SFMono-Regular, Menlo, monospace' },
  { id: 'inter',     label: 'Inter (tabular)',             stack: '"Inter", system-ui, sans-serif' },
  { id: 'ibm-sans',  label: 'IBM Plex Sans (tabular)',     stack: '"IBM Plex Sans", system-ui, sans-serif' },
]

const PREFS_KEY = 'pharos-pg-prefs'

// Pull the primary family ("Martian Mono") out of a stack string and ask the browser
// to fetch it (400 + 500). Fire-and-forget: the page repaints when the face arrives.
// REQUIRED — without this, dynamically switching --font-*-stack never triggers
// @nuxt/fonts' lazy @font-face, so picked fonts silently fall back to system mono and
// the picker looks dead. (See trap T8.)
function ensureFontLoaded(stack: string) {
  if (!import.meta.client || !document.fonts?.load) return
  const family = stack.match(/"([^"]+)"/)?.[1]
  if (!family) return
  document.fonts.load(`400 1rem "${family}"`).catch(() => {})
  document.fonts.load(`500 1rem "${family}"`).catch(() => {})
}

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
    // fonts — write the *-stack vars the utilities read (var() indirection, Phase 1)
    const mono = MONO_FONTS.find(m => m.id === monoId.value) ?? MONO_FONTS[0]
    el.style.setProperty('--font-mono-stack', mono.stack)
    const data = DATA_FONTS.find(d => d.id === dataFontId.value) ?? DATA_FONTS[0]
    // OFF => data cells fall back to the single mono (Q5 "one mono")
    el.style.setProperty('--font-data-stack', dataFontEnabled.value ? data.stack : mono.stack)
    // force the lazy @font-face fetch so the picker visibly swaps (trap T8) — without
    // this the var() swap renders as the system fallback and the picker looks dead.
    ensureFontLoaded(mono.stack)
    if (dataFontEnabled.value) ensureFontLoaded(data.stack)
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

✅ **Done-when:** the store mounts; calling `setSubBrand`, `toggleTheme`,
`setMono`, and `setDataFontEnabled` each mutate the inline CSS vars on `<html>`,
and the status tokens (`--success`/`--warning`/`--error`/`--info`) never change.
*(ES: el store monta; los setters mutan las variables CSS inline en `<html>` y los
tokens de estado nunca cambian.)*

---

## Phase 5 — `AppLogo.vue` (inline SVG) + `SidebarLogo.vue` · Logo

> **Resumen (ES) — Fase 5: Logo.**
>
> Los SVG de marca NO se pueden usar vía `<img>` (renderizan el wordmark con un
> `@import` externo de Google Fonts, bloqueado en modo estático seguro — falla y se
> ve como "dos logos"). Se renderiza el mark **inline**, que usa la Fraunces real
> de la página y se adapta al tema vía `currentColor`. El logo aparece EXACTAMENTE
> UNA VEZ, en el header del sidebar.
>
> En orden, las tareas:
>
> 1. **5.1** — Entender por qué los SVG de marca no sirven vía `<img>` (trap T6).
> 2. **5.2** — Escribir `AppLogo.vue` (SVG inline, dos variantes, dot rojo `#E4002B`).
> 3. **5.3** — Escribir `SidebarLogo.vue` que puentea `useSidebar()` dentro del provider.

### 5.1 — The brand SVG files are NOT usable via `<img>` — inline instead

- [x] **5.1** — Confirm the constraint before building the component.
  - **Why:** The brand source SVGs
    (`/Users/gczuluaga/dev/.github/brands/pharos_brand/pharos-*.svg`) render their
    wordmark as `<text>` styled by an **external** Google-Fonts `@import`. When an
    SVG is loaded through `<img src>` it runs in **secure static mode** — external
    resources are blocked and the file fails to decode entirely (`naturalWidth ===
    0`), which the browser paints as a **broken-image glyph + the `alt` text**. That
    broken glyph beside the alt text is exactly what reads as "the logo appears
    twice" (trap T6). So do NOT use `<img src>`; render the mark **inline** instead,
    where it uses the page's real Fraunces (already loaded by @nuxt/fonts) and adapts
    to the theme via `currentColor`. Copying the `public/logos/*.svg` files is
    optional (harmless if present; not referenced by the component below).

### 5.2 — `app/components/AppLogo.vue` — inline SVG (verified)

- [x] **5.2** — Write `AppLogo.vue` as below. One element per variant,
      theme-adaptive via `currentColor` on the wordmark; the pilot-light dot keeps
      the literal brand red `#E4002B` (never re-tinted — brand book). No `<img>`, no
      external font import, no light/dark file swap.

```vue
<script setup lang="ts">
// Inline SVG (NOT <img src>): the brand SVG files render their wordmark via an external
// Google-Fonts @import, which is blocked when an SVG loads through <img> (secure static
// mode) — there it fails to decode entirely (naturalWidth 0 → broken-image glyph + alt
// text, which read as "two logos"). Inlining lets the wordmark use the page's real
// Fraunces (already loaded by @nuxt/fonts) and adapt to the theme via currentColor.
// The pilot-light dot keeps the literal brand red #E4002B (never re-tinted — brand book).
withDefaults(defineProps<{ variant?: 'navbar' | 'icon' }>(), { variant: 'navbar' })
</script>

<template>
  <!-- navbar: pilot-light dot + "Pháros" wordmark -->
  <svg v-if="variant === 'navbar'" class="h-7 w-auto text-sidebar-foreground"
       viewBox="0 0 220 60" role="img" aria-label="Pháros" fill="none">
    <circle cx="22" cy="14" r="3.5" fill="#E4002B" />
    <text x="10" y="44" font-family="Fraunces, 'Times New Roman', serif"
          font-size="36" letter-spacing="-0.4" fill="currentColor">Pháros</text>
  </svg>

  <!-- icon (collapsed rail): pilot-light dot + "P" -->
  <svg v-else class="h-7 w-7 text-sidebar-foreground"
       viewBox="0 0 64 64" role="img" aria-label="Pháros" fill="none">
    <circle cx="29" cy="14" r="4.5" fill="#E4002B" />
    <text x="14" y="56" font-family="Fraunces, 'Times New Roman', serif"
          font-size="56" letter-spacing="-0.5" fill="currentColor">P</text>
  </svg>
</template>
```

### 5.3 — `app/components/SidebarLogo.vue`

- [x] **5.3** — Write `SidebarLogo.vue` as below.
  - **Why:** `useSidebar()` must be called from inside a component rendered inside
    `<SidebarProvider>` (not from the layout script setup that owns the
    `<SidebarProvider>`). This component bridges that boundary (trap T7).

```vue
<script setup lang="ts">
import { useSidebar } from '~/components/ui/sidebar'
const { state } = useSidebar()
</script>

<template>
  <AppLogo :variant="state === 'expanded' ? 'navbar' : 'icon'" />
</template>
```

✅ **Done-when:** the logo appears **exactly once** — in the sidebar header via
`<SidebarLogo />`, never in the topbar. When the sidebar expands the full navbar
wordmark shows; collapsed to the icon rail, the icon variant shows. Both stay at a
fixed x position. 0 leftover `<img alt="Pháros">`; exactly 1 visible `<svg
aria-label="Pháros">` with rendered `<text>`. *(ES: el logo aparece exactamente una
vez en el header del sidebar; nunca en el topbar; cambia navbar↔icon al colapsar.)*

---

## Phase 6 — Layout: `app/layouts/default.vue` · Layout

> **Resumen (ES) — Fase 6: Layout.**
>
> Patrón de topbar de finance-lch sobre el substrato `.dark`/shadcn. El header del
> sidebar lleva el logo. El área de contenido es un grid CSS de 3 pistas:
> `preview | resizer 6px | panel Marca`, imitando el panel redimensionable de
> finance-lch.
>
> En orden, las tareas:
>
> 1. **6.1** — Escribir `app/layouts/default.vue` (sidebar, topbar con breadcrumb-popover y toggle de tema, grid redimensionable con persistencia).
> 2. **6.2** — Crear `app/app.vue`.

- [x] **6.1** — Write `app/layouts/default.vue` as below.
  - **Why:** `SidebarInset` is already a `<main>` — do NOT nest a `<main>` inside
    it; `<NuxtPage>` goes inside a `<div>` with `overflow-y-auto`. The content area
    is a 3-track CSS grid (`preview | 6px-resizer | Marca-panel`) mimicking
    finance-lch's `FacturaDrawerPanel`/`CausacionPanel` pattern for the resizable
    right panel.

```vue
<script setup lang="ts">
import { Sun, Moon, LayoutGrid, BarChart3, ChevronDown } from 'lucide-vue-next'
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
        <SidebarLogo />
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

- [x] **6.2** — Create `app/app.vue`:

```vue
<template><NuxtLayout><NuxtPage /></NuxtLayout></template>
```

✅ **Done-when:** topbar shows `[trigger] | [Diseño ▾ / Componentes] … [org]
[theme btn]`; the Pháros logo appears once, in the sidebar header; dragging the 6px
divider resizes the panel; width persists across reload; double-click resets to
26%; theme toggle in topbar works; **no `<h1>` anywhere**. *(ES: el topbar muestra
la migaja con popover y el toggle de tema; el logo aparece una vez; el divisor
redimensiona y persiste; no hay `<h1>`.)*

🚦 **Checkpoint 6 (first real UI).** Show gczuluaga: the running app — topbar,
sidebar collapse to icon rail, the resizable Marca panel, and the theme toggle
flipping `.dark` with no FOUC. Questions:
1. Why is the theme toggle in the topbar and not in the Marca panel — and why is
   the logo never repeated in the topbar? *(ES: ¿por qué el toggle de tema va en el
   topbar y no en el panel, y por qué el logo no se repite en el topbar?)*
2. Walk the resize live: drag the divider, reload, double-click — explain where the
   width is persisted and how the default (26%) is enforced. *(ES: recorre el
   resize en vivo y explica dónde se persiste el ancho y cómo se fuerza el 26% por
   defecto.)*

---

## Phase 7 — Marca panel: `app/components/PlaygroundPanel.vue` · Panel de marca

> **Resumen (ES) — Fase 7: Panel de marca.**
>
> Un `<aside>` plano (NO un Sheet/overlay) — el layout lo monta inline como la
> tercera pista del grid. El control de tema vive en el topbar; el panel tiene
> sub-marca, acento personalizado y fuentes.
>
> En orden, las tareas:
>
> 1. **7.1** — Escribir `PlaygroundPanel.vue` (sub-marca, acento, mono, toggle de fuente de datos, nota de independencia del acento).

- [x] **7.1** — Write `PlaygroundPanel.vue` as below.

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
        como el brand book (mono para cifras).
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

✅ **Done-when:** the panel renders inline as the third grid track (not an
overlay); selecting a sub-brand, picking a custom accent, choosing a mono, and
toggling the data font all visibly re-theme the preview. *(ES: el panel renderiza
inline como tercera pista del grid; sub-marca, acento, mono y fuente de datos
re-tematizan el preview de forma visible.)*

---

## Phase 8 — Component gallery: `app/pages/index.vue` · Galería de componentes

> **Resumen (ES) — Fase 8: Galería de componentes.**
>
> Usa `font-data` (no `font-mono`) en todas las cifras para que el eje de fuente de
> datos sea visible. Las píldoras de estado usan tokens de estado y NO se recolorean
> al cambiar el acento.
>
> En orden, las tareas:
>
> 1. **8.1** — Escribir `app/pages/index.vue` con las tarjetas en orden y las cifras en `font-data`.

- [x] **8.1** — Write `app/pages/index.vue`. Use `font-data` (not `font-mono`) on
      all cifras so the data-font axis is visible. Status pills use status tokens;
      they must NOT recolor on accent change.

Key lines to get right:

```vue
<!-- Table numeric cell — font-data + tabular features: -->
<TableCell class="text-right font-data tabular-nums slashed-zero lining-nums" :class="row.monto < 0 ? 'text-error' : ''">

<!-- Typography card — two samples: -->
<p class="font-mono text-sm">Mono · IBM Plex Mono · etiquetas · ABCDEF · {} [] =></p>
<p class="font-data tabular-nums slashed-zero lining-nums text-sm">Datos · 0123456789 · $1.234.567 · 0 con barra (cero/letra O)</p>
```

Full `app/pages/index.vue` structure (cards in order): Botones · Insignias y estados ·
Formulario · Tabla financiera · Pestañas · Diálogo · Tipografía. All headings Spanish.

✅ **Done-when:** all gallery cards render in order; cifras use `font-data` and
visibly change when the data-font axis switches; status pills keep their colors
when the accent changes. *(ES: todas las tarjetas renderizan en orden; las cifras
usan `font-data` y las píldoras de estado no cambian con el acento.)*

---

## Phase 9 — Charts: `app/pages/graficas.vue` + `app/components/PgCharts.client.vue` · Gráficas

> **Resumen (ES) — Fase 9: Gráficas.**
>
> `PgCharts.client.vue` usa `@unovis/vue` (VisXYContainer/VisLine/VisDonut). Los
> colores vienen de `var(--chart-N)`. El sufijo `.client` lo mantiene fuera de SSR;
> `build.transpile` está puesto.
>
> En orden, las tareas:
>
> 1. **9.1** — Escribir `graficas.vue` (envuelto en `ClientOnly` con fallback).
> 2. **9.2** — Mantener `PgCharts.client.vue` idéntico a la implementación v1.

- [x] **9.1** — Write `graficas.vue` as below.

```vue
<!-- graficas.vue -->
<template>
  <ClientOnly>
    <PgCharts />
    <template #fallback><div class="h-72 animate-pulse rounded-md bg-muted" /></template>
  </ClientOnly>
</template>
```

- [x] **9.2** — Keep `PgCharts.client.vue` identical to the v1 implementation —
      @unovis + chart data unchanged.

✅ **Done-when:** `/graficas` renders charts (line + donut); the breadcrumb leaf
reads "Gráficas"; the charts recolor on accent change (via `--chart-1`); no SSR
errors. *(ES: `/graficas` renderiza las gráficas; la migaja dice "Gráficas"; las
gráficas se recolorean con el acento; sin errores de SSR.)*

---

## 10. Known issues, traps, and fixes (discovered during build) · Trampas y arreglos

> **Resumen (ES).** Las trampas que se descubrieron construyendo. El picker de
> fuentes solo funciona con tres arreglos en capas (T4 → T5 → T8). Los SVG de marca
> solo sirven inline (T6). `useSidebar()` no se puede llamar en el script del layout
> (T7). Léelas antes de tocar fuentes o logo.

### T1 — `reka-ui` TypeScript resolution
`tsc` error: `Failed to resolve import source "reka-ui"`. Fix: `pnpm add -D typescript`
(ensures TS ≥5.5) + add `typescript.tsConfig.compilerOptions.paths['reka-ui']` in
`nuxt.config.ts` (Phase 2 already includes this).

### T2 — `striptags` CJS/ESM conflict
`@unovis/ts` imports `striptags` (CJS); Vite 7 doesn't auto-wrap it unless it's a
direct dep. Fix: `pnpm add striptags` + `vite.optimizeDeps.include: ['striptags']`
(Phase 2 already includes both).

### T3 — `shadcn-vue add` injects Google Fonts CDN
The CLI may inject `@import url('https://fonts.googleapis.com/...')` and a duplicate
`@layer base {}` block into `main.css`. After running `shadcn-vue add`, verify
`main.css` still matches Phase 1 exactly; restore if not.

> **Font picker — three layered traps (T4 → T5 → T8).** The picker only renders
> correctly with ALL THREE fixes. T4 makes the CSS var override take effect; T5 makes
> the `@font-face` rules exist; T8 makes the browser actually FETCH the face on switch.
> Missing any one → the picker silently falls back to the system mono and "does nothing."

### T4 — `@theme inline` bakes font literals (necessary, not sufficient)
`@theme inline { --font-mono: "IBM Plex Mono", ... }` bakes the literal into the
`.font-mono` utility at build time. Runtime `setProperty('--font-mono', ...)` on `<html>`
has NO effect because the utility uses the baked literal, not the var. Fix: route
through `var(--font-mono-stack)` so the utility reads the overridable var (Phase 1).
Verified: after the fix, setting `--font-mono-stack` changes
`getComputedStyle(el).fontFamily` for `.font-mono` elements. **But the glyphs still
won't change until T8 — the computed family updates while the face is unfetched.**

### T5 — `@nuxt/fonts` misses picker fonts without `global:true` + preload class
`@nuxt/fonts` only generates `@font-face` for fonts it detects in CSS. With the
`var()` indirection (T4 fix), no font names appear in the Tailwind utility CSS —
only in the JS store. Fix: (a) add `global: true` to every picker family in
`nuxt.config.ts`, AND (b) add a `.fonts-preload` CSS class listing all picker font
names in a `font-family` property (Phase 1 CSS). Both are required; either alone
is insufficient. After this change, a **cold restart** (`rm -rf .nuxt && pnpm dev`)
is required to regenerate the font cache. Verified: all 10 picker `@font-face`
families are present in the document.

### T8 — @nuxt/fonts faces don't auto-fetch on a dynamic font-family change (the real "picker does nothing")
This is the bug the user actually saw. Even with T4 + T5 done, selecting a font in the
picker changed the computed `font-family` but **did not change the rendered glyphs** —
every option kept rendering as the system mono. Runtime evidence:
`document.fonts.check('1rem "Martian Mono"')` was **false** right after the picker set
the var, and the rendered text width was unchanged; yet an explicit
`document.fonts.load('1rem "Martian Mono"')` returned the face and made the same text
render **72.8px wider** (Martian's wider advance). So the faces are valid and DO render
distinctly — the browser's lazy `@font-face` loader simply doesn't re-fire when a
`var()`-indirected `font-family` changes on already-laid-out text.
**Fix:** the store's `apply()` calls `ensureFontLoaded(stack)` — extract the primary
family from the stack and `document.fonts.load()` it (400 + 500) to force the fetch
(Phase 4). Fire-and-forget; the page repaints when the face arrives. Verified: after
the fix, picking Martian Mono changes the rendered width 436.81 → 509.61px and
`document.fonts.check` → true.

### T6 — Brand SVGs can't be used via `<img>` (the real "logo appears twice")
The brand SVG files render their wordmark as `<text>` styled by an **external**
Google-Fonts `@import` inside `<style>`. Loaded through `<img src>`, an SVG runs in
**secure static mode** (external resources blocked) and **fails to decode entirely** —
runtime evidence: `img.complete === true` but `img.naturalWidth === 0`. The browser
paints that as a **broken-image glyph + the `alt="Pháros"` text**, which reads as "the
logo appears twice." (HTTP 200 + valid markup + correct MIME — so curl/network checks
look fine; only `naturalWidth` and a screenshot reveal it.) **Fix:** render the mark as
**inline SVG** in `AppLogo.vue` (Phase 5) — uses the page's real Fraunces and adapts via
`currentColor`; no `<img>`, no external import, no light/dark file swap. Verified: 0
leftover `<img alt="Pháros">`, exactly 1 visible `<svg aria-label="Pháros">` with
rendered `<text>`. The single-instance + fixed-on-collapse rule (one `<SidebarLogo>` in
the sidebar header, never in the topbar) still holds — verified the logo stays at x=12
and swaps navbar↔icon on collapse.

### T7 — `useSidebar()` cannot be called in the layout's script setup
`useSidebar()` uses Vue `inject()` and must be called from within a component that's
a descendant of `<SidebarProvider>`. The layout script setup runs for the component
that owns `<SidebarProvider>` in its template — calling `useSidebar()` there would fail.
Fix: `SidebarLogo.vue` is a separate component, rendered inside `<Sidebar>` (which is
inside `<SidebarProvider>`), so its script setup can safely call `useSidebar()`.

---

## 11. Q9 snapshot determinism (required guard for Playwright) · Determinismo de snapshots

> **Resumen (ES).** Antes de cada snapshot, siembra/limpia `localStorage` al estado
> canónico para que los snapshots sean reproducibles.

Before each snapshot, seed/clear localStorage to canonical state:

```js
await page.addInitScript(() => {
  localStorage.removeItem('pharos-pg-panel-pct')    // -> DEFAULT_PCT (26)
  localStorage.removeItem('pharos-pg-prefs')        // -> ERP / IBM Plex Mono / data-font OFF
  localStorage.setItem('pharos-pg-theme', 'light')  // set explicitly per snapshot variant
})
```

The panel's default width (26%) is the canonical snapshot width. Mono/data-font/accent
are likewise set explicitly per snapshot variant, never inherited from a prior session.

---

## 12. Run & acceptance checklist · Correr y checklist de aceptación

> **Resumen (ES).** Cómo correr la app (con reinicio en frío) y la lista de
> aceptación completa. La app NO está verificada hasta que cada línea sea
> literalmente cierta en el navegador.

```bash
cd /Users/gczuluaga/dev/pharos-playground
rm -rf .nuxt                # cold start so @nuxt/fonts regenerates with all families
pnpm dev                    # http://localhost:3000
```

✅ **Done-when (exit acceptance).** Drive the page and confirm ALL of:

- [ ] **Logo** renders as a real **inline-SVG Fraunces wordmark** (NOT a broken image —
      `img.naturalWidth` must be >0, or better, there are 0 `<img alt="Pháros">` and exactly
      1 visible `<svg aria-label="Pháros">`). Appears exactly once — in the sidebar header,
      never the topbar. Wordmark recolors with the theme (via `currentColor`); pilot-light dot
      stays `#E4002B`. Shows full "Pháros" expanded, switches to "P" icon when collapsed,
      and stays at a fixed left position (x≈12) — does not shift with sidebar state. (T6)
- [ ] **Topbar (finance-lch pattern):** `[SidebarTrigger] | [Diseño ▾ / Componentes]` breadcrumb
      where "Diseño" chip opens a popover listing both pages; right side shows org name +
      round theme toggle. **No `<h1>` anywhere.**
- [ ] **Sidebar** stays the shadcn `Sidebar collapsible="icon"`; trigger collapses to icon rail.
- [ ] **Marca panel fixed in-view on the right** (no overlay). Dragging the 6px divider
      resizes it; width persists across reload; double-click resets to 26%.
- [ ] **Theme toggle** (topbar) flips light ↔ dark (`.dark` on `<html>`), no FOUC. No cobol.
- [ ] **Sub-brand switch** recolors buttons, sidebar active, focus ring, chart-1 (`--primary`
      propagates); **status pills do NOT move** (Q4 proof).
- [ ] **Custom accent** live-retints; "Limpiar" restores preset.
- [ ] **Mono picker (8 families)** visibly changes the typography sample AND the table cifras.
      The font must actually RENDER differently — measure rendered text width, not just the
      computed CSS var (T8: a changed `font-family` whose face is unfetched looks identical).
      Use Martian Mono for an obvious test: rendered width jumps ~+70px and
      `document.fonts.check('1rem "Martian Mono"')` becomes true. Requires `ensureFontLoaded`
      in `apply()` (T8) on top of T4 + T5.
- [ ] **Data-font toggle:** OFF → cifras use the selected mono (one mono, Q5); ON → cifras
      switch to the chosen data font (default JetBrains Mono — exploration only) with
      `tabular-nums`/`slashed-zero`. The data Select is disabled while OFF.
- [ ] **Charts** (`/graficas`) render; breadcrumb leaf reads "Gráficas"; recolor on accent change.
- [ ] No console errors; **`pnpm build` succeeds** (charts stay `.client`/`ClientOnly`).

Screenshots: (1) light+ERP, (2) dark+ERP, (3) light+placeholder accent,
(4) data-font toggle ON/OFF, (5) panel resized.

🚦 **Checkpoint 12 (exit).** Show gczuluaga: every acceptance line walked live in
the browser, plus the 5 screenshots and a green `pnpm build`. This checkpoint
**blocks archiving the plan** until Checkpoints 0, 6, and 12 have all been walked.
Questions:
1. Demonstrate the Q4 accent-independence proof live — switch sub-brands and show the
   status pills do not move. *(ES: demuestra en vivo la independencia del acento —
   cambia de sub-marca y muestra que las píldoras de estado no se mueven.)*
2. Pick Martian Mono and show — with a width measurement, not just the CSS var — that
   the glyphs actually changed (T8). *(ES: elige Martian Mono y muestra, con una
   medición de ancho, que los glifos cambiaron de verdad.)*

---

## Decisions · Decisiones

> Collected 🛑 markers that are still open, and resolved decisions logged below for
> traceability.

**Open:**

- 🛑 **Non-ERP sub-brand accents** — LIS clínico, LIS deportivo, Admisiones, CRM,
  and Archivo accents are TBD. Pending: @SKuger01 decides via this playground (RFC
  0008 Q1/Q6); the placeholder hexes in the store are NOT decisions.
- 🛑 **Q5 final mono / data-font split** — the brand-book "mono for cifras" vs Q5's
  "one mono" conflict is deliberately left open. Pending: brand owner decides after
  seeing both axes in the playground.

**Resolved during planning (2026-06-15 unless noted):**

- **Design system shape** — Pháros is the umbrella product design system; LCH and
  Biuman are tenants. Source of truth = the registry at
  `.github/brands/pharos_brand/registry/`; token contract = `registry/tokens.css`
  (shadcn-vue vars + accent-independent `--success`/`--warning`/`--error`/`--info`).
- **Token collapse** — legacy tokens fold into the contract: `--text-secondary` /
  `--text-muted` → `--muted-foreground`; `--text-brand` → `--primary`; `--nav-*` →
  `--sidebar-*`.
- **Theming** — shadcn `.dark` class, light + dark only; no cobol/CRT; no
  `[data-theme]` (Q7).
- **Fonts** — Fraunces (display/wordmark) + Inter (sans UI) + IBM Plex Mono (data +
  labels). JetBrains Mono and Apax are NOT product-UI fonts; Apax stays an LCH
  brand-identity asset; JetBrains Mono appears only as a playground exploration
  candidate.
- **ERP accent locked** — Pháros · Timón = LCH Navy `#003A70` (+ teal `#A0D1CA`
  success) — locked (RFC 0008 Q1/Q6).
- **Merge mode** — merge-commit everywhere; squash merging disabled org-wide.
- **Commit/branch type vocabulary** — canonical set is `feat | fix | refactor | test
  | chore | docs | hotfix | ci` (`ci` added org-wide; `hotfix` valid as both a
  branch and a commit type).
- **Distribution** — copy-in via `scripts/sync-pharos-registry.sh`, not an npm
  package.
- **Tenancy naming** — a tenant never prefixes an app name (`Pháros · Timón`, never
  "LCH Pháros"); maker credit = Interval · The Human Tech Co. (footer only).
- **Supersedes** — `brand-playground-tweaks-plan.md` merged into this plan and
  archived. *(2026-06-14.)*

## Risks · Riesgos

> **Resumen (ES).** Lo que puede salir mal y dónde está la mitigación concreta —
> sobre todo el picker de fuentes y los SVG de marca.

- **Font picker silently dead** → a font is selected, the CSS var changes, but the
  glyphs never change (the three-layered T4/T5/T8 failure). **Mitigation:** keep
  ALL THREE fixes — `var()` indirection (Phase 1), `global:true` + `.fonts-preload`
  (Phases 1–2) with a cold restart, and `ensureFontLoaded` in `apply()` (Phase 4).
  Verify in the browser by measuring rendered text width with Martian Mono, not by
  reading the computed CSS var.
- **Logo renders as a broken image** → using `<img src>` for the brand SVG fails to
  decode in secure static mode and reads as "two logos" (T6). **Mitigation:** render
  the mark inline in `AppLogo.vue` (Phase 5); never reintroduce `<img src>` for the
  brand SVG. Verify with `naturalWidth`/screenshot, not curl (HTTP 200 hides it).
- **`shadcn-vue add` overwrites the token contract** → the CLI may inject a Google
  Fonts `@import` and a duplicate `@layer base` into `main.css` (T3). **Mitigation:**
  after every `shadcn-vue init`/`add`, diff `main.css` against Phase 1 and restore.
- **Accent independence regresses** → a future edit moves a status token with the
  accent, breaking the Q4 proof. **Mitigation:** `apply()` writes the accent only to
  `--primary`/`--ring`/`--sidebar-primary`/`--sidebar-ring`/`--chart-1`; the exit
  checkpoint demonstrates the status pills staying put on a sub-brand switch.
- **A placeholder accent gets shipped as a decision** → the non-ERP hexes are
  mistaken for locked values. **Mitigation:** they carry `locked: false` and a
  "propuesta" badge; escalate to @SKuger01 before promoting any.

## References

- RFC 0008 — Pháros design system + co-creation (Q1/Q4/Q5/Q6/Q7/Q9/Q11).
- Token contract source of truth: `../brands/pharos_brand/registry/tokens.css`.
- Registry README + frontend standards: `../brands/pharos_brand/registry/README.md`,
  `../brands/pharos_brand/registry/frontend-standards.md`.
- Distribution script: `../scripts/sync-pharos-registry.sh`.
- Brand book + backbone: `../brands/pharos_brand/BRAND.md`,
  `../brands/pharos_brand/BACKBONE.md` (`.es.md` Spanish counterpart).
- Tracking issue: Interval-Col/.github#27.
- Superseded plan: `brand-playground-tweaks-plan.md` (merged here; slated for
  `archive/`).
- Plan authoring guidance: `.github/agents/plan-craft.agent.md`; template at
  `../templates/plan-template.md`.
