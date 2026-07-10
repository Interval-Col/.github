<script setup lang="ts">
// RoleCapabilityMatrix — the Pháros shared role×capability admin grid (RFC 0016
// Phase 4, .github#110). ONE definition of the roles matrix so it can't drift
// finance ↔ lab-qc ↔ admission. Extracted from finance-lch's pages/admin/roles.vue.
//
// Self-contained: give it a `pharosAdminApi` instance (the app owns transport +
// base — like SearchableSelect's searchFn) and it loads capabilities + roles,
// runs the per-role draft/dirty/save buffer, and (when customRolesEnabled)
// create/rename/delete custom roles. The admin role is hard-locked read-only.
//
// Per-app config = props (the §2b extension points), so no fork:
//   • adminRoleName      — the superuser role name (finance/admission `admin`,
//                          lab-qc `administrator`). Locked to all-granted, read-only.
//   • customRolesEnabled — finance ON (create/rename/delete roles); closed-set
//                          apps (lab-qc/admission) OFF → only the matrix is editable.
//
//   <RoleCapabilityMatrix :api="admin" :custom-roles-enabled="true" />
import { computed, onMounted, reactive, ref } from 'vue'
import { ChevronRightIcon } from 'lucide-vue-next'
import { Badge } from '~/components/ui/badge'
import { Button } from '~/components/ui/button'
import { Checkbox } from '~/components/ui/checkbox'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '~/components/ui/collapsible'
import { Input } from '~/components/ui/input'
import type { PharosAdminApi, PharosCapability, PharosRoleCapabilities } from '~/lib/pharosAdminApi'

const props = withDefaults(defineProps<{
  api: PharosAdminApi
  adminRoleName?: string
  customRolesEnabled?: boolean
}>(), {
  adminRoleName: 'admin',
  customRolesEnabled: false,
})

const capabilities = ref<PharosCapability[]>([])
const roles = ref<PharosRoleCapabilities[]>([])
// Local edit buffer: role -> Set<capability_id>. Mirrors `roles` until the user
// clicks Guardar; that way toggles feel instant.
const drafts = ref<Record<string, Set<string>>>({})
const dirty = ref<Record<string, boolean>>({})
const saving = ref<Record<string, boolean>>({})
const loading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

// Group capabilities by area for a readable matrix.
const groupedCaps = computed(() => {
  const groups = new Map<string, PharosCapability[]>()
  for (const c of capabilities.value) {
    if (!groups.has(c.area)) groups.set(c.area, [])
    groups.get(c.area)!.push(c)
  }
  return [...groups.entries()].map(([area, caps]) => ({ area, caps }))
})

// ── Estado de los desplegables (rol + grupo), colapsados por defecto ──────────
const roleOpen = reactive<Record<string, boolean>>({})
const groupOpen = reactive<Record<string, boolean>>({})
const groupKey = (role: string, area: string) => `${role}::${area}`

function groupGranted(role: string, caps: PharosCapability[]): number {
  return isReadonly(role) ? caps.length : caps.filter(c => isChecked(role, c.id)).length
}
function roleGranted(role: PharosRoleCapabilities): number {
  return isReadonly(role.role) ? capabilities.value.length : (drafts.value[role.role]?.size ?? 0)
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const [caps, rls] = await Promise.all([
      props.api.listCapabilities(),
      props.api.listRoles(),
    ])
    capabilities.value = caps
    roles.value = rls
    drafts.value = Object.fromEntries(rls.map(r => [r.role, new Set(r.capabilities)]))
    dirty.value = Object.fromEntries(rls.map(r => [r.role, false]))
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudieron cargar los datos.'
  } finally {
    loading.value = false
  }
}

function isChecked(role: string, capId: string): boolean {
  return drafts.value[role]?.has(capId) ?? false
}

// The admin role is locked at the API level — its checkboxes always reflect
// "everything granted" and can't be toggled.
function isReadonly(role: string): boolean {
  return role === props.adminRoleName
}

function toggle(role: string, capId: string) {
  if (isReadonly(role)) return
  const set = new Set(drafts.value[role] ?? [])
  if (set.has(capId)) set.delete(capId); else set.add(capId)
  drafts.value = { ...drafts.value, [role]: set }
  dirty.value = { ...dirty.value, [role]: true }
  successMsg.value = null
}

function labelOf(roleName: string): string {
  return roles.value.find(r => r.role === roleName)?.label ?? roleName
}

async function save(role: string) {
  if (isReadonly(role) || !dirty.value[role]) return
  saving.value = { ...saving.value, [role]: true }
  error.value = null
  successMsg.value = null
  try {
    const updated = await props.api.setRoleCapabilities(role, {
      capabilities: [...(drafts.value[role] ?? [])],
    })
    const idx = roles.value.findIndex(r => r.role === role)
    if (idx >= 0) roles.value[idx] = updated
    drafts.value[role] = new Set(updated.capabilities)
    dirty.value[role] = false
    successMsg.value = `Permisos de ${labelOf(role)} guardados.`
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo guardar el rol.'
  } finally {
    saving.value[role] = false
  }
}

