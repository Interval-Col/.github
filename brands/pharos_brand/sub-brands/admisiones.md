# Pháros · Pacientes — Admisiones sub-brand *(glyph: «Muelle» / anchor)*

> **✅ LOCKED 2026-06-17** (RFC 0008 co-creation; seeded from the brand-playground export).
> Locked facts only; deeper brand narrative is **TODO — author with @SKuger01**. Parent
> source: [`../BRAND.md`](../BRAND.md) · [`../BACKBONE.md`](../BACKBONE.md).

## 1. At a glance

```
SUB-BRAND          Pháros · Pacientes       (user-facing; glyph = Muelle/anchor)
FUNCTIONAL NAME    Pháros Admisiones        (RFC 0004 §2)
USER-FACING NAME   Pháros · Pacientes       (corregido 2026-06-18; antes «Recepción»)
MARITIME GLYPH     Muelle → anchor mark (lucide Anchor)
DESCRIPTOR         Admisiones · Recepción
PERSONA            Recepcionista · front-desk · cajero (intake, queue, lab-order, caja)
TENANCY            LCH (+ shared) — front-desk patient intake
ACCENT (LOCKED)    Rosa #FFE0E6 (light + dark)
ACCENT SPREAD      Neutro
PILOT LIGHT        #E4002B — SHARED family constant
WORDMARK           Fraunces, burgundy #782F40 — SHARED construction
```

## 2. Positioning

Front-desk patient intake / queue / lab-order — the "Pháros Admisiones" surface (RFC 0004).
**Caja lives here** (the cashier/clerk surface, RFC 0004 §2) — the supervisor cuadre stays in
the ERP (Números). The arrival metaphor (muelle/anchor — where people *come in*) fits the
front-desk role.

## 3. Visual (overrides only)

- **Accent** `--primary` = rosa `#FFE0E6`; status colours accent-independent (Q4). Being a light
  pastel, the accent reads as a soft tint — pair with strong foreground for AA contrast on text.
- **Glyph** the «Muelle» anchor mark (lucide `Anchor`) as the app icon.
- **Lockup** ver §Lockup a continuación.
- Everything else inherited unchanged from `../BRAND.md`.

### Lockup (contrato de sidebar — playground 2026-06-17)

El sidebar muestra **solo el logo Pháros** (marca compartida de la familia) y una etiqueta
descriptiva en mono. El acento de sub-marca **no** aparece como sub-nombre junto al logo.

| Elemento | Valor |
|---|---|
| Logo en sidebar | Solo logo Pháros (sin sub-nombre acento al lado) |
| Sublabel descriptivo | `Admisiones · Recepción` (IBM Plex Mono, uppercase, tracked, muted) |
| Eco en breadcrumb | Sí — «Pacientes» aparece como primer nodo del breadcrumb |
| Glyph de app | «Muelle» → `Anchor` (lucide), tintado rosa; identidad marítima vive en la marca, no en la palabra |

> Fuente: RFC 0008 Q1 · playground 2026-06-17.

> ⏸ **Tune (RFC 0008 Q6):** the rosa accent currently reuses one pastel on **both** light and
> dark grounds (no distinct dark value) — pick a legible dark variant in the playground.

## 4. Voice

Inherits the shared Pháros voice; warm + brief for a high-traffic front-desk surface.
*(TODO — refine with @SKuger01.)*

## References

- [RFC 0008 — Pháros design system](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) (Decisions 2026-06-17).
- [`README.md`](README.md) — family index · [`../BRAND.md`](../BRAND.md) — shared spec.
