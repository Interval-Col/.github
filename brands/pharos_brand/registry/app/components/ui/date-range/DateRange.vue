<script lang="ts">
</script>

<script setup lang="ts">
// DateRange — «Rango de fechas» (plan de búsqueda, 0.7). Desde/Hasta inclusivos, con
// atajos calculados en America/Bogota. SIN ventana máxima (D21): sólo avisa.
import { parseDate } from '@internationalized/date'
import { computed, useId, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { DatePicker } from '@/components/ui/date-picker'
import { Label } from '@/components/ui/label'
import { TEXTOS } from '@/lib/busqueda/textos'
import { ATAJOS, detectar, rangoDe, type Atajo, type RangoFechas } from './atajos'

const props = defineProps<{
  /** Si el rango abarca más días que esto, muestra el aviso (nunca bloquea). */
  avisoAmplioDesdeDias?: number
}>()

const modelo = defineModel<RangoFechas>({ default: () => ({ desde: null, hasta: null }) })
const emit = defineEmits<{ 'update:valido': [valido: boolean] }>()

// El atajo marcado SALE de las fechas, no de qué botón se oprimió: si escribes a mano
// del 1 al 27 de noviembre, se marca «Este mes» (lo encontró German, 2026-11-27).
// «Personalizado» queda marcado cuando las fechas no son de ningún atajo.
// Ids propios por instancia: dos rangos en la misma página no se pisan.
const uid = useId()
const idDesde = `${uid}-desde`
const idHasta = `${uid}-hasta`
const idMensaje = `${uid}-mensaje`

const activo = computed<Atajo | null>(() => detectar(modelo.value))

function elegir(a: Atajo) {
  if (a !== 'personalizado') modelo.value = rangoDe(a)
  else document.getElementById(idDesde)?.querySelector<HTMLElement>('[contenteditable], input, [role=spinbutton]')?.focus()
}

function editar(campo: 'desde' | 'hasta', valor: string | null) {
  modelo.value = { ...modelo.value, [campo]: valor }
}

const alReves = computed(() => !!modelo.value.desde && !!modelo.value.hasta && modelo.value.desde > modelo.value.hasta)
const valido = computed(() => !alReves.value)
watch(valido, v => emit('update:valido', v), { immediate: true })

const dias = computed(() => {
  const { desde, hasta } = modelo.value
  if (!desde || !hasta || alReves.value) return 0
  const a = parseDate(desde)
  const b = parseDate(hasta)
  return Math.round((Date.UTC(b.year, b.month - 1, b.day) - Date.UTC(a.year, a.month - 1, a.day)) / 86400000) + 1
})
const amplio = computed(() => props.avisoAmplioDesdeDias != null && dias.value > props.avisoAmplioDesdeDias)

defineExpose({ valido })
</script>

<template>
  <div class="flex flex-col">
    <div class="mb-3 flex flex-wrap gap-2" role="group" aria-label="Atajos de fechas">
      <Button
        v-for="a in ATAJOS"
        :key="a.id"
        type="button"
        size="sm"
        :variant="activo === a.id ? 'default' : 'outline'"
        :aria-pressed="activo === a.id"
        @click="elegir(a.id)"
      >
        {{ a.texto }}
      </Button>
    </div>

    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <div class="flex min-w-0 flex-col gap-1.5">
        <Label :for="idDesde">{{ TEXTOS.rango.desde }}</Label>
        <DatePicker
          :id="idDesde"
          :model-value="modelo.desde"
          :error="alReves"
          :aria-describedby="idMensaje"
          @update:model-value="editar('desde', $event)"
        />
      </div>
      <div class="flex min-w-0 flex-col gap-1.5">
        <Label :for="idHasta">{{ TEXTOS.rango.hasta }}</Label>
        <DatePicker
          :id="idHasta"
          :model-value="modelo.hasta"
          :error="alReves"
          :aria-describedby="idMensaje"
          @update:model-value="editar('hasta', $event)"
        />
      </div>
    </div>

    <div :id="idMensaje" aria-live="polite">
      <p v-if="alReves" class="mt-3 text-sm text-destructive">{{ TEXTOS.rango.alReves }}</p>
      <p v-else-if="amplio" class="mt-3 text-sm text-status-warning">{{ TEXTOS.rango.amplio }}</p>
    </div>
  </div>
</template>
