---
status: proposed
created: 2026-06-15
updated: 2026-06-29
owner: gczuluaga
implementation: TBD
language: English body; Spanish "Resumen" + decision glosses.
issue: TBD
relates-to: brands/biuman/BIUMAN-BRAND.md · brands/pharos_brand/BRAND.md §10
---

# Biuman brand-doc — verification & asset hardening · Verificación y endurecimiento de activos

> **Resumen (ES).** El documento de marca Biuman
> (`brands/biuman/BIUMAN-BRAND.md`) ya quedó redactado y, según la verificación
> multi-agente + crítica adversarial, es **internamente fiel**. Pero hay **cuatro
> huecos** por cerrar antes de tratarlo como **canónico/listo para producción**:
> (1) **verificar la paleta** contra el Brandbook con ojos humanos — no se pudo
> re-renderizar el PDF en la máquina que generó el doc; (2) **licenciamiento de la
> fuente** Pragmática Ext (comercial); (3) **faltan SVG reales** (solo existen los
> `.ai`); (4) **discrepancia de descriptor** ("LABORATORIO DEPORTIVO" en el PNG vs
> los descriptores del Brandbook). Más una cola de **preguntas abiertas** menores.
> Este plan las cierra en orden de prioridad.

The Biuman tenant brand doc was generated from the brand masters
(`Backbone-BIUMAN.pdf` 23pp + `Brandbook-BIUMAN.pdf` 47pp + fonts/logos) by a
multi-agent extraction → author → adversarial fidelity critic → finalize pass,
and reviewed line-by-line. The critic returned **faithful: True** and the doc is
correctly positioned as a **tenant of Pháros** (sibling of LCH; see
`BRAND.md §10`). What remains are the items a software pass **cannot** settle on
its own: a human-eyes color check, a licensing fact, a vector-export task, and a
brand-management naming call. Until they're closed, the doc's palette/logo specs
are **provisional-but-trusted**, not canonical.

> **Masters (heavy — kept OUT of git).** The source files live in the
> `biuman_brand/` working folder at the workspace root: `Brandbook-BIUMAN.pdf`,
> `Backbone-BIUMAN.pdf`, `LOGO BM.ai`, `LogoB.ai`, `FONTS/` (5 Pragmática Ext
> OTF). Do **not** commit them. Only small PNGs (and, after Phase 3, SVGs) belong
> in `brands/biuman/logos/`.

---

## How to use this plan · Cómo usar este plan

**EN.** This plan is written to be executed with AI-agent assistance —
that is expected and encouraged. The plan, not the agent, makes the
technical decisions. Your job has three parts: **execute** the tasks,
**verify** each one against its Done-when list, and **escalate** the
decisions the plan marks for a human.

Read each task fully — including its **Why** and **Done-when** — *before*
you start it. A task is not finished because an agent said so; it is
finished when every Done-when line is literally true and you have
checked it yourself.

If a task or its **Why** doesn't make sense, that is a gap in *this
plan*, not a failing in you — stop and ask gczuluaga. A question costs
minutes; a misunderstanding shipped costs days.

**If the English here slows you down:** every section opens with a
Spanish **Resumen**, and your AI agent will translate or explain any
part of this plan in Spanish if you ask it — that is a completely
legitimate thing to do. Don't let the language be the reason a task
stalls.

**ES.** Este plan está escrito para ejecutarse con ayuda de agentes de
IA — eso se espera y se fomenta. Las decisiones técnicas las toma el
plan, no el agente. Tu trabajo tiene tres partes: **ejecutar** las
tareas, **verificar** cada una contra su lista *Done-when*, y **escalar**
las decisiones que el plan marca para un humano.

Lee cada tarea completa — incluyendo su **Why** y su **Done-when** —
*antes* de empezarla. Una tarea no está terminada porque un agente lo
diga; está terminada cuando cada línea *Done-when* es literalmente cierta
y tú mismo la verificaste.

Si una tarea o su **Why** no te quedan claras, eso es un vacío de *este
plan*, no una falla tuya — pregúntale a gczuluaga. Y si el inglés te
frena: cada sección tiene un **Resumen** en español, y tu agente de IA
te traduce o explica cualquier parte en español si se lo pides — hazlo
sin problema.

## Conventions · Convenciones

