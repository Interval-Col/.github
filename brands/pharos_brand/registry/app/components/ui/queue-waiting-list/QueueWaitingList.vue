<script setup lang="ts">
// QueueWaitingList — the Pháros waiting-queue list primitive (RFC 0008 library,
// RFC 0031 «cola como servicio»). Born for the sample-collection station in
// pharos-lis/lab-qc (plan task 5.4: look at the queue WITHOUT claiming a turn),
// shaped to serve any queue viewer later — the RFC 0031 read-only process
// viewer included.
//
// Ownership split (same as PharosHelpChat): this component RENDERS rows it is
// handed. Transport, auth, refresh cadence and the PHI-reveal policy (e.g.
// lab-qc's useIdlePrivacy) stay app-side. It never fetches, never writes, and
// treats an empty queue as the normal state of an up-to-date station — not an
// error.
import { computed } from 'vue'
import { AlertCircle, RefreshCw, Users } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
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
}>(), {
  loading: false,
  error: null,
  revealed: true,
  maskedText: '•••',
  emptyText: 'Nadie en espera — la estación está al día.',
  refreshable: true,
})

const emit = defineEmits<{ refresh: [] }>()

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
  <div class="flex flex-col gap-3">
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center gap-2 text-sm text-muted-foreground">
        <Users class="size-4" aria-hidden="true" />
        <span>
          En espera:
          <span class="font-medium text-foreground tabular-nums">{{ count }}</span>
        </span>
      </div>
      <Button
        v-if="refreshable"
        variant="outline"
        size="sm"
        :disabled="loading"
        @click="emit('refresh')"
      >
        <RefreshCw class="size-4" :class="loading ? 'animate-spin' : ''" aria-hidden="true" />
        Actualizar
      </Button>
    </div>

    <div
      v-if="error"
      role="alert"
      class="flex items-start gap-2 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
    >
      <AlertCircle class="mt-0.5 size-4 shrink-0" aria-hidden="true" />
      <span>{{ error }}</span>
    </div>

    <div v-else-if="loading" class="flex flex-col gap-2" aria-busy="true">
      <Skeleton v-for="n in 3" :key="n" class="h-10 w-full" />
    </div>

    <p v-else-if="rows.length === 0" class="rounded-md border border-dashed px-3 py-6 text-center text-sm text-muted-foreground">
      {{ emptyText }}
    </p>

    <Table v-else>
      <TableHeader>
        <TableRow>
          <TableHead class="w-12 text-right">#</TableHead>
          <TableHead>Paciente</TableHead>
          <TableHead>Documento</TableHead>
          <TableHead>Órdenes</TableHead>
          <TableHead class="w-24 text-right">Desde</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="row in rows" :key="row.queueId">
          <TableCell class="text-right font-medium tabular-nums">{{ row.position }}</TableCell>
          <TableCell>{{ masked(row.fullName) }}</TableCell>
          <TableCell class="text-muted-foreground">
            <span v-if="row.documentType" class="mr-1">{{ row.documentType }}</span>
            <span class="tabular-nums">{{ masked(row.documentNumber) }}</span>
          </TableCell>
          <TableCell>
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
            <span v-else class="text-sm text-muted-foreground">sin órdenes registradas</span>
          </TableCell>
          <TableCell class="text-right text-muted-foreground tabular-nums">
            {{ clockOf(row.waitingSince) }}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
