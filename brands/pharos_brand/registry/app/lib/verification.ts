// Estado de VERIFICACIÓN de una vista (PROT-SW-001, lch-kb fase-0).
//
// Esto NO es un badge «beta» inventado. Es la cara de pantalla de un estado que el
// sistema documental del laboratorio ya define. `PROT-SW-001` §6 dice, literalmente,
// que mientras no se cumplan las tres condiciones de liberación la funcionalidad
// «puede estar DESPLEGADA Y EN USO EN PARALELO, pero NO se retira su predecesora».
// Ese es exactamente el estado que la banda pinta: la vista funciona, se usa, y el
// sistema que sustituye sigue siendo el patrón de referencia.
//
// Reglas que vienen de la norma, no del diseño:
//
//  1. `liberada` NO RENDERIZA NADA. La ausencia de la marca ES el estado liberado.
//     Un sello verde de «verificado» es una atestación que envejece: nadie la quita
//     cuando deja de ser cierta, y a los seis meses la pantalla afirma algo que ya
//     nadie sostiene. Solo se dibuja lo que RESTRINGE al usuario.
//  2. El responsable va NOMBRE + CARGO, nunca un @handle ni un identificador
//     técnico (`SOP-000` §4). Una vista que dice «responsable: @gczuluaga» no le
//     sirve a un auditor ni a la persona del mesón.
//  3. `no-conforme-acotado` EXIGE `restriccion` (`PROT-SW-001` §6.1): ese estado solo
//     existe si hay una restricción operativa escrita y verificable. Sin el texto de
//     la restricción, la marca afirmaría una salvaguarda que no está declarada.
//  4. CERO datos de paciente acá (`PROT-SW-001` §8). Este archivo describe software.
//
// El expediente concreto de una entrega (`FOR-SW-001`) es un REGISTRO y vive fuera
// de git — acá solo se referencia por código, nunca se transcribe.
//
// ── DÓNDE VIVE QUÉ ──
// Este archivo es del REGISTRY: vocabulario, tipos y reglas, iguales en todas las
// apps. El MANIFIESTO —qué vista está en qué estado y quién responde— es de la APP:
// `app/verification.manifest.ts`, que el sync copia una vez y nunca vuelve a tocar.
// Esa frontera es deliberada: el manifiesto nombra personas y entregas concretas, y
// se revisa en el PR de esa app. Un archivo del sistema de diseño que lo cargara
// estaría diciendo que el registry decide quién responde por una vista clínica.
import { VERIFICATION_MANIFEST } from '~/verification.manifest'

export type VerificationState =
  | 'en-verificacion'      // desplegada, en uso en paralelo, NO liberada
  | 'no-conforme-acotado'  // liberada CON restricción operativa escrita (§6.1)
  | 'no-conforme'          // no liberada; una dimensión falló
  | 'liberada'             // cumple §6 — no dibuja nada

/** Quien responde por la verificación. Nombre + cargo (SOP-000 §4), nunca un handle. */
export interface Responsable {
  nombre: string
  cargo: string
}

export interface ViewVerification {
  estado: VerificationState
  responsable: Responsable
  /** Protocolo que gobierna. Default: PROT-SW-001. */
  protocolo?: string
  /** Código del expediente de la entrega (FOR-SW-001 …). Referencia, nunca contenido. */
  expediente?: string
  /** Fecha en que la vista entró en verificación (ISO). */
  desde?: string
  /**
   * Fecha en que la entrada debe revisarse. Una marca sin caducidad se vuelve
   * mobiliario: sigue en pantalla mucho después de dejar de ser cierta, y entonces
   * la gente deja de leerla — que es peor que no tenerla. El gate
   * `check-view-verification.mjs` FALLA cuando esta fecha queda atrás.
   */
  revisarAntes?: string
  /** Restricción operativa. OBLIGATORIA en `no-conforme-acotado` (§6.1). */
  restriccion?: string
}

interface StateMeta {
  /** Titular de la banda. Corto: se lee de pie, de lejos. */
  label: string
  /** Qué implica para quien está usando la vista AHORA. */
  leyenda: string
  /** Clave del registro curado de iconos (app/components/ui/icon/icons.ts). */
  icon: string
  /** `false` = el estado no dibuja nada (ver regla 1). */
  renders: boolean
}

export const VERIFICATION_STATES: Record<VerificationState, StateMeta> = {
  'en-verificacion': {
    label: 'En verificación · no liberada',
    leyenda: 'Uso en paralelo. El sistema anterior sigue siendo la referencia.',
    icon: 'waitingRoom',
    renders: true,
  },
  'no-conforme-acotado': {
    label: 'Liberada con restricción',
    leyenda: 'Autorizada solo dentro del límite declarado abajo.',
    icon: 'warning',
    renders: true,
  },
  'no-conforme': {
    label: 'No conforme · no liberada',
    leyenda: 'No la use como fuente para decisiones clínicas.',
    icon: 'ban',
    renders: true,
  },
  liberada: {
    label: 'Liberada',
    leyenda: '',
    icon: 'success',
    renders: false,
  },
}

/**
 * Registros de color. La app escoge UNO (spec `family.md` § *Vista en verificación*;
 * default de familia = `verify`, el token propio). El estado no escoge — salvo
 * `no-conforme`, ver `toneFor()`.
 */
export const VERIFICATION_TONES = [
  { id: 'verify', label: 'Token propio', hint: 'Violeta fuera de la paleta clínica — no compite con ⚠/✓ de resultados' },
  { id: 'warning', label: 'Ámbar (status-warning)', hint: 'Reusa la paleta bloqueada; choca con las marcas clínicas ámbar' },
  { id: 'error', label: 'Carmesí (status-error)', hint: 'Máxima alarma; se lee como «esta vista está rota»' },
  { id: 'neutral', label: 'Neutro', hint: 'Sin hue propio; sobrevive B/N pero pierde el grito' },
] as const

export type VerificationTone = typeof VERIFICATION_TONES[number]['id']

/** Cuánto cromo ocupa la banda. */
export const VERIFICATION_DENSITIES = [
  { id: 'completa', label: 'Completa', hint: 'Titular + leyenda + responsable + expediente' },
  { id: 'compacta', label: 'Compacta', hint: 'Una línea: titular + responsable' },
  { id: 'franja', label: 'Franja', hint: 'Tira delgada; el lavado del lienzo carga el mensaje' },
] as const

export type VerificationDensity = typeof VERIFICATION_DENSITIES[number]['id']

/**
 * Registro de color EFECTIVO de un estado.
 *
 * `no-conforme` rompe el registro escogido por la app y va **siempre** en la tinta de
 * error (German, 2026-08-13). Su mensaje —«no la use como fuente para decisiones
 * clínicas»— es alarma clínica, no nota meta: es el único de los tres estados donde
 * chocar con el rojo de resultados es aceptable, porque lo que dice es «pare», no
 * «tenga en cuenta». Los otros dos sí siguen el registro, y esa diferencia hace que
 * la escalada se lea sin tener que leerla.
 */
export function toneFor(estado: VerificationState, tone: VerificationTone): VerificationTone {
  return estado === 'no-conforme' ? 'error' : tone
}

/**
 * Estado de verificación de una ruta, leído del manifiesto de la app.
 * `undefined` = liberada / no aplica ⇒ la vista se renderiza sin marca.
 */
export function verificationFor(path: string): ViewVerification | undefined {
  const v = VERIFICATION_MANIFEST[path]
  if (!v || !VERIFICATION_STATES[v.estado].renders) return undefined
  return v
}
