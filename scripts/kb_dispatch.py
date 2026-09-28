#!/usr/bin/env python3
"""Tell every registered consumer that a KB changed — then wait for their verdict.

Task 1.3 of `pharos-llm-proxy/plans/nerea-con-conocimiento-plan.md`, run by
`kb-publish.yml` after the KB's site image is in ECR.

Why it waits: **an accepted dispatch (HTTP 204) proves nothing.** GitHub accepts
`repository_dispatch` for a repo with no handler, and for one whose run then
fails (Codex, #70). Admisiones proved it: from 2026-08-28 every `kb-updated`
run it received was red, and biuman-kb's build stayed green for a month. So:

- `notify` consumers get the dispatch, and a non-204 fails the publish;
- `wait` consumers get it with a correlation id; this script finds the run it
  started and fails unless that run finishes `success` within the timeout.

The correlation id travels in `client_payload.correlation_id`. A consumer that
puts it in its `run-name` is matched exactly:

    run-name: ${{ github.event_name == 'repository_dispatch'
                  && format('kb-updated · {0} · {1}', github.event.client_payload.source,
                            github.event.client_payload.correlation_id) || '' }}

One that doesn't is matched by time (the first `repository_dispatch` run created
after the dispatch), with a warning — right in the quiet case, ambiguous when two
KBs publish in the same minute.

Reading the consumer's runs needs `actions: read` on the token. The org bot
(`pharos-planning-bot`) mints it; without that permission the wait fails with a
message saying so, never silently.

    GH_TOKEN=… python3 scripts/kb_dispatch.py --kb biuman-kb --sha <sha>

Exit codes: 0 every consumer answered green · 1 a consumer failed, timed out or
refused the dispatch · 2 usage / registry.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corpus_lib import RegistryError, consumers_of, load_registry  # noqa: E402

API = "https://api.github.com"
DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "corpus-registry.yml"
EVENT = "kb-updated"


class Http:
    """The one door to the GitHub API, so tests can replace it."""

    def __init__(self, token: str) -> None:
        self.token = token

    def request(self, method: str, url: str, body: dict | None = None) -> tuple[int, dict]:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else {})
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            try:
                return exc.code, json.loads(raw) if raw else {}
            except ValueError:
                return exc.code, {"message": raw[:200].decode(errors="replace")}
        except (urllib.error.URLError, TimeoutError) as exc:
            return 0, {"message": str(exc)}


@dataclass
class Outcome:
    repo: str
    app: str
    mode: str
    ok: bool = False
    detail: str = ""
    run_url: str = ""
    warnings: list[str] = field(default_factory=list)


def correlation_id(kb: str, sha: str) -> str:
    run = os.environ.get("GITHUB_RUN_ID", "local")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    return f"{kb}-{sha[:12]}-{run}-{attempt}"


def dispatch(http: Http, owner: str, repo: str, payload: dict) -> tuple[bool, str]:
    code, body = http.request(
        "POST", f"{API}/repos/{owner}/{repo}/dispatches",
        {"event_type": EVENT, "client_payload": payload},
    )
    if code == 204:
        return True, "dispatched (204)"
    return False, f"dispatch refused: HTTP {code} {body.get('message', '')}".strip()


def find_run(http: Http, owner: str, repo: str, cid: str, since: datetime,
             ) -> tuple[dict | None, str | None]:
    """(run, warning). The run whose title carries `cid`, else the first
    repository_dispatch run created after `since`."""
    # One minute of slack: the consumer's clock stamps `created_at`, ours stamps `since`.
    after = (since - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, body = http.request(
        "GET",
        f"{API}/repos/{owner}/{repo}/actions/runs"
        f"?event=repository_dispatch&created=%3E%3D{after}&per_page=30",
    )
    if code == 403:
        raise PermissionError(
            f"HTTP 403 reading {owner}/{repo}'s runs — the token lacks `actions: read`. "
            "Grant it on pharos-planning-bot (org App settings → Repository permissions "
            "→ Actions: Read-only) and accept it on the installation."
        )
    if code != 200:
        raise RuntimeError(f"HTTP {code} listing {owner}/{repo}'s runs: {body.get('message', '')}")
    runs = body.get("workflow_runs", [])
    for run in runs:
        if cid in (run.get("display_title") or "") or cid in (run.get("name") or ""):
            return run, None
    later = sorted(
        (r for r in runs if r.get("created_at", "") >= since.strftime("%Y-%m-%dT%H:%M:%SZ")),
        key=lambda r: r["created_at"],
    )
    if later:
        return later[0], (
            f"{repo}: matched by time, not by correlation id — add the id to the consumer's "
            "`run-name` so two publishes in the same minute cannot be confused"
        )
    return None, None


def wait_for(http: Http, owner: str, out: Outcome, cid: str, since: datetime,
             deadline: float, poll_s: float, clock=time.monotonic, sleep=time.sleep) -> None:
    run = None
    while clock() < deadline:
        if run is None:
            run, warning = find_run(http, owner, out.repo, cid, since)
            if warning:
                out.warnings.append(warning)
        else:
            url = f"{API}/repos/{owner}/{out.repo}/actions/runs/{run['id']}"
            code, body = http.request("GET", url)
            if code == 200:
                run = body
        if run is not None:
            out.run_url = run.get("html_url", "")
            if run.get("status") == "completed":
                out.ok = run.get("conclusion") == "success"
                out.detail = f"run finished `{run.get('conclusion')}`"
                return
        sleep(poll_s)
    out.detail = (
        "no verdict before the timeout — "
        + ("the run is still going" if run else "no run started: is there a `kb-updated` handler "
           "on the default branch?")
    )


def publish(http: Http, owner: str, kb: str, sha: str, consumers: list[dict],
            timeout_s: float, poll_s: float, **clock) -> list[Outcome]:
    """Dispatch to EVERY consumer first, then wait for the `wait` ones against one
    shared deadline — their runs progress in parallel, so waiting in turn costs
    nothing, while dispatching in turn would delay the second consumer by the
    first one's whole run."""
    cid = correlation_id(kb, sha)
    payload = {"source": kb, "sha": sha, "correlation_id": cid}
    outcomes, pending = [], []
    for c in consumers:
        out = Outcome(repo=c["repo"], app=c["app"], mode=c["mode"])
        since = datetime.now(timezone.utc)
        sent, out.detail = dispatch(http, owner, c["repo"], payload)
        if sent and c["mode"] == "notify":
            out.ok = True
            out.warnings.append(f"{c['repo']}: notify-only — nothing verifies that it refreshed")
        elif sent:
            pending.append((out, since))
        outcomes.append(out)
    now = clock.get("clock", time.monotonic)
    deadline = now() + timeout_s
    for out, since in pending:
        try:
            wait_for(http, owner, out, cid, since, deadline, poll_s, **clock)
        except (PermissionError, RuntimeError) as exc:
            out.detail = str(exc)
    return outcomes


