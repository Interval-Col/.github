---
status: done
created: 2026-06-13
completed: 2026-06-14
owner: gczuluaga
tracking-issue: Interval-Col/.github#24
---

> **DONE (2026-06-14)** — merged to `main` in [#30](https://github.com/Interval-Col/.github/pull/30); issue #24 closed. The only remainder is the non-blocking, separately-gated app-chrome remake (e.g. lab-qc `PharosLogo`), which folds into the full logo remake once sub-brand names/accents lock (RFC 0008); lab-qc#8 was closed.
>
> **Phase 1 + 2 (the writing work).** `BRAND.md`, `BACKBONE.md`, `BACKBONE.es.md`
> reconciled to the umbrella model (+ `sub-brands/erp.md` JetBrains→IBM Plex Mono
> fix and its now-stale "not done" note). Folded the 2026-06-13 walk: Interval =
> LCH's in-house maker, LCH · Biuman = tenants; ERP = `Pháros · Timón` (Navy +
> teal); maritime theme + lighthouse→Timón soul bridge; `·` separator; 3-font
> system (JetBrains dropped); light/dark only via `.dark`; accent-independent
> status palette; QC = LIS state palette; Archivo = utility; `nucleus-db` never
> branded. Shared brand SVGs also cleaned (QC sublabel + off-system Helvetica
> removed, pilot-dot proportion fixed, `@import` XML ampersand escaped). The
> app-chrome remake (e.g. lab-qc `PharosLogo`) remains as the non-blocking
> follow-up; lab-qc#8 was closed (folded into the gated remake).

# Brand-doc reconciliation → Pháros umbrella model

Reconcile the canonical brand docs (`brands/pharos_brand/BRAND.md`,
`BACKBONE.md`, `BACKBONE.es.md`) from the **pre-RFC-0004** framing
("Pháros = the QC module of LCH", no accent, sub-brand *of LCH*) to the
**umbrella** model the org has since adopted: **Pháros = parent family**;
**ERP / LIS / Admisiones / CRM = endorsed sub-brands** (accent + evocative
name + icon); **QC = surfaces *inside* LIS** (its burgundy/red is a *state*
palette, not a sibling accent); **Archivo = utility tier** (neutral family
accent, no evocative name); **`nucleus-db` is never branded**.

Spun out of the **RFC 0008 co-creation walk (Q10)** so the session stays on
live design calls. The *direction* is already locked (RFC 0004 rev. 2026-06-04
+ RFC 0008 decisions 2026-06-10 + the 2026-06-13 walk) — this plan is the
**writing work**, not a debate.

## Locked inputs to fold in (from the 2026-06-13 walk)

- **ERP = `Pháros · Timón`** — LCH Navy `#003A70` accent + teal `#A0D1CA`
  success; maritime family theme; `·` separator.
- **Type:** 3-font system — Fraunces (display/wordmark), Inter (sans UI),
  IBM Plex Mono (data/labels). No per-app fonts.
- **Theming:** `.dark` class mechanism; **light/dark only** — the `cobol`
  theme is dropped.
- **Tokens:** shadcn-vue base + an accent-**independent** status palette
  (success/warning/error/info); QC burgundy/red lives in that status layer
  for LIS.
- Evocative↔functional name mapping is being recorded in **RFC 0004** (RFC
  0008 Q2); only **ERP↔Timón** is named so far — the other sibling names are
  still open (Q1, → SKuger).

## Phases

### Phase 1 — `BRAND.md` (visual/voice spec)
- [x] Reframe the opening: Pháros = umbrella family, not "the QC module of LCH".
- [x] Brand architecture section (§10): parent + endorsed sub-brands; the
      shared-vs-differentiated split (shared: type, app-shell, spacing/radius/
      flatness, mark + wordmark, voice, token-contract *names*, gates;
      differentiated: accent value, sub-name, icon tint).
- [x] Record the curated family palette + that each sub-brand draws ONE accent;
      seed ERP = Navy `#003A70`.
- [x] QC: describe burgundy/red as the LIS **state** palette
      (en-control / fuera-de-control / alerta), explicitly **not** a sibling
      accent.
- [x] Archivo = utility tier (neutral accent, no evocative name);
      `nucleus-db` never branded.
- [x] Type section → 3 families (drop the 2nd mono). Theming → light/dark only.

### Phase 2 — `BACKBONE.md` + `BACKBONE.es.md` (strategy)
- [x] Same umbrella reconciliation in both language strategy docs (light
      generalization — soul kept near-verbatim; lighthouse→Timón bridge added).
- [x] Keep `.es.md` and `.md` in sync (neutral-Colombian Spanish for `.es.md`).

### Phase 3 — Downstream chrome (non-blocking)
- [x] Shared brand SVGs cleaned here: horizontal mark drops the
      "CONTROL DE CALIDAD" sublabel + the off-system Helvetica face; pilot dot
      rescaled to the navbar dot:P ratio (horizontal + icon); `@import`
      ampersand XML-escaped across all six.
- [ ] App chrome (e.g. lab-qc `PharosLogo`: accent "Pharos"→"Pháros", drop the
      QC sublabel, Helvetica→IBM Plex Mono) re-syncs with the full logo remake
      (RFC 0008 Implementation §). Not separately tracked — lab-qc#8 closed.

## Out of scope
- The evocative names for the non-ERP siblings (open — RFC 0008 Q1, → SKuger).
- The full per-app UI brand remake (gated on RFC 0008 acceptance + locked
  names/accents — see RFC 0008 Implementation §).

## References
- RFC 0008 (cocreation branch `docs/rfc-0008-cocreation-2026-06-10`) +
  `rfcs/0008-cocreation-prep.md` (Q10).
- RFC 0004 — portfolio + functional names; evocative↔functional mapping table
  (RFC 0008 Q2).
- `brands/pharos_brand/sub-brands/erp.md` — already umbrella-model (`Pháros ·
  Timón`).
