/** What the widget knows about the form it is showing. The APP resolves this
 *  from the signature service (catalog / `by_order`); the widget never fetches. */
export interface ConsentFormDescriptor {
  /** `pdf_form.id` in the signature service — the id `POST /pdf_form/fill/{id}` takes. */
  id: number
  /** `pdf_form.internal_name` (e.g. `data_treatment`, `consent_bone_marrow_aspiration_and_biopsy`). */
  internalName: string
  /** Human title printed on the card. */
  name: string
  /** The 13 bench forms allow a legal representative to sign; `data_treatment` does not. */
  allowsLegalRepresentative: boolean
  /** The form carries a bacteriologist signature slot (filled by the service from the SSO profile). */
  requiresBacteriologist: boolean
  /** The form prints the city where the SIGNER's document was issued (14 of 15;
   *  `data_treatment` is the only one that does not print it). */
  requiresExpeditionCity: boolean
  /** The form ALSO prints the city where the PATIENT's own document was issued — a
   *  separate box, and a different value from the signer's only when a legal
   *  representative signs. Ten forms print both. */
  requiresPatientExpeditionCity: boolean
  /** The form prints the entity (EPS) the patient is served by. */
  requiresEntityServed: boolean
  /** Extra declarations some forms print as checkboxes. */
  hasSampleConservationChoice: boolean
  hasMicroscopicImagesChoice: boolean
}

/** Who is signing, already resolved by the app. PHI — mask via `revealed`. */
export interface ConsentSubject {
  identificationType: string
  identificationNumber: string
  /** Display only; the service re-reads the patient from CobolQL. */
  fullName?: string
  /** Pre-fills `patient_identification_expedition_place` when the app knows it. */
  expeditionPlace?: string
}

/** The bacteriologist at the bench, display only (the service takes the
 *  signature image from the SSO profile behind the token). */
export interface ConsentBacteriologist {
  fullName: string
  identificationNumber?: string
}

/** The canonical `POST /pdf_form/fill/{id}` body — 13 fields, snake_case as the
 *  service expects. `signature_image` / `legal_representative_signature` are
 *  PNG **base64 without the data-URL prefix** (the service `b64decode`s them).
 *  This is the ONLY shape any surface may send (RFC 0030 enmienda 2026-08-26). */
export interface ConsentSignaturePayload {
  identification_number: string
  identification_type: string
  signature_image: string
  identification_expedition_city: string | null
  legal_representative_name: string | null
  legal_representative_identification: string | null
  legal_representative_identification_type: string | null
  patient_identification_expedition_place: string | null
  order_number: number | null
  entity_served: string | null
  authorize_conservation_of_biological_samples: boolean | null
  authorize_the_use_of_microscopic_images: boolean | null
  legal_representative_signature: string
}

export interface IdentificationTypeOption {
  value: string
  label: string
}

export const IDENTIFICATION_TYPES: IdentificationTypeOption[] = [
  { value: 'NATIONAL_ID', label: 'Cédula de ciudadanía' },
  { value: 'UNDERAGE_NATIONAL_ID', label: 'Tarjeta de identidad' },
  { value: 'CIVIL_REGISTRY', label: 'Registro civil' },
  { value: 'INTERNATIONAL_ID', label: 'Cédula de extranjería' },
  { value: 'PASSPORT', label: 'Pasaporte' },
  { value: 'SPECIAL_PERMIT', label: 'Permiso especial' },
]
