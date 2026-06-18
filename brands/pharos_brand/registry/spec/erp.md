<!-- spec-version: bbe68096 · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Números — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-numeros` (+ `dark`). → `registry/tokens.css` (.theme-numeros).
- **Acento** claro `#7A5D00` / oscuro `#E6C34D`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Sutil (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Números» · náutico «Timón» · glyph lucide `ShipWheel` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `ShipWheel` (acento) + sublabel "ERP · Finanzas y operaciones"; eco en breadcrumb «Números». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-numeros">`. 3. Layout: `subName="Números" glyph="ShipWheel" subLabel="ERP · Finanzas y operaciones"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
