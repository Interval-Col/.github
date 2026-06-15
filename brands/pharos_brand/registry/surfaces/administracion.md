---
description: "Use when creating components or pages for the Pháros Administración surface — the cross-cutting administrative console (user/role management, system configuration, multi-app status overview). Neutral, management-oriented, full navigation. Audience: directors, coordinators, admin staff."
surface: Administración
family: Pháros (cross-cutting platform surface)
accent: TBD — Administración is not ERP · Timón; sub-brand accent is OPEN (RFC 0008 Q1/Q6, @SKuger01). Use --primary generically; never invent a specific accent.
---
# Pháros — Administración (surface guidance)

**Audiencia:** Directivos, coordinadores, personal administrativo general.
**Surface / app:** Consola administrativa **transversal** del producto Pháros —
gestión de usuarios y roles, configuración, métricas globales y estado de las
distintas apps/superficies de la familia (LIS, Calidad, ERP · Timón, Reportes,
Portal Pacientes). Es una superficie de **plataforma/shell**, no una app de
dominio.
**Prioridades:** visión global del sistema, navegación multi-sección, gestión de
accesos, configuración sin fricciones.

> Token contract: [`../tokens.css`](../tokens.css) — shadcn-vue vars + the
> accent-independent status palette. Authoring conventions: `../frontend-standards.md`.
> This doc is per-surface guidance only; the component library is the tracked
> Phase-1 follow-up (registry README, "Decided vs open").

---

## Accent — read this first

Administración is a **cross-cutting** surface; it does **not** belong to
ERP · Timón, so it does **not** inherit the locked navy accent. Per RFC 0008
(Q1/Q6, @SKuger01 / brand playground), a per-surface accent for the platform
console is **OPEN — TBD**.

- Use `--primary` / `--accent` / `--ring` / `--sidebar-primary` **generically**
  (the contract default). **Never** invent a specific accent for this surface.
- The shared, accent-independent status palette (`--success` / `--warning` /
  `--error` / `--info`) and the family mark constants (`--pharos-burgundy`,
  `--pharos-red`) are **fixed** and do not shift with any future accent decision.
- If Administración renders a tile/section for a sub-brand (e.g. the ERP · Timón
  status card), that tile may borrow the sub-brand's own accent — but the console
  chrome itself stays on the generic `--primary`.

---

## Palette mapping (shadcn semantic tokens)

Everything is a semantic token; no raw hex, no `--adm-*`, no `--color-navy` /
`--color-brand-red`. `.dark`-aware by construction — these tokens flip with the
`.dark` class.

| Role | Token (utility) | Notes |
|---|---|---|
| App background | `bg-background` | replaces `#F1F5F9` |
| Card / panel | `bg-card` `text-card-foreground` | replaces `bg-white` |
| Section / sidebar surface | `bg-sidebar` / `bg-secondary` | replaces the navy `--adm-sidebar-bg` |
| Primary action / active nav | `bg-primary` `text-primary-foreground` | generic accent (TBD) |
| Subtle hover surface | `bg-accent` `text-accent-foreground` | replaces `rgba(255,255,255,.1)` |
| Secondary text / descriptions | `text-muted-foreground` | was `--text-secondary` / `--adm-text-muted` |
| Borders | `border-border` / `border-input` | replaces `--color-border` / `lch-gray-mid` |
| Focus ring | `ring-ring` | replaces `focus:ring-lch-red` |
| **OK / activo / habilitado** | `bg-success/20` `text-success-foreground` (badge) | was `--adm-positive` (teal) |
| **Pendiente / advertencia config** | `bg-warning/20` `text-warning-foreground` | was `--adm-warning` (orange) |
| **Crítico / destructivo (Eliminar, Deshabilitar)** | `bg-destructive` / `text-error` | was `--adm-accent` (red). Red is reserved for error + pilot light — never a primary action. |
| Informativo / resuelto | `text-info` / `bg-info/15` | system-health "info" rows |

Status mapping rule (canonical): positive/income → `--success`; pending/drift →
`--warning`; overdue/critical/out-of-control → `--error` / `--destructive`;
info/resolved → `--info`.

---

## Typography

- **Section titles:** `text-xl font-semibold text-foreground` (was 1.25rem navy).
- **Subtitles / section descriptions:** `text-sm text-muted-foreground`.
- **Config form labels:** `text-sm font-medium text-foreground`.
- **Summary statistics / counters / IDs / timestamps:** `font-mono tabular-nums`
  (IBM Plex Mono) — e.g. `text-2xl font-semibold font-mono tabular-nums`.
  **No JetBrains Mono.** Display/wordmark only ever uses Fraunces (`font-display`).

Any number, count, KPI, or "último acceso" timestamp uses `font-mono tabular-nums`
so columns align.

---

## App shell (layout)

