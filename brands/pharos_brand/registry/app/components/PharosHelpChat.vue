<script setup lang="ts">
// PharosHelpChat — the shared Pháros in-app AI assistant widget (RFC 0017 Phase 4).
// Lifted from finance-lch's HelpChat.vue into the registry so every app's chat FE
// is ONE definition (copy-in, keep-at-par) — the backend converges via the
// chat-contract (Interval-Col/.github/chat-contract.md); this is its FE half.
//
// Everything app-specific is a prop: the transport (`send` — the app owns Bearer /
// 401→SSO bounce, exactly like createPharosAdminApi), the brand name, the starter
// prompts, the sessionStorage key. Colors are the registry token contract
// (tokens.css) only — no hex, no legacy --text-*/--bg-* vars — so it renders
// coherently under any sub-brand `.theme-*`. Deps: marked + DOMPurify (add per
// chat-widget.md). Docs: registry/chat-widget.md.
//
// PRESENTATION (RFC 0017, decided 2026-07-13 — registry/spec/chat.md): the launcher can be a
// floating bubble OR an in-flow topbar button, and the panel a corner card OR a full-height side
// sheet. The topbar variant does NOT need a slot or `defineExpose`: the app mounts this component
// INSIDE its topbar, and the root goes in-flow (`display: contents`) so the button sits among the
// topbar actions — while `floating` breaks out with `position: fixed`. Mount location is therefore
// load-bearing; see registry/chat-widget.md.
//
// EVERY presentation prop defaults to the pre-2026-07-13 behaviour (floating · corner · no persona),
// so an app that re-syncs without changing its mount keeps rendering exactly what it rendered before.
import { ref, computed, nextTick, onMounted, onBeforeUnmount, watch } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import PharosChatAvatar from './PharosChatAvatar.vue'

/** One turn in the conversation. `sources` is set on assistant turns grounded on
 *  a corpus (chat-contract CH5); absent/empty for non-RAG chats. */
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

/** The chat endpoint's reply shape (chat-contract wire format). */
export interface ChatReply {
  reply: string
  sources?: string[]
  blocked?: boolean
  reason?: string
}

/** The health endpoint's reply shape (chat-contract CH8 — `GET {base}/v1/chat/health`).
 *  Three independent reasons the assistant may be unusable, kept separate so the widget
 *  can name the RIGHT one instead of collapsing them into "no disponible". */
export interface ChatHealth {
  /** Chat is switched on in this deployment (CHAT_ENABLED / kill switch). */
  enabled: boolean
  /** THIS caller holds the capability the chat route requires (e.g. `chat.access`). */
  allowed: boolean
  /** The shared proxy answered `/readyz`. */
  upstream: boolean
}

const props = withDefaults(defineProps<{
  /** App-owned transport to the chat endpoint (Bearer / 401 bounce stay app-side). */
  send: (payload: { message: string; history: ChatMessage[] }) => Promise<ChatReply>
  /** Brand name shown in the unnamed greeting ("la asistente de {brandName}"). */
  brandName?: string
  /** Panel title + dialog aria-label. */
  title?: string
  /** Suggested opening questions (empty = no starter chips). */
  starters?: string[]
  /** sessionStorage key — MUST be unique per app so histories never collide. */
  storageKey?: string
  /** Textarea placeholder. */
  placeholder?: string

  // ── Presentation (registry/spec/chat.md) — all default to the pre-existing behaviour ──
  /** Launcher: floating bubble (fixed, bottom-right) or an in-flow button for the app's topbar.
   *  `topbar` REQUIRES mounting this component inside the topbar — see chat-widget.md. */
  trigger?: 'floating' | 'topbar'
  /** Panel shape: corner card (bottom-right) or a full-height side drawer with backdrop. */
  form?: 'corner' | 'sheet'
  /** The assistant's proper name (e.g. "Nerea"). Empty = unnamed; the panel falls back to `title`. */
  assistantName?: string
  /** Avatar mark — see PharosChatAvatar. Empty = the plain speech-bubble mark. */
  avatar?: string
  /** Avatar treatment: on a round chip, or the bare glyph. */
  avatarBg?: 'circulo' | 'solo'
  /** Show the presence dot + status line under the name.
   *
   *  The state is REAL, never a decorative "always green" (it used to be exactly that, and it
   *  lied: a user without the chat capability saw «En línea», asked a question, and ate a 403).
   *  It comes from two sources, freshest-wins: the `probe` below, and what actually happened on
   *  the wire on the last send. */
  statusLine?: boolean
  /** App-owned health probe (chat-contract CH8), same shape of ownership as `send`: the app owns
   *  Bearer / 401 bounce, the widget owns what the answer MEANS.
   *
   *  Optional only so the registry widget can land ahead of the per-app routes — with no probe the
   *  status falls back to traffic-derived, which cannot know anything until the first message is
   *  sent. That fallback is a migration window, not a resting place: ship the route. */
  probe?: () => Promise<ChatHealth>
  /** Render corpus citations on grounded replies (chat-contract CH5). */
  citations?: boolean
}>(), {
  brandName: 'Pháros',
  title: 'Asistente de ayuda',
  starters: () => [],
  storageKey: 'pharos-help-chat-history',
  placeholder: 'Escriba su pregunta…',
  trigger: 'floating',
  form: 'corner',
  assistantName: '',
  avatar: '',
  avatarBg: 'circulo',
  statusLine: false,
  probe: undefined,
  citations: true,
})

