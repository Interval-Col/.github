<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { TEXTOS } from '@/lib/busqueda/textos'

defineProps<{ termino: string }>()
const emit = defineEmits<{ quitar: [] }>()
</script>

<template>
  <div class="flex flex-col items-center gap-3 rounded-md border border-dashed p-6 text-center">
    <p class="text-sm text-muted-foreground">{{ TEXTOS.filtro.ninguna(termino) }}</p>
    <Button type="button" variant="outline" size="sm" @click="emit('quitar')">
      {{ TEXTOS.filtro.quitar }}
    </Button>
  </div>
</template>
