<script setup lang="ts">
// ConsentSignature — the generic signing surface of RFC 0030 (enmienda
// 2026-08-26): shows the consent document, captures the signature (patient or
// legal representative, plus the per-form declarations) and EMITS the
// canonical 13-field `fill` body. Presentation only: the app resolves the form
// and the blank PDF, posts the payload with its own transport/token, decides
// the PHI reveal policy and maps errors to a sentence with an owner — the same
// cut as `QueueWaitingList` / `PharosHelpChat`. The widget never fetches and
// never writes.
import { computed, ref, watch } from 'vue'
import { AlertCircle, Eraser, FileSignature, Loader2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import SignaturePad from './SignaturePad.vue'
import {
  IDENTIFICATION_TYPES,
  type ConsentBacteriologist,
  type ConsentFormDescriptor,
  type ConsentSignaturePayload,
  type ConsentSubject,
} from './types'

const props = withDefaults(defineProps<{
  form: ConsentFormDescriptor
  subject: ConsentSubject
  /** Blank PDF of the form, as a URL the browser can render (blob/object URL
   *  the app built from `GET /pdf_form/view/{name}`). `null` = still loading. */
  documentUrl: string | null
  /** A sentence with an owner when the document could not be loaded. */
  documentError?: string | null
  orderNumber?: number | null
  /** Pre-fills `entity_served` (bench forms). */
  entityServed?: string | null
  bacteriologist?: ConsentBacteriologist | null
  /** The app is posting the payload. */
  submitting?: boolean
  /** A sentence with an owner, from the app's error mapping. `null` = fine. */
  error?: string | null
  /** PHI reveal policy, decided by the app. */
  revealed?: boolean
  maskedText?: string
  /** Show the «no firma» control; the app records the decline. */
  declinable?: boolean
  title?: string
  /**
   * A QUÉ DISTANCIA SE MIRA ESTA SUPERFICIE.
   *
   * `escritorio` (por omisión) — un empleado sentado, con ratón, dentro de una
   * app con barra lateral. Es lo que consumen lab-qc y Admisiones.
   *
   * `tablet` — un dispositivo que se le ENTREGA a un paciente: de pie, con el
   * dedo, a veces con una sola mano. Cambia tres cosas y ninguna es cosmética:
   *   · el área de firma MANDA sobre el documento. Una franja delgada se firma
   *     mal —el trazo se sale y hay que repetirlo—, así que la firma crece con
   *     el alto disponible en vez de quedarse en 200 px fijos.
   *   · el documento deja de medir 384 px fijos y ocupa lo que le queda.
   *   · nada táctil por debajo de 56 px, y el texto sube a 18–20 px.
   * El widget no decide cuál es: la app lo sabe y lo dice.
   */
  density?: 'escritorio' | 'tablet'
}>(), {
  documentError: null,
  orderNumber: null,
  entityServed: null,
  bacteriologist: null,
  submitting: false,
  error: null,
  revealed: true,
  maskedText: '•••',
  declinable: true,
  title: 'Firma del consentimiento',
  density: 'escritorio',
})

const esTablet = computed(() => props.density === 'tablet')

const emit = defineEmits<{
  /** The canonical body, ready for `POST /pdf_form/fill/{form.id}`. */
  sign: [payload: ConsentSignaturePayload]
  /** The patient (or representative) refused to sign. */
  decline: []
}>()

const pad = ref<InstanceType<typeof SignaturePad> | null>(null)
const hasInk = ref(false)

const representativeSigns = ref(false)
const representativeName = ref('')
const representativeIdType = ref('NATIONAL_ID')
const representativeIdNumber = ref('')
const expeditionCity = ref('')
const conserveSamples = ref<boolean>(false)
const microscopicImages = ref<boolean>(false)

// Switching who signs empties the pad: a stroke drawn as one person is not
// evidence of the other.
watch(representativeSigns, () => {
  pad.value?.clear()
})

const masked = (value: string | undefined): string => {
  if (!value) return ''
  return props.revealed ? value : props.maskedText
}

const subjectLine = computed(() => {
  const type = IDENTIFICATION_TYPES.find(t => t.value === props.subject.identificationType)?.label
    ?? props.subject.identificationType
  const number = masked(props.subject.identificationNumber)
  return props.subject.fullName ? `${masked(props.subject.fullName)} · ${type} ${number}` : `${type} ${number}`
})

const representativeIncomplete = computed(() =>
  representativeSigns.value
  && (representativeName.value.trim().length < 3 || representativeIdNumber.value.trim().length < 3),
)

const canSign = computed(() =>
  hasInk.value
  && !props.submitting
  && !!props.documentUrl
  && !representativeIncomplete.value,
)

function onInk(value: boolean) {
  hasInk.value = value
}

function clearPad() {
  pad.value?.clear()
}

function submit() {
  const image = pad.value?.toPngBase64()
  if (!image || !canSign.value) return
  const representative = props.form.allowsLegalRepresentative && representativeSigns.value
  const payload: ConsentSignaturePayload = {
    identification_number: props.subject.identificationNumber,
    identification_type: props.subject.identificationType,
    // When the representative signs, the service prints THEIR stroke as the
    // signature and keeps a copy in the representative slot (legacy contract).
    signature_image: image,
    identification_expedition_city: expeditionCity.value.trim() || null,
    legal_representative_name: representative ? representativeName.value.trim() : null,
    legal_representative_identification: representative ? representativeIdNumber.value.trim() : null,
    legal_representative_identification_type: representative ? representativeIdType.value : null,
    patient_identification_expedition_place: props.subject.expeditionPlace ?? null,
    order_number: props.orderNumber ?? null,
    entity_served: props.entityServed ?? null,
    authorize_conservation_of_biological_samples: props.form.hasSampleConservationChoice
      ? conserveSamples.value
      : null,
    authorize_the_use_of_microscopic_images: props.form.hasMicroscopicImagesChoice
      ? microscopicImages.value
      : null,
    legal_representative_signature: representative ? image : '',
  }
  emit('sign', payload)
}
</script>

<template>
  <section
    class="flex flex-col"
    :class="esTablet
      ? 'min-h-0 flex-1 gap-5'
      : 'gap-4 rounded-lg border border-border bg-card p-4'"
    :aria-busy="submitting"
  >
    <!-- Header: what is being signed, by whom -->
    <header class="flex flex-wrap items-start justify-between gap-2">
      <div class="flex flex-col gap-0.5">
        <h2
          class="flex items-center gap-2 font-semibold text-foreground"
          :class="esTablet ? 'text-2xl' : 'text-base'"
        >
          <FileSignature :class="esTablet ? 'size-7 text-primary' : 'size-5 text-primary'" aria-hidden="true" />
          {{ title }}
        </h2>
        <p :class="esTablet ? 'text-lg text-muted-foreground' : 'text-sm text-muted-foreground'">{{ form.name }}</p>
      </div>
      <dl class="text-right text-sm">
        <dt class="text-xs uppercase tracking-wide text-muted-foreground">Paciente</dt>
        <dd class="font-mono tabular-nums text-foreground">{{ subjectLine }}</dd>
        <template v-if="orderNumber">
          <dt class="mt-1 text-xs uppercase tracking-wide text-muted-foreground">Orden</dt>
          <dd class="font-mono tabular-nums text-foreground">{{ orderNumber }}</dd>
        </template>
      </dl>
    </header>

    <!-- The document: read before signing -->
    <div
      class="overflow-hidden rounded-md border border-border bg-background"
      :class="esTablet && 'flex min-h-0 flex-[3]'"
    >
      <iframe
        v-if="documentUrl"
        :src="documentUrl"
        title="Documento de consentimiento"
        class="w-full"
        :class="esTablet ? 'h-full' : 'h-96'"
      />
      <div v-else-if="documentError" class="flex items-center gap-2 p-4 text-sm text-destructive">
        <AlertCircle class="size-4 shrink-0" aria-hidden="true" />
        <span>{{ documentError }}</span>
      </div>
      <div v-else class="flex h-96 items-center justify-center gap-2 text-sm text-muted-foreground">
        <Loader2 class="size-4 animate-spin" aria-hidden="true" />
        Cargando el documento…
      </div>
    </div>

    <!-- Who signs (bench forms only) -->
    <div v-if="form.allowsLegalRepresentative" class="flex flex-col gap-3">
      <div class="flex items-center gap-2">
        <Checkbox
          id="consent-representative"
          v-model="representativeSigns"
          :disabled="submitting"
          
        />
        <Label for="consent-representative">Firma un representante legal</Label>
      </div>
      <div v-if="representativeSigns" class="grid gap-3 sm:grid-cols-3">
        <div class="flex flex-col gap-1.5 sm:col-span-3">
          <Label for="consent-rep-name">Nombre del representante</Label>
          <Input id="consent-rep-name" v-model="representativeName" autocomplete="off" :disabled="submitting" />
        </div>
        <div class="flex flex-col gap-1.5">
          <Label for="consent-rep-id-type">Tipo de documento</Label>
          <Select v-model="representativeIdType" :disabled="submitting">
            <SelectTrigger id="consent-rep-id-type">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="t in IDENTIFICATION_TYPES" :key="t.value" :value="t.value">
                {{ t.label }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="flex flex-col gap-1.5 sm:col-span-2">
          <Label for="consent-rep-id">Número de documento</Label>
          <Input
            id="consent-rep-id"
            v-model="representativeIdNumber"
            inputmode="numeric"
            autocomplete="off"
            :disabled="submitting"
          />
        </div>
      </div>
      <div class="flex flex-col gap-1.5 sm:max-w-xs">
        <Label for="consent-expedition">Ciudad de expedición del documento</Label>
        <Input id="consent-expedition" v-model="expeditionCity" autocomplete="off" :disabled="submitting" />
      </div>
    </div>

    <!-- Declarations some forms print -->
    <div v-if="form.hasSampleConservationChoice || form.hasMicroscopicImagesChoice" class="flex flex-col gap-2">
      <div v-if="form.hasSampleConservationChoice" class="flex items-center gap-2">
        <Checkbox
          id="consent-conserve"
          v-model="conserveSamples"
          :disabled="submitting"
          
        />
        <Label for="consent-conserve">Autorizo la conservación de mis muestras biológicas</Label>
      </div>
      <div v-if="form.hasMicroscopicImagesChoice" class="flex items-center gap-2">
        <Checkbox
          id="consent-images"
          v-model="microscopicImages"
          :disabled="submitting"
          
        />
        <Label for="consent-images">Autorizo el uso de imágenes microscópicas con fines académicos</Label>
      </div>
    </div>

    <!-- The pad -->
    <div class="flex flex-col gap-2" :class="esTablet && 'min-h-[180px] flex-[2]'">
      <div class="flex items-center justify-between">
        <Label :class="esTablet && 'text-lg'">
          Firma {{ representativeSigns ? 'del representante legal' : 'del paciente' }}
        </Label>
        <Button
          variant="ghost"
          :size="esTablet ? 'default' : 'sm'"
          :class="esTablet && 'h-14 px-5 text-base'"
          :disabled="!hasInk || submitting"
          @click="clearPad"
        >
          <Eraser class="mr-1 size-4" aria-hidden="true" />
          Borrar
        </Button>
      </div>
      <SignaturePad
        ref="pad"
        :disabled="submitting"
        :height="esTablet ? 260 : 200"
        @change="onInk"
      />
      <p v-if="form.requiresBacteriologist && bacteriologist" class="text-xs text-muted-foreground">
        Firma también {{ masked(bacteriologist.fullName) }} (bacteriólogo/a), con la firma registrada en su perfil.
      </p>
    </div>

    <p v-if="error" class="flex items-center gap-2 text-sm text-destructive">
      <AlertCircle class="size-4 shrink-0" aria-hidden="true" />
      <span>{{ error }}</span>
    </p>
    <p v-else-if="representativeIncomplete" class="text-xs text-muted-foreground">
      Completa el nombre y el documento del representante para poder firmar.
    </p>

    <footer class="flex flex-wrap items-center justify-end gap-3">
      <Button
        v-if="declinable"
        variant="outline"
        :class="esTablet && 'h-14 px-6 text-lg'"
        :disabled="submitting"
        @click="emit('decline')"
      >
        No firma
      </Button>
      <Button :class="esTablet && 'h-14 px-8 text-lg'" :disabled="!canSign" @click="submit">
        <Loader2 v-if="submitting" class="mr-1 size-4 animate-spin" aria-hidden="true" />
        {{ submitting ? 'Guardando…' : 'Guardar firma' }}
      </Button>
    </footer>
  </section>
</template>
