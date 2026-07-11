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

## Cross-repo decision ledger

### RFCs (org-wide)

The authoritative index is [`rfcs/README.md`](https://github.com/Interval-Col/rfcs/blob/main/README.md);
this mirror is for quick orientation from the hub.

| # | Title | Status |
|---|---|---|
| [0001](https://github.com/Interval-Col/rfcs/blob/main/0001-org-wide-harmonization.md) | Org-wide engineering standards harmonization | `proposed` |
| [0002](https://github.com/Interval-Col/rfcs/blob/main/0002-browser-auth-httponly-cookie-csrf.md) | Move browser auth to httponly cookie + CSRF token | `draft` |
| [0003](https://github.com/Interval-Col/rfcs/blob/main/0003-object-storage-strategy.md) | Object storage strategy — harden MinIO, replicate off-site, plan for AI workloads | `draft` |
| [0004](https://github.com/Interval-Col/rfcs/blob/main/0004-pharos-product-portfolio.md) | Pháros product portfolio — umbrella brand, persona-scoped apps, holding multi-tenancy | `draft` |
| [0005](https://github.com/Interval-Col/rfcs/blob/main/0005-nucleus-data-platform.md) | nucleus-db — shared database platform, schema stewardship, historical archive | `active` |
| [0006](https://github.com/Interval-Col/rfcs/blob/main/0006-cobol-decommissioning.md) | COBOL decommissioning — strangler-fig migration to the Pháros stack | `draft` |
| [0007](https://github.com/Interval-Col/rfcs/blob/main/0007-onprem-ha-dr-topology.md) | On-prem production infrastructure — virtualization platform, HA, and DR | `draft` |
| [0008](https://github.com/Interval-Col/rfcs/blob/main/0008-pharos-design-system.md) | Pháros design system — shared FE foundation + endorsed sub-brands | `accepted` |
| [0009](https://github.com/Interval-Col/rfcs/blob/main/0009-bitbucket-to-github-forge-migration.md) | Bitbucket → GitHub forge migration (decommission the intervalica workspace) | `draft` |
| [0010](https://github.com/Interval-Col/rfcs/blob/main/0010-planning-as-code-and-self-hosted-reporting.md) | Planning-as-code and self-hosted team-sync reporting | `draft` |

> RFC 0009 and 0010 each carry companion working files in the rfcs repo
> (`0009-disposition-tracker.md`, `0009-docker-images-note.md`,
> `0010-grounding-survey.md`) — trackers/surveys, not separate RFCs.

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
