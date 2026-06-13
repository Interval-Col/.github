---
status: blocked
created: 2026-06-13
owner: gczuluaga
tracking-issue: Interval-Col/.github#25
blocked-on: RFC 0008 acceptance + Phase 1 foundation (shared chart tokens + components)
---

# Charting migration → @unovis (org standard)

Per **RFC 0008 Q11** (decided 2026-06-13): **`@unovis` is the shared charting
standard for all Pháros apps**, and the shared **chart-token shape is numbered
`--chart-1..5`** (brand-colored from the family palette — it's shadcn-vue's
native chart-token convention; shadcn-vue's chart components are themselves built
on @unovis). This plan migrates the apps currently hand-building on **Chart.js**
off it.

Why @unovis (diligence summary): F5-backed and **dogfooded as F5 Distributed
Cloud's own viz engine** (strong maintenance incentive), v1.6.5 (Apr 2026),
**Apache-2.0**, SVG + **CSS-variable-native** (charts obey the token cascade like
every other component, unlike Chart.js's canvas which needs a manual JS bridge),
and consumed **copy-in** via the shadcn-vue registry → you own the source, never
trapped (the alexandria lesson). SVG perf is fine at LCH's chart scale
(hundreds–low-thousands of points).

## Gating

Do **not** start app migrations until: (1) RFC 0008 is accepted, and (2) the
Phase-1 foundation exists — the shared `--chart-1..5` tokens are defined in the
token contract and the shared chart components are in the registry. Charts are
**prototyped + validated in the brand playground** (RFC 0008 Q5 artifact) first.

## Inventory (apps on Chart.js today)

| App | Chart surfaces | Library today | Risk |
|---|---|---|---|
| **finance-lch** | `KpiCard`, `KpiTrendModal` (dashboards) | `chart.js ^4.5.1` + `vue-chartjs ^5.3.3` | Low–medium — standard KPI/trend charts |
| **lab-qc** | media-móvil, correlación, **CLSI-EP15**, Levey-Jennings-style QC charts | `chart.js ^4.4.1` | **High** — statistically specialized; needs output parity |

*(admission-patient + biuman-lis have no significant chart surfaces today — they
adopt @unovis natively when they build charts.)*

## Phases

### Phase 0 — Foundation (in the registry, gated above)
- [ ] Define `--chart-1..5` in the shared token contract, colored from the
      family palette; document semantic chart-token *extensions* for domains
      that need them (e.g. lab-qc QC charts).
- [ ] Add the shared @unovis-based chart components to the registry
      (area/bar/line/donut + legend/tooltip), prototyped in the playground.
- [ ] Wire Q9 visual-regression snapshots for the shared chart components.

### Phase 1 — finance-lch (lower risk first)
- [ ] Port `KpiCard` + `KpiTrendModal` to the shared @unovis components.
- [ ] Replace `getChartPalette()` JS-bridge with token-native CSS-var theming.
- [ ] Remove `chart.js` + `vue-chartjs` deps once no surface uses them.
- [ ] Visual + behavioral parity check against the current dashboards.

### Phase 2 — lab-qc (specialized, port carefully)
- [ ] Port the QC charts (media-móvil, correlación, CLSI-EP15, Levey-Jennings).
      Treat these as **statistical-parity** ports: verify the rendered
      statistics (control limits, regression, EP15 bands) match the current
      Chart.js output exactly — not just visual likeness.
- [ ] Keep lab-qc's semantic chart tokens as per-app extensions if the QC charts
      read them at runtime; map onto the shared base where possible.
- [ ] Remove `chart.js` once all QC surfaces are ported.

## Risks
- **Statistical-chart parity (lab-qc)** — the QC charts encode clinical
  statistics; a port that looks right but computes/renders bands wrong is a
  correctness bug. Gate Phase 2 on parity verification, not eyeballing.
- **Thinner community** than Chart.js — fewer SO answers; budget learning time.
- **Scope** — this widens the design system into data-viz (a maintenance
  surface). Courtesy-ratified with @SKuger01 alongside RFC 0008.

## References
- RFC 0008 Q11 + `rfcs/0008-cocreation-prep.md`.
- shadcn-vue charts (built on @unovis): <https://www.shadcn-vue.com/charts>.
- @unovis: <https://unovis.dev/> · <https://github.com/f5/unovis> (Apache-2.0).
