---
description: Scaffold a per-repo ADR (docs/decisions/) from the session's reasoning, index it, and commit it. English. Warns to use an RFC instead when the decision is cross-cutting.
---

# /decision — capture an Architecture Decision Record

You are capturing a decision the user has just made (or is about to make)
in this session as a **per-repo ADR**. Capture is a step in the work, not
an afterthought: do it now, while the reasoning is fresh.

Optional argument: `$ARGUMENTS` is a short title hint for the ADR (e.g.
`device-token sede resolution`). If empty, infer the title from the
session.

## 0 · Decide ADR vs RFC first (threshold gate)

Before scaffolding, judge the **blast radius** of this decision against the
org threshold (see `.github/KNOWLEDGE-MANAGEMENT.md`):

- **ADR (stay here)** — single-repo **AND** reversible **AND**
  low-blast-radius.
- **RFC (stop, escalate)** — cross-repo **OR** a durable org-wide
  constraint **OR** irreversible / touches the **PHI or prod boundary**
  (schema changes, GRANTs, migrations, anything that could leak patient
  data).

If it looks like an RFC, **warn the user clearly before creating anything**:

> ⚠️ This looks cross-cutting (cross-repo / durable org constraint /
> irreversible / PHI-prod boundary). Per the threshold in
> `.github/KNOWLEDGE-MANAGEMENT.md` this likely belongs as an **RFC in
> `Interval-Col/rfcs/`**, not a per-repo ADR. Do you want me to scaffold
> the ADR here anyway (e.g. to promote to an RFC later), or stop?

Wait for the user's call. A repo-local ADR can still be created as a
staging step and promoted to an RFC later — that is fine if the user
chooses it.

## 1 · Determine the next ADR number

Scan `docs/decisions/` in the **current repo** for existing
`NNNN-*.md` files and take the **highest** 4-digit prefix, then add 1.
Zero-pad to 4 digits. If `docs/decisions/` is empty or missing, start at
`0001` (create the directory).

```bash
ls docs/decisions/ 2>/dev/null | grep -oE '^[0-9]{4}' | sort -n | tail -1
```

Next number = that value + 1, zero-padded (e.g. `0003` → `0004`).

## 2 · Create the ADR file

Filename: `docs/decisions/NNNN-kebab-title-YYYY-MM-DD.md`

- `NNNN` — the number from step 1.
- `kebab-title` — short, lowercase, hyphenated; derived from
  `$ARGUMENTS` or the inferred title.
- `YYYY-MM-DD` — today's date.

Copy the structure from **`.github/templates/adr-template.md`** (the
canonical ADR template). Match the existing house style exactly (see any
file already in `docs/decisions/`):

- First line: `# ADR NNNN — <Title> (YYYY-MM-DD)`
- Then **inline** `**Status:** proposed` (no YAML frontmatter).
- Optionally `**Deciders:**` line.
- Sections, in order: **Context** · **Decision** · **Consequences** ·
  **Alternatives considered** · **References**.

**Pre-fill from this session's reasoning:**

- **Context** — the problem, what surfaced it, constraints in play.
- **Decision** — what was decided and the mental model behind it.
- **Consequences** — tradeoffs, follow-on work, anything gated on a human
  decision (mark those `🛑 HUMAN DECISION:`).
- **Alternatives considered** — the options weighed and why each was
  kept/discarded.
- **References** — branches, migrations, RFCs, related ADRs, artifacts.

Write in **English** (ADRs/RFCs/standards are English). Set
**`**Status:** proposed`** — the user accepts it later.

## 3 · Index it

Append a row to this repo's `docs/INDEX.md`, in the **Decisions (ADRs)**
table, matching the existing column layout:

```
| NNNN | <Title> | proposed | YYYY-MM-DD | [NNNN](decisions/NNNN-kebab-title-YYYY-MM-DD.md) |
```

If `docs/INDEX.md` has no ADR table yet, create the section following the
shape used by other repos' indexes.

## 4 · Commit

Commit **only** the files you created/edited (the new ADR + `docs/INDEX.md`)
on the **current working branch** — never `git add -A`/`.`, never push.
Branch off the default first if you are on it.

```
docs(decision): add ADR NNNN — <short title>
```

End the commit body with the standard `Co-Authored-By` trailer.

## 5 · Report

Tell the user: the ADR path, its number + status (`proposed`), whether you
flagged it as a possible RFC, and the commit. Remind them to flip
`**Status:**` to `accepted` once they confirm.
