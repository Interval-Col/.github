<script setup lang="ts">
// UsersRoleTable — the Pháros shared "assign a role to an SSO user" admin table
// (RFC 0016 Phase 4, .github#110). ONE definition so it can't drift across apps.
// Extracted from finance-lch's pages/admin/users.vue. Users authenticate via
// SSO (no local passwords); each username gets a role row; unassigned users fall
// back to the default role.
//
// Self-contained: pass a `pharosAdminApi` instance (app owns transport + base).
// Per-app config = props (the §2b extension points):
//   • adminRoleName — the reserved superuser role (excluded from assignment,
//                     shown as a locked badge). finance/admission `admin`, lab-qc
//                     `administrator`.
//   • defaultRole   — pre-selected when adding a user (finance `viewer`).
//   • currentUsername — for self-protection (can't change/delete your own row);
//                     defaults to the shared pharosAuth session store.
//
//   <UsersRoleTable :api="admin" default-role="viewer" />
import { onMounted, ref, computed } from 'vue'
import { Badge } from '~/components/ui/badge'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '~/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '~/components/ui/table'
import { usePharosAuthStore } from '~/composables/useCan'
import type { PharosAdminApi, PharosRoleCapabilities, PharosUserRole } from '~/lib/pharosAdminApi'

const props = withDefaults(defineProps<{
  api: PharosAdminApi
  adminRoleName?: string
  defaultRole?: string
  currentUsername?: string
}>(), {
  adminRoleName: 'admin',
  defaultRole: 'viewer',
  currentUsername: '',
})

const auth = usePharosAuthStore()
const myUsername = computed(() => props.currentUsername || auth.user?.username || '')

