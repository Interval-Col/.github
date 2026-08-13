#!/usr/bin/env node
/**
 * CI gate: la marca de «vista en verificación» (PROT-SW-001) y su manifiesto
 * no pueden separarse de la pantalla.
 *
 * Por qué existe. La marca declara, EN LA PANTALLA, que una vista está desplegada
 * pero todavía no liberada — `PROT-SW-001` §6. Eso la convierte en una afirmación
 * de seguridad clínica, y una afirmación así falla de dos maneras opuestas:
 *
 *   • FALTA donde se debe  — el manifiesto dice que una vista está en verificación
 *     pero la página no monta el componente, así que quien la usa no ve nada.
 *   • SOBRA donde ya no    — la vista se liberó hace meses y la banda sigue ahí.
 *     Eso es peor que no tenerla: la gente aprende a no leerla, y cuando aparezca
 *     una de verdad tampoco la va a leer.
 *
 * Los ocho chequeos de abajo cierran esas dos, más las reglas que el protocolo y
 * `SOP-000` imponen sobre el contenido. Ninguno es un warning: un warning en un
 * gate se ignora por definición.
 *
 * Qué NO hace: no decide qué vista va marcada ni con qué estado. Eso lo deciden
 * Calidad y Dirección Médica, y queda escrito en `app/verification.manifest.ts`.
 *
 * Silencioso y exit 0 cuando la app no adoptó la marca (sin manifiesto y sin
 * montajes): la mayoría de las apps del estado no la necesitan todavía.
 *
 * Uso:  node scripts/check-view-verification.mjs [--today YYYY-MM-DD]
 *       (--today solo para probar el gate; en CI se usa la fecha real)
 */
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = resolve(__dirname, '..')
const APP_DIR = join(REPO_ROOT, 'app')
const MANIFEST_FILE = join(APP_DIR, 'verification.manifest.ts')
const PAGES_DIR = join(APP_DIR, 'pages')
const LAYOUTS_DIR = join(APP_DIR, 'layouts')

const todayArg = process.argv.indexOf('--today')
const TODAY = todayArg !== -1 && process.argv[todayArg + 1]
  ? process.argv[todayArg + 1]
  : new Date().toISOString().slice(0, 10)

const errors = []
const notes = []
const rel = p => relative(REPO_ROOT, p)

function walk(dir, exts) {
  if (!existsSync(dir)) return []
  const out = []
  for (const name of readdirSync(dir)) {
    const full = join(dir, name)
    if (statSync(full).isDirectory()) out.push(...walk(full, exts))
    else if (exts.some(e => name.endsWith(e))) out.push(full)
  }
  return out
}

// ── Adopción ─────────────────────────────────────────────────────────────────
// El gate corre en toda app que sincroniza el registry, la haya adoptado o no.
const pages = walk(PAGES_DIR, ['.vue'])
const layouts = walk(LAYOUTS_DIR, ['.vue'])
const MOUNT_RE = /<ViewVerification(?![a-zA-Z])/

// Salida explícita para páginas de CATÁLOGO: una página que muestra el componente
// con objetos de ejemplo (un playground, una guía de estilo) monta <ViewVerification>
// sin que ninguna vista real esté marcada. Se declara EN EL ARCHIVO, no por forma ni
// por ruta: adivinar «esto parece una demo» sería exactamente el hueco por el que se
// cuela la banda a mano que el chequeo 3 existe para atrapar. Y no es silenciosa —
// se imprime, para que un `grep` y la salida del gate digan lo mismo.
const SHOWCASE_MARKER = 'view-verification:showcase'
const isShowcase = f => readFileSync(f, 'utf8').includes(SHOWCASE_MARKER)
const showcase = pages.filter(f => MOUNT_RE.test(readFileSync(f, 'utf8')) && isShowcase(f))
const mounted = pages.filter(f => MOUNT_RE.test(readFileSync(f, 'utf8')) && !isShowcase(f))
if (showcase.length) {
  notes.push(`${showcase.length} página(s) de catálogo exentas (${SHOWCASE_MARKER}): ${showcase.map(rel).join(', ')}`)
}
const hasManifest = existsSync(MANIFEST_FILE)

if (!hasManifest && mounted.length === 0) {
  process.exit(0)   // no adoptada — nada que revisar, y sin ruido
}

// El componente sin su manifiesto ni siquiera compila (lib/verification.ts lo
// importa), pero fallar acá da un mensaje que se entiende sin leer un stack de Vite.
if (!hasManifest && mounted.length > 0) {
  errors.push(
    `Hay ${mounted.length} montaje(s) de <ViewVerification> pero no existe ${rel(MANIFEST_FILE)}.\n` +
    `      Cópialo del registry (app/verification.manifest.ts) y declara ahí las vistas.`,
  )
}

