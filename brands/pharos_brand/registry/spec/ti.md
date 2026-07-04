<!-- spec-version: 311729e5 · generado 2026-07-03 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Tecnología — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-ti` (+ `dark`). → `registry/tokens.css` (.theme-ti).
- **Acento** claro `#002A52` / oscuro `#7FB0E6`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Tecnología» · náutico «Submarino» · glyph custom `Submarine` (no existe en lucide — vendorizado en `registry/app/lib/custom-glyphs.ts`; logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Submarine` (acento — `text-primary`/`--primary`) + sublabel "TI · Administración de plataforma"; eco en breadcrumb «Tecnología». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-ti">`. 3. Layout: `subName="Tecnología" glyph="Submarine" subLabel="TI · Administración de plataforma"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
