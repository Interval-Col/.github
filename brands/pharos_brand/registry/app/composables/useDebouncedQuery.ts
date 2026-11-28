// useDebouncedQuery — buscar al teclear, SÓLO para fuentes baratas y sin PHI de
// pacientes (plan de búsqueda, regla de costo; D3 (a): 300 ms, German 2026-11-27).
// Mínimo 2 caracteres, cancela la anterior y descarta respuestas viejas.
import { onScopeDispose, ref, shallowRef, watch, type Ref } from 'vue'

export const ESPERA_MS = 300
export const MINIMO_CARACTERES = 2

export function useDebouncedQuery<T>(
  termino: Ref<string>,
  buscar: (t: string, signal: AbortSignal) => Promise<T[]>,
  opciones: { esperaMs?: number, minimo?: number } = {},
) {
  const esperaMs = opciones.esperaMs ?? ESPERA_MS
  const minimo = opciones.minimo ?? MINIMO_CARACTERES
  const resultados = shallowRef<T[]>([])
  const cargando = ref(false)
  const error = ref(false)
  let timer: ReturnType<typeof setTimeout> | undefined
  let control: AbortController | undefined
  let generacion = 0

  let ultimo = ''
  watch(termino, (crudo) => {
    const t = crudo.trim()
    if (t === ultimo) return // un espacio al final no vuelve a preguntar
    ultimo = t
    clearTimeout(timer)
    control?.abort()
    const mia = ++generacion // cualquier respuesta anterior queda vieja desde YA
    error.value = false
    if (t.length < minimo) {
      resultados.value = []
      cargando.value = false
      return
    }
    timer = setTimeout(async () => {
      if (mia !== generacion) return
      control = new AbortController()
      cargando.value = true
      try {
        const r = await buscar(t, control.signal)
        if (mia === generacion) resultados.value = r
      }
      catch (e) {
        if ((e as Error).name !== 'AbortError' && mia === generacion) {
          error.value = true
          resultados.value = []
        }
      }
      finally {
        if (mia === generacion) cargando.value = false
      }
    }, esperaMs)
  })

  onScopeDispose(() => {
    clearTimeout(timer)
    control?.abort()
    generacion++
  })

  return { resultados, cargando, error }
}
