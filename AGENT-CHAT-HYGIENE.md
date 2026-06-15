# 🧹 Agent Chat Hygiene — Interval-Col

> **Org guide — this is a RECOMMENDATION, not enforced.** No CI check, no required setting, nobody's going to bounce your PR over it. It's the advice a senior teammate would give you over coffee about keeping your Claude Code sessions cheap and tidy without ever losing real work. Read it, take the bits that help, ignore the rest.

> 🇪🇸 **Versión en español:** [`AGENT-CHAT-HYGIENE.es.md`](AGENT-CHAT-HYGIENE.es.md).

**TL;DR (safe defaults):** keep durable knowledge in the repo or memory — never _only_ in the chat. Then: **one chat per task**; **`/compact`** to finish the current task; **`/clear`** (or a new chat) to switch tasks or start a new day; **keep** when in doubt (transcripts auto-delete after 30 days); **delete** only a truly-spent transcript. Everything below is the _why_.

---

## 1. The one principle

**Chats are disposable working sessions. The repo and your memory are the persistence layer.**

A Claude Code conversation is a workbench, not a filing cabinet. The moment a decision, a rationale, or an artifact matters beyond _this sitting_, it should live somewhere durable — a doc, an RFC, a plan, the code itself, or memory — **not** trapped in a transcript you're hoping to scroll back through next week.

Once durable knowledge is written where it survives, **throwing away or compacting the chat costs you nothing.** That's the whole game. Externalize first, then be ruthless with the chat.

---

## 2. Why it matters — tokens, in plain language

You don't pay for "having a long chat" the way you pay for storage. You pay every time you _send a turn_, and a long chat re-sends its **entire growing history** on every single turn. The conversation is the cost.

Three things compound here:

- **Long chats re-send a growing context every turn.** Turn 50 of a mega-chat ships all 49 prior exchanges along with your new question. Each turn in a bloated session is more expensive than the same turn in a fresh one — for the same amount of actual signal.
- **Auto-compaction is lossy _and_ costs tokens.** When a conversation approaches the context-window limit, Claude Code automatically replaces older exchanges with a structured summary. Key decisions and learnings are preserved, but **detailed instructions from early in the conversation may be lost.** And the summarization itself is an API call that consumes tokens — you pay to shrink your own history. (Edge case: if a single file or output is so large that context refills _immediately_ after each summary, Claude Code stops auto-compacting and shows a "thrashing" error rather than looping.)
- **The prompt cache goes cold.** Within a session, repeated context can be served from a prompt cache (default TTL **5 minutes**, or 1 hour at 2× cache-write cost) at ~0.1× the base input-token rate. But the cache **expires if not accessed within its TTL window** — so a chat you come back to the _next day_ has a stone-cold cache. The first turn re-pays the full cache-write cost. Picking up a day-old mega-chat is close to worst-case: huge context, no warm cache, little new signal.

**The intuition:** a stale, sprawling chat burns tokens for very little signal. A short, focused one stays cheap. None of this matters if your knowledge is already safe in the repo — which is exactly why principle #1 comes first.

> The Claude Code CLI's auto-compaction and the `/compact` and `/clear` commands are **CLI features**, handled transparently. They are distinct from the Anthropic _API's_ separate beta compaction mechanism (`compact-2026-01-12`, opt-in via SDK config). If you're just using the CLI, you don't touch any of that — `/compact` and `/clear` are plain commands, no beta flags.

---

## 3. One chat per task (not a mega-chat)

Default to **one conversation per task or per logical unit of work.** When you move to a genuinely different thing, start a new chat.

Why not one rolling mega-chat for the whole day?

- Every unrelated turn you add makes _every future turn_ in that chat carry dead weight (see §2).
- Auto-compaction will eventually summarize away the early, detailed parts you might still care about.
- A scoped chat is easier to resume, audit, or hand to a teammate later — the transcript reads as "the thing we did," not "everything I touched on Tuesday."

This isn't about being precious. It's just cheaper and clearer.

---

## 4. The "save gate" before you end a chat

Before you close, clear, or delete a session, run this 10-second check:

> **Is any decision, rationale, or artifact ONLY in this chat?**

