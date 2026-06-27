---
description: Scaffold a Spanish operator/team guide in operations/guides/ from the relevant code or flow, fill its app/repo frontmatter, index it, and commit. Output is Spanish (neutral Colombian).
---

# /guide — capture an operator / team guide

You are writing a **user-facing guide** for operators or teammates and
filing it in the **centralized, private** guides home. Capture is a step
in the work: write it while the flow is fresh in this session.

Optional argument: `$ARGUMENTS` is a short title or topic hint (e.g.
`cómo se enrola un terminal`). If empty, infer the topic from the session.

> **Home & language (locked):** guides are **centralized** in
> `operations/guides/` — `operations` is a **private** repo, so guides may
> describe internal flows freely. Output is **Spanish (neutral Colombian
> — warm, polite; no voseo / "parce" / paisa).** Code and DB terms stay in
> **English**.

## 1 · Create the guide file

Path: `operations/guides/<kebab>.md`

- `<kebab>` — short, lowercase, hyphenated; from `$ARGUMENTS` or the
  inferred topic.

If `operations/` is a sibling repo (it is, under `~/dev/operations`),
write the file there. Use the absolute path
`/Users/gczuluaga/dev/operations/guides/<kebab>.md`.

Copy the structure from **`.github/templates/guide-template.es.md`** (the
canonical Spanish guide template). Match the house style of any guide
already in `operations/guides/`.

**Fill the YAML frontmatter** — note the **required `app:` and `repo:`
fields** that state which app + repo this guide pertains to:

```yaml
---
title: <Título en español>
app: <the product, e.g. admission-patient / Pháros Admisiones>
repo: <the repo this guide is about, e.g. admission-patient>
audience: operador | recepción | administrador   # adjust to fit
status: borrador
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: @gczuluaga
---
```

Set **`status: borrador`** (draft) — the user promotes it to `vigente`
later. Set both `created` and `updated` to today.

## 2 · Draft the steps from the code / flow

Read the relevant code, endpoints, or flow in the current repo and turn it
into clear operator steps — **what the user does and sees**, not the
implementation. Good guides in this house include:

- A short **TL;DR / "En breve"** up top.
- **"Para qué sirve esta guía"** (what the reader will understand).
- Numbered steps, often with a small ASCII flow diagram and a
  paso/quién/qué-pasa table.
- **"¿Qué pasa si…?"** troubleshooting table and a short FAQ.
- **"Estado actual"** if the feature is partially shipped.
- **"Relacionado"** links (RFCs, ADRs, endpoints, any visual artifact).

Keep all user-facing copy in Spanish; keep `device_id`, `terminal`,
endpoint paths, SQL, etc. in English.

## 3 · Index it

Append a row to the **relevant repo's** `docs/INDEX.md` (the repo named in
the `repo:` frontmatter — e.g. for an `admission-patient` guide, edit
`admission-patient/docs/INDEX.md`), in the **Guides** table:

```
| <Título en español> | <audiencia> | [<kebab>.md](../../operations/guides/<kebab>.md) |
```

The link is relative from that repo's `docs/` to `operations/guides/`
(`../../operations/guides/<kebab>.md`). If the target INDEX has no Guides
table yet, add the section following the shape used by other repos.

## 4 · Commit

The guide and the INDEX live in **two different repos** — commit each in
its own repo, touching **only** the files you created/edited (never
`git add -A`/`.`, never push). Branch off the default first if you are on
it in either repo.

- In `operations`: `docs(guide): add <kebab> — <short title>`
- In the app repo (INDEX row): `docs(guide): index <kebab> guide`

End each commit body with the standard `Co-Authored-By` trailer.

## 5 · Report

Tell the user: the guide path, its `status` (`borrador`), the `app`/`repo`
it was tagged for, which INDEX you updated, and the commit(s). Remind them
to flip `status:` to `vigente` and (optionally) generate a rendered visual
version once they approve the draft.
