<script setup lang="ts">
// ReportarEvento — el BOTÓN que abre el formulario de reporte en un panel lateral sobre la
// pantalla actual (Pháros · Organización, plan 2.4; recorrido O3 aprobado en la puerta G8).
//
// Pensado para el pie del sidebar de cualquier app Pháros. El panel lleva el mismo
// `EventoFormulario` que usa Organización: UNA pieza, no una copia por app.
import { ref } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle,
} from '@/components/ui/sheet'
import EventoFormulario from './EventoFormulario.vue'
import { TEXTOS } from './types'
import type { ErrorDeEventos, ProcesoOpcion, Sede } from './types'
import type { EventosApi, FetchLike } from '@/lib/eventosApi'

defineProps<{
  apiBase: string
  app: string
  pantalla: string
  procesos: ProcesoOpcion[]
  ordenSugerida?: string | null
  sedeInicial?: Sede | null
  avisoQueja?: string
  headers?: () => Record<string, string>
  fetcher?: FetchLike
  api?: EventosApi
}>()

const emit = defineEmits<{
  (e: 'reportado', evento: { id: string, consecutivo: string, pendienteDeRevision: boolean }): void
  (e: 'error', error: ErrorDeEventos): void
}>()

const abierto = ref(false)
</script>

<template>
  <Sheet v-model:open="abierto">
    <Button type="button" variant="outline" size="sm" class="justify-start gap-2" data-pg-reportar-boton @click="abierto = true">
      <slot name="icono" />
      {{ TEXTOS.reportarBoton }}
    </Button>
    <SheetContent side="right" class="w-full overflow-y-auto p-4 sm:max-w-lg" data-pg-reportar-panel>
      <SheetHeader class="p-0">
        <SheetTitle>{{ TEXTOS.reportarTitulo }}</SheetTitle>
        <SheetDescription>{{ TEXTOS.reportarDescripcion }}</SheetDescription>
      </SheetHeader>
      <!-- El contenido del panel se desmonta al cerrarlo (reka-ui no lo deja montado), así que el formulario vuelve vacío. -->
      <EventoFormulario
        v-bind="$props"
        @reportado="emit('reportado', $event)"
        @error="emit('error', $event)"
        @cancelar="abierto = false"
      />
    </SheetContent>
  </Sheet>
</template>
