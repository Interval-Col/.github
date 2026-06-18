<script setup lang="ts">
// "Oleaje" — the calm ukiyo-e sea at the foot of the sidebar that the lighthouse
// rises from (BRAND / RFC 0008 family decision: oleaje sí · altura Medio · tinte
// Acento · espuma sí · barco sí). A whisper, never the Great Wave: monochrome
// line-art at low opacity, slow drift, an occasional little boat ("the light that
// lets every ship come home").
//
// DECOUPLED from the design-studio playground store: the locked config is baked
// in (medium swell, accent tint, foam + boat on). Sea-state follows the system
// health beacon via <html data-status> (set by the health-beacon plugin) — calm
// at "ok", quickening on "drift"/"out" — wired purely in CSS (pharos-components.css).
// The boat sits BETWEEN the back and front swells so the front crests lap in front
// of its hull; layers tile every 50% (w-200% → translateX -50%) to loop seamlessly.
</script>

<template>
  <div
    class="pharos-ocean pointer-events-none absolute inset-x-0 bottom-0 z-0 overflow-hidden"
    aria-hidden="true"
  >
    <!-- back swell -->
    <svg class="ocean-layer ocean-back absolute inset-0 h-full w-[200%]" preserveAspectRatio="none" viewBox="0 0 240 40" fill="currentColor">
      <path d="M0 27 q30 -5 60 0 t60 0 t60 0 t60 0 L240 40 L0 40 Z" opacity="0.06" />
    </svg>

    <!-- the little boat, sitting at the waterline (front waves lap in front of it) -->
    <div class="pharos-boat absolute" style="top: 36%">
      <svg class="pharos-boat-hull" width="22" height="16" viewBox="0 0 22 16" fill="currentColor">
        <path d="M2 9 Q11 14 20 9 L18 12 Q11 15 4 12 Z" opacity="0.5" />
        <path d="M11 9 L11 2 L5.5 8 Z" opacity="0.5" />
        <line x1="11" y1="9" x2="11" y2="1.5" stroke="currentColor" stroke-width="0.8" opacity="0.5" />
      </svg>
    </div>

    <!-- front swell + crest (drawn over the hull → boat nestles in the waves) -->
    <svg class="ocean-layer ocean-front absolute inset-0 h-full w-[200%]" preserveAspectRatio="none" viewBox="0 0 240 40" fill="none">
      <path d="M0 21 q30 -9 60 0 t60 0 t60 0 t60 0 L240 40 L0 40 Z" fill="currentColor" opacity="0.09" />
      <path d="M0 21 q30 -9 60 0 t60 0 t60 0 t60 0" stroke="currentColor" stroke-width="0.7" opacity="0.32" />
    </svg>

    <!-- foam: a FILLED ribbon with a finer ripple → froth riding the front crest -->
    <svg class="ocean-layer ocean-foam absolute inset-0 h-full w-[200%]" preserveAspectRatio="none" viewBox="0 0 240 40" fill="currentColor">
      <path d="M0 18 q15 -5 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 L240 40 L0 40 Z" opacity="0.13" />
    </svg>
  </div>
</template>
