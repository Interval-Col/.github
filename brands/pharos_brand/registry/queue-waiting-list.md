# Pháros queue waiting list — QueueWaitingList (RFC 0008 · RFC 0031)

La lista de espera de una cola, en orden de llegada — **mirar sin tomar**. Nació
para la estación de toma de muestras de `pharos-lis/lab-qc` (tarea 5.4 del plan
del port: antes de esta lista, la única forma de saber si alguien esperaba era
reclamarlo — `call-next` consume el turno), y su forma es deliberadamente
agnóstica de superficie: es candidata directa a visor de proceso de sólo
lectura de RFC 0031 («¿dónde está esta muestra y por qué?»).

> Este es el **widget** (presentación pura). El **transporte** — a qué cola se
> pregunta, con qué token, cada cuánto se refresca — es de cada app, igual que
> el corte `send`/`probe` de `PharosHelpChat`. El widget nunca hace fetch y
> nunca escribe.

## What's in the registry (synced verbatim)

| Entry | Path | What it is |
|---|---|---|
| `QueueWaitingList` | `app/components/ui/queue-waiting-list/QueueWaitingList.vue` | encabezado con conteo + botón «Actualizar», tabla (posición · paciente · documento · órdenes · desde), y los tres estados no-lista: vacía (estado normal, no error), cargando (esqueleto), error con dueño |
| tipos | `app/components/ui/queue-waiting-list/types.ts` | `QueueWaitingRow` — el contrato de fila |
| barrel | `app/components/ui/queue-waiting-list/index.ts` | exporta componente + tipo |

**Deps (per adopting app):** ninguna nueva — `lucide-vue-next` y los primitivos
`ui/badge`, `ui/button`, `ui/skeleton`, `ui/table` que toda app adoptante ya
sincroniza (companions).

**Tokens:** sólo contrato de tokens (`--muted-foreground`, `--destructive`,
`--border`, …) — sin hex, re-acenta limpio bajo cualquier `.theme-*`.

## Per-app config

| Prop | Type | Default | Notes |
|---|---|---|---|
| `rows` | `QueueWaitingRow[]` | — | **required**; en orden de llegada — la fila 1 es la que «llamar siguiente» reclamaría |
| `loading` | `boolean` | `false` | esqueleto + botón deshabilitado |
| `error` | `string \| null` | `null` | UNA frase ya mapeada por la app, con su dueño (sede → coordinador, permiso → German, red → Yanna) — nunca la línea cruda de HTTP |
| `revealed` | `boolean` | `true` | política de revelado de PHI, decidida por la app (p. ej. `useIdlePrivacy` en lab-qc); en `false` enmascara nombre y documento |
| `maskedText` | `string` | `'•••'` | texto de máscara |
| `emptyText` | `string` | `'Nadie en espera — la estación está al día.'` | la cola vacía se dice en positivo |
| `refreshable` | `boolean` | `true` | muestra «Actualizar»; la app responde el emit `refresh` |

**Emits:** `refresh` — la app decide qué endpoint consulta y con qué token.

## PHI

`fullName` y `documentNumber` son PHI. El widget los recibe ya resueltos y los
enmascara según `revealed`; **la política es de la app**, nunca del registry.
Las filas jamás viajan en URLs ni logs (eso lo fijan las pruebas del backend
adoptante, p. ej. `test_no_phi_in_urls`). Órdenes sin registrar se dicen
(«sin órdenes registradas»), no se callan — recepción pudo no anotarlas y el
técnico tiene que poder verlo.

## Adopters

| App | Surface | Transport |
|---|---|---|
| `pharos-lis/lab-qc` | Muestras › Toma de muestra (estación) | `GET /sample-collection/waiting` (relay caller-bearer al listado de Admisiones) |
| _RFC 0031 viewer_ | pendiente de decisión (OQ#5 del RFC) | pendiente |

Gate de adopción: cubierto por los genéricos `check-registry-drift` /
`check-registry-fresh`; no lleva gate propio — es presentación pura, sin
decisión de marca parametrizada que pueda divergir (si aparece una, se
promueve a `registry/spec/` como en `chat.md`).
