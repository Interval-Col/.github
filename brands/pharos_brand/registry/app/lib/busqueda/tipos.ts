// Tipos del estándar de búsqueda que viajan al registry (plan de búsqueda, 0.3).
// No dependen de los datos sintéticos ni del simulador del Playground: cada app
// conecta su propio cliente a estas formas.

export type Fuente = 'pharos' | 'lis'
export type Sexo = 'F' | 'M'

/** Lo que el Buscador sabe pintar por defecto de una persona encontrada. */
export interface PacienteBuscado {
  id: string
  /** Tipo y número de documento; una búsqueda por nombre en el LIS no los trae. */
  tipo?: string
  numero?: string
  nombres: string
  apellido1: string
  apellido2: string
  /** ISO YYYY-MM-DD. */
  nacimiento?: string
  sexo?: Sexo
}

export interface ConsultaNombre {
  nombres: string
  apellido1: string
  apellido2?: string
}

export type ConsultaPaciente =
  | { modo: 'orden', orden: string }
  | { modo: 'documento', tipo: string, numero: string }
  | ({ modo: 'nombre' } & ConsultaNombre)

export interface Respuesta<T> {
  filas: T[]
  /** Dónde se buscó: el «sin resultados» dice «en Pháros» o «en el LIS». */
  fuente: Fuente
  /** Demasiadas coincidencias: se niega y pide afinar, nunca una lista parcial. */
  truncado: boolean
}

/** Un examen del catálogo, con las claves por las que se puede encontrar. */
export interface Examen {
  codigo: string
  nombre: string
  cups: string
  sinonimos: string[]
  enfermedades: string[]
  seccion: string
}

export function nombreCompleto(p: Pick<PacienteBuscado, 'nombres' | 'apellido1' | 'apellido2'>): string {
  return [p.nombres, p.apellido1, p.apellido2].filter(Boolean).join(' ')
}

/** Edad en años cumplidos a una fecha dada (por defecto, hoy). */
export function edad(nacimiento: string, hoy = new Date()): number {
  const [y, m, d] = nacimiento.split('-').map(Number) as [number, number, number]
  let e = hoy.getFullYear() - y
  if (hoy.getMonth() + 1 < m || (hoy.getMonth() + 1 === m && hoy.getDate() < d)) e--
  return e
}