// A TS literal union is erased at runtime — Vue does not validate it — so an app passing a typo
// ("topBar") would render NO launcher at all, or a panel with no size. Normalise instead of trusting
// the type: anything unrecognised degrades to the known-good default.
const triggerMode = computed(() => props.trigger === 'topbar' ? 'topbar' : 'floating')
const formMode = computed(() => props.form === 'sheet' ? 'sheet' : 'corner')

/** The SHEET is a modal drawer (it dims the app behind it) — the corner card is a non-modal
 *  popover. Focus trap, scroll lock and aria-modal apply to the former ONLY: trapping focus in a
 *  little corner popover would be hostile, not helpful. */
const isModal = computed(() => formMode.value === 'sheet')

/** Panel heading: the assistant's name when it has one, else the generic title. */
const heading = computed(() => props.assistantName || props.title)
/** Greeting: the canonical micro-copy (NEREA.md §7) when named, else the brand fallback. */
const greeting = computed(() => props.assistantName
  ? `Hola, soy ${props.assistantName}. ¿En qué te ayudo?`
  : `Hola, soy la asistente de ${props.brandName}. ¿En qué te ayudo?`)

const isOpen = ref(false)
const input = ref('')
const messages = ref<ChatMessage[]>([])
const loading = ref(false)
const errorText = ref('')
const scrollEl = ref<HTMLElement | null>(null)
const inputEl = ref<HTMLTextAreaElement | null>(null)

// ── Estado de conexión REAL ───────────────────────────────────────────────────
// Cuatro maneras distintas de no servir, y cada una merece su propia palabra: el
// despliegue la tiene apagada, este usuario no tiene la capacidad, el proxy no
// responde, o el usuario agotó su cuota. Decir «no disponible» a las cuatro manda
// a recepción a abrir un ticket cuando lo que faltaba era un permiso.
type ChatStatus = 'desconocido' | 'en-linea' | 'sin-permiso' | 'limitado' | 'no-disponible'

const status = ref<ChatStatus>('desconocido')

const STATUS_TEXT: Record<ChatStatus, string> = {
  'desconocido': 'sin verificar',
  'en-linea': 'en línea',
  'sin-permiso': 'sin permiso',
  'limitado': 'límite alcanzado',
  'no-disponible': 'no disponible',
}
const statusText = computed(() => STATUS_TEXT[status.value])

// El estado NUNCA se comunica solo por color (dos de estos rojos/ámbar se confunden
// entre sí y con el verde para un ojo daltónico, y el punto mide 10px): cada estado
// lleva palabra propia + glifo propio + relleno propio del punto.
const statusGlyph = computed(() => {
  switch (status.value) {
    case 'en-linea': return 'check'
    case 'sin-permiso': return 'lock'
    case 'limitado': return 'hourglass'
    case 'no-disponible': return 'cross'
    default: return 'question'
  }
})

// Una sonda recién corrida no se repite en cada apertura del panel; el tráfico real
// la refresca de todos modos.
const PROBE_TTL_MS = 60_000
let lastProbeAt = 0

async function runProbe(force = false) {
  if (!props.probe || !props.statusLine) return
  const now = Date.now()
  if (!force && lastProbeAt && now - lastProbeAt < PROBE_TTL_MS) return
  try {
    const h = await props.probe()
    lastProbeAt = Date.now()
    // Orden deliberado: lo que el usuario puede ARREGLAR va primero. Si le falta el
    // permiso, eso es lo accionable aunque además el proxy esté caído.
    status.value = h?.allowed === false ? 'sin-permiso'
      : (h?.enabled === false || h?.upstream === false) ? 'no-disponible'
      : 'en-linea'
  } catch {
    // Una sonda que falla es señal en sí misma, pero no debe TAPAR un estado más
    // específico que ya aprendimos del tráfico real (un 403 dice más que «no llegué»).
    if (status.value === 'desconocido' || status.value === 'en-linea') {
      status.value = 'no-disponible'
    }
  }
}

onMounted(() => {
  try {
    const raw = sessionStorage.getItem(props.storageKey)
    if (raw) {
      const parsed = JSON.parse(raw) as unknown
      if (Array.isArray(parsed)) {
        // Drop entries with missing/invalid content — they crash marked.parse on
        // render. Belt-and-suspenders for sessions saved before this guard.
        messages.value = parsed.filter(
          (m): m is ChatMessage =>
            m && typeof m === 'object'
            && (m as ChatMessage).role !== undefined
            && typeof (m as ChatMessage).content === 'string',
        )
      }
    }
  } catch {
    // sessionStorage may be unavailable (private mode); not fatal
  }
  // El punto de presencia se ve ANTES de abrir el panel (variante `topbar`), así que
  // la sonda corre al montar o el punto mentiría hasta el primer clic.
  void runProbe()
})

watch(messages, val => {
  try {
    sessionStorage.setItem(props.storageKey, JSON.stringify(val))
  } catch {
    // ignore
  }
}, { deep: true })

function open() {
  isOpen.value = true
  // Re-sondea al abrir si el último resultado ya está viejo: el panel se abre justo
  // cuando la respuesta importa.
  void runProbe()
  nextTick(() => {
    inputEl.value?.focus()
    scrollToBottom()
  })
}

function close() {
  isOpen.value = false
  // Return focus to the launcher. Without this the panel unmounts while holding focus and the
  // browser drops it to <body> — a keyboard user loses their place and has to Tab from the top.
  nextTick(() => launcherEl.value?.focus())
}

