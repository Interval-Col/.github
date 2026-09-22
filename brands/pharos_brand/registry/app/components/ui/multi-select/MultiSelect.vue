<script setup lang="ts" generic="T = any">
// MultiSelect — the Pháros «pick several» dropdown primitive (RFC 0008 component
// library). A Popover with one Checkbox row per option — the shape lab-qc hand-
// rolled twice (Liberación ▸ Sección, Media móvil) before this existed.
//
// Why it is a primitive and not a snippet: every hand-rolled copy forgot the
// height cap, so on a short screen the list ran past the bottom edge and the
// last options were unreachable (pharos-lis PR 496). Here the list is capped at the
// room reka measures below the trigger and scrolls — the consumer cannot forget.
//
// The trigger keeps a stable height: the chosen names on ONE truncating line,
// the count alongside, the full list in `title` for a hover.
import type { HTMLAttributes } from 'vue'
import { computed } from 'vue'
import { ChevronsUpDown, Loader2 } from 'lucide-vue-next'
import { Button } from '~/components/ui/button'
import { Checkbox } from '~/components/ui/checkbox'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'
import { cn } from '~/lib/utils'

const props = withDefaults(defineProps<{
  /** Selected items, in `items` order. `[]` = nothing selected. */
  modelValue?: T[]
  /** The options. Strings, or objects read through `labelKey` / `valueKey`. */
  items?: T[]
  /** For object items: the property to render as the label. */
  labelKey?: string
  /** For object items: the property that identifies a value (used for equality). */
  valueKey?: string
  placeholder?: string
  emptyText?: string
  /** Shows a select-all row above the options (all ⇄ none; indeterminate when some). */
  selectAll?: boolean
  /** Label of the select-all row — «Todos» for masculine items. */
  selectAllLabel?: string
  loading?: boolean
  disabled?: boolean
  /** `true` or a message → error styling (+ the message if a string). */
  error?: boolean | string
  class?: HTMLAttributes['class']
  /** Extra classes for the floating panel (e.g. a fixed width). */
  contentClass?: HTMLAttributes['class']
}>(), {
  modelValue: () => [],
  items: () => [],
  labelKey: 'label',
  valueKey: 'value',
  placeholder: 'Seleccionar…',
  emptyText: 'No hay opciones disponibles.',
  selectAllLabel: 'Todas',
})

const emit = defineEmits<{ 'update:modelValue': [value: T[]] }>()

const asRecord = (v: unknown): Record<string, unknown> | null =>
  (typeof v === 'object' && v !== null) ? (v as Record<string, unknown>) : null
const labelOf = (item: T): string => {
  const r = asRecord(item)
  return r ? String(r[props.labelKey] ?? '') : String(item)
}
const keyOf = (item: T): string => {
  const r = asRecord(item)
  return r ? String(r[props.valueKey] ?? r[props.labelKey]) : String(item)
}

const selectedKeys = computed(() => new Set(props.modelValue.map(keyOf)))
const isSelected = (item: T) => selectedKeys.value.has(keyOf(item))

// Emit in `items` order, so the value never depends on click order.
function emitKeys(keys: Set<string>) {
  emit('update:modelValue', props.items.filter(i => keys.has(keyOf(i))))
}
function toggle(item: T) {
  const keys = new Set(selectedKeys.value)
  const k = keyOf(item)
  if (keys.has(k)) keys.delete(k)
  else keys.add(k)
  emitKeys(keys)
}

const allSelected = computed(() => props.items.length > 0 && props.items.every(isSelected))
const someSelected = computed(() => !allSelected.value && props.items.some(isSelected))
function toggleAll() {
  emitKeys(allSelected.value ? new Set() : new Set(props.items.map(keyOf)))
}

const selectedLabels = computed(() => props.items.filter(isSelected).map(labelOf))
const triggerLabel = computed(() => selectedLabels.value.join(', '))

const hasError = computed(() => props.error === true || typeof props.error === 'string')
const errorMessage = computed(() => (typeof props.error === 'string' ? props.error : ''))
</script>

<template>
  <div :class="cn('w-full', props.class)">
    <Popover>
      <PopoverTrigger as-child>
        <Button
          type="button"
          variant="outline"
          :disabled="disabled"
          :aria-invalid="hasError || undefined"
          :title="triggerLabel || undefined"
          :class="cn('w-full justify-between gap-2 font-normal', hasError && 'border-destructive')"
        >
          <span v-if="selectedLabels.length" class="flex min-w-0 items-center gap-2">
            <span class="truncate text-left">{{ triggerLabel }}</span>
            <span
              class="inline-flex min-w-5 shrink-0 items-center justify-center rounded-full bg-primary px-1.5 font-data text-xs tabular-nums text-primary-foreground"
            >
              {{ selectedLabels.length }}
            </span>
          </span>
          <span v-else class="truncate text-muted-foreground">{{ placeholder }}</span>
          <ChevronsUpDown class="size-4 shrink-0 text-muted-foreground" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        align="start"
        :collision-padding="8"
        :class="cn(
          'max-h-(--reka-popover-content-available-height) w-(--reka-popover-trigger-width) min-w-56 overflow-y-auto overscroll-contain p-1',
          contentClass,
        )"
      >
        <div v-if="loading" class="flex items-center gap-2 px-2 py-1.5 text-sm text-muted-foreground">
          <Loader2 class="size-4 animate-spin" /> Cargando…
        </div>
        <p v-else-if="!items.length" class="px-2 py-1.5 text-sm text-muted-foreground">
          <slot name="empty">{{ emptyText }}</slot>
        </p>
        <div v-else class="flex flex-col gap-0.5">
          <label v-if="selectAll" :class="cn(rowClass, 'border-b pb-2 mb-1 rounded-none')">
            <Checkbox
              :model-value="allSelected ? true : someSelected ? 'indeterminate' : false"
              @update:model-value="toggleAll"
            />
            <span class="font-medium text-foreground">{{ selectAllLabel }}</span>
          </label>
          <label v-for="item in items" :key="keyOf(item)" :class="rowClass">
            <Checkbox :model-value="isSelected(item)" @update:model-value="() => toggle(item)" />
            <span class="text-foreground">
              <slot name="item" :item="item">{{ labelOf(item) }}</slot>
            </span>
          </label>
        </div>
      </PopoverContent>
    </Popover>

    <p v-if="errorMessage" class="mt-1 text-xs text-destructive">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
const rowClass
  = 'flex cursor-pointer items-center gap-2 rounded-sm px-2 py-1.5 text-sm transition hover:bg-accent hover:text-accent-foreground'
</script>
