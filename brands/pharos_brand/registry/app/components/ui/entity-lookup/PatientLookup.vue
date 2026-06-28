<script setup lang="ts">
// PatientLookup — a thin preset over EntityLookup for patient search. Prototype
// uses a MOCK searchFn; in production it routes tokens to the real backends
// (exact doc GET / demographic POST / order lookup). The point: this and
// PhysicianLookup share EntityLookup, so the two pages look + behave identically.
import EntityLookup from './EntityLookup.vue'
import type { Patient } from './types'
import type { QualifierConfig, SearchToken } from '@/components/ui/scoped-search'

const emit = defineEmits<{ select: [patient: Patient] }>()

const qualifiers: QualifierConfig[] = [
  { key: 'cc', label: 'Cédula', kind: 'document', placeholder: 'Número de documento…', docTypes: [
    { value: 'CC', label: 'Cédula de ciudadanía' },
    { value: 'TI', label: 'Tarjeta de identidad' },
    { value: 'CE', label: 'Cédula de extranjería' },
    { value: 'PA', label: 'Pasaporte' },
  ] },
  { key: 'nombre', label: 'Nombre', kind: 'text', placeholder: 'Nombre del paciente…' },
  { key: 'orden', label: 'N° de orden', kind: 'text', placeholder: 'Número de orden…' },
  { key: 'tel', label: 'Teléfono', kind: 'text', placeholder: 'Teléfono…' },
]

// Mock data + search (prototype only).
const MOCK: Patient[] = [
  { uuid: '1', name: 'María García López', docType: 'CC', docNumber: '12345678', order: '9876' },
  { uuid: '2', name: 'Carlos García Niño', docType: 'CC', docNumber: '80123456', order: '9912' },
  { uuid: '3', name: 'Ana María Rodríguez', docType: 'TI', docNumber: '1002003004', order: '9810' },
  { uuid: '4', name: 'José García Mora', docType: 'CE', docNumber: 'E456789', order: '9745' },
  { uuid: '5', name: 'Lucía Fernández Gil', docType: 'CC', docNumber: '52998877', order: '9701' },
]

function mockSearch(tokens: SearchToken[]): Promise<Patient[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      const matches = MOCK.filter(p =>
        tokens.every((t) => {
          const v = t.value.toLowerCase()
          if (t.qualifier === 'cc') return p.docNumber.toLowerCase().includes(v) && (!t.docType || p.docType === t.docType)
          if (t.qualifier === 'nombre') return p.name.toLowerCase().includes(v)
          if (t.qualifier === 'orden') return p.order.includes(t.value)
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
    placeholder="Buscar paciente — agrega un filtro…"
    @select="emit('select', $event)"
  >
    <template #result="{ item }">
      <span class="font-medium">{{ item.name }}</span>
      <span class="text-xs text-muted-foreground">{{ item.docType }} {{ item.docNumber }} · #{{ item.order }}</span>
    </template>
  </EntityLookup>
</template>
