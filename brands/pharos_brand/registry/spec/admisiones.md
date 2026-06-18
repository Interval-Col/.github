<!-- spec-version: 93f2eb80 · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Pacientes — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-recepcion` (+ `dark`). → `registry/tokens.css` (.theme-recepcion).
- **Acento** claro `#FFE0E6` / oscuro `#FFE0E6`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Pacientes» · náutico «Muelle» · glyph lucide `Anchor` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Anchor` (acento) + sublabel "Admisiones · Recepción"; eco en breadcrumb «Pacientes». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-recepcion">`. 3. Layout: `subName="Pacientes" glyph="Anchor" subLabel="Admisiones · Recepción"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
