// useFlow — the Pháros multi-step flow + back-stack composable (RFC 0008
// component library, Phase 2). Generalises admission-patient's `useProcessState`
// wizard: steps are CONFIG (not hardcoded Paciente/Orden), it's a per-call
// COMPOSABLE instance (not a global Pinia singleton, so multiple flows coexist),
// and `goBack()` pops a REAL back-stack (`history`) — the fix for "I go forward
// but there's no natural way back". Optional SSR-safe localStorage persistence
// restores the step after a mid-flow reload.
//
//   const flow = useFlow({
//     steps: [
//       { key: 'paciente', label: 'Paciente', icon: 'user' },
//       { key: 'orden',    label: 'Orden',    icon: 'clipboardList' },
//       { key: 'confirm',  label: 'Confirmación', icon: 'check' },
//     ],
//     persistKey: 'flow:recepcion',
//   })
//   flow.goNext() · flow.goBack() · flow.goTo('orden') · flow.cancel()
import { computed, reactive, ref } from 'vue'

export type FlowStepStatus = 'pending' | 'active' | 'done' | 'error' | 'skipped'

export interface FlowStep {
  /** Stable id used by goTo/persistence. */
  key: string
  /** Human label (Spanish, operator-facing). */
  label: string
  /** Optional <Icon> registry key. */
  icon?: string
  /** Initial status; defaults to 'pending' (the entry step becomes 'active'). */
  status?: FlowStepStatus
}

export interface UseFlowOptions {
  steps: FlowStep[]
  /** Entry step key; defaults to the first step. */
  initial?: string
  /** localStorage key. Omit → no persistence (purely in-memory). */
  persistKey?: string
}

/** The persisted shape (documented so a migration can map old keys → new). */
interface FlowPersistState {
  current: string
  statuses: Record<string, FlowStepStatus>
}

export interface ResolvedFlowStep extends FlowStep {
  status: FlowStepStatus
}

export function useFlow(options: UseFlowOptions) {
  const steps = reactive(
    options.steps.map((s): ResolvedFlowStep => ({ ...s, status: s.status ?? 'pending' })),
  ) as ResolvedFlowStep[]
  const keys = steps.map(s => s.key)

  const initialKey = options.initial && keys.includes(options.initial) ? options.initial : keys[0]!
  const currentKey = ref(initialKey)
  /** The back-stack: keys visited before the current one, most-recent last. */
  const history = ref<string[]>([])

  const canPersist = () => !!options.persistKey && typeof window !== 'undefined'

  // SSR note: design-studio is ssr:false (SPA), so a synchronous guarded load is
  // safe. In an SSR app this should move to onMounted to avoid a hydration
  // mismatch (server renders the initial step, client would load a later one).
  function loadPersisted() {
    if (!canPersist()) return
    try {
      const raw = window.localStorage.getItem(options.persistKey!)
      if (!raw) return
      const data = JSON.parse(raw) as Partial<FlowPersistState>
      if (data.current && keys.includes(data.current)) currentKey.value = data.current
      if (data.statuses) {
        for (const s of steps) {
          const st = data.statuses[s.key]
          if (st) s.status = st
        }
      }
    }
    catch {
      // corrupt payload → ignore, start clean
    }
  }

  function persist() {
    if (!canPersist()) return
    const data: FlowPersistState = {
      current: currentKey.value,
      statuses: Object.fromEntries(steps.map(s => [s.key, s.status])),
    }
    try {
      window.localStorage.setItem(options.persistKey!, JSON.stringify(data))
    }
    catch {
      // quota / private-mode → persistence is best-effort
    }
  }

  const currentIndex = computed(() => keys.indexOf(currentKey.value))
  const currentStep = computed<ResolvedFlowStep | undefined>(() => steps[currentIndex.value])
  const canGoBack = computed(() => history.value.length > 0)
  const canGoNext = computed(() => currentIndex.value < steps.length - 1)

  function findStep(key: string) {
    return steps.find(s => s.key === key)
  }

  function setStepStatus(key: string, status: FlowStepStatus) {
    const s = findStep(key)
    if (s) {
      s.status = status
      persist()
    }
  }

  /** Jump to a step, recording the current one on the back-stack (unless record:false). */
  function goTo(key: string, opts: { record?: boolean } = {}) {
    if (!keys.includes(key) || key === currentKey.value) return
    if (opts.record !== false) history.value.push(currentKey.value)
    currentKey.value = key
    const s = findStep(key)
    if (s && s.status === 'pending') s.status = 'active'
    persist()
  }

  function goNext() {
    if (!canGoNext.value) return
    setStepStatus(currentKey.value, 'done')
    goTo(keys[currentIndex.value + 1]!)
  }

  /** Pop the back-stack → real back-navigation (not just index-1). */
  function goBack() {
    if (!canGoBack.value) return
    const prev = history.value.pop()!
    currentKey.value = prev
    const s = findStep(prev)
    if (s) s.status = 'active'
    persist()
  }

  function reset() {
    for (const s of steps) s.status = 'pending'
    history.value = []
    currentKey.value = initialKey
    const first = findStep(initialKey)
    if (first) first.status = 'active'
    persist()
  }

  /** reset() + drop the persisted payload (use when leaving the flow entirely). */
  function cancel() {
    reset()
    if (canPersist()) {
      try {
        window.localStorage.removeItem(options.persistKey!)
      }
      catch { /* best-effort */ }
    }
  }

  // init: restore persisted state, then ensure the current step reads as active.
  loadPersisted()
  const cur = findStep(currentKey.value)
  if (cur && cur.status === 'pending') cur.status = 'active'

  return {
    steps,
    currentKey,
    currentStep,
    currentIndex,
    history,
    canGoBack,
    canGoNext,
    goNext,
    goBack,
    goTo,
    reset,
    cancel,
    setStepStatus,
  }
}

export type UseFlowReturn = ReturnType<typeof useFlow>
