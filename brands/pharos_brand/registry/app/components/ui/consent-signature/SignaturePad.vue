<script setup lang="ts">
// Signature pad — a plain <canvas> with pointer events. No dependency on
// purpose: the registry rule is «no new deps per adopting app», and the two
// legacy fronts' `vue-signature-pad` is exactly the kind of one-off this
// replaces. Exports PNG base64 WITHOUT the data-URL prefix (the service
// `b64decode`s the string as-is).
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  /** Drawing surface height in CSS px; width follows the container. */
  height?: number
  /** Stroke width in CSS px. */
  strokeWidth?: number
  disabled?: boolean
}>(), {
  height: 200,
  strokeWidth: 2.5,
  disabled: false,
})

const emit = defineEmits<{
  /** Fires on every completed stroke with whether the pad has ink. */
  change: [hasInk: boolean]
}>()

const canvas = ref<HTMLCanvasElement | null>(null)
const drawing = ref(false)
const hasInk = ref(false)
let ctx: CanvasRenderingContext2D | null = null
let last: { x: number, y: number } | null = null

function pointOf(ev: PointerEvent): { x: number, y: number } {
  const rect = canvas.value!.getBoundingClientRect()
  return { x: ev.clientX - rect.left, y: ev.clientY - rect.top }
}

function resize() {
  const el = canvas.value
  if (!el) return
  const ratio = window.devicePixelRatio || 1
  const width = el.clientWidth
  // Keep the ink across a resize: re-paint the previous bitmap scaled.
  const snapshot = hasInk.value ? el.toDataURL('image/png') : null
  el.width = Math.max(1, Math.round(width * ratio))
  el.height = Math.max(1, Math.round(props.height * ratio))
  ctx = el.getContext('2d')
  if (!ctx) return
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  ctx.lineWidth = props.strokeWidth
  ctx.strokeStyle = getComputedStyle(el).color
  if (snapshot) {
    const img = new Image()
    img.onload = () => ctx?.drawImage(img, 0, 0, width, props.height)
    img.src = snapshot
  }
}

function onDown(ev: PointerEvent) {
  if (props.disabled || !ctx) return
  canvas.value?.setPointerCapture(ev.pointerId)
  drawing.value = true
  last = pointOf(ev)
  ctx.beginPath()
  ctx.moveTo(last.x, last.y)
  // A tap without movement still leaves a dot — a signature can start with one.
  ctx.lineTo(last.x + 0.01, last.y + 0.01)
  ctx.stroke()
  hasInk.value = true
}

function onMove(ev: PointerEvent) {
  if (!drawing.value || !ctx || !last) return
  const p = pointOf(ev)
  ctx.beginPath()
  ctx.moveTo(last.x, last.y)
  ctx.lineTo(p.x, p.y)
  ctx.stroke()
  last = p
}

function onUp(ev: PointerEvent) {
  if (!drawing.value) return
  drawing.value = false
  last = null
  canvas.value?.releasePointerCapture(ev.pointerId)
  emit('change', hasInk.value)
}

function clear() {
  const el = canvas.value
  if (!el || !ctx) return
  ctx.save()
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.clearRect(0, 0, el.width, el.height)
  ctx.restore()
  hasInk.value = false
  emit('change', false)
}

/** PNG base64 without the `data:image/png;base64,` prefix; `null` when empty. */
function toPngBase64(): string | null {
  const el = canvas.value
  if (!el || !hasInk.value) return null
  return el.toDataURL('image/png').replace(/^data:image\/png;base64,/, '')
}

function isEmpty(): boolean {
  return !hasInk.value
}

let observer: ResizeObserver | null = null
onMounted(() => {
  resize()
  if (typeof ResizeObserver !== 'undefined' && canvas.value) {
    observer = new ResizeObserver(() => resize())
    observer.observe(canvas.value)
  }
})
onBeforeUnmount(() => observer?.disconnect())
watch(() => props.height, resize)

defineExpose({ clear, toPngBase64, isEmpty })
</script>

<template>
  <canvas
    ref="canvas"
    class="w-full touch-none rounded-md border border-dashed border-border bg-background text-foreground"
    :class="disabled ? 'cursor-not-allowed opacity-60' : 'cursor-crosshair'"
    :style="{ height: `${height}px` }"
    role="img"
    aria-label="Área de firma"
    @pointerdown="onDown"
    @pointermove="onMove"
    @pointerup="onUp"
    @pointercancel="onUp"
    @pointerleave="onUp"
  />
</template>
