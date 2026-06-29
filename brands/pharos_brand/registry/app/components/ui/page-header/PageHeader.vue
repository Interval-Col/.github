<script setup lang="ts">
// PageHeader — the standard Pháros page content-header (RFC 0008 component
// library, Phase 1.3). It sits at the TOP of a page's content area, BELOW the
// app-shell breadcrumb. The breadcrumb is THE page title (RFC 0008
// "breadcrumb-as-title"), so PageHeader's `title` is OPTIONAL and, when used, a
// section-level heading (<h2>, text-xl) — never repeat the breadcrumb's page
// name here (DRY). Most pages use PageHeader title-LESS: just the #actions row
// and/or a #toolbar (filters/lookup), optionally a #description subtitle. The
// header collapses to zero height when it has nothing to show, so a title-less
// PageHeader costs no vertical space. Presentational only, no state.
//
//   <!-- title-less: actions + toolbar only (the common case) -->
//   <PageHeader>
//     <template #actions><Button>Nuevo paciente</Button></template>
//     <template #toolbar><SearchableSelect … /></template>
//   </PageHeader>
//
//   <!-- with a section heading (only when it is NOT the page name) -->
//   <PageHeader title="Resumen del día" description="…" />
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

withDefaults(defineProps<{
  /** Optional section title. OMIT on most pages — the breadcrumb is the page
   *  title. Use only for a section heading that is NOT the page name. */
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
    <!-- title row: title + description on the left, actions on the right. Renders
         only when there's something to show — a title-less PageHeader (actions/
         toolbar only) takes no extra vertical space. -->
    <div
      v-if="title || $slots.title || description || $slots.description || $slots.actions"
      class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between sm:gap-4"
    >
      <div v-if="title || $slots.title || description || $slots.description" class="min-w-0 space-y-1">
        <h2 v-if="title || $slots.title" class="truncate text-xl font-semibold tracking-tight text-foreground">
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

    <!-- optional second row for filters / search / tabs. mt-4 only when a row
         rendered above (so a toolbar-only header has no leading gap). -->
    <div
      v-if="$slots.toolbar"
      :class="(title || $slots.title || description || $slots.description || $slots.actions) ? 'mt-4' : ''"
    >
      <slot name="toolbar" />
    </div>
  </div>
</template>
