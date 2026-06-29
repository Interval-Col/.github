# 🧹 Higiene de Chats con Agentes — Interval-Col

> **Guía de la organización — esto es una RECOMENDACIÓN, no es obligatorio.** No hay chequeo de CI, ni configuración requerida, y nadie te va a rebotar un PR por esto. Es el consejo que un compañero senior te daría tomando un café: cómo mantener tus sesiones de Claude Code baratas y ordenadas sin perder nunca trabajo real. Léela, toma lo que te sirva, ignora el resto.

> 🇬🇧 **Fuente en inglés:** [`AGENT-CHAT-HYGIENE.md`](AGENT-CHAT-HYGIENE.md). Los bloques de código se mantienen idénticos al inglés (una sola fuente de verdad para los comandos).

**TL;DR (valores por defecto seguros):** mantén el conocimiento duradero en el repo o en la memoria — nunca _solo_ en el chat. Luego: **un chat por tarea**; **`/compact`** para terminar la tarea actual; **`/clear`** (o un chat nuevo) para cambiar de tarea o empezar un nuevo día; **consérvalo** ante la duda (los transcripts se borran solos a los 30 días); **borra** solo un transcript verdaderamente agotado; cuando **abras varios** sub-agentes, usa el modelo más barato que sirva y prefiere un agente fresco sobre un `fork` (§11). Todo lo de abajo es el _porqué_.

---

## 1. El principio único

**Los chats son sesiones de trabajo desechables. El repo y tu memoria son la capa de persistencia.**

Una conversación de Claude Code es un banco de trabajo, no un archivador. En el momento en que una decisión, un porqué o un artefacto importa más allá de _esta sesión_, debe vivir en un lugar duradero — un doc, un RFC, un plan, el código mismo, o la memoria — y **no** atrapado en un transcript que esperas volver a leer la próxima semana.

Una vez que el conocimiento duradero está escrito donde sobrevive, **botar o compactar el chat no te cuesta nada.** De eso se trata todo. Externaliza primero, luego sé implacable con el chat.

---

## 2. Por qué importa — tokens, en palabras simples

No pagas por "tener un chat largo" como pagas por almacenamiento. Pagas cada vez que _envías un turno_, y un chat largo reenvía **todo su historial creciente** en cada turno. La conversación es el costo.

Tres cosas se acumulan acá:

- **Los chats largos reenvían un contexto creciente en cada turno.** El turno 50 de un mega-chat manda los 49 intercambios previos junto con tu nueva pregunta. Cada turno en una sesión inflada es más caro que el mismo turno en una fresca — para la misma cantidad de señal real.
- **La auto-compactación pierde detalle _y_ cuesta tokens.** Cuando una conversación se acerca al límite de la ventana de contexto, Claude Code reemplaza automáticamente los intercambios viejos por un resumen estructurado. Las decisiones y aprendizajes clave se conservan, pero **las instrucciones detalladas del comienzo de la conversación se pueden perder.** Y el propio resumen es una llamada a la API que consume tokens — pagas por encoger tu propio historial. (Caso límite: si un solo archivo o salida es tan grande que el contexto se vuelve a llenar _de inmediato_ tras cada resumen, Claude Code deja de auto-compactar y muestra un error de "thrashing" en vez de quedar en bucle.)
- **El caché de prompt se enfría.** Dentro de una sesión, el contexto repetido se puede servir desde un caché de prompt (TTL por defecto **5 minutos**, o 1 hora a 2× el costo de escritura de caché) a ~0.1× la tarifa base de tokens de entrada. Pero el caché **expira si no se accede dentro de su ventana de TTL** — así que un chat que retomas _al día siguiente_ tiene el caché frío como piedra. El primer turno vuelve a pagar el costo completo de escritura de caché. Retomar un mega-chat de un día atrás es casi el peor caso: contexto enorme, sin caché tibio, poca señal nueva.

**La intuición:** un chat viejo y desparramado quema tokens por muy poca señal. Uno corto y enfocado se mantiene barato. Nada de esto importa si tu conocimiento ya está a salvo en el repo — que es exactamente por qué el principio #1 va primero.

