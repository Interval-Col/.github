# Pháros · eventos — reporte y panel del proceso (plan Pháros · Organización, 2.4)

El componente compartido para **reportar un evento** (no conformidad, queja u oportunidad de
mejora) desde cualquier app Pháros, y el panel **«Eventos de mi proceso»** donde trabaja el equipo
del proceso. Una sola definición para que no haya una copia por app (mismo argumento que
`PharosHelpChat`, RFC 0017). Este README **es su especificación**.

> Es el **widget**. El **servidor** de los eventos es «Pháros · Organización»; la app anfitriona no
> habla con él directo: lo hace su propio backend (BFF). RFC 0013 / RFC 0017.

## Qué trae (se sincroniza verbatim)

| Entrada | Ruta | Qué es |
|---|---|---|
| `ReportarEvento` | `app/components/ui/eventos/ReportarEvento.vue` | el **botón** («Reportar un evento») y el panel lateral que lo abre; lleva el formulario |
| `EventoFormulario` | `app/components/ui/eventos/EventoFormulario.vue` | el **formulario**, suelto, para montarlo en una página propia (Organización) |
| `EventosDeMiProceso` | `app/components/ui/eventos/EventosDeMiProceso.vue` | el **panel** del equipo del proceso: lista con estado y plazo |
| tipos y textos | `app/components/ui/eventos/types.ts` | enums, etiquetas, mensajes de error (todo en «tú») |
| barrel | `app/components/ui/eventos/index.ts` | exporta lo anterior |
| cliente | `app/lib/eventosApi.ts` | `crearEventosApi({ apiBase, headers?, fetch? })`: las tres llamadas, con la base validada |

**Dependencias por app:** ninguna nueva. Usa `ui/button`, `ui/badge`, `ui/sheet`, `lib/utils` y
`lucide-vue-next`, que toda app adoptante ya sincroniza (compañeros declarados en
`sync-pharos-registry.sh`). Solo contrato de tokens: sin hex, sin paleta cruda.

## Props que pasa la app anfitriona

| Prop | Tipo | Obligatoria | Notas |
|---|---|---|---|
| `apiBase` | `string` | sí | ruta **relativa al origen** de la propia app, `/<app>/api`; el componente añade `/eventos`. Se rechaza lo que no sea una ruta relativa (esquema, `//`, host, `..`) |
| `app` | `string` | sí | nombre de la app, solo para mostrar («Abierto desde»). El servidor deriva la app de origen de la autenticación, **nunca del cuerpo** |
| `pantalla` | `string` | sí | identificador de la pantalla (minúscula inicial; minúsculas, dígitos, `.`, `_`, `-`; hasta 64). Viaja como `pantalla_origen`; si no cumple el patrón se omite |
| `procesos` | `{ codigo, nombre }[]` | sí | el mapa de procesos, que la app trae de Organización |
| `ordenSugerida` | `string \| null` | no | la orden que la pantalla tiene abierta. **Sugerencia**: solo viaja si quien reporta marca la casilla. Solo se acepta si son dígitos; la validación de fondo es del servidor y de la app |
| `sedeInicial` | `Sede \| null` | no | sede de la sesión, si la app la conoce |
| `avisoQueja` | `string` | no | texto del aviso de tratamiento de datos para quien se queja. Por omisión, un texto genérico (**pendiente el texto oficial**) |
| `headers` | `() => Record<string,string>` | no | encabezados extra por llamada (p. ej. el token CSRF). Nunca el secreto de servicio: es del BFF |

`EventosDeMiProceso` recibe `apiBase`, `headers` y `mostrarOrden` (**apagado por omisión**: la orden no
se muestra a menos que la app lo pida). Emite `abrir(id)` y `error`. `ReportarEvento` y
`EventoFormulario` emiten `reportado({ id, consecutivo, pendienteDeRevision })`, `error` y, el
formulario, `cancelar`.

## Qué dice el formulario y qué viaja

Campos: **tipo** (no conformidad / queja / oportunidad de mejora), **proceso**, **sede**, **¿qué
pasó?** (texto libre), **fecha de ocurrencia**, **fecha en que te enteraste**, **¿llegó a alguien?**
(sí / no / no sé), **seguridad del paciente** (sí / no) y, solo si hay sugerencia **y se confirma**, la
**orden de servicio**. Si el tipo es **queja**: nombre de quien se queja, **un** medio de contacto
(correo o teléfono) y el aviso, que hay que aceptar.

Reglas que el componente sostiene (no son opciones):

