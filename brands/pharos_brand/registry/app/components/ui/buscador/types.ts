// Tipos públicos del Buscador (plan de búsqueda, 0.5).
import type { BorradorBuscador, ModoBuscador } from '@/composables/useBuscador'
import type { ConsultaPaciente, Fuente, PacienteBuscado, Respuesta } from '@/lib/busqueda/tipos'

/** El tipo de fila por defecto del Buscador. */
export type Paciente = PacienteBuscado
export type { BorradorBuscador, ConsultaPaciente, Fuente, ModoBuscador, Respuesta }

/** Lo que el Buscador expone por `ref` a la pantalla que lo usa. */
export interface BuscadorExpuesto {
  /** Lleva el foco al primer campo del modo activo. */
  enfocar: () => void
  /** El mismo submit que el botón y Enter. */
  enviar: () => Promise<void>
  /** Llena campos del borrador (p. ej. desde un escaneo). No busca. */
  llenar: (parcial: Partial<BorradorBuscador>) => void
}

export const MODOS: readonly ModoBuscador[] = ['orden', 'documento', 'nombre']
