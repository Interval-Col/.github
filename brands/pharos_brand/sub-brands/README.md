# Pháros sub-brands — family index

> **Locked 2026-06-17** (RFC 0008 co-creation, @gczuluaga + @SKuger01; seeded from the
> `design-studio` brand-playground export). The five apps that carry a **full endorsed
> sub-brand** (user-facing name + nautical glyph + family accent). Naming model: **semi-
> functional name + a nautical glyph** — the maritime identity lives in the *logo*, not the
> word, so names stay legible to clinicians / front-desk / athletes. Separator `·`.

| Functional (RFC 0004) | Spec | User-facing name | Glyph (náutico → lucide) | Accent — light / dark | Spread | Descriptor |
|---|---|---|---|---|---|---|
| ERP | [`erp.md`](erp.md) | **Números** | Timón → `ShipWheel` | `#7A5D00` / `#E6C34D` (ámbar) | Sutil | ERP · Finanzas y operaciones |
| LIS clínico (LCH) | [`lis-clinico.md`](lis-clinico.md) | **Clínico** | Sonda → `Radar` | `#1B6B5A` / `#4CD1B0` (teal prof.) | Neutro | LIS · Laboratorio clínico |
| LIS deportivo (Biuman) | [`lis-deportivo.md`](lis-deportivo.md) | **Deportivo** | Vela → `Sailboat` | `#004F70` / `#16749C` (azul prof.) | Neutro | LIS · Laboratorio deportivo |
| Admisiones | [`admisiones.md`](admisiones.md) | **Recepción** | Muelle → `Anchor` | `#FFE0E6` (rosa) | Neutro | Admisiones · Recepción |
| CRM | [`crm.md`](crm.md) | **Clientes** | Catalejo → `Telescope` | `#FFB86B` (ámbar claro) | Sutil | CRM · Relaciones comerciales |

## Family constants (shared — never a sub-brand accent)

- **Wordmark** `Pháros` — Fraunces, burgundy `#782F40` (never re-tinted per app).
- **Pilot light** `#E4002B` — the red beacon over the `P` (focus dot / critical).
- **Type** — Fraunces (display) · DM Sans (UI) · IBM Plex Mono (labels) · JetBrains Mono
  (data figures). **Status palette** (success/warning/error/info) is accent-INDEPENDENT
  (RFC 0008 Q4) — it does not move when an app re-accents.
- **Shell** — the shared app-shell ("Faro + Instrumento": beacon rail + ⌘K, live pilot-light
  system-health beacon). **Themes** — light + dark (`.dark`); no cobol.

## Not full sub-brands

- **QC** — folded into LIS (RFC 0004 §2); its burgundy/red survives as the LIS **state**
  palette, not a sibling accent.
- **Caja** — a surface inside Admisiones.
- **Pháros Archivo** — utility tier: shared shell + a neutral family accent, no evocative name.
- **`nucleus-db`** — infrastructure, never branded.

## Notes

- These specs record the **locked facts** (name, glyph, accent, descriptor) from the 06-17
  walk. The deeper brand narrative per sibling (naming rationale, voice nuance, taglines) is
  marked **TODO — author with @SKuger01**; only `erp.md` carries the full rationale today
  (it predates the walk and was reconciled in place).
- Source of truth for shared visual/voice spec: [`../BRAND.md`](../BRAND.md) ·
  [`../BACKBONE.md`](../BACKBONE.md). Decisions: [RFC 0008][rfc0008] (Decisions 2026-06-17).

[rfc0008]: https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md
