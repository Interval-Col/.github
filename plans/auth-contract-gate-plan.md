---
status: in-progress
owner: gczuluaga
created: 2026-07-07
issue: Interval-Col/.github#109
epic: Interval-Col/finance-lch#101
rfc: 0016
sibling: plans/db-tenant-gate-plan.md
---

# auth-contract gate — build plan (RFC 0016 Phase 1)

The anti-drift spine for the shared roles/capabilities module. Mirrors the
`db-tenant-check` build (`plans/db-tenant-gate-plan.md`): a normative contract in
`.github`, a reusable `workflow_call` gate + stdlib-only checker, per-repo
adoption, advisory → required. Difference from the DB gate: the three auth
modules **start non-conformant by construction** (that is the drift RFC 0016
pays down), so adoption is advisory during convergence, not green-on-day-one.

## Phase 1 — contract + gate (this issue, #109)

- [x] `auth-contract.md` — normative contract (C1–C8) + the `.auth-contract.yml` manifest shape + adoption + rollout.
- [x] `.github/workflows/auth-contract-check.yml` — reusable `workflow_call` (inputs `runner`/`enforce`/`manifest`; self-hosted; no secrets), mirroring `db-tenant-check.yml`.
- [x] `scripts/auth-contract-check.py` — stdlib-only checker, A1–A8, shares the strict mini-YAML parser + report/annotation/exit scaffolding with `db-tenant-check.py`.
- [x] Verified locally against all five apps (advisory): finance & admission → A4 FAIL (startup seeding), all three → A6 WARN (role width), clones → A7 INFO (no registry); lab-qc conformant; greenfields conformant. No false positives.
- [ ] Cross-links: `README.md`, `ENGINEERING_STANDARDS.md`, `BRANCHING-AND-DEPLOY.md` (required-checks row + gate-seam note).
- [ ] Conformance dashboard row per app (hand-seeded, alongside `operations/ops/db-tenant/DASHBOARD.md`; never Pages).

## Phase 2 — per-app adoption (each under its RFC 0016 issue)

Each app adds a root `.auth-contract.yml` manifest + a thin caller workflow
(`.github/workflows/auth-contract-check.yml`, `uses: …@main`, `enforce: false`).
Drafts of all five manifests already exist (untracked) in the app repos as a
head-start. Adoption lands with each convergence PR:

- [ ] finance-lch (#111) — A4/A6 already flagged; adopt + fix startup seeding + widen `role`.
- [ ] lab-qc (#73) — conformant today; adopt now (`enforce: false`), flip true after the registry (A7) + width (A6) land.
- [ ] admission-patient (#165, PILOT) — adopt + move bootstrap-admin seed to a deploy step + registry + matrix.
- [ ] commercial-lch (#72) / biuman-lis (#25) — greenfield manifests; full contract at auth-module build.

## Phase 3 — flip to required

Per app, once its first run is green: caller `enforce: true` + mark
`auth-contract-check / auth-contract-check` a required status on `develop`+`main`
(the `db-tenant-check` recipe). New/greenfield adopters enforce from day one.

## Notes

- The checks are **text-level heuristics** (cheap, deterministic, stdlib-only, no PyPI on the merge path). They catch the drift classes that actually occurred across the three clones; the RFC + human review cover judgment.
- A fix merged to the checker `@main` heals every app at once — no re-adoption.
- Allowlists (`startup_seed_allow`, `require_role_allow`) are the escape hatch: a manifest entry with a written reason, reviewed like any code change.
