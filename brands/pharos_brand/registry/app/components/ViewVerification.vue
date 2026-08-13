<script setup lang="ts">
// ViewVerification — la marca de «esta vista todavía no está liberada».
// Cara de pantalla de PROT-SW-001 (lch-kb fase-0). Vocabulario y reglas:
// app/lib/verification.ts — léelo primero, ahí está el porqué de cada una.
//
// ES UN ENVOLTORIO, no un banner suelto, y esa es la decisión de diseño principal:
//
//   <ViewVerification :v="verificationFor(route.path)">
//     …toda la vista…
//   </ViewVerification>
//
// Un solo punto de montaje por vista ⇒ (a) una línea para poner la marca y una para
// quitarla, (b) un script de CI puede contar montajes y cruzarlos contra el
// manifiesto, y (c) —lo que de verdad importa— la banda y el lavado del lienzo NO
// PUEDEN SEPARARSE. Si fueran dos piezas, alguien copia la banda a una vista nueva y
// olvida el lavado, o al revés, y la marca queda a medias sin que nada lo note.
//
// ── Por qué el lavado se IZA al contenedor (`bleed`) ──
// El lavado tiene que cubrir el lienzo ENTERO, incluido el padding del scroller;
// pintado solo dentro del envoltorio deja un marco sin teñir que delata el truco.
// Podría pedirse que cada app le ponga una clase a su `<main>` — y ahí está
// exactamente la trampa de SystemBeacon: su registro se elige en runtimeConfig pero
// el montaje del lienzo vive en `layouts/default.vue`, que el script de sync nunca
// toca, así que una app puede quedar con un registro que nadie renderiza. Acá el
// componente BUSCA su contenedor y le pone los atributos él mismo (y los quita al
// desmontarse). Cero scaffold que adoptar, cero manera de adoptarlo a medias.
//
// `v` undefined (vista liberada) ⇒ renderiza el contenido tal cual, sin envoltorio y
// sin marca. La ausencia ES el estado liberado.
import { computed, onBeforeUnmount, ref, watchEffect } from 'vue'
import {
  VERIFICATION_STATES,
  toneFor,
  type VerificationDensity,
  type VerificationTone,
  type ViewVerification,
} from '~/lib/verification'

const props = withDefaults(defineProps<{
  /** Entrada del manifiesto. `undefined` = vista liberada ⇒ no dibuja nada. */
  v?: ViewVerification
  /** Registro de color. Default `verify` (token propio, fuera de la paleta clínica). */
  tone?: VerificationTone
  /** Cuánto cromo ocupa la banda. */
  density?: VerificationDensity
  /** Franja diagonal = segundo canal no cromático. Apagarla es solo para comparar. */
  hatch?: boolean
  /** Teñir el lienzo. Apagarlo es solo para comparar: la banda sola se scrollea fuera. */
  wash?: boolean
  /**
   * Izar el lavado al contenedor de la vista + fijar la banda arriba. Así se usa de
   * verdad. `false` = todo contenido en el envoltorio, para mostrarlo dentro de una
   * tarjeta (el playground) sin que varias muestras se peleen el mismo lienzo.
   */
  bleed?: boolean
  /** Selector del contenedor a teñir. `[data-pg-content]` es el lienzo del shell Pháros. */
  container?: string
}>(), {
  v: undefined,   // sin entrada de manifiesto = vista liberada
  tone: 'verify',
  density: 'completa',
  hatch: true,
  wash: true,
  bleed: true,
  container: '[data-pg-content]',
})

// Plegar/desplegar. NUNCA se descarta: plegada sigue siendo una franja visible con el
// titular Y el responsable. Una marca de seguridad clínica con botón de «cerrar» es
// una marca que no está — la primera persona apurada la cierra y la vista queda muda.
const open = ref(true)

const meta = computed(() => props.v ? VERIFICATION_STATES[props.v.estado] : null)
// `no-conforme` ignora el registro de la app y va siempre en rojo — ver toneFor().
const tone = computed(() => props.v ? toneFor(props.v.estado, props.tone) : props.tone)
const compact = computed(() => props.density === 'compacta')
const strip = computed(() => props.density === 'franja')
// Franja y plegada son la misma forma; se separan por origen, no por pintura.
const folded = computed(() => strip.value || !open.value)
const root = ref<HTMLElement | null>(null)

// ── izado del lavado ──
// El elemento teñido se recuerda en `painted` en vez de re-resolverse al limpiar: si
// la vista se desmonta durante una navegación, el contenedor puede haber cambiado ya
// y una segunda resolución dejaría el tinte pegado en el lienzo de la vista SIGUIENTE.
let painted: HTMLElement | null = null

function clear() {
  if (!painted) return
  delete painted.dataset.viewVerification
  delete painted.dataset.verifyTone
  painted = null
}

watchEffect(() => {
  if (!import.meta.client) return
  const on = !!props.v && !!meta.value && props.bleed && props.wash
  const target = on ? (root.value?.closest(props.container) as HTMLElement | null) : null
  if (painted && painted !== target) clear()
  if (!target) return
  target.dataset.viewVerification = props.v!.estado
  target.dataset.verifyTone = tone.value
  painted = target
})

onBeforeUnmount(clear)

const aria = computed(() => {
  if (!props.v || !meta.value) return ''
  const r = props.v.responsable
  return `${meta.value.label}. ${meta.value.leyenda} Responsable de la verificación: ${r.nombre}, ${r.cargo}.`
})
</script>

