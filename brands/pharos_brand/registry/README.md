# Pháros design-system registry

The shared front-end foundation for the **Pháros product family** (`Pháros · Timón`
ERP, `Pháros LIS`, `Pháros Admisiones`, `Pháros CRM`, `Pháros Archivo`). This is the
**single source of truth** for tokens, the frontend conventions, and per-surface
design guidance; it is distributed to each app by **copy-in**, not as a runtime
package (RFC 0008 Q3).

> Strategy & meaning: [`../BACKBONE.md`](../BACKBONE.md). How Pháros looks/sounds/
> behaves: [`../BRAND.md`](../BRAND.md). Palette origin (tenant): [`../../hematologico/LCH-BRAND.md`](../../hematologico/LCH-BRAND.md).
> The decision record this registry implements: `rfcs/0008-pharos-design-system.md`
> + the decision-walk `rfcs/0008-cocreation-prep.md`.

---

## What's here

| Path | What it is |
|---|---|
| `tokens.css` | The token contract — shadcn-vue vars + accent-independent status palette + the 3-font system + `.dark` theme. **Authoritative.** |
| `frontend-standards.md` | Nuxt 4 / Vue 3 / Tailwind v4 authoring conventions for any Pháros app (the former `instructions/nuxt-standards`, re-cut onto this contract). |
| `surfaces/*.md` | Per-surface design guidance (Finanzas/ERP, Laboratorio, Calidad, Reportes, Administración, Portal Pacientes) — the durable intent ported from the old `ds-lch-*` instructions, re-expressed on the shadcn token contract. |
| `../../../scripts/sync-pharos-registry.sh` | The copy-in sync script (skeleton) — drops `tokens.css` (and, later, components) into a consuming app. |

## How an app consumes it (copy-in)

1. Run the sync script from the consuming app, or copy `tokens.css` into the app's
   `app/assets/css/` and `@import` it from `main.css`.
2. Load the three fonts (Fraunces + Inter + IBM Plex Mono) — see `frontend-standards.md`.
3. Theme by sub-brand: override **only** the accent slots (`--primary`,
   `--accent`, `--ring`, `--sidebar-primary`) in a small per-app block; everything
   else (status palette, neutrals, mark constants, radius) is inherited unchanged.
4. Toggle light/dark with the shadcn **`.dark` class** on the root element.

## Decided vs open

**Decided (RFC 0008, 2026-06-13) — stable contract:**
- shadcn-vue token base + **one** accent-independent status palette (success/warning/error/info).
- Three fonts: Fraunces / Inter / IBM Plex Mono (JetBrains dropped).
- `.dark` class theming; `cobol` theme dropped; light+dark only.
- ERP · Timón accent = LCH Navy `#003A70` (+ teal success).
- Charts: `@unovis` + numbered `--chart-1..5` (migration tracked: `plans/chart-unovis-migration-plan.md`).

**Open — NOT in this foundation (for @SKuger01 / the brand playground, RFC 0008 Q1/Q6):**
- Non-ERP sub-brand **accents** (LIS clínico, LIS deportivo, Admisiones, CRM, Archivo).
- Sub-brand **names** beyond `Timón`.
- Shell **character** ("Faro + Instrumento" candidate).
- The **component library** itself (Vue SFCs). This registry currently ships the
  *token + convention + surface-guidance* foundation; the shadcn-vue component
  build is the tracked Phase-1 follow-up — see `plans/brand-playground-build-plan.md`.

## Tenancy

LCH and Biuman are **tenants**, not parents. A tenant never prefixes an app name
(`Pháros · Timón`, never "LCH Pháros"). The maker is **Interval · The Human Tech Co.**,
credited only in the footer/app-shell chrome (BRAND.md §10). The palette this
contract draws from is the LCH colour set (`../../hematologico/LCH-BRAND.md`).
