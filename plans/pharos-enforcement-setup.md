---
status: in-progress
owner: gczuluaga
created: 2026-06-18
updated: 2026-06-29
issue: none — admin runbook; related open tracking issues Interval-Col/.github#43 and #73
start: TBD
target: TBD
implementation: gczuluaga
effort: S
model: claude-sonnet-4-6
sources: [.github, admission-patient, finance-lch, commercial-lch]
language: English body; Spanish "Resumen" + decision/criteria glosses.
---

# Pháros Enforcement Setup — Branch-Protection & Retro-Gate Admin Runbook · Configuración de controles Pháros — runbook de branch-protection y Retro Gate

> **Resumen (ES).** Este runbook de administración configura los controles técnicos del estándar Pháros en los repositorios del stack: branch-protection, checks requeridos de sistema de diseño (`pharos-lint-check`) y el Retro Gate. Lo ejecuta únicamente el administrador de la organización (@gczuluaga). Cubre tres momentos: la configuración inicial una sola vez antes del Track A, la activación por-track a medida que se sincroniza `pharos-lint-check.yml` en cada repo, y las decisiones diferidas para cuando exista un segundo code-owner real en la organización.

# Pháros rollout — enforcement setup (admin runbook · @gczuluaga only)

> ⚠️ These change **branch-protection / repo settings** — run by the org admin (German), not by an
> agent. They arm the "dictatorial standard" the v2 plan + Retro Gate assume. The recon found
> `pharos-lint-check` is **not** a required check in any target repo today, so the design-system gate
> is currently unenforced at CI. **Confirm exact context strings + `gh api` syntax against a first run
> before relying on them** (they're written indicatively; not agent-tested).

> **Markers** — ✅ **Done-when** (verifiable definition of done) · 🚦 **Checkpoint** (stop, show @gczuluaga the named evidence) · 🛑 **HUMAN DECISION** (an agent must not pick this — escalate to @gczuluaga) · 💡 **Heuristic** (a task-earned lesson). *(ES: ✅ terminado-cuando · 🚦 punto de control · 🛑 decisión humana · 💡 heurística.)*

## Glossary · Glosario

> **Resumen (ES).** Términos técnicos en inglés que se repiten en este plan, con su traducción y una línea de qué significan.

| English | Español | Means |
|---|---|---|
| branch protection | protección de rama | GitHub setting that enforces required checks and reviews before merging into a branch |
| required check / required status check | check requerido | a CI job whose green result is mandatory before a PR can be merged |
| context (name) | nombre de contexto | the string GitHub uses to identify a specific CI check (e.g. `Pháros — lint-check`) — must match exactly |
| Retro Gate | Retro Gate (compuerta de retroceso) | the automated CI gate in `.github` that verifies the next repo is standards-ready before a track handoff |
| pharos-lint-check | pharos-lint-check | the design-system lint workflow synced per-repo that enforces Pháros DS standards |
| dismiss_stale_reviews | invalidar revisiones obsoletas | branch-protection option that voids existing PR approvals when new commits are pushed |
| enforce_admins | enforce_admins | branch-protection option that prevents org admins from bypassing required checks — currently deferred |
| CODEOWNERS | CODEOWNERS | repository file that auto-assigns reviewers based on which paths changed in a PR |
| label | etiqueta | a GitHub tag on a PR or issue (e.g. `retro-gate`, `blocked:retro-gate`) used by workflows and triage |

## Out of scope · Fuera de alcance

> **Resumen (ES).** Lo siguiente **no** es parte de este alcance.

- Enabling `enforce_admins` on any branch now — explicitly deferred to Section C until a second real code-owner exists.
- Verifying exact CI context strings without a live workflow run — they must be confirmed from actual run output, not assumed.
- Parity adjustments beyond `commercial-lch` (`dismiss_stale_reviews`) and `admission-patient` (CODEOWNERS for `@SKuger01`).
- Changes to any repo's existing `gitleaks`, lint/test/contract required checks — those are preserved, never replaced.

---

## A. Now — one-time, before Track A

> **Resumen (ES) — Sección A: Configuración inicial (una sola vez, antes del Track A).**
>
> Pasos únicos que establecen la infraestructura de control antes de arrancar el primer track. Incluye una decisión humana que requiere confirmar el nombre exacto del contexto tras la primera ejecución real del workflow.
>
> En orden, las tareas:
>
> 1. **A.1** — Fusionar el PR del plan v2 (incluye `retro-gate.yml`) y el PR del RFC.
> 2. **A.2** — Crear la etiqueta `retro-gate` en `.github` y `blocked:retro-gate` en los repos de producto.
> 3. **A.3** — Registrar `retro-gate` como check requerido en `.github` `main`, confirmando el nombre exacto del contexto tras la primera ejecución.
> 4. **A.4** — Aplicar correcciones de paridad: `dismiss_stale_reviews` en `commercial-lch` `main` y CODEOWNERS de `admission-patient`.
>
> Decisión humana: confirmar el nombre exacto del contexto de `retro-gate` (tarea A.3) antes de agregarlo como check requerido.

1. **Merge** the v2 plan PR (includes `retro-gate.yml`) + the RFC PR.
2. **Create labels:**
   ```sh
   gh label create retro-gate -R Interval-Col/.github -c 5319e7 -d 'Pháros track handoff (Retro Gate) PR'
   for r in admission-patient finance-lch commercial-lch; do
     gh label create blocked:retro-gate -R "Interval-Col/$r" -c b60205 -d 'Blocked: awaiting prior track Retro Gate'
   done
   ```
3. **Register `retro-gate` as a required check on `.github` `main`** — after the workflow has run once
   on a `retro-gate`-labeled PR (so the context name is registered). Confirm the exact context name
   (`Pháros — retro-gate` / `retro-gate`) from that run, then add it to the existing required checks
   on `Interval-Col/.github` `main` (keep `gitleaks`).
4. **Parity fixes:**
   - `commercial-lch` `main`: enable `dismiss_stale_reviews` (the other two repos have it).
   - `admission-patient` `CODEOWNERS`: add `@SKuger01` for the frontend path(s) (a PR, not a setting) —
     matches finance-lch/commercial-lch granularity.

✅ **Done-when:**
- Labels `retro-gate` and `blocked:retro-gate` exist in all listed repos (`gh label list -R Interval-Col/.github` and `gh label list -R Interval-Col/<repo>` show the labels).
- `gh api repos/Interval-Col/.github/branches/main/protection --jq '.required_status_checks.contexts'` lists the `retro-gate` context (exact name confirmed from a live run).
- `gh api repos/Interval-Col/commercial-lch/branches/main/protection --jq '.required_pull_request_reviews.dismiss_stale_reviews'` returns `true`.
- A PR against `admission-patient` touching frontend paths auto-assigns `@SKuger01` via CODEOWNERS.
*(ES: terminado-cuando — cada punto se verifica con el comando indicado o abriendo una PR de prueba.)*

## B. Per-track — during each track's Stage 1–2 (once sync lands `pharos-lint-check.yml`)

> **Resumen (ES) — Sección B: Por-track — Stage 1–2 de cada track.**
>
> Para cada repo del track, una vez que el workflow `pharos-lint-check.yml` ha sido sincronizado y ha reportado al menos un resultado en `develop`, agregar su contexto confirmado a los checks requeridos de `develop` y `main`, sin eliminar los checks existentes.
>
> En orden, las tareas:
>
> 1. **B.1** — Confirmar el nombre exacto del contexto del workflow `pharos-lint-check` en el repo del track, desde una ejecución real.
> 2. **B.2** — Agregar el contexto confirmado a los checks requeridos de `develop` y `main` del repo, junto a `gitleaks` y los checks existentes.
>
> Decisión humana: confirmar el nombre exacto del contexto (tarea B.1) antes de configurarlo como requerido.

For the track's repo `<repo>`, after the workflow is synced + has reported once on `develop`:
- Add the design-system context (confirm exact name, e.g. `Pháros — lint-check`) to the **required
  status checks on BOTH `develop` and `main`** — **alongside** the existing required contexts
  (`gitleaks` + the repo's lint/test/contract jobs); do not remove them.
- Required checks on `develop` block **even direct pushes** (per `BRANCHING-AND-DEPLOY.md`) — this is
  the load-bearing lever that makes the standard non-negotiable.
- The Retro Gate's STANDARD-conformance step verifies the **next** repo is armed before handoff, so
  this closes Gap 1 track-by-track.

✅ **Done-when:** `gh api repos/Interval-Col/<repo>/branches/develop/protection --jq '.required_status_checks.contexts'` and the same for `main` both list the `pharos-lint-check` context alongside `gitleaks` and the prior required checks. *(ES: ambas ramas del repo del track muestran el contexto de lint como check requerido, junto con los checks previos.)*

## C. Deferred (escalation)

> **Resumen (ES) — Sección C: Diferido (escalación futura).**
>
> Control postergado deliberadamente hasta que las condiciones organizacionales lo justifiquen. No hay acción inmediata.
>
> En orden, las tareas:
>
> 1. **C.1** — Cuando exista un segundo code-owner real en la organización, activar `enforce_admins` en `Interval-Col/.github` `main`.

- Leave `enforce_admins` **OFF** for now — it preserves the documented solo-merge flow
  (`gh pr merge --admin`). Once a real second code-owner exists, turn it ON for `Interval-Col/.github`
  so even an admin cannot merge a red `retro-gate` check.

✅ **Done-when:** N/A — this section is deferred; it activates only when a second real code-owner exists in the org. The activation decision is recorded in *Decisions* below with a date. *(ES: no hay criterio de cierre inmediato; la condición de activación es que exista un segundo code-owner real.)*

---

## Decisions · Decisiones

**Open:**

- 🛑 **Context string — retro-gate** — The exact CI context name for `retro-gate` cannot be confirmed until the workflow has run at least once on a `retro-gate`-labeled PR on `.github` `main`. Pending: @gczuluaga confirms the exact string from that run, then adds it as a required check.
- 🛑 **Context string — pharos-lint-check** — Same applies per-repo: the exact context name is only known from a live run. Pending: @gczuluaga confirms per track during Section B, before setting it as required.
- 🛑 **enforce_admins activation** — Whether and when to enable `enforce_admins` on `.github` `main`. Pending: @gczuluaga confirms a second real code-owner is active in the org (Section C).

**Resolved during planning:**

- **Retro Gate scope** — `retro-gate` check goes only on `.github` `main`; product repos get `pharos-lint-check` on both `develop` and `main`. *(2026-06-18.)*
- **Preserve existing required checks** — When adding new contexts, existing ones (`gitleaks`, lint/test/contract) are never removed. *(2026-06-18.)*
- **enforce_admins stays OFF initially** — preserves the documented `gh pr merge --admin` solo-merge flow; deferred to Section C. *(2026-06-18.)*

## Risks · Riesgos

> **Resumen (ES).** Los riesgos principales son agregar un check requerido antes de que el workflow haya reportado (bloquea todas las PRs) y activar `enforce_admins` antes de tener un segundo code-owner (rompe el flujo de merge en solitario). Las mitigaciones están integradas en el orden de las secciones A, B y C.

- **Context not yet registered** → adding a required check for a context that has never run on that branch makes every PR immediately fail with "required status check not found." **Mitigation:** both Section A.3 and B.1 explicitly require the workflow to have produced at least one result before the required-check is set.
- **`dismiss_stale_reviews` mis-applied to the wrong repo** → accidentally tightening a repo's protection that should not be touched. **Mitigation:** always pass `-R Interval-Col/<repo>` explicitly in every `gh api` invocation; confirm with a read call before writing.
- **`enforce_admins` turned on too early** → blocks the `gh pr merge --admin` solo-merge flow that the current single-code-owner setup depends on. **Mitigation:** kept in Section C (deferred) with an explicit activation condition.

## References

- `.github/plans/branching-policy-rollout.md` — counterpart plan tracking the broader branching + deploy rollout.
- `Interval-Col/.github#43` and `Interval-Col/.github#73` — related open tracking issues (see frontmatter).
- `.github/BRANCHING-AND-DEPLOY.md` — org-wide branching and deploy standard that the enforcement here makes non-negotiable.
- GitHub docs — [About protected branches and required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches).
