# 🏷️ Issue Title Style — Interval-Col

How we title issues across the org, so the **Project board reads like a plan, not a changelog**.
This governs the **title only** — body and comments follow the normal team register (Spanish).

> Quick rule: **`[Área] short outcome in plain English`** — say *what it delivers*, not *how*.
> Target **≤60 characters**, hard max **70**. Sentence case, no trailing period.

---

## The format

```
[Área] Outcome in plain English
```

- **`[Área]` prefix** — one short code (legend below), mapped 1:1 to the board **Workstream** field, so the prefix and the board chip say the same thing. It keeps the area visible even off-board (search results, notifications, email).
- **Outcome, not mechanism** — describe the result a reader cares about (verb-led), not the implementation. `Stand up the production database`, not `Run prod-deploy-zero ansible play`.
- **Plain English** — issue titles are English (a **deliberate exception** to the Spanish-for-team-facing default: they sit next to repo / commit / code English, and the board's Workstream chip + labels carry the Spanish-readable area). Bodies and comments stay in the team's Spanish register.
- **Length** — aim for **≤60 chars**, never exceed **70** (board cards truncate beyond that). The `[Área]` code counts toward the budget — that's why the codes are short.
- **Sentence case**, no trailing period, no `- [ ]` checkboxes in the title.

### Keep OUT of the title (put it in the body or a field)
- Conventional-commit / scope prefixes: `fix(db):`, `chore(cobolql):`, `feat:` → those belong on **commits/PRs**, not issues.
- Phase / RFC / branch noise: `(RFC 0009 Phase 2)`, `develop → main`, `Phase 4.2` → the **body**.
- Status / area as words (`[BLOCKED]`, `[diferido]`) → the board **Status** / **Workstream** fields + **labels**.
- Issue/PR numbers, dates, owners → GitHub already tracks these.

---

## Área legend (short codes — 1:1 with the board Workstream field)

| Code | Workstream | Covers |
|---|---|---|
| `[Adm]` | Admisiones | admission-patient / Pháros Admisiones |
| `[Com]` | Comercial | commercial-lch (CRM, quotes, agreements) |
| `[Infra]` | Infraestructura | hosts, network, IaC, prod-deploy-zero, RFC 0007 |
| `[Plat]` | Plataforma | nucleus-db, shared platform, identity, security, CobolQL, migrations — **catch-all if nothing else fits** |
| `[Tarifas]` | Tarifas | pricing / tariff chain, fee_set, price_list |
| `[ETL]` | ETL | cobol-migration harness, income/analyte lanes |
| `[Diseño]` | Diseño | Pháros design system, RFC 0008, brand |

Pick the one that matches the card's **Workstream** field. If it genuinely fits none, use **`[Plat]`** and (optionally) propose a new code via PR to this file — the legend is the single source of truth, so it changes here, not ad-hoc.

---

## Examples (real before → after)

| ❌ Before | ✅ After |
|---|---|
| `fix(db): align app DB role to canonical admission_user` | `[Adm] Align the app DB role to admission_user` |
| `Migrate cobolql: Bitbucket → GitHub (RFC 0009 Phase 2)` | `[Plat] Migrate CobolQL from Bitbucket to GitHub` |
| `Ejecutar prod-deploy-zero — nucleus-db de producción` | `[Infra] Stand up the production database` |
| `Service / business calendar (ERP primitive) — opcional…` | `[Plat] Lab operating calendar` |
| `Promote finance-lch a producción (develop → main, first prod release)` | `[Tarifas] Promote finance-lch to production` |

### Good (born right)
- `[Com] Fix $0 prices in the quote search`
- `[ETL] Backfill the analyte coverage gaps`
- `[Diseño] Pick the Pháros sibling palette`

### Avoid
- `feat(scheduling): military 24h time picker` → `[Adm] Use 24h time in the booking picker`
- `nucleus-db prod deploy zero phase 4 schemas + grants` → `[Infra] Apply prod schemas and grants` (phases → body)
- `URGENT!! rotate leaked finance secrets ASAP` → `[Plat] Rotate the leaked finance-lch secrets` (urgency → a label / due date, not SHOUTING)

---

## How to apply

- **New issues:** write the title in this format from the start (the org default issue template pre-fills `[Área] `).
- **The board does the rest:** set **Workstream** to match the prefix, plus **Status** / **Owner** / labels — those carry categorization so the title can stay a clean sentence.
- **Existing issues:** being retrofitted to this style in a reviewed batch (titles are freely editable and renames don't break automation — the board/EOD sync key on `repo#number`, not the title).

This is an org standard (like [Engineering Standards](ENGINEERING_STANDARDS.md) and [Branching & Deploy](BRANCHING-AND-DEPLOY.md)) — adopt it for every repo under Interval-Col.
