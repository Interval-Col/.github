<script setup lang="ts">
// ════════════════════════════════════════════════════════════════════════════
// Pháros "Faro + Instrumento" app shell — the canonical, app-AGNOSTIC layout.
//
// Decoupling (RFC 0008 app-shell, non-negotiable):
//  • Nav comes from the app via `~/navigation/menu` (the documented contract:
//    groups → items, item = {to,label,icon?}, one optional sub-group level). No
//    app route is hard-coded here; the shell walks whatever tree the app exports.
//  • i18n-free: nav items carry a literal `label`; the breadcrumb + ⌘K use it
//    directly (the app localizes its nav model before handing it over).
//  • No auth coupling: the user/footer block + sign-out are injected by the app
//    via <slot name="user"/>; app-specific topbar extras via <slot name="topbar-end"/>.
//  • Self-contained theme: the .dark class + localStorage('pharos-theme') + a
//    Sun/Moon toggle. The ⌘K palette delegates its "toggle theme" action back here
//    so the DOM/localStorage logic lives in ONE place.
//  • Breadcrumb-as-title (NO page <h1>): derived purely from the route + nav model;
//    non-final crumbs are dropdowns of siblings, the last segment is the bold page.
//  • Beacon spine is the DEFAULT and only treatment (the lit-rail CSS lives in
//    pharos-components.css, keyed to data-pg-sidebar — no runtime spine toggle).
//  • <html data-status> is owned by the health-beacon.client.ts plugin; this
//    layout never touches it. <SystemBeacon/> reads it; the pilot dot animates off it.
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronDown, Moon, Sun } from 'lucide-vue-next'
import * as lucide from 'lucide-vue-next'
import type { Component } from 'vue'

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarProvider,
  SidebarTrigger,
} from '~/components/ui/sidebar'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '~/components/ui/collapsible'
import { Popover, PopoverContent, PopoverTrigger } from '~/components/ui/popover'
import { Button } from '~/components/ui/button'

import AppLogo from '~/components/AppLogo.vue'
import CommandPalette from '~/components/CommandPalette.vue'
import SystemBeacon from '~/components/SystemBeacon.vue'

import { isNavSubGroup, menu } from '~/navigation/menu'
import type { NavGroup, NavItem, NavLeaf } from '~/navigation/menu'

// ── App lockup props (the app sets these in app.vue via <NuxtLayout> or here) ──
// Exposed as layout props so an app picks its sub-brand without forking the shell.
withDefaults(defineProps<{
  /** Sub-brand name shown beside the wordmark, e.g. "Clínico". */
  subName?: string
  /** A lucide icon name for the sub-brand glyph, e.g. "Radar". */
  glyph?: string
}>(), { glyph: 'Radar' })

const route = useRoute()
const isSidebarOpen = ref(true)

// ── Theme (self-contained, single source of truth) ───────────────────────────
const themeMode = ref<'light' | 'dark'>('light')
function toggleTheme() {
  const next: 'light' | 'dark' = themeMode.value === 'dark' ? 'light' : 'dark'
  document.documentElement.classList.toggle('dark', next === 'dark')
  localStorage.setItem('pharos-theme', next)
  themeMode.value = next
}

// ── Per-group open state (pharos-lis pattern) ────────────────────────────────
// All groups start collapsed; when the rail itself collapses to icon-only, every
// group resets to closed so the next open gives a clean tree.
const groupOpenStates = ref<Record<string, boolean>>(
  Object.fromEntries(menu.map(g => [g.label, false])),
)
watch(isSidebarOpen, (open) => {
  if (!open) {
    for (const key of Object.keys(groupOpenStates.value)) groupOpenStates.value[key] = false
  }
})
function openSidebarIfCollapsed() {
  if (!isSidebarOpen.value) isSidebarOpen.value = true
}

// ── Icon resolution: a nav icon may be a lucide component OR a name string ────
function resolveIcon(icon?: Component | string): Component | null {
  if (!icon) return null
  if (typeof icon === 'string') return (lucide as Record<string, Component>)[icon] ?? null
  return icon
}