> La auto-compactación del CLI de Claude Code y los comandos `/compact` y `/clear` son **funciones del CLI**, manejadas de forma transparente. Son distintas del mecanismo de compactación beta separado de la _API_ de Anthropic (`compact-2026-01-12`, opcional vía configuración del SDK). Si solo usas el CLI, no tocas nada de eso — `/compact` y `/clear` son comandos normales, sin flags beta.

---

## 3. Un chat por tarea (no un mega-chat)

Por defecto, **una conversación por tarea o por unidad lógica de trabajo.** Cuando pases a algo genuinamente distinto, abre un chat nuevo.

¿Por qué no un mega-chat continuo para todo el día?

- Cada turno no relacionado que agregas hace que _todos los turnos futuros_ de ese chat carguen peso muerto (ver §2).
- La auto-compactación eventualmente resumirá y borrará las partes tempranas y detalladas que quizá todavía te importan.
- Un chat acotado es más fácil de retomar, auditar o pasarle a un compañero después — el transcript se lee como "lo que hicimos", no como "todo lo que toqué el martes".

No es por ser quisquilloso. Simplemente es más barato y más claro.

---

## 4. El "save gate" antes de cerrar un chat

Antes de cerrar, limpiar (`/clear`) o borrar una sesión, corre este chequeo de 10 segundos:

> **¿Hay alguna decisión, porqué o artefacto que esté SOLO en este chat?**

Si sí — externalízalo _primero_, y luego haz lo que quieras con el transcript:

- [ ] **Una decisión o su porqué** ("elegimos X sobre Y porque…") → un doc, un RFC (`rfcs/`), o un comentario en el código / descripción del PR.
- [ ] **Un diseño o plan duradero** → un RFC, un archivo de plan, o `operations/` para detalle tipo runbook.
- [ ] **Código / config funcional** → haz commit (o al menos stash/branch).
- [ ] **Una convención o preferencia personal que quieras reutilizar** → memoria (ver §9).
- [ ] **Conocimiento entre repos o relevante para el equipo** → docs del repo, _no_ memoria.

Si todo lo que importa ya vive en el repo o en la memoria, el transcript es ahora solo papel borrador. El save gate es el único hábito que hace seguro todo lo demás de este documento.

---

## 5. Cuándo usar `/compact` (a mitad de tarea, misma sesión)

Usa `/compact` cuando estés **a mitad de una tarea, en una sola sesión, y el contexto se esté poniendo pesado** pero aún necesitas el hilo para terminar _esta_ tarea.

- `/compact` resume la conversación actual **en el lugar** y guarda el resumen de vuelta en el transcript de la sesión — así que no es una pérdida permanente; el resumen se vuelve el historial de trabajo.
- Puedes pasar instrucciones de enfoque opcionales (`/compact enfócate en los cambios de la API`). _El modelo exacto de interacción no lo podemos afirmar con certeza — parece pasarse en línea como `/compact [instrucciones]`, pero trata la pista de enfoque como "mejor esfuerzo", no como garantía de lo que se conserva._
- **Lo que sobrevive una compactación y se recarga desde disco:** el `CLAUDE.md` raíz del proyecto, la memoria automática, el system prompt, y los cuerpos de skills invocadas (tope ~5 KB/skill, ~25 KB total).
- **Lo que NO sobrevive hasta que se vuelve a disparar:** reglas con alcance por ruta (frontmatter `paths:`) y `CLAUDE.md` anidados en subdirectorios — estos se recargan solo cuando Claude vuelve a leer un archivo en esa ruta. Así que tras un compact, si el comportamiento en un subdir se siente "raro", toca un archivo ahí para re-armar sus reglas.

**No** uses `/compact` como forma de cargar conocimiento _entre_ tareas. Recorta el historial de la tarea actual; no reemplaza el escribir las cosas (§4). Modelo mental: `/compact` cambia un costo único de resumen ahora por turnos más baratos durante el resto de esta tarea.

---

## 6. Cuándo empezar de cero / `/clear` (tarea nueva, o nuevo día)

