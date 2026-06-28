// Demo entity types for the prototype presets (production would import the real
// domain models). Kept here so the SFCs stay single-<script setup> blocks.

export interface Patient {
  uuid: string
  name: string
  docType: string
  docNumber: string
  order: string
}

export interface Physician {
  uuid: string
  name: string
  registry: string
  specialty: string
}