function discard(role: string) {
  const original = roles.value.find(r => r.role === role)
  if (!original) return
  drafts.value = { ...drafts.value, [role]: new Set(original.capabilities) }
  dirty.value = { ...dirty.value, [role]: false }
  successMsg.value = null
}

// ── Crear rol personalizado (solo si customRolesEnabled) ──────────────────────
const newName = ref('')
const newLabel = ref('')
const newDesc = ref('')
const creating = ref(false)

async function createRole() {
  const name = newName.value.trim().toLowerCase()
  const label = newLabel.value.trim()
  if (!name || !label) return
  creating.value = true
  error.value = null
  successMsg.value = null
  try {
    await props.api.createRole({ name, label, description: newDesc.value.trim() || undefined })
    newName.value = ''
    newLabel.value = ''
    newDesc.value = ''
    successMsg.value = `Rol «${label}» creado.`
    await load()
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo crear el rol.'
  } finally {
    creating.value = false
  }
}

// ── Editar nombre visible + descripción (el slug es fijo) ─────────────────────
const editing = ref<string | null>(null)
const editLabel = ref('')
const editDesc = ref('')
const savingEdit = ref(false)

function startEdit(role: PharosRoleCapabilities) {
  editing.value = role.role
  editLabel.value = role.label
  editDesc.value = role.description
  error.value = null
  successMsg.value = null
}
function cancelEdit() {
  editing.value = null
}

async function saveEdit(roleName: string) {
  const label = editLabel.value.trim()
  if (!label) return
  savingEdit.value = true
  error.value = null
  try {
    const updated = await props.api.editRole(roleName, {
      label,
      description: editDesc.value.trim(),
    })
    const idx = roles.value.findIndex(r => r.role === roleName)
    if (idx >= 0) roles.value[idx] = updated
    editing.value = null
    successMsg.value = `Rol «${label}» actualizado.`
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo actualizar el rol.'
  } finally {
    savingEdit.value = false
  }
}

// ── Eliminar rol personalizado (solo si customRolesEnabled) ───────────────────
async function removeRole(role: PharosRoleCapabilities) {
  if (!window.confirm(`¿Eliminar el rol «${role.label}»? Esta acción no se puede deshacer.`)) return
  error.value = null
  successMsg.value = null
  try {
    await props.api.deleteRole(role.role)
    successMsg.value = `Rol «${role.label}» eliminado.`
    await load()
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo eliminar el rol.'
  }
}

onMounted(load)
</script>

