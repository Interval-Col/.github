// El vocabulario del visor del recorrido (RFC 0031, tarea 1.9).
//
// 🔑 Por qué el vocabulario vive en el REGISTRY y no en cada app: la matriz
// canónica de estados es de `pharos-queue` (`docs/state-machine.md`), y la
// pantalla sólo la TRADUCE. Si cada superficie escribiera sus etiquetas, la
// segunda las reinventaría — y dos pantallas llamando distinto al mismo estado
// es cómo una operadora termina sin saber si son dos cosas o una.
//
// ⚠️ Los nombres de estado NO se traducen: son el contrato con el servicio. Lo
// que se traduce es lo que lee la persona.

/** Un paso del recorrido, tal como lo rinde la cola. Sin datos de paciente. */
export interface QueueTraceStep {
  status: string
  created_by: string
  assigned_to?: string | null
  at: string
}

/** Quién manda en cada tramo. Es la mitad del «por qué». */
export type QueueTraceOwner = 'recepcion' | 'toma' | 'movimiento'

export interface QueueTraceStatusInfo {
  /** Lo que lee la operadora. */
  label: string
  /** La superficie que emite este estado, según la matriz canónica. */
  owner: QueueTraceOwner
}

// Los doce estados que las superficies conocen hoy, con su emisor medido.
//
// 💡 **Siete de estos doce tienen uso CERO** en 476 días de historia. No se
// omiten —un estado sin uso que aparece igual es justo lo que hay que poder
// leer— pero explica por qué casi todo recorrido real es
// `Waiting → Taken → Finished`.
export const QUEUE_TRACE_STATUS: Record<string, QueueTraceStatusInfo> = {
  Waiting: { label: 'En espera', owner: 'recepcion' },
  Taken: { label: 'Llamado a recepción', owner: 'recepcion' },
  Returned: { label: 'Devuelto a la espera', owner: 'recepcion' },
  Cancelled: { label: 'Cancelado', owner: 'recepcion' },
  TakenEvidences: { label: 'Evidencias tomadas', owner: 'recepcion' },
  FinishedReception: { label: 'Recepción terminada', owner: 'recepcion' },
  Finished: { label: 'Atención terminada', owner: 'recepcion' },
  // 🪤 Los dos «Waiting» de destino los emite RECEPCIÓN, no el destino: son «lo
  // mandé para allá», no «llegó allá». Es la confusión más fácil de esta tabla.
  SampleCollectionWaiting: { label: 'Enviado a toma de muestra', owner: 'recepcion' },
  SampleCollectionTaken: { label: 'Recibido en toma de muestra', owner: 'toma' },
  BiumanWaitingAttention: { label: 'Enviado a Movimiento', owner: 'recepcion' },
  BiumanInAttention: { label: 'En atención en Movimiento', owner: 'movimiento' },
  BiumanFinished: { label: 'Movimiento terminado', owner: 'movimiento' },
}

export const QUEUE_TRACE_OWNER_LABEL: Record<QueueTraceOwner, string> = {
  recepcion: 'Recepción',
  toma: 'Toma de muestra',
  movimiento: 'Movimiento',
}

/** Un estado que el servicio mande y esta tabla no conozca todavía.
 *
 * 🔑 Se muestra con su nombre crudo en vez de omitirse. El contrato tiene 14
 * estados y esta tabla conoce 12: un paso que desaparece hace que la historia
 * MIENTA por omisión, que es peor que mostrar un nombre técnico — quien lo lea
 * va a preguntar, y preguntar es el comportamiento correcto.
 */
export function queueTraceStatus(status: string): QueueTraceStatusInfo {
  return QUEUE_TRACE_STATUS[status] ?? { label: status, owner: 'recepcion' }
}

/** ¿El rastro se acaba acá porque el paciente pasó al laboratorio?
 *
 * 🔴 Ésta es la promesa honesta del visor: **la cola sólo sabe hasta la puerta
 * del laboratorio.** Cuando la muestra fue recibida en toma, lo que pasa después
 * vive en el LIS y este servicio no lo ve. Decirlo es la diferencia entre «no
 * hay más pasos» y «no sabemos qué más pasó» — y sólo la segunda es cierta.
 */
export function endsAtCobol(steps: Pick<QueueTraceStep, 'status'>[]): boolean {
  return steps[steps.length - 1]?.status === 'SampleCollectionTaken'
}