Abre una conversación nueva — o usa `/clear` — cuando:

- Pasas a una **tarea nueva** no relacionada con el hilo actual.
- Es **un nuevo día** y de otro modo retomarías el chat de ayer — el caché de prompt está frío (§2), así que retomar te cobra el costo completo del contexto sin nada del ahorro del caché. Un chat fresco y acotado suele ser más barato y más claro.

Buena noticia sobre seguridad: **`/clear` NO borra nada.** Empieza un contexto fresco y vacío y etiqueta/guarda la conversación vieja para que siga siendo retomable (sigue en `claude --resume` y en `/resume`). Tanto `/clear` como `/compact` conservan el historial — `/clear` aparca la vieja bajo una etiqueta y te lleva a un contexto limpio; `/compact` resume la actual en el lugar. Así que echar mano de `/clear` es de bajo riesgo: obtienes un arranque fresco barato y conservas el rastro.

---

## 7. Cuándo BORRAR un transcript — y un one-liner seguro

Borrar es para transcripts **verdaderamente agotados**: el trabajo está externalizado (§4), no lo vas a retomar, y no tiene valor de auditoría/onboarding (lee §8 antes de echar mano de esto).

Qué hace realmente el borrado y dónde viven las cosas:

- Los transcripts de sesión son JSONL en `~/.claude/projects/<project>/<session-id>.jsonl`, donde `<project>` se deriva de la ruta del directorio de trabajo.
- **Borrar el `.jsonl` quita esa sesión del selector de `claude --resume`** — la lista de resume es solo un escaneo de los `.jsonl` existentes en ese directorio de proyecto. Sin archivo, sin entrada.
- Normalmente no _necesitas_ borrar: los transcripts se **borran solos a los 30 días por defecto** (`cleanupPeriodDays` en settings). El borrado manual es para "lo quiero fuera ya", no para limpieza de rutina.
- Los **artefactos de subagentes / workflows** de una sesión están en un directorio hermano junto al transcript: `~/.claude/projects/<project>/<session-id>/` (con `subagents/`, `workflows/`). Las corridas de workflows _pueden_ dejar también salidas transitorias en `/tmp` (locales a la máquina, auto-limpiadas) — no vale la pena perseguirlas, así que el snippet de abajo deja `/tmp` en paz y solo borra el transcript + ese directorio hermano.

### Encuentra la sesión actual, no la escribas a mano

Nunca escribas un session id de memoria — derívalo en tiempo de ejecución. El segmento `<project>` es la ruta de tu cwd con **cada carácter no alfanumérico** convertido en guion — puntos y barras por igual (p. ej. `/Users/tu/dev/.github` → `-Users-tu-dev--github`, fíjate en el doble guion). Para encontrar el transcript **más reciente** del proyecto actual:

```bash
# Project dir for the CURRENT working directory:
proj_dir="$HOME/.claude/projects/$(pwd | sed 's/[^a-zA-Z0-9]/-/g')"

# Most-recently-modified session in this project (likely the current one):
sid="$(ls -t "$proj_dir"/*.jsonl 2>/dev/null | head -1 | xargs -r basename | sed 's/\.jsonl$//')"
echo "project dir : $proj_dir"
echo "session id  : $sid"
```

> Verifica `$sid` contra la sesión que realmente quieres antes de borrar. Si tienes el id de un hook `SessionEnd` (§10), prefiérelo — es exacto.

### La limpieza segura, acotada a una sesión

Esto **primero imprime lo que borraría**, solo toca archivos que coincidan con ese único session id, y **nunca toca `memory/` ni ninguna otra sesión**. Revisa, y luego corre las líneas `rm` tú mismo.

```bash
proj_dir="$HOME/.claude/projects/$(pwd | sed 's/[^a-zA-Z0-9]/-/g')"
sid="${1:-$(ls -t "$proj_dir"/*.jsonl 2>/dev/null | head -1 | xargs -r basename | sed 's/\.jsonl$//')}"

# HARD GUARD — never proceed on an empty id (an empty $sid would collapse the
# paths below to whole directories). Abort loudly instead.
[ -n "$sid" ] || { echo "No session id resolved — aborting."; return 1 2>/dev/null || exit 1; }

echo "== would remove for session: $sid =="
ls -ld "$proj_dir/$sid.jsonl" "$proj_dir/$sid" 2>/dev/null   # transcript + its subagent/workflow artifacts

# --- only after eyeballing the above, run the removal yourself: ---
# rm -rf "$proj_dir/$sid.jsonl" "$proj_dir/$sid"
```

