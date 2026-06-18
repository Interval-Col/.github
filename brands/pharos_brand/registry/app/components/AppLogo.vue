<script setup lang="ts">
// AppLogo — the canonical Pháros wordmark, inline-SVG (NOT <img src>): the brand
// mark renders the wordmark in the page's real Fraunces, and inlining is the only
// way the wordmark <text> inherits the loaded webfont (an <img>-loaded SVG is
// isolated and any @import inside it is blocked → blank glyphs).
//
// Brand rules baked in (pharos_brand/BRAND.md §2.5, RFC 0008):
//  • wordmark is ALWAYS Fraunces — never substituted, never `currentColor`;
//  • wordmark fill is the family constant burgundy (light) / white (dark) — set
//    via `fill-[var(--pharos-burgundy)] dark:fill-white`, tracking the layout's
//    class-based theme. NEVER a sub-brand accent;
//  • the pilot-light dot floats CLEAR above the "P"; its fill comes from the
//    `.pharos-pilot` class (var(--pharos-red), animated) in pharos-components.css
//    — so the <circle> carries NO inline fill (stays no-hex-gate clean);
//  • the optional sub-brand lockup (subName + glyph) uses font-mono (IBM Plex
//    Mono), uppercase + tracked — NEVER Helvetica/any stray family, NEVER the accent.
import { computed } from 'vue'
import * as lucide from 'lucide-vue-next'
import type { Component } from 'vue'

const props = withDefaults(defineProps<{
  /** `navbar` = compact wordmark (sidebar header / topbar). `icon` = the "P" +
   *  dot for the collapsed rail / favicons. `horizontal` = larger wordmark with
   *  the optional sub-brand sublabel baked into the mark. */
  variant?: 'navbar' | 'horizontal' | 'icon'
  /** Sub-brand name, e.g. "Clínico". Shown only on `horizontal` (as the SVG
   *  sublabel) — the sidebar lockup composition lives in the layout. */
  subName?: string
  /** A lucide icon NAME, e.g. "Radar", resolved dynamically. Used by the layout
   *  lockup; exposed here so callers can read the resolved glyph component. */
  glyph?: string
}>(), { variant: 'navbar' })

// Resolve the lucide glyph by name (no fixed/vendored glyph map). Falls back to
// Radar — the brief's default — when the name is missing or unknown.
const Glyph = computed<Component>(
  () => (lucide as Record<string, Component>)[props.glyph ?? ''] ?? lucide.Radar,
)
defineExpose({ Glyph })
</script>

<template>
  <!-- navbar: pilot-light beacon (.pharos-pilot — the ONE live beacon, breathes
       and quickens with system health) seated above the "P" + the Pháros wordmark. -->
  <svg
    v-if="variant === 'navbar'"
    class="h-10 w-auto"
    viewBox="0 0 145 60"
    role="img"
    aria-label="Pháros"
    fill="none"
  >
    <circle class="pharos-pilot" cx="22" cy="9.5" r="3.5" />
    <text
      x="10"
      y="44"
      font-family="Fraunces, 'Times New Roman', serif"
      font-size="36"
      letter-spacing="-0.36"
      class="fill-[var(--pharos-burgundy)] dark:fill-white"
    >Pháros</text>
  </svg>

  <!-- horizontal: larger wordmark + optional sub-brand sublabel (font-mono,
       uppercase, tracked) for apps that want the lockup baked into the mark. -->
  <svg
    v-else-if="variant === 'horizontal'"
    class="h-auto w-auto"
    viewBox="0 0 230 115"
    overflow="visible"
    role="img"
    :aria-label="subName ? `Pháros · ${subName}` : 'Pháros'"
    fill="none"
  >
    <circle class="pharos-pilot" cx="34" cy="22" r="5" />
    <text
      x="14"
      y="78"
      font-family="Fraunces, 'Times New Roman', serif"
      font-size="64"
      letter-spacing="-0.64"
      class="fill-[var(--pharos-burgundy)] dark:fill-white"
    >Pháros</text>
    <text
      v-if="subName"
      x="18"
      y="100"
      font-family="'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
      font-size="9"
      letter-spacing="0.32em"
      class="fill-[var(--muted-foreground)] uppercase"
    >{{ subName }}</text>
  </svg>

  <!-- icon (collapsed rail): pilot-light beacon seated above the "P". -->
  <svg
    v-else
    class="h-9 w-9"
    viewBox="0 0 64 64"
    role="img"
    aria-label="Pháros"
    fill="none"
  >
    <circle class="pharos-pilot" cx="32.7" cy="6.5" r="5.4" />
    <text
      x="14"
      y="56"
      font-family="Fraunces, 'Times New Roman', serif"
      font-size="56"
      letter-spacing="-0.56"
      class="fill-[var(--pharos-burgundy)] dark:fill-white"
    >P</text>
  </svg>
</template>
