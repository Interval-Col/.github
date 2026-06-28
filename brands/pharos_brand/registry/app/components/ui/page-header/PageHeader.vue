<script setup lang="ts">
// PageHeader — the standard Pháros page content-header (RFC 0008 component
// library, Phase 1.3). It sits at the TOP of a page's content area, BELOW the
// app-shell breadcrumb. The breadcrumb is the ROUTE title (RFC 0008
// "breadcrumb-as-title"), so PageHeader's title is a section-level heading
// (<h2>, text-xl) — NOT a giant page <h1>. Presentational only, no state.
//
//   <PageHeader title="Pacientes" description="Gestión de admisiones">
//     <template #actions><Button>Nuevo paciente</Button></template>
//     <template #toolbar><SearchableSelect … /></template>
//   </PageHeader>
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

withDefaults(defineProps<{
  /** Section title. Omit and use the #title slot for richer content. */
  title?: string
  /** Muted subtitle line. Omit and use the #description slot. */
  description?: string
  /** Draw a divider under the header to separate it from content. Default: off. */
  bordered?: boolean
  class?: HTMLAttributes['class']
}>(), {
  bordered: false,
})
</script>

<template>
  <div :class="cn('w-full', bordered && 'border-b border-border pb-4', $props.class)">
    <!-- title row: title + description on the left, actions on the right -->
    <div class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between sm:gap-4">
      <div class="min-w-0 space-y-1">
        <h2 class="truncate text-xl font-semibold tracking-tight text-foreground">
          <slot name="title">{{ title }}</slot>
        </h2>
        <p v-if="description || $slots.description" class="text-sm text-muted-foreground">
          <slot name="description">{{ description }}</slot>
        </p>
      </div>
      <div v-if="$slots.actions" class="flex shrink-0 flex-wrap items-center gap-2">
        <slot name="actions" />
      </div>
    </div>

    <!-- optional second row for filters / search / tabs -->
    <div v-if="$slots.toolbar" class="mt-4">
      <slot name="toolbar" />
    </div>
  </div>
</template>
