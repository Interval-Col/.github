export interface QueueWaitingRow {
  /** 1-based arrival position — the first row is who `call-next` would claim. */
  position: number
  /** Queue row id in the owning queue service (admission-patient today). */
  queueId: number
  /** Patient full name, already joined by the app. PHI — mask via `revealed`. */
  fullName: string
  /** Document type label (CC, TI, …). */
  documentType?: string
  /** Document number. PHI — mask via `revealed`. */
  documentNumber?: string
  /** Order numbers reception attached to the turn. Empty is legitimate. */
  orders: string[]
  /** ISO timestamp of when the row entered the waiting state. */
  waitingSince?: string | null
}
