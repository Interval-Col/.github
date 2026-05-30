# Pháros · Timón — ERP sub-brand

> **⚠️ PRELIMINARY.** This is a starting point for the ERP sub-brand,
> authored 2026-05-30. The endorsed sub-brand model, the family naming
> theme, the per-app accent allocation, and the evocative-vs-functional
> naming reconciliation are all still **open questions in [RFC 0008]**
> (Pháros design system) and will be walked in the @gczuluaga + @SKuger01
> co-creation session. Treat the **name "Timón"** and the **navy accent**
> as the working proposal, not a locked decision. Update once RFC 0008 is
> consolidated.
>
> Parent brand source: [`../BRAND.md`](../BRAND.md) ·
> [`../BACKBONE.md`](../BACKBONE.md). This doc only specifies what the ERP
> sub-brand *adds to* or *overrides in* the shared Pháros foundation.

---

## 1. At a glance

```
SUB-BRAND          Pháros · Timón
REPLACES           "Pulso" (finance-lch) — the retired per-app name
FUNCTIONAL NAME    Pháros ERP            (RFC 0004 §1)
EVOCATIVE NAME     Pháros · Timón        (RFC 0008 endorsed sub-brand)
DESCRIPTOR         ERP · Finanzas y Operaciones
PERSONA            Contador · COO · jefe de operaciones (the operator who
                   runs the whole holding from one place)
TENANCY            Multi-tenant (LCH + Biuman + future members) — RFC 0004 §3
ACCENT (proposed)  LCH Navy #003A70  (draws ONE colour from the family palette)
PILOT LIGHT        #E4002B  — SHARED across the family (the constant; never re-tinted)
WORDMARK           Fraunces, burgundy #782F40 — SHARED construction
```

The sub-brand is mechanically a **theme** of the shared Pháros contract
(RFC 0008 §1–2): same type, same app-shell, same pilot-light + wordmark
construction, same voice — it differs only in **accent colour, sub-name,
and icon tint**.

---

## 2. The name — why "Timón"

**Meaning.** The *timón* is the helm — the single station from which you
govern the entire vessel. That is exactly what an ERP is: the place from
which the operator steers the whole operation (caja, pagadores, tarifas,
órdenes, facturas, notas crédito, DIAN/Siigo export, reportes), not one
ledger among many.

**Why it fits the family.** In an endorsed sub-brand, the child must play a
**different role in the same world** as the parent — not duplicate it.
Pháros (the lighthouse) **guides from outside**; Timón (the helm) is where
you **govern from inside**. Complementary, not competing. This is the test
that disqualified the obvious alternatives: *Brújula* and *Norte* both died
because the lighthouse is *already* the guidance instrument — a second
"which way?" device competes with the parent.

**Why it reads ERP, not accounting.** "Tomar el timón / llevar el timón de
la operación" is live Spanish idiom for *taking command of everything that
moves*. It cannot be read as a passive ledger — which is precisely why it
beats accounting-flavored candidates (*Cuentas, Números, Balanza*) on the
scope criterion.

**Selection provenance.** Chosen over ~50 candidates across three
adversarial naming rounds (any-length, short-nautical, natural-regional).
Timón was the **only** name that topped its round *and* survived adversarial
refutation with merely a *minor* objection. The short-nautical and
natural-regional lanes produced no clean winner:

- *Short-nautical* — every finalist failed: **Popa** (= trasero, paisa slang),
  **Proa** (duplicates the lighthouse's guide role), **Motor** (generic
  tech cliché / reads as an internal component), **Quilla** (not actually
  shorter; invisible/passive), **Ancla** ("anclar" = to stop/fix — contradicts
  *steer & move the operation*).
- *Natural-regional* — a collision minefield **because the product is
  Colombian**: **Savia** = Savia Salud EPS (a *payer* the ERP bills daily),
  **Ceiba** = Ceiba Software (a Medellín software firm), **Páramo** = an
  outdoor-clothing brand + politically charged. **Cauce** duplicated the
  lighthouse again.

**The one honest objection to Timón (minor).** A monolingual paisa speaker
hears *timón* first as the **car steering wheel** (volante), not the ship's
helm. This does **not** weaken the meaning — "gobernar la operación" holds
whether the image is a wheel or a helm — it only softens the maritime rhyme
with the lighthouse. Accepted as a known cost.

---

## 3. Positioning & scope

Pháros · Timón is the **operational backbone of the holding** — one
multi-tenant instance serving LCH, Biuman, and future members (RFC 0004 §3).
It owns finance + accounting + the operational surfaces that hang off them.

It is **not** an accounting-only tool. The accounting domain (AR, caja,
pagadores, tarifas, órdenes, facturas, notas crédito, Siigo/DIAN) is the
core, but the brand promise is *running the operation*, not *keeping the
books*. The cashier (caja) surface for clerks lives in **Pháros Admisiones**
per the RFC 0004 §2 revision; Timón keeps the **supervisor** surface
(conciliar / reabrir / ver todas las cajas) and the entity, rules, and
cuadre.

---

## 4. Visual

Everything not listed here is **inherited unchanged** from
[`../BRAND.md`](../BRAND.md) (type scale, spacing, radius, flatness,
iconography, layout).

