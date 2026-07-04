<!-- spec-version: 85cb038e · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->
<!-- renombre 2026-07-03: «Deportivo» → «Movimiento» (RFC 0008 Decisions 2026-07-03) — alineado a mano; regenerar spec-version en el próximo export del playground -->

# Pháros · Movimiento — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-deportivo` (+ `dark`). → `registry/tokens.css` (.theme-deportivo).
- **Acento** claro `#004F70` / oscuro `#16749C`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Movimiento» · náutico «Vela» · glyph lucide `Sailboat` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Sailboat` (acento — `text-primary`/`--primary`) + sublabel "LIS · Laboratorio deportivo"; eco en breadcrumb «Movimiento». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-deportivo">`. 3. Layout: `subName="Movimiento" glyph="Sailboat" subLabel="LIS · Laboratorio deportivo"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
