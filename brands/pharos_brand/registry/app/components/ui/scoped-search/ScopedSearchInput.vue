<script setup lang="ts">
// ScopedSearchInput — the Pháros guided filter-chip query builder (RFC 0008
// component library, Phase 1.2). GitHub's scoped-search concept, adapted for
// clinical reception staff: instead of a hidden text DSL (`cc:123 nombre:x`),
// the operator ADDS filters from a picker; each becomes a removable pill, and a
// Cédula pill carries its document type (CC/TI/…) so identity is never ambiguous.
// v-model is the structured token array; `search` fires on Enter / commit.
import { computed, nextTick, ref } from 'vue'
import { Plus, X } from 'lucide-vue-next'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import type { QualifierConfig, SearchToken } from './types'

const props = withDefaults(defineProps<{
  /** The filter dimensions the operator can add. */
  qualifiers: QualifierConfig[]
  placeholder?: string
  disabled?: boolean
}>(), {
  placeholder: 'Agregar filtro o buscar…',
})

const emit = defineEmits<{ search: [tokens: SearchToken[]] }>()

/** Committed pills. */
const tokens = defineModel<SearchToken[]>({ default: () => [] })

const inputText = ref('')
const pickerOpen = ref(false)
const activeQualifier = ref<QualifierConfig | null>(null)
const docType = ref<string | null>(null)
const inputEl = ref<HTMLInputElement | null>(null)

// A document qualifier is chosen but its type isn't picked yet → the value
// input stays locked until a type is selected (identity-safety).
const needsDocType = computed(() => activeQualifier.value?.kind === 'document' && !docType.value)

const inputPlaceholder = computed(() => {
  if (activeQualifier.value) {
    if (needsDocType.value) return 'Elige el tipo de documento…'
    return activeQualifier.value.placeholder ?? `${activeQualifier.value.label}…`
  }
  return props.placeholder
})

// Free text with no chosen qualifier commits as this (sensible default = Nombre).
const defaultQualifier = computed(() =>
  props.qualifiers.find(q => q.key === 'nombre')
  ?? props.qualifiers.find(q => q.kind === 'text')
  ?? null)

function focusInput() {
  nextTick(() => inputEl.value?.focus())
}

function openPicker() {
  if (props.disabled) return
  pickerOpen.value = true
}

function chooseQualifier(q: QualifierConfig) {
  activeQualifier.value = q
  docType.value = null
  inputText.value = ''
  pickerOpen.value = false
  focusInput()
}

function chooseDocType(dt: string) {
  docType.value = dt
  focusInput()
}

function pillLabel(t: SearchToken) {
  return t.docType ? `${t.label} ${t.docType}: ${t.value}` : `${t.label}: ${t.value}`
}

function resetDraft() {
  activeQualifier.value = null
  docType.value = null
  inputText.value = ''
}

function commit() {
  const text = inputText.value.trim()
  if (!text) {
    // Nothing to add → Enter just (re)runs the search with the current chips.
    emit('search', tokens.value)
    return
  }
  if (activeQualifier.value) {
    if (needsDocType.value) return // must pick a document type first
    const token: SearchToken = {
      qualifier: activeQualifier.value.key,
      label: activeQualifier.value.label,
      value: text,
    }
    if (docType.value) token.docType = docType.value
    tokens.value = [...tokens.value, token]
  }
  else {
    const def = defaultQualifier.value
    if (!def) return
    tokens.value = [...tokens.value, { qualifier: def.key, label: def.label, value: text }]
  }
  resetDraft()
  pickerOpen.value = false
  emit('search', tokens.value)
}

function removeToken(i: number) {
  tokens.value = tokens.value.filter((_, idx) => idx !== i)
  emit('search', tokens.value)
}

function onBackspace() {
  if (inputText.value) return
  if (activeQualifier.value) { resetDraft(); return }
  if (tokens.value.length) removeToken(tokens.value.length - 1)
}