const rows = ref<PharosUserRole[]>([])
const roleDefs = ref<PharosRoleCapabilities[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

// Assignable roles come from the API, so custom roles show up too. The admin
// role is excluded — it's reserved for the bootstrap user and the backend
// rejects assigning it to anyone else.
const roleOptions = computed(() =>
  roleDefs.value
    .filter(r => r.role !== props.adminRoleName)
    .map(r => ({ value: r.role, label: r.label })),
)
const roleLabel = (r: string) => roleDefs.value.find(d => d.role === r)?.label ?? r

const newUsername = ref('')
const newRole = ref<string>(props.defaultRole)
const newNotes = ref('')

async function load() {
  loading.value = true
  error.value = null
  try {
    const [users, defs] = await Promise.all([
      props.api.listUsers(),
      props.api.listRoles(),
    ])
    rows.value = users
    roleDefs.value = defs
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudieron cargar los usuarios.'
  } finally {
    loading.value = false
  }
}

async function add() {
  if (!newUsername.value.trim()) return
  error.value = null
  successMsg.value = null
  try {
    await props.api.createUser({
      username: newUsername.value.trim(),
      role: newRole.value,
      notes: newNotes.value.trim() || null,
    })
    successMsg.value = `Usuario ${newUsername.value} agregado.`
    newUsername.value = ''
    newRole.value = props.defaultRole
    newNotes.value = ''
    await load()
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo agregar el usuario.'
  }
}

async function changeRole(row: PharosUserRole, role: string) {
  if (row.role === role) return
  error.value = null
  successMsg.value = null
  try {
    const updated = await props.api.updateUser(row.username, { role })
    Object.assign(row, updated)
    successMsg.value = `Rol de ${row.username} actualizado a ${roleLabel(role)}.`
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo actualizar el rol.'
  }
}

async function remove(row: PharosUserRole) {
  if (!window.confirm(`¿Eliminar permisos de ${row.username}?`)) return
  error.value = null
  successMsg.value = null
  try {
    await props.api.deleteUser(row.username)
    successMsg.value = `Usuario ${row.username} eliminado.`
    await load()
  } catch (e) {
    error.value = (e as { data?: { detail?: string } })?.data?.detail
      ?? 'No se pudo eliminar el usuario.'
  }
}

onMounted(load)
</script>

<template>
  <div class="flex h-full flex-col">
    <p class="text-muted-foreground mb-6 text-sm shrink-0">
      Asigna roles a usuarios del SSO. Los usuarios sin fila asignada caen
      automáticamente en el rol por defecto.
    </p>

    <section class="bg-card rounded-md p-6 shadow-[var(--shadow-soft)] mb-6 shrink-0">
      <h2 class="text-lg font-semibold text-foreground mb-4">Agregar usuario</h2>
      <div class="flex items-end flex-wrap gap-4">
        <div class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Usuario SSO</label>
          <Input v-model="newUsername" type="text" placeholder="p.ej. juan.perez" class="min-w-[180px]" />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Rol</label>
          <Select v-model="newRole">
            <SelectTrigger class="min-w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="opt in roleOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div class="flex flex-col gap-1.5 flex-1 min-w-[220px]">
          <label class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Notas (opcional)</label>
          <Input v-model="newNotes" type="text" placeholder="p.ej. Contadora externa" class="min-w-[180px]" />
        </div>
        <Button :disabled="!newUsername.trim()" @click="add">
          Agregar
        </Button>
      </div>
    </section>

    <div v-if="error" class="px-4 py-3 rounded-md mb-4 text-sm bg-status-error-bg text-status-error shrink-0">{{ error }}</div>
    <div v-if="successMsg" class="px-4 py-3 rounded-md mb-4 text-sm bg-status-success-bg text-status-success shrink-0">{{ successMsg }}</div>

    <section class="flex min-h-0 flex-1 flex-col">
      <div v-if="loading" class="px-4 py-3 rounded-md mb-4 text-sm">Cargando…</div>
      <div v-else-if="rows.length === 0" class="px-4 py-3 rounded-md mb-4 text-sm">Sin usuarios registrados.</div>
      <div v-else class="min-h-0 overflow-auto rounded-lg border border-border bg-card [&>div]:overflow-visible [&_thead_th]:sticky [&_thead_th]:top-0 [&_thead_th]:z-10 [&_thead_th]:bg-card">
        <Table class="text-sm">
          <TableHeader>
            <TableRow class="bg-background border-b-2 border-b-primary hover:bg-transparent">
              <TableHead class="px-4 py-3 text-xs font-semibold text-foreground uppercase tracking-wide">Usuario</TableHead>
              <TableHead class="px-4 py-3 text-xs font-semibold text-foreground uppercase tracking-wide">Rol</TableHead>
              <TableHead class="px-4 py-3 text-xs font-semibold text-foreground uppercase tracking-wide">Notas</TableHead>
              <TableHead class="px-4 py-3 text-xs font-semibold text-foreground uppercase tracking-wide">Actualizado</TableHead>
              <TableHead class="w-px whitespace-nowrap text-right px-4 py-3"/>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="row in rows" :key="row.id" class="hover:bg-background">
              <TableCell class="px-4 py-2.5 text-foreground font-medium">
                {{ row.username }}
                <Badge v-if="row.username === myUsername" variant="secondary" class="ml-2 px-1.5 py-0.5 text-xs font-semibold uppercase tracking-wide">tú</Badge>
              </TableCell>
              <TableCell class="px-4 py-2.5 text-foreground">
                <span v-if="row.role === adminRoleName" class="font-medium text-foreground">
                  {{ roleLabel(row.role) }}
                  <Badge variant="secondary" class="ml-2 px-1.5 py-0.5 text-xs font-semibold uppercase tracking-wide">reservado</Badge>
                </span>
                <Select
                  v-else
                  :model-value="row.role"
                  :disabled="row.username === myUsername"
                  @update:model-value="(v) => changeRole(row, v as string)"
                >
                  <SelectTrigger
                    class="min-w-[140px]"
                    :title="row.username === myUsername ? 'No puedes cambiar tu propio rol' : ''"
                  >
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem v-for="opt in roleOptions" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </SelectItem>
                  </SelectContent>
                </Select>
              </TableCell>
              <TableCell class="px-4 py-2.5 text-muted-foreground text-sm">{{ row.notes || '—' }}</TableCell>
              <TableCell class="px-4 py-2.5 text-muted-foreground text-sm whitespace-nowrap">{{ new Date(row.updated_at).toLocaleString('es-CO') }}</TableCell>
              <TableCell class="w-px whitespace-nowrap text-right px-4 py-2.5">
                <Button
                  variant="outline"
                  size="icon-sm"
                  class="text-muted-foreground hover:text-destructive hover:border-destructive"
                  :disabled="row.username === myUsername"
                  :title="row.username === myUsername ? 'No puedes eliminar tu propia fila' : 'Eliminar'"
                  @click="remove(row)"
                >🗑</Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </section>
  </div>
</template>
