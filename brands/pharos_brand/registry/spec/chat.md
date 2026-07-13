<!-- spec-version: 95daddc9 · generado 2026-07-13 desde el playground (NO editar a mano; regenerar) -->

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

De las 8 perillas, el componente publicado sólo expone **`starters`** como prop real. Las demás son
comportamiento cableado o no existen. Esta tabla es el contrato honesto: no adopte una perilla
marcada ❌ creyendo que ya funciona.

| Perilla | Decisión | Soporte | Detalle |
|---|---|---|---|
| Nombre | Rigel — Estrella de Orión | ❌ no existe | no existe una prop de nombre propio; `brandName` es la marca de la app, no el nombre del asistente |
| Avatar / logo | Robot (neutro) | ❌ no existe | el lanzador dibuja un ícono fijo; no hay prop de avatar |
| Fondo del avatar | Sobre círculo | ❌ no existe | depende de una prop de avatar que no existe |
| Disparador | Botón en topbar | ⚠️ cableado | lanzador `position: fixed` abajo-derecha, cableado en el CSS del componente — «topbar» no es una opción |
| Forma del panel | Cajón lateral | ⚠️ cableado | panel esquina cableado; no hay variante «cajón lateral» (sheet) |
| Estado «En línea» | sí | ❌ no existe | el encabezado no renderiza línea de estado «En línea» |
| Fuentes (citas) | sí | ⚠️ cableado | las fuentes se pintan SIEMPRE que la respuesta traiga `sources` (CH5); no se pueden apagar por configuración |
| Sugerencias | sí | ✅ prop | prop `starters: string[]` — `[]` las apaga; la app aporta el texto de cada chip |

Props reales del componente (las únicas perillas por app): `send` (requerida) · `brandName` ·
`title` · `starters` · `storageKey` (única por app) · `placeholder`.

### Brecha — trabajo pendiente en el registry (`.github`#126)

Para que este pick se honre de punta a punta, `PharosHelpChat.vue` necesita:

- **Nombre** — no existe una prop de nombre propio; `brandName` es la marca de la app, no el nombre del asistente
- **Avatar / logo** — el lanzador dibuja un ícono fijo; no hay prop de avatar
- **Fondo del avatar** — depende de una prop de avatar que no existe
- **Disparador** — lanzador `position: fixed` abajo-derecha, cableado en el CSS del componente — «topbar» no es una opción
- **Forma del panel** — panel esquina cableado; no hay variante «cajón lateral» (sheet)
- **Estado «En línea»** — el encabezado no renderiza línea de estado «En línea»
- **Fuentes (citas)** — las fuentes se pintan SIEMPRE que la respuesta traiga `sources` (CH5); no se pueden apagar por configuración

Mientras la brecha exista, la decisión queda **registrada pero no implementada**: las apps siguen
montando el widget con su comportamiento cableado (burbuja flotante + panel esquina, sin persona).

### Consumir (junior / Sonnet)

1. `scripts/sync-pharos-registry.sh --add components/PharosHelpChat.vue <app-fe-dir>` — copia el widget
   y lo registra en el manifiesto de drift (Lock 3, `check-registry-drift`).
2. `pnpm add marked dompurify && pnpm add -D @types/dompurify` — ambas cargan el borde XSS (`marked`
   renderiza, `DOMPurify` sanea antes del `v-html`); nunca quite una.
3. Móntelo UNA vez en el shell de la app, cableando el transporte propio y un `storageKey` único.
4. Prenda `fe_registry_widget: on` en `.chat-contract.yml`; el check H8 sostiene el widget en su lugar
   (un `HelpChat.vue` hecho a mano reprueba la compuerta).