function focusFirstQualifier() {
  // PopoverContent is teleported; only one picker is mounted at a time, so a
  // document query reliably finds the open list.
  nextTick(() => document.querySelector<HTMLButtonElement>('[data-qualifier]')?.focus())
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') {
    e.preventDefault()
    commit()
  }
  else if (e.key === 'Backspace') {
    onBackspace()
  }
  else if (e.key === 'Escape') {
    if (pickerOpen.value) pickerOpen.value = false
    else if (activeQualifier.value) resetDraft()
  }
  else if (e.key === 'ArrowDown' && !activeQualifier.value) {
    // open + dive into the picker for keyboard-only operators
    e.preventDefault()
    openPicker()
    focusFirstQualifier()
  }
}
</script>

<template>
  <div
    :class="cn(
      'flex min-h-9 w-full flex-wrap items-center gap-1.5 rounded-md border border-input bg-transparent px-2 py-1 text-sm shadow-xs transition-colors',
      'focus-within:border-ring focus-within:ring-1 focus-within:ring-ring',
      disabled && 'cursor-not-allowed opacity-50',
    )"
    @click="focusInput"
  >
    <!-- committed pills -->
    <span
      v-for="(t, i) in tokens"
      :key="`${t.qualifier}-${i}`"
      class="inline-flex items-center gap-1 rounded bg-accent px-1.5 py-0.5 text-xs font-medium text-accent-foreground"
    >
      {{ pillLabel(t) }}
      <button
        type="button"
        class="opacity-60 hover:opacity-100"
        :disabled="disabled"
        :aria-label="`Quitar filtro ${t.label}`"
        @click.stop="removeToken(i)"
      >
        <X class="size-3" />
      </button>
    </span>

    <!-- draft in progress: the qualifier prefix + (for documents) the type chooser -->
    <template v-if="activeQualifier">
      <span class="inline-flex items-center gap-1 rounded bg-muted px-1.5 py-0.5 text-xs font-medium text-muted-foreground">
        {{ activeQualifier.label }}<template v-if="docType">&nbsp;{{ docType }}</template>:
      </span>
      <template v-if="needsDocType">
        <button
          v-for="dt in activeQualifier.docTypes"
          :key="dt.value"
          type="button"
          class="rounded border border-border px-1.5 py-0.5 text-xs hover:bg-accent hover:text-accent-foreground"
          :title="dt.label"
          @click.stop="chooseDocType(dt.value)"
        >
          {{ dt.value }}
        </button>
      </template>
    </template>

    <!-- qualifier picker -->
    <Popover v-model:open="pickerOpen">
      <PopoverTrigger as-child>
        <button
          type="button"
          class="inline-flex size-5 shrink-0 items-center justify-center rounded text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          :disabled="disabled"
          aria-label="Agregar filtro"
          @click.stop="openPicker"
        >
          <Plus class="size-3.5" />
        </button>
      </PopoverTrigger>
      <PopoverContent align="start" class="w-52 p-1" @open-auto-focus.prevent>
        <p class="px-2 py-1 text-xs text-muted-foreground">Filtrar por…</p>
        <button
          v-for="q in qualifiers"
          :key="q.key"
          type="button"
          data-qualifier
          class="flex w-full items-center rounded px-2 py-1.5 text-left text-sm outline-hidden hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground"
          @click="chooseQualifier(q)"
        >
          {{ q.label }}
          <span v-if="q.kind === 'document'" class="ml-auto text-xs text-muted-foreground">elige tipo</span>
        </button>
      </PopoverContent>
    </Popover>

    <!-- value / free-text input -->
    <input
      ref="inputEl"
      v-model="inputText"
      :placeholder="inputPlaceholder"
      :disabled="disabled || needsDocType"
      :aria-label="inputPlaceholder"
      autocomplete="off"
      class="min-w-32 flex-1 bg-transparent outline-hidden placeholder:text-muted-foreground disabled:cursor-not-allowed"
      @keydown="onKeydown"
    >
  </div>
</template>
