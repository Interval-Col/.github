<script setup lang="ts">
// ListFilter — «Filtro de lista» (plan de búsqueda, 0.4). Estrecha lo que YA está en
// pantalla; nunca llama a un servicio. Sólo reporta el término: la página filtra con
// `useSearchText`.
import { useId } from 'vue'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { TEXTOS } from '@/lib/busqueda/textos'

const props = withDefaults(defineProps<{
  total: number
  visibles: number
  etiqueta?: string
  placeholder?: string
  /** Una sola línea: etiqueta, cuadro y conteo lado a lado (barras de herramientas). */
  compacto?: boolean
}>(), {
  etiqueta: TEXTOS.filtro.etiqueta,
  placeholder: TEXTOS.filtro.placeholder,
})

const termino = defineModel<string>({ default: '' })
const id = useId()
</script>

<template>
  <div :class="props.compacto ? 'flex min-w-0 items-center gap-2' : 'flex flex-col gap-1.5'">
    <Label :for="id" :class="props.compacto && 'shrink-0'">{{ props.etiqueta }}</Label>
    <div class="relative" :class="props.compacto && 'w-48 min-w-0 shrink'">
      <Input
        :id="id"
        v-model="termino"
        type="text"
        autocomplete="off"
        :placeholder="props.placeholder"
        class="pr-10"
        @keydown.esc="termino = ''"
      />
      <Button
        v-if="termino"
        type="button"
        variant="ghost"
        size="icon-sm"
        class="absolute right-0.5 top-0.5 size-8"
        :aria-label="TEXTOS.filtro.quitar"
        @click="termino = ''"
      >
        <Icon name="close" :size="4" />
      </Button>
    </div>
    <p aria-live="polite" class="text-sm tabular-nums text-muted-foreground" :class="props.compacto ? 'shrink-0 whitespace-nowrap' : 'min-h-5'">
      <template v-if="props.total > 0">
        {{ TEXTOS.filtro.mostrando(props.visibles, props.total) }}
      </template>
    </p>
  </div>
</template>
