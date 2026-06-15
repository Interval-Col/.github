# Interval — brand evaluation & the intuition it gives Pháros

> **Reference doc** (not a plan — no status field; edited in place).
> Captured **2026-06-14** during the brand-doc umbrella reconciliation
> (issue `Interval-Col/.github#24`, RFC 0008 Q10). `INTERVAL-BRAND.md` is the
> *spec*; this is the *assessment* — an evaluation of the Interval house brand
> and the transferable brand-intuition it gives the **Pháros** product family.
> Forward-looking input for the still-open sub-brand **names + accent
> allocation** (RFC 0008 Q1/Q6) and the **brand playground** (Q5).

---

## 1. Interval — the evaluation

**Essence (one line).** Interval is a black-first, near-silent studio brand built
on a single idea — *the interval*: the gap, the pause, the space between, made
visible — rooted in **Wu Wei** ("no forzar"). Its thesis: technology's job is to
cover the fronts and give time back, so people spend it *viviendo, sintiendo,
pensando*. It whispers instead of shouts.

### What makes it work (distinctive devices)
- **The broken/segmented logotype where the gaps *are* the letters.** Custom
  mono-width artwork (never a font); the negative gaps complete each glyph in the
  eye, so the name *enacts* its meaning. The single most ownable, hard-to-copy asset.
- **The `[ ]` interval brackets framing pure void** — the thesis as a scalable
  mark; the bracket notch rhymes with the i-bar of the logotype, tying mark to wordmark.
- **Black canvas (`#121010`) as the *default*, not an option** — inverts the SaaS
  light-default to signal premium calm.
- **One rare orange flare (UT Naranja `#FF8010`)** carrying all the energy against
  an otherwise monochrome field; its *rarity* is the whole point.
- **"Espacio vital" — negative space as a *named*, load-bearing asset**, with
  clear-space rules and spacing tokens, not leftover room.
- **Grotesque pairing** (Pragmatica Cond + Avenue X) that recedes so space and the
  single accent can speak.
- **Bilingual rhythm** — Spanish carries the soul/manifesto, English the crisp claims.
- **Wu Wei as the organizing belief** — turns minimalism into conviction, not fashion.