1. **La orden no viaja sin confirmar.** Sin marcar la casilla, el cuerpo ni siquiera lleva la llave `orden_servicio`.
2. **«No escribas nombres ni documentos»** va junto al texto libre y no se puede cerrar.
3. **El rechazo del portón no devuelve el texto.** Con un 422 de datos de pacientes se pintan los
   **nombres de las reglas** y se conserva lo escrito para que la persona lo corrija.
4. **El contacto de una queja** va en su propia llamada, después de crear el evento, y sale del estado del componente apenas se envía.
5. Las fechas viajan **con zona horaria** (instante ISO); el servidor rechaza las que no la traen.
6. El navegador **solo** llama a `${apiBase}/eventos…`. Nada más.

## Rutas que el BFF de la app anfitriona debe exponer

Todas bajo `<apiBase>/eventos` (misma ruta de la app; el BFF reenvía a Organización con su
secreto de servicio y el token de la persona, y deriva de ahí quién reporta y la app de origen).
La orden de servicio viaja **solo en el cuerpo** de un reporte: nunca en una URL, un filtro, un log ni un mensaje de error.

| Método | Ruta | Cuerpo | Respuesta | Quién la llama |
|---|---|---|---|---|
| `POST` | `/eventos` | `ReporteEnvio` (abajo) | `201` con `{ id, consecutivo, pendiente_de_revision, … }` | formulario |
| `PUT` | `/eventos/{id}/contacto` | `{ nombre, medio: "correo"\|"telefono", contacto, aviso_aceptado: true }` | `204` sin cuerpo | formulario, solo si el tipo es queja |
| `GET` | `/eventos?vista=mis_procesos` | — | `200` con una lista de `ResumenEvento`, sin texto libre | panel |

`ReporteEnvio`: `tipo` · `proceso_codigo` · `sede` · `descripcion` (1–4000) · `fecha_ocurrencia` ·
`fecha_conocimiento` (ambas con zona) · `llego_a_alguien` (`si`/`no`/`no_se`) · `seguridad_paciente`
(bool) · `pantalla_origen` (opcional) · `orden_servicio` (opcional, solo confirmada). Cuerpo estricto:
una llave desconocida es 422. Valores de `tipo`: `no_conformidad`, `queja`, `oportunidad_mejora`;
de `sede`: `oviedo`, `viva_palmas`, `domicilios`, `sabaneta`.

`ResumenEvento`: `id` · `consecutivo` · `tipo` · `estado` · `proceso_codigo` · `sede` · `severidad` ·
`urgente` · `oculto` · `creado_en`; `plazo` (fecha ISO) es **opcional**: el panel lo pinta si llega.

### Códigos de error que el BFF debe pasar tal cual (mismo código, mismo cuerpo)

| Código | Cuándo | Qué hace el componente |
|---|---|---|
| `401` | sin sesión | «Tu sesión terminó…» |
| `403` | sin permiso de reportar | «No tienes permiso…» |
| `404` | el módulo de eventos está apagado en Organización | «Este módulo todavía no está disponible.» |
| `422` con `detail: { mensaje, reglas: [...] }` | **el portón de datos de pacientes rechazó el texto** | pinta los nombres de las reglas y conserva el texto |
| `422` con `detail: { errores: [{ codigo, campo, mensaje }] }` | validación de negocio (proceso desconocido, fecha futura, …) | marca los campos señalados y pinta el primer mensaje |
| `503` | **no están las reglas del portón**: no se guardó nada | «Ahora mismo no podemos revisar el texto…» |
| red caída | — | «No pudimos conectar…» |

Un `4xx` con mensaje propio del servidor (texto plano, hasta 300 caracteres) gana sobre el texto
cableado; el cuerpo de un `5xx` nunca se pinta. Un reporte guardado sin poder revisar el texto
responde `201` con `pendiente_de_revision: true` y el componente lo dice.

## Montaje

```vue
<ReportarEvento
  api-base="/mi-app/api"
  app="Pháros LIS"
  pantalla="control-calidad.liberacion"
  :procesos="procesos"
  :orden-sugerida="ordenAbierta"
/>
<EventosDeMiProceso api-base="/mi-app/api" @abrir="(id) => router.push(`/eventos/${id}`)" />
```

`ReportarEvento` va en el **pie del sidebar**; `EventosDeMiProceso` en la página del proceso.
Adopción: `scripts/sync-pharos-registry.sh --add components/ui/eventos/ReportarEvento.vue` (trae sus
compañeros), `--add components/ui/eventos/EventosDeMiProceso.vue` y `--add lib/eventosApi.ts`.

## Fuera de este componente

La bandeja global (Calidad y Cumplimiento), el detalle de un evento, el análisis, las acciones y el
cierre son de «Pháros · Organización» y no viajan por aquí. Este componente tampoco guarda nada en el
navegador: ni el borrador, ni el contacto.