Salvaguardas incorporadas:

- **Guarda dura ante un id vacío** — si no se resuelve ninguna sesión, aborta, así que un objetivo nunca puede colapsar a un directorio entero.
- **Imprime antes de borrar** — la línea `rm` está comentada a propósito; revisa la salida de `ls` primero.
- Se **acota a un único session id** (`$proj_dir/$sid*`), así que otras sesiones quedan intactas.
- **Nunca referencia `memory/`** — tu memoria automática y tu `MEMORY.md` están fuera de alcance y persisten igual (§9).

> **Advertencia honesta.** Corre esto en una sesión de la que ya _saliste_, no en la que estás sentado. Si la misma sesión sigue abierta en otra terminal, el selector de resume puede no actualizarse hasta que esa sesión se cierre y su archivo se sincronice — no cuentes con la eliminación instantánea de una sesión viva.

---

## 8. Cuándo NO borrar

No te emociones borrando. Un transcript es _evidencia de trabajo_, y eso tiene valor real. **Consérvalo** cuando cualquiera de estas sea cierta:

- **El trabajo sigue en curso.** Obvio, pero: si podrías retomarlo, mantenlo retomable.
- **Aún no está externalizado.** Si el save gate (§4) no está completo, el chat sigue siendo la única copia. No borres la única copia.
- **Lo podrías retomar.** Es más barato retomar una sesión acotada que re-explicar el contexto desde cero — y dentro del mismo día el caché todavía puede ayudar.
- **Rastros de auditoría / "¿por qué hicimos esto?".** Las decisiones tomadas de forma interactiva, sobre todo las que tocan infra, seguridad, esquema, o cualquier cosa en territorio `nucleus-db` / RFC, vale la pena conservarlas para trazabilidad.
- **Valor de onboarding.** Un transcript limpio de "cómo construimos X" puede enseñarle a la siguiente persona más que un resumen pulido.
- **Rastros de PR o de depuración.** La conversación que produjo un fix o le dio forma a un PR es útil cuando un revisor pregunta "¿qué intentaste?" o cuando el bug reaparece.

Recuerda que los valores por defecto ya te protegen: la auto-limpieza a 30 días significa que rara vez _necesitas_ borrar manualmente. Ante la duda, **consérvalo** — y apóyate en `/clear` (§6), que te da un arranque fresco barato _sin_ destruir nada.

---

## 9. Memoria vs repo — qué va dónde

Ambas sobreviven entre sesiones y son **independientes de los transcripts de chat** — no se borran cuando borras un `.jsonl`. La división es por _audiencia_:

| Conocimiento | Dónde va | Por qué |
|---|---|---|
| Duradero para el equipo: decisiones, diseños, porqués, convenciones entre repos, runbooks | **Repo** — docs, `rfcs/`, planes, `operations/`, comentarios de código, descripciones de PR | El equipo lo necesita; debe ser revisable y descubrible, no atrapado en tu máquina |
| Personal: tus preferencias de trabajo, tus atajos, convenciones que le repites a Claude | **Memoria** (`CLAUDE.md`, memoria automática en `~/.claude/projects/<project>/memory/MEMORY.md`) | Reutilizable para _ti_ entre sesiones; sin valor forzárselo a los compañeros |

Cómo carga la memoria basada en archivos (para que sepas qué es "gratis" al inicio de la sesión):