### Real strengths
Exceptional conceptual integrity (one idea drives logotype, icon, palette, spacing,
copy); a genuinely defensible custom mark; restraint-as-competitive-signal in a
category drowning in glow; **enforceable, code-ready rules** (min sizes, clear-space,
"one accent per view"); emotionally differentiated anti-burnout positioning; and —
most relevant to us — a **clean maker/product/tenant brand architecture** (§10 keeps
Interval the *house* separate from the product/tenant brands: "the product brand wins
on its own screens").

### Honest gaps (so Pháros doesn't inherit them)
- **Color section unfinished**: §4 itself flags the two-accent CMYK as
  "transposed/atypical" and ships it anyway. No WCAG posture; indigo `#261277` on
  black fails contrast.
- **The signature logotype has zero construction spec** — no grid, stroke-to-gap
  ratio, or module unit. Undocumented artwork can't be reproduced or extended.
- **Orphaned min-sizes table** (rows 1–5 vs three defined logo versions, no legend)
  — the most safety-critical reproduction rule is unusable as written.
- **Fonts are unobtainable**; the documented type is rarely what renders (fallbacks
  change the brand) and the book never flags the risk.
- **No worked application examples** — "one accent per view" / "space as asset" are
  slogans with nothing to calibrate against.
- **Provenance TODO unfilled** ("‹set when filed›") for the only true-vector master.
- **"Human/warm" claim never reconciled with a cold, brutalist-futurist look** —
  the visuals argue against the words.

### Verdict
A small in-house studio made itself look *senior* through ruthless conceptual
discipline — and left execution incomplete in exactly the places where rigor is
hardest (color, mark construction, accessibility, worked examples). The
**transferable gold is the *method and architecture*** (anchor to one idea, let every
decision ladder back, make rules code-enforceable, keep maker/product/tenant
separate) — **not a single pixel** of the black canvas, orange, brackets, or
segmented glyphs.

---

## 2. The intuition this gives Pháros

### Lean into (Interval *validates* the locked Pháros decisions — the *why* behind them)
1. **One defensible idea, laddered everywhere.** Wu Wei is Interval's spine; the
   **lighthouse / helm (maritime)** is Pháros's. "How would a lighthouse behave?"
   (guidance, a fixed point, signal-in-the-dark, safe passage) is the test for every
   umbrella decision — which is why the BACKBONE's lighthouse soul became the
   *family* soul, not a QC-only metaphor.
2. **A constant core mark + a single accent that carries energy.** Interval =
   monochrome + one rare orange. Pháros = the untouchable Fraunces "Pháros" wordmark
   (burgundy `#782F40` + red `#E4002B` pilot dot, **never re-tinted per app**) +
   exactly **one** sub-brand accent per surface (ERP = navy `#003A70`). Borrow the
   *discipline* ("one accent, used rarely, against a calm field"), never the orange.
3. **Calm / whitespace as a *named*, load-bearing asset.** Interval names it
   "espacio vital." In a clinical LIS this is *strategic* (reduces cognitive load and
   error for a tired tech), not just stylistic — make flatness/whitespace explicit
   doctrine with measurable tokens.
4. **Rules enforceable in code.** Mirror Interval's rigor: shadcn-vue token base,
   accent-independent status palette, the 3-font system as concrete vars, and "mark
   never re-tinted / `.dark`-class theming only / one accent per app" written as
   lint-able constraints, not prose.
5. **Explicit maker ↔ product ↔ tenant architecture (who-wins-when).** Interval §10
   is the rule Pháros codified in BRAND.md §10: Interval is only the *maker*
   (footers/repos, "Hecho por Interval"); Pháros is the umbrella; LCH/Biuman are
   tenants that never prefix an app name; the product brand wins on its own screens.
6. **A naming *system*, not a per-name debate.** A maritime lexicon pre-decides the
   still-open sub-brand names so each new one feels inevitable; record every
   evocative↔functional mapping in RFC 0004 (only `Pháros · Timón` locked so far).

### Keep strictly separate (do NOT let any of this leak into Pháros)
- **Express calm in the *opposite* idiom.** Interval = black-first; Pháros =
  **light/dark only, airy, low-glare**. Same value (calm-as-asset), inverted
  execution — a dark canvas would *fight* Pháros's own restraint and harm QC-data
  legibility on long shifts.
- **No UT Naranja, no Persian Indigo.** Orange would read as a warning and collide
  with the QC status layer (drift `#FBD872`); a deep blue/violet would muddy the
  meaning-bearing navy `#003A70` / teal data palette.
- **No segmented logotype / `[ ]` brackets** in product UI — studio identity, used
  only in the small "Hecho por Interval" maker credit.
- **No all-caps condensed grotesque headlines.** Pháros's display voice is Fraunces
  (warm serif); the rule is "headlines never ALL CAPS — weight contrast instead."
  All-caps + mono tracking stays reserved for tiny IBM Plex Mono labels.
- **No English marketing claims in product UI** — Pháros is Spanish-first clinical
  copy; English is a quiet secondary in the same register.
- **Don't inherit Interval's documented gaps** — Pháros *does* fix color/token
  provenance, *does* keep a WCAG/contrast posture in the status layer, and *does*
  keep worked component examples (BRAND.md already does).

### The shared DNA (why one studio can legitimately make both)
Restraint, whitespace-as-asset, calm-over-urgency, attention-stewardship, human
warmth, and flatness/anti-ornament are *genuinely shared ethic* — expressed through
**opposite visual means**: Interval = cold-futurist visuals + human copy; Pháros =
warm-serif visuals + warm copy. That shared ethic is why the BRAND/BACKBONE
reconciliation was **light and surgical, not a rebrand**.

---

## See also
- `INTERVAL-BRAND.md` — the Interval house-brand spec (esp. §10, maker/product/tenant).
- `../pharos_brand/BRAND.md` — the Pháros shared spec (mark, palette, type, §10 architecture, maker credit).
- `../pharos_brand/BACKBONE.md` — the Pháros family soul (lighthouse → maritime).
- RFC 0008 — Pháros design system (open: Q1 names, Q5 playground, Q6 accents).
