<script setup lang="ts">
// PharosChatAvatar — the assistant's mark (RFC 0017). Companion to PharosHelpChat.
//
// Two families: hand-drawn NAUTICAL-ROBOT marks (buzo, capitán, faro-bot, boya-bot, sub-bot)
// and plain nautical marks. Line-art, 24×24, `currentColor`, stroke language matched to lucide.
//
// Every glyph is INLINE on purpose. The playground's ChatAvatar.vue imports these from
// lucide-vue-next, but the registry widget is deliberately dependency-light (marked + DOMPurify
// and nothing else) — pushing an icon library onto every adopting app for six glyphs is not a
// trade worth making. The lucide-derived paths below are copied verbatim from lucide-vue-next
// (ISC), so the two stay visually identical.
//
// Sizing/colour come from the caller via CSS (`width`/`height`/`color`), not props.
defineProps<{
  /** Avatar id — see CHAT_AVATARS in design-studio's build-spec.ts. Unknown id → robot. */
  id?: string
}>()
</script>

<template>
  <!-- ── Nautical-robot marks (hand-drawn) ───────────────────────────────────── -->

  <!-- Buzo — casco de escafandra -->
  <svg
    v-if="id === 'diver'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M6 11a6 6 0 0 1 12 0v4a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z"/>
    <circle cx="12" cy="12" r="3.2"/>
    <circle cx="10.9" cy="12" r=".55" fill="currentColor" stroke="none"/>
    <circle cx="13.1" cy="12" r=".55" fill="currentColor" stroke="none"/>
    <circle cx="12" cy="3.2" r=".85"/>
    <path d="M12 5.2V4M5 12H3.5M19 12h1.5"/>
  </svg>

  <!-- Capitán — robot con gorra -->
  <svg
    v-else-if="id === 'captain'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect x="6" y="10.5" width="12" height="9" rx="2.5"/>
    <path d="M8.5 7.5h7l1 3H7.5z"/>
    <path d="M5.5 10.5h13"/>
    <circle cx="9.8" cy="14.5" r=".7" fill="currentColor" stroke="none"/>
    <circle cx="14.2" cy="14.5" r=".7" fill="currentColor" stroke="none"/>
    <path d="M10 17.5h4"/>
  </svg>

  <!-- Faro-bot — linterna + haz -->
  <svg
    v-else-if="id === 'beacon'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect x="6.5" y="11" width="11" height="8" rx="2.5"/>
    <path d="M10.5 8h3v3h-3z"/>
    <path d="M12 5.6V4.4M9.4 6.4l.7.7M14.6 6.4l-.7.7"/>
    <circle cx="9.8" cy="15" r=".65" fill="currentColor" stroke="none"/>
    <circle cx="14.2" cy="15" r=".65" fill="currentColor" stroke="none"/>
  </svg>

  <!-- Boya-bot — boya con luz y oleaje -->
  <svg
    v-else-if="id === 'buoy'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M8 10a4 4 0 0 1 8 0v4.5a4 4 0 0 1-8 0z"/>
    <path d="M12 6V4.6"/>
    <circle cx="12" cy="4" r=".85" fill="currentColor" stroke="none"/>
    <path d="M8.2 12.5h7.6"/>
    <circle cx="10.4" cy="10.4" r=".55" fill="currentColor" stroke="none"/>
    <circle cx="13.6" cy="10.4" r=".55" fill="currentColor" stroke="none"/>
    <path d="M4.5 19c1.4 1 2.6 1 4 0m3 0c1.4 1 2.6 1 4 0"/>
  </svg>

  <!-- Sub-bot — periscopio -->
  <svg
    v-else-if="id === 'periscope'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect x="5" y="11.5" width="11" height="8" rx="2.5"/>
    <path d="M16 16.5v-7.5h3.5"/>
    <circle cx="9" cy="15.5" r=".65" fill="currentColor" stroke="none"/>
    <circle cx="12.5" cy="15.5" r=".65" fill="currentColor" stroke="none"/>
    <path d="M8.5 18h4"/>
  </svg>

  <!-- ── Plain nautical marks (lucide paths, inlined) ─────────────────────────── -->

  <!-- Brújula (lucide compass) -->
  <svg
    v-else-if="id === 'compass'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="10"/>
    <path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/>
  </svg>

  <!-- Estrella norte (lucide star) -->
  <svg
    v-else-if="id === 'star'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>
  </svg>

  <!-- Catalejo (lucide telescope) -->
  <svg
    v-else-if="id === 'spyglass'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="m10.065 12.493-6.18 1.318a.934.934 0 0 1-1.108-.702l-.537-2.15a1.07 1.07 0 0 1 .691-1.265l13.504-4.44"/>
    <path d="m13.56 11.747 4.332-.924"/>
    <path d="m16 21-3.105-6.21"/>
    <path d="M16.485 5.94a2 2 0 0 1 1.455-2.425l1.09-.272a1 1 0 0 1 1.212.727l1.515 6.06a1 1 0 0 1-.727 1.213l-1.09.272a2 2 0 0 1-2.425-1.455z"/>
    <path d="m6.158 8.633 1.114 4.456"/>
    <path d="m8 21 3.105-6.21"/>
    <circle cx="12" cy="13" r="2"/>
  </svg>

  <!-- Haz de faro (lucide sparkles) -->
  <svg
    v-else-if="id === 'beam'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"/>
    <path d="M20 2v4"/>
    <path d="M22 4h-4"/>
    <circle cx="4" cy="20" r="2"/>
  </svg>

  <!-- Burbuja (lucide message-circle) -->
  <svg
    v-else-if="id === 'bubble'" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/>
  </svg>

  <!-- Robot (lucide bot) — also the fallback for any unknown id -->
  <svg
    v-else viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M12 8V4H8"/>
    <rect x="4" y="8" width="16" height="12" rx="2"/>
    <path d="M2 14h2"/>
    <path d="M20 14h2"/>
    <path d="M15 13v2"/>
    <path d="M9 13v2"/>
  </svg>
</template>
