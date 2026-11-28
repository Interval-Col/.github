<script setup lang="ts">
// BuscadorModo — los campos de UN modo del Buscador (plan de búsqueda, 0.5).
// No busca ni valida: sólo edita el borrador. El submit vive en Buscador.vue.
//
//   • Orden: número de orden.
//   • Documento: tipo PRIMERO y sin defecto (D8), escogido tecleando iniciales
//     («c» → CC y CE, «ced» → las cédulas); luego el número.
//   • Nombre: tres campos (D4), cada uno con la palabra completa o sus 3 primeras
//     letras, y la llave 3+3+3 que se va a enviar, a la vista mientras escribes.
//
// Los `id`/`name` de los campos no dicen qué son (`bq-…`) para que el navegador no
// ofrezca autocompletar con datos de otra persona.
import { computed, nextTick, ref, useId, watch } from 'vue'
import {
  ComboboxAnchor, ComboboxContent, ComboboxEmpty, ComboboxInput, ComboboxItem,
  ComboboxItemIndicator, ComboboxPortal, ComboboxRoot, ComboboxTrigger, ComboboxViewport,
  type AcceptableValue,
} from 'reka-ui'
import { Icon } from '@/components/ui/icon'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { cn } from '@/lib/utils'
import { useDocumentTypes } from '@/composables/useDocumentTypes'
import { ecoDeLlave, llaveDeNombre } from '@/lib/busqueda/llave-nombre'
import { TEXTOS } from '@/lib/busqueda/textos'
import type { ModoBuscador } from './types'

const props = defineProps<{
  modo: ModoBuscador
  /** Una sola línea para una barra de herramientas: etiquetas sólo para lectores de
   *  pantalla (siguen ligadas a su campo), el nombre del campo en el placeholder. */
  compacto?: boolean
}>()
const ph = (largo: string, corto: string) => (props.compacto ? corto : largo)

const orden = defineModel<string>('orden', { required: true })
const tipo = defineModel<string | null>('tipo', { required: true })
const numero = defineModel<string>('numero', { required: true })
const nombres = defineModel<string>('nombres', { required: true })
const apellido1 = defineModel<string>('apellido1', { required: true })
const apellido2 = defineModel<string>('apellido2', { required: true })

const T = TEXTOS.buscador
const uid = useId()
const id = (n: string) => `${uid}-bq-${n}`

// ── Tipo de documento: combobox con type-ahead por iniciales ──────────────────
const { tipos, tipoPorCodigo, tiposQueEmpiezanPor } = useDocumentTypes()
const raizTipo = ref<{ highlightFirstItem?: () => void } | null>(null)
const campoNumero = ref<{ $el: HTMLInputElement } | null>(null)
const terminoTipo = ref('')

function mostrarTipo(codigo: AcceptableValue): string {
  const t = tipoPorCodigo(codigo as string | null)
  return t ? `${t.codigo} · ${t.nombre}` : ''
}

// Si lo que dice el campo es la etiqueta del tipo ya escogido, se ofrecen todos.
// Los que empiezan por el CÓDIGO van primero: «ce» resalta CE antes que «Cédula de
// ciudadanía», y «ce» + Enter escoge CE.
const tiposVisibles = computed(() => {
  const t = terminoTipo.value
  if (!t || t === mostrarTipo(tipo.value)) return [...tipos]
  const porCodigo = (c: string) => (c.toLowerCase().startsWith(t.trim().toLowerCase()) ? 0 : 1)
  return tiposQueEmpiezanPor(t).sort((a, b) => porCodigo(a.codigo) - porCodigo(b.codigo))
})

// Al teclear, el primero que queda se resalta: «cc» + Enter escoge CC.
watch(tiposVisibles, () => nextTick(() => raizTipo.value?.highlightFirstItem?.()))

function alEscogerTipo(v: AcceptableValue) {
  tipo.value = (v as string | null) ?? null
  if (v) nextTick(() => campoNumero.value?.$el?.focus())
}

const llavePrevia = computed(() =>
  ecoDeLlave(llaveDeNombre({ nombres: nombres.value, apellido1: apellido1.value, apellido2: apellido2.value }))
  || T.llaveVacia)

const comunes = { autocomplete: 'off', spellcheck: 'false' } as const
</script>

