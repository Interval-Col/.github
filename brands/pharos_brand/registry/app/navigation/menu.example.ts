// registry/app/navigation/menu — THE NAV CONTRACT the Pháros app-shell consumes.
//
// COPY-IN: rename this file to `menu.ts` in your app (the layout imports it as
// `~/navigation/menu`) and replace `menu` with your real navigation tree. The
// shell only ever reads the exported `menu` (a `NavMenu`) and the `isNavSubGroup`
// helper — nothing else. Keep the SHAPE; swap the data.
//
// Decoupling rules baked into this contract (RFC 0008 app-shell):
//   • i18n-free — items carry a LITERAL `label`, never an i18n key. Your app
//     localizes its nav model BEFORE handing it to the shell (build the tree
//     inside a `computed`/composable that resolves `$t(...)` if you use i18n).
//   • route-driven — `to` is the canonical path; the shell derives the
//     breadcrumb-as-title and the ⌘K palette purely from `to` + `label`.
//   • no app routes are hard-coded in the shell — the shell walks whatever
//     tree you export here.
//
// SHAPE:  groups → items ; an item is either a leaf {to,label,icon?} OR a
// sub-group {label,items:leaf[]}. One optional level of sub-grouping; the
// shell renders sub-groups as a labelled block inside the expandable group
// and as the breadcrumb's immediate-parent dropdown.

import type { Component } from 'vue'
import { BarChart3, Database, FlaskConical, Settings2 } from 'lucide-vue-next'

/** A navigable page. `icon` is a lucide component OR a lucide icon NAME
 *  (string) the shell resolves dynamically — pass whichever is convenient. */
export type NavLeaf = {
  to: string
  label: string
  icon?: Component | string
}

/** A labelled cluster of leaves nested under a top-level group. Has no `to`
 *  of its own (it is not navigable) — that is how the shell tells it apart
 *  from a leaf (see `isNavSubGroup`). */
export type NavSubGroup = {
  label: string
  items: NavLeaf[]
}

/** A top-level group item: either a direct leaf or a sub-group of leaves. */
export type NavItem = NavLeaf | NavSubGroup

/** A top-level sidebar group: a labelled, icon-headed, expandable section. */
export type NavGroup = {
  label: string
  icon?: Component | string
  items: NavItem[]
}

/** The whole menu the shell consumes. */
export type NavMenu = NavGroup[]

/** Type-guard the shell uses to tell a sub-group from a leaf: a sub-group has
 *  `items` and NO `to`. (Mirrors pharos-lis's `isSubGroup`, i18n-stripped.) */
export const isNavSubGroup = (i: NavItem): i is NavSubGroup =>
  'items' in i && !('to' in i)

// ── Sample tree (replace in your app) ─────────────────────────────────────
// Demonstrates: a group with a sub-group + a direct leaf (Control de calidad),
// a group with only a sub-group (Experimentos), and flat groups (Datos, Admin).
export const menu: NavMenu = [
  {
    label: 'Control de calidad',
    icon: BarChart3,
    items: [
      {
        label: 'QC interno',
        items: [
          { to: '/analytics/media-movil', label: 'Media móvil' },
          { to: '/qc/qc-diario', label: 'QC diario' },
        ],
      },
      { to: '/analytics/correlacion-metodos', label: 'Correlación de métodos' },
    ],
  },
  {
    label: 'Experimentos',
    icon: FlaskConical,
    items: [
      {
        label: 'Verificaciones',
        items: [
          { to: '/verificacion', label: 'Experimentos' },
          { to: '/verificacion/nuevo', label: 'Nuevo' },
          { to: '/verificacion/protocolos', label: 'Protocolos' },
        ],
      },
    ],
  },
  {
    label: 'Datos',
    icon: Database,
    items: [
      { to: '/datos/catalogo', label: 'Catálogo' },
      { to: '/datos/resultados', label: 'Resultados' },
      { to: '/datos/test-codes', label: 'Códigos de prueba' },
    ],
  },
  {
    label: 'Administración',
    icon: Settings2,
    items: [
      { to: '/admin/users', label: 'Usuarios' },
      { to: '/admin/roles', label: 'Roles' },
    ],
  },
]
