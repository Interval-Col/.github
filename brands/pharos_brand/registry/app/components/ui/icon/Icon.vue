<script setup lang="ts">
// Icon — the ONE Pháros icon tag (RFC 0008 icon standard, Phase 1.4).
// Renders an @iconify/tailwind mask (the prefix--name form). Accepts a curated
// registry key (preferred — guaranteed to render, see icons.ts) OR a raw
// `prefix:name` / `prefix--name` id (only renders if that id is in the
// main.css @source safelist). Decorative by default (aria-hidden); pass `label`
// to make it meaningful (role="img" + aria-label).
// NOTE: the class is built by concatenation (not a template literal) so the
// Tailwind source-scanner never sees a complete arbitrary icon class here —
// generation is driven solely by the @source safelist in main.css.
//
//   <Icon name="search" />                 · curated key, 16px
//   <Icon name="patient" :size="6" class="text-primary" />
//   <Icon name="lucide:calendar" :size="5" label="Fecha" />
import type { HTMLAttributes } from 'vue'
import { computed } from 'vue'
import { cn } from '@/lib/utils'
import { ICONS, type IconName } from './icons'

const props = withDefaults(defineProps<{
  /** A curated registry key (icons.ts) or a raw `prefix:name` id. */
  name: IconName | (string & {})
  /** 4 = 16px (inline), 5 = 20px (buttons/nav), 6 = 24px (headers). Default 4. */
  size?: 4 | 5 | 6
  class?: HTMLAttributes['class']
  /** When set, the icon is meaningful: role="img" + this aria-label. Else decorative. */
  label?: string
}>(), {
  size: 4,
})

const SIZE_CLASS: Record<4 | 5 | 6, string> = {
  4: 'size-4',
  5: 'size-5',
  6: 'size-6',
}

const iconId = computed(() => {
  const n = props.name
  if (n in ICONS) return ICONS[n as IconName]
  return n.replace(':', '--')
})

// Built by concatenation on purpose (see the note above) — no complete arbitrary
// icon class literal in source. twMerge passes the arbitrary class through.
const iconClass = computed(() => 'icon-[' + iconId.value + ']')
</script>

<template>
  <span
    :class="cn(iconClass, SIZE_CLASS[size], 'inline-block shrink-0', props.class)"
    :role="label ? 'img' : undefined"
    :aria-label="label || undefined"
    :aria-hidden="label ? undefined : 'true'"
  />
</template>
