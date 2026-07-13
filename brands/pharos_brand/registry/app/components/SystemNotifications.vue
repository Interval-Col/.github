<script setup lang="ts">
// ── Pháros notifications bell — topbar upper-right affordance (RFC 0008). ──────
// App-AGNOSTIC, like SidebarUser: the consuming app passes its notifications via
// `:items` (props-in) and reacts to `@view-all` (events-out); the shell owns the
// bell + count badge + popover chrome. With no items it shows a quiet bell + an
// "al día" empty state — the affordance is part of the brand shell whether or not
// an app has wired a source yet. Status-dot colours come from the accent-INDEPENDENT
// --status-* tokens (RFC 0008 Q4) via inline var() (gate-safe: no hex / no palette
// utilities); the count badge uses --status-error on --destructive-foreground.
import { computed } from 'vue'
import { Bell } from 'lucide-vue-next'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'
import { Button } from '~/components/ui/button'

type NotificationKind = 'success' | 'warning' | 'error' | 'info'
export interface PharosNotification {
  id?: string | number
  /** Status role → leading dot colour (accent-independent). */
  kind: NotificationKind
  text: string
  time?: string
}

const props = withDefaults(defineProps<{
  items?: PharosNotification[]
  /** Cap the badge number, e.g. "9+". 0 disables the cap. */
  max?: number
}>(), { items: () => [], max: 9 })

defineEmits<{ (e: 'view-all'): void }>()

const count = computed(() => props.items.length)
const badge = computed(() =>
  props.max > 0 && count.value > props.max ? `${props.max}+` : String(count.value),
)
</script>

<template>
  <Popover>
    <PopoverTrigger
      aria-label="Notificaciones"
      class="relative inline-flex size-9 shrink-0 items-center justify-center rounded-full border border-border bg-muted text-foreground outline-none transition-colors hover:bg-accent focus-visible:ring-2 focus-visible:ring-ring"
    >
      <Bell class="size-[18px]" aria-hidden="true" />
      <span
        v-if="count > 0"
        class="absolute -right-0.5 -top-0.5 inline-flex min-w-4 items-center justify-center rounded-full px-1 text-[9px] font-bold leading-4"
        :style="{ backgroundColor: 'var(--status-error)', color: 'var(--destructive-foreground)' }"
      >{{ badge }}</span>
    </PopoverTrigger>
    <PopoverContent align="end" :side-offset="8" class="w-72 p-0">
      <div class="flex items-center justify-between border-b border-border px-3 py-2">
        <span class="text-sm font-medium">Notificaciones</span>
        <span class="font-mono text-[10px] uppercase tracking-wide text-muted-foreground">
          {{ count > 0 ? `${count} ${count === 1 ? 'nueva' : 'nuevas'}` : 'Al día' }}
        </span>
      </div>
      <div v-if="count > 0" class="max-h-72 overflow-y-auto">
        <div
          v-for="(n, i) in items"
          :key="n.id ?? i"
          class="flex gap-2 px-3 py-2.5 transition-colors hover:bg-accent"
        >
          <span
            class="mt-1 size-2 shrink-0 rounded-full"
            :style="{ backgroundColor: `var(--status-${n.kind})` }"
            aria-hidden="true"
          />
          <div class="min-w-0">
            <p class="text-sm leading-tight">{{ n.text }}</p>
            <p v-if="n.time" class="text-[11px] text-muted-foreground">{{ n.time }}</p>
          </div>
        </div>
      </div>
      <div v-else class="px-3 py-6 text-center text-xs text-muted-foreground">
        Sin notificaciones
      </div>
      <Button
        v-if="count > 0"
        variant="ghost"
        class="block h-auto w-full rounded-none border-t border-border px-3 py-2 text-center text-xs font-normal text-primary hover:bg-accent"
        @click="$emit('view-all')"
      >
        Ver todas
      </Button>
    </PopoverContent>
  </Popover>
</template>