// ════════════════════════════════════════════════════════════════════════════
// Breadcrumb-as-title — derived purely from route.path + the nav model.
// Ports pharos-lis's ancestry/parent-only-dropdown rule onto the literal-label
// simple nav contract (no i18n). Implemented INSIDE the layout so the shell needs
// only the documented {groups→items, leaf, sub-group} shape — no app-side helpers.
// ════════════════════════════════════════════════════════════════════════════

type Ancestry = { group: NavGroup; subGroup?: NavItem & { items: NavLeaf[] }; leaf: NavLeaf }

function findAncestry(path: string): Ancestry | null {
  for (const group of menu) {
    for (const entry of group.items) {
      if (isNavSubGroup(entry)) {
        for (const leaf of entry.items) {
          if (leaf.to === path) return { group, subGroup: entry, leaf }
        }
      } else if ((entry as NavLeaf).to === path) {
        return { group, leaf: entry as NavLeaf }
      }
    }
  }
  return null
}

/** First navigable leaf inside a group (for the fallback label-casing only). */
function lastSlugLabel(path: string): string {
  const slug = path.split('/').filter(Boolean).pop() ?? 'Inicio'
  return slug
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}

type Crumb =
  // Section above an existing sub-group → plain orientation text (no dropdown,
  // so it does not duplicate the sub-group's dropdown).
  | { kind: 'section-static'; label: string }
  // Section IS the immediate parent (no sub-group) → dropdown of its children.
  | { kind: 'section-parent'; label: string; group: NavGroup }
  // Sub-group is always the immediate parent when present → dropdown of its leaves.
  | { kind: 'subgroup'; label: string; leaves: NavLeaf[] }
  // Current page → bold, aria-current, no dropdown.
  | { kind: 'current'; label: string }

const crumbs = computed<Crumb[]>(() => {
  const a = findAncestry(route.path)
  if (!a) {
    const title = typeof route.meta.title === 'string' ? route.meta.title : lastSlugLabel(route.path)
    return [{ kind: 'current', label: title }]
  }
  const segs: Crumb[] = []
  // Parent-only-dropdown rule: only the immediate parent gets a dropdown.
  if (a.subGroup) {
    segs.push({ kind: 'section-static', label: a.group.label })
    segs.push({ kind: 'subgroup', label: a.subGroup.label, leaves: a.subGroup.items })
  } else {
    segs.push({ kind: 'section-parent', label: a.group.label, group: a.group })
  }
  segs.push({ kind: 'current', label: a.leaf.label })
  return segs
})

onMounted(() => {
  // Sync with whatever an FOUC head-script already applied to <html>.
  themeMode.value = document.documentElement.classList.contains('dark') ? 'dark' : 'light'
})
</script>

