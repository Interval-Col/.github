<script setup lang="ts" generic="T = Paciente">
// Buscador — búsqueda de pacientes AL SERVIDOR (plan de búsqueda, 0.5). Reemplaza a
// EntityLookup y sus presets. Las reglas del estándar viven en `useBuscador`; aquí
// está la cara:
//
//   • Modos «Orden · Documento · Nombre» como pestañas reales (D1): `tablist`,
//     flechas para moverse. Con un solo modo no hay pestañas (campo de código).
//   • UN `<form role="search">`: Enter y «Buscar» son el mismo submit. El botón está
//     apagado hasta que el modo tenga lo que necesita; Enter con datos incompletos
//     dice qué falta en vez de buscar.
//   • El eco de lo que se buscó va SIEMPRE encima de los resultados; en Nombre, la
//     llave 3+3+3 que de verdad fue al LIS (D4).
//   • Cada estado tiene su propio texto: un error nunca se ve como «sin resultados»,
//     truncado no muestra filas, y si cambias los datos dice que lo que ves es viejo.
//   • Enmascarado hasta revelar (D20): nombres detrás de un solo «Mostrar»/«Ocultar»
//     para toda la lista; documentos •••+3 últimos. Un resultado por nombre muestra
//     fecha de nacimiento, edad y sexo para distinguir homónimos (D16).
//   • Ningún dato buscado va a la URL, al almacenamiento del navegador ni a la consola.
//
// Filas que no son pacientes (p. ej. órdenes de Liberación): slot `#fila`. La fila
// entera ya es el botón que emite `seleccionar`, así que el slot no lleva controles.
import { computed, nextTick, onBeforeUnmount, ref, useId, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { cn } from '@/lib/utils'
import { useBuscador } from '@/composables/useBuscador'
import { edad, nombreCompleto } from '@/lib/busqueda/tipos'
import { enmascararDocumento, enmascararNombre } from '@/lib/busqueda/enmascarar'
import { TEXTOS } from '@/lib/busqueda/textos'
import BuscadorModo from './BuscadorModo.vue'
import {
  MODOS,
  type BorradorBuscador, type ConsultaPaciente, type Fuente, type ModoBuscador, type Paciente, type Respuesta,
} from './types'

const props = defineProps<{
  buscar: (c: ConsultaPaciente, signal: AbortSignal) => Promise<Respuesta<T>>
  modoInicial?: ModoBuscador
  /** Qué modos ofrecer (por defecto, los tres). */
  modos?: ModoBuscador[]
  /** Llave para restaurar la última búsqueda en memoria al volver atrás. */
  memoriaClave?: string
  titulo?: string
}>()

const emit = defineEmits<{ seleccionar: [fila: T] }>()

defineSlots<{
  'fila'?: (p: { fila: T, revelado: boolean, modo: ModoBuscador, indice: number }) => unknown
  'sin-resultados'?: (p: { consulta: ConsultaPaciente, fuente: Fuente }) => unknown
}>()

const T_ = TEXTOS.buscador
const E = TEXTOS.estados
const uid = useId()

const modosVisibles = computed<ModoBuscador[]>(() =>
  props.modos?.length ? MODOS.filter(m => props.modos!.includes(m)) : [...MODOS])
const hayPestanas = computed(() => modosVisibles.value.length > 1)

const {
  borrador, aplicada, estado, filas, fuente, falta, valido, cargando, desactualizado, eco,
  cambiarModo, enviar,
} = useBuscador<T>({
  buscar: (c, s) => props.buscar(c, s),
  modoInicial: props.modoInicial && modosVisibles.value.includes(props.modoInicial)
    ? props.modoInicial
    : modosVisibles.value[0],
  memoriaClave: props.memoriaClave,
})

// v-model de los seis campos, en un solo objeto para no repetirlo por modo.
const enlaces = computed(() => ({
  'orden': borrador.orden,
  'onUpdate:orden': (v: string) => { borrador.orden = v },
  'tipo': borrador.tipo,
  'onUpdate:tipo': (v: string | null) => { borrador.tipo = v },
  'numero': borrador.numero,
  'onUpdate:numero': (v: string) => { borrador.numero = v },
  'nombres': borrador.nombres,
  'onUpdate:nombres': (v: string) => { borrador.nombres = v },
  'apellido1': borrador.apellido1,
  'onUpdate:apellido1': (v: string) => { borrador.apellido1 = v },
  'apellido2': borrador.apellido2,
  'onUpdate:apellido2': (v: string) => { borrador.apellido2 = v },
}))

// ── Submit: botón y Enter son el mismo evento `submit` ────────────────────────
const formulario = ref<HTMLFormElement | null>(null)

function alEnviar() {
  void enviar()
}

// Con el botón apagado el navegador no hace el submit implícito de Enter; lo pedimos
// nosotros con `requestSubmit()` para que Enter recorra el mismo camino y, si falta
// algo, lo diga. Un Enter que ya usó el combobox (escoger un tipo) no llega aquí.
function alEnter(e: KeyboardEvent) {
  if (e.defaultPrevented || e.isComposing) return
  if ((e.target as HTMLElement | null)?.tagName !== 'INPUT') return
  e.preventDefault()
  formulario.value?.requestSubmit()
}

// ── Estado visible ────────────────────────────────────────────────────────────
const revelado = ref(false)
watch(aplicada, () => { revelado.value = false })

const lento = ref(false)
let reloj: ReturnType<typeof setTimeout> | undefined
const encabezado = ref<HTMLElement | null>(null)

// Se reinicia con cada envío (no sólo al cambiar de estado): una búsqueda que reemplaza
// a otra en vuelo vuelve a contar sus 2 s.
watch([estado, envios], ([e]) => {
  clearTimeout(reloj)
  lento.value = false
  if (e === 'loading') reloj = setTimeout(() => { lento.value = true }, 2000)
  // Al llegar resultados, el foco va al encabezado de resultados.
  if (e === 'results') nextTick(() => encabezado.value?.focus())
})
onBeforeUnmount(() => clearTimeout(reloj))

type Tono = 'neutro' | 'aviso' | 'error' | 'cargando' | 'oculto'

const mensaje = computed<{ texto: string, tono: Tono }>(() => {
  switch (estado.value) {
    case 'idle': return { texto: E.idle, tono: 'neutro' }
    case 'incomplete': return { texto: falta.value ?? '', tono: 'aviso' }
    case 'loading': return { texto: E.cargando, tono: 'cargando' }
    case 'results': return { texto: T_.resultados(filas.value.length), tono: 'oculto' }
    case 'no-results': return {
      texto: aplicada.value?.modo === 'documento' ? E.sinResultadosDocumento(fuente.value) : E.sinResultados(fuente.value),
      tono: 'neutro',
    }
    case 'error': return { texto: E.error, tono: 'error' }
    case 'forbidden': return { texto: E.prohibido, tono: 'error' }
    case 'rate-limited': return { texto: E.limitado, tono: 'aviso' }
    case 'truncated': return { texto: E.truncado, tono: 'aviso' }
  }
  return { texto: '', tono: 'oculto' }
})

const ICONO: Record<Exclude<Tono, 'oculto'>, string> = {
  neutro: 'info', aviso: 'warning', error: 'error', cargando: 'spinner',
}

const cajaDe = (tono: Tono) => cn(
  'flex items-start gap-2 rounded-md px-3 py-2 text-sm',
  tono === 'neutro' && 'bg-muted text-muted-foreground',
  tono === 'cargando' && 'text-muted-foreground',
  tono === 'aviso' && 'border border-status-warning/40 bg-status-warning-bg text-foreground',
  tono === 'error' && 'border border-status-error/40 bg-status-error-bg text-foreground',
)
const iconoDe = (tono: Tono) => cn(
  'mt-0.5 shrink-0',
  tono === 'cargando' && 'animate-spin',
  tono === 'aviso' && 'text-status-warning',
  tono === 'error' && 'text-status-error',
)

const verFilas = computed(() => filas.value.length > 0 && !cargando.value)

// ── Render por defecto de un Paciente ─────────────────────────────────────────
function esPaciente(x: unknown): x is Paciente {
  return typeof x === 'object' && x !== null && 'nombres' in x && 'apellido1' in x
}
function claveDe(fila: T, i: number): string | number {
  const r = fila as Record<string, unknown> | null
  return typeof r === 'object' && r !== null && (typeof r.id === 'string' || typeof r.orden === 'string')
    ? String(r.id ?? r.orden)
    : i
}
const fecha = (iso: string) => iso.split('-').reverse().join('/')

// ── API para la pantalla ──────────────────────────────────────────────────────
function enfocar() {
  nextTick(() => formulario.value?.querySelector<HTMLElement>('[data-bq-primero]')?.focus())
}

function llenar(parcial: Partial<BorradorBuscador>) {
  const { modo, ...campos } = parcial
  if (modo && modosVisibles.value.includes(modo)) cambiarModo(modo)
  Object.assign(borrador, campos)
}

defineExpose({ enfocar, enviar, llenar })
</script>

<template>
  <section class="@container flex min-w-0 flex-col gap-4" :aria-labelledby="`${uid}-titulo`">
    <h2 :id="`${uid}-titulo`" class="text-base font-semibold">
      {{ titulo ?? T_.titulo }}
    </h2>

    <form
      ref="formulario"
      role="search"
      autocomplete="off"
      novalidate
      :aria-labelledby="`${uid}-titulo`"
      class="flex flex-col gap-4"
      @submit.prevent="alEnviar"
      @keydown.enter="alEnter"
    >
      <Tabs
        v-if="hayPestanas"
        :model-value="borrador.modo"
        class="gap-4"
        @update:model-value="(v) => cambiarModo(v as ModoBuscador)"
      >
        <TabsList
          :aria-label="T_.buscarPor"
          :class="cn('grid w-full', modosVisibles.length === 3 ? 'grid-cols-3' : 'grid-cols-2')"
        >
          <TabsTrigger v-for="m in modosVisibles" :key="m" :value="m" class="min-w-0 px-1 text-xs @xs:text-sm">
            {{ T_.modos[m] }}
          </TabsTrigger>
        </TabsList>
        <TabsContent v-for="m in modosVisibles" :key="m" :value="m">
          <BuscadorModo :modo="m" v-bind="enlaces" />
        </TabsContent>
      </Tabs>
      <BuscadorModo v-else :modo="borrador.modo" v-bind="enlaces" />

      <div>
        <Button type="submit" :disabled="!valido" class="w-full sm:w-auto">
          <Icon name="search" />
          {{ T_.buscar }}
        </Button>
      </div>
    </form>

    <div class="flex min-w-0 flex-col gap-3">
      <!-- El eco va SIEMPRE encima de los resultados. -->
      <p v-if="eco" class="text-sm" data-testid="buscador-eco">
        {{ eco }}
      </p>

      <!-- Una sola región viva: cada cambio de estado se anuncia una vez. -->
      <div role="status" aria-live="polite" class="flex flex-col gap-2" data-testid="buscador-estado">
        <p
          v-if="mensaje.texto && mensaje.tono !== 'oculto'"
          :class="cajaDe(mensaje.tono)"
          :data-estado="estado"
        >
          <Icon :name="ICONO[mensaje.tono]" :class="iconoDe(mensaje.tono)" />
          <span>
            {{ mensaje.texto }}
            <template v-if="estado === 'loading' && lento"><br>{{ E.cargandoLento }}</template>
          </span>
        </p>
        <span v-else-if="mensaje.texto" class="sr-only">{{ mensaje.texto }}</span>

        <p v-if="desactualizado" :class="cajaDe('aviso')" data-testid="buscador-desactualizado">
          <Icon name="refresh" :class="iconoDe('aviso')" />
          <span>{{ E.desactualizado }}</span>
        </p>
      </div>

      <slot
        v-if="estado === 'no-results' && aplicada"
        name="sin-resultados"
        :consulta="aplicada"
        :fuente="fuente"
      />

      <section v-if="verFilas" class="flex min-w-0 flex-col gap-2" :aria-labelledby="`${uid}-res`">
        <div class="flex items-center justify-between gap-2">
          <h3
            :id="`${uid}-res`"
            ref="encabezado"
            tabindex="-1"
            class="text-sm font-semibold outline-none focus-visible:ring-3 focus-visible:ring-ring/50 rounded-sm"
          >
            {{ T_.resultados(filas.length) }}
          </h3>
          <Button
            type="button"
            variant="outline"
            size="sm"
            :aria-pressed="revelado"
            :aria-label="revelado ? T_.ocultarNombres : T_.mostrarNombres"
            @click="revelado = !revelado"
          >
            <Icon name="view" />
            {{ revelado ? T_.ocultar : T_.mostrar }}
          </Button>
        </div>

        <ul :class="cn('divide-y rounded-lg border', desactualizado && 'opacity-60')" data-testid="buscador-filas">
          <li v-for="(fila, i) in filas" :key="claveDe(fila, i)">
            <button
              type="button"
              class="flex w-full min-w-0 flex-col items-start gap-0.5 px-3 py-2.5 text-left text-sm outline-none hover:bg-accent focus-visible:bg-accent focus-visible:ring-3 focus-visible:ring-ring/50"
              @click="emit('seleccionar', fila)"
            >
              <slot name="fila" :fila="fila" :revelado="revelado" :modo="aplicada?.modo ?? borrador.modo" :indice="i">
                <template v-if="esPaciente(fila)">
                  <span class="font-medium" :class="revelado ? '' : 'font-mono tracking-wide'">
                    {{ revelado ? nombreCompleto(fila) : enmascararNombre(nombreCompleto(fila)) }}
                  </span>
                  <span v-if="aplicada?.modo === 'nombre'" class="text-xs text-muted-foreground">
                    {{ [
                      fila.nacimiento ? fecha(fila.nacimiento) : '',
                      fila.nacimiento ? T_.edad(edad(fila.nacimiento)) : '',
                      fila.sexo ? T_.sexo[fila.sexo] : '',
                    ].filter(Boolean).join(' · ') }}
                  </span>
                  <span v-else-if="fila.numero" class="font-mono text-xs text-muted-foreground">
                    {{ fila.tipo }} {{ enmascararDocumento(fila.numero) }}
                  </span>
                </template>
                <span v-else-if="typeof fila !== 'object'">{{ String(fila) }}</span>
              </slot>
            </button>
          </li>
        </ul>
      </section>
    </div>
  </section>
</template>
