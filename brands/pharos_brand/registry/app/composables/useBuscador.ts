// useBuscador — el motor del Buscador (plan de búsqueda, 0.3 y 0.5).
//
// Reglas que vive aquí, no en cada pantalla:
//   • borrador ≠ aplicada: lo que se escribe no busca; buscar es un acto (botón o Enter,
//     un solo submit). Si el borrador cambia después de buscar, los resultados quedan
//     «desactualizados» y lo dice.
//   • una búsqueda a la vez: un segundo envío igual mientras carga se ignora (el doble
//     clic no busca dos veces); uno distinto cancela el anterior.
//   • guarda de generación: una respuesta vieja nunca pisa una nueva.
//   • error ≠ sin resultados; truncado = sin filas y pide afinar.
//   • al volver atrás se restaura la última búsqueda SÓLO en memoria: nunca en la URL ni
//     en el almacenamiento del navegador. Una recarga la borra.
import { computed, reactive, ref, shallowRef } from 'vue'
import { FallaBusqueda, type EstadoBusqueda } from '../lib/busqueda/estados'
import { faltaEnNombre, llaveDeNombre, ecoDeLlave } from '../lib/busqueda/llave-nombre'
import { enmascararDocumento } from '../lib/busqueda/enmascarar'
import { TEXTOS } from '../lib/busqueda/textos'
import type { ConsultaPaciente, Fuente, Respuesta } from '../lib/busqueda/tipos'

export type ModoBuscador = 'orden' | 'documento' | 'nombre'

export interface BorradorBuscador {
  modo: ModoBuscador
  orden: string
  tipo: string | null
  numero: string
  nombres: string
  apellido1: string
  apellido2: string
}

const vacio = (modo: ModoBuscador): BorradorBuscador =>
  ({ modo, orden: '', tipo: null, numero: '', nombres: '', apellido1: '', apellido2: '' })

interface Guardado<T> {
  borrador: BorradorBuscador
  aplicada: ConsultaPaciente
  estado: EstadoBusqueda
  filas: T[]
  fuente: Fuente
}

/**
 * Memoria de la pestaña para volver atrás (D19): sobrevive a navegar, no a una recarga.
 * Guarda datos de pacientes, así que tiene dos frenos (revisión adversarial, 2026-11-27):
 *   • vence a los `VIGENCIA_MS` (una estación compartida no le muestra a la siguiente
 *     persona la búsqueda de la anterior);
 *   • `olvidarBusquedas()` la vacía: cada app la llama al cerrar sesión o cambiar de usuario.
 * Una búsqueda que falla borra lo guardado: volver nunca muestra un resultado viejo como actual.
 */
export const VIGENCIA_MS = 10 * 60_000
const memoria = new Map<string, Guardado<unknown> & { guardadoEn: number }>()

export function olvidarBusquedas(): void {
  memoria.clear()
}

function recordar<T>(clave: string | undefined): Guardado<T> | undefined {
  if (!clave) return undefined
  const g = memoria.get(clave)
  if (!g) return undefined
  if (Date.now() - g.guardadoEn > VIGENCIA_MS) {
    memoria.delete(clave)
    return undefined
  }
  return g as unknown as Guardado<T>
}

export function consultaDe(b: BorradorBuscador): ConsultaPaciente | null {
  if (b.modo === 'orden') return b.orden.trim() ? { modo: 'orden', orden: b.orden.trim() } : null
  if (b.modo === 'documento') {
    return b.tipo && b.numero.trim() ? { modo: 'documento', tipo: b.tipo, numero: b.numero.trim() } : null
  }
  return faltaEnNombre(b) ? null : { modo: 'nombre', nombres: b.nombres, apellido1: b.apellido1, apellido2: b.apellido2 }
}

export function faltaDe(b: BorradorBuscador): string | null {
  if (b.modo === 'orden') return b.orden.trim() ? null : TEXTOS.estados.faltaNumero
  if (b.modo === 'documento') {
    if (!b.tipo) return TEXTOS.estados.faltaTipo
    return b.numero.trim() ? null : TEXTOS.estados.faltaNumero
  }
  const f = faltaEnNombre(b)
  return f === 'nombres' ? TEXTOS.estados.faltaNombres : f === 'apellido' ? TEXTOS.estados.faltaApellido : null
}

export function ecoDe(c: ConsultaPaciente): string {
  if (c.modo === 'nombre') return TEXTOS.buscador.ecoNombre(ecoDeLlave(llaveDeNombre(c)))
  if (c.modo === 'documento') return TEXTOS.buscador.ecoDocumento(c.tipo, enmascararDocumento(c.numero))
  return TEXTOS.buscador.ecoOrden(enmascararDocumento(c.orden))
}

