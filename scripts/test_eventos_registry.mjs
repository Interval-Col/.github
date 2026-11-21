// Pruebas del componente de eventos de Pháros · Organización (plan 2.4):
//   1. el registro NO usa «usted» ni «vos» (todo el español de la org es «tú»);
//   2. el componente y su README no filtran nada interno (el repo es PÚBLICO);
//   3. la mitad pura del cliente: la base solo puede ser una ruta relativa, y los errores
//      del BFF se traducen sin devolver nunca el texto escrito.
// Datos sintéticos únicamente. Node ≥ 23.6 (TypeScript sin transpilar):
//   node --test scripts/test_eventos_registry.mjs
import assert from 'node:assert/strict'
import { readFileSync, readdirSync } from 'node:fs'
import { register } from 'node:module'
import { dirname, join } from 'node:path'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'

const REGISTRY = join(dirname(fileURLToPath(import.meta.url)), '..', 'brands', 'pharos_brand', 'registry')
const CARPETA = join(REGISTRY, 'app', 'components', 'ui', 'eventos')
const ARCHIVOS = [
  ...readdirSync(CARPETA).map(n => join(CARPETA, n)),
  join(REGISTRY, 'app', 'lib', 'eventosApi.ts'),
]
const texto = Object.fromEntries(ARCHIVOS.map(p => [p, readFileSync(p, 'utf8')]))

// Formas de «usted» y de «vos» que no pueden aparecer. Lista corta y deliberada: palabras que no
// existen en «tú» (nada ambiguo como «su» o «más»).
// \b de JS es ASCII: con tildes no corta bien, así que se usan límites Unicode.
const palabra = lista => new RegExp(`(?<![\\p{L}])(?:${lista})(?![\\p{L}])`, 'iu')
// Formas que solo existen en «usted» (o con enclítico/tilde que el «tú» no usa)…
const USTED_SEGURO = palabra('usted(?:es)?|uds?\\.|ingrese|seleccione|asegúrese|déjelo|comuníquese|póngase')
// …y los imperativos que coinciden con el subjuntivo de tercera persona («para que lo revise» es «tú»
// correcto): solo se marcan al ARRANCAR una frase o una cadena, que es donde son una orden a «usted».
const USTED_AL_INICIO = new RegExp("(?:^|[.:;¿¡'\"`>])\\s*(?:escriba|revise|elija|indique|describa|confirme|quite|envíe|verifique|intente|espere|consulte|complete)(?![\\p{L}])", 'iu')
export const USTED = { test: t => USTED_SEGURO.test(t) || USTED_AL_INICIO.test(t) }
// Voseo: solo las formas CON tilde (sin ella son palabras del español de «tú»: «confirma», «revisa»).
export const VOS = palabra('vos|sos|tenés|podés|querés|escribí|poné|mirá|hacé|decime|intentá|revisá|elegí|confirmá|dejá|avisá')

test('el detector marca lo que debe (control positivo)', () => {
  for (const mala of ['Escriba su nombre', 'Usted debe revisar', 'Seleccione una sede', 'Podés enviarlo', 'Vos tenés que elegir', 'Escribí aquí']) {
    assert.ok(USTED.test(mala) || VOS.test(mala), `debía marcar: ${mala}`)
  }
  for (const buena of ['Escribe tu nombre', 'Elige un proceso', 'Revisa los campos marcados', 'Fecha en que te enteraste', 'Tu sesión terminó']) {
    assert.ok(!USTED.test(buena) && !VOS.test(buena), `no debía marcar: ${buena}`)
  }
})

test('ningún archivo del componente trata de «usted» ni de «vos»', () => {
  for (const [ruta, t] of Object.entries(texto)) {
    for (const [n, linea] of t.split('\n').entries()) {
      assert.ok(!USTED.test(linea), `${ruta}:${n + 1} usa «usted»: ${linea.trim()}`)
      assert.ok(!VOS.test(linea), `${ruta}:${n + 1} usa «vos»: ${linea.trim()}`)
    }
  }
})

