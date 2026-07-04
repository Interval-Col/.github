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

export const CUSTOM_GLYPHS: Record<string, FunctionalComponent> = { Submarine }
