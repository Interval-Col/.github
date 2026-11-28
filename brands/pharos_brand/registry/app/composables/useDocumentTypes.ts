// useDocumentTypes — la lista de tipos de documento (plan de búsqueda, 0.3).
// En el prototipo es estática. Al adoptar, cada app la pide a su backend y usa ésta
// como respaldo si la petición falla.
import { TIPOS_DOCUMENTO, tipoPorCodigo, tiposQueEmpiezanPor } from '../lib/busqueda/tipos-documento'

export function useDocumentTypes() {
  return { tipos: TIPOS_DOCUMENTO, tipoPorCodigo, tiposQueEmpiezanPor }
}
