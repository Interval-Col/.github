<!-- spec-version: ea73319d · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->

# Pháros — especificación de familia (shell + tokens)

> Fuente: design-studio playground. Cada app COPIA el registry (`registry`) y fija 5 perillas: { clase `theme-*`, glyph, subLabel, navegación, slot user }. Implementar contra los anclajes `registry/…` indicados.

## Tipografía (4 familias)
- **Display** Fraunces (Pháros) · **UI** DM Sans · **Mono/etiquetas** IBM Plex Mono (Pháros default) · **Datos** JetBrains Mono (datos · RFC 0008 Q5) (tabular-nums). → `registry/tokens.css` (@theme --font-*). Datos ≠ etiquetas.

## Tema
- Claro + oscuro vía clase `.dark`; sin cobol, sin [data-theme]. → `registry/tokens.css`.

## Shell — "Faro + Instrumento"
- Estructura **Beacon rail + ⌘K · faro ★** (riel-faro + ⌘K) · radio **Nítido** · densidad **Media** (Amplia 2.5rem / Media 1.5rem / Compacta .875rem). → riel `registry/app/assets/css/pharos-components.css ([data-pg-sidebar] [data-active])`; densidad `registry/app/layouts/default.vue (density prop) + pharos-components.css ([data-pg-content][data-density])`; ⌘K `registry/app/navigation/menu.ts (contract) + app/components/CommandPalette.vue`. Breadcrumb-como-título (sin `<h1>`).
- **Faro (pilot light)** #E4002B (constante de marca `#E4002B`); halo al latir; ritmo ligado a `<html data-status>`. → `registry/app/components/SystemBeacon.vue + app/plugins/health-beacon.client.ts; pilot in AppLogo.vue + pharos-components.css (.pharos-pilot)`.
- **Oleaje** sí — altura Medio, tinte Acento, espuma sí, barco sí; estado de mar sigue al faro. → `registry/app/components/SystemOcean.vue + app/assets/css/pharos-components.css (.pharos-ocean)`.
- **Lockup** marca = Solo logo; sub-nombre con acento: no; sublabel: descriptor completo; eco en breadcrumb: sí. → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`, `registry/app/layouts/default.vue (crumbs)`.
- **Usuario / sesión** Sidebar · abajo (avatar + punto de estado independiente del acento + nombre/rol + popover). → `registry/app/components/SidebarUser.vue (via the layout #user slot)`.
- **Maker ribbon** "Interval · Tecnología Humana" — monocromo, requerido (BRAND.md §10). → `registry/app/components/MakerCredit.vue`.

## Paleta de estado (independiente del acento, RFC 0008 Q4)
- `--status-{success,warning,error,info}` + `-bg`; nunca el acento de sub-marca. → `registry/tokens.css (--status-* + -bg)`.

## Gráficas
- @unovis + `--chart-1..5` fijos de marca. → `registry/tokens.css (--chart-1..5) + @unovis`.
