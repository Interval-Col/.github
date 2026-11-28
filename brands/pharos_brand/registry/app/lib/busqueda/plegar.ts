// Plegado de texto para FILTRAR lo que ya está en pantalla (plan de búsqueda, 0.3).
// Hoy hay cuatro implementaciones distintas en las apps; ésta es la del estándar.
//
// Sólo para filtrar local. NUNCA para armar la llave de nombre del LIS: esa no quita
// tildes (ver `llave-nombre.ts`), porque COBOL compara los bytes que guardó.

/** Quita tildes y diéresis, pasa a minúsculas, colapsa espacios. La ñ se vuelve n. */
export function plegar(s: string | null | undefined): string {
  return (s ?? '')
    .normalize('NFD')
    .replace(/\p{M}/gu, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim()
}

/** ¿Cada palabra del término aparece en algún lado del texto? (orden libre). */
export function coincide(texto: string, termino: string): boolean {
  const t = plegar(termino)
  if (!t) return true
  const h = plegar(texto)
  return t.split(' ').every(p => h.includes(p))
}
