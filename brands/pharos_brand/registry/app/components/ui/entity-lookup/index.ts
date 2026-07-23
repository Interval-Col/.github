// Portable primitive barrel — exports ONLY what the sync copies into every app.
// PatientLookup / PhysicianLookup are app-local scaffold presets (SCAFFOLD_SKIP_RELPATHS
// in sync-pharos-registry.sh): they are NOT synced, so re-exporting them here left every
// selective adopter with a dangling import. Import a preset by its path instead
// (e.g. `import PatientLookup from '.../entity-lookup/PatientLookup.vue'`).
export { default as EntityLookup } from './EntityLookup.vue'
export type { Patient, Physician } from './types'
