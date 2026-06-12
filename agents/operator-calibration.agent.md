# Operator calibration — tuning human↔agent collaboration

> **Resumen (ES).** Un protocolo para que cada persona calibre cómo trabaja con su
> agente (fluidez técnica, autoridad, apetito de riesgo, cómo quiere estar en el
> loop). Mejora notablemente la productividad del agente. **Las respuestas son
> privadas y propias de cada quien** — solo el protocolo, la plantilla y el ejemplo
> se comparten; los perfiles llenos NUNCA van a un repo compartido.

An agent works dramatically better when it knows *who it's working with* — what you
can author vs. only read, what you own vs. what needs sign-off, how cautious to be
where, and how you want to be kept in the loop. ~5 minutes of calibration removes
hours of over-explaining, mis-pitched suggestions, and wrong-altitude work.

## Privacy rules — read first (non-negotiable)

This is **self-owned tooling, not evaluation.** It only works if people answer
honestly, and they only answer honestly if it's safe.

1. **Answers are private to each person.** A filled profile lives in *that person's
   own* agent memory (user-level `~/.claude/…` or their project memory) — **never**
   committed to a shared repo, never readable by peers or managers.
2. **Only three files are shared:** this protocol, the blank template
   (`operator-profile-template.md`), and the redacted example
   (`operator-profile-example.md`). The *answers* are not.
3. **Agent-calibration only** — explicitly **not** a performance file, skills matrix,
   or HR artifact. Repurposing it as one destroys the honesty that makes it useful.
4. **Opt-in.** Nobody is required to do it, or to share any of it.

## How to run it (≈5 min, with your agent)

1. Tell your agent: *"Run the operator calibration on me"* (point it at this file).
2. The agent administers it as a short multiple-choice conversation (the dimensions
   below), one round at a time. Pick the closest option; "other" is always fine.
3. The agent writes the result — using the template — into **your private agent
   memory**, and from then on adapts vocabulary, teach-vs-tell, autonomy, and answer
   format to you.
4. Re-run whenever your role, stack, or risk context changes.

## The dimensions

**Part A — Fluency & background** *(decides: teach the* why *vs. just give the* what*)*
- **Home language(s)** — where *authoring* (not just reading) is effortless.
- **Per-stack depth** — for each language you touch: author fluently / read only / learning.
- **Domain depth** — do you own the business domain (defer to you) or are you learning it (reason out loud)?
- **Background shape** — CS-trained / DBA→architect / domain-expert-who-codes / self-taught generalist (which analogies land).
- **Low-level/internals** — comfortable with runtime/DB/systems internals, or flag-the-trap territory?
- **Register** — precise technical terms / domain glosses / bilingual.

**Part B — Authority, risk, pacing, operating style** *(decides: "just run it" vs. "stop, this needs review")*
- **Change authority** — what you can green-light vs. what needs sign-off (and from whom); any regulatory change-window.
- **Compliance boundary** — formal/external audit on the data? PHI / retention / traceability constraints?
- **Timeline driver** — hard date / ready-when-correct / soft-target-with-pressure.
- **Bandwidth** — focused full-time / a few hours a day / fragmented.
- **Risk posture** — fast-and-verify-after / balanced / belt-and-suspenders — and *where* (dev vs. prod).
- **Cost of an incident** — regulatory / revenue / reputation / personal accountability.
- **In-the-loop** — agent drives & you review / you drive & agent checks / mix by task.
- **Autonomy** — commit-and-show-after / show-diff-before-commit / ask-before-non-trivial.
- **Answer format** — recommendation-first / menu-with-tradeoffs / depends-on-stakes.
- **Your definition of *your* win** + the specific failure you most fear (→ where the agent spends disproportionate rigor).

## Output

A filled `operator-profile` (see `operator-profile-template.md`) in your private agent
memory, plus the agent's standing adaptation to it. See `operator-profile-example.md`
for what "good" looks like.
