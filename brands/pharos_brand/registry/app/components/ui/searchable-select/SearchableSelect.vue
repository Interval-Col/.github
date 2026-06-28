<script setup lang="ts" generic="T = any">
// SearchableSelect — the Pháros type-to-filter dropdown primitive (RFC 0008
// component library). Built on reka-ui's Combobox primitives. Two modes:
//   • static  — pass `items`; reka-ui filters them as you type.
//   • async   — pass `searchFn`; results are fetched (debounced) and reka-ui's
//               own filter is disabled (`ignoreFilter`).
// Empty / null `modelValue` is a first-class "nothing selected" state — there is
// NO empty-string sentinel (the finance-lch NONE_* pain this primitive removes).
import type { AcceptableValue } from 'reka-ui'
import type { HTMLAttributes } from 'vue'
import { computed, ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { Check, ChevronsUpDown, Loader2, Search } from 'lucide-vue-next'
import {
  ComboboxAnchor,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxGroup,
  ComboboxInput,
  ComboboxItem,
  ComboboxItemIndicator,
  ComboboxLabel,
  ComboboxPortal,
  ComboboxRoot,
  ComboboxTrigger,
  ComboboxViewport,
} from 'reka-ui'
import { cn } from '@/lib/utils'

const props = withDefaults(defineProps<{
  /** Selected value (the item itself). `null` = nothing selected. */
  modelValue?: T | null
  /** Static options — reka-ui filters these client-side as you type. */
  items?: T[]
  /** Async/remote search. When set, results come from here (debounced) and the built-in filter is off. */
  searchFn?: (query: string) => Promise<T[]>
  /** For object items: the property to render as the label. */
  labelKey?: string
  /** For object items: the property that identifies a value (used for equality). */
  valueKey?: string
  /** Group items under headings. */
  groupBy?: (item: T) => string
  placeholder?: string
  searchPlaceholder?: string
  emptyText?: string
  disabled?: boolean
  required?: boolean
  /** `true` or a message → error styling (+ the message if a string). */
  error?: boolean | string
  /** reka-ui equality key for object values. Defaults to `valueKey` for object items. */
  by?: string
  debounceMs?: number
  class?: HTMLAttributes['class']
}>(), {
  modelValue: null,
  items: () => [],
  labelKey: 'label',
  valueKey: 'value',
  placeholder: 'Seleccionar…',
  emptyText: 'Sin resultados',
  debounceMs: 300,
})

const emit = defineEmits<{ 'update:modelValue': [value: T | null] }>()

const isAsync = computed(() => typeof props.searchFn === 'function')
const asyncItems = ref<T[]>([]) as { value: T[] }
const loading = ref(false)
const open = ref(false)

const sourceItems = computed<T[]>(() => (isAsync.value ? asyncItems.value : props.items))

const asRecord = (v: unknown): Record<string, unknown> | null =>
  (typeof v === 'object' && v !== null) ? (v as Record<string, unknown>) : null
const labelOf = (item: T | null | undefined): string => {
  if (item == null) return ''
  const r = asRecord(item)
  return r ? String(r[props.labelKey] ?? '') : String(item)
}
const keyOf = (item: T, idx: number): string | number => {
  const r = asRecord(item)
  return r ? String(r[props.valueKey] ?? r[props.labelKey] ?? idx) : String(item)
}

// Default equality: by `valueKey` when items are objects, else reference/value equality.
const equality = computed(() => props.by ?? (asRecord(sourceItems.value[0]) ? props.valueKey : undefined))

// Grouped view (order-preserving). Null when no groupBy.
const groups = computed(() => {
  if (!props.groupBy) return null
  const out: { heading: string, items: T[] }[] = []
  const index = new Map<string, number>()
  for (const item of sourceItems.value) {
    const heading = props.groupBy(item)
    let at = index.get(heading)
    if (at === undefined) { at = out.length; index.set(heading, at); out.push({ heading, items: [] }) }
    out[at]!.items.push(item)
  }
  return out
})

const runSearch = useDebounceFn(async (query: string) => {
  if (!props.searchFn) return
  loading.value = true
  try {
    asyncItems.value = await props.searchFn(query)
  }
  finally {
    loading.value = false
  }
}, () => props.debounceMs)

function onQuery(query: string) {
  if (isAsync.value) void runSearch(query)
}

const hasError = computed(() => props.error === true || typeof props.error === 'string')
const errorMessage = computed(() => (typeof props.error === 'string' ? props.error : ''))

const model = computed<AcceptableValue>({
  get: () => (props.modelValue ?? null) as AcceptableValue,
  set: v => emit('update:modelValue', (v ?? null) as T | null),
})
</script>

<template>
  <div :class="cn('w-full', props.class)">
    <ComboboxRoot
      v-model="model"
      v-model:open="open"
      :by="equality"
      :ignore-filter="isAsync"
      :disabled="disabled"
      reset-search-term-on-blur
      class="relative w-full"
    >
      <ComboboxAnchor
        :class="cn(
          'flex h-9 w-full items-center gap-2 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-colors',
          'focus-within:ring-1 focus-within:ring-ring focus-within:border-ring',
          hasError && 'border-destructive focus-within:ring-destructive',
          disabled && 'cursor-not-allowed opacity-50',
        )"
      >
        <Search class="size-4 shrink-0 opacity-50" />
        <ComboboxInput
          :display-value="(v) => labelOf(v as T)"
          :placeholder="searchPlaceholder ?? placeholder"
          :aria-required="required || undefined"
          :aria-invalid="hasError || undefined"
          autocomplete="off"
          class="flex-1 bg-transparent outline-hidden placeholder:text-muted-foreground disabled:cursor-not-allowed"
          @update:model-value="onQuery"
        />
        <Loader2 v-if="loading" class="size-4 shrink-0 animate-spin opacity-50" />
        <ComboboxTrigger class="shrink-0 opacity-50 hover:opacity-100">
          <ChevronsUpDown class="size-4" />
        </ComboboxTrigger>
      </ComboboxAnchor>

      <ComboboxPortal>
        <ComboboxContent
          position="popper"
          :side-offset="4"
          :class="cn(
            'group/combobox-content z-50 max-h-72 w-[var(--reka-combobox-trigger-width)] min-w-36 overflow-hidden rounded-lg border bg-popover text-popover-foreground shadow-md',
            'data-open:animate-in data-closed:animate-out data-closed:fade-out-0 data-open:fade-in-0',
          )"
        >
          <ComboboxViewport class="max-h-72 overflow-y-auto p-1 scroll-py-1">
            <!-- loading (async) -->
            <div v-if="loading" class="flex items-center justify-center gap-2 py-3 text-sm text-muted-foreground">
              <Loader2 class="size-4 animate-spin" /> Buscando…
            </div>

            <!-- empty -->
            <ComboboxEmpty
              v-if="!loading"
              class="hidden w-full justify-center py-3 text-center text-sm text-muted-foreground group-data-empty/combobox-content:flex"
            >
              <slot name="empty">{{ emptyText }}</slot>
            </ComboboxEmpty>

            <!-- grouped -->
            <template v-if="groups">
              <ComboboxGroup v-for="g in groups" :key="g.heading" class="overflow-hidden text-foreground">
                <ComboboxLabel class="px-2 py-1.5 text-xs text-muted-foreground">{{ g.heading }}</ComboboxLabel>
                <ComboboxItem
                  v-for="(item, i) in g.items"
                  :key="keyOf(item, i)"
                  :value="item as AcceptableValue"
                  :text-value="labelOf(item)"
                  :class="itemClass"
                >
                  <slot name="item" :item="item">{{ labelOf(item) }}</slot>
                  <ComboboxItemIndicator class="pointer-events-none absolute right-2 flex size-4 items-center justify-center">
                    <Check class="size-4" />
                  </ComboboxItemIndicator>
                </ComboboxItem>
              </ComboboxGroup>
            </template>

            <!-- flat -->
            <template v-else>
              <ComboboxItem
                v-for="(item, i) in sourceItems"
                :key="keyOf(item, i)"
                :value="item as AcceptableValue"
                :text-value="labelOf(item)"
                :class="itemClass"
              >
                <slot name="item" :item="item">{{ labelOf(item) }}</slot>
                <ComboboxItemIndicator class="pointer-events-none absolute right-2 flex size-4 items-center justify-center">
                  <Check class="size-4" />
                </ComboboxItemIndicator>
              </ComboboxItem>
            </template>
          </ComboboxViewport>
        </ComboboxContent>
      </ComboboxPortal>
    </ComboboxRoot>

    <p v-if="errorMessage" class="mt-1 text-xs text-destructive">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
// item row classes, shared by the grouped + flat branches
const itemClass
  = 'relative flex w-full cursor-default select-none items-center gap-2 rounded-md py-1.5 pr-8 pl-2 text-sm outline-hidden data-highlighted:bg-accent data-highlighted:text-accent-foreground data-disabled:pointer-events-none data-disabled:opacity-50'
</script>
