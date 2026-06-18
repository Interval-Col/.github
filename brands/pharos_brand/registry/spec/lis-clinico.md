<!-- spec-version: 52802ac5 · generado 2026-06-18 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Laboratorio — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-clinico` (+ `dark`). → `registry/tokens.css` (.theme-clinico).
- **Acento** claro `#1B6B5A` / oscuro `#4CD1B0`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Laboratorio» · náutico «Sonda» · glyph lucide `Radar` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `Radar` (acento — `text-primary`/`--primary`) + sublabel "LIS · Laboratorio clínico"; eco en breadcrumb «Laboratorio». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-clinico">`. 3. Layout: `subName="Laboratorio" glyph="Radar" subLabel="LIS · Laboratorio clínico"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
