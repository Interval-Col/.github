# Knowledge Management

The single navigation hub for **where org knowledge lives, in what form, and how
to add it**. If you learned something worth keeping — a decision, a how-to, a
hard-won lesson, an operator guide, a piece of business knowledge — this page
tells you which bucket it belongs to and how to file it so the next engineer
(or the next Claude session) finds it.

Capture is a step in the work, not a chore for later. The `/decision` and
`/guide` slash-commands (see [How to add knowledge](#how-to-add-knowledge))
scaffold the right file in the right place and wire up the index for you.

> **Audience:** the Interval-Col / Interval engineering org. Markdown is the
> canonical store; any rich render (the visual artifact, the docs site) is a
> generated *view* of these files — edit the Markdown, never the render.

---

## The five buckets

Every durable thing you want to keep falls into exactly one of five buckets.
Pick the bucket, then file it in that bucket's **home** in the prescribed
**format** and **language**.

| Bucket | What it is | Home | Format | Language |
|---|---|---|---|---|
| **Decisions** | A choice we made and the *why* behind a constraint | Per-repo [`docs/decisions/`](#) (ADR). Promote to [`Interval-Col/rfcs/`](https://github.com/Interval-Col/rfcs) when cross-cutting | ADR: `NNNN-kebab-title-YYYY-MM-DD.md`, inline **Status:** · RFC: `NNNN-kebab-title.md`, YAML frontmatter | **English** |
| **Methodologies** | How we work — standards, conventions, playbooks | [`.github/`](.) (org-wide) + lab-qc **STANDARDS** (`pharos-lis/lab-qc/docs/STANDARDS.md`) | Markdown standards docs | **English** |
| **Lessons** | What broke and what we learned — incidents + retros | [`operations/incidents/`](https://github.com/Interval-Col/operations) + `operations/lessons.md` | Incident write-up / lessons log | **English** |
| **User guides** | Operator / team how-tos for a specific app | **Centralized** in [`operations/guides/`](https://github.com/Interval-Col/operations) (operations is **private**) | Markdown guide with **`app:` + `repo:`** frontmatter | **Spanish** (neutral Colombian) |
| **Business knowledge** | Durable knowledge of how a brand's *business* works — services, protocols, processes, commercial rules, policies | Per-brand KB repo (**private**): [`biuman-kb`](https://github.com/Interval-Col/biuman-kb) (Biuman) | Markdown article with frontmatter (`title` / `area` / `status` / `owner` / `fuente`); Spanish issue-form intake for non-technical staff | **Spanish** (neutral Colombian) |

**Notes that matter:**

- **Guides are centralized, not per-repo.** Every operator/team guide lives in
  `operations/guides/` (a private repo — safe for screenshots and operational
  detail). Each guide **must** declare which app and repo it pertains to in its
  frontmatter:

  ```yaml
  ---
  title: Cómo cada terminal sabe en qué sede trabaja
  audience: operador | recepción | administrador
  app: admission-patient      # which app the guide is about
  repo: admission-patient     # which repo owns that app
  status: vigente
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  owner: @gczuluaga
  ---
  ```

  The owning repo's `docs/INDEX.md` links **out** to the guide; the guide content
  itself never lives in the app repo.

- **Language split.** ADRs, RFCs, and standards are **English**. Operator/team
  guides are **Spanish** (neutral Colombian — warm, polite, not paisa). Code and
  DB terms stay English inside Spanish prose.

- **The docs site is self-hosted.** A MkDocs Material site serves
  `operations/guides/` (private content — self-hosting keeps it off public
  GitHub Pages, which would also need a different GH subscription). The site is
  a *generated view* of the Markdown; scaffolded now, deploy deferred (no CI /
  Pages wired yet).

- **Business knowledge is per-brand, fed by the whole team.** Each brand's KB
  is its own private repo (first: [`biuman-kb`](https://github.com/Interval-Col/biuman-kb))
  so non-technical staff get access to the KB without seeing code repos.
  Zero-friction intake via Spanish issue forms (technical members convert
  proposals into articles — the *gardener* workflow); hard **no-PHI rule** on
  all content. Rationale + consumption pattern:
  [`biuman-kb/docs/decisions/0001`](https://github.com/Interval-Col/biuman-kb/blob/main/docs/decisions/0001-kb-source-control-git-2026-07-10.md).

---

## RFC vs. ADR — which one?

Both record decisions. The difference is **blast radius and durability**.

> **Decision rule.** Single-repo **and** reversible **and** low-blast-radius
> → **ADR** (in that repo's `docs/decisions/`). Cross-repo **or** a durable
> org-wide constraint **or** irreversible / touches the PHI / prod boundary
> → **RFC** (in `Interval-Col/rfcs/`).

| | **ADR** | **RFC** |
|---|---|---|
| Scope | One repo | Cross-repo / org-wide |
| Reversibility | Reversible, low blast radius | Durable constraint or irreversible |
| PHI / prod boundary | No | Anything touching it → RFC |
| Home | `<repo>/docs/decisions/` | `Interval-Col/rfcs/` |
| Naming | `NNNN-kebab-title-YYYY-MM-DD.md` (per-repo sequence) | `NNNN-kebab-title.md` (org-wide sequence) |
| Status | Inline `**Status:**` line (no frontmatter) | YAML frontmatter `status:` |
| Sections | Context / Decision / Consequences / Alternatives considered / References | Per [`rfcs/template.md`](https://github.com/Interval-Col/rfcs/blob/main/template.md) |

When an ADR turns out to be cross-cutting after all, **promote** it: open an RFC
in `rfcs/`, summarize and link back to the originating ADR, and update the ADR's
**Status:** to point at the RFC.

---

## How to add knowledge

Two slash-commands do the filing for you. Their canonical source lives in
[`.github/commands/`](commands/) and is **installed (copied) into each repo's
`.claude/commands/`** so the whole team has them locally.

| Command | What it scaffolds |
|---|---|
| **`/decision`** | A new **ADR** in the current repo's `docs/decisions/` — auto-numbers the next `NNNN`, pre-fills Context / Decision / Consequences / Alternatives / References from the session, sets the date in the filename, and **appends a row to `docs/INDEX.md`**. If the decision is cross-cutting it prompts you to promote to an RFC instead. |
| **`/guide`** | A new **Spanish** operator/team guide in `operations/guides/` — fills the `app:` + `repo:` frontmatter, drops the guide body skeleton, and **appends a row to the owning repo's `docs/INDEX.md`** (the cross-link out to the centralized guide). |

**Templates** live in [`.github/templates/`](templates/):

- [`plan-template.md`](templates/plan-template.md) — plan-craft methodology.
- [`incident-template.md`](templates/incident-template.md) — Lessons bucket.
- [`ops-plan-template.md`](templates/ops-plan-template.md) — operations plans.
- [`issue-template.md`](templates/issue-template.md) — issue authoring.

The RFC template is in the rfcs repo:
[`rfcs/template.md`](https://github.com/Interval-Col/rfcs/blob/main/template.md).

**Doing it by hand?** Match the existing pattern exactly: ADRs follow
[nucleus-db's sequence](https://github.com/Interval-Col/nucleus-db) and
admission-patient's `docs/decisions/`; guides follow
`operations/guides/verificacion-terminal-sede.md`. Always update the relevant
`docs/INDEX.md` in the same change.

---

## Where each fact lives

One class of fact, one owning document. Everything else **points** at it.

This table exists because copying is how the estate drifts. A 2026-08 sweep found
the same three mechanisms behind nearly every stale claim: indexes copied by hand
(the RFC index existed in three copies, and all three were wrong), documents
forked and both sides calling themselves authoritative, and investigative prose
poured into tables meant for scanning.

**How to use it.** Before writing a fact down, find its row. If you are not
writing in the owner, write a pointer instead. If the owner is wrong, fix the
owner — do not correct it locally and leave the owner lying.

| Fact class | Owner | Read it there because |
|---|---|---|
| Repo inventory & navigation | `operations/WORKSPACE-MAP.md` | Symlinked as `~/dev/CLAUDE.md`; loaded into every session |
| Repo disposition (archived / folded / deleted) | `rfcs/0009-disposition-tracker.md` | The per-repo ruling, with dates |
| Runtime topology (what runs where, behind which route) | `proxy/templates.d/*.conf.template` | Config, not prose — it cannot drift from itself |
| Host roster (hostname, IP, environment, role) | `infrastructure/inventory/` | The inventory is what Ansible actually reads |
| Schema ownership & GRANTs | `nucleus-db/operations/grants/grant-matrix.md` | It is what `apply-grants.sql` implements |
| Branching / CI / deploy policy | `.github/BRANCHING-AND-DEPLOY.md` | ⚠️ States the standard; per-repo settings drift — verify with `gh api …/branches/<b>/protection` |
| Org-level engineering standards (stack choices) | `.github/ENGINEERING_STANDARDS.md` | What a new repo adopts |
| Implementation standards (tool configs, CI-enforced) | `pharos-lis/lab-qc/docs/STANDARDS.md` | Shared by lab-qc and finance-lch |
| Machine-checked contracts | `.github/db-tenant-contract.md`, `auth-contract.md` | A CI check reads these |
| Pháros design system | `.github/brands/pharos_brand/registry/` | Synced into apps by `sync-pharos-registry.sh`; ⚠️ `pharos-brand/` at the workspace root is assets only |
| Tenant brand books & assets (LCH · Biuman · Interval) | `Interval-Col/brand-assets` | PRIVADO — holds licensed commercial fonts; masters in Git LFS |
| Plan methodology & templates | `.github/templates/plan-template.md` | `plan_lint.py` enforces this schema |
| RFC index & lifecycle | `rfcs/README.md` | Do not mirror it — mirrors cannot stay true |
| Incident history | `operations/incidents/` + `operations/lessons.md` | Postmortem, then the durable rule |
| Technical debt | `operations/tech-debt.md` | The capture inbox |
| Runbooks (operator procedures) | `operations/runbooks/` | One home, including runbooks about infrastructure |
| Schema / data-platform decisions | `nucleus-db/docs/decisions/` (single-repo) → `rfcs/` (cross-repo) | See *RFC vs. ADR* above |
| PHI & security policy | `operations/policies/` | |
| Team roster & operating model | `operations/ops/shared/` | Private by design |
| **Operational facts a session must not miss, per repo** | that repo's **`CLAUDE.md`** | ⚠️ It is the **only** vector that reaches another person's agent — see below |
| Knowledge-management conventions | this file | |

### ⚠️ The vector that reaches other people's agents is a committed file

A fact can be **correct in the RFC and still absent** from where it gets read. The
two do not conflict, nothing fails, and the stale copy is the one that wins.

**What does NOT reach a teammate's session:** your memory store, your personal
`~/.claude/CLAUDE.md`, your chat context. Those are yours.

**What does:** a file **committed in the repo they are working in** — that repo's
`CLAUDE.md` above all, because it loads automatically into every session opened
anywhere inside it.

> 🔴 **Measured, 2026-08.** The cobolql forge cutover was executed **and documented**
> in RFC 0009 on 2026-08-20. But `cobolql/CLAUDE.md` kept saying *"externalUse
> deploys from Bitbucket"* for a week. Someone working the other lineage had no way
> to know two deploy paths shared one set of host-secret names. Cost: **two days** of
> blocked production deploys, CI green throughout.
> Postmortem: `operations/incidents/2026-08-cobolql-secretos-compartidos-entre-linajes.md`.

**So, when closing a cutover or an incident**, the question is not *"did I write it
down?"* but *"where will the next person read it?"*:

1. The **`CLAUDE.md` of every repo touched.** If a repo has none, that is the finding.
2. The long document (`operations/docs/`, a runbook), **pointed at** from step 1.
3. The **RFC**, if the decision is durable — but an RFC does **not** load into a
   session on its own, so it never replaces step 1.
4. The **durable rule** in `operations/lessons.md`.

**And date the change.** *"Since 2026-08-20"* lets a reader recognise older material
as superseded. Undated, two contradictory documents look equally credible.

💡 **The test for a duplicate.** If two documents state the same fact and one goes
stale, would a reader be able to tell which? If not, one of them must become a
pointer. A wrong copy is worse than no copy, because it looks like an answer.

---

## Cross-repo decision ledger

### RFCs (org-wide)

The index lives in
[`rfcs/README.md`](https://github.com/Interval-Col/rfcs/blob/main/README.md),
with the number, title, status and target repos of every RFC. Some numbers also
carry companion working files — trackers and surveys, not separate RFCs; the
index marks them.

This page carried a hand-copied mirror of that table until 2026-08-07. By then it
was wrong about three RFCs' status and missing sixteen of the twenty-six, while
sitting one line below the pointer above. A mirror of an index has no way to stay
true, and a reader cannot tell a stale mirror from a current one.

### Notable ADRs (per repo)

Each repo keeps its decisions in `docs/decisions/` and indexes them in its own
**`docs/INDEX.md`** — start there per repo:

| Repo | Knowledge index |
|---|---|
| `admission-patient` | [`docs/INDEX.md`](https://github.com/Interval-Col/admission-patient/blob/main/docs/INDEX.md) |
| `nucleus-db` | [`docs/decisions/`](https://github.com/Interval-Col/nucleus-db/tree/main/docs/decisions) |

As more repos adopt `/decision`, add their `docs/INDEX.md` here.

---

## See also

- [Engineering Standards](ENGINEERING_STANDARDS.md) — stack, structure, conventions, design gates (Methodologies bucket).
- [Branching & Deploy](BRANCHING-AND-DEPLOY.md) — branching model, CI, deploy.
- [Agent Chat Hygiene](AGENT-CHAT-HYGIENE.md) · [español](AGENT-CHAT-HYGIENE.es.md) — keeping Claude Code sessions cheap and durable.
- lab-qc **STANDARDS** — `pharos-lis/lab-qc/docs/STANDARDS.md` (extracted engineering standards).