def report(kb: str, sha: str, outcomes: list[Outcome]) -> str:
    lines = [f"## kb-publish · `{kb}` @ `{sha[:12]}`", "",
             "| Consumer | Mode | Result | Run |", "|---|---|---|---|"]
    for o in outcomes:
        run = f"[run]({o.run_url})" if o.run_url else "—"
        lines.append(f"| `{o.repo}` ({o.app}) | {o.mode} | {'✅' if o.ok else '❌'} {o.detail} "
                     f"| {run} |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--kb", required=True)
    ap.add_argument("--sha", required=True)
    ap.add_argument("--owner", default="Interval-Col")
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    ap.add_argument("--timeout-minutes", type=float, default=45)
    ap.add_argument("--poll-seconds", type=float, default=30)
    args = ap.parse_args()

    token = os.environ.get("GH_TOKEN", "")
    if not token:
        print("::error::GH_TOKEN is empty — the org bot token was not minted", file=sys.stderr)
        return 2
    try:
        reg = load_registry(Path(args.registry).read_text(encoding="utf-8"), args.registry)
    except (OSError, RegistryError) as exc:
        print(f"::error::corpus-registry.yml is invalid:\n{exc}", file=sys.stderr)
        return 2
    if args.kb not in reg["kbs"]:
        print(f"::error::kb `{args.kb}` is not in the registry", file=sys.stderr)
        return 2
    consumers = consumers_of(reg, args.kb, ("wait", "notify"))
    if not consumers:
        print(f"::notice::{args.kb} has no active consumers in the registry — nothing to tell")
        return 0

    outcomes = publish(Http(token), args.owner, args.kb, args.sha, consumers,
                       args.timeout_minutes * 60, args.poll_seconds)
    text = report(args.kb, args.sha, outcomes)
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
    for o in outcomes:
        for w in o.warnings:
            print(f"::warning::{w}")
        if not o.ok:
            print(f"::error::{o.repo} ({o.mode}): {o.detail}")
    return 0 if all(o.ok for o in outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())