- **Memoria automática:** las primeras **200 líneas o 25 KB de `MEMORY.md`** (lo que ocurra primero) cargan al inicio de la sesión. Los archivos por tema (`debugging.md`, `architecture.md`, …) se leen **bajo demanda**, no al arranque — así que mantén lo caliente cerca del tope de `MEMORY.md` y empuja el detalle a archivos por tema.
- **Los `CLAUDE.md` suben por el árbol de directorios** desde tu cwd, cargando desde `./` y `./.claude/`. Los archivos en subdirectorios cargan **bajo demanda** cuando Claude lee un archivo ahí. `CLAUDE.local.md` se anexa después de `CLAUDE.md` en cada nivel.
- Los settings (y por ende los hooks, §10) siguen una cadena de precedencia: **Managed > flags de CLI > Local (`.claude/settings.local.json`) > Proyecto (`.claude/settings.json`) > Usuario (`~/.claude/settings.json`)**. Los settings de tipo arreglo como `permissions.allow` se combinan entre scopes; los escalares toman el valor más específico.

> Regla práctica: **si a un compañero le sirve, va en el repo. Si solo te sirve a ti-del-futuro, la memoria está bien.**

---

## 10. Opcional, opt-in: un hook `SessionEnd` de recordatorio

**Totalmente opcional, opt-in, personal.** Si te gusta la idea de que te _recuerden_ el comando de borrado seguro cuando termina una sesión, puedes agregar un hook `SessionEnd` a tu `~/.claude/settings.json` **personal**. **Imprime** un comando acotado a la sesión y derivado en tiempo de ejecución para que lo revises y lo corras tú mismo — **nunca corre `rm`.**

```jsonc
// ~/.claude/settings.json  (PERSONAL scope — opt-in, not committed, not org-mandated)
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "tp=$(jq -r '.transcript_path // empty'); [ -n \"$tp\" ] && printf 'Chat ended. If this work is saved (repo/memory), review then delete it:\\n  rm -rf \"%s\" \"%s\"\\n' \"${tp%.jsonl}\" \"$tp\""
          }
        ]
      }
    ]
  }
}
```

Notas y límites honestos:

- **`SessionEnd` se dispara cuando una sesión termina** y recibe un **payload JSON por stdin** — `session_id`, `transcript_path`, `cwd`, `hook_event_name`, y un `reason` (`clear` / `resume` / `logout` / `prompt_input_exit` / …). El hook lee `transcript_path` con **`jq`** y deriva el directorio + el transcript en tiempo de ejecución — **nada está hardcodeado.** (Necesita `jq` instalado.)
- **Construye el comando pero nunca ejecuta el borrado.** A propósito: tú sigues siendo quien decide, después del save gate (§4).
- **Un hook no puede conversar ni juzgar.** Los hooks `Stop` y `SessionEnd` solo corren comandos de shell y se disparan _después_ de que Claude termina, así que no pueden razonar sobre si tu trabajo está realmente guardado. Es un recordatorio tonto pero útil; el juicio es tuyo.
- _Advertencia de visibilidad — trátalo como experimental._ Si la salida estándar del hook se te muestra al final de la sesión depende de tu versión de Claude Code. Si no la ves, haz que el comando emita un `systemMessage` en su lugar — un hook puede imprimir JSON como `{"systemMessage":"…"}`, que es el canal documentado para texto mostrado al usuario.

Si no quieres el recordatorio, no hagas nada — nada de esto es obligatorio.

---

## 11. Cuando abres varios agentes — gasto multi-agente

Todo lo de arriba es sobre un _solo_ chat. En el momento en que empiezas a abrir sub-agentes — llamadas `Agent`, `fork`s, o etapas de `Workflow` — entra una segunda curva de costo, y escala más rápido de lo que uno espera. Medimos nuestro propio uso (auditoría interna, jun-2026): casi todo el gasto en sub-agentes venía de tres cosas evitables. No se trata de tacañería — un fan-out más ajustado normalmente da _mejor_ trabajo: menos ruido en el contexto, agentes más enfocados.

**La fórmula del costo:** gasto multi-agente = **modelo × contexto que carga cada agente × ancho del fan-out.** Casi todo sobrecosto es uno de esos tres mal calibrado, no "los agentes son caros" en general.

**Tres ganancias para todos (aplícalas desde hoy):**

