<!-- spec-version: 9d131f69 · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Clientes — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-clientes` (+ `dark`). → `registry/tokens.css` (.theme-clientes).
- **Acento** claro `#e37600` / oscuro `#f59e3c`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Wash decorativo** claro `#FFB86B` / oscuro `#FFB86B` → `--brand-wash`. SOLO decorativo (no interactivo); nunca en `--primary`/`--ring`/`--sidebar-primary` ni en ningún slot funcional. → `registry/tokens.css` (.theme-clientes).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Clientes» · náutico «Catalejo» · glyph lucide `Telescope` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Telescope` (acento — `text-primary`/`--primary`) + sublabel "CRM · Relaciones comerciales"; eco en breadcrumb «Clientes». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-clientes">`. 3. Layout: `subName="Clientes" glyph="Telescope" subLabel="CRM · Relaciones comerciales"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