### 4.1 Accent colour (proposed — pending RFC 0008 open-q #6)

| Token | Hex | Role in Timón |
|---|---|---|
| `--accent` (primary) | **`#003A70`** LCH Navy | Primary actions, active nav, links, focus on data surfaces |
| `--accent-secondary` | `#A0D1CA` LCH Teal | "En cuadre / conciliado" success state — aligns with finance-lch's existing `--status-success` token |
| `--pilot-light` | `#E4002B` | **SHARED, not overridden** — the family constant (focus dot, critical) |

**Why navy.** It is the calmest, most data-dense member of the family
palette — right for an ERP of tabular finance/ops data — and it carries the
maritime undertone of the name (deep water, the sea you steer across)
without shouting it. One accent, drawn from the curated family set, so
Timón stays a sibling of QC (burgundy/red), LIS, CRM by construction.

### 4.2 Lockup

`Pháros` (Fraunces, burgundy `#782F40`) + red pilot-light dot over the `P`
+ separator `·` + `Timón` (sub-name) + optional sublabel
`ERP · FINANZAS Y OPERACIONES` (IBM Plex Mono, uppercase, tracked, muted).
The separator (`·` vs `—`) is RFC 0008 open-q #1 — using `·` provisionally.

### 4.3 Icon

Shared Pháros mark (`P` + pilot light), **navy tint**. No new icon shape —
differentiation is tint only (RFC 0008 §1). A subtle helm/ship's-wheel
motif is noted as a *possible* future exploration but is **out of scope**
for the preliminary mark; do not build it until RFC 0008 locks the icon
approach.

---

## 5. Voice

Inherits the shared Pháros voice unchanged: **Spanish-first, technically
precise, humanly warm, never alarmist** (see [`../BACKBONE.md`](../BACKBONE.md)
§7 and [`../BRAND.md`](../BRAND.md) §5).

Domain note for the ERP surface: the register is that of correct **Colombian
accounting practice** — arqueo, base, cuadre, conciliación, retenciones,
DIAN/UVT. Numbers are stated plainly and exactly (tabular-nums, JetBrains
Mono per the parent type system); error and validation copy names the
contable reality precisely rather than softening it. Trust comes from
accuracy, not reassurance.

---

## 6. Tagline & copy (drafts — for co-creation)

- **Descriptor (safe):** *Finanzas y Operaciones*
- **Evocative line (draft):** *Desde el timón se gobierna la operación.*
- **Slogan candidates (draft):** *"El mando de la operación." · "Una sola
  mano al timón."*

These are drafts only; finalize in the RFC 0008 session alongside the
sibling sub-names.

---

## 7. Relationship to the family — the open theme question

The two strongest names in the exploration (Timón, Rumbo) were **nautical**,
and they won *because* they rhyme with the lighthouse. That surfaces a
family-level decision that is **deliberately left open**:

- **Maritime family** — Timón anchors a nautical naming system; siblings
  (Admisiones, etc.) could follow (e.g. a dock/port for arrivals). Maximum
  cohesion with Pháros, but commits the whole portfolio.
- **"Nature that orients & sustains" family** — looser: the lighthouse is
  the *coastal* member of a wider natural world (mountain, river, tree).
  More semi-neutral, but the natural-regional lane proved a collision
  minefield for a Colombian product (§2).
- **Abstract family** — siblings stay abstract (Lab, Gente, Números); Timón
  becomes a maritime outlier.

**Do not decide this here.** It is **RFC 0008 open-question #1** and feeds
back into RFC 0004's functional names. Timón works in all three framings;
only its degree of family-rhyme changes.

---

## 8. Pending RFC 0008 (what can still change)

| Item | This doc's working assumption | RFC 0008 ref |
|---|---|---|
| Sub-name | **Timón** | open-q #1 |
| Family naming theme | undecided (maritime / nature / abstract) | open-q #1, §7 above |
| Separator | `·` | open-q #1 |
| Evocative vs functional ("Timón" vs "ERP") reconciliation | both shown; lockup uses evocative + functional sublabel | open-q #2 |
| Accent allocation | Navy `#003A70` | open-q #6 |
| Token-contract base | inherit shared contract (shadcn vars) | open-q #4 |
| Dark / `cobol` theme | inherit family decision | open-q #7 |

> Note: the existing [`../BRAND.md`](../BRAND.md) / [`../BACKBONE.md`](../BACKBONE.md)
> predate RFC 0004 and still describe Pharos as *the QC module of LCH*
> rather than the umbrella brand. That reconciliation is its own task and
> is **not** done here — this doc follows the RFC 0004 / 0008 umbrella model
> (Pháros = family; Timón = the ERP sub-brand).

## References

- [RFC 0004 — Pháros product portfolio][RFC 0004] — umbrella brand, functional app names, multi-tenancy.
- [RFC 0008 — Pháros design system][RFC 0008] — endorsed sub-brand model, open questions this doc tracks.
- [`../BRAND.md`](../BRAND.md) — shared brand source (type, colour, components, voice).
- [`../BACKBONE.md`](../BACKBONE.md) — shared brand strategy.

[RFC 0004]: https://github.com/Interval-Col/rfcs/blob/main/0004-pharos-product-portfolio.md
[RFC 0008]: https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md
