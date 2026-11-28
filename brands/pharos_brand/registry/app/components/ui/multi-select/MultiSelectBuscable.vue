<script setup lang="ts" generic="T">
// MultiSelectBuscable — escoger varias opciones con un cuadro para buscarlas por texto
// y por varias claves (plan de búsqueda, 0.6 y 0.11). La familia de MultiSelect: el
// mismo panel con casillas y tope de alto, más búsqueda. Filtra SÓLO las opciones que
// ya tiene: nunca llama al servidor. Cada opción dice por qué coincidió («Coincide por
// sinónimo «HbA1c»»). Nació como faceta de Liberación (Examen, Médico, Sección) y German
// la aprobó ahí el 2026-11-27.
import { computed, ref, watch } from 'vue'
import { ChevronsUpDown, Search, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

export interface OpcionFaceta<T> {
  item: T
  /** Texto corto de por qué coincidió; vacío si coincidió por la etiqueta. */
  pista?: string
}

const props = defineProps<{
  modelValue: string[]
  /** Etiqueta visible de la faceta («Examen», «Médico»). */
  etiqueta: string
  items: readonly T[]
  claveDe: (item: T) => string
  etiquetaDe: (item: T) => string
  /** Detalle en gris al lado de la etiqueta (código, sección…). */
  detalleDe?: (item: T) => string
  /** Filtra por el término; sin término, devuelve todos. */
  filtrar: (items: readonly T[], termino: string) => OpcionFaceta<T>[]
  placeholderBusqueda?: string
  /** Fila «Todas» arriba (todas ⇄ ninguna). */
  conTodas?: boolean
  /** Resumen sin nada escogido (por defecto «Todos»: una faceta vacía no filtra). */
  textoVacio?: string
  /** Resumen con todo escogido (por defecto, se nombran). */
  textoTodas?: string
  /** Ancho FIJO del botón (clases de Tailwind): fijo para que la barra no cambie de
   *  ancho con lo escogido. Por defecto `sm:w-40`. */
  anchoClase?: string
  /** Aviso corto sobre lo que esta faceta oculta («1 requiere atención»). Se ve como un
   *  punto de alerta DENTRO del botón —la barra no cambia de alto— y se lee completo en el
   *  `title` y por lector de pantalla. Con scroll no se pierde lo que importa. */
  aviso?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string[]] }>()

const abierto = ref(false)
const termino = ref('')
watch(abierto, (a) => {
  if (!a) termino.value = ''
})

const opciones = computed(() => props.filtrar(props.items, termino.value))
const elegidas = computed(() => new Set(props.modelValue))
const resumen = computed(() => {
  const n = props.modelValue.length
  if (!n) return props.textoVacio ?? 'Todos'
  if (props.textoTodas && n === props.items.length) return props.textoTodas
  const primera = props.items.find(i => props.claveDe(i) === props.modelValue[0])
  const nombre = primera ? props.etiquetaDe(primera) : ''
  return n === 1 ? nombre : `${nombre} y ${n - 1} más`
})
const titulo = computed(() =>
  props.items.filter(i => elegidas.value.has(props.claveDe(i))).map(props.etiquetaDe).join('\n'))

const todas = computed(() => props.items.length > 0 && props.modelValue.length === props.items.length)
function alternarTodas() {
  emit('update:modelValue', todas.value ? [] : props.items.map(props.claveDe))
}

function alternar(item: T) {
  const k = props.claveDe(item)
  const s = new Set(elegidas.value)
  if (s.has(k)) s.delete(k)
  else s.add(k)
  emit('update:modelValue', props.items.map(props.claveDe).filter(c => s.has(c)))
}
</script>

<template>
  <Popover v-model:open="abierto">
    <PopoverTrigger as-child>
      <Button
        type="button"
        variant="outline"
        :class="['w-full justify-between gap-2 font-normal', anchoClase ?? 'sm:w-40']"
        :title="[titulo, aviso].filter(Boolean).join('\n') || undefined"
      >
        <span class="flex min-w-0 items-center gap-1.5">
          <span class="shrink-0 text-muted-foreground">{{ etiqueta }}:</span>
          <span class="truncate" :class="modelValue.length ? 'font-medium text-foreground' : 'text-muted-foreground'">{{ resumen }}</span>
          <span v-if="aviso" class="inline-flex shrink-0 items-center text-status-warning" :title="aviso">
            <span class="size-2 rounded-full bg-status-warning" aria-hidden="true" />
            <span class="sr-only">{{ aviso }}</span>
          </span>
        </span>
        <ChevronsUpDown class="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
      </Button>
    </PopoverTrigger>
    <PopoverContent
      align="start"
      :collision-padding="8"
      class="flex max-h-(--reka-popover-content-available-height) w-80 max-w-[calc(100vw-2rem)] flex-col gap-1 p-1"
    >
      <div class="relative">
        <Search class="pointer-events-none absolute left-2 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
        <Input
          v-model="termino"
          :aria-label="`Buscar ${etiqueta.toLowerCase()} en la lista`"
          :placeholder="placeholderBusqueda ?? `Buscar ${etiqueta.toLowerCase()}…`"
          autocomplete="off"
          class="h-8 pl-8"
        />
      </div>
      <div class="min-h-0 flex-1 overflow-y-auto overscroll-contain">
        <label
          v-if="conTodas && !termino"
          class="mb-1 flex cursor-pointer items-center gap-2 border-b px-2 py-1.5 pb-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
        >
          <Checkbox
            :model-value="todas ? true : modelValue.length ? 'indeterminate' : false"
            @update:model-value="alternarTodas"
          />
          {{ textoTodas ?? 'Todas' }}
        </label>
        <p v-if="!opciones.length" class="px-2 py-1.5 text-sm text-muted-foreground">
          Ninguna opción coincide con «{{ termino }}».
        </p>
        <label
          v-for="o in opciones"
          :key="claveDe(o.item)"
          class="flex cursor-pointer items-start gap-2 rounded-sm px-2 py-1.5 text-sm hover:bg-accent hover:text-accent-foreground"
        >
          <Checkbox class="mt-0.5" :model-value="elegidas.has(claveDe(o.item))" @update:model-value="() => alternar(o.item)" />
          <span class="flex min-w-0 flex-col">
            <span class="text-foreground">
              {{ etiquetaDe(o.item) }}
              <span v-if="detalleDe" class="font-data text-xs text-muted-foreground">{{ detalleDe(o.item) }}</span>
            </span>
            <span v-if="o.pista" class="text-xs text-muted-foreground">{{ o.pista }}</span>
          </span>
        </label>
      </div>
      <!-- Opciones propias de la faceta (p. ej. qué se muestra de los exámenes): van DENTRO
           del panel para no gastar ancho en la barra. -->
      <div v-if="$slots.pie && modelValue.length" class="border-t px-1 pt-1">
        <slot name="pie" />
      </div>
      <div v-if="modelValue.length" class="border-t pt-1">
        <Button type="button" variant="ghost" size="sm" class="h-7 w-full justify-start gap-1.5 text-xs" @click="emit('update:modelValue', [])">
          <X class="size-3.5" aria-hidden="true" /> Quitar selección
        </Button>
      </div>
    </PopoverContent>
  </Popover>
</template>
