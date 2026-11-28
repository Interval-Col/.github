// Enmascarado hasta revelar (D20, German 2026-11-26) — plan de búsqueda, 0.3.
// Documentos: •••+3 últimos. Nombres: inicial de cada palabra + asteriscos,
// detrás de «Mostrar» / «Ocultar».

export function enmascararDocumento(numero: string | null | undefined): string {
  const n = (numero ?? '').replace(/\s/g, '')
  if (!n) return ''
  return `•••${n.slice(-3)}`
}

/** «Ana Ejemplo Prueba» → «A** E****** P*****». Conserva la longitud de cada palabra. */
export function enmascararNombre(nombre: string | null | undefined): string {
  return (nombre ?? '')
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map(p => p[0] + '*'.repeat(Math.max(p.length - 1, 0)))
    .join(' ')
}
