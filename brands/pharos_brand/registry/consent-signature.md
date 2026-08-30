# Pháros consent signature — ConsentSignature (RFC 0008 · RFC 0030)

La **superficie de firma** de un consentimiento informado — **una sola para los tres
momentos**: recepción (paciente nuevo → tratamiento de datos), banco de toma de
muestras (bacteriólogo + paciente, por orden) y el kiosco de tablet
(`consent-kiosk`, `document-signing/kiosk/`). Muestra el documento, captura la
firma —del paciente o de su **representante legal**, con sus datos— y las
declaraciones que el formulario imprime (conservación de muestras, imágenes
microscópicas), y **emite el cuerpo canónico de 13 campos** de
`POST /pdf_form/fill/{id}` del servicio compartido `api-document-signature`.
Nació de las dos implementaciones vivas (`informed-consent-nuxt`, 6 campos;
`sample-take-nuxt`, 13) tomando de cada una lo que la otra no tenía, para que
**no exista una tercera copia** (RFC 0030 §1: dos cuerpos ya divergieron y
produjeron consentimientos sin episodio).

> Este es el **widget** (presentación pura). El **transporte** — resolver el
> formulario y el PDF en blanco, enviar el cuerpo con el token de la persona,
> crear/cerrar la `signing_request`, la política de revelado de PHI y el error
> con dueño — es de cada app, igual que el corte `send`/`probe` de
> `PharosHelpChat`. El widget nunca hace fetch y nunca escribe.

## What's in the registry (synced verbatim)

| Entry | Path | What it is |
|---|---|---|
| `ConsentSignature` | `app/components/ui/consent-signature/ConsentSignature.vue` | encabezado (formulario, paciente, orden), documento en `<iframe>`, firmante (paciente / representante legal con nombre, tipo y número de documento; ciudad de expedición), declaraciones por formulario, pad, nota del bacteriólogo, estados cargando / error / enviando, «No firma» |
| `SignaturePad` | `app/components/ui/consent-signature/SignaturePad.vue` | `<canvas>` con pointer events, DPR-aware; `clear()`, `isEmpty()`, `toPngBase64()` (**sin prefijo data-URL** — el servicio hace `b64decode` tal cual) |
| tipos | `app/components/ui/consent-signature/types.ts` | `ConsentFormDescriptor`, `ConsentSubject`, `ConsentBacteriologist`, **`ConsentSignaturePayload`** (los 13 campos), `IDENTIFICATION_TYPES` |
| barrel | `app/components/ui/consent-signature/index.ts` | exporta componentes + tipos |

**Deps (per adopting app):** ninguna nueva — `lucide-vue-next` y los primitivos
`ui/button`, `ui/checkbox`, `ui/input`, `ui/label`, `ui/select` que toda app
adoptante ya sincroniza (companions). El pad es propio: `vue-signature-pad`
se queda en los fronts viejos.

**Tokens:** sólo contrato de tokens (`--border`, `--card`, `--primary`,
`--destructive`, `--muted-foreground`, …) — sin hex, re-acenta limpio bajo
cualquier `.theme-*`. El trazo usa `currentColor` del canvas (`text-foreground`).

## Per-app config

