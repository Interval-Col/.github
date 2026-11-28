// Tipos de documento — la única lista del módulo de búsqueda (plan de búsqueda, 0.3).
// Hoy hay ≥5 listas distintas en las apps; una sola fuente es lo que deja que el
// portón marque una sexta. Esta es estática para el prototipo: en la adopción, cada
// app la toma del backend (`useDocumentTypes`) con ésta como respaldo.
//
// Sin defecto (D8 (a), German 2026-11-27): ningún tipo viene escogido. El campo de
// tipo va primero y se escoge tecleando iniciales.

export interface TipoDocumento {
  /** Código que viaja al servidor. */
  codigo: string
  /** Nombre en español para la etiqueta. */
  nombre: string
}

export const TIPOS_DOCUMENTO: readonly TipoDocumento[] = [
  { codigo: 'CC', nombre: 'Cédula de ciudadanía' },
  { codigo: 'TI', nombre: 'Tarjeta de identidad' },
  { codigo: 'RC', nombre: 'Registro civil' },
  { codigo: 'CE', nombre: 'Cédula de extranjería' },
  { codigo: 'PA', nombre: 'Pasaporte' },
  { codigo: 'PT', nombre: 'Permiso por protección temporal' },
  { codigo: 'MS', nombre: 'Menor sin identificación' },
  { codigo: 'AS', nombre: 'Adulto sin identificación' },
]

export function tipoPorCodigo(codigo: string | null | undefined): TipoDocumento | undefined {
  return TIPOS_DOCUMENTO.find(t => t.codigo === codigo)
}

/**
 * Escoger por iniciales: «c» → CC y CE, «cc» → CC, «ced» → los que dicen cédula.
 * Compara contra el código y contra el nombre plegado (sin tildes ni mayúsculas).
 */
export function tiposQueEmpiezanPor(texto: string): TipoDocumento[] {
  const t = plegarSimple(texto)
  if (!t) return [...TIPOS_DOCUMENTO]
  return TIPOS_DOCUMENTO.filter(tipo =>
    plegarSimple(tipo.codigo).startsWith(t) || plegarSimple(tipo.nombre).startsWith(t),
  )
}

function plegarSimple(s: string): string {
  return s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().trim()
}
