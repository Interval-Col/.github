# 🏗️ Engineering Standards — Interval-Col

This document defines the official engineering standards for all primary projects under the Interval-Col GitHub organization, especially as adopted by and standardized in [biuman-reports](https://github.com/Interval-Col/biuman-reports), [lab-qc](https://github.com/Interval-Col/lab-qc), and to be used for [finance-lch](https://github.com/Interval-Col/finance-lch).

---

## 🚀 Stack & Architecture

### **Backend (Python)**
- FastAPI
- Pydantic v2
- SQLAlchemy
- pytest for testing
- Directory structure:
  ```
  backend/
    app/
      core/
      features/
      main.py
      ...
    tests/
    scripts/
    Dockerfile
    pyproject.toml (preferred) or requirements.txt
  ```
- Pin Python version ≥ 3.11
- `.env.example` with all required config variables

### **Frontend (Nuxt 4, Vue 3, TypeScript)**
- Nuxt 4 as framework (SSR/SPA ready)
- Vue 3, Vite, Pinia, Tailwind v4, TypeScript
- Pin Node version in `package.json` and/or `.nvmrc`
- `.env.example` in `frontend/`
- Directory structure:
  ```
  frontend/
    ...
    Dockerfile
    ...
  ```

---

## 📝 Branching, Commits, and CI/CD

| Practice           | Standard                                                            |
|--------------------|---------------------------------------------------------------------|
| Default Branch     | `main`                                                              |
| Integration Branch | `develop`                                                           |
| Feature Branches   | `feat/`, `fix/`, `refactor/`, `test/`, etc.                         |
| Commit Style       | [Conventional Commits](https://www.conventionalcommits.org/)        |
| CI/CD              | GitHub Actions in `.github/workflows/` for lint, test, build, deploy|

---

## 🤖 Tooling, Lint, Format

### Python Backend

- **Linter:** [Ruff](https://beta.ruff.rs/docs/)
- **Formatter:** [Black](https://black.readthedocs.io/en/stable/)
- **Test runner:** pytest
- **Type checks:** mypy (recommended)

### Frontend

- **Linter:** ESLint
- **Formatter:** Prettier
- **Test runner:** Vitest or Jest
- **Style:** Tailwind v4

---

## 🔠 Cross-platform path safety

Mac developers + Linux CI is a mixed-FS environment. macOS APFS is
case-insensitive by default; Git is case-sensitive. **Never commit
two files whose paths differ only in case** (e.g. `Order.ts` and
`order.ts` in the same folder). On Linux they coexist; on macOS the
filesystem can hold only one of the pair, leaving the other
permanently "modified" in `git status` because the disk content can
never match both blobs simultaneously. Recovery from a Mac is
expensive (see the biuman-lis runbook linked below); prevention is
cheap.

### Required in every repo

1. **Pre-commit hook + CI check** rejecting any commit that
   introduces a case-collision pair. Reference implementation:
   [`biuman-lis/scripts/check-case-collisions.sh`](https://github.com/Interval-Col/biuman-lis/blob/main/scripts/check-case-collisions.sh).
   Detection is one-liner:
   ```bash
   git ls-tree -r HEAD | awk '{print $4}' \
     | awk '{print tolower($0), $0}' | sort \
     | awk '{ if ($1==prev) { print "case-collision:", lastpath, "vs", $2; bad=1 } prev=$1; lastpath=$2 } END { exit bad }'
   ```
2. **Repo-level convention**: pick one casing style per folder
   (`PascalCase.ts` for components, `camelCase.ts` for utilities,
   `kebab-case.vue` for pages — whatever the repo settles on) and
   keep it consistent. Mixed casing within a folder is the
   precondition for collisions.

### If a collision lands on `main` anyway

Fix from a case-sensitive system (Linux container, WSL, or a
case-sensitive APFS volume on Mac) — `git rm --cached <dead-path>`
on the dead casing, commit, push. Trying to fix it from a vanilla
Mac requires the index-mirror dance documented in the biuman-lis
[`CONTRIBUTING.md`](https://github.com/Interval-Col/biuman-lis/blob/main/CONTRIBUTING.md)
case-collision runbook because `git stash` and `git reset --hard`
oscillate the dirty status without ever clearing it.

---

## 🛡️ Security & Config

- No secrets/config in source; use `.env.example` for all config.
- All `.env` files listed in `.gitignore`.
- Python/node versions pinned.
- Separate `Dockerfile` for BE and FE.
- Root-level `docker-compose.yml` or `compose.yaml`.

---

## 📄 Project Documentation

- Root `README.md` must document:
  - Architecture overview
  - Setup (BE & FE)
  - How to run tests
  - Local development with Docker
  - Deployment instructions

- Refer to this `ENGINEERING_STANDARDS.md` for any refactor, migration, or new major feature.

---

## 🧑‍💻 Review & Collaboration

- Branch protection on `main`
- Required status checks and PR reviews
- Use PR and Issue templates from `.github/`
- All teams/contributors must follow the standards here for all major projects

---

## Example Project Checklist

- [ ] BE Python: FastAPI, Ruff, Black, pytest, Pydantic v2, `.env.example`, `Dockerfile`
- [ ] FE: Nuxt 4, Vue 3, TypeScript, Pinia, Tailwind v4, ESLint, Prettier, `.env.example`, `Dockerfile`
- [ ] `README.md` and `ENGINEERING_STANDARDS.md` present
- [ ] `.github/` directory with workflows and templates
- [ ] **CI must run all tests, lint, and builds**
- [ ] Branch protection enabled on `main`
- [ ] Case-collision check installed (pre-commit hook + CI step) — see "Cross-platform path safety"

---

_This standards file is the source of truth for new code, refactors, upgrades, and onboarding._
