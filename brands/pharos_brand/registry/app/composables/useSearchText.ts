// useSearchText — el término de un Filtro de lista, plegado una sola vez (plan de
// búsqueda, 0.3). Filtra lo que ya está en pantalla y NUNCA llama al servidor.
//
//   const { termino, filtrar } = useSearchText()
//   const visibles = computed(() => filtrar(filas.value, f => [f.nombre, f.orden]))
import { ref } from 'vue'
import { coincide } from '../lib/busqueda/plegar'

export function useSearchText(inicial = '') {
  const termino = ref(inicial)

  function filtrar<T>(filas: readonly T[], campos: (fila: T) => (string | null | undefined)[]): T[] {
    if (!termino.value.trim()) return [...filas]
    return filas.filter(f => coincide(campos(f).filter(Boolean).join(' '), termino.value))
  }

  function limpiar() {
    termino.value = ''
  }

  return { termino, filtrar, limpiar }
}
