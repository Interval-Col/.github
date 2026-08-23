<script setup lang="ts">
// QueueWaitingList — the Pháros waiting-queue panel primitive (RFC 0008
// library, RFC 0031 «cola como servicio»). Born for the sample-collection
// station in pharos-lis/lab-qc (plan task 5.4: look at the queue WITHOUT
// claiming a turn); the RFC 0031 read-only viewer is its next candidate.
//
// FORM: calcado del panel de cola de Recepción (admission-patient
// Reception.vue) — the app that already does "queue in a side panel" best,
// which is how RFC 0008 says primitives are extracted. An in-flow <aside>
// docked RIGHT, width-animated: a collapsed rail (count chip, NO PHI) that
// expands to a w-80 panel with a vertical stack of patient cards. In-flow on
// purpose: a fixed/Sheet drawer overlays the app nav and topbar — the exact
// problem Reception already paid for.
//
// Ownership split (same as PharosHelpChat): this component RENDERS rows it is
// handed. Transport, auth, refresh cadence and the PHI-reveal policy (e.g.
// lab-qc's useIdlePrivacy) stay app-side. It never fetches, never writes, and
// treats an empty queue as the normal state of an up-to-date station — not an
// error. Collapsed, it shows only the count — no PHI on screen by default.
import { computed, ref } from 'vue'
import { AlertCircle, ChevronLeft, ChevronRight, RefreshCw, UsersRound } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import type { QueueWaitingRow } from './types'

const props = withDefaults(defineProps<{
  /** Rows in arrival order. Row 1 is who «llamar siguiente» would claim. */
  rows: QueueWaitingRow[]
  loading?: boolean
  /** A sentence with an owner, from the app's error mapping. `null` = fine. */
  error?: string | null
  /** PHI reveal policy, decided by the app (idle-privacy, role, …). */
  revealed?: boolean
  maskedText?: string
  emptyText?: string
  /** Show the refresh control; the app answers the `refresh` emit. */
  refreshable?: boolean
  title?: string
  /** Vertical label on the collapsed rail. */
  railLabel?: string
  /** Whether the panel starts expanded. */
  defaultOpen?: boolean
}>(), {
  loading: false,
  error: null,
  revealed: true,
  maskedText: '•••',
  emptyText: 'Nadie en espera — la estación está al día.',
  refreshable: true,
  title: 'Cola de pacientes',
  railLabel: 'Cola',
  defaultOpen: true,
})

const emit = defineEmits<{ refresh: [] }>()

const open = ref(props.defaultOpen)

const masked = (value: string | undefined): string => {
  if (!value) return ''
  return props.revealed ? value : props.maskedText
}

const clockOf = (iso: string | null | undefined): string => {
  if (!iso) return ''
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return ''
  return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
}

const count = computed(() => props.rows.length)
</script>

<template>
  <!-- In-flow on the RIGHT, width-animated. It lives INSIDE the page and
       pushes the workspace — it never overlays the nav or the topbar. -->
  <aside
    class="flex shrink-0 flex-col overflow-hidden border-l border-border bg-card transition-[width] duration-300 ease-in-out"
    :class="open ? 'w-80' : 'w-12'"
  >
    <!-- Collapsed rail: the count is visible, the PHI is not. -->
    <div v-if="!open" class="flex h-full flex-col items-center gap-3 py-3">
      <Button
        variant="ghost"
        size="icon"
        class="size-8"
        :aria-label="`Abrir ${title.toLowerCase()}`"
        @click="open = true"
      >
        <ChevronLeft class="size-5" aria-hidden="true" />
      </Button>
      <UsersRound class="size-5 text-muted-foreground" aria-hidden="true" />
      <span class="rounded-full bg-primary/15 px-1.5 py-0.5 text-xs font-semibold tabular-nums text-primary">
        {{ count }}
      </span>
      <span class="rotate-180 text-xs font-medium uppercase tracking-wide text-muted-foreground [writing-mode:vertical-rl]">
        {{ railLabel }}
      </span>
    </div>

    <!-- Expanded panel -->
    <div v-else class="flex h-full w-80 flex-col">
      <div class="flex items-center justify-between border-b border-border p-3">
        <h2 class="text-sm font-semibold text-foreground">
          {{ title }}
          <span class="ml-1 rounded-full bg-primary/15 px-1.5 py-0.5 text-xs font-semibold tabular-nums text-primary">
            {{ count }}
          </span>
        </h2>
        <div class="flex items-center gap-1">
          <Button
            v-if="refreshable"
            variant="ghost"
            size="icon"
            class="size-7"
            :disabled="loading"
            aria-label="Actualizar la cola"
            @click="emit('refresh')"
          >
            <RefreshCw class="size-4" :class="loading ? 'animate-spin' : ''" aria-hidden="true" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            class="size-7"
            :aria-label="`Cerrar ${title.toLowerCase()}`"
            @click="open = false"
          >
            <ChevronRight class="size-5" aria-hidden="true" />
          </Button>
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-3">
        <div
          v-if="error"
          role="alert"
          class="flex items-start gap-2 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
        >
          <AlertCircle class="mt-0.5 size-4 shrink-0" aria-hidden="true" />
          <span>{{ error }}</span>
        </div>

        <div v-else-if="loading" class="flex flex-col gap-2" aria-busy="true">
          <Skeleton v-for="n in 3" :key="n" class="h-16 w-full" />
        </div>

        <p v-else-if="rows.length === 0" class="mt-8 text-center text-sm text-muted-foreground">
          {{ emptyText }}
        </p>

        <template v-else>
          <div
            v-for="row in rows"
            :key="row.queueId"
            class="mb-3 rounded-lg border border-border bg-background p-3"
          >
            <div class="flex items-start justify-between gap-2">
              <div class="flex min-w-0 items-center gap-2">
                <span class="shrink-0 rounded-full bg-primary/15 px-1.5 py-0.5 text-xs font-semibold tabular-nums text-primary">
                  {{ row.position }}
                </span>
                <span class="truncate text-sm font-medium text-foreground">{{ masked(row.fullName) }}</span>
              </div>
              <span class="shrink-0 text-xs text-muted-foreground tabular-nums">{{ clockOf(row.waitingSince) }}</span>
            </div>
            <p class="mt-1 text-xs text-muted-foreground">
              <span v-if="row.documentType" class="mr-1">{{ row.documentType }}</span>
              <span class="tabular-nums">{{ masked(row.documentNumber) }}</span>
            </p>
            <div class="mt-2">
              <template v-if="row.orders.length">
                <Badge
                  v-for="order in row.orders"
                  :key="order"
                  variant="secondary"
                  class="mr-1 tabular-nums"
                >
                  {{ order }}
                </Badge>
              </template>
              <!-- Recepción pudo no registrar órdenes: se dice, no se calla. -->
              <span v-else class="text-xs text-muted-foreground">sin órdenes registradas</span>
            </div>
          </div>
        </template>
      </div>
    </div>
  </aside>
</template>
