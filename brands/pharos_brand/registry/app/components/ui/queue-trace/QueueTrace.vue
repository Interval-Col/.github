<!--
  Pháros queue trace — el recorrido de una fila de la cola (RFC 0008 · RFC 0031).

  Contesta «¿dónde está esta muestra y por qué?»: los pasos en orden, con quién
  los hizo y **qué superficie manda en cada tramo**.

  💡 **No inventa una pantalla: hace honesta una que ya existe mal.** El tablero
  de recepción filtra por «hoy, esta oficina, no Cancelled/Finished» y NO por
  estado de recepción, así que **ya muestra** pacientes que salieron de recepción
  —recibidos en toma, en atención en Movimiento— sin decir a dónde se fueron.

  > Este es el **widget** (presentación pura). El **transporte** — a qué cola se
  > pregunta, con qué token, cuándo se pide — es de cada app, igual que
  > `QueueWaitingList` y `PharosHelpChat`. El widget nunca hace fetch y nunca
  > escribe.

  ⚠️ **Sin datos de paciente, y no por olvido:** un recorrido son cambios de
  estado —quién, cuándo, de qué a qué—. Quien lo abre ya sabe de qué paciente es,
  así que devolvérselos sería un sitio más donde pueden filtrarse.
-->
<template>
  <div class="flex flex-col gap-3">
    <!-- Cargando -->
    <div v-if="loading" class="flex items-center gap-2 py-8 text-sm text-muted-foreground">
      <slot name="spinner" />
      Consultando el recorrido…
    </div>

    <!-- Error. El texto viene de la app, que es quien sabe a quién mandar:
         «no está configurada» lo arregla quien despliega, «no responde» se
         espera, «no autorizó» se pide. Este widget no los reescribe. -->
    <div
      v-else-if="error"
      class="flex items-start gap-2 rounded-md border border-border bg-muted/40 p-3 text-sm"
    >
      <slot name="error-icon" />
      <span>{{ error }}</span>
    </div>

    <!-- Sin pasos. Es un hecho posible y distinto de un error: una fila recién
         creada todavía no tiene trazabilidad. -->
    <p v-else-if="!steps.length" class="py-8 text-center text-sm text-muted-foreground">
      {{ emptyText }}
    </p>

    <!-- El recorrido -->
    <ol v-else class="space-y-0">
      <li v-for="(step, i) in steps" :key="i" class="flex gap-3">
        <!-- El riel: punto y línea. El último punto no lleva línea debajo. -->
        <div class="flex flex-col items-center">
          <span
            class="mt-1.5 size-2 shrink-0 rounded-full"
            :class="i === steps.length - 1 ? 'bg-primary' : 'bg-muted-foreground'"
          />
          <span v-if="i < steps.length - 1" class="w-px grow bg-border" aria-hidden="true" />
        </div>

        <div class="min-w-0 grow pb-4">
          <div class="flex flex-wrap items-baseline gap-x-2">
            <span class="text-sm font-semibold">{{ queueTraceStatus(step.status).label }}</span>
            <!-- Quién manda en este tramo. Es la mitad del «por qué». -->
            <span
              class="rounded-full bg-muted px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground"
            >
              {{ QUEUE_TRACE_OWNER_LABEL[queueTraceStatus(step.status).owner] }}
            </span>
          </div>
          <p class="text-xs text-muted-foreground">
            {{ formatAt(step.at) }} · {{ step.created_by }}
          </p>
        </div>
      </li>
    </ol>

    <!-- 🔴 El marcador del laboratorio. Sólo cuando aplica, y es la promesa
         honesta del visor: la cola sólo sabe hasta la puerta del LIS. -->
    <div
      v-if="endsAtCobol(steps)"
      class="flex items-start gap-2 rounded-md border border-border bg-muted/40 p-3 text-sm"
    >
      <slot name="lab-icon" />
      <span>{{ labHandoffText }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { QueueTraceStep } from './types'
import { QUEUE_TRACE_OWNER_LABEL, endsAtCobol, queueTraceStatus } from './types'

withDefaults(defineProps<{
  /** Los pasos, en orden de ocurrencia. El último es el estado actual. */
  steps: QueueTraceStep[]
  loading?: boolean
  /** Una frase con dueño, del mapeo de errores de la app. `null` = bien. */
  error?: string | null
  /** Qué decir cuando la fila existe pero no tiene recorrido todavía. */
  emptyText?: string
  /** El aviso de que desde acá manda el laboratorio. Parametrizable porque cada
   *  superficie le habla a un público distinto. */
  labHandoffText?: string
}>(), {
  loading: false,
  error: null,
  emptyText: 'Esta fila todavía no tiene recorrido registrado.',
  labHandoffText:
    'Desde aquí el recorrido lo lleva el laboratorio. La cola de recepción no ve lo que pasa después de la toma.',
})

/** Fecha corta y local. `Intl` y no una librería: es una fecha, no un formato. */
function formatAt(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString('es-CO', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
