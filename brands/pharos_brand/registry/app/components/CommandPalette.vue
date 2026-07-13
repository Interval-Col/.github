<script setup lang="ts">
// ⌘K command palette — "search to jump" — built on the vendored reka-ui cmdk
// `command` primitive. Cmd/Ctrl-K toggles it open; the primitive filters the
// flattened nav by `value` as you type (no hand-rolled match logic); Enter on the
// active item navigates; a "toggle theme" action rounds it out.
//
// Decoupled from any app: it takes the SAME nav model the layout already holds as
// a PROP (it does not import `~/navigation/menu`), flattens it to leaves locally,
// and DELEGATES the theme toggle to the layout (emit) so the DOM-class/localStorage
// logic lives in ONE place (the layout) — never duplicated here.
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '~/components/ui/command'
import { isNavSubGroup } from '~/navigation/menu'
import type { NavGroup, NavItem, NavLeaf } from '~/navigation/menu'

defineProps<{ nav: NavGroup[] }>()
const emit = defineEmits<{ (e: 'toggle-theme'): void }>()

// Two root nodes (the trigger button + the teleported dialog) → fallthrough
// attrs can't auto-inherit. Forward them onto the trigger so a consumer's
// `class` (e.g. `hidden md:block`) lands on the button instead of being dropped.
defineOptions({ inheritAttrs: false })

const router = useRouter()
const open = ref(false)

// Recursively collect every NavLeaf from a list of NavItems — handles NavLeaves
// directly nested in a NavGroup *and* NavLeaves nested inside a NavSubGroup.
function collectLeaves(items: NavItem[]): NavLeaf[] {
  return items.flatMap(i => isNavSubGroup(i) ? collectLeaves(i.items) : [i])
}

function onKey(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    open.value = !open.value
  }
}
onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => window.removeEventListener('keydown', onKey))

function go(to: string) {
  router.push(to)
  open.value = false
}
function toggleTheme() {
  emit('toggle-theme')
  open.value = false
}
</script>

<template>
  <!-- Trigger: a search BUTTON living in the topbar. (components/** is exempt from
       the no-raw-html gate, so a native <button>/<kbd> is fine here.) -->
  <button
    v-bind="$attrs"
    type="button"
    class="flex h-9 w-full max-w-sm items-center gap-2 rounded-lg border border-border bg-muted/50 px-3 text-sm text-muted-foreground transition-colors hover:bg-accent"
    @click="open = true"
  >
    <Search class="size-4 shrink-0" aria-hidden="true" />
    <span>Buscar o navegar…</span>
    <kbd class="ml-auto rounded border border-border bg-background px-1.5 py-0.5 font-mono text-[10px]">⌘K</kbd>
  </button>

  <!-- The dialog is teleported by the primitive; CommandDialog supplies the
       sr-only DialogTitle/Description, so a11y is handled. -->
  <CommandDialog v-model:open="open">
    <CommandInput placeholder="Buscar o navegar…" />
    <CommandList>
      <CommandEmpty>Sin resultados</CommandEmpty>
      <template v-for="group in nav" :key="group.label">
        <CommandGroup :heading="group.label">
          <CommandItem
            v-for="leaf in collectLeaves(group.items)"
            :key="leaf.to"
            :value="leaf.label"
            @select="go(leaf.to)"
          >
            {{ leaf.label }}
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
      </template>
      <CommandGroup heading="Acciones">
        <CommandItem value="cambiar tema claro oscuro" @select="toggleTheme">
          Cambiar tema (claro / oscuro)
        </CommandItem>
      </CommandGroup>
    </CommandList>
  </CommandDialog>
</template>
