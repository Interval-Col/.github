<!-- spec-version: 4b9988bc · generado 2026-11-02 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Analítica — especificación de sub-marca

> Hereda la spec de familia. Una sub-marca difiere SOLO en el acento + la identidad; el resto se hereda sin cambios. Para implementar: añade la clase de tema a `<html>` y fija las perillas del lockup; nunca toques `--primary`/`--chart-*` a mano.

- **Clase de tema** `theme-analitica` (+ `dark`). → `registry/tokens.css` (.theme-analitica).
- **Acento** claro `#3F5212` / oscuro `#B5CF6B`. Solo en `--primary`/`--ring`/`--sidebar-primary` (+ foregrounds).
- **Intensidad** Neutro (difusión en superficies neutras; estado + gráficas intactos).
- **Carácter** forma Auto · profundidad Plano · énfasis Sobrio · movimiento Natural.
- **Nomenclatura** nombre «Analítica» · náutico «Carta» · glyph lucide `MapPinned` (logo náutico sí, RFC 0008 Q1).
- **Lockup** sidebar = logo Pháros + glyph `MapPinned` (acento — `text-primary`/`--primary`) + sublabel "Analítica · Inteligencia de negocio"; eco en breadcrumb «Analítica». → `registry/app/layouts/default.vue (SidebarHeader) + app/components/AppLogo.vue`.
- **Paleta de estado** Referencia (actual) (independiente del acento). → `registry/tokens.css (--status-* + -bg)`.

### Consumir (junior / Sonnet)
1. Copia el registry; no edites los archivos copiados. 2. `<html class="theme-analitica">`. 3. Layout: `subName="Analítica" glyph="MapPinned" subLabel="Analítica · Inteligencia de negocio"`. 4. `navigation/menu.ts` con etiquetas es-CO. 5. `#user` ← SidebarUser con tu sesión. Correr → marca completa; el parity-gate atrapa desvíos.
