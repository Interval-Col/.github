<!-- spec-version: 8129be41 · generado 2026-10-28 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Documentos — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-documentos` (+ `dark`). → `registry/tokens.css` (.theme-documentos).
- **Acento** claro `#5B3F8C` / oscuro `#B79CE8`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Documentos» · náutico «Bitácora» · glyph lucide `Map` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Map` (acento — `text-primary`/`--primary`) + sublabel "Documentos · Control documental"; eco en breadcrumb «Documentos». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-documentos">`. 3. Layout: `subName="Documentos" glyph="Map" subLabel="Documentos · Control documental"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
