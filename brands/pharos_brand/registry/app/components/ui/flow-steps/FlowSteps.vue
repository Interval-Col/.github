<script setup lang="ts">
// FlowSteps — presentational step indicator for useFlow (RFC 0008, Phase 2).
// Drive it straight from a useFlow instance: <FlowSteps :steps="flow.steps"
// :current-index="flow.currentIndex" />. Decorative status colours come from the
// accent-independent status palette + the brand accent for the active ring.
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'

interface StepLike {
  key: string
  label: string
  icon?: string
  status: 'pending' | 'active' | 'done' | 'error' | 'skipped'
}

defineProps<{
  steps: StepLike[]
  currentIndex: number
}>()
</script>

<template>
  <ol class="flex w-full items-center gap-2">
    <template v-for="(step, index) in steps" :key="step.key">
      <li class="flex shrink-0 flex-col items-center gap-1">
        <span
          :class="cn(
            'flex size-7 items-center justify-center rounded-full text-xs font-semibold transition-all',
            step.status === 'done' && 'bg-status-success text-white',
            step.status === 'error' && 'bg-destructive text-white',
            step.status === 'skipped' && 'bg-muted text-muted-foreground',
            (step.status === 'pending' || step.status === 'active') && 'bg-muted text-muted-foreground',
            index === currentIndex && 'scale-110 shadow-sm ring-2 ring-primary ring-offset-1 ring-offset-background',
          )"
        >
          <Icon v-if="step.status === 'done'" name="check" :size="4" class="text-white" />
          <Icon v-else-if="step.status === 'error'" name="close" :size="4" class="text-white" />
          <Icon v-else-if="step.icon" :name="step.icon" :size="4" />
          <template v-else>{{ index + 1 }}</template>
        </span>
        <span
          :class="cn(
            'text-xs transition-colors',
            index === currentIndex ? 'font-medium text-primary' : 'text-muted-foreground',
            step.status === 'done' && index !== currentIndex && 'text-foreground',
          )"
        >
          {{ step.label }}
        </span>
      </li>

      <!-- connector -->
      <li
        v-if="index < steps.length - 1"
        aria-hidden="true"
        :class="cn(
          'mb-4 h-0.5 flex-1 rounded transition-colors',
          step.status === 'done' ? 'bg-status-success' : 'bg-muted',
        )"
      />
    </template>
  </ol>
</template>
