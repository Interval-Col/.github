// Contrato de estados de una búsqueda al servidor (plan de búsqueda, 0.3 y 0.8).
//
//   idle → incomplete → loading → results | no-results | error | rate-limited | forbidden | truncated
//
// más `stale` como bandera aparte: los datos que se ven son de una búsqueda anterior
// y el borrador ya cambió. Dos reglas que este módulo hace cumplir:
//   1. un error NUNCA se pinta como «sin resultados» (el bug de recepción);
//   2. truncado = se niega y se pide afinar, nunca una lista parcial (el LIS devuelve lo
//      más viejo primero, así que «los primeros» serían los menos útiles).

export type EstadoBusqueda =
  | 'idle'
  | 'incomplete'
  | 'loading'
  | 'results'
  | 'no-results'
  | 'error'
  | 'rate-limited'
  | 'forbidden'
  | 'truncated'

export const ESTADOS_FINALES: readonly EstadoBusqueda[] = [
  'results', 'no-results', 'error', 'rate-limited', 'forbidden', 'truncated',
]

const TRANSICIONES: Record<EstadoBusqueda, readonly EstadoBusqueda[]> = {
  'idle': ['incomplete', 'loading'],
  'incomplete': ['idle', 'incomplete', 'loading'],
  'loading': ['loading', 'idle', ...ESTADOS_FINALES],
  'results': ['idle', 'incomplete', 'loading'],
  'no-results': ['idle', 'incomplete', 'loading'],
  'error': ['idle', 'incomplete', 'loading'],
  'rate-limited': ['idle', 'incomplete', 'loading'],
  'forbidden': ['idle', 'incomplete', 'loading'],
  'truncated': ['idle', 'incomplete', 'loading'],
}

export function puedePasar(de: EstadoBusqueda, a: EstadoBusqueda): boolean {
  return TRANSICIONES[de].includes(a)
}

/** Qué falló, como lo devuelve el simulador o un cliente real. */
export type Falla = 'error' | 'rate-limited' | 'forbidden'

export class FallaBusqueda extends Error {
  constructor(public readonly tipo: Falla) {
    super(tipo)
    this.name = 'FallaBusqueda'
  }
}

/** Un 4xx/5xx de cualquier servicio → estado. Un 404 es «sin resultados» sólo si el servicio lo dice así. */
export function estadoDeHttp(status: number): Falla {
  if (status === 429) return 'rate-limited'
  if (status === 401 || status === 403) return 'forbidden'
  return 'error'
}