// ── Lectura del manifiesto ────────────────────────────────────────────────────
// Se parsea el TEXTO, no se importa: el gate corre en node plano, sin el resolver
// de alias de Nuxt, y arrastrar un bundler a un gate de CI es cambiar una
// verificación barata por una cadena de herramientas que también se puede romper.
// El manifiesto es un literal de objeto plano por contrato — el registry lo emite
// así y el chequeo 0 rechaza cualquier cosa que no lo sea.
const src = hasManifest ? readFileSync(MANIFEST_FILE, 'utf8') : ''
const body = src.replace(/^[\s\S]*?VERIFICATION_MANIFEST\s*:[^=]*=\s*/, '')
const entries = []

if (hasManifest) {
  // Cada entrada: 'ruta': { … } en el primer nivel. Se cortan por llaves balanceadas.
  const keyRe = /(^|[,{\s])(['"])(\/[^'"]*)\2\s*:\s*\{/gm
  let m
  while ((m = keyRe.exec(body)) !== null) {
    const start = body.indexOf('{', m.index + m[0].length - 1)
    let depth = 0, end = -1
    for (let i = start; i < body.length; i++) {
      if (body[i] === '{') depth++
      else if (body[i] === '}') { depth--; if (depth === 0) { end = i; break } }
    }
    if (end === -1) continue
    const raw = body.slice(start, end + 1)
    // Se ignora lo comentado: la plantilla del registry viene con un ejemplo en //
    const line = body.slice(0, m.index).split('\n').pop() ?? ''
    if (line.trimStart().startsWith('//')) continue
    const field = k => {
      const f = raw.match(new RegExp(`${k}\\s*:\\s*(['"])([\\s\\S]*?)\\1`))
      return f ? f[2] : null
    }
    const resp = raw.match(/responsable\s*:\s*\{([\s\S]*?)\}/)
    const respField = k => {
      if (!resp) return null
      const f = resp[1].match(new RegExp(`${k}\\s*:\\s*(['"])([\\s\\S]*?)\\1`))
      return f ? f[2] : null
    }
    entries.push({
      path: m[3],
      raw,
      estado: field('estado'),
      restriccion: field('restriccion'),
      revisarAntes: field('revisarAntes'),
      nombre: respField('nombre'),
      cargo: respField('cargo'),
    })
  }

  // 0 · el manifiesto tiene que ser legible. Si trae entradas que el parser no ve,
  // todos los demás chequeos pasarían en verde sobre un archivo que nadie revisó.
  const declaredKeys = (body.match(/(^|[,{\s])(['"])\/[^'"]*\2\s*:/gm) ?? []).length
  if (declaredKeys !== entries.length) {
    errors.push(
      `No pude leer ${rel(MANIFEST_FILE)} completo (${entries.length} de ${declaredKeys} entradas).\n` +
      `      El manifiesto tiene que ser un literal de objeto plano, sin spreads ni valores calculados.`,
    )
  }
}

// ── 1 · toda ruta del manifiesto resuelve a una página real ───────────────────
// Renombrar una ruta borraría la marca EN SILENCIO: el manifiesto seguiría
// declarándola y `verificationFor()` no encontraría nada.
const pageRoutes = new Map(pages.map(f => {
  let r = '/' + relative(PAGES_DIR, f).replace(/\.vue$/, '').replace(/\\/g, '/')
  r = r.replace(/\/index$/, '') || '/'
  return [r, f]
}))
for (const e of entries) {
  if (!pageRoutes.has(e.path)) {
    errors.push(`Ruta declarada que no existe como página: ${e.path} (${rel(MANIFEST_FILE)}).`)
  }
}

// ── 2 · toda ruta marcada monta el componente ─────────────────────────────────
// Sin esto el manifiesto afirma una marca que quien usa la vista NO VE. Es la
// falla peor de las dos: la app queda diciendo por escrito que avisó, sin avisar.
for (const e of entries) {
  const f = pageRoutes.get(e.path)
  if (f && !mounted.includes(f)) {
    errors.push(
      `${e.path} está en el manifiesto pero ${rel(f)} no monta <ViewVerification>.\n` +
      `      Quien abra esa vista no ve ninguna marca.`,
    )
  }
}

// ── 3 · todo montaje tiene entrada en el manifiesto ───────────────────────────
// Una banda puesta a mano es una marca que nadie puede auditar ni retirar: no
// aparece en la lista que Calidad revisa, y ningún chequeo de caducidad la alcanza.
const declaredPaths = new Set(entries.map(e => e.path))
for (const f of mounted) {
  let r = '/' + relative(PAGES_DIR, f).replace(/\.vue$/, '').replace(/\\/g, '/')
  r = r.replace(/\/index$/, '') || '/'
  if (!declaredPaths.has(r)) {
    errors.push(
      `${rel(f)} monta <ViewVerification> pero ${r} no está en el manifiesto.\n` +
      `      Declárala, o quita el envoltorio.`,
    )
  }
}

// ── 4 · responsable NOMINAL: nombre + cargo, nunca un handle ──────────────────
// `SOP-000` §4. Una vista que dice «responsable: @alguien» no le sirve al auditor
// ni a la persona del mesón que necesita saber a quién preguntarle.
const HANDLE_RE = /^@|^[a-z0-9][a-z0-9._-]*$/
for (const e of entries) {
  if (!e.nombre || !e.cargo) {
    errors.push(`${e.path}: falta responsable con \`nombre\` y \`cargo\` (SOP-000 §4).`)
  } else if (HANDLE_RE.test(e.nombre.trim())) {
    errors.push(
      `${e.path}: \`responsable.nombre\` = "${e.nombre}" parece un identificador técnico.\n` +
      `      SOP-000 §4 pide nombre completo y cargo, nunca un handle.`,
    )
  }
}

// ── 5 · `no-conforme-acotado` exige el texto de la restricción ────────────────
// `PROT-SW-001` §6.1: ese estado SOLO existe si hay una restricción operativa
// escrita y verificable. Sin el texto, la marca afirmaría una salvaguarda que
// nadie declaró.
for (const e of entries) {
  if (e.estado === 'no-conforme-acotado' && !e.restriccion) {
    errors.push(`${e.path}: estado \`no-conforme-acotado\` sin \`restriccion\` (PROT-SW-001 §6.1).`)
  }
}

// ── 6 · caducidad — el chequeo que evita que esto se vuelva mobiliario ────────
// Una marca sin fecha de revisión sobrevive a su propia verdad. El arreglo cuando
// esto falla NO es alargar la fecha por reflejo: es mirar si la vista ya se liberó
// (⇒ borrar la entrada) o si sigue en verificación (⇒ Calidad mueve la fecha en un PR).
const ISO_RE = /^\d{4}-\d{2}-\d{2}$/
for (const e of entries) {
  if (!e.revisarAntes) {
    errors.push(`${e.path}: falta \`revisarAntes\` (YYYY-MM-DD). Una marca sin caducidad se vuelve mobiliario.`)
  } else if (!ISO_RE.test(e.revisarAntes)) {
    errors.push(`${e.path}: \`revisarAntes\` = "${e.revisarAntes}" no es YYYY-MM-DD.`)
  } else if (e.revisarAntes < TODAY) {
    errors.push(
      `${e.path}: \`revisarAntes\` venció el ${e.revisarAntes} (hoy ${TODAY}).\n` +
      `      ¿La vista ya se liberó? Borra la entrada. ¿Sigue en verificación? Calidad mueve la fecha.`,
    )
  }
}

// ── 7 · cero datos de paciente ────────────────────────────────────────────────
// `PROT-SW-001` §8. El manifiesto describe SOFTWARE. Un documento o un número de
// orden acá es dato personal de salud dentro de un archivo versionado — y el
// número de orden es seudónimo, no anonimato.
const PHI_RE = [
  { re: /\b(CC|TI|CE|RC|PA|NIT)\s*[.\s-]?\s*\d{4,}/i, what: 'un documento de identidad' },
  { re: /\bord(en)?\s*[#.\s-]?\s*\d{5,}/i, what: 'un número de orden' },
]
for (const e of entries) {
  for (const { re, what } of PHI_RE) {
    if (re.test(e.raw)) {
      errors.push(`${e.path}: el manifiesto parece traer ${what}. Cero datos de paciente (PROT-SW-001 §8).`)
    }
  }
}

// ── 8 · si hay marcas, el layout avisa ANTES de entrar ────────────────────────
// `layouts/default.vue` es scaffold propio de la app: el sync NUNCA lo toca. Ahí
// fue exactamente donde SystemBeacon dejó su hueco — registro elegido en
// runtimeConfig, montaje del lienzo en scaffold que nadie adoptó, y una app con un
// registro que nada renderiza. El envoltorio se libra solo porque busca su lienzo;
// el chip no puede, así que lo cierra este chequeo.
if (entries.length > 0) {
  const chipMounted = layouts.some(f => /<ViewVerificationMark(?![a-zA-Z])/.test(readFileSync(f, 'utf8')))
  if (!chipMounted) {
    errors.push(
      `Hay ${entries.length} vista(s) marcada(s) pero ningún layout monta <ViewVerificationMark>.\n` +
      `      Habría banda dentro de la vista, pero ningún aviso ANTES de entrar. Móntalo en\n` +
      `      app/layouts/default.vue (nav + breadcrumb) — el sync no lo hace por ti.`,
    )
  }
}

// ── Salida ────────────────────────────────────────────────────────────────────
if (errors.length) {
  console.error('[view-verification] FALLA — la marca de PROT-SW-001 y la pantalla no coinciden:\n')
  for (const e of errors) console.error(`  ✗ ${e}`)
  console.error('\n  Contexto: registry/app/verification.manifest.ts explica cada regla.')
  process.exit(1)
}

for (const n of notes) console.log(`[view-verification] ${n}`)
console.log(
  `[view-verification] OK — ${entries.length} vista(s) marcada(s), ` +
  `montaje y manifiesto de acuerdo, ninguna revisión vencida (hoy ${TODAY}).`,
)
