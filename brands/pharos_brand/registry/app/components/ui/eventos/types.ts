// Tipos y textos del componente de eventos de Pháros · Organización (plan 2.4).
//
// Las formas de abajo son las del contrato de la API de Organización
// (`/organizacion/eventos`), tal como las reenvía el BFF de la app anfitriona. Los
// valores de los enums son los que acepta esa API; las etiquetas son las que lee la persona.
//
// 🛑 Sin datos de pacientes ni de personas reales en ningún ejemplo de este archivo.

export type TipoEvento = 'no_conformidad' | 'queja' | 'oportunidad_mejora'
export type Sede = 'oviedo' | 'viva_palmas' | 'domicilios' | 'sabaneta'
export type LlegoAAlguien = 'si' | 'no' | 'no_se'
export type EstadoEvento =
  | 'reportado'
  | 'clasificado'
  | 'en_analisis'
  | 'en_ejecucion'
  | 'en_verificacion'
  | 'cerrado'
  | 'descartado'
export type MedioContacto = 'correo' | 'telefono'

export const TIPOS_EVENTO: { id: TipoEvento, label: string, ayuda: string }[] = [
  { id: 'no_conformidad', label: 'No conformidad', ayuda: 'Algo no se hizo como está definido.' },
  { id: 'queja', label: 'Queja', ayuda: 'Alguien externo manifiesta su inconformidad.' },
  { id: 'oportunidad_mejora', label: 'Oportunidad de mejora', ayuda: 'Una idea para hacer mejor algo que ya funciona.' },
]

export const SEDES: { id: Sede, label: string }[] = [
  { id: 'oviedo', label: 'Oviedo' },
  { id: 'viva_palmas', label: 'Viva Palmas' },
  { id: 'domicilios', label: 'Domicilios' },
  { id: 'sabaneta', label: 'Sabaneta' },
]

export const LLEGO_A_ALGUIEN: { id: LlegoAAlguien, label: string }[] = [
  { id: 'si', label: 'Sí' },
  { id: 'no', label: 'No' },
  { id: 'no_se', label: 'No sé' },
]

export const ETIQUETA_ESTADO: Record<EstadoEvento, string> = {
  reportado: 'Reportado',
  clasificado: 'Clasificado',
  en_analisis: 'En análisis',
  en_ejecucion: 'En ejecución',
  en_verificacion: 'En verificación',
  cerrado: 'Cerrado',
  descartado: 'Descartado',
}

export const ETIQUETA_TIPO: Record<TipoEvento, string> = {
  no_conformidad: 'No conformidad',
  queja: 'Queja',
  oportunidad_mejora: 'Oportunidad de mejora',
}

/** Un proceso del mapa. La app anfitriona lo trae de Organización; este componente no lo inventa. */
export interface ProcesoOpcion {
  codigo: string
  nombre: string
}

/** Cuerpo de `POST {apiBase}/eventos`. Lo que no viaja aquí (quién reporta, la app de origen)
 *  lo pone el servidor desde la sesión, nunca el navegador. */
export interface ReporteEnvio {
  tipo: TipoEvento
  proceso_codigo: string
  sede: Sede
  descripcion: string
  fecha_ocurrencia: string
  fecha_conocimiento: string
  llego_a_alguien: LlegoAAlguien
  seguridad_paciente: boolean
  /** La pantalla desde la que se abrió, tal como la pasó la app anfitriona. */
  pantalla_origen?: string
  /** SOLO si quien reporta confirmó la sugerencia. Nunca se manda por omisión. */
  orden_servicio?: string
  /** Solo si `tipo` es `queja`: viaja DENTRO del reporte y el servidor no lo devuelve nunca. */
  contacto?: ContactoEnvio
}

/** Contacto de quien se queja (solo quejas). */
export interface ContactoEnvio {
  nombre: string
  medio: MedioContacto
  contacto: string
  aviso_aceptado: true
}

/** Respuesta de `POST {apiBase}/eventos` (201). */
export interface EventoReportado {
  id: string
  consecutivo: string
  pendiente_de_revision: boolean
  [otro: string]: unknown
}

/** Una fila de `GET {apiBase}/eventos` (vista `mis_procesos`). Sin texto libre. */
export interface ResumenEvento {
  id: string
  consecutivo: string
  tipo: TipoEvento
  estado: EstadoEvento
  proceso_codigo: string
  sede: Sede
  severidad: 'critica' | 'mayor' | 'menor' | null
  urgente: boolean
  oculto: boolean
  creado_en: string
  /** Próximo vencimiento (fecha ISO). Opcional: lo muestra si la API lo trae. */
  plazo?: string | null
  /** La orden de servicio solo llega si quien consulta puede verla; nunca se pinta por omisión. */
  orden_servicio?: string
}

/** Lo que el componente emite al fallar una llamada. */
export type CausaDeError = 'phi' | 'validacion' | 'reglas' | 'sesion' | 'permiso' | 'apagado' | 'red' | 'otro'