If yes — externalize it _first_, then do whatever you want with the transcript:

- [ ] **A decision or its rationale** ("we chose X over Y because…") → a doc, an RFC (`rfcs/`), or a code comment / PR description.
- [ ] **A durable design or plan** → an RFC, a plan file, or `operations/` for runbook-flavored detail.
- [ ] **Working code / config** → commit it (or at least stash/branch it).
- [ ] **A personal convention or preference you want to keep reusing** → memory (see §9).
- [ ] **Cross-repo or team-relevant knowledge** → repo docs, _not_ memory.

If everything that matters already lives in the repo or memory, the transcript is now just scratch paper. The save gate is the one habit that makes everything else in this doc safe.

---

## 5. When to `/compact` (mid-task, same sitting)

Use `/compact` when you're **in the middle of one task, in one sitting, and the context is getting heavy** but you still need the thread to finish _this_ task.

- `/compact` summarizes the current conversation **in place** and saves the summary back into the session transcript — so it's not a permanent loss; the summary becomes the working history.
- You can optionally pass focus instructions (`/compact focus on the API changes`). _The exact interaction model isn't something we can state with certainty — it appears to be passed inline as `/compact [instructions]`, but treat the focus hint as best-effort rather than a guarantee of what's kept._
- **What survives a compaction and reloads from disk:** project-root `CLAUDE.md`, auto memory, the system prompt, and invoked skill bodies (capped ~5 KB/skill, ~25 KB total).
- **What does NOT survive until re-triggered:** path-scoped rules (`paths:` frontmatter) and nested `CLAUDE.md` files in subdirectories — these reload only when Claude next reads a file in that path. So after a compact, if behavior in a subdir feels "off," touch a file there to re-arm its rules.

**Don't** use `/compact` as a way to carry knowledge _between_ tasks. It trims history for the current task; it's not a substitute for writing things down (§4). Mental model: `/compact` trades a one-time summarization cost now for cheaper turns for the rest of this task.

---

## 6. When to start fresh / `/clear` (new task, or next day)

Start a new conversation — or use `/clear` — when:

- You're moving to a **new task** unrelated to the current thread.
- It's **a new day** and you'd otherwise resume yesterday's chat — the prompt cache is cold (§2), so resuming buys you the full context cost with none of the cache savings. A fresh, scoped chat is usually cheaper and clearer.

Good news on safety: **`/clear` does NOT delete anything.** It starts a fresh, empty context and labels/stores the old conversation so it stays resumable (it remains in `claude --resume` and in `/resume`). Both `/clear` and `/compact` preserve history — `/clear` parks the old one under a label and moves you to a clean context; `/compact` summarizes the current one in place. So reaching for `/clear` is low-risk: you get a cheap fresh start and keep the trail.

---

## 7. When to DELETE a transcript — and a safe one-liner

Deleting is for transcripts that are **truly spent**: the work is externalized (§4), you won't resume it, and it has no audit/onboarding value (read §8 before you reach for this).

What deletion actually does and where things live:

- Session transcripts are JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is derived from the working-directory path.
- **Deleting the `.jsonl` removes that session from the `claude --resume` picker** — the resume list is just a scan of existing `.jsonl` files in that project dir. No file, no entry.
- You usually don't _need_ to delete: transcripts are **auto-deleted after 30 days by default** (`cleanupPeriodDays` in settings). Manual delete is for "I want it gone now," not routine cleanup.
- A session's **subagent / workflow artifacts** sit in a sibling dir next to the transcript: `~/.claude/projects/<project>/<session-id>/` (holding `subagents/`, `workflows/`). Workflow runs _may_ also drop transient outputs under `/tmp` (machine-local, auto-cleaned) — not worth hunting down, so the snippet below leaves `/tmp` alone and just removes the transcript + that sibling dir.

### Find the current session, don't hardcode

Never type a session id from memory — derive it at runtime. The `<project>` segment is your cwd path with **every non-alphanumeric character** turned into a dash — dots and slashes alike (e.g. `/Users/you/dev/.github` → `-Users-you-dev--github`, note the double dash). To find the **most recent** transcript for the current project:

