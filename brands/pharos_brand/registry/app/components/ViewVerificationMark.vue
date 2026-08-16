<script setup lang="ts">
// ViewVerificationMark — la misma verdad que ViewVerification, pero ANTES de entrar.
//
// Existe porque el envoltorio llega tarde: para leerlo hay que estar ya adentro, y
// para entonces la persona ya escogió esa vista sobre otra. El chip del sidebar
// convierte el estado en algo que se ve mientras se decide a dónde ir.
//
// place="nav"        · punto en la opción del sidebar (cabe en el riel colapsado)
// place="breadcrumb" · chip con palabra en el topbar — el estado, junto al nombre
//
// El punto del nav NO lleva palabra por espacio, así que su segundo canal es el
// `title` + el texto sr-only. El del breadcrumb sí la lleva: color + icono + palabra.
import { computed } from 'vue'
import { VERIFICATION_STATES, toneFor, type VerificationTone, type ViewVerification } from '~/lib/verification'

const props = withDefaults(defineProps<{
  v?: ViewVerification
  place?: 'nav' | 'breadcrumb'
  /** Registro de color de la app. `no-conforme` lo ignora y va siempre en rojo (toneFor). */
  tone?: VerificationTone
}>(), { v: undefined, place: 'nav', tone: 'verify' })

// El chip pinta su propio registro, sin depender de que un ancestro lo haya puesto: en el nav y
// el breadcrumb no hay envoltorio de vista arriba que lo herede.
const tone = computed(() => props.v ? toneFor(props.v.estado, props.tone) : props.tone)

const meta = computed(() => props.v ? VERIFICATION_STATES[props.v.estado] : null)
// Titular sin el sufijo declarativo: en un chip de 90px «En verificación» basta,
// y el detalle completo ya lo carga la banda de la vista.
const corto = computed(() => meta.value?.label.split(' · ')[0] ?? '')
</script>

<template>
  <template v-if="v && meta">
    <!-- nav: un punto. Sobrevive el sidebar colapsado a riel de iconos, donde
         cualquier palabra se truncaría a nada. -->
    <span
      v-if="place === 'nav'"
      :data-verify-tone="tone"
      class="ml-auto flex shrink-0 items-center"
      :title="`${meta.label} — responsable: ${v.responsable.nombre}, ${v.responsable.cargo}`"
    >
      <span aria-hidden="true" class="size-1.5 rounded-full bg-verify-ink ring-2 ring-verify-ink/25" />
      <span class="sr-only">{{ meta.label }}</span>
    </span>

    <!-- breadcrumb: color + icono + palabra, los tres canales. -->
    <span
      v-else
      :data-verify-tone="tone"
      class="inline-flex shrink-0 items-center gap-1.5 whitespace-nowrap rounded-full bg-verify-bg px-2 py-0.5 text-verify-ink"
      :title="`${meta.label} — responsable: ${v.responsable.nombre}, ${v.responsable.cargo}`"
    >
      <Icon :name="meta.icon" :size="4" />
      <span class="font-mono text-[10px] font-semibold uppercase tracking-wider">{{ corto }}</span>
    </span>
  </template>
</template>
