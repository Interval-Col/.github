<!-- spec-version: b80b3aec · generado 2026-07-13 desde el playground (NO editar a mano; regenerar) -->

# Pháros · Asistente — especificación del chat (RFC 0017)

> Fuente: el playground de design-studio (sección «Asistente»). La realiza `registry/app/components/PharosHelpChat.vue`; la adopción
> por app vive en `registry/chat-widget.md`.
> UNA sola definición canónica: finance-lch y biuman-lis la hidratan desde el registry — sin 3ª variante.
> El **widget** (esta spec) es agnóstico del transporte; el **producto** — qué sabe el asistente, cómo
> recupera — es por app (chat-contract CH7), y la pasarela (`pharos-llm-proxy`) es compartida.

## Decisión — el pick del playground

- **Nombre** — Rigel — Estrella de Orión
- **Avatar / logo** — Robot (neutro)
- **Fondo del avatar** — Sobre círculo
- **Disparador** — Botón en topbar
- **Forma del panel** — Cajón lateral
- **Estado «En línea»** — sí
- **Fuentes (citas)** — sí
- **Sugerencias** — sí

## Estado de implementación — qué honra HOY `PharosHelpChat.vue`

Las 8 perillas son props reales del componente — **no hay brecha**: el pick de arriba se
honra tal cual. Cada prop cae, por defecto, al comportamiento previo a 2026-07-13 (burbuja flotante ·
panel esquina · sin persona), así que una app que re-sincronice sin tocar su montaje sigue viéndose igual.

| Perilla | Decisión | Soporte | Detalle |
|---|---|---|---|
| Nombre | Rigel — Estrella de Orión | ✅ prop | prop `assistantName` — `''` = sin nombre (el encabezado cae al `title` y el saludo queda genérico) |
| Avatar / logo | Robot (neutro) | ✅ prop | prop `avatar` — un id de `PharosChatAvatar`; `''` = la burbuja de diálogo simple |
| Fondo del avatar | Sobre círculo | ✅ prop | prop `avatarBg: 'circulo' \| 'solo'` — marca sobre chip redondo, o el glifo desnudo |
| Disparador | Botón en topbar | ✅ prop | prop `trigger: 'floating' \| 'topbar'`. ⚠️ `topbar` exige montar el componente DENTRO del topbar de la app (la raíz pasa a `display: contents`) |
| Forma del panel | Cajón lateral | ✅ prop | prop `form: 'corner' \| 'sheet'` — tarjeta esquina, o cajón lateral de altura completa con backdrop |
| Estado «En línea» | sí | ✅ prop | prop `statusLine` — «En línea» bajo el nombre + punto en el botón del topbar. Es COSMÉTICO: no consulta el backend |
| Fuentes (citas) | sí | ✅ prop | prop `citations` — pinta las fuentes en respuestas fundamentadas (CH5); `false` las apaga |
| Sugerencias | sí | ✅ prop | prop `starters: string[]` — `[]` las apaga; la app aporta el texto de cada chip |

Además, el transporte y el texto siguen siendo por app: `send` (requerida) · `brandName` · `title` ·
`storageKey` (única por app) · `placeholder`.

⚠️ `trigger: topbar` cambia **dónde** se monta el widget: la raíz pasa a `display: contents`, así que el
botón se dibuja como hijo directo de lo que lo contenga. Móntelo dentro de la fila de acciones del
topbar de la app, no en cualquier punto del shell.

### Brecha — ninguna

`PharosHelpChat.vue` honra las 8 perillas (`.github`#126, 2026-07-13). Antes de esa fecha
6 de 8 no existían y esta sección listaba el trabajo pendiente; se conserva, vacía, a propósito: si el
playground gana una perilla nueva antes de que el componente la soporte, la brecha reaparece sola.

### Consumir (junior / Sonnet)

1. `scripts/sync-pharos-registry.sh --add components/PharosHelpChat.vue <app-fe-dir>` — copia el widget
   y lo registra en el manifiesto de drift (Lock 3, `check-registry-drift`).
2. `pnpm add marked dompurify && pnpm add -D @types/dompurify` — ambas cargan el borde XSS (`marked`
   renderiza, `DOMPurify` sanea antes del `v-html`); nunca quite una.
3. Móntelo UNA vez en el shell de la app, cableando el transporte propio y un `storageKey` único.
4. Prenda `fe_registry_widget: on` en `.chat-contract.yml`; el check H8 sostiene el widget en su lugar
   (un `HelpChat.vue` hecho a mano reprueba la compuerta).
