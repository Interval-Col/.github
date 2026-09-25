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

// ⚠️ LOS DOCUMENTOS SON SINTÉTICOS A PROPÓSITO — dígitos repetidos, no un patrón
// que parezca una cédula. Este repo es el ÚNICO PÚBLICO de la organización, y un
// número de documento realista acá es indistinguible de uno real para quien lo
// lea desde fuera. Saneados el 2026-09-12, cuando la regla de PHI de gitleaks
// (`lch-phi-colombian-document`) los marcó al subirla al config canónico: tres de
// los cinco disparaban el gate. La convención es la misma del resto del estate —
// repetidos o secuencia estricta — para que el marcador se lea como marcador.
// Los `order` ya eran de 4 dígitos, que no puede ser una orden del LIS (6-8).
// Mock data + search (prototype only).
const MOCK: Patient[] = [
  { uuid: '1', name: 'María García López', docType: 'CC', docNumber: '11111111', order: '9876' },
  { uuid: '2', name: 'Carlos García Niño', docType: 'CC', docNumber: '22222222', order: '9912' },
  { uuid: '3', name: 'Ana María Rodríguez', docType: 'TI', docNumber: '33333333', order: '9810' },
  { uuid: '4', name: 'José García Mora', docType: 'CE', docNumber: 'E4444444', order: '9745' },
  { uuid: '5', name: 'Lucía Fernández Gil', docType: 'CC', docNumber: '55555555', order: '9701' },
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
