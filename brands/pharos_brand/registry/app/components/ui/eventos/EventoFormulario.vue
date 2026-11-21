<script setup lang="ts">
// EventoFormulario — el formulario de reporte de un evento (Pháros · Organización, plan 2.4).
//
// Lo usan Organización y, por el pie del sidebar, cualquier otra app Pháros (Pháros LIS primero).
// Es la misma pieza para todas: la app anfitriona le pasa DÓNDE está (`app`, `pantalla`) y, si
// quiere, la orden de servicio que tiene abierta como SUGERENCIA.
//
// Reglas que este componente sostiene (no son opciones):
//   • Solo habla con `${apiBase}/eventos` — el BFF de la propia app (RFC 0013 / 0017).
//   • La orden sugerida NO viaja a menos que quien reporta marque la casilla. Sin marcar, el
//     cuerpo del POST ni siquiera lleva la llave `orden_servicio`.
//   • El texto libre pasa por el portón de datos de pacientes en el servidor; si lo rechaza (422),
//     se pintan los NOMBRES de las reglas, nunca el texto, y el texto escrito se conserva para que
//     la persona lo corrija.
//   • El aviso «no escribas nombres» no se puede quitar ni cerrar.
//   • El contacto de una queja viaja DENTRO del mismo reporte (nunca en una llamada aparte) y se borra
//     del estado del componente apenas se envía.
//
// Colores y tipografía: solo el contrato de tokens (tokens.css). Spec: ./README.md
import { computed, reactive, ref, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { crearEventosApi, ErrorEventosApi } from '@/lib/eventosApi'
import type { EventosApi, FetchLike } from '@/lib/eventosApi'
import {
  ERRORES, LLEGO_A_ALGUIEN, SEDES, TEXTOS, TIPOS_EVENTO,
} from './types'
import type {
  ErrorDeEventos, EventoReportado, LlegoAAlguien, MedioContacto,
  ProcesoOpcion, ReporteEnvio, Sede, TipoEvento,
} from './types'

const props = withDefaults(defineProps<{
  /** Ruta de la app anfitriona, relativa al origen (`/<app>/api`). El componente añade `/eventos`. */
  apiBase: string
  /** Nombre de la app anfitriona, tal como se lee («Pháros LIS»). Solo se muestra. */
  app: string
  /** Pantalla desde la que se abrió, como identificador (`minúsculas, dígitos, . _ -`). Viaja como `pantalla_origen`. */
  pantalla: string
  /** Procesos del mapa que la app trae de Organización. */
  procesos: ProcesoOpcion[]
  /** Orden de servicio que la pantalla tiene abierta. SUGERENCIA: solo se guarda si se confirma. */
  ordenSugerida?: string | null
  /** Sede con la que arranca el formulario (la de la sesión), si la app la conoce. */
  sedeInicial?: Sede | null
  /** Aviso de tratamiento de datos para quien se queja. Si falta el texto oficial, va el genérico. */
  avisoQueja?: string
  /** Encabezados extra por llamada (CSRF). Nunca secretos de servicio. */
  headers?: () => Record<string, string>
  /** Solo para pruebas: reemplaza el `fetch` del navegador. */
  fetcher?: FetchLike
  /** Para pruebas: reemplaza el cliente completo. */
  api?: EventosApi
  class?: string
}>(), {
  ordenSugerida: null,
  sedeInicial: null,
  avisoQueja: TEXTOS.quejaAvisoDefecto,
})

const emit = defineEmits<{
  (e: 'reportado', evento: { id: string, consecutivo: string, pendienteDeRevision: boolean }): void
  (e: 'cancelar'): void
  (e: 'error', error: ErrorDeEventos): void
}>()

const SLUG = /^[a-z][a-z0-9_.-]{0,63}$/
const SOLO_DIGITOS = /^\d+$/

const api = computed(() => props.api ?? crearEventosApi({
  apiBase: props.apiBase, headers: props.headers, fetch: props.fetcher,
}))

const f = reactive({
  tipo: '' as TipoEvento | '',
  proceso: '',
  sede: (props.sedeInicial ?? '') as Sede | '',
  descripcion: '',
  ocurrencia: '',
  conocimiento: '',
  llego: '' as LlegoAAlguien | '',
  seguridad: '' as 'si' | 'no' | '',
  confirmaOrden: false,
  quejaNombre: '',
  quejaMedio: 'correo' as MedioContacto,
  quejaContacto: '',
  quejaAviso: false,
})

const enviando = ref(false)
const fallo = ref<ErrorDeEventos | null>(null)
const exito = ref<{ id: string, consecutivo: string, pendiente: boolean } | null>(null)
const intentado = ref(false)

const esQueja = computed(() => f.tipo === 'queja')
const ordenLimpia = computed(() => (props.ordenSugerida ?? '').trim())
const hayOrden = computed(() => ordenLimpia.value !== '' && SOLO_DIGITOS.test(ordenLimpia.value))
// El tope de las fechas es «ahora», y «ahora» cambia: se recalcula al enviar y al enfocar una fecha,
// no una sola vez al montar (un formulario abierto una hora no puede rechazar lo ocurrido hace un minuto).
const ahoraLocal = () => {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
}
const maximo = ref(ahoraLocal())
const refrescarMaximo = () => { maximo.value = ahoraLocal() }

// Una orden sugerida distinta es OTRA orden: la confirmación de la anterior no se hereda.
watch(() => props.ordenSugerida, () => { f.confirmaOrden = false })

watch(() => f.tipo, () => { fallo.value = null })

// El servidor nombra los campos como en su cuerpo; el formulario los llama distinto.
const CAMPO_CLIENTE: Record<string, string> = {
  tipo: 'tipo', proceso_codigo: 'proceso', sede: 'sede', descripcion: 'descripcion',
  fecha_ocurrencia: 'ocurrencia', fecha_conocimiento: 'conocimiento', llego_a_alguien: 'llego',
  seguridad_paciente: 'seguridad', orden_servicio: 'orden', contacto: 'quejaContacto',
}
const marcadosPorServidor = computed(() => {
  const m = new Set<string>()
  for (const c of fallo.value?.campos ?? []) { const k = CAMPO_CLIENTE[c]; if (k) m.add(k) }
  return m
})

const errores = computed(() => {
  const e: Record<string, string> = {}
  if (!f.tipo) e.tipo = TEXTOS.campoObligatorio
  if (!f.proceso) e.proceso = TEXTOS.campoObligatorio
  if (!f.sede) e.sede = TEXTOS.campoObligatorio
  if (!f.descripcion.trim()) e.descripcion = TEXTOS.campoObligatorio
  if (!f.ocurrencia) e.ocurrencia = TEXTOS.campoObligatorio
  else if (f.ocurrencia > maximo.value) e.ocurrencia = TEXTOS.fechaFutura
  if (!f.conocimiento) e.conocimiento = TEXTOS.campoObligatorio
  else if (f.conocimiento > maximo.value) e.conocimiento = TEXTOS.fechaFutura
  if (!f.llego) e.llego = TEXTOS.campoObligatorio
  if (!f.seguridad) e.seguridad = TEXTOS.campoObligatorio
  if (esQueja.value) {
    if (!f.quejaNombre.trim()) e.quejaNombre = TEXTOS.campoObligatorio
    if (f.quejaContacto.trim().length < 3) e.quejaContacto = TEXTOS.campoObligatorio
    if (!f.quejaAviso) e.quejaAviso = TEXTOS.campoObligatorio
  }
  return e
})
const ver = (campo: string) => {
  const propio = intentado.value ? errores.value[campo] : undefined
  if (propio) return propio
  if (!marcadosPorServidor.value.has(campo)) return undefined
  // Un mensaje propio del servidor, solo si señaló UN campo; si no, el genérico del campo.
  const f1 = fallo.value
  return f1 && f1.causa === 'validacion' && f1.campos?.length === 1 && f1.mensaje !== ERRORES.validacion
    ? f1.mensaje
    : TEXTOS.campoRevisar
}
/** Une el id de la ayuda fija con el del error visible, para `aria-describedby`. */
const descrito = (campo: string, fija?: string) => [fija, ver(campo) ? `pg-ev-err-${campo}` : undefined].filter(Boolean).join(' ') || undefined

/** Un instante con zona horaria (el servidor rechaza fechas sin zona). */
const aInstante = (local: string) => new Date(local).toISOString()

function construirCuerpo(): ReporteEnvio {
  const cuerpo: ReporteEnvio = {
    tipo: f.tipo as TipoEvento,
    proceso_codigo: f.proceso,
    sede: f.sede as Sede,
    descripcion: f.descripcion.trim(),
    fecha_ocurrencia: aInstante(f.ocurrencia),
    fecha_conocimiento: aInstante(f.conocimiento),
    llego_a_alguien: f.llego as LlegoAAlguien,
    seguridad_paciente: f.seguridad === 'si',
  }
  if (SLUG.test(props.pantalla)) cuerpo.pantalla_origen = props.pantalla
  // 🔑 La orden viaja SOLO si hay una sugerida Y la persona la confirmó.
  if (hayOrden.value && f.confirmaOrden) cuerpo.orden_servicio = ordenLimpia.value
  if (esQueja.value) {
    cuerpo.contacto = {
      nombre: f.quejaNombre.trim(),
      medio: f.quejaMedio,
      contacto: f.quejaContacto.trim(),
      aviso_aceptado: true,
    }
  }
  return cuerpo
}

async function enviar() {
  refrescarMaximo()
  intentado.value = true
  fallo.value = null
  if (Object.keys(errores.value).length) {
    fallo.value = { causa: 'validacion', mensaje: TEXTOS.faltanCampos }
    return
  }
  enviando.value = true
  let creado: EventoReportado
  try {
    creado = await api.value.reportar(construirCuerpo())
  } catch (e) {
    const detalle = e instanceof ErrorEventosApi ? e.detalle : { causa: 'otro', mensaje: ERRORES.otro } as ErrorDeEventos
    fallo.value = detalle
    emit('error', detalle)
    enviando.value = false
    return
  }
  // El contacto es dato personal: sale del estado en cuanto el reporte quedó guardado.
  f.quejaNombre = ''
  f.quejaContacto = ''
  f.quejaAviso = false
  exito.value = {
    id: creado.id,
    consecutivo: creado.consecutivo,
    pendiente: creado.pendiente_de_revision === true,
  }
  enviando.value = false
  emit('reportado', {
    id: creado.id, consecutivo: creado.consecutivo, pendienteDeRevision: creado.pendiente_de_revision === true,
  })
}

const campo = 'h-9 w-full rounded-md border border-input bg-background px-2 text-sm text-foreground outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 aria-invalid:border-status-error'
</script>

<template>
  <form
    :class="cn('space-y-3 text-sm', props.class)"
    data-pg-evento-form
    novalidate
    @submit.prevent="enviar"
  >
    <p class="text-xs text-muted-foreground">
      {{ TEXTOS.abiertoDesde }}: <span class="font-mono" data-pg-evento-origen>{{ app }} / {{ pantalla }}</span>
    </p>

    <!-- Éxito: reemplaza el formulario. El consecutivo es un identificador, no un dato de persona. -->
    <div v-if="exito" class="space-y-3" data-pg-evento-exito>
      <div
        role="status"
        :class="cn('rounded-md border px-3 py-2', exito.pendiente ? 'border-status-warning bg-status-warning-bg' : 'border-status-success bg-status-success-bg')"
      >
        {{ exito.pendiente ? TEXTOS.pendiente(exito.consecutivo) : TEXTOS.reportado(exito.consecutivo) }}
      </div>
      <div class="flex justify-end">
        <Button type="button" size="sm" variant="outline" @click="emit('cancelar')">{{ TEXTOS.cerrar }}</Button>
      </div>
    </div>

    <template v-else>
      <div class="grid gap-3 sm:grid-cols-2">
        <div class="space-y-1">
          <label for="pg-ev-tipo" class="font-medium">{{ TEXTOS.tipo }}</label>
          <select id="pg-ev-tipo" v-model="f.tipo" :class="campo" :aria-invalid="!!ver('tipo')" :aria-describedby="descrito('tipo', 'pg-ev-tipo-ayuda')" data-pg-campo="tipo">
            <option value="">{{ TEXTOS.tipoElige }}</option>
            <option v-for="t in TIPOS_EVENTO" :key="t.id" :value="t.id">{{ t.label }}</option>
          </select>
          <p id="pg-ev-tipo-ayuda" class="text-xs text-muted-foreground">{{ TEXTOS.tipoAyuda }}</p>
          <p v-if="ver('tipo')" id="pg-ev-err-tipo" class="text-xs text-status-error">{{ ver('tipo') }}</p>
        </div>

        <div class="space-y-1">
          <label for="pg-ev-proceso" class="font-medium">{{ TEXTOS.proceso }}</label>
          <select id="pg-ev-proceso" v-model="f.proceso" :class="campo" :aria-invalid="!!ver('proceso')" :aria-describedby="descrito('proceso')" required data-pg-campo="proceso">
            <option value="">{{ TEXTOS.procesoElige }}</option>
            <option v-for="p in procesos" :key="p.codigo" :value="p.codigo">{{ p.codigo }} · {{ p.nombre }}</option>
          </select>
          <p v-if="ver('proceso')" id="pg-ev-err-proceso" class="text-xs text-status-error">{{ ver('proceso') }}</p>
        </div>

        <div class="space-y-1">
          <label for="pg-ev-sede" class="font-medium">{{ TEXTOS.sede }}</label>
          <select id="pg-ev-sede" v-model="f.sede" :class="campo" :aria-invalid="!!ver('sede')" :aria-describedby="descrito('sede')" required data-pg-campo="sede">
            <option value="">{{ TEXTOS.sedeElige }}</option>
            <option v-for="s in SEDES" :key="s.id" :value="s.id">{{ s.label }}</option>
          </select>
          <p v-if="ver('sede')" id="pg-ev-err-sede" class="text-xs text-status-error">{{ ver('sede') }}</p>
        </div>

        <div class="space-y-1">
          <label for="pg-ev-llego" class="font-medium">{{ TEXTOS.llego }}</label>
          <select id="pg-ev-llego" v-model="f.llego" :class="campo" :aria-invalid="!!ver('llego')" :aria-describedby="descrito('llego')" required data-pg-campo="llego">
            <option value="">{{ TEXTOS.llegoElige }}</option>
            <option v-for="o in LLEGO_A_ALGUIEN" :key="o.id" :value="o.id">{{ o.label }}</option>
          </select>
          <p v-if="ver('llego')" id="pg-ev-err-llego" class="text-xs text-status-error">{{ ver('llego') }}</p>
        </div>

        <div class="space-y-1">
          <label for="pg-ev-ocurrio" class="font-medium">{{ TEXTOS.fechaOcurrencia }}</label>
          <input id="pg-ev-ocurrio" v-model="f.ocurrencia" type="datetime-local" :max="maximo" @focus="refrescarMaximo" :class="campo" :aria-invalid="!!ver('ocurrencia')" :aria-describedby="descrito('ocurrencia')" required data-pg-campo="ocurrencia">
          <p v-if="ver('ocurrencia')" id="pg-ev-err-ocurrencia" class="text-xs text-status-error">{{ ver('ocurrencia') }}</p>
        </div>

        <div class="space-y-1">
          <label for="pg-ev-supo" class="font-medium">{{ TEXTOS.fechaConocimiento }}</label>
          <input id="pg-ev-supo" v-model="f.conocimiento" type="datetime-local" :max="maximo" @focus="refrescarMaximo" :class="campo" :aria-invalid="!!ver('conocimiento')" :aria-describedby="descrito('conocimiento')" required data-pg-campo="conocimiento">
          <p v-if="ver('conocimiento')" id="pg-ev-err-conocimiento" class="text-xs text-status-error">{{ ver('conocimiento') }}</p>
        </div>
      </div>

      <fieldset class="space-y-1">
        <legend class="font-medium">{{ TEXTOS.seguridad }}</legend>
        <div class="flex gap-4" data-pg-campo="seguridad">
          <label class="flex items-center gap-2"><input v-model="f.seguridad" type="radio" name="pg-ev-seguridad" value="si"> {{ TEXTOS.si }}</label>
          <label class="flex items-center gap-2"><input v-model="f.seguridad" type="radio" name="pg-ev-seguridad" value="no"> {{ TEXTOS.no }}</label>
        </div>
        <p v-if="ver('seguridad')" id="pg-ev-err-seguridad" class="text-xs text-status-error">{{ ver('seguridad') }}</p>
      </fieldset>

      <div class="space-y-1">
        <label for="pg-ev-que" class="font-medium">{{ TEXTOS.quePaso }}</label>
        <textarea
          id="pg-ev-que" v-model="f.descripcion" rows="4" maxlength="4000"
          :class="cn('w-full rounded-md border bg-background px-2 py-1.5 text-foreground outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50', fallo?.causa === 'phi' ? 'border-status-error' : 'border-input')"
          :aria-invalid="!!ver('descripcion') || fallo?.causa === 'phi'"
          :aria-describedby="descrito('descripcion', 'pg-ev-nombres')"
          :placeholder="TEXTOS.quePasoPlaceholder"
          data-pg-campo="descripcion"
        />
        <p id="pg-ev-nombres" class="text-xs" data-pg-aviso-nombres>
          <strong>{{ TEXTOS.avisoNombres }}</strong> {{ TEXTOS.avisoNombresDetalle }}
        </p>
        <p v-if="ver('descripcion')" id="pg-ev-err-descripcion" class="text-xs text-status-error">{{ ver('descripcion') }}</p>
      </div>

      <!-- La orden sugerida: se muestra, NO se envía hasta que se confirma. -->
      <div v-if="hayOrden" class="rounded-md border border-border bg-muted/40 p-3" data-pg-sugerencia-orden>
        <p class="font-medium">{{ TEXTOS.ordenSugerida }}: <span class="font-mono">{{ ordenLimpia }}</span></p>
        <p class="text-xs text-muted-foreground">{{ TEXTOS.ordenAyuda }}</p>
        <label class="mt-2 flex items-center gap-2">
          <input v-model="f.confirmaOrden" type="checkbox" :aria-invalid="!!ver('orden')" :aria-describedby="descrito('orden')" data-pg-confirma-orden>
          {{ TEXTOS.ordenConfirmar }}
        </label>
        <p v-if="ver('orden')" id="pg-ev-err-orden" class="mt-1 text-xs text-status-error" role="alert">{{ ver('orden') }}</p>
      </div>

      <!-- Queja: el contacto de quien se queja, con su aviso. Va aparte, no en «¿Qué pasó?». -->
      <fieldset v-if="esQueja" class="space-y-2 rounded-md border border-status-warning bg-status-warning-bg p-3" data-pg-queja>
        <legend class="px-1 font-medium">{{ TEXTOS.quejaTitulo }}</legend>
        <p class="text-xs">{{ TEXTOS.quejaNombreNota }}</p>
        <div class="grid gap-3 sm:grid-cols-2">
          <div class="space-y-1 sm:col-span-2">
            <label for="pg-ev-q-nombre" class="font-medium">{{ TEXTOS.quejaNombre }}</label>
            <input id="pg-ev-q-nombre" v-model="f.quejaNombre" type="text" maxlength="160" autocomplete="off" :class="campo" :aria-invalid="!!ver('quejaNombre')" :aria-describedby="descrito('quejaNombre')" data-pg-campo="quejaNombre">
            <p v-if="ver('quejaNombre')" id="pg-ev-err-quejaNombre" class="text-xs text-status-error">{{ ver('quejaNombre') }}</p>
          </div>
          <div class="space-y-1">
            <label for="pg-ev-q-medio" class="font-medium">{{ TEXTOS.quejaMedio }}</label>
            <select id="pg-ev-q-medio" v-model="f.quejaMedio" :class="campo" data-pg-campo="quejaMedio">
              <option value="correo">{{ TEXTOS.quejaCorreo }}</option>
              <option value="telefono">{{ TEXTOS.quejaTelefono }}</option>
            </select>
          </div>
          <div class="space-y-1">
            <label for="pg-ev-q-contacto" class="font-medium">{{ TEXTOS.quejaContacto }}</label>
            <input id="pg-ev-q-contacto" v-model="f.quejaContacto" :type="f.quejaMedio === 'correo' ? 'email' : 'tel'" maxlength="160" autocomplete="off" :class="campo" :aria-invalid="!!ver('quejaContacto')" :aria-describedby="descrito('quejaContacto')" data-pg-campo="quejaContacto">
            <p v-if="ver('quejaContacto')" id="pg-ev-err-quejaContacto" class="text-xs text-status-error">{{ ver('quejaContacto') }}</p>
          </div>
        </div>
        <p class="text-xs" data-pg-aviso-queja>{{ avisoQueja }}</p>
        <label class="flex items-center gap-2">
          <input v-model="f.quejaAviso" type="checkbox" data-pg-campo="quejaAviso">
          {{ TEXTOS.quejaAvisoAcepto }}
        </label>
        <p v-if="ver('quejaAviso')" id="pg-ev-err-quejaAviso" class="text-xs text-status-error">{{ ver('quejaAviso') }}</p>
      </fieldset>

      <!-- Rechazo del portón de datos de pacientes: nombres de reglas, jamás el texto. -->
      <div v-if="fallo?.causa === 'phi'" role="alert" class="rounded-md border border-status-error bg-status-error-bg px-3 py-2" data-pg-rechazo-phi>
        <p class="font-semibold">{{ fallo.mensaje }}</p>
        <p v-if="fallo.reglas?.length">{{ TEXTOS.rechazoPhiReglas }}: <span class="font-mono">{{ fallo.reglas.join(', ') }}</span>.</p>
        <p>{{ TEXTOS.rechazoPhiPie }}</p>
      </div>
      <p v-else-if="fallo" role="alert" class="rounded-md border border-status-error bg-status-error-bg px-3 py-2" data-pg-error>
        {{ fallo.mensaje }}
      </p>

      <div class="flex justify-end gap-2">
        <Button type="button" variant="outline" size="sm" :disabled="enviando" @click="emit('cancelar')">{{ TEXTOS.cancelar }}</Button>
        <Button type="submit" size="sm" :disabled="enviando" data-pg-enviar>{{ enviando ? TEXTOS.enviando : TEXTOS.enviar }}</Button>
      </div>
    </template>
  </form>
</template>
