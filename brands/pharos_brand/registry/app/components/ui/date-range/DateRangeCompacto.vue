<script setup lang="ts">
// DateRangeCompacto — el mismo Rango de fechas detrás de UN botón que dice el rango
// («Este mes · 01/11 – 27/11»). Para barras de herramientas: en un portátil pequeño
// cada línea de controles le quita alto a la tabla (German, 2026-11-27).
import { computed, watch } from 'vue'
import { CalendarRange } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import DateRange from './DateRange.vue'
import type { RangoFechas } from './atajos'
import { etiquetaAtajo, ZONA } from './atajos'
import { today } from '@internationalized/date'

const props = defineProps<{ avisoAmplioDesdeDias?: number }>()
const modelo = defineModel<RangoFechas>({ default: () => ({ desde: null, hasta: null }) })
const emit = defineEmits<{ 'update:valido': [valido: boolean] }>()
// La validez sale del modelo, no del panel: el panel sólo existe abierto, y un valor
// puesto desde afuera con el panel cerrado también tiene que validarse.
const valido = computed(() => !(modelo.value.desde && modelo.value.hasta && modelo.value.desde > modelo.value.hasta))
watch(valido, v => emit('update:valido', v), { immediate: true })

function corta(iso: string | null): string {
  if (!iso) return '…'
  const [y, m, d] = iso.split('-')
  return y === String(today(ZONA).year) ? `${d}/${m}` : `${d}/${m}/${y}`
}
const resumen = computed(() => {
  const { desde, hasta } = modelo.value
  if (!desde && !hasta) return 'Escoge las fechas'
  const fechas = desde === hasta ? corta(desde) : `${corta(desde)} – ${corta(hasta)}`
  const atajo = etiquetaAtajo(modelo.value)
  return atajo ? `${atajo} · ${fechas}` : fechas
})

</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button
        type="button"
        variant="outline"
        :aria-invalid="!valido || undefined"
        :class="cn('justify-start gap-2 font-normal tabular-nums', !valido && 'border-destructive')"
      >
        <CalendarRange class="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
        <span class="sr-only">Fechas:</span>
        {{ resumen }}
      </Button>
    </PopoverTrigger>
    <PopoverContent align="start" :collision-padding="8" class="w-auto max-w-[calc(100vw-2rem)] p-3">
      <DateRange v-model="modelo" :aviso-amplio-desde-dias="props.avisoAmplioDesdeDias" />
    </PopoverContent>
  </Popover>
</template>