// ── Modal behaviour (sheet only) ──────────────────────────────────────────────
// The sheet covers the app behind a backdrop, so it owes the user what any modal owes them: Escape
// to dismiss, focus that cannot wander out behind the backdrop, and a page that does not scroll
// underneath. The corner card is a popover and gets only Escape.
const panelEl = ref<HTMLElement | null>(null)
const launcherEl = ref<HTMLElement | null>(null)

const FOCUSABLE = 'button:not([disabled]), textarea:not([disabled]), input:not([disabled]), a[href], select:not([disabled]), [tabindex]:not([tabindex="-1"])'
function focusables(): HTMLElement[] {
  if (!panelEl.value) return []
  return Array.from(panelEl.value.querySelectorAll<HTMLElement>(FOCUSABLE))
    .filter(el => el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement)
}

function onPanelKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    e.stopPropagation()
    close()
    return
  }
  if (e.key !== 'Tab' || !isModal.value) return

  const els = focusables()
  if (!els.length) return
  const first = els[0]!
  const last = els[els.length - 1]!
  const active = document.activeElement as HTMLElement | null

  // Wrap at both ends, and pull focus back in if it somehow escaped the panel.
  if (e.shiftKey && (active === first || !panelEl.value?.contains(active))) {
    e.preventDefault()
    last.focus()
  } else if (!e.shiftKey && active === last) {
    e.preventDefault()
    first.focus()
  }
}

// Lock page scroll behind the sheet, restoring whatever the app had set (never assume '').
let priorOverflow: string | null = null
function setScrollLock(on: boolean) {
  if (typeof document === 'undefined') return
  if (on) {
    if (priorOverflow === null) priorOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
  } else if (priorOverflow !== null) {
    document.body.style.overflow = priorOverflow
    priorOverflow = null
  }
}
watch([isOpen, isModal], ([openNow, modalNow]) => setScrollLock(openNow && modalNow), { immediate: true })
// A route change can unmount the widget mid-open; never leave the app unscrollable.
onBeforeUnmount(() => {
  setScrollLock(false)
  if (clearConfirmTimer) clearTimeout(clearConfirmTimer)
})

// Inline two-step delete confirmation — no native confirm()/modal. The
// trash icon arms an inline "¿Borrar? ✓ ✕" in the header; it auto-disarms
// after a few seconds if ignored, so a stray click never destroys history.
const confirmingClear = ref(false)
let clearConfirmTimer: ReturnType<typeof setTimeout> | null = null

function requestClear() {
  confirmingClear.value = true
  if (clearConfirmTimer) clearTimeout(clearConfirmTimer)
  clearConfirmTimer = setTimeout(() => { confirmingClear.value = false }, 4000)
}

function cancelClear() {
  confirmingClear.value = false
  if (clearConfirmTimer) { clearTimeout(clearConfirmTimer); clearConfirmTimer = null }
}

function clearHistory() {
  cancelClear()
  messages.value = []
  errorText.value = ''
  showJump.value = false
}

function scrollToBottom() {
  const el = scrollEl.value
  if (el) el.scrollTop = el.scrollHeight
  showJump.value = false
}

// ── Ancho expandible (1× → 2× → 3×, tope en viewport) ────────────────────────
// Un solo botón cicla los tres anchos; pensado para respuestas con tablas o citas
// largas. Las clases .size-2x/.size-3x viven en el <style> de ambos formularios.
const sizeStep = ref(0)
const sizeLabel = computed(() =>
  sizeStep.value === 0 ? 'Ampliar (2×)' : sizeStep.value === 1 ? 'Ampliar (3×)' : 'Ancho normal')
function cycleSize() { sizeStep.value = (sizeStep.value + 1) % 3 }

// ── Copiar mensaje (texto plano del turno, no el HTML renderizado) ────────────
const copiedIdx = ref(-1)
async function copyMessage(i: number, text: string) {
  try {
    await navigator.clipboard.writeText(text)
    copiedIdx.value = i
    setTimeout(() => { if (copiedIdx.value === i) copiedIdx.value = -1 }, 1200)
  } catch {
    // clipboard denegado (permiso / contexto inseguro): el botón simplemente no confirma
  }
}

// ── Regenerar la última respuesta ─────────────────────────────────────────────
// Retira el último intercambio y re-envía la misma pregunta por submit(), que ya
// posee el transport, el recorte de historia y el manejo de errores.
function regenerate() {
  if (loading.value) return
  const msgs = messages.value
  const last = msgs[msgs.length - 1]
  const prevUser = msgs[msgs.length - 2]
  if (!last || last.role !== 'assistant' || !prevUser || prevUser.role !== 'user') return
  msgs.pop()
  msgs.pop()
  void submit(prevUser.content)
}

// ── Píldora «Al final» cuando el usuario scrollea lejos del último mensaje ────
const showJump = ref(false)
function onScroll() {
  const el = scrollEl.value
  if (!el) return
  showJump.value = el.scrollHeight - el.scrollTop - el.clientHeight > 160
}

function renderMarkdown(text: string | null | undefined): string {
  if (typeof text !== 'string' || !text) return ''
  const raw = marked.parse(text, { async: false, breaks: true }) as string
  return DOMPurify.sanitize(raw)
}

// Shell-style input history: ↑/↓ recall previously-sent messages.
// historyCursor === -1 means "editing the live draft"; navigating stashes
// the draft so ↓ past the newest entry restores it.
const inputHistory = ref<string[]>([])
let historyCursor = -1
let historyDraft = ''

function restoreCaretEnd(ta: HTMLTextAreaElement) {
  nextTick(() => { const len = ta.value.length; ta.setSelectionRange(len, len) })
}

