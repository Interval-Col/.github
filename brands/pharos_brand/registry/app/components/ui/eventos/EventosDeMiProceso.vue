<script setup lang="ts">
// EventosDeMiProceso — el panel donde trabaja el equipo de un proceso (Pháros · Organización, plan 2.4).
//
// Lista los eventos del proceso de quien consulta, con su estado y su plazo. Lee
// `GET ${apiBase}/eventos?vista=mis_procesos`: el alcance (qué procesos son «míos») lo decide el
// servidor desde la sesión, nunca este componente.
//
// 🛑 No pinta la orden de servicio por omisión, aunque la API la mande para quien puede verla
// (`mostrarOrden` la enciende, y la app decide quién). Las filas no llevan texto libre.
//
// Abrir un evento es de la app anfitriona: el componente emite `abrir` con el id.
import { computed, onMounted, ref } from 'vue'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { crearEventosApi, ErrorEventosApi } from '@/lib/eventosApi'
import type { EventosApi, FetchLike } from '@/lib/eventosApi'
import { ERRORES, ETIQUETA_ESTADO, ETIQUETA_TIPO, TEXTOS } from './types'
import type { ErrorDeEventos, ResumenEvento } from './types'

const props = withDefaults(defineProps<{
  apiBase: string
  headers?: () => Record<string, string>
  fetcher?: FetchLike
  api?: EventosApi
  /** Enciende la columna de orden de servicio. Apagado por omisión. */
  mostrarOrden?: boolean
  /** «Hoy», para marcar vencidos. Solo para pruebas; por omisión, la fecha del navegador. */
  hoy?: string
  class?: string
}>(), { mostrarOrden: false })

const emit = defineEmits<{
  (e: 'abrir', id: string): void
  (e: 'error', error: ErrorDeEventos): void
}>()

const api = computed(() => props.api ?? crearEventosApi({
  apiBase: props.apiBase, headers: props.headers, fetch: props.fetcher,
}))

const filas = ref<ResumenEvento[]>([])
const cargando = ref(true)
const fallo = ref<ErrorDeEventos | null>(null)

const hoyIso = computed(() => props.hoy ?? new Date().toISOString().slice(0, 10))
const vencido = (r: ResumenEvento) =>
  !!r.plazo && r.plazo.slice(0, 10) < hoyIso.value && r.estado !== 'cerrado' && r.estado !== 'descartado'
// Urgentes primero, luego por fecha de reporte (lo más viejo arriba: es lo que más espera).
const ordenadas = computed(() => [...filas.value].sort((a, b) =>
  Number(b.urgente) - Number(a.urgente) || a.creado_en.localeCompare(b.creado_en)))

async function cargar() {
  cargando.value = true
  fallo.value = null
  try {
    filas.value = await api.value.listar('mis_procesos')
  } catch (e) {
    const detalle = e instanceof ErrorEventosApi ? e.detalle : { causa: 'otro', mensaje: ERRORES.otro } as ErrorDeEventos
    fallo.value = detalle
    filas.value = []
    emit('error', detalle)
  } finally {
    cargando.value = false
  }
}
onMounted(cargar)
defineExpose({ recargar: cargar })

const fecha = (iso: string) => iso.slice(0, 10)
</script>

<template>
  <section :class="cn('space-y-3 text-sm', props.class)" data-pg-eventos-panel :aria-label="TEXTOS.panelTitulo">
    <header class="flex items-center justify-between gap-2">
      <h2 class="font-heading text-base font-semibold">{{ TEXTOS.panelTitulo }}</h2>
    </header>

    <p v-if="cargando" class="text-muted-foreground" role="status" data-pg-eventos-cargando>{{ TEXTOS.panelCargando }}</p>

    <div v-else-if="fallo" role="alert" class="flex items-center justify-between gap-2 rounded-md border border-status-error bg-status-error-bg px-3 py-2" data-pg-eventos-error>
      <span>{{ fallo.mensaje }}</span>
      <Button type="button" size="sm" variant="outline" @click="cargar">{{ TEXTOS.panelReintentar }}</Button>
    </div>

    <p v-else-if="!ordenadas.length" class="rounded-md border border-border bg-muted/40 px-3 py-3 text-muted-foreground" data-pg-eventos-vacio>
      {{ TEXTOS.panelVacio }}
    </p>

    <div v-else class="overflow-x-auto rounded-md border border-border">
      <table class="w-full text-left" data-pg-eventos-tabla>
        <thead class="bg-muted/40 text-xs text-muted-foreground">
          <tr>
            <th scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelConsecutivo }}</th>
            <th scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelTipo }}</th>
            <th scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelProceso }}</th>
            <th scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelEstado }}</th>
            <th scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelPlazo }}</th>
            <th v-if="mostrarOrden" scope="col" class="px-3 py-2 font-medium">{{ TEXTOS.panelOrden }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="r in ordenadas" :key="r.id"
            :class="cn('cursor-pointer border-t border-border hover:bg-accent/50', r.oculto && 'bg-status-warning-bg')"
            role="button" tabindex="0" :data-pg-evento-fila="r.id"
            @click="emit('abrir', r.id)" @keydown.enter.prevent="emit('abrir', r.id)" @keydown.space.prevent="emit('abrir', r.id)"
          >
            <td class="px-3 py-2">
              <span class="font-mono text-xs">{{ r.consecutivo }}</span>
              <Badge v-if="r.urgente" variant="destructive" class="ml-1">{{ TEXTOS.panelUrgente }}</Badge>
            </td>
            <td class="px-3 py-2">{{ ETIQUETA_TIPO[r.tipo] ?? r.tipo }}</td>
            <td class="px-3 py-2 font-mono text-xs">{{ r.proceso_codigo }}</td>
            <td class="px-3 py-2">
              {{ ETIQUETA_ESTADO[r.estado] ?? r.estado }}
              <Badge v-if="r.oculto" variant="outline" class="ml-1">{{ TEXTOS.panelRevision }}</Badge>
            </td>
            <td class="px-3 py-2">
              <template v-if="r.plazo">
                {{ fecha(r.plazo) }}
                <Badge v-if="vencido(r)" variant="destructive" class="ml-1">{{ TEXTOS.panelVencido }}</Badge>
              </template>
              <span v-else class="text-muted-foreground">{{ TEXTOS.panelSinPlazo }}</span>
            </td>
            <td v-if="mostrarOrden" class="px-3 py-2 font-mono text-xs">{{ r.orden_servicio ?? '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="!mostrarOrden" class="text-xs text-muted-foreground">{{ TEXTOS.panelNota }}</p>
  </section>
</template>
