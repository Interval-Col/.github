<script setup lang="ts">
// Live system-health beacon — "vigilamos lo invisible" made literal. Reads the
// shared poller (useHealthBeacon) and renders the accent-INDEPENDENT status palette
// (RFC 0008 Q4), NOT the brand accent, so it never shifts when a sub-brand re-accents.
// 'ok' is the calm rest/all-clear state (steady); 'drift'/'out' pulse. When the
// backend reports subsystems, the dot becomes a popover with the per-subsystem
// breakdown (structure + status only — never PHI).
import { computed } from 'vue'
import type { BeaconStatus } from '~/composables/useHealthBeacon'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'

const state = useHealthBeacon()

const MAP: Record<BeaconStatus, { label: string; dot: string; text: string }> = {
  ok: { label: 'En orden', dot: 'bg-status-success', text: 'text-status-success' },
  drift: { label: 'Derivando', dot: 'bg-status-warning', text: 'text-status-warning' },
  out: { label: 'Fuera de rango', dot: 'bg-status-error', text: 'text-status-error' },
}

const s = computed(() => MAP[state.value.status] ?? MAP.ok)
const alert = computed(() => state.value.status !== 'ok')
const hasSubsystems = computed(() => state.value.subsystems.length > 0)
const checkedLabel = computed(() =>
  state.value.checkedAt
    ? new Date(state.value.checkedAt).toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
    : '—',
)
</script>

<template>
  <!-- With subsystems → the dot opens a hover/click breakdown popover. -->
  <Popover v-if="hasSubsystems">
    <PopoverTrigger
      class="hidden items-center gap-2 outline-none lg:inline-flex"
      :title="`Sistema: ${s.label}`"
      aria-live="polite"
    >
      <span class="relative flex size-2">
        <span
          v-if="alert"
          class="absolute inline-flex size-full animate-ping rounded-full opacity-60"
          :class="s.dot"
        />
        <span class="relative inline-flex size-2 rounded-full" :class="s.dot" />
      </span>
      <span class="font-mono text-[11px] uppercase tracking-wide" :class="s.text">{{ s.label }}</span>
    </PopoverTrigger>
    <PopoverContent align="end" class="w-64 p-2">
      <div class="mb-1.5 flex items-center justify-between">
        <span class="font-mono text-[11px] uppercase tracking-wide" :class="s.text">{{ s.label }}</span>
        <span class="text-[11px] text-muted-foreground">{{ checkedLabel }}</span>
      </div>
      <ul class="flex flex-col gap-1">
        <li
          v-for="sub in state.subsystems"
          :key="sub.name"
          class="flex items-center justify-between gap-2 text-[0.8rem]"
        >
          <span class="truncate text-foreground">{{ sub.name }}</span>
          <span class="size-1.5 shrink-0 rounded-full" :class="(MAP[sub.status] ?? MAP.ok).dot" />
        </li>
      </ul>
    </PopoverContent>
  </Popover>

  <!-- No subsystems → just the dot + label. -->
  <span
    v-else
    class="hidden items-center gap-2 lg:inline-flex"
    :title="`Sistema: ${s.label}`"
    aria-live="polite"
  >
    <span class="relative flex size-2">
      <span
        v-if="alert"
        class="absolute inline-flex size-full animate-ping rounded-full opacity-60"
        :class="s.dot"
      />
      <span class="relative inline-flex size-2 rounded-full" :class="s.dot" />
    </span>
    <span class="font-mono text-[11px] uppercase tracking-wide" :class="s.text">{{ s.label }}</span>
  </span>
</template>