function navigateHistory(dir: -1 | 1, ta: HTMLTextAreaElement) {
  const n = inputHistory.value.length
  if (!n) return
  if (historyCursor === -1) {
    if (dir === 1) return
    historyDraft = input.value
    historyCursor = n - 1
  } else {
    historyCursor += dir
    if (historyCursor >= n) {
      historyCursor = -1
      input.value = historyDraft
      restoreCaretEnd(ta)
      return
    }
    if (historyCursor < 0) historyCursor = 0
  }
  input.value = inputHistory.value[historyCursor]
  restoreCaretEnd(ta)
}

async function submit(textOverride?: string) {
  const text = (textOverride ?? input.value).trim()
  if (!text || loading.value) return

  errorText.value = ''
  // Trim local history to last 6 messages for the wire payload (matches the
  // backend's context window — see chat-contract).
  const history = messages.value.slice(-6)
  messages.value.push({ role: 'user', content: text })
  inputHistory.value.push(text)
  historyCursor = -1
  historyDraft = ''
  input.value = ''
  loading.value = true
  await nextTick()
  scrollToBottom()

  try {
    let resp = await props.send({ message: text, history })
    // Nerea standard: a gate block caused by CONTAMINATED HISTORY (an earlier
    // turn, not this message) bricks the thread — every resend re-includes the
    // poisoned turn. Retry once WITHOUT history; this message was already gated
    // on its own, so it's safe and recovers the conversation instead of looping
    // "no puedo procesar…". (Depends on the backend returning 200 + blocked:true
    // on a gate block, per the Nerea client contract — not a 503.)
    if (resp?.blocked && history.length) {
      resp = await props.send({ message: text, history: [] })
    }
    // Defensive: backend may legitimately return null/undefined on a gate-blocked
    // or upstream-error path. Render an inline notice instead of pushing a poison
    // message that crashes marked.
    const reply = typeof resp?.reply === 'string' && resp.reply
      ? resp.reply
      : '_(respuesta vacía del asistente)_'
    const sources = Array.isArray(resp?.sources) ? resp.sources.filter(Boolean) : []
    messages.value.push({ role: 'assistant', content: reply, sources })
    // Una respuesta real es la mejor prueba de vida que existe — mejor que cualquier
    // sonda. (Un `blocked` también llegó por el cable: el gate opinó, la conexión sirve.)
    status.value = 'en-linea'
    lastProbeAt = Date.now()
  } catch (err: unknown) {
    const code = (err as { status?: number; statusCode?: number }).status
      ?? (err as { status?: number; statusCode?: number }).statusCode
    if (code === 429) {
      errorText.value = 'Ha alcanzado el límite de consultas. Intente más tarde.'
      status.value = 'limitado'
    } else if (code === 401) {
      // La app dueña del transporte rebota a SSO; aquí solo se dice la verdad mientras tanto.
      errorText.value = 'Su sesión expiró. Vuelva a iniciar sesión.'
      status.value = 'desconocido'
    } else if (code === 403) {
      errorText.value = 'No tiene permiso para usar el asistente. Solicítelo a su administrador.'
      status.value = 'sin-permiso'
    } else {
      errorText.value = 'Asistente no disponible. Intente más tarde.'
      status.value = 'no-disponible'
    }
    lastProbeAt = Date.now()
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
    // Devolver el cursor al cuadro de texto. Sin esto, el foco se queda en el botón
    // «Enviar» (si se envió con clic) y hay que volver al campo con el mouse en cada
    // turno — el hilo de la conversación se rompe en la mano del usuario.
    if (isOpen.value) inputEl.value?.focus()
  }
}

