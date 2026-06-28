<script setup lang="ts">
// FormField — the Pháros field wrapper (RFC 0008 component library, Phase 3).
// Label + control + inline error/hint, with the a11y wiring (aria-invalid,
// aria-describedby) done once. VALIDATION-AGNOSTIC: it does not import
// vee-validate or any validator — you pass `error` in. The standard pairing is
// vee-validate + @vee-validate/zod (what admission-patient uses), but keeping
// the field agnostic means any validator (or none) can drive it. Whether the
// registry also ships a vee-validate-BOUND wrapper on top is a session decision.
//
//   <FormField label="Cédula" :error="errors.cedula" required v-slot="f">
//     <Input :id="f.id" v-bind="f.aria" v-model="cedula" />
//   </FormField>
import type { HTMLAttributes } from 'vue'
import { computed, useId } from 'vue'
import { cn } from '@/lib/utils'
import { Label } from '@/components/ui/label'

const props = defineProps<{
  label?: string
  /** Override the generated control id (else an auto id is provided to the slot). */
  for?: string
  error?: string | string[]
  hint?: string
  required?: boolean
  class?: HTMLAttributes['class']
}>()

const autoId = useId()
const fieldId = computed(() => props.for ?? `ff-${autoId}`)
const errors = computed(() =>
  Array.isArray(props.error) ? props.error.filter(Boolean) : props.error ? [props.error] : [],
)
const hasError = computed(() => errors.value.length > 0)
const describedBy = computed(() =>
  hasError.value ? `${fieldId.value}-error` : props.hint ? `${fieldId.value}-hint` : undefined,
)
// convenience object to v-bind onto the control inside the slot
const aria = computed(() => ({
  'aria-invalid': hasError.value || undefined,
  'aria-describedby': describedBy.value,
}))
</script>

<template>
  <div :class="cn('flex flex-col gap-1.5', props.class)">
    <Label v-if="label || $slots.label" :for="fieldId" :class="hasError && 'text-destructive'">
      <slot name="label">{{ label }}</slot>
      <span v-if="required" class="text-destructive" aria-hidden="true">&nbsp;*</span>
    </Label>

    <!-- the control: bind :id and v-bind="f.aria" for correct a11y -->
    <slot :id="fieldId" :aria="aria" :has-error="hasError" />

    <p v-if="hasError" :id="`${fieldId}-error`" role="alert" class="text-xs text-destructive">
      <slot name="error">{{ errors.join(' · ') }}</slot>
    </p>
    <p v-else-if="hint" :id="`${fieldId}-hint`" class="text-xs text-muted-foreground">
      {{ hint }}
    </p>
  </div>
</template>