```bash
# Project dir for the CURRENT working directory:
proj_dir="$HOME/.claude/projects/$(pwd | sed 's/[^a-zA-Z0-9]/-/g')"

# Most-recently-modified session in this project (likely the current one):
sid="$(ls -t "$proj_dir"/*.jsonl 2>/dev/null | head -1 | xargs -r basename | sed 's/\.jsonl$//')"
echo "project dir : $proj_dir"
echo "session id  : $sid"
```

> Sanity-check `$sid` against the session you actually mean before deleting. If you have the id from a `SessionEnd` hook (§10), prefer that — it's exact.

### The safe, session-scoped clean-up

This **prints what it would remove first**, only touches files matching that one session id, and **never touches `memory/` or any other session**. Review, then run the `rm` lines yourself.

```bash
proj_dir="$HOME/.claude/projects/$(pwd | sed 's/[^a-zA-Z0-9]/-/g')"
sid="${1:-$(ls -t "$proj_dir"/*.jsonl 2>/dev/null | head -1 | xargs -r basename | sed 's/\.jsonl$//')}"

# HARD GUARD — never proceed on an empty id (an empty $sid would collapse the
# paths below to whole directories). Abort loudly instead.
[ -n "$sid" ] || { echo "No session id resolved — aborting."; return 1 2>/dev/null || exit 1; }

echo "== would remove for session: $sid =="
ls -ld "$proj_dir/$sid.jsonl" "$proj_dir/$sid" 2>/dev/null   # transcript + its subagent/workflow artifacts

# --- only after eyeballing the above, run the removal yourself: ---
# rm -rf "$proj_dir/$sid.jsonl" "$proj_dir/$sid"
```

Guardrails baked in:

- **Hard guard on an empty id** — if no session resolves, it aborts, so a target can never collapse to a whole directory.
- It **prints before it removes** — the `rm` line is commented out on purpose; review the `ls` output first.
- It scopes to a **single session id** (`$proj_dir/$sid*`), so other sessions are untouched.
- It **never references `memory/`** — your auto memory and `MEMORY.md` are off-limits and persist regardless (§9).

> **Honest caveat.** Run this on a session you've _moved on from_, not the one you're sitting in. If the same session is still open in another terminal, the resume picker may not update until that session closes and its file syncs — don't count on instant removal of a live session.

---

## 8. When NOT to delete

Don't be delete-happy. A transcript is _evidence of work_, and that has real value. **Keep it** when any of these is true:

- **Work is still in flight.** Obvious, but: if you might pick it back up, keep it resumable.
- **It isn't externalized yet.** If the save gate (§4) isn't fully done, the chat is still the only copy. Don't delete the only copy.
- **You may resume it.** Cheaper to resume a scoped session than to re-explain context from scratch — and within the same day the cache may still help.
- **Audit / "why did we do this" trails.** Decisions made interactively, especially ones touching infra, security, schema, or anything in `nucleus-db` / RFC territory, are worth keeping for traceability.
- **Onboarding value.** A clean transcript of "how we built X" can teach the next person more than a tidy summary.
- **PR or debug trails.** The conversation that produced a fix or shaped a PR is useful when a reviewer asks "what did you try?" or when the bug resurfaces.

Remember the defaults already protect you: 30-day auto-cleanup means you rarely _need_ to delete manually. When unsure, **keep** — and lean on `/clear` (§6), which gives you a cheap fresh start _without_ destroying anything.

---

## 9. Memory vs repo — what goes where

Both survive across sessions and are **independent of chat transcripts** — they're not removed when you delete a `.jsonl`. The split is about _audience_:

| Knowledge | Where it goes | Why |
|---|---|---|
| Team-durable: decisions, designs, rationale, cross-repo conventions, runbooks | **Repo** — docs, `rfcs/`, plans, `operations/`, code comments, PR descriptions | The team needs it; it must be reviewable and discoverable, not stuck on your machine |
| Personal: your working prefs, your shortcuts, conventions you keep re-stating to Claude | **Memory** (`CLAUDE.md`, auto memory at `~/.claude/projects/<project>/memory/MEMORY.md`) | Reusable for _you_ across sessions; no value forcing it on teammates |