function onKeydown(e: KeyboardEvent) {
  const ta = e.target as HTMLTextAreaElement
  // ↑/↓ recall input history — only when the caret is on the first/last line,
  // so multi-line editing (Shift+Enter drafts) still moves the caret normally.
  if (e.key === 'ArrowUp' && !e.shiftKey && !ta.value.slice(0, ta.selectionStart).includes('\n')) {
    if (inputHistory.value.length) { e.preventDefault(); navigateHistory(-1, ta); return }
  }
  if (e.key === 'ArrowDown' && !e.shiftKey && !ta.value.slice(ta.selectionEnd).includes('\n')) {
    if (historyCursor !== -1) { e.preventDefault(); navigateHistory(1, ta); return }
  }
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="pharos-chat-root" :class="`is-${triggerMode}`">
    <!-- LAUNCHER · floating — fixed, out of flow, bottom-right (the default) -->
    <button
      v-if="!isOpen && triggerMode === 'floating'"
      ref="launcherEl"
      type="button"
      class="pharos-chat-launcher"
      :class="`bg-${avatarBg}`"
      aria-label="Abrir asistente de ayuda"
      :title="heading"
      @click="open"
    >
      <PharosChatAvatar v-if="avatar" :id="avatar"/>
      <svg
        v-else
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>

    <!-- LAUNCHER · topbar — IN FLOW, sits among the app's topbar actions. Requires the component
         to be mounted inside the topbar (chat-widget.md); the root is `display: contents` here.
         Es un TOGGLE: no se desmonta al abrir — queda con estado activo y un segundo click cierra.
         (Con `form: sheet` el drawer de altura completa lo cubre físicamente mientras está abierto;
         el ciclo completo abrir/cerrar luce con `form: corner`, donde el botón queda siempre visible.) -->
    <button
      v-if="triggerMode === 'topbar'"
      ref="launcherEl"
      type="button"
      class="pharos-chat-topbar-btn"
      :class="[`bg-${avatarBg}`, isOpen ? 'is-open' : '']"
      :aria-label="isOpen ? 'Cerrar asistente de ayuda' : 'Abrir asistente de ayuda'"
      :aria-expanded="isOpen"
      :title="heading"
      @click="isOpen ? close() : open()"
    >
      <PharosChatAvatar v-if="avatar" :id="avatar"/>
      <svg
        v-else
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <span
        v-if="statusLine"
        class="pharos-chat-dot"
        :class="`is-${status}`"
        role="img"
        :aria-label="`Asistente: ${statusText}`"
      />
    </button>

    <!-- Backdrop — only the side sheet dims the app behind it. -->
    <div
      v-if="isOpen && isModal"
      class="pharos-chat-backdrop"
      aria-hidden="true"
      @click="close"
    />

    <!-- PANEL — corner card, or full-height side sheet -->
    <section
      v-if="isOpen"
      ref="panelEl"
      class="pharos-chat-panel"
      :class="[`is-${formMode}`, sizeStep === 1 ? 'size-2x' : sizeStep === 2 ? 'size-3x' : '']"
      role="dialog"
      :aria-modal="isModal ? 'true' : undefined"
      :aria-label="heading"
      tabindex="-1"
      @keydown="onPanelKeydown"
    >
      <header class="pharos-chat-header">
        <span v-if="avatar" class="pharos-chat-avatar" :class="`bg-${avatarBg}`">
          <PharosChatAvatar :id="avatar"/>
        </span>
        <div class="pharos-chat-identity">
          <h3>{{ heading }}</h3>
          <p v-if="statusLine" class="pharos-chat-status" :class="`is-${status}`" role="status">
            <svg
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path v-if="statusGlyph === 'check'" d="M20 6 9 17l-5-5"/>
              <template v-else-if="statusGlyph === 'lock'">
                <rect width="16" height="10" x="4" y="11" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>
              </template>
              <template v-else-if="statusGlyph === 'hourglass'">
                <path d="M5 22h14"/><path d="M5 2h14"/>
                <path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"/>
                <path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"/>
              </template>
              <template v-else-if="statusGlyph === 'cross'">
                <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
              </template>
              <template v-else>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>
              </template>
            </svg>
            {{ statusText }}
          </p>
        </div>
        <div class="pharos-chat-header-actions">
          <button
            type="button"
            class="pharos-chat-icon-btn"
            :title="sizeLabel"
            :aria-label="sizeLabel"
            @click="cycleSize"
          >
            <!-- lucide fold-horizontal / unfold-horizontal (inlined, ISC) -->
            <svg
              v-if="sizeStep === 2"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M2 12h6"/><path d="M22 12h-6"/><path d="M12 2v2"/><path d="M12 8v2"/>
              <path d="M12 14v2"/><path d="M12 20v2"/><path d="m19 9-3 3 3 3"/><path d="m5 15-3-3 3-3"/>
            </svg>
            <svg
              v-else
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M16 12h6"/><path d="M8 12H2"/><path d="M12 2v2"/><path d="M12 8v2"/>
              <path d="M12 14v2"/><path d="M12 20v2"/><path d="m19 15 3-3-3-3"/><path d="m5 9-3 3 3 3"/>
            </svg>
          </button>
          <template v-if="messages.length">
            <button
              v-if="!confirmingClear"
              type="button"
              class="pharos-chat-icon-btn"
              title="Borrar conversación"
              aria-label="Borrar conversación"
              @click="requestClear"
            >
              <svg
                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M3 6h18"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
            <template v-else>
              <span class="pharos-chat-clear-confirm" role="status">¿Borrar?</span>
              <button
                type="button"
                class="pharos-chat-icon-btn pharos-chat-icon-btn--danger"
                title="Confirmar borrado"
                aria-label="Confirmar borrado"
                @click="clearHistory"
              >
                <svg
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M20 6 9 17l-5-5"/>
                </svg>
              </button>
              <button
                type="button"
                class="pharos-chat-icon-btn"
                title="Cancelar"
                aria-label="Cancelar borrado"
                @click="cancelClear"
              >
                <svg
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M18 6 6 18"/>
                  <path d="m6 6 12 12"/>
                </svg>
              </button>
            </template>
          </template>
          <button
            type="button"
            class="pharos-chat-icon-btn"
            aria-label="Cerrar"
            @click="close"
          >
            <svg
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M18 6 6 18"/>
              <path d="m6 6 12 12"/>
            </svg>
          </button>
        </div>
      </header>

      <div ref="scrollEl" class="pharos-chat-scroll" @scroll.passive="onScroll">
        <!-- Empty state with starter chips -->
        <div v-if="!messages.length" class="pharos-chat-empty">
          <p class="pharos-chat-empty-hint">
            {{ greeting }}
          </p>
          <div v-if="starters.length" class="pharos-chat-starters">
            <button
              v-for="(s, i) in starters"
              :key="i"
              type="button"
              class="pharos-chat-starter"
              :disabled="loading"
              @click="submit(s)"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <!-- Conversation -->
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="pharos-chat-msg"
          :class="m.role === 'user' ? 'is-user' : 'is-bot'"
        >
          <div class="pharos-chat-bubble-wrap">
            <!-- eslint-disable-next-line vue/no-v-html -->
            <div class="pharos-chat-bubble" v-html="renderMarkdown(m.content)"/>
            <!-- Corpus citations (chat-contract CH5) — only on grounded assistant replies. -->
            <p v-if="citations && m.role === 'assistant' && m.sources && m.sources.length" class="pharos-chat-sources">
              <span class="pharos-chat-sources-label">Fuentes:</span>
              <span v-for="(src, j) in m.sources" :key="j" class="pharos-chat-source">{{ src }}</span>
            </p>
            <!-- Acciones por turno — visibles al pasar el mouse o con foco de teclado.
                 Copiar toma el markdown crudo del turno; regenerar solo en la última respuesta. -->
            <div class="pharos-chat-msg-actions">
              <button
                type="button"
                class="pharos-chat-icon-btn"
                :title="copiedIdx === i ? 'Copiado' : 'Copiar mensaje'"
                :aria-label="copiedIdx === i ? 'Copiado' : 'Copiar mensaje'"
                @click="copyMessage(i, m.content)"
              >
                <svg
                  v-if="copiedIdx === i"
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="is-copied">
                  <path d="M20 6 9 17l-5-5"/>
                </svg>
                <svg
                  v-else
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
                  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
                </svg>
              </button>
              <button
                v-if="m.role === 'assistant' && i === messages.length - 1 && !loading"
                type="button"
                class="pharos-chat-icon-btn"
                title="Regenerar respuesta"
                aria-label="Regenerar respuesta"
                @click="regenerate"
              >
                <svg
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                  <path d="M3 3v5h5"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="pharos-chat-msg is-bot">
          <div class="pharos-chat-bubble pharos-chat-thinking">
            <span/><span/><span/>
            <span class="pharos-chat-visually-hidden">Pensando…</span>
          </div>
        </div>

        <p v-if="errorText" class="pharos-chat-error" role="alert">{{ errorText }}</p>
      </div>

      <!-- Píldora «Al final» — aparece cuando el usuario está lejos del último mensaje. -->
      <button
        v-if="showJump"
        type="button"
        class="pharos-chat-jump"
        aria-label="Bajar al final"
        @click="scrollToBottom"
      >
        <svg
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M12 5v14"/>
          <path d="m19 12-7 7-7-7"/>
        </svg>
        Al final
      </button>

      <footer class="pharos-chat-input-row">
        <!-- El textarea NO se deshabilita mientras carga. Deshabilitar el elemento enfocado hace
             que el navegador suelte el foco al <body>, y nada lo devolvía: se escribía, se enviaba
             con Enter, y el cursor desaparecía del cuadro. Nada se ganaba a cambio — submit() ya
             corta la reentrada con `if (!text || loading.value) return`. De paso, ahora se puede ir
             redactando la siguiente pregunta mientras Nerea piensa. -->
        <textarea
          ref="inputEl"
          v-model="input"
          rows="2"
          :placeholder="placeholder"
          class="pharos-chat-input"
          @keydown="onKeydown"
        />
        <button
          type="button"
          class="pharos-chat-send"
          :disabled="loading || !input.trim()"
          aria-label="Enviar"
          @click="submit()"
        >
          <svg
            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M22 2 11 13"/>
            <path d="M22 2 15 22l-4-9-9-4z"/>
          </svg>
        </button>
      </footer>
    </section>
  </div>
</template>

<style scoped>
/* FLOATING: the root itself is the fixed bottom-right anchor (the historical behaviour).
   TOPBAR:   the root must NOT be a positioned box, or the in-flow button would be yanked out of
             the topbar. `display: contents` removes it from layout entirely, so the button becomes
             a direct flex child of the app's topbar. The panel/backdrop are `position: fixed` in
             their own right, so they are unaffected by this. */
.pharos-chat-root.is-floating {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  z-index: 90;
}
.pharos-chat-root.is-topbar {
  display: contents;
}

.pharos-chat-launcher {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--primary);
  color: var(--primary-foreground);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
  transition: transform 120ms ease, box-shadow 120ms ease;
}
.pharos-chat-launcher:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.28);
}
.pharos-chat-launcher svg { width: 22px; height: 22px; }
/* Bare glyph: no chip, the mark itself IS the launcher (accent-coloured, no plate). */
.pharos-chat-launcher.bg-solo {
  width: 56px;
  height: 56px;
  border: none;
  background: transparent;
  color: var(--primary);
  box-shadow: none;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.22));
}
.pharos-chat-launcher.bg-solo svg { width: 40px; height: 40px; }