/** En modo Nombre se compara la LLAVE: «Prueba» y «Pru» envían lo mismo al LIS. */
function normalizada(c: ConsultaPaciente | null) {
  return c?.modo === 'nombre' ? { modo: 'nombre', ...llaveDeNombre(c) } : c
}
const misma = (a: ConsultaPaciente | null, b: ConsultaPaciente | null) =>
  JSON.stringify(normalizada(a)) === JSON.stringify(normalizada(b))

export function useBuscador<T>(opciones: {
  buscar: (c: ConsultaPaciente, signal: AbortSignal) => Promise<Respuesta<T>>
  modoInicial?: ModoBuscador
  /** Llave para restaurar en memoria al volver atrás. Sin llave, no se restaura. */
  memoriaClave?: string
}) {
  const previo = recordar<T>(opciones.memoriaClave)
  const borrador = reactive<BorradorBuscador>(previo ? { ...previo.borrador } : vacio(opciones.modoInicial ?? 'orden'))
  const aplicada = shallowRef<ConsultaPaciente | null>(previo?.aplicada ?? null)
  const estado = ref<EstadoBusqueda>(previo?.estado ?? 'idle')
  const filas = shallowRef<T[]>(previo?.filas ?? [])
  const fuente = ref<Fuente>(previo?.fuente ?? 'pharos')
  const envios = ref(0)

  let control: AbortController | undefined
  let generacion = 0

  const consulta = computed(() => consultaDe(borrador))
  const falta = computed(() => faltaDe(borrador))
  const valido = computed(() => consulta.value !== null)
  const cargando = computed(() => estado.value === 'loading')
  /** Hay resultados (o un estado final) de otra consulta distinta a la del borrador. */
  const desactualizado = computed(() =>
    aplicada.value !== null && estado.value !== 'loading' && !misma(aplicada.value, consulta.value))
  const eco = computed(() => (aplicada.value ? ecoDe(aplicada.value) : ''))

  function cambiarModo(m: ModoBuscador) {
    borrador.modo = m
  }

  async function enviar() {
    const c = consulta.value
    if (!c) {
      // Si había una búsqueda en vuelo, se cancela: no puede llegar después y pasar
      // de «incompleto» a «resultados» (transición ilegal en estados.ts).
      if (estado.value === 'loading') {
        control?.abort()
        generacion++
        filas.value = []
      }
      estado.value = 'incomplete'
      return
    }
    if (estado.value === 'loading' && misma(c, aplicada.value)) return // doble clic
    control?.abort()
    const mia = ++generacion
    const propio = new AbortController()
    control = propio
    aplicada.value = c
    estado.value = 'loading'
    filas.value = []
    envios.value++
    try {
      const r = await opciones.buscar(c, propio.signal)
      if (mia !== generacion) return
      fuente.value = r.fuente
      if (r.truncado) {
        estado.value = 'truncated'
        filas.value = []
      }
      else {
        filas.value = r.filas
        estado.value = r.filas.length ? 'results' : 'no-results'
      }
      guardar()
    }
    catch (e) {
      if (mia !== generacion) return
      // Sólo se ignora la cancelación PROPIA. Un abort ajeno (el timeout de un cliente,
      // una navegación) es una falla: si se callara, el buscador quedaría «Buscando…» para siempre.
      if ((e as Error).name === 'AbortError' && propio.signal.aborted) return
      estado.value = e instanceof FallaBusqueda ? e.tipo : 'error'
      filas.value = []
      if (opciones.memoriaClave) memoria.delete(opciones.memoriaClave)
    }
  }

  function guardar() {
    if (!opciones.memoriaClave || !aplicada.value) return
    memoria.set(opciones.memoriaClave, {
      borrador: { ...borrador }, aplicada: aplicada.value, estado: estado.value, filas: filas.value, fuente: fuente.value,
      guardadoEn: Date.now(),
    })
  }

  function limpiar() {
    control?.abort()
    generacion++
    Object.assign(borrador, vacio(borrador.modo))
    aplicada.value = null
    filas.value = []
    estado.value = 'idle'
    if (opciones.memoriaClave) memoria.delete(opciones.memoriaClave)
  }

  return {
    borrador, aplicada, estado, filas, fuente, envios,
    consulta, falta, valido, cargando, desactualizado, eco,
    cambiarModo, enviar, limpiar,
  }
}
