# The Pháros chat contract

> **Normative** org standard — RFC 0017 Phase 3 (`rfcs/0017-llm-chat-architecture.md`).
> Machine-checked subset enforced by the reusable workflow
> [`chat-contract-check.yml`](.github/workflows/chat-contract-check.yml) +
> [`scripts/chat-contract-check.py`](scripts/chat-contract-check.py).
> Cites rather than restates: the *what/why* is RFC 0017 (the shared gateway +
> per-app features + registry widget ruling); this doc is the *how* a conforming
> chat feature behaves. Sibling of the [auth contract](auth-contract.md) and the
> [nucleus-db tenant contract](db-tenant-contract.md).

**"Chat feature" here means**: an app's in-app AI assistant — a chat endpoint
that takes a user message (+ short history), optionally retrieves grounding
context from the app's own corpus, and returns an assistant reply. It is the
product surface; it is unrelated to the *gateway* (`pharos-llm-proxy` is the
single cross-tenant service holding provider SDKs/keys, PHI guards, quotas, the
kill switch, and hash-only audit — RFC 0017 Phase 2). The chat feature never
talks to a provider; it talks to the proxy.

Current chat apps: finance-lch («chatbot-ayuda» — source, the reference this
contract is drawn from; dormant in prod, fin#140, revived in RFC 0017 Phase 5).
Planned adopters (no chat feature yet): biuman-lis (KB chat over «Conocimiento
Biuman», Phase 5). Unlike the auth modules — which started non-conformant by
construction (RFC 0016) — chat has exactly one prior implementation, so the
contract is a **forward** baseline: new chats comply from day one.

---

## The contract

| # | Clause | Source of authority |
|---|---|---|
| **CH1** | **All provider calls go through `pharos-llm-proxy`.** A chat feature MUST NOT import a provider SDK (`google-genai`, `openai`, `anthropic`, `vertexai`, …) or call a model endpoint directly. The only outbound path is the shared proxy (`POST /v1/chat`, `/v1/embed`), authenticated with the app's own per-caller secret (`X-LLM-Proxy-Secret`) and identified by its `caller` id. The proxy is the single enforcement point for keys, PHI guards, quotas, kill switch, and hash-only audit. | RFC 0017 Phase 2/3; reference impl: finance-lch `backend/app/features/help/proxy_client.py` |
| **CH2** | **No plaintext prompt/reply persistence.** The chat feature's own tables store **usage/metadata only** — username, token counts, timestamps — never the message or reply body. Content is audited hash-only, and only in the proxy (`llm_proxy_audit`). This is the tenant-data boundary: conversation bodies never land in an app table. | RFC 0017 (hash-only audit); finance-lch `help_chat_usage` |
| **CH3** | **Per-user rate limit, before the upstream call.** Every request is gated by a per-end-user quota (daily + burst) resolved from the app's own store, **before** the proxy call — independent of, and in addition to, the proxy's per-caller/day and org/month token quotas. A failed upstream call does not burn the user's budget. | RFC 0017; finance-lch `rate_limit.check_user_quota` |
| **CH4** | **Graceful degradation.** When the proxy is unreachable or 5xx, the endpoint returns **503** with a neutral Spanish message — never a 500 / stack trace — and the widget renders a "no disponible" state. Chats are **assistive, never load-bearing**; an outage or the kill switch degrades the feature, it never breaks the page. A proxy-side quota (429) surfaces as 429; a blocked-outbound (PHI gate) surfaces as a 200 safe-reply. | RFC 0017 Drawbacks; finance-lch `router.py` (`ProxyUnavailable → 503`) |
| **CH5** | **Cite sources for corpus answers.** A retrieval-backed (RAG / context-stuffing over a corpus) chat MUST return the source ids/labels it grounded on (`sources: [...]`) and surface them in the UI. A chat with no corpus declares `rag: off` and this clause does not apply. | RFC 0017 Phase 3; finance-lch `ChatResponse.sources` |
| **CH6** | **UI copy in neutral-Colombian Spanish (usted).** Every user-facing chat string — launcher/aria labels, empty state, starters, thinking state, error and rate-limit notices — is in es-CO, usted register. *Prose clause — not machine-checked.* | RFC 0017 Phase 3; finance-lch `HelpChat.vue` |
| **CH7** | **Per-app variation is only the corpus + copy.** What varies per app is the endpoint path, retrieval strategy, embeddings (in the app's **own** schema), brand name, and starter prompts — declared in the manifest. The machinery (CH1–CH4) does not vary, and the FE widget is the registry **`PharosHelpChat`** (RFC 0017 Phase 4), parameterized per app — never re-forked. | RFC 0017 §Tenant frame (cross-tenant proxy is stateless re content) / Phase 4 (registry widget) |

---

## Enforcement — `chat-contract-check`

Each chat app carries a `.chat-contract.yml` manifest (its declared shape) and a
thin caller workflow; the check itself lives here and evolves centrally.

| Check | Asserts | Clause |
|---|---|---|
| H1 | manifest valid, referenced paths exist | — |
| H2 | no provider SDK imported anywhere under `chat_dirs` (allowlist = file + reason) | CH1 |
| H3 | the proxy client speaks the contract: `X-LLM-Proxy-Secret` + `LLM_PROXY_URL` + a `/v1/{chat,embed}` route | CH1 |
| H4 | *info/warn:* chat models carry no plaintext prompt/reply column (usage/metadata only) | CH2 |
| H5 | a per-user rate limit exists and the router gates on it (a 429 path) before the upstream call | CH3 |
| H6 | *info/warn:* the router maps a proxy outage to 503 (not a 500) | CH4 |
| H7 | with `rag: on`, the chat response exposes a `sources` field | CH5 |
| H8 | *info until adopted:* with `fe_registry_widget: on`, the FE references the registry `PharosHelpChat` — a hand-rolled `HelpChat.vue` **FAILs** | CH7 |
| H9 | *info until adopted:* with `persona: nerea`, a synced `nerea_persona.py` exists in a `chat_dir`, matches the registry canon byte-for-byte (when the org checkout is reachable; else warn), and `SYSTEM_PROMPT` composes from `NEREA_PERSONA` | CH7 |

The checks are deliberate **text-level heuristics** — cheap, deterministic,
stdlib-only (no PyPI on the merge path, same rule as `auth-contract-check.py` /
`db-tenant-check.py`; the manifest parser is shared verbatim). They catch the
drift classes that matter for a second implementation; the RFC and human review
cover judgment. CH6 (Spanish register) is prose — reviewed, not machine-checked.

### Manifest

```yaml
app: <name>
profile: chat | planned               # planned = adopter, no chat feature yet (H1 + info only)
caller_id: <name>-backend             # the per-caller identity to pharos-llm-proxy

chat_dirs:                            # feature dir(s); the SDK + persistence scan is scoped here
  - backend/app/features/help
proxy_client: backend/app/features/help/proxy_client.py
router: backend/app/features/help/router.py
rate_limit: backend/app/features/help/rate_limit.py
models: backend/app/features/help/models.py   # str or list; scanned for plaintext columns
response_model: backend/app/features/help/router.py   # optional; where the `sources` field lives (defaults to router)

rag: on                               # H7: corpus-backed → a `sources` field is required
frontend_dir: frontend                # app-scoped in a monorepo (e.g. lis/frontend)
fe_registry_widget: off               # H8; flip `on` once the FE mounts PharosHelpChat (Phase 4/5)
persona: off                          # H9; `nerea` = the shared Pháros persona (brands/pharos_brand/NEREA.md §6):
                                      #   sync-pharos-registry.sh --persona-dir <backend-chat-dir> copies the
                                      #   fragment; SYSTEM_PROMPT = NEREA_PERSONA + <local block>. Other values
                                      #   (e.g. `rigel`) = app-owned persona, informational only.
provider_sdk_allow:                   # optional; every entry needs a reason (H2 escape hatch)
  - file: backend/app/features/help/legacy_client.py
    reason: "transitional local proxy, removed in Phase 5 — fin#NNN"
```

Strict YAML subset (scalars, inline/block lists, one-level maps, lists of flat
maps); unquoted `#` starts a comment — quote values containing `#`. The parser
fails loudly on anything else: misparse never passes silently. (Same parser as
`auth-contract-check.py` / `db-tenant-check.py`.)

**Profiles:** `chat` = has a chat feature, full H1–H9 · `planned` = an adopter
whose chat feature is not built yet (H1 + an informational row; the full contract
applies at build time, RFC 0017 Phase 5).

**Scoping note (H2).** The SDK scan is scoped to `chat_dirs`, not the whole
backend, on purpose: the gateway is being *centralized* (`pharos-llm-proxy`), so
a transitional local proxy service or an unrelated SDK use (e.g. an ETL's Gemini
extractor) is out of scope by construction. If a provider SDK genuinely must live
inside a chat dir during a migration, allowlist the file with a reason.

### Adoption (caller)

```yaml
# .github/workflows/chat-contract-check.yml  (standalone file — not in app ci.yml)
name: chat-contract-check
on:
  pull_request:
  workflow_dispatch:
jobs:
  chat-contract-check:
    uses: Interval-Col/.github/.github/workflows/chat-contract-check.yml@main
    with:
      enforce: true   # forward baseline: chat apps comply from day one (see rollout)
```

### Rollout — enforce from day one

Unlike the auth modules (which started non-conformant and adopted `enforce: false`
during convergence, RFC 0016 Phase 1), chat has a single prior implementation and
a clean reference:

- **finance-lch** is the reference the contract is drawn from; its gate run is
  green (H1–H7 pass, H8 info until the FE adopts `PharosHelpChat`), so it adopts
  with **`enforce: true`** — drift blocks the merge, same recipe as
  `auth-contract-check` / `db-tenant-check`.
- **A `planned` adopter** (biuman-lis until its KB chat lands) passes trivially;
  it adopts `enforce: true` now and, when the chat ships, flips `profile: chat` +
  fills the paths in the **same PR** that lands the feature. No warn cycle.

**False-positive escape hatches** (why enforcing is safe): an allowlist entry
with a written reason in the app's own manifest (`provider_sdk_allow`, reviewed
like any code change), and the checker lives here — a fix merged `@main` heals
every app at once, no re-adoption.

---

## References

RFC 0017 (this contract — shared gateway, per-app features, registry widget) ·
RFC 0016 + [`auth-contract.md`](auth-contract.md) (the sibling gate this mirrors;
the D2 no-shared-package precedent) · RFC 0015 +
[`db-tenant-contract.md`](db-tenant-contract.md) (schema-per-owner; the shared
mini-YAML parser) · RFC 0008 (design-system registry — the `PharosHelpChat`
widget, RFC 0017 Phase 4;
[`brands/pharos_brand/registry/chat-widget.md`](brands/pharos_brand/registry/chat-widget.md)) ·
finance-lch `backend/app/features/help/*` (the reference implementation).