| Prop | Type | Default | Notes |
|---|---|---|---|
| `form` | `ConsentFormDescriptor` | — | **required**; la app lo resuelve del catálogo del servicio (`/pdf_forms`, `/pdf_forms/by_order`). Decide qué controles aparecen: representante legal (los 13 formularios de banco), bacteriólogo, declaraciones |
| `subject` | `ConsentSubject` | — | **required**; tipo y número de documento (PHI — se enmascaran según `revealed`), nombre y ciudad de expedición si la app los tiene |
| `documentUrl` | `string \| null` | — | **required**; el PDF en blanco como URL que el navegador pueda pintar (blob/object URL que la app construyó desde `GET /pdf_form/view/{name}`). `null` = cargando: no se puede firmar lo que no se ha leído |
| `documentError` | `string \| null` | `null` | UNA frase con dueño si el documento no cargó |
| `orderNumber` | `number \| null` | `null` | la orden del episodio (banco); viaja como `order_number` |
| `entityServed` | `string \| null` | `null` | pre-llena `entity_served` |
| `bacteriologist` | `ConsentBacteriologist \| null` | `null` | sólo se muestra quién firma además; la imagen la pone el servicio desde el perfil SSO del token |
| `submitting` | `boolean` | `false` | la app está enviando: controles deshabilitados, botón en «Guardando…» |
| `error` | `string \| null` | `null` | UNA frase ya mapeada por la app, con su dueño — nunca la línea cruda de HTTP |
| `revealed` | `boolean` | `true` | política de revelado de PHI, decidida por la app (p. ej. `useIdlePrivacy` en lab-qc) |
| `maskedText` | `string` | `'•••'` | texto de máscara |
| `declinable` | `boolean` | `true` | muestra «No firma»; la app responde el emit registrando el `declined` |
| `title` | `string` | `'Firma del consentimiento'` | encabezado |
| `density` | `'escritorio' \| 'tablet'` | `'escritorio'` | **a qué distancia se mira la superficie.** `escritorio` = un empleado sentado, con ratón, dentro de una app con barra lateral (lab-qc, Admisiones). `tablet` = un dispositivo que se le **entrega** a un paciente: de pie, con el dedo, a veces con una sola mano (consent-kiosk) |

### `density: 'tablet'` — qué cambia, y por qué no es cosmético

- **El área de firma manda sobre el documento** (`flex-[2]` con piso de 180 px,
  contra `flex-[3]` del documento). Una franja delgada se firma mal: el trazo se
  sale del área y hay que repetirlo, de pie y con el paciente esperando. El pad
  sube de 200 a 260 px. ⚠️ El pad lleva su alto como **estilo en línea**, así que
  una clase `flex-1` encima no hace nada — el alto se pasa por `height`.
- **El documento deja de medir 384 px fijos** y ocupa el resto del alto. En una
  tablet apaisada, 384 px fijos dejaban media pantalla en blanco.
- **Nada táctil por debajo de 56 px** y el texto sube a 18–20 px.
- **La tarjeta desaparece** (sin borde ni relleno propio): en un kiosco la
  superficie ES la pantalla, y la app pone el fondo.

El widget no adivina cuál es: la app lo sabe y lo declara.

**Emits:**

| Emit | Payload | Qué hace la app |
|---|---|---|
| `sign` | `ConsentSignaturePayload` | `POST /pdf_form/fill/{form.id}` con el token de la persona (+ `signing_request_id` si viene de una solicitud); el servicio guarda el PDF, registra el `signing_event` (SHA-256) y cierra la solicitud |
| `decline` | — | `POST /signing_requests/{id}/decline`: un rechazo es un resultado de primera clase, no una ausencia |

**El cuerpo emitido es el ÚNICO contrato.** Trece campos, `snake_case`, tal como
`PDFFormDataSchema` del servicio; `signature_image` y
`legal_representative_signature` en PNG base64 sin prefijo. Cuando firma el
representante, el mismo trazo va en ambos campos (contrato heredado de
`sample-take-nuxt`). Ninguna superficie manda otro cuerpo.

## PHI

`subject.identificationNumber`, `subject.fullName` y el nombre del bacteriólogo son
PHI: el widget los recibe ya resueltos y los enmascara según `revealed`; **la
política es de la app**. El trazo de la firma no se persiste en el navegador ni
se muestra fuera del canvas. El link prefirmado que devuelve el `fill` **no**
debe viajar a la tablet (RFC 0030 dossier §4): la app lo ignora o lo sirve por
su propio API.

## Adopters

| App | Surface | Transport |
|---|---|---|
| `document-signing/kiosk/` (`consent-kiosk`) | tablet de recepción y de banco | directo al servicio con el token del terminal; lista de `signing_request` por estación |
| `admission-patient` | ingreso de paciente nuevo (crea la solicitud) | pendiente (RFC 0030 Fase 3) |
| `pharos-lis/lab-qc` | estación de toma de muestras (`call-next` crea la solicitud) | pendiente (RFC 0030 Fase 3) |

Prototipo: `design-studio` `/componentes/consent-signature` (design-studio#55).
Gate de adopción: los genéricos `check-registry-drift` / `check-registry-fresh`.
