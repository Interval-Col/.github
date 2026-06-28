<script setup lang="ts">
// DatePicker — the Pháros date input primitive (RFC 0008 component library).
// PROTOTYPE for co-creation (registry promotion deferred).
//
// Two entry modes on ONE field, driven by a real reception need (prereception
// birthdate): a SEGMENTED TYPED FIELD (dd/mm/aaaa, fast keyboard entry — nobody
// should click back 40 years) PLUS a CALENDAR POPOVER (browse, with month + year
// quick-navigation). It is also PROGRAMMATICALLY SETTABLE: a cédula CC scan parses
// a birthdate and sets `v-model` directly.
//
// ── Model type ──────────────────────────────────────────────────────────────
// reka-ui works internally in `CalendarDate` (@internationalized/date). This
// wrapper exposes a CLEAN model so app code + a scan handler can set it trivially:
//   v-model :: string (ISO 'YYYY-MM-DD') | Date | null
// It ACCEPTS an ISO string OR a JS Date and always EMITS an ISO string (or null).
// Convert at the edge, keep app state boring.
//
//   <DatePicker v-model="birthdate" :max="todayIso" />          ← manual
//   birthdate = '1985-07-23'                                     ← scan fill
//
import type { DateValue } from '@internationalized/date'
import { CalendarDate, DateFormatter, getLocalTimeZone, parseDate, today } from '@internationalized/date'
import {
  DatePickerArrow,
  DatePickerCalendar,
  DatePickerCell,
  DatePickerCellTrigger,
  DatePickerContent,
  DatePickerField,
  DatePickerGrid,
  DatePickerGridBody,
  DatePickerGridHead,
  DatePickerGridRow,
  DatePickerHeadCell,
  DatePickerInput,
  DatePickerNext,
  DatePickerPrev,
  DatePickerRoot,
  DatePickerTrigger,
} from 'reka-ui'
import { computed, ref, watch } from 'vue'
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'

// DatePickerRoot renders no DOM node of its own, so fallthrough attrs (e.g. the
// aria-invalid / aria-describedby a FormField hands the control) must be placed
// explicitly — we land them on the inner field container.
defineOptions({ inheritAttrs: false })

/** Anything the wrapper accepts as a value: ISO 'YYYY-MM-DD', a JS Date, or empty. */
type DateInput = string | Date | null | undefined

const props = withDefaults(defineProps<{
  /** v-model — accepts ISO 'YYYY-MM-DD' or a JS Date; emits ISO string (or null). */
  modelValue?: DateInput
  /** Earliest selectable date (ISO string or Date). */
  min?: DateInput
  /** Latest selectable date (ISO string or Date). For birthdates, pass today. */
  max?: DateInput
  disabled?: boolean
  /** Inline error state — wires aria-invalid on the control. (Message lives in the field wrapper.) */
  error?: boolean | string
  /** Placeholder shown in empty segments. */
  placeholder?: string
  /** BCP-47 locale used to format the field + calendar. */
  locale?: string
  /** Optional id for the control (a11y: pair with a FormField label). */
  id?: string
  /** Lightweight provenance hint — set to 'scan' when filled programmatically. */
  source?: 'manual' | 'scan'
}>(), {
  locale: 'es-CO',
})

const emit = defineEmits<{
  /** Emits an ISO 'YYYY-MM-DD' string, or null when cleared. */
  'update:modelValue': [value: string | null]
  /** Fires 'manual' when the USER edits the field/calendar (clears a 'scan' badge). */
  'update:source': [source: 'manual']
}>()

// ── ISO <-> CalendarDate conversion (the only place the two representations meet) ──
// We build CalendarDate at runtime but annotate as reka's DateValue union, which
// is what every reka-ui date prop expects (a bare CalendarDate doesn't satisfy
// the union under SFC strict prop typing).
function toCalendarDate(value: DateInput): DateValue | undefined {
  if (value == null || value === '') return undefined
  if (value instanceof Date) {
    if (Number.isNaN(value.getTime())) return undefined
    return new CalendarDate(value.getFullYear(), value.getMonth() + 1, value.getDate())
  }
  // ISO 'YYYY-MM-DD' (parseDate is calendar-only, no timezone — exactly what we want)
  try {
    const parsed = parseDate(value.slice(0, 10))
    return new CalendarDate(parsed.year, parsed.month, parsed.day)
  } catch {
    return undefined
  }
}

