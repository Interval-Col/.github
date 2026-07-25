# Dependency updates — org standard

How Dependabot is configured across Interval-Col, and why it is configured that
way. Template to copy: [`templates/dependabot.yml`](templates/dependabot.yml).

## The problem this solves

Measured 2026-07-25, before this standard existed:

| Repo | Dependabot PRs since 2026-06-01 | Open | Config |
|---|---|---|---|
| `biuman-lis` | 20 | 10 | weekly, **no grouping, no limit, no cooldown**, filed against `main` |
| `finance-lch` | 15 | 0 | weekly, grouped minor/patch (the good pattern) |
| everything else | 0 | 0 | **no `dependabot.yml` at all** |

Ten open PRs in one repo is not a dependency strategy — it is a queue nobody
drains. There is no org-level `dependabot.yml`: the file is per-repo, read from
that repo's **default branch**, so every repo needs its own copy.

## The standard

Four levers, and they multiply:

| Lever | Setting | Effect |
|---|---|---|
| `schedule.interval` | `monthly` | 1 run/month instead of 4 — one dependency day, not a weekly drip |
| `groups` | minor+patch in one group, major in another | 1–2 PRs per ecosystem per run instead of 1 per package |
| `open-pull-requests-limit` | `2` (`1` for actions) | hard ceiling on what can be outstanding per entry |
| `cooldown.default-days` | `7` | skips packages that released in the last week — kills churn PRs |

Result per repo, per month: **~2–4 PRs** (npm batch, pip batch, actions batch,
plus a majors batch when majors exist) instead of 10–20.

Majors get their **own** grouped PR on purpose. They are the breaking surface —
they deserve a real review, and they must not hold the routine hygiene batch
hostage. Closing a majors PR unreviewed is a legitimate outcome.

`directories` (plural, glob-capable) covers every app in a monorepo from one
entry. List only maintained surfaces — **frozen apps stay out** (e.g.
`pharos-lis/pathology/**`, frozen since 2026-03-06, gets no dependency PRs).

Docker base images are deliberately **not** enabled: high churn, low signal, and
our images are rebuilt from pinned bases on every deploy anyway.

## Volume across the estate

Per repo the standard is calm; multiplied by ~22 repos it is not. Expect
**~25–45 dependency PRs/month org-wide** once every repo is on it — more total
churn than the ~17/month the org saw when only `biuman-lis` and `finance-lch`
had configs, in exchange for the other 20 repos no longer drifting silently.

**Decided 2026-07-25: monthly everywhere, per-ecosystem grouping everywhere** —
freshest dependency surface and the tightest failure isolation (a pip bump that
reddens CI never blocks the npm batch). If the volume turns out to grate, the
lever is tiering, not un-grouping:

- keep the flagship apps (`finance-lch`, `pharos-lis`, `biuman-lis`,
  `admission-patient`, `public-web`) on monthly + per-ecosystem groups;
- move the quiet repos to `interval: quarterly`, a single cross-ecosystem PR
  (`multi-ecosystem-groups`), majors ignored, and no separate actions entry.

That lands the estate near ~15 PRs/month and is a per-repo config edit — no
migration, no new tooling.

## Two traps

**1. The config is read from the DEFAULT branch (`main`), never from `develop`.**
A `dependabot.yml` merged only to `develop` does nothing at all. Our trunk is
`develop` in most repos, so the file has to reach `main` — either on the repo's
next release, or via a config-only PR to `main` where that is safe. Check first:
in `finance-lch` and `pharos-lis` a push to `main` runs `ci-cd.yml` and deploys
**prod**, with no path filter to stop it. In `biuman-lis`, `admission-patient`
and `public-web` the prod deploy is gated behind a repo variable, so a
config-only push to `main` fails the gate job and ships nothing.

**2. `target-branch` silently disables everything security-scoped on that entry.**
The options reference: options marked for security updates apply *"except where
`target-branch` is used."* `finance-lch` carried `npm-security` /
`pip-security` groups next to `target-branch: develop` for weeks — they never
fired once. Do not write security groups on an entry that sets `target-branch`.

Related: **Dependabot security updates are currently OFF org-wide**
(`automated-security-fixes.enabled == false` on every repo checked 2026-07-25),
so today there is no security-PR stream at all — only version updates. Alerts
still fire; nobody opens PRs for them. Turning them on is a separate decision:
it adds a PR stream that always targets `main`, cannot be grouped per the trap
above, and needs its own review lane before it is switched on.

## Review routing — CODEOWNERS, not `reviewers`

Dependabot **cannot assign a GitHub team**: `assignees` takes users only, and
the `reviewers:` key is gone from the current options reference. Team routing
happens through CODEOWNERS, and the team must hold **write** access on the repo
or GitHub ignores it as a code owner.

Append this block to `.github/CODEOWNERS` (last matching pattern wins, so it
goes at the **end** of the file):

```
# ── Dependency manifests → @Interval-Col/dependabot ────────────────────────
# Dependabot PRs touch only these paths, so the deps team is auto-requested for
# review instead of the repo's catch-all owner. See
# Interval-Col/.github → DEPENDENCY-UPDATES.md.
package.json            @Interval-Col/dependabot
package-lock.json       @Interval-Col/dependabot
pnpm-lock.yaml          @Interval-Col/dependabot
pyproject.toml          @Interval-Col/dependabot
uv.lock                 @Interval-Col/dependabot
poetry.lock             @Interval-Col/dependabot
requirements*.txt       @Interval-Col/dependabot
Cargo.toml              @Interval-Col/dependabot
Cargo.lock              @Interval-Col/dependabot
```

`.github/workflows/` is **not** routed to the deps team — CI ownership stays
with the repo's infra owner, so the grouped actions PR still pings them.

## Adding a new repo

1. Copy [`templates/dependabot.yml`](templates/dependabot.yml), keep only the
   ecosystems that exist, point `directories` at the real manifest paths.
2. Set `target-branch: develop` — or delete the line if trunk is the default
   branch.
3. Append the CODEOWNERS block above.
4. Grant the team write:
   `gh api -X PUT /orgs/Interval-Col/teams/dependabot/repos/Interval-Col/<repo> -f permission=push`
5. Land it on **`main`** (see trap 1), not just `develop`.
