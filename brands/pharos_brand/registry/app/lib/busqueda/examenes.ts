// Encontrar un examen por cualquiera de sus claves (plan de búsqueda, 0.6):
// nombre, código LIS, CUPS, sinónimo o abreviatura, y enfermedad relacionada.
// Cada coincidencia dice POR QUÉ coincidió («Coincide por: sinónimo «HbA1c»»).
//
// El mapa de sinónimos y enfermedades lo mantendrá quien cuida el catálogo en lab-qc
// (D23 (a), German 2026-11-27). Aquí es el mapa de prueba de `datos.ts`.

import type { Examen } from './tipos'
import { plegar } from './plegar'

export type ClaveExamen = 'nombre' | 'codigo' | 'cups' | 'sinonimo' | 'enfermedad'

export const NOMBRE_CLAVE: Record<ClaveExamen, string> = {
  nombre: 'nombre',
  codigo: 'código LIS',
  cups: 'CUPS',
  sinonimo: 'sinónimo',
  enfermedad: 'enfermedad',
}

export interface CoincidenciaExamen {
  examen: Examen
  clave: ClaveExamen
  valor: string
}

const ORDEN: ClaveExamen[] = ['nombre', 'codigo', 'cups', 'sinonimo', 'enfermedad']

function valores(e: Examen, clave: ClaveExamen): string[] {
  switch (clave) {
    case 'nombre': return [e.nombre]
    case 'codigo': return [e.codigo]
    case 'cups': return [e.cups]
    case 'sinonimo': return e.sinonimos
    case 'enfermedad': return e.enfermedades
  }
}

/**
 * Coincidencias en orden de clave (nombre primero, enfermedad al final) y, dentro de
 * cada clave, las que empiezan por el término antes que las que sólo lo contienen.
 * Un examen aparece una sola vez, por su mejor clave.
 */
export function buscarExamenes(
  catalogo: readonly Examen[],
  termino: string,
  claves: readonly ClaveExamen[] = ORDEN,
): CoincidenciaExamen[] {
  const t = plegar(termino)
  if (!t) return catalogo.map(examen => ({ examen, clave: 'nombre' as const, valor: examen.nombre }))
  const vistos = new Set<string>()
  const empiezan: CoincidenciaExamen[] = []
  const contienen: CoincidenciaExamen[] = []
  for (const clave of ORDEN.filter(c => claves.includes(c))) {
    for (const examen of catalogo) {
      if (vistos.has(examen.codigo)) continue
      for (const valor of valores(examen, clave)) {
        const v = plegar(valor)
        if (v.startsWith(t) || v.split(' ').some(p => p.startsWith(t))) {
          empiezan.push({ examen, clave, valor }); vistos.add(examen.codigo); break
        }
        if (v.includes(t)) {
          contienen.push({ examen, clave, valor }); vistos.add(examen.codigo); break
        }
      }
    }
  }
  return [...empiezan, ...contienen]
}

export function textoCoincidencia(c: CoincidenciaExamen): string {
  return c.clave === 'nombre' ? '' : `Coincide por ${NOMBRE_CLAVE[c.clave]} «${c.valor}»`
}
