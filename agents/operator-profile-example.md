# Operator profile — example (real, anonymized)

> An illustrative filled profile, anonymized and shared with the operator's consent as
> a "what good looks like" sample. **Your own profile stays in your private agent
> memory**, never here.

## Identity & role
- Name / role: Physician-executive — MD, board-certified pathologist; CEO + medical/informatics director.
- What you own end-to-end vs. what others own: owns the data layer end-to-end (DB stewardship, migrations, the data model); the rest of the team works on app surfaces.

## Coding fluency (authoring ≠ reading)
- Author natively: Python; basic FE/Vue and R as needed.
- Write slowly: SQL.
- Read only: Rust; COBOL only with difficulty — read, do **not** write.
- Learning / avoid: lighter on low-level internals and formal-CS core → the agent authors COBOL/Rust *for* this operator and explains SQL.

## Domain authority
- Domains you own (defer to you on semantics): clinical / lab / billing (LIS workflow, tariffs, payers, pathology) — defer on every domain-semantic call; don't reason the domain out loud.
- Domains you're learning (reason out loud): modern web/app architecture patterns and the Rust service surface — walk through tradeoffs here rather than assuming.
- Framing that lands best: clinical-informatics; full SWE vocabulary is fine.

## Working agreement
- Register: English with me; Spanish for team-facing artifacts; code + DB terms in English.
- Change authority: full authority over the data layer (no sign-off chasing).
- Compliance: formal/external audit applies to clinical + billing (CAP-style rigor — traceability, retention).
- Bandwidth: a few focused hours/day → bring decision-ready reviews; do heavy lifting async.
- In the loop: mix by task — agent drives the mechanical/code; surface domain + architecture calls.
- Git autonomy: branch + commit + show the diff after; don't push to shared/main or deploy without OK.
- Answer format: recommendation-first for small calls; menu-with-tradeoffs for big ones.

## Risk posture & stakes
- Posture: fast in dev, **strict at the prod + PHI boundary**; keep an auditable trail.
- An incident costs me: regulatory, revenue/billing, reputation, **and** personal accountability (all four).
- Timeline driver: mostly ready-when-correct on the data layer; hard dates only when a payer/regulatory deadline forces one — flag those explicitly.

## North star
- Win: pay down the data-layer technical debt so I can return to medicine and the business.
- Most-feared failure: **PHI breach or loss** → spend disproportionate rigor on data protection.