test('superficie pública (S5): nada interno en el componente ni en su README', () => {
  const prohibido = [
    [/hematologico/i, 'dominio interno'],
    [/SECRET/, 'nombre de secreto'],
    [/_KEY/, 'nombre de llave'],
    [/X-Pharos-/i, 'encabezado de servicio'],
    [/\[0-9\]\{\d+\}|\\d\{\d+\}|\b\d{7}\b/, 'formato o ejemplo de orden de servicio'],
    [/\b(?:\d{1,3}\.){3}\d{1,3}\b/, 'dirección IP'],
    [/https?:\/\//i, 'URL absoluta'],
  ]
  for (const [ruta, t] of Object.entries(texto)) {
    for (const [re, que] of prohibido) assert.ok(!re.test(t), `${ruta}: ${que} (${re})`)
  }
})

test('el componente no manda la orden sin confirmar (el cuerpo solo la lleva tras la casilla)', () => {
  const f = texto[join(CARPETA, 'EventoFormulario.vue')]
  assert.match(f, /hayOrden\.value && f\.confirmaOrden/)
  assert.equal((f.match(/orden_servicio/g) ?? []).length, 2) // el `if` que la agrega y su comentario no la duplican
})

// ── Mitad pura del cliente ───────────────────────────────────────────────────────────────────
register('data:text/javascript,' + encodeURIComponent(
  'export async function resolve(s,c,n){try{return await n(s,c)}catch(e){if(e.code==="ERR_MODULE_NOT_FOUND"&&s.startsWith("."))return n(s+".ts",c);throw e}}',
))
const { normalizarBase, interpretarError, crearEventosApi, ErrorEventosApi } = await import(join(REGISTRY, 'app', 'lib', 'eventosApi.ts'))

test('normalizarBase: solo rutas relativas de la propia app', () => {
  assert.equal(normalizarBase('/mi-app/api'), '/mi-app/api')
  assert.equal(normalizarBase('/mi-app/api/'), '/mi-app/api')
  for (const mala of ['https://otro.example/api', '//otro.example/api', 'mi-app/api', '/a/../b', '', '/a b']) {
    assert.throws(() => normalizarBase(mala), /ruta relativa/, mala)
  }
})

test('interpretarError: el portón de datos devuelve reglas, nunca texto', () => {
  const e = interpretarError(422, { detail: { mensaje: 'x', reglas: ['regla_a', 'regla_b'] } })
  assert.equal(e.causa, 'phi')
  assert.deepEqual(e.reglas, ['regla_a', 'regla_b'])
  assert.ok(!('texto' in e))
})

test('interpretarError: validación, 503, sesión, permiso y apagado', () => {
  const v = interpretarError(422, { detail: { errores: [{ codigo: 'X', campo: 'proceso_codigo', mensaje: 'Ese proceso no está en el mapa.' }] } })
  assert.equal(v.causa, 'validacion')
  assert.deepEqual(v.campos, ['proceso_codigo'])
  assert.equal(v.mensaje, 'Ese proceso no está en el mapa.')
  assert.equal(interpretarError(503, { detail: 'texto del servidor' }).causa, 'reglas')
  assert.notEqual(interpretarError(503, { detail: 'texto del servidor' }).mensaje, 'texto del servidor') // un 5xx no se pinta
  assert.equal(interpretarError(401, null).causa, 'sesion')
  assert.equal(interpretarError(403, { detail: 'No tienes la capacidad.' }).mensaje, 'No tienes la capacidad.') // 4xx: gana el servidor
  assert.equal(interpretarError(404, null).causa, 'apagado')
  assert.notEqual(interpretarError(403, { detail: '<html>' }).mensaje, '<html>')
})

test('crearEventosApi: solo llama a ${apiBase}/eventos…, con la sesión y sin secretos', async () => {
  const llamadas = []
  const fetch = async (url, init) => {
    llamadas.push({ url, init })
    if (init.method === 'PUT') return new Response(null, { status: 204 })
    if (init.method === 'POST') return new Response(JSON.stringify({ id: 'a', consecutivo: 'EV-0', pendiente_de_revision: false }), { status: 201 })
    return new Response('[]', { status: 200 })
  }
  const api = crearEventosApi({ apiBase: '/mi-app/api', fetch, headers: () => ({ 'X-Csrf': 't' }) })
  await api.listar()
  await api.reportar({ tipo: 'queja' })
  await api.guardarContacto('id con/barra', { nombre: 'n', medio: 'correo', contacto: 'c@ejemplo.invalid', aviso_aceptado: true })
  assert.deepEqual(llamadas.map(l => l.url), [
    '/mi-app/api/eventos?vista=mis_procesos',
    '/mi-app/api/eventos',
    '/mi-app/api/eventos/id%20con%2Fbarra/contacto',
  ])
  assert.ok(llamadas.every(l => l.init.credentials === 'same-origin' && l.init.headers['X-Csrf'] === 't'))
})

test('crearEventosApi: un fallo de red es un error en «tú», no una excepción cruda', async () => {
  const api = crearEventosApi({ apiBase: '/mi-app/api', fetch: async () => { throw new TypeError('x') } })
  await assert.rejects(api.listar(), (e) => e instanceof ErrorEventosApi && e.detalle.causa === 'red')
})