<template>
  <!-- Sin entrada de manifiesto: la vista se renderiza intacta, sin envoltorio. -->
  <slot v-if="!v || !meta" />

  <div
    v-else
    ref="root"
    :data-verify-tone="tone"
    :data-view-verification="bleed ? undefined : v.estado"
    :class="[
      'flex min-w-0 flex-col',
      // sin izado el envoltorio carga el lavado él mismo (muestra en tarjeta)
      !bleed && wash && 'bg-verify-wash overflow-hidden rounded-lg border border-verify-ink/25',
    ]"
  >
    <!-- LA BANDA. Fija arriba: el lienzo es el scroller, así que una banda estática se
         va con el contenido y una vista larga acaba pareciendo liberada. Se queda. -->
    <div :class="bleed ? 'sticky top-0 z-20 mb-6' : ''">
      <!-- Tapa el padding del scroller. `sticky top-0` se ancla al borde de la CAJA DE
           PADDING, no al del scrollport, así que arriba de la banda queda una franja por
           la que el contenido desfila — y una tabla clínica pasando por encima de su
           propia advertencia se ve como un error de render. Alto generoso: lo que sobre
           queda fuera del scrollport y se recorta solo, así sirve para las 3 densidades. -->
      <span
        v-if="bleed"
        aria-hidden="true"
        :class="['pointer-events-none absolute inset-x-0 bottom-full h-12', wash ? 'bg-verify-wash' : 'bg-background']"
      />
      <aside
        :aria-label="aria"
        :class="[
          'flex overflow-hidden border-verify-ink/30 bg-verify-ink text-verify-on-ink',
          bleed ? 'rounded-lg border shadow-md' : 'border-b',
        ]"
      >
      <!-- Riel rayado: el segundo canal. Sobrevive B/N, fotocopia y daltonismo. -->
      <span v-if="hatch" aria-hidden="true" class="pharos-verify-hatch w-3.5 shrink-0" />

      <div :class="['flex min-w-0 flex-1 items-start gap-3', folded ? 'px-4 py-1.5' : 'px-4 py-3']">
        <Icon :name="meta.icon" :size="folded ? 4 : 5" :class="folded ? 'mt-0.5' : 'mt-px'" />

        <div class="min-w-0 flex-1">
          <!-- Titular. Mono + versalitas: el registro de «esto es un sello», no prosa. -->
          <p class="flex flex-wrap items-baseline gap-x-2 gap-y-0.5 font-mono text-[11px] font-semibold uppercase tracking-wider">
            {{ meta.label }}
            <!-- Plegada o compacta, el responsable viaja EN el titular: es el dato que
                 no puede desaparecer al ahorrar espacio. Sin él la banda dice que algo
                 está a medias y no dice a quién preguntar. -->
            <span v-if="folded || compact" class="font-sans text-[11px] font-normal normal-case tracking-normal opacity-90">
              · {{ v.responsable.nombre }} · {{ v.responsable.cargo }}
            </span>
          </p>

          <template v-if="!folded">
            <p class="mt-1 text-sm leading-snug">{{ meta.leyenda }}</p>

            <!-- La restricción de §6.1. Es la razón de ser del estado acotado: sin el
                 texto, la marca afirmaría una salvaguarda que nadie declaró. -->
            <p
              v-if="v.restriccion"
              class="mt-2 border-l-2 border-verify-on-ink/40 pl-2.5 text-sm font-medium leading-snug"
            >
              {{ v.restriccion }}
            </p>

            <!-- Responsable NOMINAL: nombre + cargo, nunca un @handle (SOP-000 §4). -->
            <p v-if="!compact" class="mt-2 flex flex-wrap items-center gap-x-1.5 text-sm">
              <Icon name="userRound" :size="4" class="opacity-80" />
              <span class="opacity-80">Responsable de la verificación:</span>
              <span class="font-medium">{{ v.responsable.nombre }}</span>
              <span class="opacity-80">· {{ v.responsable.cargo }}</span>
            </p>

            <p
              v-if="v.protocolo || v.expediente || v.desde"
              class="mt-1.5 font-mono text-[10px] uppercase tracking-wide opacity-75"
            >
              <span v-if="v.protocolo">{{ v.protocolo }}</span>
              <span v-if="v.expediente"> · {{ v.expediente }}</span>
              <span v-if="v.desde"> · desde {{ v.desde }}</span>
            </p>
          </template>
        </div>

        <!-- Plegar, no descartar: `franja` es una decisión de la vista y no ofrece el
             control; en las otras densidades el control colapsa a la MISMA franja. -->
        <Button
          v-if="!strip"
          variant="ghost"
          size="sm"
          class="-my-1 h-7 shrink-0 gap-1 px-2 font-mono text-[10px] uppercase tracking-wide text-verify-on-ink hover:bg-verify-on-ink/15 hover:text-verify-on-ink"
          :aria-expanded="open"
          @click="open = !open"
        >
          {{ open ? 'Plegar' : 'Ver detalle' }}
          <Icon name="chevronDown" :size="4" :class="open ? 'rotate-180' : ''" />
        </Button>
        </div>
      </aside>
    </div>

    <div :class="['min-w-0 flex-1', !bleed && 'p-4']">
      <slot />
    </div>
  </div>
</template>
