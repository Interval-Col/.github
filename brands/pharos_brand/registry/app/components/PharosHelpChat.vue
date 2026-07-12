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
import { ref, nextTick, onMounted, watch } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

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

const props = withDefaults(defineProps<{
  /** App-owned transport to the chat endpoint (Bearer / 401 bounce stay app-side). */
  send: (payload: { message: string; history: ChatMessage[] }) => Promise<ChatReply>
  /** Brand name shown in the greeting ("el asistente de {brandName}"). */
  brandName?: string
  /** Panel title + dialog aria-label. */
  title?: string
  /** Suggested opening questions (empty = no starter chips). */
  starters?: string[]
  /** sessionStorage key — MUST be unique per app so histories never collide. */
  storageKey?: string
  /** Textarea placeholder. */
  placeholder?: string
}>(), {
  brandName: 'Pháros',
  title: 'Asistente de ayuda',
  starters: () => [],
  storageKey: 'pharos-help-chat-history',
  placeholder: 'Escriba su pregunta…',
})

const isOpen = ref(false)
const input = ref('')
const messages = ref<ChatMessage[]>([])
const loading = ref(false)
const errorText = ref('')
const scrollEl = ref<HTMLElement | null>(null)
const inputEl = ref<HTMLTextAreaElement | null>(null)

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
  nextTick(() => {
    inputEl.value?.focus()
    scrollToBottom()
  })
}

function close() {
  isOpen.value = false
}

function clearHistory() {
  if (!window.confirm('¿Borrar la conversación actual?')) return
  messages.value = []
  errorText.value = ''
}

function scrollToBottom() {
  const el = scrollEl.value
  if (el) el.scrollTop = el.scrollHeight
}

function renderMarkdown(text: string | null | undefined): string {
  if (typeof text !== 'string' || !text) return ''
  const raw = marked.parse(text, { async: false, breaks: true }) as string
  return DOMPurify.sanitize(raw)
}

async function submit(textOverride?: string) {
  const text = (textOverride ?? input.value).trim()
  if (!text || loading.value) return

  errorText.value = ''
  // Trim local history to last 6 messages for the wire payload (matches the
  // backend's context window — see chat-contract).
  const history = messages.value.slice(-6)
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  await nextTick()
  scrollToBottom()

  try {
    const resp = await props.send({ message: text, history })
    // Defensive: backend may legitimately return null/undefined on a gate-blocked
    // or upstream-error path. Render an inline notice instead of pushing a poison
    // message that crashes marked.
    const reply = typeof resp?.reply === 'string' && resp.reply
      ? resp.reply
      : '_(respuesta vacía del asistente)_'
    const sources = Array.isArray(resp?.sources) ? resp.sources.filter(Boolean) : []
    messages.value.push({ role: 'assistant', content: reply, sources })
  } catch (err: unknown) {
    const status = (err as { status?: number; statusCode?: number }).status
      ?? (err as { status?: number; statusCode?: number }).statusCode
    if (status === 429) {
      errorText.value = 'Ha alcanzado el límite de consultas. Intente más tarde.'
    } else {
      errorText.value = 'Asistente no disponible. Intente más tarde.'
    }
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="pharos-chat-root">
    <!-- Floating launcher -->
    <button
      v-if="!isOpen"
      type="button"
      class="pharos-chat-launcher"
      aria-label="Abrir asistente de ayuda"
      :title="title"
      @click="open"
    >
      <svg
        viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>

    <!-- Slide-up panel -->
    <section
      v-if="isOpen"
      class="pharos-chat-panel"
      role="dialog"
      :aria-label="title"
    >
      <header class="pharos-chat-header">
        <h3>{{ title }}</h3>
        <div class="pharos-chat-header-actions">
          <button
            v-if="messages.length"
            type="button"
            class="pharos-chat-icon-btn"
            title="Borrar conversación"
            aria-label="Borrar conversación"
            @click="clearHistory"
          >
            <svg
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M3 6h18"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
              <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
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

      <div ref="scrollEl" class="pharos-chat-scroll">
        <!-- Empty state with starter chips -->
        <div v-if="!messages.length" class="pharos-chat-empty">
          <p class="pharos-chat-empty-hint">
            Hola, soy el asistente de {{ brandName }}. ¿En qué puedo ayudarle?
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
            <p v-if="m.role === 'assistant' && m.sources && m.sources.length" class="pharos-chat-sources">
              <span class="pharos-chat-sources-label">Fuentes:</span>
              <span v-for="(src, j) in m.sources" :key="j" class="pharos-chat-source">{{ src }}</span>
            </p>
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

      <footer class="pharos-chat-input-row">
        <textarea
          ref="inputEl"
          v-model="input"
          rows="2"
          :placeholder="placeholder"
          :disabled="loading"
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
.pharos-chat-root {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  z-index: 90;
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

.pharos-chat-panel {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  width: 380px;
  max-width: calc(100vw - 1rem);
  height: 540px;
  max-height: calc(100vh - 2rem);
  background-color: var(--popover);
  color: var(--popover-foreground);
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.32), 0 2px 6px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: pharos-chat-rise 160ms ease-out;
}

@keyframes pharos-chat-rise {
  from { transform: translateY(8px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

.pharos-chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
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
}
.pharos-chat-header-actions {
  display: inline-flex;
  gap: 0.25rem;
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
