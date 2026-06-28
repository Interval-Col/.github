---
description: Capture what shipped this session as a dated business-framed bullet in ~/lch-strategic/ceo-captures.md. Spanish capture prompt, English meta. Runs from any repo.
---

# /ceo-capture — log a session's engineering output for the board

You are capturing what shipped in this session as a **one-line business-framed
entry** in the CEO/board capture ledger `~/lch-strategic/ceo-captures.md`.
This is the lightweight, per-session analog of `/board-brief`. Run it at
session end (or any point worth logging), from any repo or folder.

Optional argument: `$ARGUMENTS` is a short hint about what moved
(e.g. `admission prod landing`, `tariff-chain fee-set`). If empty, derive
from the git log.

**BOUNDARY — always enforce, no exceptions:**
- **NO PHI ever.** Structure + aggregates + business narrative only.
- Business numbers (revenue, EBITDA, FCF, cash) are **hand-entered by German
  from lch-strategic** — never derived from `~/dev` or any database.
- The ledger is **APPEND-ONLY** — never rewrite or delete existing lines.

## 0 · Scope

This command captures engineering progress in **business terms for the board**.
It runs from any repo (user-level command). The file write is done by **this
interactive driving session** — there is no workflow sandbox here; the driving
session has filesystem access and performs the append directly.

## 1 · Gather — see what shipped this session

Run the following from the **current working directory** (or the repo most
active this session) to get a concise picture of what moved:

```bash
git log --since="8 hours ago" --oneline --decorate
```

If the session spanned multiple repos, scan the most relevant one (or ask
German which repo to use). Also pull recently merged PRs if useful:

```bash
gh pr list --author @me --state merged --limit 10 \
  --json number,title,repository,mergedAt
```

Summarize in **1–2 lines** what changed: which repo, what feature/fix/deploy.
Do NOT copy commit messages verbatim — translate to business-legible language
(e.g. "se activó el rol finance_user en prod DB", not
"feat: nucleus-db role provisioning step 3").

## 2 · Ask German for the business framing (in Spanish)

Prompt German with the following (adapt to what you found in step 1). Keep
the ask to **1–3 lines**; don't force a number.

---

**Prompt to show German (in Spanish):**

> Lo que moví esta sesión: _<tu resumen 1–2 líneas del paso 1>_.
>
> Para el registro ejecutivo necesito tu encuadre de negocio (breve):
>
> 1. **¿Qué se movió?** (una línea, en términos de negocio — no de código)
> 2. **¿Sobre qué apuesta estratégica?** — elige la que mejor aplica.
>    **Las que normalmente mueve la ingeniería:**
>    - Pháros · productización del conocimiento _(de-concentración pura)_
>    - Habilitador · decomisión COBOL + plataforma de datos
>    - Biuman · lab deportivo
>
>    **Otras apuestas del tablero** (por si capturas un movimiento no-código):
>    Molecular/ThyroidPrint · Centro Médico ambulatorio · Sede Oviedo · Ecoparking ·
>    Turismo médico · 5 sedes propias · _(u otra que identifiques)_
> 3. **¿Por qué le importa a la junta?** (una línea — impacto en negocio,
>    riesgo reducido, cliente ganado, margen, etc.)
> 4. **Referencia opcional** — PR#, issue#, o cifra (ej. "917K filas
>    migradas"). Puedes omitirla.

---

Wait for German's answers before proceeding to step 3. Do not fabricate
business framing — if German skips a field, leave it as `<sin dato>` rather
than guessing.

## 3 · Append the dated bullet to ~/lch-strategic/ceo-captures.md

Construct the bullet using German's answers from step 2:

```
- **YYYY-MM-DD** · _<repo/área>_ · **Qué se movió:** <1 línea> · **Apuesta:** <Pháros productización | Biuman | habilitador COBOL | …> · **Por qué importa (junta):** <1 línea> · _ref:_ <PR#/issue#/opcional cifra>
```

Then append it to `~/lch-strategic/ceo-captures.md` under the correct
`## YYYY-MM` month header. Follow these rules exactly:

1. **If the file does NOT exist** — create it with the full header block,
   the current month section, and the bullet:

   ```markdown
   # CEO captures — bitácora ejecutiva (append-only)

   > Capturas por sesión (`/ceo-capture`). Una viñeta fechada por captura. Insumo del `/board-brief`
   > semanal. SIN PHI; cifras de negocio se ingresan a mano, nunca se derivan.

   ## YYYY-MM
   - **YYYY-MM-DD** · _<repo/área>_ · **Qué se movió:** … · **Apuesta:** … · **Por qué importa (junta):** … · _ref:_ …
   ```

2. **If the file exists but the current `## YYYY-MM` header is absent** —
   append the header + bullet at the end of the file.

3. **If the file exists and the current `## YYYY-MM` header is present** —
   append the bullet immediately below the last existing bullet under that
   header (before the next `##` section, or at end-of-file if it is the
   last section).

**APPEND ONLY. Never rewrite, truncate, or delete any existing line.**

Perform the write via Bash (or the Write/Edit tool) in the driving session:

```bash
# Use shell append (>> never >) — safe only when creating a new file or
# appending after finding the correct insertion point via a script.
# For inserting mid-file (before the next ## header), use the Edit tool
# with a precise old_string/new_string match rather than raw shell >>
# to avoid clobbering adjacent sections.
```

## 4 · Report

Tell German:
- The **appended line** (full text, verbatim).
- The **file path**: `~/lch-strategic/ceo-captures.md`.
- Confirm: "APPEND-only — ninguna línea existente fue modificada."

Example report:

> Captura registrada en `~/lch-strategic/ceo-captures.md`:
>
> `- **2026-06-28** · _finance-lch_ · **Qué se movió:** primer app en producción en nucleus-db · **Apuesta:** Pháros productización · **Por qué importa (junta):** sienta la base de datos compartida que habilita la separación de tenants · _ref:_ PR#21`

## 5 · Future option — Stop hook (document only; do NOT wire)

> **Futura mejora (no activa):** Claude Code admite un hook `Stop` que se
> ejecuta automáticamente cuando el agente termina una sesión. En el futuro
> `/ceo-capture` podría registrarse como un `Stop` hook en
> `.claude/settings.json`, haciendo la captura automática al cierre de cada
> sesión. **Por ahora la captura es MANUAL** (decisión de German). No
> configurar el hook hasta que German lo apruebe explícitamente.
