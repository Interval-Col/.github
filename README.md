# .github

Org-wide community-health files + engineering standards for **Interval-Col**.

## Guides & standards
- [Engineering Standards](ENGINEERING_STANDARDS.md) — stack, structure, conventions, design gates.
- [Branching & Deploy](BRANCHING-AND-DEPLOY.md) — branching model, CI, deploy.
- [Issue Title Style](ISSUE_TITLE_STYLE.md) — `[Área]` + plain-English outcome, ≤60 chars (hard max 70), so the board reads like a plan.
- [Agent Chat Hygiene](AGENT-CHAT-HYGIENE.md) · [español](AGENT-CHAT-HYGIENE.es.md) — *recommendation* for keeping Claude Code sessions cheap and durable (one chat per task; save knowledge to the repo/memory; when to compact / clear / delete).

## Enforcement & tooling
- [`.pre-commit-config.yaml`](.pre-commit-config.yaml) — pre-commit hooks (branch-name check, gitleaks).
- [`.gitleaks.toml`](.gitleaks.toml) — secret-scan config.
- [`.github/workflows/gitleaks.yml`](.github/workflows/gitleaks.yml) — required CI secret scan.
- [`.github/workflows/stale.yml`](.github/workflows/stale.yml) — stale issue/PR sweeper.
- [`scripts/check-branch-name.sh`](scripts/check-branch-name.sh) — enforce branch naming.
- [`scripts/sync-pharos-registry.sh`](scripts/sync-pharos-registry.sh) — sync the Pháros design-system registry.

## Agents, instructions & templates
- [`agents/`](agents/) — reusable agent definitions (frontend, plan-craft, operator calibration).
- [`templates/`](templates/) — shared doc templates (plan template).
- [`plans/`](plans/) — cross-repo plans (active + [`archive/`](plans/archive/)).
- [`instructions/`](instructions/) — Nuxt + per-area authoring instructions.

## Brands & design system
- [`brands/`](brands/) — brand books: [LCH](brands/hematologico/LCH-BRAND.md), [Interval](brands/interval/INTERVAL-BRAND.md), [Pháros](brands/pharos_brand/BRAND.md).
- [`brands/pharos_brand/registry/`](brands/pharos_brand/registry/) — the product design system (tokens, components). Ported here from the old `instructions/` design files.