/* TOPBAR launcher — in-flow, sized like a topbar icon action (not a floating bubble). */
.pharos-chat-topbar-btn {
  position: relative;
  width: 36px;
  height: 36px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--muted);
  color: var(--foreground);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 120ms ease, color 120ms ease;
}
.pharos-chat-topbar-btn:hover {
  background: var(--accent);
}
.pharos-chat-topbar-btn svg { width: 20px; height: 20px; }
.pharos-chat-topbar-btn.bg-solo {
  border: none;
  background: transparent;
}
.pharos-chat-topbar-btn.bg-solo:hover { color: var(--primary); }
.pharos-chat-topbar-btn.bg-solo svg { width: 24px; height: 24px; }
/* Toggle abierto: el launcher queda montado y lo dice visualmente. */
.pharos-chat-topbar-btn.is-open {
  color: var(--primary);
  box-shadow: 0 0 0 2px color-mix(in oklab, var(--primary) 45%, transparent);
}
.pharos-chat-topbar-btn.bg-solo.is-open {
  box-shadow: none;
  background: color-mix(in oklab, var(--primary) 12%, transparent);
  border-radius: 8px;
}

/* Presence dot on the topbar launcher — 10px, so colour alone is NOT a legible signal
   (and «warning» vs «success» is a known confusable pair in this palette). Each state
   therefore differs in FILL and SHAPE as well as hue, and carries an aria-label with the
   word; the panel header spells the state out in full. */
