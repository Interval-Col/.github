// Shared types for the Pháros scoped (filter-chip) search — RFC 0008 component
// library, Phase 1.2. Kept in a plain .ts module so the component, the presets,
// and consumers can import them without an SFC import cycle.

/** One configured filter dimension the operator can add (e.g. Cédula, Nombre). */
export interface QualifierConfig {
  /** Stable machine key, e.g. 'cc' | 'nombre' | 'orden' | 'tel'. */
  key: string
  /** Human label shown in the picker + the pill, e.g. 'Cédula'. */
  label: string
  /**
   * 'text' — a single free-text value.
   * 'document' — an identity document: the operator first picks a TYPE
   * (CC/TI/CE/PA), then types the number. The type stays bound to the value
   * (identity-safety: a bare number is never ambiguous about its document type).
   */
  kind: 'text' | 'document'
  /** Allowed document types — required when kind === 'document'. */
  docTypes?: { value: string, label: string }[]
  /** Placeholder for the value input while this qualifier is being filled. */
  placeholder?: string
}

/** A committed filter pill. The structured unit the parent turns into a query. */
export interface SearchToken {
  /** The qualifier key it was built from. */
  qualifier: string
  /** The qualifier label (denormalized for rendering without the config). */
  label: string
  /** The typed value. */
  value: string
  /** Document type, present only for document qualifiers (e.g. 'CC'). */
  docType?: string
}
