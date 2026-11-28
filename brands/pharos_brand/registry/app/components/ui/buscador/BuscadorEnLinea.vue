<script setup lang="ts">
// BuscadorEnLinea — el Buscador en UNA línea, para una barra de herramientas
// (German, 2026-11-27: sin ventana aparte y sin quitarle alto a la tabla).
//
// Sólo edita el borrador y envía; NO pinta resultados. La pantalla es dueña del motor
// (`useBuscador`) y muestra lo que encontró donde le sirva (en Liberación, en la misma
// tabla, con un aviso «Volver a la bandeja»). Las reglas son las mismas del Buscador:
// un solo submit (botón o Enter), botón apagado hasta que el modo esté completo, tipo de
// documento sin defecto, llave de nombre a la vista.
import { Search } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import type { BorradorBuscador, ModoBuscador } from '@/composables/useBuscador'
import { TEXTOS } from '@/lib/busqueda/textos'
import BuscadorModo from './BuscadorModo.vue'
import { MODOS } from './types'

const props = withDefaults(defineProps<{
  modos?: readonly ModoBuscador[]
  valido: boolean
  cargando?: boolean
  /** Qué falta para poder buscar; va en el `title` del botón apagado. */
  falta?: string | null
  etiqueta?: string
}>(), { modos: () => MODOS, cargando: false, falta: null, etiqueta: 'Buscar por' })

const borrador = defineModel<BorradorBuscador>('borrador', { required: true })
const emit = defineEmits<{ enviar: [] }>()

function alEnter(e: KeyboardEvent) {
  if (e.defaultPrevented || e.isComposing) return
  if ((e.target as HTMLElement | null)?.tagName !== 'INPUT') return
  e.preventDefault()
  emit('enviar')
}

function alCambiarModo(m: string | number) {
  borrador.value.modo = m as ModoBuscador
}
</script>

<template>
  <!-- Enter siempre llega al motor (aunque el botón esté apagado): si falta algo, el
       motor queda en «incompleto» y la pantalla dice qué falta. Un Enter que ya usó el
       combobox (escoger un tipo) no llega aquí. -->
  <form role="search" autocomplete="off" class="flex flex-wrap items-center gap-1.5" @submit.prevent="emit('enviar')" @keydown.enter="alEnter">
    <Tabs :model-value="borrador.modo" class="flex flex-row flex-wrap items-center gap-1.5" @update:model-value="alCambiarModo">
      <TabsList :aria-label="props.etiqueta">
        <TabsTrigger v-for="m in props.modos" :key="m" :value="m" class="px-2">
          {{ TEXTOS.buscador.modos[m] }}
        </TabsTrigger>
      </TabsList>
      <!-- Mismo ancho en los tres modos (la barra no brinca al cambiar de modo), y crece
           con el espacio de la barra, no con el modo: angosto en un portátil de 1366 px,
           holgado en un monitor grande. Las medidas son del contenedor `@container` de la
           barra que lo usa (German, 2026-11-27: en su monitor los nombres no cabían). -->
      <TabsContent
        v-for="m in props.modos"
        :key="m"
        :value="m"
        class="mt-0 w-[15rem] max-w-full @[72rem]:w-[22rem] @[84rem]:w-[28rem] @[100rem]:w-[34rem]"
      >
        <BuscadorModo
          v-model:orden="borrador.orden"
          v-model:tipo="borrador.tipo"
          v-model:numero="borrador.numero"
          v-model:nombres="borrador.nombres"
          v-model:apellido1="borrador.apellido1"
          v-model:apellido2="borrador.apellido2"
          :modo="m"
          compacto
        />
      </TabsContent>
    </Tabs>
    <Button type="submit" :disabled="!props.valido" :title="props.falta ?? undefined" class="gap-1.5">
      <Search class="size-4" aria-hidden="true" />
      {{ props.cargando ? TEXTOS.estados.cargando : TEXTOS.buscador.buscar }}
    </Button>
  </form>
</template>
