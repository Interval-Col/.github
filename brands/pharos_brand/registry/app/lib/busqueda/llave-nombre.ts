// Llave de nombre del LIS — porte EXACTO de `name_key()` en
// pharos-lis `lab-qc/backend/app/services/cobolql/client.py` (origin/develop, 2026-11-27).
//
//   def name_key(value): return (value or "").strip().upper()[:3]
//
// Qué hace y qué NO hace, igual que el servidor:
//   • recorta espacios de los extremos y pasa a mayúsculas;
//   • toma las primeras 3 letras (COBOL guarda `PIC XXX`: más de 3 las corta él solo);
//   • NO quita tildes: «Ángela» → «ÁNG». COBOL compara los bytes que guardó, y adivinar
//     una transliteración convertiría «no encuentra» en «encuentra al equivocado»;
//   • NO trata partículas: «de la Cruz» → «DE ». Queda como pregunta abierta en la ficha.
//
// Por eso el eco de la llave es obligatorio (D4): quien busca ve exactamente qué
// 3+3+3 letras fueron al LIS, aunque haya escrito la palabra completa.

import type { ConsultaNombre } from './tipos'

export type { ConsultaNombre }

export const LETRAS_LLAVE = 3

export function llave(valor: string | null | undefined): string {
  // `toUpperCase` de JS y `upper()` de Python coinciden en el español (ñ → Ñ, á → Á).
  return (valor ?? '').trim().toUpperCase().slice(0, LETRAS_LLAVE)
}

export interface LlaveNombre {
  nombres: string
  apellido1: string
  apellido2: string
}

export function llaveDeNombre(c: ConsultaNombre): LlaveNombre {
  return { nombres: llave(c.nombres), apellido1: llave(c.apellido1), apellido2: llave(c.apellido2) }
}

/**
 * Las mismas dos negativas del servidor, antes de preguntar:
 * los nombres son obligatorios (COBOL no busca sin ellos) y hace falta al menos un
 * apellido (sin él, COBOL recorre a todos los que comparten 3 letras de nombre).
 */
export function faltaEnNombre(c: ConsultaNombre): 'nombres' | 'apellido' | null {
  const k = llaveDeNombre(c)
  if (!k.nombres) return 'nombres'
  if (!k.apellido1 && !k.apellido2) return 'apellido'
  return null
}

/** «ANA · EJE · PRU» — el texto del eco. Un apellido vacío no se muestra. */
export function ecoDeLlave(k: LlaveNombre): string {
  return [k.nombres, k.apellido1, k.apellido2].filter(Boolean).join(' · ')
}
