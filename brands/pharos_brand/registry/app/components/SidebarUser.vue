<script setup lang="ts">
// User / session block — the designed default that drops into the shell's
// <slot name="user"> (sidebar footer) or #user-topbar. The app supplies the live
// session via props (name/role/email/initials) and wires the actions via emits;
// the brand treatment (avatar, accent-INDEPENDENT status dot, name+role, the
// ChevronsUpDown popover) is owned here so every app looks the same.
//
// Decoupled copy-in: no auth/store coupling — props in, events out.
import { computed } from 'vue'
import { ChevronsUpDown, LogOut, UserRound, Settings } from 'lucide-vue-next'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'
import { useSidebar } from '~/components/ui/sidebar'

const props = withDefaults(defineProps<{
  /** "sidebar" → full block collapsing to the avatar on the icon rail; "navbar" → compact topbar pill. */
  variant?: 'sidebar' | 'navbar'
  name: string
  role?: string
  email?: string
  initials: string
  /** Connection state → the accent-independent status dot. */
  status?: 'ok' | 'drift' | 'out'
  /** Show the Perfil / Preferencias menu rows (wire via @profile / @preferences). */
  showMenu?: boolean
}>(), { variant: 'sidebar', role: '', email: '', status: 'ok', showMenu: true })

const emit = defineEmits<{ 'sign-out': [], profile: [], preferences: [] }>()

const { state } = useSidebar()
const showText = computed(() => props.variant === 'navbar' || state.value === 'expanded')
const menuAlign = computed(() => (props.variant === 'navbar' ? 'end' : 'end'))
const dotClass = computed(() => ({ ok: 'bg-status-success', drift: 'bg-status-warning', out: 'bg-status-error' }[props.status]))
</script>

<template>
  <Popover>
    <PopoverTrigger
      :class="[
        'flex items-center gap-2 rounded-md text-left outline-none transition-colors focus-visible:ring-2 focus-visible:ring-sidebar-ring',
        variant === 'navbar' ? 'h-9 px-1.5 hover:bg-accent' : 'w-full p-1.5 hover:bg-sidebar-accent',
        variant === 'sidebar' && state === 'collapsed' ? 'justify-center' : '',
      ]"
    >
      <span class="relative inline-flex size-8 shrink-0 items-center justify-center rounded-md bg-sidebar-primary font-mono text-xs font-medium text-sidebar-primary-foreground">
        {{ initials }}
        <span
          class="absolute -bottom-0.5 -right-0.5 size-2.5 rounded-full border-2"
          :class="[dotClass, variant === 'navbar' ? 'border-card' : 'border-sidebar']"
          title="Conectada"
        />
      </span>
      <span v-if="showText" class="min-w-0" :class="variant === 'navbar' ? 'hidden flex-1 lg:block' : 'flex-1'">
        <span class="block truncate text-sm font-medium leading-tight" :class="variant === 'navbar' ? 'text-foreground' : 'text-sidebar-foreground'">{{ name }}</span>
        <span v-if="role" class="block truncate text-xs leading-tight text-muted-foreground">{{ role }}</span>
      </span>
      <ChevronsUpDown v-if="showText" class="size-4 shrink-0 text-muted-foreground" :class="variant === 'navbar' ? 'hidden lg:block' : ''" />
    </PopoverTrigger>

    <PopoverContent :align="menuAlign" :side="variant === 'navbar' ? 'bottom' : 'right'" :side-offset="8" class="w-60 p-1">
      <div class="flex items-center gap-2 border-b border-border px-2 py-2">
        <span class="inline-flex size-8 shrink-0 items-center justify-center rounded-md bg-sidebar-primary font-mono text-xs text-sidebar-primary-foreground">{{ initials }}</span>
        <div class="min-w-0">
          <div class="truncate text-sm font-medium">{{ name }}</div>
          <div v-if="email" class="truncate text-xs text-muted-foreground">{{ email }}</div>
        </div>
      </div>
      <div class="flex items-center gap-1.5 px-2 py-1.5 font-mono text-[11px] uppercase tracking-wide text-status-success">
        <span class="size-1.5 rounded-full bg-status-success" /> Conectada
      </div>
      <div class="my-1 h-px bg-border" />
      <template v-if="showMenu">
        <button type="button" class="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors hover:bg-accent" @click="emit('profile')"><UserRound class="size-4" /> Perfil</button>
        <button type="button" class="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm transition-colors hover:bg-accent" @click="emit('preferences')"><Settings class="size-4" /> Preferencias</button>
      </template>
      <button type="button" class="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm text-destructive transition-colors hover:bg-accent" @click="emit('sign-out')"><LogOut class="size-4" /> Cerrar sesión</button>
    </PopoverContent>
  </Popover>
</template>
