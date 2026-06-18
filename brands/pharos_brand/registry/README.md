# Pháros design-system registry

The shared front-end foundation for the **Pháros product family** (`Pháros · Números`,
`Pháros · Clínico`, `Pháros · Recepción`, `Pháros · Clientes`, `Pháros · Archivo`). This is the
**single source of truth** for tokens, the frontend conventions, and per-surface
design guidance; it is distributed to each app by **copy-in**, not as a runtime
package (RFC 0008 Q3).

> Strategy & meaning: [`../BACKBONE.md`](../BACKBONE.md). How Pháros looks/sounds/
> behaves: [`../BRAND.md`](../BRAND.md). Palette origin (tenant): [`../../hematologico/LCH-BRAND.md`](../../hematologico/LCH-BRAND.md).
> The decision record this registry implements: `rfcs/0008-pharos-design-system.md`
> (the decision-walk + playground export are now its Appendix A / B).

---

## What's here

| Path | What it is |
|---|---|
| `tokens.css` | The token contract — shadcn-vue vars + accent-independent status palette + the 4-font system + the 5 LOCKED sub-brand accent themes (`.theme-*`) + `-bg` status tints + `.dark` theme. **Authoritative.** |
| `frontend-standards.md` | Nuxt 4 / Vue 3 / Tailwind v4 authoring conventions for any Pháros app (the former `instructions/nuxt-standards`, re-cut onto this contract). |
| `surfaces/*.md` | Per-surface design guidance (Finanzas/ERP, Laboratorio, Calidad, Reportes, Administración, Portal Pacientes) — the durable intent ported from the old `ds-lch-*` instructions, re-expressed on the shadcn token contract. |
| `../../../scripts/sync-pharos-registry.sh` | The copy-in sync script (skeleton) — drops `tokens.css` (and, later, components) into a consuming app. |

## How an app consumes it (copy-in)

1. Run the sync script from the consuming app, or copy `tokens.css` into the app's
   `app/assets/css/` and `@import` it from `main.css`.
2. Load the four fonts (Fraunces + DM Sans + IBM Plex Mono + JetBrains Mono) — see `frontend-standards.md`.
3. Theme by sub-brand: add the app's `.theme-*` class to `<html>` (or copy its
   accent block). A theme overrides **only** the accent slots (`--primary`, `--ring`,
   `--sidebar-primary` + their foregrounds); everything else (status palette, neutrals,
   mark constants, radius) is inherited unchanged.
4. Toggle light/dark with the shadcn **`.dark` class** on the root element.

## Decided vs open

**Decided (RFC 0008, finalized 2026-06-17) — stable contract:**
- shadcn-vue token base + **one** accent-independent status palette (`--status-{success,warning,error,info}` + `-bg`).
- **Four fonts** (Q5 re-decided 2026-06-17): Fraunces (display/wordmark) · **DM Sans** (UI/body, replaces Inter) · IBM Plex Mono (labels/mono) · **JetBrains Mono** (data figures, `tabular-nums`).
- `.dark` class theming; `cobol` theme dropped; light+dark only.
- **Sub-brand names + glyphs + accents — LOCKED Q1/Q6 2026-06-17:** the 5 accents
  live as `.theme-*` classes in `tokens.css`; an app adds its class to `<html>`.

| Sub-brand | App | Theme class | Accent light / dark |
|---|---|---|---|
| **Números** | finance-lch (ERP/finance) | `.theme-numeros` | `#7A5D00` / `#E6C34D` (ámbar — navy superseded, Q6) |
| **Clínico** | pharos-lis (lab-qc) | `.theme-clinico` | `#1B6B5A` / `#4CD1B0` (teal profundo) |
| **Deportivo** | biuman-lis | `.theme-deportivo` | `#004F70` / `#16749C` (azul) |
| **Recepción** | admission-patient | `.theme-recepcion` | `#FFE0E6` (rosa, light+dark) |
| **Clientes** | commercial-lch | `.theme-clientes` | `#FFB86B` (ámbar claro, light+dark) |

  Default/neutral (no class) = LCH Navy `#003A70` (the family-neutral / Archivo).

- **Shell character — LOCKED 2026-06-17**: Faro + Instrumento — shadcn `Sidebar collapsible="icon"` + live pilot-light health beacon + ⌘K + breadcrumb-topbar (no page H1), desktop-first.
- Charts: `@unovis` + numbered `--chart-1..5` (migration folded into `plans/pharos-fe-spec-rollout.md` → §Charts → @unovis, `.github`#43).

**Open (still to build):**
- **Step 0 of `plans/pharos-fe-spec-rollout.md` PROMOTES** the app-shell + `AppLogo`/lockup
  + live health-beacon into this registry as copy-in SFCs (plus the gate scripts / ESLint /
  lint-check / CI / pre-commit + Layer-D checks). Once promoted, those leave the open list.
- The only remaining OPEN item is the **broader curated component library** beyond
  shell/lockup/beacon — built in `design-studio` — see `plans/brand-playground-build-plan.md`.

## Tenancy

LCH and Biuman are **tenants**, not parents. A tenant never prefixes an app name
(`Pháros · Timón`, never "LCH Pháros"). The maker is **Interval · The Human Tech Co.**,
credited only in the footer/app-shell chrome (BRAND.md §10). The palette this
contract draws from is the LCH colour set (`../../hematologico/LCH-BRAND.md`).