.pharos-chat-dot {
  position: absolute;
  top: -1px;
  right: -1px;
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: 2px solid var(--card);
  background: var(--muted-foreground);
}
/* En línea — círculo lleno. El único estado «todo bien», y el único relleno sólido verde. */
.pharos-chat-dot.is-en-linea { background: var(--status-success); }
/* Sin verificar — anillo hueco: hay algo que todavía no sabemos. */
.pharos-chat-dot.is-desconocido {
  background: var(--card);
  box-shadow: inset 0 0 0 2px var(--muted-foreground);
}
/* Sin permiso / límite — cuadrado ámbar: distinto de todo círculo, accionable por el usuario. */
.pharos-chat-dot.is-sin-permiso,
.pharos-chat-dot.is-limitado {
  background: var(--status-warning);
  border-radius: 2px;
}
/* El límite además se distingue del permiso por tamaño (mismo color, otra silueta). */
.pharos-chat-dot.is-limitado { width: 8px; height: 8px; }
/* No disponible — rombo rojo: la silueta más distinta del conjunto. */
.pharos-chat-dot.is-no-disponible {
  background: var(--status-error);
  border-radius: 1px;
  transform: rotate(45deg);
}

.pharos-chat-backdrop {
  position: fixed;
  inset: 0;
  z-index: 95;
  background: rgba(0, 0, 0, 0.3);
}

.pharos-chat-panel {
  position: fixed;
  z-index: 100;
  background-color: var(--popover);
  color: var(--popover-foreground);
  border: 1px solid var(--border);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.32), 0 2px 6px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* CORNER — the historical card, bottom-right. */
.pharos-chat-panel.is-corner {
  right: 1.25rem;
  bottom: 1.25rem;
  width: 380px;
  max-width: calc(100vw - 1rem);
  height: 540px;
  max-height: calc(100vh - 2rem);
  border-radius: 14px;
  animation: pharos-chat-rise 160ms ease-out;
  transition: width 300ms ease;
}
/* Ancho expandible (botón del header): 1× → 2× → 3×, siempre bajo el max-width del viewport. */
.pharos-chat-panel.is-corner.size-2x { width: 760px; }
.pharos-chat-panel.is-corner.size-3x { width: 1140px; }

/* SHEET — full-height side drawer. Slides in from the right; only the left edge is drawn. */
.pharos-chat-panel.is-sheet {
  top: 0;
  right: 0;
  bottom: 0;
  width: 22rem;
  max-width: 92vw;
  border-radius: 0;
  border-top: none;
  border-right: none;
  border-bottom: none;
  animation: pharos-chat-slide 180ms ease-out;
  transition: width 300ms ease;
}
.pharos-chat-panel.is-sheet.size-2x { width: 44rem; }
.pharos-chat-panel.is-sheet.size-3x { width: 66rem; }

