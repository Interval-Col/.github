---
description: "Use when creating components or pages for LCH Administración — the general administrative dashboard. Neutral palette, full navigation, multi-section overview, management-oriented. Audience: directors and admin staff."
---
# Design System — LCH Administración

**Audiencia:** Directivos, coordinadores, personal administrativo general  
**Aplicación:** Panel de administración transversal (gestión de usuarios, configuración, métricas globales)  
**Prioridades:** visión global del sistema, navegación multi-sección, gestión de accesos, sin fricciones

---

## Paleta de colores — Administración

```css
/* Sección Administración — Paleta corporativa neutral */
--adm-primary:       var(--color-navy);         /* #003A70 — dominante */
--adm-secondary:     var(--color-blue);         /* #326295 — acciones secundarias */
--adm-accent:        var(--color-brand-red);    /* #E4002B — acciones de alerta / destructivas */
--adm-positive:      var(--color-teal);         /* #A0D1CA — estados OK, activo */
--adm-warning:       var(--color-brand-orange); /* #FF8200 — advertencias */
--adm-bg:            #F1F5F9;                   /* gris-azulado neutro */
--adm-surface:       #FFFFFF;
--adm-surface-alt:   #F8FAFC;
--adm-text:          var(--color-text-primary);
--adm-text-muted:    var(--color-text-secondary);
--adm-border:        var(--color-border);
--adm-sidebar-bg:    var(--color-navy);
--adm-sidebar-text:  #FFFFFF;
--adm-sidebar-hover: rgba(255,255,255,0.1);
--adm-sidebar-active:#326295;               /* ítem activo: azul */
```

### Tailwind v4 — Clases frecuentes
```
bg-[#F1F5F9]           → fondo de aplicación
bg-lch-navy            → sidebar, topbar
bg-lch-blue            → ítem activo en sidebar
text-white             → texto sobre superficies dark
bg-white               → tarjetas, paneles
border-lch-gray-mid    → bordes de cards
text-lch-red           → acciones destructivas (Eliminar, Deshabilitar)
bg-lch-teal/30         → estado activo/habilitado
bg-lch-orange/20       → advertencia de configuración
```

---

## Tipografía — Administración

```css
/* Títulos de sección de panel */
font-size: 1.25rem; font-weight: 600; color: var(--color-navy);

/* Subtítulos / descripción de sección */
font-size: 0.875rem; color: var(--color-text-secondary);

/* Etiquetas de formularios de configuración */
font-size: 0.875rem; font-weight: 500;

/* Valores estadísticos de resumen */
font-family: 'JetBrains Mono'; font-size: 1.5rem; font-weight: 600; tabular-nums;
```

---

## Layout de aplicación

```vue
<!-- Shell principal del panel de administración -->
<div class="flex min-h-screen bg-[#F1F5F9]">
  <!-- Sidebar fijo -->
  <LchAdminSidebar class="w-64 shrink-0" />

  <!-- Área de contenido -->
  <div class="flex-1 flex flex-col">
    <LchAdminTopbar />
    <main class="flex-1 p-6">
      <slot />
    </main>
  </div>
</div>
```

---

## Componentes disponibles

### `LchAdminSidebar` — Navegación lateral
Props: `items: NavGroup[]`, `activeRoute: string`

```ts
interface NavGroup {
  label: string
  items: { label: string; route: string; icon: string; badge?: string }[]
}
```

```vue
<!-- Patrón sidebar -->
<aside class="w-64 bg-lch-navy flex flex-col min-h-screen">
  <div class="p-5 border-b border-white/10">
    <LchLogo theme="dark" size="navbar" />
  </div>

  <nav class="flex-1 py-4 px-3 space-y-1">
    <div v-for="group in items" :key="group.label" class="mb-4">
      <p class="px-3 py-1 font-['IBM_Plex_Mono'] text-xs uppercase tracking-widest text-white/40">
        {{ group.label }}
      </p>
      <a v-for="item in group.items"
         :href="item.route"
         class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-white/80 hover:bg-white/10 transition-colors"
         :class="{ 'bg-lch-blue text-white font-medium': activeRoute === item.route }">
        <Icon :name="item.icon" class="w-5 h-5" />
        {{ item.label }}
      </a>
    </div>
  </nav>
</aside>
```