```vue
<!-- Shell de la consola de administración -->
<div class="flex min-h-screen bg-background text-foreground">
  <!-- Sidebar fijo -->
  <AdminSidebar class="w-64 shrink-0" />

  <!-- Área de contenido -->
  <div class="flex flex-1 flex-col">
    <AdminTopbar />
    <main class="flex-1 p-6">
      <slot />
    </main>
  </div>
</div>
```

The lab-qc shadcn `Sidebar` is the app-shell reference; the sidebar uses the
`--sidebar-*` family of tokens throughout.

---

## Component inventory

### `AdminSidebar` — multi-section navigation
Props: `items: NavGroup[]`, `activeRoute: string`

```ts
interface NavGroup {
  label: string
  items: { label: string; route: string; icon: string; badge?: string }[]
}
```

```vue
<aside class="flex min-h-screen w-64 flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border">
  <div class="border-b border-sidebar-border p-5">
    <PharosLogo size="navbar" />
  </div>

  <nav class="flex-1 space-y-1 px-3 py-4">
    <div v-for="group in items" :key="group.label" class="mb-4">
      <p class="px-3 py-1 font-mono text-xs uppercase tracking-widest text-muted-foreground">
        {{ group.label }}
      </p>
      <a v-for="item in group.items"
         :href="item.route"
         class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
         :class="{ 'bg-sidebar-primary text-sidebar-primary-foreground font-medium': activeRoute === item.route }">
        <Icon :name="item.icon" class="h-5 w-5" />
        {{ item.label }}
        <span v-if="item.badge"
              class="ml-auto rounded-full bg-info/15 px-2 py-0.5 font-mono text-xs tabular-nums text-info">
          {{ item.badge }}
        </span>
      </a>
    </div>
  </nav>
</aside>
```

### `AdminTopbar` — top bar
Props: `usuario: { nombre: string; rol: string; avatar?: string }`, `title?: string`

```vue
<header class="flex items-center justify-between border-b border-border bg-card px-6 py-4">
  <h1 class="text-lg font-semibold text-foreground">{{ title }}</h1>
  <div class="flex items-center gap-3">
    <!-- Notificaciones -->
    <button class="relative rounded-lg p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground">
      <Icon name="bell" class="h-5 w-5" />
    </button>
    <!-- Avatar de usuario -->
    <div class="flex items-center gap-2">
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-medium text-primary-foreground">
        {{ usuario.nombre[0] }}
      </div>
      <div class="hidden md:block">
        <p class="text-sm font-medium text-foreground">{{ usuario.nombre }}</p>
        <p class="text-xs text-muted-foreground">{{ usuario.rol }}</p>
      </div>
    </div>
  </div>
</header>
```

> Note: the avatar uses `bg-primary` (the generic accent), **not** red — the old
> LCH version filled it with `bg-lch-red`, conflating brand-mark red with chrome.

### `AdminUsuarioCard` — system-user card
Props: `usuario: UsuarioSistema`

```ts
interface UsuarioSistema {
  nombre: string
  email: string
  rol: 'admin' | 'patólogo' | 'técnico' | 'financiero' | 'recepción'
  estado: 'activo' | 'inactivo' | 'pendiente'
  seccion: string
  ultimoAcceso?: string
}
```

```vue
<AdminUsuarioCard :usuario="usuario" @toggle-estado="handleToggle" @editar="handleEditar" />
```

State chip mapping: `activo` → `bg-success/20 text-success-foreground`;
`pendiente` → `bg-warning/20 text-warning-foreground`; `inactivo` →
`bg-muted text-muted-foreground`. `ultimoAcceso` renders `font-mono tabular-nums`.

### `AdminRolBadge` — user-role badge
Props: `rol: string`

Roles are **categories, not statuses** — so they use neutral / accent / chart
tokens, never the status palette (which is reserved for activo/pendiente/etc.).

```vue
<!-- Admin → accent (generic primary) -->
<span class="rounded-full bg-primary px-2.5 py-1 text-xs font-medium text-primary-foreground">Admin</span>
<!-- Otros roles → tinted accent / neutral surfaces -->
<span class="rounded-full bg-accent px-2.5 py-1 text-xs font-medium text-accent-foreground">Patólogo</span>
<span class="rounded-full bg-secondary px-2.5 py-1 text-xs font-medium text-secondary-foreground">Técnico</span>
<span class="rounded-full bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">Financiero</span>
```

### `AdminConfirmDialog` — destructive-action confirmation
Props: `titulo: string`, `mensaje: string`, `accion: string`, `variant?: 'danger' | 'warning'`

```vue
<AdminConfirmDialog
  titulo="Deshabilitar usuario"
  mensaje="Esta acción impedirá el acceso del usuario al sistema."
  accion="Deshabilitar"
  variant="danger"
  @confirm="handleDesactivar"
  @cancel="showDialog = false"
/>
```

