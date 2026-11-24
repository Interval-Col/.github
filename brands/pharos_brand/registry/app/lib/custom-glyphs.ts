// =============================================================================
// custom-glyphs.ts — nautical glyphs the Pháros family needs but lucide doesn't
// carry. Hand-drawn to lucide conventions (24×24 grid, currentColor stroke,
// width 2, round caps/joins) so they compose with the library set.
//
// Resolved CUSTOM-FIRST by the shell (layouts/default.vue resolveIcon +
// components/AppLogo.vue) — lucide names keep working unchanged. Source of
// truth for the drawings: design-studio app/lib/glyphs.ts (playground); keep
// them in sync when a new custom glyph lands there.
// =============================================================================
import { h, type FunctionalComponent } from 'vue'

// «Submarino» — Pháros · Tecnología (TI, RFC 0004 rev. 2026-07-03). Capsule
// hull + conning tower + periscope + two portholes.
const Submarine: FunctionalComponent = (props, { attrs }) =>
  h(
    'svg',
    {
      xmlns: 'http://www.w3.org/2000/svg',
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': 2,
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
      ...props,
      ...attrs,
    },
    [
      h('rect', { x: 2, y: 12, width: 18, height: 8, rx: 4 }),
      h('path', { d: 'M9 12V9h5v3' }),
      h('path', { d: 'M11 9V5h3' }),
      h('circle', { cx: 7, cy: 16, r: 0.5 }),
      h('circle', { cx: 12, cy: 16, r: 0.5 }),
    ],
  )

// «Pluma» — Consentimientos (document-signing, 2026-11-24). The lucide
// `feather` at 0.8 scale, redrawn in grid coordinates (no transform), over a
// wave that stands in for the signature line: signing on board.
const Quill: FunctionalComponent = (props, { attrs }) =>
  h(
    'svg',
    {
      xmlns: 'http://www.w3.org/2000/svg',
      width: 24,
      height: 24,
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': 2,
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
      ...props,
      ...attrs,
    },
    [
      h('path', {
        d: 'M12.736 14.6a1.6 1.6 0 0 0 1.133-.47l4.923-4.938a4.8 4.8 0 0 0-6.792-6.792L7.069 7.331A1.6 1.6 0 0 0 6.6 8.462V13.8a.8.8 0 0 0 .8.8z',
      }),
      h('path', { d: 'M15.4 5.8 4.2 17' }),
      h('path', { d: 'M16.6 11.4H9.8' }),
      h('path', { d: 'M3 21q1.5-1.5 3 0t3 0t3 0t3 0t3 0t3 0' }),
    ],
  )

export const CUSTOM_GLYPHS: Record<string, FunctionalComponent> = { Submarine, Quill }