function toIso(value: DateValue | undefined): string | null {
  if (!value) return null
  const y = String(value.year).padStart(4, '0')
  const m = String(value.month).padStart(2, '0')
  const d = String(value.day).padStart(2, '0')
  return `${y}-${m}-${d}`
}

const innerValue = computed<DateValue | undefined>(() => toCalendarDate(props.modelValue))
const minValue = computed<DateValue | undefined>(() => toCalendarDate(props.min))
const maxValue = computed<DateValue | undefined>(() => toCalendarDate(props.max))
const hasError = computed(() => Boolean(props.error))

// Lazy, SSR-safe: only read the clock when we actually need a default view.
function todayDate(): DateValue {
  const t = today(getLocalTimeZone())
  return new CalendarDate(t.year, t.month, t.day)
}

// Placeholder = the calendar's "viewed" month. WRITABLE (the month/year quick-nav
// selects move it). Default it to the selected value, else max (birthdates open
// near the cap), else today — so the calendar never opens on the current month
// when you're picking a 1985 birthdate. Re-sync when the value changes externally.
const placeholderView = ref<DateValue>(
  innerValue.value ?? maxValue.value ?? minValue.value ?? todayDate(),
)
watch(innerValue, (v) => {
  if (v) placeholderView.value = v
})

// Year quick-nav range: from min (or 120y back) to max (or today). Birthdate-friendly.
const yearOptions = computed<number[]>(() => {
  const end = maxValue.value?.year ?? todayDate().year
  const start = minValue.value?.year ?? end - 120
  const years: number[] = []
  for (let y = end; y >= start; y--) years.push(y)
  return years
})

const monthFormatter = computed(() => new DateFormatter(props.locale, { month: 'long' }))
const monthOptions = computed(() =>
  Array.from({ length: 12 }, (_, i) => ({
    value: i + 1,
    // Build a throwaway date just to format the month name in-locale.
    label: monthFormatter.value.format(new Date(2000, i, 1)),
  })),
)

function onModelChange(value: DateValue | undefined) {
  emit('update:modelValue', toIso(value))
  emit('update:source', 'manual')
}

// Quick-nav (month/year selects) move the viewed placeholder, not the value.
function onMonthNav(event: Event) {
  const month = Number((event.target as HTMLSelectElement).value)
  const c = placeholderView.value
  placeholderView.value = new CalendarDate(c.year, month, Math.min(c.day, 28))
}
function onYearNav(event: Event) {
  const year = Number((event.target as HTMLSelectElement).value)
  const c = placeholderView.value
  placeholderView.value = new CalendarDate(year, c.month, Math.min(c.day, 28))
}
</script>