export interface ErrorDeEventos {
  causa: CausaDeError
  /** Una frase en «tú», lista para pintar. Nunca incluye lo que escribió la persona. */
  mensaje: string
  /** Solo para `phi`: los NOMBRES de las reglas que saltaron, nunca el texto. */
  reglas?: string[]
  /** Solo para `validacion`: los campos que el servidor señaló. */
  campos?: string[]
}

export const TEXTOS = {
  reportarBoton: 'Reportar un evento',
  reportarTitulo: 'Reportar un evento',
  reportarDescripcion: 'Cuéntanos qué pasó para que el equipo del proceso lo revise.',
  abiertoDesde: 'Abierto desde',
  avisoNombres: 'No escribas nombres ni documentos.',
  avisoNombresDetalle: 'Describe el hecho de forma general. Los datos de personas no van en este texto.',
  tipo: 'Tipo propuesto',
  tipoElige: 'Elige un tipo',
  llegoElige: 'Elige una opción',
  tipoAyuda: 'Es una propuesta: Calidad o el equipo del proceso lo confirman al clasificar.',
  proceso: 'Proceso',
  procesoElige: 'Elige un proceso',
  sede: 'Sede',
  sedeElige: 'Elige una sede',
  quePaso: '¿Qué pasó?',
  quePasoPlaceholder: 'Describe el hecho, sin datos de personas.',
  fechaOcurrencia: 'Fecha de ocurrencia',
  fechaConocimiento: 'Fecha en que te enteraste',
  llego: '¿Llegó a alguien?',
  seguridad: '¿Afecta la seguridad del paciente?',
  si: 'Sí',
  no: 'No',
  ordenSugerida: 'Orden de servicio sugerida',
  ordenConfirmar: 'Sí, el evento tiene que ver con esta orden',
  ordenAyuda: 'La pantalla donde estás tiene esta orden abierta. Solo se guarda si la confirmas. La ven el equipo del proceso, Calidad y Cumplimiento.',
  quejaTitulo: 'Datos de quien se queja',
  quejaNombre: 'Nombre de quien se queja',
  quejaMedio: 'Medio de contacto',
  quejaCorreo: 'Correo',
  quejaTelefono: 'Teléfono',
  quejaContacto: 'Dato de contacto',
  quejaAvisoDefecto: 'Usaremos estos datos solo para responder esta queja, los verán únicamente las personas que siguen el caso y los borraremos al vencer el plazo de retención.',
  quejaAvisoAcepto: 'Quien se queja fue informado de este aviso y lo acepta',
  quejaNombreNota: 'El nombre va solo en este recuadro, no en «¿Qué pasó?».',
  enviar: 'Reportar el evento',
  enviando: 'Enviando…',
  cancelar: 'Cancelar',
  cerrar: 'Cerrar',
  reportado: (consecutivo: string) => `Quedó reportado como ${consecutivo}. Gracias: el equipo del proceso lo va a revisar.`,
  pendiente: (consecutivo: string) => `Quedó reportado como ${consecutivo}, pendiente de revisión: no pudimos revisar el texto ahora. Solo Calidad y Cumplimiento lo ven hasta que se revise.`,
  rechazoPhi: 'No se guardó: el texto parece incluir datos de una persona.',
  rechazoPhiReglas: 'Reglas que saltaron',
  rechazoPhiPie: 'No mostramos el texto que escribiste. Quita el dato, déjalo general y envía de nuevo.',
  faltanCampos: 'Revisa los campos marcados antes de enviar.',
  campoRevisar: 'Revisa este campo.',
  campoObligatorio: 'Este campo es obligatorio.',
  ordenInvalida: 'La orden solo lleva dígitos.',
  fechaFutura: 'Esa fecha todavía no ha llegado.',
  panelTitulo: 'Eventos de mi proceso',
  panelVacio: 'Tu proceso no tiene eventos abiertos.',
  panelCargando: 'Cargando los eventos de tu proceso…',
  panelReintentar: 'Reintentar',
  panelUrgente: 'urgente',
  panelRevision: 'pendiente de revisión',
  panelVencido: 'vencido',
  panelSinPlazo: 'sin plazo',
  panelConsecutivo: 'Evento',
  panelTipo: 'Tipo',
  panelProceso: 'Proceso',
  panelEstado: 'Estado',
  panelPlazo: 'Plazo',
  panelOrden: 'Orden',
  panelNota: 'La orden de servicio no se muestra a menos que la app la pida.',
} as const

/** Los seis mensajes de error, en «tú». Cuando el servidor manda uno propio (4xx), gana el del servidor. */
export const ERRORES: Record<CausaDeError, string> = {
  phi: TEXTOS.rechazoPhi,
  validacion: TEXTOS.faltanCampos,
  reglas: 'Ahora mismo no podemos revisar el texto. No se guardó nada: intenta de nuevo en unos minutos.',
  sesion: 'Tu sesión terminó. Vuelve a entrar y repite el reporte.',
  permiso: 'No tienes permiso para esta acción. Pídelo a quien administra tu acceso.',
  apagado: 'Este módulo todavía no está disponible.',
  red: 'No pudimos conectar. Revisa tu conexión e intenta de nuevo.',
  otro: 'Algo salió mal y no se guardó. Intenta de nuevo; si sigue, avisa a Calidad.',
}
