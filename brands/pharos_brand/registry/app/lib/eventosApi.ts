// eventosApi — el cliente de los eventos de Pháros · Organización, UNA fábrica compartida.
//
// 🔑 RFC 0013 / RFC 0017: el navegador habla SOLO con el backend de su propia app. Este cliente
// recibe `apiBase` (la ruta de la app anfitriona, relativa al origen, p. ej. `/<app>/api`) y
// llama únicamente a `${apiBase}/eventos…`. Rechaza cualquier base que no sea una ruta relativa:
// ni esquema, ni `//`, ni host. El BFF de la anfitriona reenvía a Organización con su secreto de
// servicio y el token de la persona; nada de eso pasa por aquí.
//
// Transporte: `fetch` del navegador, `credentials: 'same-origin'` (la sesión es la cookie del SSO).
// Si la app necesita un encabezado más (p. ej. el token CSRF), lo entrega en `headers()`.
//
// 🛑 Los errores NUNCA llevan lo que la persona escribió: el 422 del portón de datos de pacientes
// trae solo los NOMBRES de las reglas, y aquí tampoco se registra el cuerpo.
import type {
  CausaDeError,
  ContactoEnvio,
  ErrorDeEventos,
  EventoReportado,
  ReporteEnvio,
  ResumenEvento,
} from '../components/ui/eventos/types'
import { ERRORES } from '../components/ui/eventos/types'

export type FetchLike = (input: string, init?: RequestInit) => Promise<Response>

export interface EventosApiOpciones {
  /** Ruta de la app anfitriona, relativa al origen. Ejemplo genérico: `/mi-app/api`. */
  apiBase: string
  /** Encabezados extra por llamada (CSRF, etc.). Nunca el secreto de servicio: ese es del BFF. */
  headers?: () => Record<string, string>
  /** Para pruebas. Por omisión, el `fetch` del navegador. */
  fetch?: FetchLike
}

export class ErrorEventosApi extends Error {
  readonly detalle: ErrorDeEventos
  readonly status: number
  constructor(status: number, detalle: ErrorDeEventos) {
    super(detalle.mensaje)
    this.name = 'ErrorEventosApi'
    this.status = status
    this.detalle = detalle
  }
}

/** Valida y normaliza la base: ruta relativa, sin esquema, sin `//`, sin `..`, sin barra final. */
export function normalizarBase(base: string): string {
  const limpia = base.trim().replace(/\/+$/, '')
  if (!/^\/[A-Za-z0-9._~/-]*$/.test(limpia) || limpia.startsWith('//') || limpia.split('/').includes('..')) {
    throw new Error('apiBase debe ser una ruta relativa de la propia app (empieza con «/», sin host).')
  }
  return limpia
}

function causaDe(status: number): CausaDeError {
  if (status === 401) return 'sesion'
  if (status === 403) return 'permiso'
  if (status === 404) return 'apagado'
  if (status === 503) return 'reglas'
  if (status === 422) return 'validacion'
  return 'otro'
}

/** Un mensaje del servidor solo se pinta si es texto corto y plano (misma regla que PharosHelpChat). */
function mensajePropio(valor: unknown): string | null {
  if (typeof valor !== 'string') return null
  const t = valor.trim()
  if (!t || t.length > 300 || /^[<{[]/.test(t)) return null
  return t
}

/** Traduce la respuesta de error del BFF a un `ErrorDeEventos`. Exportada para probarla sola. */
export function interpretarError(status: number, cuerpo: unknown): ErrorDeEventos {
  const detail = (cuerpo && typeof cuerpo === 'object' ? (cuerpo as Record<string, unknown>).detail : undefined) as unknown
  // 422 del portón de datos de pacientes: { mensaje, reglas: [...] }
  if (status === 422 && detail && typeof detail === 'object' && !Array.isArray(detail) && Array.isArray((detail as { reglas?: unknown }).reglas)) {
    const reglas = ((detail as { reglas: unknown[] }).reglas).filter((r): r is string => typeof r === 'string')
    return { causa: 'phi', mensaje: ERRORES.phi, reglas }
  }
  // 422 de validación: { errores: [{ codigo, campo, mensaje }] }
  if (status === 422 && detail && typeof detail === 'object' && Array.isArray((detail as { errores?: unknown }).errores)) {
    const errores = (detail as { errores: { campo?: unknown, mensaje?: unknown }[] }).errores
    const campos = errores.map(e => e.campo).filter((c): c is string => typeof c === 'string')
    const propio = mensajePropio(errores.find(e => mensajePropio(e.mensaje))?.mensaje)
    return { causa: 'validacion', mensaje: propio ?? ERRORES.validacion, campos }
  }
  const causa = causaDe(status)
  // Solo un 4xx deja pasar el mensaje del servidor; el de un 5xx puede traer una traza.
  const propio = status >= 400 && status < 500 ? mensajePropio(detail) : null
  return { causa, mensaje: propio ?? ERRORES[causa] }
}

export function crearEventosApi(opciones: EventosApiOpciones) {
  const base = normalizarBase(opciones.apiBase)
  const llamar: FetchLike = opciones.fetch ?? ((url, init) => globalThis.fetch(url, init))

  async function pedir<T>(metodo: string, ruta: string, cuerpo?: unknown): Promise<T> {
    const encabezados: Record<string, string> = { Accept: 'application/json', ...(opciones.headers?.() ?? {}) }
    if (cuerpo !== undefined) encabezados['Content-Type'] = 'application/json'
    let res: Response
    try {
      res = await llamar(`${base}/eventos${ruta}`, {
        method: metodo,
        headers: encabezados,
        credentials: 'same-origin',
        body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
      })
    } catch {
      throw new ErrorEventosApi(0, { causa: 'red', mensaje: ERRORES.red })
    }
    if (!res.ok) {
      let cuerpoError: unknown = null
      try { cuerpoError = await res.json() } catch { /* cuerpo vacío o no JSON */ }
      throw new ErrorEventosApi(res.status, interpretarError(res.status, cuerpoError))
    }
    if (res.status === 204) return undefined as T
    return (await res.json()) as T
  }

  return {
    /** POST /eventos → 201 */
    reportar: (cuerpo: ReporteEnvio) => pedir<EventoReportado>('POST', '', cuerpo),
    /** GET /eventos?vista=… → 200 */
    listar: (vista: 'mis_procesos' | 'mis_reportes' = 'mis_procesos') =>
      pedir<ResumenEvento[]>('GET', `?vista=${vista}`),
    /** PUT /eventos/{id}/contacto → 204 (solo quejas) */
    guardarContacto: (id: string, cuerpo: ContactoEnvio) =>
      pedir<void>('PUT', `/${encodeURIComponent(id)}/contacto`, cuerpo),
  }
}

export type EventosApi = ReturnType<typeof crearEventosApi>