<template>
  <div>
    <p class="text-muted-foreground mb-6 text-sm">
      Marca o desmarca permisos para cada rol. El rol de administrador siempre
      tiene todos los permisos y no se puede editar. Los cambios de permisos se
      aplican al guardar.
    </p>

    <!-- Crear rol personalizado -->
    <section
      v-if="customRolesEnabled"
      class="bg-card rounded-md p-6 shadow-[var(--shadow-soft)] mb-6 border border-border"
    >
      <h2 class="text-lg font-semibold text-foreground mb-1">Crear rol</h2>
      <p class="text-muted-foreground mb-4 text-sm">
        Define un rol personalizado. El <strong>identificador</strong> es un texto
        corto en minúsculas que no cambia (p.ej. <span class="font-mono">auditor_externo</span>);
        el nombre visible y la descripción se muestran en la interfaz.
      </p>
      <div class="flex items-end flex-wrap gap-4">
        <div class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Identificador</label>
          <Input v-model="newName" type="text" placeholder="p.ej. auditor_externo" class="min-w-[180px]" />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Nombre visible</label>
          <Input v-model="newLabel" type="text" placeholder="p.ej. Auditor externo" class="min-w-[180px]" />
        </div>
        <div class="flex flex-col gap-1.5 flex-1 min-w-[220px]">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Descripción (opcional)</label>
          <Input v-model="newDesc" type="text" placeholder="p.ej. Acceso de auditoría de solo lectura" class="min-w-[180px]" />
        </div>
        <Button :disabled="!newName.trim() || !newLabel.trim() || creating" @click="createRole">
          {{ creating ? 'Creando…' : 'Crear' }}
        </Button>
      </div>
    </section>

    <div v-if="loading" class="px-4 py-3 rounded-md mb-4 text-sm">Cargando…</div>
    <div v-if="error" class="px-4 py-3 rounded-md mb-4 text-sm bg-status-error-bg text-status-error">{{ error }}</div>
    <div v-if="successMsg" class="px-4 py-3 rounded-md mb-4 text-sm bg-status-success-bg text-status-success">{{ successMsg }}</div>

    <!-- Un desplegable por rol; dentro, un desplegable por grupo de permisos. -->
    <Collapsible
      v-for="role in roles"
      :key="role.role"
      v-model:open="roleOpen[role.role]"
      class="mb-4 rounded-lg border border-border bg-card shadow-sm"
      :class="{ 'opacity-85': role.is_admin }"
    >
      <div class="flex items-start justify-between gap-4 px-6 py-4">
        <CollapsibleTrigger class="group flex flex-1 items-start gap-2.5 text-left min-w-0">
          <ChevronRightIcon class="mt-1 size-4 shrink-0 text-muted-foreground transition-transform duration-200 group-data-[state=open]:rotate-90" />
          <div class="min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <h2 class="m-0 text-lg font-semibold text-foreground">{{ role.label }}</h2>
              <span class="text-xs font-medium text-muted-foreground">· {{ roleGranted(role) }} permisos</span>
              <Badge v-if="role.is_system" variant="secondary" class="border-transparent bg-muted text-muted-foreground uppercase tracking-wide">Sistema</Badge>
            </div>
            <p v-if="role.description" class="mt-0.5 text-xs text-muted-foreground">{{ role.description }}</p>
          </div>
        </CollapsibleTrigger>
        <div class="flex shrink-0 items-center gap-2">
          <Button v-if="customRolesEnabled" variant="ghost" size="sm" @click="startEdit(role)">Editar</Button>
          <Button
            v-if="customRolesEnabled && !role.is_system"
            variant="ghost"
            size="sm"
            class="text-muted-foreground hover:text-destructive"
            @click="removeRole(role)"
          >Eliminar</Button>
          <Badge v-if="role.is_admin" variant="secondary" class="border-transparent bg-muted text-muted-foreground uppercase tracking-wide">Sólo lectura</Badge>
          <template v-else>
            <Button
              variant="outline"
              size="sm"
              :disabled="!dirty[role.role] || saving[role.role]"
              @click="discard(role.role)"
            >Descartar</Button>
            <Button
              size="sm"
              :disabled="!dirty[role.role] || saving[role.role]"
              @click="save(role.role)"
            >{{ saving[role.role] ? 'Guardando…' : 'Guardar' }}</Button>
          </template>
        </div>
      </div>

      <!-- Panel de edición del nombre visible + descripción -->
      <div v-if="customRolesEnabled && editing === role.role" class="border-t border-border bg-muted/30 px-6 py-4">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-end">
          <div class="flex flex-1 flex-col gap-1.5">
            <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Nombre visible</label>
            <Input v-model="editLabel" type="text" />
          </div>
          <div class="flex flex-1 flex-col gap-1.5">
            <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Descripción</label>
            <Input v-model="editDesc" type="text" />
          </div>
          <div class="flex gap-2">
            <Button variant="outline" size="sm" :disabled="savingEdit" @click="cancelEdit">Cancelar</Button>
            <Button size="sm" :disabled="savingEdit || !editLabel.trim()" @click="saveEdit(role.role)">
              {{ savingEdit ? 'Guardando…' : 'Guardar' }}
            </Button>
          </div>
        </div>
        <p class="mt-2 text-xs text-muted-foreground">
          El identificador interno (<span class="font-mono">{{ role.role }}</span>) no cambia.
        </p>
      </div>

      <CollapsibleContent class="px-6 pb-5">
        <div class="grid grid-cols-1 items-start gap-x-5 gap-y-3 sm:grid-cols-2 lg:grid-cols-3">
          <Collapsible
            v-for="g in groupedCaps"
            :key="g.area"
            v-model:open="groupOpen[groupKey(role.role, g.area)]"
            class="rounded-md border border-border/60"
          >
            <CollapsibleTrigger class="group flex w-full items-center justify-between gap-2 rounded-md px-2.5 py-2 text-left transition-colors hover:bg-muted/50">
              <span class="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wide text-muted-foreground">
                <ChevronRightIcon class="size-3 shrink-0 transition-transform duration-200 group-data-[state=open]:rotate-90" />
                {{ g.area }}
              </span>
              <span class="shrink-0 text-xs tabular-nums text-muted-foreground">{{ groupGranted(role.role, g.caps) }}/{{ g.caps.length }}</span>
            </CollapsibleTrigger>
            <CollapsibleContent class="px-2.5 pb-2">
              <!-- .prevent is load-bearing: the row is a label wrapping a reka-ui
                   Checkbox; without it a single click fires toggle() twice (real
                   click + the label→control synthetic click) and they cancel out. -->
              <label
                v-for="cap in g.caps"
                :key="cap.id"
                class="grid grid-cols-[auto_1fr_auto] items-center gap-2 py-1.5 text-sm text-foreground"
                :class="isReadonly(role.role) ? 'cursor-default' : 'cursor-pointer'"
                @click.prevent="toggle(role.role, cap.id)"
              >
                <Checkbox
                  tabindex="-1"
                  class="pointer-events-none"
                  :model-value="role.is_admin ? true : isChecked(role.role, cap.id)"
                  :disabled="isReadonly(role.role)"
                />
                <span class="text-foreground">{{ cap.label }}</span>
                <span class="text-muted-foreground text-xs font-mono">{{ cap.id }}</span>
              </label>
            </CollapsibleContent>
          </Collapsible>
        </div>
      </CollapsibleContent>
    </Collapsible>
  </div>
</template>
