<script setup lang="ts">
// PhysicianLookup — a thin preset over EntityLookup for physician search.
// Same component as PatientLookup, different qualifiers + data → the two stay
// visually + behaviourally identical (the HandlePatient/HandlePhysician fix).
import EntityLookup from './EntityLookup.vue'
import type { Physician } from './types'
import type { QualifierConfig, SearchToken } from '@/components/ui/scoped-search'

const emit = defineEmits<{ select: [physician: Physician] }>()

const qualifiers: QualifierConfig[] = [
  { key: 'nombre', label: 'Nombre', kind: 'text', placeholder: 'Nombre del médico…' },
  { key: 'registro', label: 'Registro', kind: 'text', placeholder: 'Registro / documento…' },
]

const MOCK: Physician[] = [
  { uuid: '1', name: 'Dra. Patricia Gómez', registry: 'RM-10293', specialty: 'Hematología' },
  { uuid: '2', name: 'Dr. Andrés Gómez Ruiz', registry: 'RM-20481', specialty: 'Patología' },
  { uuid: '3', name: 'Dra. Sofía Martínez', registry: 'RM-33120', specialty: 'Medicina interna' },
  { uuid: '4', name: 'Dr. Julián Restrepo', registry: 'RM-44875', specialty: 'Oncología' },
]

function mockSearch(tokens: SearchToken[]): Promise<Physician[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      const matches = MOCK.filter(p =>
        tokens.every((t) => {
          const v = t.value.toLowerCase()
          if (t.qualifier === 'nombre') return p.name.toLowerCase().includes(v)
          if (t.qualifier === 'registro') return p.registry.toLowerCase().includes(v)
          return true
        }),
      )
      resolve(matches)
    }, 350)
  })
}
</script>

<template>
  <EntityLookup
    :qualifiers="qualifiers"
    :search-fn="mockSearch"
    label-key="name"
    value-key="uuid"
    placeholder="Buscar médico — agrega un filtro…"
    @select="emit('select', $event)"
  >
    <template #result="{ item }">
      <span class="font-medium">{{ item.name }}</span>
      <span class="text-xs text-muted-foreground">{{ item.specialty }} · {{ item.registry }}</span>
    </template>
  </EntityLookup>
</template>