How file-based memory loads (so you know what's "free" at session start):

- **Auto memory:** the first **200 lines or 25 KB of `MEMORY.md`** (whichever comes first) loads at session start. Topic files (`debugging.md`, `architecture.md`, …) are read **on demand**, not at startup — so keep the hot stuff near the top of `MEMORY.md` and push detail into topic files.
- **`CLAUDE.md` files walk up the directory tree** from your cwd, loading from both `./` and `./.claude/`. Files in subdirectories load **on demand** when Claude reads a file there. `CLAUDE.local.md` is appended after `CLAUDE.md` at each level.
- Settings (and thus hooks, §10) follow a precedence chain: **Managed > CLI flags > Local (`.claude/settings.local.json`) > Project (`.claude/settings.json`) > User (`~/.claude/settings.json`)**. Array settings like `permissions.allow` combine across scopes; scalar settings take the most specific value.

> Rule of thumb: **if a teammate would benefit, it belongs in the repo. If only future-you benefits, memory is fine.**

---

## 10. Optional opt-in: a `SessionEnd` reminder hook

**Fully optional, opt-in, personal.** If you like the idea of being _reminded_ of the safe delete command when a session ends, you can add a `SessionEnd` hook to your **personal** `~/.claude/settings.json`. It **prints** a runtime-derived, session-scoped command for you to review and run yourself — **it never runs `rm`.**

```jsonc
// ~/.claude/settings.json  (PERSONAL scope — opt-in, not committed, not org-mandated)
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "tp=$(jq -r '.transcript_path // empty'); [ -n \"$tp\" ] && printf 'Chat ended. If this work is saved (repo/memory), review then delete it:\\n  rm -rf \"%s\" \"%s\"\\n' \"${tp%.jsonl}\" \"$tp\""
          }
        ]
      }
    ]
  }
}
```

Notes and honest limits:

- **`SessionEnd` fires when a session terminates** and receives a **JSON payload on stdin** — `session_id`, `transcript_path`, `cwd`, `hook_event_name`, and a `reason` (`clear` / `resume` / `logout` / `prompt_input_exit` / …). The hook reads `transcript_path` with **`jq`** and derives the dir + transcript at runtime — **nothing is hardcoded.** (Needs `jq` installed.)
- **It builds the command but never executes the delete.** Deliberate: you stay the one who decides, after the save gate (§4).
- **A hook can't converse or judge.** `Stop` and `SessionEnd` hooks only run shell commands and fire _after_ Claude is done, so they can't reason about whether your work is actually saved. It's a dumb, helpful reminder; the judgment is yours.
- _Surfacing caveat — treat as experimental._ Whether the hook's stdout is shown to you at session end depends on your Claude Code version. If you don't see it, have the command emit a `systemMessage` instead — a hook can print JSON like `{"systemMessage":"…"}`, which is the documented channel for user-shown text.

If you don't want the reminder, do nothing — none of this is required.

---

## 11. Decision cheat-sheet

| Situation | Do this | Destroys anything? |
|---|---|---|
| Mid-task, one sitting, context getting heavy, need to finish _this_ task | **`/compact`** (optionally with a focus hint) | No — summarizes in place, saved to transcript |
| New, unrelated task / next day (cold cache) | **`/clear`** or start a new chat | No — old chat parked & resumable |
| Task done, knowledge externalized (§4), no audit/onboarding value, won't resume | **Delete** the `.jsonl` (use the §7 one-liner; review first) | Yes — removes it from resume picker |
| Work in flight, not yet externalized, might resume, or has audit/PR/debug/onboarding value | **Keep** it (auto-cleanup handles it at 30 days) | — |
| Want an end-of-session nudge toward the delete command | **Opt into the §10 `SessionEnd` hook** (personal settings) | No — it only prints |

**The through-line:** put durable knowledge where it survives (repo + memory), keep each chat scoped to one task, and then treat the transcript as cheap. Compact to finish, clear to switch, keep when in doubt, delete only when it's truly spent.

---

_Questions, or think a heuristic here is wrong for how your team actually works? Open a PR against this file — it's a living recommendation, not a rulebook._