| Marker | Meaning |
|---|---|
| ✅ **Done-when** | Definition of done — closed only when every line is literally true. *(ES: terminado-cuando.)* |
| 🛑 **HUMAN DECISION** | A brand/legal call no agent makes. Escalate to gczuluaga / brand management / SKuger. *(ES: decisión humana — no la toma un agente.)* |
| 🚦 **Checkpoint** | Stop, show the named evidence to gczuluaga before continuing. *(ES: punto de control.)* |
| 💡 **Note** | A working lesson worth 30 seconds. *(ES: nota.)* |

**How to use.** Phases are ordered by priority (P1 first). P1 makes the doc
*accurate*; P2 makes shipping lockups *unambiguous*; P3 gives web *real vectors*;
P4 is the *legal/ops gate* before any production font use; P5 is cleanup. Each
phase is independent — you can land them in any order — but P1 should not wait.

## Working rules · Reglas de trabajo

These apply to every phase.

- **Commit and push after every slice.** When a task group or a phase is
  done and its Done-when checks pass, commit and push to GitHub
  **immediately**. Work that lives only on your laptop cannot be seen,
  reviewed, helped with, or recovered. *(ES: haz commit y push a GitHub
  apenas termines — el trabajo que solo vive en tu laptop no existe para
  el equipo.)*
- **Commit messages — Conventional Commits, scope required.**
  `type(scope): description` — e.g. `docs(biuman-brand): verify palette against Brandbook pp.22–23`.
  `type` ∈ `feat|fix|refactor|test|chore|docs|hotfix|ci`. The `(scope)` is
  **mandatory**. Branch names mirror it: `type/scope-short-description`.
  *(ES: Conventional Commits; el `(scope)` es obligatorio; la rama
  refleja el commit.)*
- **Review the frontend yourself, in the browser.** A phase that touches
  the UI is **not verified** because the backend endpoint returned `200`
  — it is verified when you have opened the app, clicked through what
  you built, and seen it work the way a real user would use it. *(ES:
  revisa el frontend tú mismo, en el navegador — un `200` del backend no
  es una funcionalidad que sirve.)*
- **Which AI tool:** Claude **Sonnet** by default; **Opus** when a task
  is hard or you are stuck; **Copilot** for inline autocomplete and
  quick questions — not for executing a whole task. *(ES: Sonnet por
  defecto; Opus cuando es difícil o te atascas; Copilot para
  autocompletar.)*
- **You can tell your agent to skip the Why boxes — we won't stop you.**
  But the 🚦 checkpoint questions are asked by a person, and that you
  cannot outsource. Reading as you go is the cheap way to be ready.
  *(ES: puedes pedirle a tu agente que se salte las explicaciones — pero
  las preguntas del checkpoint las hace una persona; eso no se delega.)*