```vue
<!-- Botón de acción destructiva (variant=danger) -->
<button class="rounded-lg bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground transition-colors hover:opacity-90">
  {{ accion }}
</button>
<!-- Botón de advertencia (variant=warning) -->
<button class="rounded-lg bg-warning px-4 py-2 text-sm font-medium text-warning-foreground transition-colors hover:opacity-90">
  {{ accion }}
</button>
<!-- Botón cancelar -->
<button class="rounded-lg border border-border px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent hover:text-accent-foreground">
  Cancelar
</button>
```

Modals use `rounded-xl` (the larger radius); the rest of the surface uses
`rounded-lg` (the `--radius` default).

### `AdminResumenSistema` — multi-app status dashboard
Shows the health of every Pháros surface (LIS / Calidad / ERP · Timón / Reportes /
Portal Pacientes). Each section tile is colored by its **status**, not its
sub-brand: `operativo` → `--success`, `degradado` → `--warning`, `caído` →
`--error`, `mantenimiento/info` → `--info`.

```vue
<AdminResumenSistema :secciones="estadoSecciones" />
```

```vue
<!-- Tile de estado de una sección -->
<div class="rounded-lg border border-border bg-card p-4">
  <div class="flex items-center justify-between">
    <p class="text-sm font-medium text-foreground">{{ seccion.nombre }}</p>
    <span class="inline-flex items-center gap-1.5 rounded-full bg-success/20 px-2 py-0.5 text-xs font-medium text-success-foreground">
      <span class="h-1.5 w-1.5 rounded-full bg-success"></span> Operativo
    </span>
  </div>
  <p class="mt-2 font-mono text-2xl font-semibold tabular-nums text-foreground">{{ seccion.uptime }}</p>
  <p class="text-xs text-muted-foreground">disponibilidad 30 d</p>
</div>
```

---

## Configuration forms

```vue
<div class="space-y-1">
  <label class="text-sm font-medium text-foreground">{{ label }}</label>
  <p class="text-xs text-muted-foreground">{{ descripcion }}</p>
  <input class="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm
                transition focus:border-ring focus:ring-2 focus:ring-ring" />
</div>
```

Focus rings use `ring-ring` (the accent), **not** red — the old LCH version
focused inputs with `focus:ring-lch-red`.

---

## Target paths (consuming app, e.g. the platform/admin shell)

```
components/administracion/AdminSidebar.vue
components/administracion/AdminTopbar.vue
components/administracion/AdminUsuarioCard.vue
components/administracion/AdminRolBadge.vue
components/administracion/AdminConfirmDialog.vue
components/administracion/AdminResumenSistema.vue
layouts/admin.vue
pages/admin/index.vue
pages/admin/usuarios.vue
pages/admin/configuracion.vue
```

---

## Ported from `ds-lch-administracion`; what changed

- **Accent.** Old file hard-coded the navy/blue/red LCH corporate palette
  (`--adm-primary = --color-navy`, etc.). Administración is a cross-cutting
  platform surface, **not** ERP · Timón, so the accent is **OPEN — TBD**
  (RFC 0008 Q1/Q6, @SKuger01). It now uses `--primary`/`--accent`/`--ring`/
  `--sidebar-primary` generically; no specific accent is invented.
- **Tokens.** Removed all `--adm-*`, `--color-navy`, `--color-brand-red`,
  `--color-text-*`, `--color-border`, every `lch-*` Tailwind class, and all raw
  hex (`#F1F5F9`, `#FFFFFF`, `rgba(...)`, `text-[#...]`). Replaced with shadcn
  semantic tokens (`background`/`foreground`/`card`/`muted-foreground`/`border`/
  `sidebar-*`) per `../tokens.css`.
- **Status palette.** Hard-coded teal/orange/red states → the accent-independent
  status palette: OK/activo → `--success`, advertencia/pendiente → `--warning`,
  destructivo/crítico → `--error`/`--destructive`, informativo → `--info`.
- **Red is no longer a primary.** The old topbar avatar (`bg-lch-red`) and input
  focus ring (`focus:ring-lch-red`) used brand red for chrome/primary affordances.
  Red is now reserved for `--error`/`--destructive` and the pilot light only;
  primary actions and focus use the accent (`--primary`/`--ring`).
- **Role badges** moved off the status palette onto neutral/accent surfaces —
  roles are categories, not states.
- **Type.** `JetBrains Mono` statistic values → `font-mono` (IBM Plex Mono) with
  `tabular-nums`. Display stays Fraunces; UI stays Inter.
- **Theming.** Now `.dark`-aware by construction (all tokens flip with the
  shadcn `.dark` class); the old file was light-only with a baked-in dark sidebar.
- **Naming/tenancy.** Component prefix `Lch…` → unprefixed `Admin…`; `LchLogo` →
  `PharosLogo`. A tenant never prefixes the surface (Pháros, never "LCH Pháros").
- **Inventory & UX patterns preserved:** audience, the transversal-admin purpose,
  the full component set (sidebar/topbar/usuario-card/rol-badge/confirm-dialog/
  resumen-sistema), config forms, target routes, and the multi-app status overview.
