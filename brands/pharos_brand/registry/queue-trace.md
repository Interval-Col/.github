# Pháros queue trace — QueueTrace (RFC 0008 · RFC 0031)

El **recorrido de una fila de la cola**: los pasos en orden, con quién los hizo y
**qué superficie manda en cada tramo**. Contesta la pregunta que hoy se hace por
teléfono — *«¿dónde está esta muestra y por qué?»*.

💡 **No inventa una pantalla: hace honesta una que ya existe mal.** El tablero de
recepción filtra por «hoy, esta oficina, no Cancelled/Finished» y **no** por
estado de recepción, así que **ya muestra** pacientes que salieron de recepción
—recibidos en toma, en atención en Movimiento— sin decir a dónde se fueron. Por
eso esta fase sale más barata de lo que parece: la pantalla ya existía, le
faltaba la verdad.

> Este es el **widget** (presentación pura). El **transporte** — a qué cola se
> pregunta, con qué token, cuándo se pide — es de cada app, igual que
> `QueueWaitingList` y `PharosHelpChat`. El widget **nunca hace fetch y nunca
> escribe**.

## What's in the registry (synced verbatim)

| Entry | Path | What it is |
|---|---|---|
| `QueueTrace` | `app/components/ui/queue-trace/QueueTrace.vue` | la línea de tiempo: riel de puntos, etiqueta del estado, chip de qué superficie lo emitió, fecha y autor; más los tres estados no-lista (cargando, error con dueño, sin recorrido) y el marcador del laboratorio |
| vocabulario | `app/components/ui/queue-trace/types.ts` | `QUEUE_TRACE_STATUS` (los 12 estados con su etiqueta y su emisor), `queueTraceStatus()`, `endsAtCobol()` |

## Tres propiedades que no son negociables, y por qué

### 1 · Dice dónde se le acaba el saber

Cuando el último paso es `SampleCollectionTaken`, el widget marca que **desde ahí
manda el laboratorio**. «No hay más pasos» y «no sabemos qué más pasó» son cosas
distintas, y sólo la segunda es cierta: la cola no ve nada después de la toma.

Un visor que callara esa diferencia enseñaría que el paciente se quedó ahí.

### 2 · Un estado desconocido se MUESTRA, no se omite

El contrato de `pharos-queue` tiene **14** estados y esta tabla conoce **12**: el
servicio puede mandar uno que el widget no tenga. Se pinta con su nombre crudo.

Un paso que desaparece hace que la historia **mienta por omisión**, y eso es peor
que mostrar un nombre técnico: quien lo lea va a preguntar, y preguntar es el
comportamiento correcto.

### 3 · El vocabulario vive acá, no en cada app

La matriz canónica de estados es de `pharos-queue` (`docs/state-machine.md`) y la
pantalla sólo la **traduce**. Si cada superficie escribiera sus etiquetas, la
segunda las reinventaría — y dos pantallas llamando distinto al mismo estado es
cómo una operadora termina sin saber si son dos cosas o una.

🪤 **Y el detalle más fácil de equivocar:** `SampleCollectionWaiting` y
`BiumanWaitingAttention` los emite **recepción**, no el destino. Son «lo mandé
para allá», no «llegó allá».

## Lo que NO lleva

**Ningún dato de paciente**, y no por olvido: un recorrido son cambios de estado.
Quien lo abre ya sabe de qué paciente es —lo abrió desde su tarjeta o su fila—, así
que devolvérselos sería un sitio más donde pueden filtrarse.

## Wiring, en la app que consume

1. `scripts/sync-pharos-registry.sh --add app/components/ui/queue-trace/…`
2. Su backend expone la lectura: **el navegador nunca le habla a `pharos-queue`**
   (regla 1 del servicio). Cada app llama desde su BFF con las **dos
   credenciales** — secreto de servicio y token de la persona.
3. La app envuelve el widget en lo que le sirva —un diálogo en Recepción, un panel
   en la estación— y le pasa `steps`, `loading` y `error`.

⚠️ **El texto del error lo pone la app**, y a propósito: «no está configurada» lo
arregla quien despliega, «no responde» se espera, «no autorizó» se pide. El widget
no los reescribe porque no sabe a quién mandar.

🔴 **Y un 503 de la cola no es un 403.** La cola contesta 503 cuando el SSO no le
sabe decir quién llama o el roster no le da su sede. Aplanarlo a 403 manda a la
operadora a pedir un permiso que ya tiene. Eso lo decide el BFF, no el widget —
pero si el widget recibe el texto equivocado, lo va a mostrar tal cual.

## Precedente

Nació de la tarea 1.9 del plan de `pharos-queue`, montado primero en
`admission-patient` (diálogo desde la tarjeta del tablero) y después en
`pharos-lis/lab-qc` (la estación de toma). Se promovió acá **cuando existió el
segundo consumidor**, que es el umbral que justifica abstraer — antes habría sido
diseñar para un usuario imaginario.