1. **Usa el modelo más barato que haga el trabajo.** Haiku para lo mecánico (grep, listar, convertir formato); **Sonnet para el grueso** (buscar, leer, explorar, transformar, resumir); **Opus solo para razonamiento difícil** (arquitectura, depuración, el juicio o la síntesis final). Poner Opus en una búsqueda o en una revisión archivo-por-archivo cuesta ~5× sin ganar calidad — en nuestra auditoría fue la mayor fuga (~70% de la salida de sub-agentes era Opus, casi toda en pasos mecánicos).
2. **Un chat enfocado por tarea — y prefiere un agente _fresco_ sobre un `fork`.** Un `fork` hereda _toda_ la conversación, así que re-paga el transcript completo en su primer turno (la trampa de §2, un nivel más abajo). Abre fresco cuando el agente no necesita todo el ida y vuelta.
3. **Ajusta el ancho del fan-out a la tarea.** Tres exploradores que cubren el terreno valen más que diez. Y si ya delegaste una búsqueda, no la repitas tú en paralelo — se paga doble.

**Si orquestas con Workflows (avanzado):**

- **Revisión por ítem = Sonnet, no Opus.** "Sonnet construye cada archivo + Opus revisa cada archivo" _parece_ prudente, pero multiplica Opus por la cantidad de archivos. Deja Sonnet (o Haiku) en la revisión por ítem y reserva **un solo** Opus para la síntesis o el veredicto sobre todo el conjunto.
- **Menos agentes, más gruesos.** Un agente que procesa 5 archivos amortiza el costo de "calentar" su contexto; cinco agentes de 1 archivo lo pagan 5 veces. Agrupa ítems por agente y mantén liviano el contexto de cada uno.
- **`effort: 'low'`** en las etapas mecánicas; reserva el effort alto para verificar o sintetizar.
- **Profundidad de verificación según el riesgo:** un paso para un chequeo rápido; el panel adversarial de 3–5 votos es para "audita esto a fondo", no para trabajo rutinario.

**El gut-check de 4 preguntas antes de abrir un agente:**

1. ¿De verdad necesito un agente, o lo resuelvo yo directo?
2. ¿Fresco o `fork`? (fresco por defecto)
3. ¿Cuál es el modelo más barato que sirve?
4. ¿El ancho del fan-out está ajustado a la tarea?

---

## 12. Hoja de referencia rápida

| Situación | Haz esto | ¿Destruye algo? |
|---|---|---|
| A mitad de tarea, una sesión, contexto pesado, necesitas terminar _esta_ tarea | **`/compact`** (opcionalmente con una pista de enfoque) | No — resume en el lugar, guardado en el transcript |
| Tarea nueva no relacionada / nuevo día (caché frío) | **`/clear`** o abre un chat nuevo | No — el chat viejo queda aparcado y retomable |
| Tarea lista, conocimiento externalizado (§4), sin valor de auditoría/onboarding, no la retomarás | **Borra** el `.jsonl` (usa el one-liner de §7; revisa primero) | Sí — lo quita del selector de resume |
| Trabajo en curso, aún no externalizado, podrías retomarlo, o tiene valor de auditoría/PR/depuración/onboarding | **Consérvalo** (la auto-limpieza lo maneja a los 30 días) | — |
| Quieres un empujón al final de la sesión hacia el comando de borrado | **Opta por el hook `SessionEnd` de §10** (settings personales) | No — solo imprime |
| Abres sub-agentes o un fan-out de Workflow | **El modelo más barato que sirva** (Haiku/Sonnet para el grueso, Opus solo para verificar/sintetizar), **fresco sobre `fork`**, ancho ajustado a la tarea (§11) | — |

**El hilo conductor:** pon el conocimiento duradero donde sobrevive (repo + memoria), mantén cada chat acotado a una tarea, y luego trata el transcript como barato. Compacta para terminar, limpia (`/clear`) para cambiar, conserva ante la duda, borra solo cuando esté verdaderamente agotado.

---

_¿Preguntas, o crees que una heurística de acá está mal para cómo trabaja tu equipo de verdad? Abre un PR contra este archivo — es una recomendación viva, no un reglamento._