@keyframes pharos-chat-rise {
  from { transform: translateY(8px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}
@keyframes pharos-chat-slide {
  from { transform: translateX(12px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

.pharos-chat-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 0.9rem;
  border-bottom: 1px solid var(--border);
  background-color: var(--popover);
}
.pharos-chat-header h3 {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: var(--popover-foreground);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.pharos-chat-identity {
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.pharos-chat-status {
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.68rem;
  line-height: 1.2;
  color: var(--muted-foreground);
}
.pharos-chat-status svg { width: 10px; height: 10px; flex-shrink: 0; }
.pharos-chat-status.is-en-linea { color: var(--status-success); }
.pharos-chat-status.is-sin-permiso,
.pharos-chat-status.is-limitado { color: var(--status-warning); }
.pharos-chat-status.is-no-disponible { color: var(--status-error); }
.pharos-chat-avatar {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}
.pharos-chat-avatar.bg-circulo {
  width: 30px;
  height: 30px;
  border-radius: 999px;
  background: color-mix(in oklab, var(--primary) 12%, transparent);
}
.pharos-chat-avatar svg { width: 18px; height: 18px; }
.pharos-chat-avatar.bg-solo svg { width: 22px; height: 22px; }

.pharos-chat-header-actions {
  display: inline-flex;
  gap: 0.25rem;
  margin-left: auto;
}

.pharos-chat-icon-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--muted-foreground);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 120ms ease, color 120ms ease;
}
.pharos-chat-icon-btn:hover {
  background: var(--accent);
  color: var(--foreground);
}
.pharos-chat-icon-btn svg { width: 16px; height: 16px; }
.pharos-chat-icon-btn--danger:hover {
  background: var(--destructive, #dc2626);
  color: var(--destructive-foreground, #fff);
}
.pharos-chat-clear-confirm {
  font-size: 12px;
  color: var(--muted-foreground);
  align-self: center;
  white-space: nowrap;
  margin-right: 2px;
}

.pharos-chat-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0.85rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.pharos-chat-empty {
  text-align: center;
  padding: 1rem 0.5rem 0;
  color: var(--muted-foreground);
}
.pharos-chat-empty-hint {
  margin: 0 0 0.85rem 0;
  font-size: 0.88rem;
}
.pharos-chat-starters {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.pharos-chat-starter {
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--foreground);
  border-radius: 8px;
  padding: 0.55rem 0.7rem;
  font-size: 0.84rem;
  text-align: left;
  cursor: pointer;
  transition: background-color 120ms ease, border-color 120ms ease;
}
.pharos-chat-starter:hover:not(:disabled) {
  background: var(--accent);
  border-color: var(--primary);
}
.pharos-chat-starter:disabled { opacity: 0.6; cursor: not-allowed; }

.pharos-chat-msg {
  display: flex;
}
.pharos-chat-msg.is-user { justify-content: flex-end; }
.pharos-chat-msg.is-bot  { justify-content: flex-start; }

.pharos-chat-bubble-wrap {
  max-width: 85%;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.is-user .pharos-chat-bubble-wrap { align-items: flex-end; }

.pharos-chat-bubble {
  padding: 0.55rem 0.75rem;
  border-radius: 12px;
  font-size: 0.86rem;
  line-height: 1.45;
  word-wrap: break-word;
  overflow-wrap: anywhere;
}
.is-user .pharos-chat-bubble {
  background: var(--primary);
  color: var(--primary-foreground);
  border-bottom-right-radius: 4px;
}
.is-bot .pharos-chat-bubble {
  background: var(--muted);
  color: var(--foreground);
  border: 1px solid var(--border);
  border-bottom-left-radius: 4px;
}
.pharos-chat-bubble :deep(p)        { margin: 0.25rem 0; }
.pharos-chat-bubble :deep(p:first-child) { margin-top: 0; }
.pharos-chat-bubble :deep(p:last-child)  { margin-bottom: 0; }
.pharos-chat-bubble :deep(ul),
.pharos-chat-bubble :deep(ol)       { margin: 0.3rem 0; padding-left: 1.2rem; }
.pharos-chat-bubble :deep(li)       { margin: 0.15rem 0; }
.pharos-chat-bubble :deep(strong)   { color: inherit; font-weight: 600; }
.pharos-chat-bubble :deep(code) {
  background: var(--accent);
  padding: 0.05rem 0.3rem;
  border-radius: 4px;
  font-size: 0.85em;
  font-family: var(--font-mono);
}
.pharos-chat-bubble :deep(pre) {
  background: var(--accent);
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 0.3rem 0;
}
.pharos-chat-bubble :deep(pre code) {
  background: transparent;
  padding: 0;
}
.pharos-chat-bubble :deep(a) {
  color: var(--primary);
  text-decoration: underline;
}

/* Acciones por turno: invisibles hasta hover del turno o foco de teclado dentro de ellas. */
.pharos-chat-msg-actions {
  display: inline-flex;
  gap: 0.1rem;
  opacity: 0;
  transition: opacity 120ms ease;
}
.pharos-chat-msg:hover .pharos-chat-msg-actions,
.pharos-chat-msg-actions:focus-within { opacity: 1; }
.pharos-chat-msg-actions .pharos-chat-icon-btn { width: 24px; height: 24px; }
.pharos-chat-msg-actions .pharos-chat-icon-btn svg { width: 14px; height: 14px; }
.pharos-chat-msg-actions svg.is-copied { color: var(--status-success); }

/* Píldora «Al final» — flota sobre el borde inferior del hilo, encima del input. */
.pharos-chat-jump {
  position: absolute;
  bottom: 4.6rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--popover);
  color: var(--muted-foreground);
  padding: 0.25rem 0.65rem;
  font-size: 0.72rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
  transition: color 120ms ease;
}
.pharos-chat-jump:hover { color: var(--foreground); }
.pharos-chat-jump svg { width: 13px; height: 13px; }

.pharos-chat-sources {
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  align-items: baseline;
  font-size: 0.72rem;
  color: var(--muted-foreground);
}
.pharos-chat-sources-label { font-weight: 600; }
.pharos-chat-source {
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.05rem 0.45rem;
  background: var(--card);
}

.pharos-chat-thinking {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--muted);
  border: 1px solid var(--border);
}
.pharos-chat-thinking span {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--muted-foreground);
  animation: pharos-chat-dot 1.2s infinite ease-in-out;
}
.pharos-chat-thinking span:nth-child(2) { animation-delay: 0.15s; }
.pharos-chat-thinking span:nth-child(3) { animation-delay: 0.3s; }
@keyframes pharos-chat-dot {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.85); }
  40%           { opacity: 1;   transform: scale(1); }
}
.pharos-chat-visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0, 0, 0, 0);
  white-space: nowrap; border: 0;
}

.pharos-chat-error {
  margin: 0.4rem 0 0 0;
  padding: 0.45rem 0.6rem;
  background: var(--status-error-bg);
  color: var(--status-error);
  border: 1px solid var(--status-error);
  border-radius: 8px;
  font-size: 0.82rem;
}

.pharos-chat-input-row {
  display: flex;
  gap: 0.45rem;
  padding: 0.6rem 0.7rem;
  border-top: 1px solid var(--border);
  background-color: var(--popover);
}
.pharos-chat-input {
  flex: 1;
  resize: none;
  border: 1px solid var(--input);
  border-radius: 8px;
  padding: 0.5rem 0.6rem;
  font: inherit;
  font-size: 0.86rem;
  background: var(--background);
  color: var(--foreground);
  outline: none;
}
.pharos-chat-input:focus {
  border-color: var(--ring);
}
.pharos-chat-input:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.pharos-chat-send {
  width: 38px;
  height: 38px;
  align-self: flex-end;
  border: none;
  border-radius: 8px;
  background: var(--primary);
  color: var(--primary-foreground);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 120ms ease;
}
.pharos-chat-send:disabled { opacity: 0.5; cursor: not-allowed; }
.pharos-chat-send svg { width: 16px; height: 16px; }
</style>