<template>
  <SidebarProvider
    v-model:open="isSidebarOpen"
    class="min-h-screen bg-background text-foreground"
  >
    <!-- ── Sidebar: the lit lighthouse beam (beacon rail CSS keys off data-pg-sidebar) ── -->
    <Sidebar collapsible="icon" data-pg-sidebar>
      <SidebarHeader class="min-h-16 justify-center group-data-[collapsible=icon]:items-center group-data-[state=expanded]:flex-row group-data-[state=expanded]:items-center group-data-[state=expanded]:gap-2 group-data-[state=expanded]:px-3">
        <!-- Lockup row: AppLogo wordmark + (expanded & subName) the "· glyph subName"
             sub-brand composition. font-heading so the "·" + name read as one mark. -->
        <AppLogo :variant="isSidebarOpen ? 'navbar' : 'icon'" />
        <span
          v-if="isSidebarOpen && subName"
          class="flex items-center gap-1.5 font-display text-lg text-muted-foreground group-data-[collapsible=icon]:hidden"
        >
          <span aria-hidden="true">·</span>
          <component :is="resolveIcon(glyph)" v-if="resolveIcon(glyph)" class="size-5" :stroke-width="1.75" aria-hidden="true" />
          {{ subName }}
        </span>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <template v-for="group in menu" :key="group.label">
                <!-- Group is expandable (has items) → Collapsible header + nested sub. -->
                <Collapsible
                  v-model:open="groupOpenStates[group.label]"
                  as-child
                  class="group/collapsible"
                >
                  <SidebarMenuItem>
                    <CollapsibleTrigger as-child>
                      <SidebarMenuButton :tooltip="group.label" @click="openSidebarIfCollapsed">
                        <component :is="resolveIcon(group.icon)" v-if="resolveIcon(group.icon)" aria-hidden="true" />
                        <span>{{ group.label }}</span>
                        <ChevronDown
                          class="ml-auto h-3.5 w-3.5 transition-transform group-data-[state=closed]/collapsible:-rotate-90"
                          aria-hidden="true"
                        />
                      </SidebarMenuButton>
                    </CollapsibleTrigger>
                    <CollapsibleContent>
                      <SidebarMenuSub>
                        <template
                          v-for="entry in group.items"
                          :key="isNavSubGroup(entry) ? entry.label : (entry as NavLeaf).to"
                        >
                          <!-- Sub-group: small label + nested leaves. -->
                          <template v-if="isNavSubGroup(entry)">
                            <li class="px-2 pb-0.5 pt-2 text-[0.7rem] uppercase tracking-wider text-sidebar-foreground/50">
                              {{ entry.label }}
                            </li>
                            <SidebarMenuSubItem v-for="leaf in entry.items" :key="leaf.to">
                              <SidebarMenuSubButton as-child :is-active="route.path === leaf.to">
                                <NuxtLink :to="leaf.to">
                                  <span>{{ leaf.label }}</span>
                                </NuxtLink>
                              </SidebarMenuSubButton>
                            </SidebarMenuSubItem>
                          </template>

                          <!-- Direct leaf. -->
                          <SidebarMenuSubItem v-else>
                            <SidebarMenuSubButton as-child :is-active="route.path === (entry as NavLeaf).to">
                              <NuxtLink :to="(entry as NavLeaf).to">
                                <span>{{ (entry as NavLeaf).label }}</span>
                              </NuxtLink>
                            </SidebarMenuSubButton>
                          </SidebarMenuSubItem>
                        </template>
                      </SidebarMenuSub>
                    </CollapsibleContent>
                  </SidebarMenuItem>
                </Collapsible>
              </template>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <!-- Auth/user block injected by the app (NO SidebarUser/MakerCredit/SidebarOcean). -->
      <SidebarFooter>
        <slot name="user" />
      </SidebarFooter>
    </Sidebar>

    <!-- ── Main area: topbar + content ── -->
    <SidebarInset class="flex h-svh flex-col overflow-hidden">
      <header data-pg-topbar class="flex h-14 items-center gap-3 border-b border-border bg-card px-4">
        <SidebarTrigger />
        <span class="h-5 w-px bg-border" aria-hidden="true" />

        <!-- Breadcrumb-as-title: non-final crumbs are sibling dropdowns, the last
             segment is the bold current page. NO <h1> anywhere. -->
        <nav aria-label="Breadcrumb" class="flex min-w-0 flex-wrap items-center gap-1.5 text-[0.95rem]">
          <ol class="inline-flex min-w-0 flex-wrap items-center gap-1.5">
            <li
              v-for="(seg, i) in crumbs"
              :key="`${seg.kind}-${seg.label}-${i}`"
              class="inline-flex items-center gap-1.5"
            >
              <span v-if="i > 0" class="text-muted-foreground" aria-hidden="true">/</span>

              <!-- Section above a sub-group → plain orientation text. -->
              <span v-if="seg.kind === 'section-static'" class="text-muted-foreground">
                {{ seg.label }}
              </span>

              <!-- Section is the immediate parent → dropdown of its children. -->
              <Popover v-else-if="seg.kind === 'section-parent'">
                <PopoverTrigger
                  class="inline-flex cursor-pointer items-center gap-1 text-muted-foreground outline-none transition-colors hover:text-foreground focus-visible:underline underline-offset-4"
                >
                  {{ seg.label }}
                  <ChevronDown class="h-3.5 w-3.5" aria-hidden="true" />
                </PopoverTrigger>
                <PopoverContent align="start" class="w-64 p-1">
                  <ul class="flex flex-col gap-0.5">
                    <template
                      v-for="entry in seg.group.items"
                      :key="isNavSubGroup(entry) ? entry.label : (entry as NavLeaf).to"
                    >
                      <template v-if="isNavSubGroup(entry)">
                        <li class="px-2 pb-0.5 pt-1.5 text-[0.7rem] uppercase tracking-wider text-muted-foreground/70">
                          {{ entry.label }}
                        </li>
                        <li v-for="leaf in entry.items" :key="leaf.to">
                          <NuxtLink
                            :to="leaf.to"
                            class="block rounded-sm px-3 py-1.5 text-[0.875rem] transition-colors hover:bg-accent hover:text-accent-foreground"
                            :class="route.path === leaf.to ? 'bg-accent/50 font-medium text-foreground' : 'text-muted-foreground'"
                          >
                            {{ leaf.label }}
                          </NuxtLink>
                        </li>
                      </template>
                      <li v-else>
                        <NuxtLink
                          :to="(entry as NavLeaf).to"
                          class="block rounded-sm px-2 py-1.5 text-[0.875rem] transition-colors hover:bg-accent hover:text-accent-foreground"
                          :class="route.path === (entry as NavLeaf).to ? 'bg-accent/50 font-medium text-foreground' : 'text-muted-foreground'"
                        >
                          {{ (entry as NavLeaf).label }}
                        </NuxtLink>
                      </li>
                    </template>
                  </ul>
                </PopoverContent>
              </Popover>

              <!-- Sub-group → dropdown of just its leaves. -->
              <Popover v-else-if="seg.kind === 'subgroup'">
                <PopoverTrigger
                  class="inline-flex cursor-pointer items-center gap-1 text-muted-foreground outline-none transition-colors hover:text-foreground focus-visible:underline underline-offset-4"
                >
                  {{ seg.label }}
                  <ChevronDown class="h-3.5 w-3.5" aria-hidden="true" />
                </PopoverTrigger>
                <PopoverContent align="start" class="w-56 p-1">
                  <ul class="flex flex-col gap-0.5">
                    <li v-for="leaf in seg.leaves" :key="leaf.to">
                      <NuxtLink
                        :to="leaf.to"
                        class="block rounded-sm px-2 py-1.5 text-[0.875rem] transition-colors hover:bg-accent hover:text-accent-foreground"
                        :class="route.path === leaf.to ? 'bg-accent/50 font-medium text-foreground' : 'text-muted-foreground'"
                      >
                        {{ leaf.label }}
                      </NuxtLink>
                    </li>
                  </ul>
                </PopoverContent>
              </Popover>

              <!-- Current page → bold, no dropdown. -->
              <span v-else class="truncate font-semibold text-foreground" aria-current="page">
                {{ seg.label }}
              </span>
            </li>
          </ol>
        </nav>

        <!-- Right cluster — spec order: spacer · ⌘K · SystemBeacon · theme · user. -->
        <div class="ml-auto flex items-center gap-3">
          <CommandPalette class="hidden md:block" :nav="menu" @toggle-theme="toggleTheme" />
          <slot name="topbar-end" />
          <SystemBeacon />
          <Button
            type="button"
            variant="outline"
            size="icon"
            class="rounded-full"
            :aria-label="themeMode === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro'"
            @click="toggleTheme"
          >
            <Sun v-if="themeMode === 'dark'" class="size-[18px]" aria-hidden="true" />
            <Moon v-else class="size-[18px]" aria-hidden="true" />
          </Button>
          <slot name="user-topbar" />
        </div>
      </header>

      <!-- Page content. NO <h1> (breadcrumb is the title), NO playground panel/letterbox. -->
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </SidebarInset>
  </SidebarProvider>
</template>
