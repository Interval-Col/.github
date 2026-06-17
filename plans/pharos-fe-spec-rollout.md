# Pháros FE-spec rollout — single-sweep migration of the 4 pre-launch apps

> **Execution plan for [RFC 0008](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) (ACCEPTED 2026-06-17), Phases 1–3.**
> Migrate the four **pre-launch** Pháros apps to the accepted FE contract in one coordinated
> sweep — each app fully. *(Pre-go-live, so the legacy "gate + recommend" gradual policy does NOT
> apply — that's for already-shipped pages.)*
>
> **Written to be mostly executable by a Sonnet-class agent.** Steps are file-anchored and
> imperative; each app has explicit **VERIFY** commands. Judgment-heavy steps are tagged
> **🟠 ESCALATE** (human/architect decides — do NOT guess); everything else is **🔵 mechanical**.
> Grounded in a 2026-06-17 per-app FE characterization. All repos branch off **`develop`**.
> Tracking issue: [`.github`#43](https://github.com/Interval-Col/.github/issues/43).

## Execution protocol (read first, implementing agent)

For each app, work its section top-to-bottom as one branch:

1. `git -C <repo> checkout develop && git -C <repo> pull && git -C <repo> checkout -b feat/pharos-fe-spec`.
2. Do the 🔵 steps in order. For each 🟠 step: **stop and ask the human/owner** (don't improvise).
3. **Gate after every step**: `pnpm lint-check` must stay green (or get greener). Run the app and eyeball the changed surface in **both light and dark**.
4. **Commit per step**, scoped to files you touched (Conventional Commits + the `Co-Authored-By` trailer). **Never `git add -A`/`.`** (shared repos carry other actors' WIP). **Never push** unless the owner asks.
5. App is **done** when the per-app **VERIFY** block all passes. Then the owner opens the PR (owners merge their own).

**Copy, don't reinvent.** The 4 gate scripts + `eslint.config.mjs` are portable verbatim from
`design-studio` (PR #4) or `finance-lch/frontend`. The shell/tokens/lockup come from the registry
(Step 0). Lucide glyph imports: `Radar`, `Anchor`, `ShipWheel`, `Telescope` from `lucide-vue-next`.

**Global ESCALATE list (never let a Sonnet agent guess these):** the system-health **beacon backend
contract**; **chart** migrations (statistical parity — defer to `.github`#25, pair with a human);
**admission cashier/queue** flow refactors; mapping an app's ad-hoc palette (emerald/gray) to
semantic roles when the intent is ambiguous.

## Owners & order

| # | App | FE dir | Owner | Effort | Role |
|---|---|---|---|---|---|
| **0** | **pharos-lis** | `lab-qc/frontend` | **@gczuluaga** | L | **First pass — extracts the shared foundation + refines this plan** (architect-led) |
| 1 | admission-patient | `.` (root `app/`) | @SKuger01 | XL | Full adoption (design impl lead, Q8) |
| 2 | finance-lch | `frontend/` | @egomez | L | Token-reference cleanup + shell |
| 3 | commercial-lch | `frontend/` | @crincon | XL | Near-greenfield shell build |

**Sequencing.** Step 0 (foundation) is a **hard prerequisite** — it produces the registry every other
app copies in. After it lands, **admission / finance-lch / commercial depend only on the foundation,
not on each other** — run them in the stated order *or* overlap across owners. finance-lch is L (lighter
than admission's XL) and can move fast once unblocked.

---

## The contract — definition of "migrated" (every app)

Done when all hold and `pnpm lint-check` + visual-regression are green:

- [ ] **Stack**: Nuxt 4 · Vue 3 · TS · Tailwind v4 (CSS-first `@theme`, no `tailwind.config.js`) · shadcn-vue (new-york, reka-ui).
- [ ] **Tokens**: shadcn vars + **accent-independent status palette** (`--status-{success,warning,error,info}` + `-bg`) + `--sidebar-*`; **0 hardcoded hex outside `app/assets/css`**; legacy aliases drained.
- [ ] **Type — 4 families**: Fraunces (display) · **DM Sans** (UI) · IBM Plex Mono (labels) · JetBrains Mono (data, `tabular-nums`).
- [ ] **Theme**: `.dark` **class**, light + dark **only** (no `cobol`, no `[data-theme]`).
- [ ] **App-shell**: shared **"Faro + Instrumento"** — shadcn `Sidebar collapsible="icon"` + **beacon rail + ⌘K** + **live pilot-light health beacon** + breadcrumb-topbar (**no page H1**), desktop-first.
- [ ] **Sub-brand**: the app's glyph + accent + `Pháros · <name>` lockup (wordmark = Fraunces burgundy `#782F40` + red `#E4002B` pilot light, never re-tinted).
- [ ] **Gates + compliance testing**: 4 design gates + ESLint in `pnpm lint-check`, a pre-commit hook, a required CI check, Playwright visual-regression, + token-drift/contrast/font checks — see **FE brand-compliance testing** below (Layers A–D).
- [ ] **Registry**: shell + tokens **copied in** from `.github/brands/pharos_brand/` (not a package).
- [ ] **Charts** 🟠: `@unovis` + brand-fixed `--chart-1..5` (RFC 0008 Q11; via `.github`#25).

### Per-app sub-brand (RFC 0008 Q1/Q6 — LOCKED 2026-06-17)

| App | Name | Glyph (lucide) | Accent light / dark |
|---|---|---|---|
| pharos-lis | **Clínico** | Sonda → `Radar` | `#1B6B5A` / `#4CD1B0` (teal) |
| admission-patient | **Recepción** | Muelle → `Anchor` | `#FFE0E6` (rosa) |
| finance-lch | **Números** | Timón → `ShipWheel` | `#7A5D00` / `#E6C34D` (ámbar) |
| commercial-lch | **Clientes** | Catalejo → `Telescope` | `#FFB86B` (ámbar claro) |

---

## Step 0 — Foundation extraction 🟠 architect-led (@gczuluaga, via pharos-lis)

**Not a Sonnet step** — this is design extraction. The pharos-lis first pass distils the shared source
from the three proven impls — **pharos-lis** (shell + gates, cleanest), **finance-lch** (token/status
pipeline), **`design-studio`** (already prototypes the Faro+Instrumento shell, the live beacon, the
lockup, the per-sub-brand accent model) — into `.github/brands/pharos_brand/`:

- [ ] **Token contract** copy-in CSS: shadcn vars + status palette + `--sidebar-*` + the **5 sub-brand accent themes** + brand-fixed `--chart-1..5`.
- [ ] **App-shell registry component(s)**: `Sidebar collapsible="icon"` + beacon rail + ⌘K + live pilot-light beacon + breadcrumb-topbar (harden from `design-studio`).
- [ ] **Wordmark/lockup component**: reuse `design-studio`'s `AppLogo` (beacon-over-"P" already correct).
- [ ] **4 gate scripts + `eslint.config.mjs` + visual-regression scaffold** — promote the `design-studio`/`finance-lch` copies as canonical.
- [ ] **Copy-in sync mechanism** (committed script; resolve `npx shadcn add` vs thin copy).
- [ ] **🟠 Decide the beacon backend health contract** (endpoint + shape) — blocks the beacon in every app.
- [ ] **Refine this plan** with what the first pass surfaces, then unblock steps 1–3.

> Roles stay distinct: `design-studio` = prototype/validation (local-dev) · registry = source of truth · `pharos-ui` (future) = component library.

---

## Step 0 (cont.) — pharos-lis migration (@gczuluaga) · L · `lab-qc/frontend`

Already conforms: stack · `.dark` · `Sidebar collapsible=icon` · breadcrumb-no-H1 · **4 gates · 0 violations** · i18n.

- [ ] 🔵 **Accent PINK → TEAL.** In `app/assets/css/main.css` (~L51–97) replace `--primary`/`--accent`/`--sidebar-accent` (+ the `.dark` block + `@theme inline`): pink `#e4002b`/`#fc9bb3` → teal `#1B6B5A` (light) / `#4CD1B0` (dark). Burgundy stays the wordmark constant. *(Resolves shipped-pink-vs-burgundy.)*
- [ ] 🔵 **Inter → DM Sans**: `nuxt.config.ts` (~L23) `{ name: 'Inter' … }` → `{ name: 'DM Sans', weights: [400,500,600] }`; update `--font-sans` in `main.css @theme`.
- [ ] 🔵 **Lockup**: `PharosLogo.vue` → `Pháros · Clínico` + Sonda/`Radar` glyph; sublabel `CONTROL DE CALIDAD` → `CLÍNICO`.
- [ ] 🟠 **Beacon**: add the live pilot-light health beacon to the topbar — needs the Step-0 backend contract.
- [ ] 🟠 **Charts → @unovis** (`pages/analytics/media-movil.vue`, Chart.js today) — statistical-parity port via `.github`#25.
- [ ] 🔵 **Registry copy-in**: repoint shell + tokens + `public/brand/` to the extracted registry (dogfood the sync).
- **VERIFY**: `pnpm lint-check` green · `grep -rn "#e4002b\|#fc9bb3" app/` → 0 · DM Sans renders · teal correct in light+dark across sidebar/breadcrumb/buttons/badges.

---

## Step 1 — admission-patient (@SKuger01) · XL · root `app/`

Has Nuxt4/TW4/shadcn + `.dark`, but greyscale tokens, emerald bespoke shell, no RFC fonts, **0 gates**.
Today: **77 raw-HTML · 35 emerald palette · 28 hex**, page H1s.

- [ ] 🔵 **Wire the gates first** (report-only): copy `scripts/check-no-*.mjs` + `eslint.config.mjs` + the `lint-check` script from `design-studio`/`finance-lch`. Run them to get the live violation list (the numbers below are estimates).
- [ ] 🔵 **Adopt the registry shell** (replaces the emerald `app.vue` shell): sidebar + breadcrumb-topbar; **delete page H1s**.
- [ ] 🔵 **Token layer**: add semantic + status + `--sidebar-*` + Recepción **rosa `#FFE0E6`** accent (replaces greyscale-only).
- [ ] 🔵 **Fonts**: add the 4-family stack (`nuxt.config.ts` + `main.css`).
- [ ] 🔵 **Sub-brand**: Recepción lockup + Muelle/`Anchor` glyph (registry lockup component).
- [ ] 🟠 **Kill raw HTML (77 → shadcn)**: `Button`/`Table`/`Input`/`Select`/`Textarea`. **Cashier/queue/scheduling pages (Reception.vue, AdminManagement.vue, Scheduling.vue) are behaviorally fragile — pair with the owner, convert behind tests, one page per commit.**
- [ ] 🟠 **Emerald (35) → semantic**: map by role (brand/primary→`--primary`/accent; success→`--status-success`; etc.). **If a usage's intent is ambiguous, ask the owner** before mapping.
- [ ] 🔵 **Hex (28) → tokens** in `main.css`.
- **VERIFY**: `pnpm lint-check` green (allowlist only documented exceptions) · no page `<h1>` in content · rosa accent both themes · raw-HTML gate exits 0.

---

## Step 2 — finance-lch (@egomez) · L · `frontend/`

Token reference: stack/status-palette/**gates clean · 0 violations**. Gaps are theme + shell:

- [ ] 🔵 **`[data-theme]` → `.dark` class**: replace every `:root[data-theme='dark']` selector in `main.css` and the JS toggle (`setAttribute('data-theme', …)` → `classList.toggle('dark', …)`). **VERIFY** `grep -rn "data-theme" app/` → 0.
- [ ] 🔵 **DROP cobol**: remove the ~140-line terminal theme + VT323 import + the 3rd toggle option (→ 2-way light/dark). Add a read-time fallback: `if (stored === 'cobol') stored = 'light'`. **VERIFY** `grep -rni "cobol\|vt323" app/` → 0.
- [ ] 🔵 **Fonts**: add Fraunces (display) + **DM Sans** (UI) + import JetBrains Mono (data); keep IBM Plex Mono (labels).
- [ ] 🔵 **Accent**: define `--accent` = ámbar `#7A5D00`/`#E6C34D` (currently only `--status-warning`). Drain residual **"Pulso"** strings + Spanish bridge aliases (`grep -rni "pulso" app/`).
- [ ] 🟠 **Define + migrate charts**: `--chart-1..5` (referenced-but-undefined) → brand-fixed @unovis palette; KpiCard/KpiTrendModal off Chart.js via `.github`#25 (statistical parity).
- [ ] 🔵 **Shell**: custom CSS-grid → registry `Sidebar collapsible=icon` + ⌘K + beacon.
- [ ] 🔵 **Sub-brand**: `Pháros · Números` wordmark + Timón/`ShipWheel` glyph.
- **VERIFY**: `pnpm lint-check` green · 0 `data-theme`/`cobol`/`vt323` · `--chart-1..5` defined · ámbar accent both themes · no "Pulso" in user-facing strings.

---

## Step 3 — commercial-lch (@crincon) · XL · `frontend/`

Least mature — a **shell build**. shadcn **declared but never initialized** (no `app/components/ui/`),
**no `layouts/`, bare `app.vue`**, light-only. Today: **61 raw-HTML · 106 gray palette · 26 hex**, no gates/Playwright.

- [ ] 🔵 **Initialize shadcn-vue** (new-york, reka-ui): copy the `ui/` registry from `.github/brands/pharos_brand/`.
- [ ] 🔵 **Build the shell**: create `app/layouts/default.vue` from the registry (Sidebar + breadcrumb-topbar + beacon); wrap `app.vue`'s bare `NuxtPage`.
- [ ] 🔵 **Tokens + `.dark`**: add the full contract + Clientes **ámbar-claro `#FFB86B`** accent; implement the `.dark` class mechanism (light-only today).
- [ ] 🔵 **Fonts**: 4-family stack (has Inter/JetBrains today).
- [ ] 🔵 **Kill raw HTML (61 → shadcn)** across the quotes pages (`index.vue`/`new.vue`/`[id].vue`).
- [ ] 🟠 **Gray palette (106) → semantic tokens.** Bulk, but mechanical for `gray-*` → `--muted`/`--border`/`--foreground` by context; **for the 16 SVG-gradient hex in `quotes/new.vue`, if it's brand artwork use a documented `lint-allow-hex`** rather than tokenizing — confirm with owner.
- [ ] 🔵 **Hex (10 inline) → tokens** in `main.css`.
- [ ] 🔵 **Sub-brand**: Clientes lockup + Catalejo/`Telescope` glyph.
- [ ] 🔵 **Wire gates + ESLint + Playwright** (only `eslint .` today; `test:run` is a stub).
- **VERIFY**: `pnpm lint-check` green · `app/components/ui/` exists · `app/layouts/default.vue` renders the shell · `.dark` toggles · ámbar-claro accent both themes.

---

## FE brand-compliance testing (hooks + CI/CD) — keep apps from drifting back

The migration is one-time; **compliance must stay enforced** after. The 4 static gates check *rules*
(no hex, no raw HTML) but **not** visual/contrast/drift — so we layer. Each app wires Layers A+B during
its migration; Layers C+D ship from the foundation (Step 0) as shared scaffolds the apps adopt. Builds
on existing substrate: `.pre-commit-config.yaml` already exists in every repo; `design-studio` PR #4
already ships the `lint-check` CI job; both reference apps already carry `@playwright/test`.

| Layer | What it catches | Where it runs | Mechanism |
|---|---|---|---|
| **A — pre-commit hook** | rule violations, before they land | local (fast) | a `design-gates` hook in `.pre-commit-config.yaml` running the 4 gates + ESLint on staged `app/**.{vue,ts,css}` |
| **B — CI required check** | the authoritative PR gate | CI on PR + push to `develop`/`main` | the `lint-check` job (ESLint + 4 gates), made a **required status check** (like `gitleaks`) |
| **C — visual-regression** | unintended visual change | CI on PR | Playwright snapshots of the shell + components + each sub-brand accent in **light + dark**; fail on un-reviewed diff (RFC 0008 Q9) |
| **D — brand-semantic checks** | what rules can't see | CI on PR | token-drift + contrast/a11y + font allowlist (below) |

**Layer A — pre-commit hook 🔵.** Add to each repo's `.pre-commit-config.yaml` a local hook that runs
the gate scripts (or `pnpm lint-check`) on staged FE files. Fails the commit on violation — the cheapest,
earliest catch. (Owner copies the hook block from the foundation's reference `.pre-commit-config.yaml`.)

**Layer B — CI required check 🔵 to wire / 🟠 to enforce.** Each app gets the `lint-check` CI job
(copy `design-studio/.github/workflows/ci.yml`, adjust working dir). Wiring the job is 🔵; **making it a
*required* branch-protection check on `develop`/`main` is an admin action → @gczuluaga (gatekeeper, Q8) 🟠.**

**Layer C — visual-regression 🟠 (human-reviewed baselines).** Playwright snapshot suite, seeded from the
**`design-studio` playground** (it already renders the shell + components across themes/accents — the
natural snapshot surface, RFC 0008 Q9). Snapshot: the app-shell, the shared components, and the app's
sub-brand accent in light **and** dark. Baselines are committed and **reviewed by a human** on first run
and on intentional change (don't let an agent bless a diff).

**Layer D — brand-semantic checks (the part static rules miss):**
- [ ] 🔵 **Token-contract drift** — a `check-token-drift` script asserts the app's copied token file matches the authoritative `.github/brands/pharos_brand/` source (checksum/diff). Guards the **copy-in** so an app can't silently fork the contract. Add to `lint-check`.
- [ ] 🟠 **Contrast / a11y** — automated **WCAG AA** assertion on the token pairs (accent↔foreground, each `--status-*`↔its `-bg`) in light + dark, via axe-core in the Playwright pass or a small token-contrast unit test. **Directly motivated**: the **rosa `#FFE0E6`** (Recepción) and **ámbar-claro `#FFB86B`** (Clientes) accents are light pastels flagged for contrast risk — this check fails the build if a sub-brand accent can't hit AA, forcing a foreground/tint fix. Threshold tuning is a human call.
- [ ] 🔵 **Font allowlist** — assert only the 4 sanctioned families (Fraunces/DM Sans/IBM Plex Mono/JetBrains Mono) are loaded; fail on a stray family.

**Sequencing of the testing itself.** Step 0 promotes the canonical gate scripts + eslint config +
Playwright scaffold + the `check-token-drift` + contrast helpers into the registry. Each app's migration
then **wires Layer A + B as its first step** (so violations are visible from the start) and **adds Layer C
+ D before its acceptance gate**. An app is not "done" until Layers A–D are green.

## Per-repo execution & done

Each owner keeps task-level detail in that repo's **`plans/*.md`** (branch off `develop`). This file
is the cross-repo coordinator. **RFC 0008 flips `accepted → implemented`** when all four apps pass the
contract + their per-app VERIFY block with **Layers A–D green** (`pnpm lint-check`, visual-regression,
token-drift, contrast, fonts) and the sub-brand applied — then update the RFC index row + Implementation
section.
