<script setup lang="ts" generic="T = any">
// EntityLookup — the Pháros person/entity lookup primitive (RFC 0008 component
// library, Phase 1.2). Composes ScopedSearchInput (the guided filter-chip query
// builder) + a results panel + select, with an explicit idle|searching|found|
// notfound state machine. PatientLookup / PhysicianLookup are thin presets over
// it — so HandlePatient and HandlePhysician converge by construction.
import { computed, ref, type Ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { Loader2, SearchX } from 'lucide-vue-next'
import { ScopedSearchInput } from '@/components/ui/scoped-search'
import { cn } from '@/lib/utils'
import type { QualifierConfig, SearchToken } from '@/components/ui/scoped-search'

const props = withDefaults(defineProps<{
  /** The filter dimensions, forwarded to ScopedSearchInput. */
  qualifiers: QualifierConfig[]
  /** Runs the query for the current tokens and resolves the matching entities. */
  searchFn: (tokens: SearchToken[]) => Promise<T[]>
  labelKey?: string
  sublabelKey?: string
  valueKey?: string
  placeholder?: string
  emptyText?: string
  idleText?: string
  debounceMs?: number
}>(), {
  labelKey: 'label',
  emptyText: 'Sin resultados',
  idleText: 'Agrega un filtro para buscar.',
  debounceMs: 300,
})

const emit = defineEmits<{ select: [entity: T] }>()

type LookupState = 'idle' | 'searching' | 'found' | 'notfound'

const tokens = defineModel<SearchToken[]>('tokens', { default: () => [] })
const results = ref([]) as Ref<T[]>
const state = ref<LookupState>('idle')
const active = ref(-1)

const asRecord = (v: unknown): Record<string, unknown> | null =>
  (typeof v === 'object' && v !== null) ? (v as Record<string, unknown>) : null
const labelOf = (item: T): string => {
  const r = asRecord(item)
  return r ? String(r[props.labelKey] ?? '') : String(item)
}
const sublabelOf = (item: T): string => {
  if (!props.sublabelKey) return ''
  const r = asRecord(item)
  return r ? String(r[props.sublabelKey] ?? '') : ''
}
const keyOf = (item: T, idx: number): string | number => {
  const r = asRecord(item)
  return r && props.valueKey ? String(r[props.valueKey] ?? idx) : idx
}

const runSearch = useDebounceFn(async (current: SearchToken[]) => {
  if (!current.length) {
    state.value = 'idle'
    results.value = []
    return
  }
  state.value = 'searching'
  try {
    const found = await props.searchFn(current)
    results.value = found
    active.value = found.length ? 0 : -1
    state.value = found.length ? 'found' : 'notfound'
  }
  catch {
    results.value = []
    state.value = 'notfound'
  }
}, () => props.debounceMs)

function onSearch(current: SearchToken[]) {
  void runSearch(current)
}

function pick(item: T) {
  emit('select', item)
}

function move(delta: number) {
  if (state.value !== 'found' || !results.value.length) return
  const n = results.value.length
  active.value = (active.value + delta + n) % n
}

function onListKeydown(e: KeyboardEvent) {
  if (e.key === 'ArrowDown') { e.preventDefault(); move(1) }
  else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1) }
  else if (e.key === 'Enter' && active.value >= 0) {
    e.preventDefault()
    pick(results.value[active.value]!)
  }
}

const rowClass = (idx: number) =>
  cn(
    'flex w-full cursor-pointer flex-col items-start gap-0.5 rounded-md px-3 py-2 text-left text-sm outline-hidden',
    idx === active.value ? 'bg-accent text-accent-foreground' : 'hover:bg-accent/60',
  )

defineExpose({ state: computed(() => state.value) })
</script>

<template>
  <div class="flex w-full flex-col gap-2" @keydown="onListKeydown">
    <ScopedSearchInput
      v-model="tokens"
      :qualifiers="qualifiers"
      :placeholder="placeholder"
      @search="onSearch"
    />

    <!-- results panel -->
    <div class="min-h-24 rounded-lg border bg-popover text-popover-foreground shadow-xs">
      <!-- idle -->
      <p v-if="state === 'idle'" class="flex items-center justify-center gap-2 px-3 py-8 text-center text-sm text-muted-foreground">
        {{ idleText }}
      </p>

      <!-- searching -->
      <p v-else-if="state === 'searching'" class="flex items-center justify-center gap-2 px-3 py-8 text-sm text-muted-foreground">
        <Loader2 class="size-4 animate-spin" /> Buscando…
      </p>

      <!-- notfound -->
      <p v-else-if="state === 'notfound'" class="flex flex-col items-center justify-center gap-1 px-3 py-8 text-center text-sm text-muted-foreground">
        <SearchX class="size-5 opacity-60" />
        {{ emptyText }}
      </p>

      <!-- found -->
      <ul v-else class="max-h-72 overflow-y-auto p-1">
        <li v-for="(item, i) in results" :key="keyOf(item, i)">
          <button
            type="button"
            :class="rowClass(i)"
            @mouseenter="active = i"
            @click="pick(item)"
          >
            <slot name="result" :item="item">
              <span class="font-medium">{{ labelOf(item) }}</span>
              <span v-if="sublabelOf(item)" class="text-xs text-muted-foreground">{{ sublabelOf(item) }}</span>
            </slot>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>
