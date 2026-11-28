// Atajos del Rango de fechas, calculados en America/Bogota (plan de búsqueda, 0.7).
// Compartidos por DateRange y DateRangeCompacto.
import { CalendarDate, today } from '@internationalized/date'
import { TEXTOS } from '../../../lib/busqueda/textos'

export interface RangoFechas { desde: string | null, hasta: string | null }
export type Atajo = 'hoy' | 'ayer' | 'ultimos7' | 'esteMes' | 'personalizado'

export const ZONA = 'America/Bogota'
export const ATAJOS: { id: Atajo, texto: string }[] = [
  { id: 'hoy', texto: TEXTOS.rango.hoy },
  { id: 'ayer', texto: TEXTOS.rango.ayer },
  { id: 'ultimos7', texto: TEXTOS.rango.ultimos7 },
  { id: 'esteMes', texto: TEXTOS.rango.esteMes },
  { id: 'personalizado', texto: TEXTOS.rango.personalizado },
]

function iso(d: CalendarDate): string {
  return `${String(d.year).padStart(4, '0')}-${String(d.month).padStart(2, '0')}-${String(d.day).padStart(2, '0')}`
}

export function rangoDe(atajo: Exclude<Atajo, 'personalizado'>): RangoFechas {
  const t = today(ZONA)
  const hoy = new CalendarDate(t.year, t.month, t.day)
  switch (atajo) {
    case 'hoy': return { desde: iso(hoy), hasta: iso(hoy) }
    case 'ayer': { const a = hoy.subtract({ days: 1 }); return { desde: iso(a), hasta: iso(a) } }
    case 'ultimos7': return { desde: iso(hoy.subtract({ days: 6 })), hasta: iso(hoy) }
    case 'esteMes': return { desde: iso(hoy.set({ day: 1 })), hasta: iso(hoy) }
  }
}

/** Qué atajo describen estas fechas; «personalizado» si ninguno; null si no hay fechas. */
export function detectar(r: RangoFechas): Atajo | null {
  if (!r.desde && !r.hasta) return null
  for (const a of ATAJOS) {
    if (a.id === 'personalizado') continue
    const e = rangoDe(a.id)
    if (e.desde === r.desde && e.hasta === r.hasta) return a.id
  }
  return 'personalizado'
}

/** El nombre del atajo para un resumen («Este mes»), o vacío si es personalizado. */
export function etiquetaAtajo(r: RangoFechas): string {
  const a = detectar(r)
  return a && a !== 'personalizado' ? ATAJOS.find(x => x.id === a)!.texto : ''
}

/** Hoy menos `dias`, en Bogotá, como ISO: para rangos por defecto de una pantalla. */
export function isoHaceDias(dias: number): string {
  return iso(today(ZONA).subtract({ days: dias }) as unknown as CalendarDate)
}
