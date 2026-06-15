# `agents/` — agent files & artifacts

This directory holds two kinds of file, distinguished by extension + content.

## The contract

| Pattern | Meaning |
|---|---|
| **`*.agent.md` + YAML frontmatter** (`name` / `description` / `tools`) | An **invokable agent**. The frontmatter is what makes it loadable; the body is the system prompt. |
| **plain `*.md`** (no frontmatter) | A **data artifact** — a template, example, or doc referenced *by* an agent. Not invokable on its own. |

Minimal frontmatter for an invokable agent:

```yaml
---
name: "my-agent"
description: "Use when ..."   # when to reach for it
tools: [read, edit, search]   # tools it may use
---
```

## Current files

### Invokable agents (`*.agent.md`)
- **`pharos-frontend.agent.md`** — the Pháros-aligned frontend agent (Nuxt 4 + Vue 3 + Tailwind v4, Pháros design system / registry tokens). The frontend agent. *(Replaced the former `lch-frontend.agent.md`, removed in this harmonization — see git history.)*
- **`plan-craft.agent.md`** — authors/rebuilds execution plans for the junior, Spanish-native, AI-agent-assisted dev team (org plan methodology: structure, bilingual surfaces, markers, tone).
- **`operator-calibration.agent.md`** — runs the operator calibration protocol (multiple-choice) to tune human↔agent collaboration and write a private operator profile.

### Data artifacts (plain `*.md`)
- **`operator-profile-template.md`** — blank operator profile, filled by `operator-calibration` and stored in private agent memory (not committed).
- **`operator-profile-example.md`** — anonymized "what good looks like" sample profile.

## Adding an agent

Name it `<slug>.agent.md`, add the frontmatter above, write the system prompt in the body, and list it here. If you're adding a template/example/doc instead, use a plain `.md` and file it under "Data artifacts."