### `LchAdminTopbar` — Barra superior
Props: `usuario: { nombre: string, rol: string, avatar?: string }`, `title?: string`

```vue
<header class="bg-white border-b border-lch-gray-mid px-6 py-4 flex items-center justify-between">
  <h1 class="font-semibold text-lch-navy text-lg">{{ title }}</h1>
  <div class="flex items-center gap-3">
    <!-- Notificaciones -->
    <button class="relative p-2 rounded-lg hover:bg-lch-blush/30 text-lch-gray-dark">
      <Icon name="bell" class="w-5 h-5" />
    </button>
    <!-- Avatar de usuario -->
    <div class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-full bg-lch-red flex items-center justify-center text-white text-sm font-medium">
        {{ usuario.nombre[0] }}
      </div>
      <div class="hidden md:block">
        <p class="text-sm font-medium text-lch-navy">{{ usuario.nombre }}</p>
        <p class="text-xs text-lch-gray-dark">{{ usuario.rol }}</p>
      </div>
    </div>
  </div>
</header>
```

### `LchAdminUsuarioCard` — Tarjeta de usuario del sistema
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
<LchAdminUsuarioCard :usuario="usuario" @toggle-estado="handleToggle" @editar="handleEditar" />
```

### `LchAdminRolBadge` — Badge de rol de usuario
Props: `rol: string`

```vue
<!-- Admin → navy -->
<span class="bg-lch-navy text-white px-2.5 py-1 rounded-full text-xs font-medium">Admin</span>
<!-- Patólogo → blue -->
<span class="bg-lch-blue/20 text-lch-navy px-2.5 py-1 rounded-full text-xs font-medium">Patólogo</span>
<!-- Técnico → teal -->
<span class="bg-lch-teal/30 text-lch-navy px-2.5 py-1 rounded-full text-xs font-medium">Técnico</span>
<!-- Financiero → yellow -->
<span class="bg-lch-yellow/40 text-lch-black px-2.5 py-1 rounded-full text-xs font-medium">Financiero</span>
```

### `LchAdminConfirmDialog` — Diálogo de confirmación de acción destructiva
Props: `titulo: string`, `mensaje: string`, `accion: string`, `variant?: 'danger' | 'warning'`

```vue
<LchAdminConfirmDialog
  titulo="Deshabilitar usuario"
  mensaje="Esta acción impedirá el acceso del usuario al sistema."
  accion="Deshabilitar"
  variant="danger"
  @confirm="handleDesactivar"
  @cancel="showDialog = false"
/>
```

```vue
<!-- Botón de acción destructiva -->
<button class="bg-lch-red hover:bg-lch-red-dark text-white font-medium px-4 py-2 rounded-lg text-sm transition-colors">
  {{ accion }}
</button>
<!-- Botón cancelar -->
<button class="border border-lch-gray-mid text-lch-gray-dark hover:bg-lch-blush/30 font-medium px-4 py-2 rounded-lg text-sm transition-colors">
  Cancelar
</button>
```

### `LchAdminResumenSistema` — Dashboard de estado del sistema
Muestra estado de todas las secciones (Laboratorio, Finanzas, Calidad, Reportes, Portal).

```vue
<LchAdminResumenSistema :secciones="estadoSecciones" />
```

---

## Formularios de configuración

```vue
<!-- Campo de configuración -->
<div class="space-y-1">
  <label class="text-sm font-medium text-lch-navy">{{ label }}</label>
  <p class="text-xs text-lch-gray-dark">{{ descripcion }}</p>
  <input class="w-full border border-lch-gray-mid rounded-lg px-3 py-2 text-sm
                focus:ring-2 focus:ring-lch-red focus:border-lch-red transition" />
</div>
```

---

## Rutas de destino
```
components/Administracion/LchAdminSidebar.vue
components/Administracion/LchAdminTopbar.vue
components/Administracion/LchAdminUsuarioCard.vue
components/Administracion/LchAdminRolBadge.vue
components/Administracion/LchAdminConfirmDialog.vue
components/Administracion/LchAdminResumenSistema.vue
layouts/admin.vue
pages/admin/index.vue
pages/admin/usuarios.vue
pages/admin/configuracion.vue
```