<template>
  <!-- Orden -->
  <div v-if="modo === 'orden'" :class="compacto ? 'w-full' : 'grid gap-2'">
    <Label :for="id('o')" :class="compacto && 'sr-only'">{{ T.numeroOrden }}</Label>
    <Input
      :id="id('o')"
      v-model="orden"
      name="bq-o"
      inputmode="numeric"
      :placeholder="ph('', T.numeroOrden)"
      data-bq-primero
      v-bind="comunes"
    />
  </div>

  <!-- Documento -->
  <div v-else-if="modo === 'documento'" :class="compacto ? 'flex w-full items-center gap-2' : 'grid gap-4 sm:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]'">
    <div :class="compacto ? 'min-w-0 flex-1' : 'grid content-start gap-2'">
      <Label :for="id('t')" :class="compacto && 'sr-only'">{{ T.tipoDocumento }}</Label>
      <ComboboxRoot
        ref="raizTipo"
        :model-value="tipo"
        ignore-filter
        reset-search-term-on-blur
        open-on-click
        class="relative w-full"
        @update:model-value="alEscogerTipo"
      >
        <ComboboxAnchor
          class="flex h-9 w-full min-w-0 items-center gap-2 rounded-md border border-input bg-transparent px-3 shadow-xs transition-[color,box-shadow] focus-within:border-ring focus-within:ring-3 focus-within:ring-ring/50 dark:bg-input/30"
        >
          <ComboboxInput
            :id="id('t')"
            v-model="terminoTipo"
            name="bq-t"
            :display-value="mostrarTipo"
            :placeholder="ph(T.escogeTipo, 'Tipo')"
            data-bq-primero
            v-bind="comunes"
            class="h-full min-w-0 flex-1 bg-transparent text-base outline-none placeholder:text-muted-foreground md:text-sm"
          />
          <ComboboxTrigger :aria-label="T.tipoDocumento" class="shrink-0 text-muted-foreground hover:text-foreground">
            <Icon name="selector" />
          </ComboboxTrigger>
        </ComboboxAnchor>
        <ComboboxPortal>
          <ComboboxContent
            position="popper"
            :side-offset="4"
            class="z-50 max-h-72 w-[var(--reka-combobox-trigger-width)] min-w-52 overflow-hidden rounded-lg border bg-popover text-popover-foreground shadow-md"
          >
            <ComboboxViewport class="max-h-72 overflow-y-auto p-1">
              <ComboboxEmpty class="py-3 text-center text-sm text-muted-foreground">
                {{ T.ningunTipo }}
              </ComboboxEmpty>
              <ComboboxItem
                v-for="t in tiposVisibles"
                :key="t.codigo"
                :value="t.codigo"
                :text-value="t.nombre"
                :class="cn(
                  'relative flex w-full cursor-default items-center gap-2 rounded-md py-1.5 pr-8 pl-2 text-sm outline-hidden select-none',
                  'data-highlighted:bg-accent data-highlighted:text-accent-foreground',
                )"
              >
                <span class="w-7 shrink-0 font-mono text-xs font-medium">{{ t.codigo }}</span>
                <span>{{ t.nombre }}</span>
                <ComboboxItemIndicator class="absolute right-2 flex size-4 items-center justify-center">
                  <Icon name="check" />
                </ComboboxItemIndicator>
              </ComboboxItem>
            </ComboboxViewport>
          </ComboboxContent>
        </ComboboxPortal>
      </ComboboxRoot>
    </div>
    <div :class="compacto ? 'min-w-0 flex-1' : 'grid content-start gap-2'">
      <Label :for="id('n')" :class="compacto && 'sr-only'">{{ T.numeroDocumento }}</Label>
      <Input
        :id="id('n')"
        ref="campoNumero"
        v-model="numero"
        name="bq-n"
        :inputmode="tipo === 'PA' ? 'text' : 'numeric'"
        :placeholder="ph('', 'Número')"
        :aria-describedby="id('pn')"
        v-bind="comunes"
      />
      <p :id="id('pn')" :class="compacto ? 'sr-only' : 'text-xs text-muted-foreground'">{{ T.pistaNumero }}</p>
    </div>
  </div>

  <!-- Nombre -->
  <div v-else :class="compacto ? 'relative flex w-full items-center' : 'grid gap-3'">
    <p :id="id('pa')" :class="compacto ? 'sr-only' : 'text-xs text-muted-foreground'">{{ T.pistaNombre }}</p>
    <div :class="compacto ? 'flex w-full items-center gap-1.5' : 'grid gap-3 sm:grid-cols-3'">
      <div :class="compacto ? 'min-w-0 flex-1' : 'grid content-start gap-2'">
        <Label :for="id('c1')" :class="compacto && 'sr-only'">{{ T.nombres }}</Label>
        <Input
          :id="id('c1')"
          v-model="nombres"
          name="bq-c1" :class="compacto && 'px-2'"
          :aria-describedby="id('pa')"
          :placeholder="ph('', T.nombres)"
          :title="compacto ? `${T.pistaNombre} ${T.llavePrevia} ${llavePrevia}` : undefined"
          data-bq-primero
          v-bind="comunes"
        />
      </div>
      <div :class="compacto ? 'min-w-0 flex-1' : 'grid content-start gap-2'">
        <Label :for="id('c2')" :class="compacto && 'sr-only'">{{ T.apellido1 }}</Label>
        <Input :id="id('c2')" v-model="apellido1" name="bq-c2" :class="compacto && 'px-2'" :aria-describedby="id('pa')" :placeholder="ph('', 'Primer apellido')" :title="compacto ? `${T.pistaNombre} ${T.llavePrevia} ${llavePrevia}` : undefined" v-bind="comunes" />
      </div>
      <div :class="compacto ? 'min-w-0 flex-1' : 'grid content-start gap-2'">
        <Label :for="id('c3')" :class="compacto && 'sr-only'">{{ T.apellido2 }}</Label>
        <Input :id="id('c3')" v-model="apellido2" name="bq-c3" :class="compacto && 'px-2'" :aria-describedby="id('pa')" :placeholder="ph('', 'Segundo (opcional)')" :title="compacto ? `${T.pistaNombre} ${T.llavePrevia} ${llavePrevia}` : undefined" v-bind="comunes" />
      </div>
    </div>
    <!-- En compacto la llave no ocupa ancho ni alto (la barra no debe cambiar de tamaño
         entre modos): se anuncia a lectores de pantalla, va en el `title` de los campos,
         y el eco después de buscar la muestra siempre (D4). -->
    <p
      :class="compacto ? 'sr-only' : 'flex flex-wrap items-baseline gap-x-2 text-sm text-muted-foreground'"
      data-testid="llave-previa"
      aria-live="polite"
    >
      <span>{{ T.llavePrevia }}</span>
      <span class="font-mono font-medium tracking-wide text-foreground">{{ llavePrevia }}</span>
    </p>
  </div>
</template>