- **Auto mode is slice-bounded.** Auto mode (running without clarifying
  questions between turns) is allowed for the duration of **one
  slice** — a single numbered task, or one phase when the plan groups
  tasks that way. At the end of every slice, the agent **STOPS**,
  surfaces what landed (Done-when items verified, files touched,
  what's next), and waits for explicit human acknowledgement before
  starting the next slice. At 🚦 Checkpoints the stop is stronger —
  the human walks the evidence with the agent. Auto mode is **never**
  "execute the whole plan unattended." *(ES: el modo auto va por
  slice, no por plan entero. Al final de cada slice, el agente
  **PARA**, te muestra qué cerró (Done-when, archivos tocados, qué
  viene) y espera tu visto bueno antes del siguiente slice. En los
  🚦 el alto es más fuerte — recorres la evidencia con el agente.
  Auto **nunca** significa "ejecuta el plan completo solo".)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que vas a ver muchas
> veces en este plan, con su traducción y una línea de qué significan.
> Si te encuentras un término del plan que no está aquí y no lo
> entiendes, pregúntale a tu agente — no es una falla tuya, es un vacío
> de esta tabla.

| English | Español | Means |
|---|---|---|
| lockup | bloqueo de marca | a branded composition of logo + wordmark + descriptor treated as a single printable or digital unit |
| descriptor | descriptor de marca | the short brand tagline that appears beneath the wordmark in a lockup (e.g. *CIENCIA DEL MOVIMIENTO*) |
| wordmark | wordmark | the brand name set in its official typeface, without any icon or symbol |
| isotipo | isotipo | the standalone symbol/icon element of a brand (the `B` mark for Biuman), used without the wordmark |
| swatch | muestra de color | a printed or digital color patch that displays a specific CMYK/Pantone/hex value |
| outlined text | texto en curvas | vector text converted to paths — renders correctly with no font file present |
| Brandbook | manual de marca | the comprehensive brand specification document (here: `Brandbook-BIUMAN.pdf`) |
| Done-when | terminado-cuando | the literal, checkable list that defines when a task is truly finished — not "the agent said so" |
| commit + push | hacer commit y push | save to git locally **and** send to GitHub — both steps are required |
| slice | unidad de trabajo | a single numbered task, or one phase, treated as the boundary for auto mode |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance — es
> v1+ / para después. Si un agente sugiere construir algo de esta lista,
> no lo hagas.

Explicitly out of scope — not for this plan:

- **Pháros design-system registry token authoring for the Biuman tenant** — this plan verifies the brand identity source of truth; mapping identity specs to registry tokens is a separate downstream step.
- **Updating product UI to consume the corrected palette** — that is an implementation step that follows once the doc is declared canonical.
- **Expanding the brand doc beyond the four documented gaps** — new brand decisions or additional sections are out of scope; flag them as a new plan item.
- **Publishing the brand doc to external design handoff platforms** (Figma, Zeroheight, etc.) — out of scope until the doc is fully canonical.

---

## P1 — Palette verification (human eyes on the Brandbook color page) · Verificar la paleta

> **Resumen (ES).** Confirmar con ojos humanos que los tres tonos del doc
> (`#F0EEED` Cool Gray C · `#1B1B1B` Black C · `#A4A9A6` Pantone 429 C, con sus
> CMYK) coinciden con la página **TONOS** impresa del Brandbook (pp. 22–23, sección
> 006 "Color de Marca"). El doc las tomó de los lectores del workflow + crítica;
> nadie las re-verificó visualmente porque la máquina generadora **no tenía
> `poppler`/PDFKit** para re-renderizar el PDF.

The doc's §2.1 palette is sourced from the Brandbook's printed *TONOS* page but
was **not** independently re-rendered (no `poppler`/PDFKit on the generating
host). Close that gap:

- [ ] **1.1** — Open `Brandbook-BIUMAN.pdf` pp. 22–23 (section 006 *Color de
      Marca* / *TONOS*) and read the **printed** specs. Pick one route:
  - macOS Preview / Acrobat — open the page, read the CMYK/Pantone/hex labels
    directly (and use the eyedropper to sample the swatches), **or**
  - `brew install poppler` then re-render
    (`pdftoppm -f 22 -l 23 -png Brandbook-BIUMAN.pdf /tmp/biuman-tonos`) and read
    the PNGs, **or**
  - open `LOGO BM.ai` in Illustrator and read the swatch library.
- [ ] **1.2** — Compare each printed value to `brands/biuman/BIUMAN-BRAND.md`
      §2.1 / §2.7:
  - `#F0EEED` — CMYK 10/7/5/0 — Cool Gray C
  - `#1B1B1B` — CMYK 65/66/68/82 — Black C
  - `#A4A9A6` — CMYK 35/23/19/2 — Pantone 429 C
- [ ] **1.3** — If any value differs: correct §2.1, §2.3, §2.7, the §10 Quick
      Reference Card, and the logo-treatment hexes in §4.1 (they reference the
      same three tones), then note "human-verified against Brandbook pp.22–23" in
      the doc's front note.

💡 **Note.** The Backbone deck prints **no** swatch specs (its grey was *sampled*
≈`#A3A9A6`); only the Brandbook *TONOS* page carries real CMYK/Pantone. So the
Brandbook page is the single authority for this check — the Backbone only
corroborates.

✅ **Done-when:** the three tones in the doc are confirmed (or corrected) against
the Brandbook's printed *TONOS* page by a human, and the doc records that it was
human-verified. *(ES: los tres tonos quedan confirmados/corregidos contra la
página TONOS impresa, y el doc lo registra.)*

🚦 **Checkpoint 1.** Show gczuluaga the Brandbook color page (screenshot or
rendered PNG) next to the doc's §2.1 table.

---

## P2 — Descriptor canonicalization (brand-management call) · Descriptor canónico

> **Resumen (ES).** El PNG de lockup horizontal dice **"LABORATORIO DEPORTIVO"**,
> pero el Brandbook documenta otros descriptores. Hay que decidir cuál es el
> **canónico para producción** y reconciliar el arte. El doc ya lo marca como
> discrepancia (§1.5, §4.2, §10) — esto la resuelve.

The supplied horizontal-lockup PNG (`logos/logo-horizontal.png`) carries
**"LABORATORIO DEPORTIVO"**, which is **not** among the Brandbook's four
documented descriptor versions (V.1 *HUMANS CONQUERING MOVEMENT* · V.2 *CIENCIA
DEL MOVIMIENTO* · V.3 *CENTRO DE EXPERIENCIA MOVIMIENTO* · V.4 wordmark-only).

- [ ] **2.1** — 🛑 **HUMAN DECISION (brand management / SKuger):** which
      descriptor is canonical for shipping lockups? Options:
  - bless one Brandbook version (V.1/V.2/V.3) as the default web lockup;
  - approve "Laboratorio Deportivo" as a *new, intentional* tenant descriptor
    (then it should be added to the Brandbook's version set, not left as an
    orphan on one PNG);
  - keep wordmark-only (V.4) as the default and treat descriptors as contextual.
- [ ] **2.2** — Reconcile the artwork to the decision: if a Brandbook version
      wins, regenerate `logo-horizontal.png` (and the future SVG, P3) from the
      `.ai` master with the approved descriptor; if "Laboratorio Deportivo" wins,
      document it as canonical.
- [ ] **2.3** — Update the doc: remove the hedges in §1.5 (Descriptors row), §4.2
      (discrepancy callout), and §10 (Quick Reference BRAND NAME line); state the
      single canonical descriptor.

✅ **Done-when:** one canonical descriptor is chosen and recorded; the shipped
lockup artwork matches it; the doc no longer flags a discrepancy. *(ES: hay un
descriptor canónico, el arte coincide, y el doc ya no marca discrepancia.)*

---

## P3 — Vector assets (real SVGs from the `.ai` masters) · Vectores SVG reales

> **Resumen (ES).** Solo existen vectores `.ai` (no commiteables). Web necesita
> **SVG reales**. Exportar `logo-*.svg` del wordmark y del isotipo desde los `.ai`
> y commitearlos en `brands/biuman/logos/` (como ya hace `hematologico/logos/`).

Today only `.ai` vectors exist (heavy, uncommitted). The committed assets are
raster PNGs. Web needs true vectors.

- [ ] **3.1** — From `LOGO BM.ai` / `LogoB.ai`, export clean SVGs (outlined text
      — do **not** rely on the embedded Pragmática Ext font; convert to paths):
  - `logos/logo-horizontal.svg` (wordmark + bar + **canonical** descriptor from P2)
  - `logos/logo-wordmark.svg` (V.4, wordmark only)
  - `logos/logo-icon.svg` (isotipo `B`)
- [ ] **3.2** — Commit them to `brands/biuman/logos/` (mirrors
      `hematologico/logos/`, which already ships `.svg`). 💡 The org gitleaks
      allowlist already covers `brands/**/logos/*.svg`; verify the pre-commit/CI
      gitleaks check passes on the new files.
- [ ] **3.3** — Update `BIUMAN-BRAND.md` §4.2 (SVG status), §4.8 (Vue component
      `logoSrc` → `.svg`), and the appendix SVG TODO to reflect that real vectors
      now exist.

✅ **Done-when:** outlined `logo-*.svg` for wordmark + descriptor lockup + isotipo
are committed under `brands/biuman/logos/`, gitleaks passes, and the doc points at
the SVGs. *(ES: hay SVG con texto en curvas commiteados, gitleaks pasa, y el doc
apunta a los SVG.)*

---

## P4 — Font licensing (Pragmática Ext) · Licenciamiento de la fuente

> **Resumen (ES).** Pragmática Ext es **comercial**. Hay que confirmar el estado
> de licencia y su **alcance** (¿web/`@font-face`? ¿app embebida? ¿cuántos
> dominios/seats?) **antes** de cualquier uso en producción, y decidir
> bundle-vs-fallback. Los `.otf` no se commitean.

Pragmática Ext is a licensed commercial typeface (5 OTF weights live in
`biuman_brand/FONTS/`, uncommitted). Production use needs a confirmed license.

- [ ] **4.1** — 🛑 **HUMAN DECISION (gczuluaga / ops + legal):** confirm the
      Pragmática Ext license status and **scope** — does it cover **web embedding
      (`@font-face`)** and/or **app bundling**, for how many domains/seats? Locate
      the license document / vendor (ParaType or reseller).
- [ ] **4.2** — Decide the production strategy and record it in the doc §3.1:
  - licensed for web → self-host the licensed weights behind the org font
    pipeline (note where the licensed files are stored — **not** this repo);
  - not licensed for web → use a documented fallback (an extended geometric
    grotesque) for product UI and reserve Pragmática Ext for brand/marketing
    artwork only.
- [ ] **4.3** — Keep the `.otf` masters **out of git**; record their location +
      license reference in the doc/appendix.

✅ **Done-when:** the license scope is confirmed in writing, the production
font strategy (self-host vs fallback) is decided and recorded in §3.1, and no
`.otf` is committed. *(ES: el alcance de la licencia está confirmado por escrito,
la estrategia de fuente en producción está decidida y registrada, y no se
commitea ningún `.otf`.)*

---

## P5 — Residual open questions (cleanup) · Preguntas abiertas restantes

> **Resumen (ES).** Cabos sueltos menores que el doc ya marca como "no
> especificado": de dónde salen los colores de estado, specs de párrafo, padding
> de avatar, nombres PostScript de la fuente, y si existe una hoja de
> do's/don'ts. Resolver o confirmar "lo gobierna el registro Pháros".

Each is already marked **no especificado en el material fuente** in the doc;
close by either finding the spec in the masters or confirming the Pháros registry
governs it.

- [ ] **5.1** — **Semantic-state palette** (success/warning/error): confirm Biuman
      product UI pulls these from the **Pháros registry** semantic tokens (not a
      Biuman-specific set). Likely a one-line confirmation → doc §2.4.
- [ ] **5.2** — **Typography paragraph specs** (type scale, line-height,
      alignment, body min sizes) + brand-name casing in running copy: check
      whether a later Brandbook page specifies them; else confirm the registry
      governs → doc §3.2/§3.3.
- [ ] **5.3** — **Avatar/icon padding ratio** for square/circular slots: confirm a
      Biuman value or adopt the LCH ¼-height default → doc §4.6.
- [ ] **5.4** — **Pragmática Ext PostScript face names** (camel-case, cited by the
      Backbone deck but unverified): if needed for `@font-face`/loader config,
      verify against the actual font metadata → doc §3.1 note.
- [ ] **5.5** — **Logo misuse / do's-and-don'ts sheet:** confirm none exists in the
      Brandbook (the reviewed pages had none) or author one; until then the doc's
      conservative defaults stand → doc §4.7.

✅ **Done-when:** each item is resolved or explicitly confirmed as
registry-governed, and the doc's corresponding "no especificado" notes are updated
with the resolution. *(ES: cada ítem queda resuelto o confirmado como gobernado
por el registro, y las notas del doc se actualizan.)*

---

## Decisions · Decisiones

- **Tenant positioning is settled** — Biuman is a **tenant** of the Pháros family
  (sibling of LCH), per `BRAND.md §10`; not a sub-brand, not the maker. No action.
- **Heavy masters stay out of git** — PDFs, `.ai`, `.otf` are referenced from
  `biuman_brand/`, never committed (mirrors the Pháros "documented but not
  vendored" approach).
- **Product UI is built from the Pháros registry**, themed for the Biuman tenant —
  this brand doc is the **identity/palette source of truth**, not the product
  token contract.

## Risks · Riesgos

- **Palette drift** — if P1 finds the sampled/extracted hexes differ from the
  printed Brandbook specs, any downstream Biuman theming inherits the error. P1
  is therefore the gating accuracy check. *(ES: riesgo de deriva de paleta.)*
- **Font legal exposure** — shipping Pragmática Ext on the web without a web
  license is a real legal risk; P4 must precede any production embedding. *(ES:
  exposición legal de la fuente.)*
- **Orphan descriptor** — leaving "Laboratorio Deportivo" unreconciled means
  shipping a lockup that contradicts the Brandbook; P2 resolves it.

## References

- `brands/biuman/BIUMAN-BRAND.md` — the doc this plan hardens.
- `brands/hematologico/LCH-BRAND.md` — the tenant-doc convention mirrored, and the
  `logos/` (incl. `.svg`) precedent for P3.
- `brands/pharos_brand/BRAND.md §10` — the tenant architecture.
- `biuman_brand/` (workspace root, uncommitted) — the brand masters (Brandbook,
  Backbone, `.ai`, `FONTS/`).