<template>
  <DatePickerRoot
    :id="props.id"
    :model-value="innerValue"
    :min-value="minValue"
    :max-value="maxValue"
    :placeholder="placeholderView as DateValue"
    :locale="props.locale"
    :disabled="props.disabled"
    granularity="day"
    @update:model-value="onModelChange"
    @update:placeholder="(p) => (placeholderView = p)"
  >
    <div
      v-bind="$attrs"
      :class="cn(
        'flex h-9 w-full items-center justify-between rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs transition-[color,box-shadow]',
        'focus-within:border-ring focus-within:ring-ring/50 focus-within:ring-3',
        hasError && 'border-destructive ring-destructive/20',
        props.disabled && 'pointer-events-none cursor-not-allowed opacity-50',
      )"
      :data-invalid="hasError || undefined"
      :aria-invalid="hasError || undefined"
    >
      <!-- Segmented typed field: dd/mm/aaaa, fast keyboard entry -->
      <DatePickerField v-slot="{ segments }" class="flex select-none items-center">
        <template v-for="item in segments" :key="item.part">
          <DatePickerInput
            v-if="item.part === 'literal'"
            :part="item.part"
            class="px-px text-muted-foreground"
          >
            {{ item.value }}
          </DatePickerInput>
          <DatePickerInput
            v-else
            :part="item.part"
            class="rounded px-px tabular-nums data-[placeholder]:text-muted-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none"
          >
            {{ item.value }}
          </DatePickerInput>
        </template>
      </DatePickerField>

      <!-- Calendar popover trigger -->
      <DatePickerTrigger
        class="ml-2 inline-flex size-6 items-center justify-center rounded text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none"
        aria-label="Abrir calendario"
      >
        <Icon name="calendar" :size="4" />
      </DatePickerTrigger>
    </div>

    <DatePickerContent
      :side-offset="6"
      align="end"
      class="z-50 w-auto rounded-md border bg-popover p-3 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
    >
      <DatePickerArrow class="fill-popover stroke-border" />
      <DatePickerCalendar v-slot="{ weekDays, grid }">
        <!-- Header: prev / quick-nav (month + year) / next -->
        <div class="mb-2 flex items-center justify-between gap-2">
          <DatePickerPrev
            class="inline-flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-40"
            aria-label="Mes anterior"
          >
            <Icon name="back" :size="4" />
          </DatePickerPrev>

          <div class="flex items-center gap-1.5">
            <!-- Month quick-nav -->
            <select
              :value="placeholderView.month"
              aria-label="Mes"
              class="h-7 rounded-md border border-input bg-transparent px-1.5 text-sm capitalize outline-none focus-visible:ring-2 focus-visible:ring-ring"
              @change="onMonthNav"
            >
              <option v-for="m in monthOptions" :key="m.value" :value="m.value" class="capitalize">
                {{ m.label }}
              </option>
            </select>
            <!-- Year quick-nav — the load-bearing one for birthdates -->
            <select
              :value="placeholderView.year"
              aria-label="Año"
              class="h-7 rounded-md border border-input bg-transparent px-1.5 text-sm tabular-nums outline-none focus-visible:ring-2 focus-visible:ring-ring"
              @change="onYearNav"
            >
              <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>

          <DatePickerNext
            class="inline-flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-40"
            aria-label="Mes siguiente"
          >
            <Icon name="arrowRight" :size="4" />
          </DatePickerNext>
        </div>

        <!-- Month grid(s) -->
        <div class="flex flex-col gap-4 sm:flex-row sm:gap-6">
          <DatePickerGrid
            v-for="month in grid"
            :key="month.value.toString()"
            class="border-collapse select-none"
          >
            <DatePickerGridHead>
              <DatePickerGridRow class="flex">
                <DatePickerHeadCell
                  v-for="day in weekDays"
                  :key="day"
                  class="w-9 rounded-md text-[0.7rem] font-normal capitalize text-muted-foreground"
                >
                  {{ day }}
                </DatePickerHeadCell>
              </DatePickerGridRow>
            </DatePickerGridHead>
            <DatePickerGridBody>
              <DatePickerGridRow
                v-for="(weekDates, index) in month.rows"
                :key="`week-${index}`"
                class="flex w-full"
              >
                <DatePickerCell
                  v-for="weekDate in weekDates"
                  :key="weekDate.toString()"
                  :date="weekDate"
                  class="relative p-0 text-center text-sm"
                >
                  <DatePickerCellTrigger
                    :day="weekDate"
                    :month="month.value"
                    class="inline-flex size-9 items-center justify-center rounded-md p-0 text-sm font-normal tabular-nums transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring data-[selected]:bg-primary data-[selected]:text-primary-foreground data-[selected]:hover:bg-primary data-[today]:bg-accent data-[today]:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:text-muted-foreground/40 data-[outside-view]:text-muted-foreground/40 data-[unavailable]:pointer-events-none data-[unavailable]:line-through"
                  />
                </DatePickerCell>
              </DatePickerGridRow>
            </DatePickerGridBody>
          </DatePickerGrid>
        </div>
      </DatePickerCalendar>
    </DatePickerContent>
  </DatePickerRoot>
</template>
