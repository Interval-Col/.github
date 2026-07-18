---
description: Build a house deck (didactic or executive-brand) following the guides in operations/guides/decks.md — audience-first, brand-canonical, animated, stored as a regenerable recipe. Content language follows the audience (usually Spanish).
---

# /deck — construir un deck de la casa

You are building a presentation following the house deck methodology.
**Read `operations/guides/decks.md` (the type index) first**, then the
guide for the chosen type. Never invent brand values — everything visual
comes from `.github/brands/` (manuals, `tokens.css` LOCKED accents,
registry glyphs/components).

Optional argument: `$ARGUMENTS` is a topic hint (e.g. `pitch sistema
documental a liderazgo del lab`). If empty, derive from the session.

## 1 · Tipo y audiencia (AskUserQuestion, recommendation-first)

- **Tipo** — from the `decks.md` index: *didáctico técnico*
  (`decks-didacticos.md`) or *ejecutivo de marca* (`decks-ejecutivos.md`).
  Recommend from the audience: equipo de ingeniería → didáctico;
  liderazgo de dominio que debe aprobar algo → ejecutivo.
- **Audiencia con nombre propio** — who exactly attends, role by role.
  For executive decks each leader gets a slide and the decision gate is
  handed explicitly to whoever owns it.
- **Marca protagonista** — which brand leads (LCH/Biuman/…); Pháros is
  the credit, never the protagonist, on domain-facing decks.

## 2 · Construir

Follow the chosen guide. Non-negotiables from both:

- Self-contained single HTML (fonts as data-URI — brand font embedded,
  raw OTF base64 works without fonttools), light+dark, `@media print`,
  `prefers-reduced-motion` → full static (default state = final state).
- Publish as a private **Artifact and iterate on the SAME URL** with
  version labels; the owner reviews live.
- **Layout/typography changes go through ASCII wireframes via
  AskUserQuestion BEFORE any rework** — never reprocess blindly.
- **Density pass**: every slide fits ~900px viewport height (projectors).
- Executive decks: end with the **guion del presentador** (1 anchor line
  + 1 stage note per slide) once the slide order is stable.

## 3 · Guardar como código (nunca como binario)

- The deck lives in **its content-owner's repo** (readers decide the
  repo — `como-trabajamos.md`): built HTML (generated view) +
  `build/` with `template.html` (placeholders), `brand-fonts-all.css`
  (with provenance notes) and `build.py`. Verify the round-trip
  regenerates byte-identical before committing.
- Reference implementation: `lch-kb/fase-0/` + `lch-kb/fase-0/build/`.
- If the deck taught a new reusable pattern, propose updating the type's
  guide (PR to `operations`) — the guide is the durable knowledge, the
  deck is the ejemplar.
