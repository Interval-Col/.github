<!--
INCIDENT POSTMORTEM TEMPLATE — copy into `Interval-Col/operations/incidents/`
as `YYYY-MM-<host-or-service>-<slug>.md`. Use after any incident that took a
service down, risked data, or required manual recovery.

CANONICAL FRONTMATTER (resolves the 2026-06 drift — the two earlier incidents
disagreed on key names). Use these exactly:
  status   — open | mitigated | resolved
  owner    — the incident owner (one github handle)
  created  — date the incident was opened (YYYY-MM-DD)
  updated  — bump on every edit (YYYY-MM-DD)
  severity — low | medium | high | critical
  issues   — LIST of tracking issues (incidents commonly spawn several):
             `Interval-Col/operations#NN`. (Plans use singular `issue:`;
             incidents use `issues:` because remediation usually forks.)
  remediation — the durable-remediation owner (one github handle)
  target   — durable-remediation target date (YYYY-MM-DD)
  language — note (incidents are typically Spanish body, code/terms in English)

BODY: Spanish body is fine and common for incidents (the team reads these under
pressure). Keep the marker conventions table, the summary table, the timeline,
the per-step Done-when ✅ and Checkpoints 🚦.

Delete this comment when you start filling in.
-->
---
status: open
owner: <github-handle>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
severity: <low | medium | high | critical>
issues:
  - Interval-Col/operations#<NN>
remediation: <github-handle>
target: <YYYY-MM-DD>
language: Español · términos técnicos y de código en inglés
---

# Incidente — <título corto del fallo> · <host/servicio> (<YYYY-MM-DD>)

> **Resumen ejecutivo.** <4–8 líneas en español: qué falló, en qué host/servicio,
> el disparador inmediato, el impacto (qué se cayó), la resolución inmediata, y
> la remediación durable con su responsable y meta. Cierra con la línea de PHI:
> **"Sin pérdida de datos ni exposición de PHI."** (o lo que aplique — y si hubo
> exposición, dilo explícitamente y enlaza el proceso de notificación).>

---

## Tabla de resumen del incidente

| Campo | Detalle |
|---|---|
| **Fecha y hora (aproximada)** | <YYYY-MM-DD HH:MM> |
| **Host afectado** | `<host>` · `<ip>` |
| **Servicio caído** | `<servicio/contenedor>` |
| **Síntoma observado** | <qué vio el equipo: errores, códigos HTTP, dashboards vacíos> |
| **Causa raíz** | <la causa estructural, no el síntoma> |
| **Disparador inmediato** | <el evento puntual que detonó el fallo> |
| **Qué NO fue la causa** | <hipótesis descartadas explícitamente — evita re-investigar lo mismo> |
| **Recurrencia** | <¿pasó antes? ¿dónde, cuándo? enlaza el incidente previo> |
| **Severidad** | <low/medium/high/critical> — <impacto en una frase>. <línea PHI>. |
| **Resuelto** | <Sí/No> (resolución inmediata por @<handle>, <fecha>). Remediación durable: <#NN>. |

---

## Convenciones de marcadores

| Marcador | Significado |
|---|---|
| 🤖 **Sonnet-ejecutable** | Un agente (Claude Sonnet) puede ejecutar y verificar el paso de forma determinista. |
| 👤 **Junior** | Lo ejecuta la persona, con verificación explícita. |
| 🛑 **Humano** | Requiere consola física/iLO, ventana de mantenimiento o aprobación de @<owner>; un agente NO lo hace. |
| 💡 **Aprendizaje** | Explica el concepto o el porqué. |
| ✅ **Hecho-cuando** | Definición de terminado, verificable línea por línea. |
| 🚦 **Punto de control** | Detente y muestra la evidencia nombrada a @<owner>. |

---

## Cronología del incidente

| Momento | Evento |
|---|---|
| Antes del incidente | <estado previo / condición latente> |
| Acumulación gradual | <lo que se fue degradando sin alerta> |
| Disparador | <el evento puntual> |
| Fallo | <cómo se propagó> |
| Síntomas en la pila | <qué servicios dependientes cayeron> |
| Resolución inmediata | <qué hizo @<handle> para restablecer el servicio> |
| Estado post-resolución | <estado actual; qué queda pendiente> |

---

## Resolución inmediata (<YYYY-MM-DD> · @<handle>)

> El procedimiento genérico y reutilizable vive en el runbook
> `operations/runbooks/<runbook>.md`. Aquí se documenta lo que se ejecutó, para
> reproducibilidad.

### Paso 1 — <verificar estado>

👤 **Junior**

```bash
<comando>
# Esperado ANTES: <…>
# Esperado DESPUÉS: <…>
```

### Paso 2 — <acción correctiva>

👤 **Junior**

```bash
<comando>
```

💡 **Aprendizaje — <concepto>.** <2–4 líneas explicando el porqué.>

✅ **Hecho-cuando (resolución inmediata):**
- <criterio verificable 1 — un comando y su salida esperada>
- <criterio verificable 2>

🚦 **Punto de control A.** Mostrar a @<owner>:
1. <evidencia 1>
2. <evidencia 2>

---

## Remediación durable

> El incidente inmediato está resuelto, pero <la causa raíz estructural
> persiste>. Ítems de remediación:

### operations#<NN> — <título de la remediación>

**Responsable:** @<handle> · **Meta:** <YYYY-MM-DD>

1. 🛑 **<aprobación / ventana de mantenimiento, si aplica>** — <por qué>.
2. 👤 **Junior** — <pasos, enlazando la Parte X del runbook>.

💡 **Aprendizaje — <concepto>.** <2–4 líneas.>

✅ **Hecho-cuando (#<NN>):**
- <criterio verificable 1>
- <criterio verificable 2>

🚦 **Punto de control B.** Mostrar a @<owner> antes de cerrar #<NN>:
1. <evidencia 1>
2. <evidencia 2>

---

## Práctica adoptada (decisión post-incidente)

> Solo si el incidente cambia una práctica org-wide. Lista lo que la org adopta
> formalmente a partir de aquí, y dónde queda codificado (política / runbook).

1. **<práctica 1>.**
2. **<práctica 2>.**

---

## 💡 Aprendizajes

1. **<lección 1 — un titular en negrita>.** <2–4 líneas, concreto, no genérico.>
2. **<lección 2>.** <…>

---

## Fuera de alcance

- <qué deliberadamente no se toca / se evalúa aparte como RFC>

---

## Decisiones

**Resueltas durante el incidente:**

- **<decisión>** — <qué se decidió y por qué>. *(YYYY-MM-DD.)*

---

## Referencias

- **Runbook:** `operations/runbooks/<runbook>.md`
- **Incidente previo (si aplica):** <enlace>
- **operations#<NN>:** <título> · @<handle> · meta <YYYY-MM-DD>

---

## Glosario

| Término (EN) | Explicación (ES) |
|---|---|
| `<término>` | <explicación en una o dos líneas> |
