# Code Reviewer

A single agent that builds up knowledge of your codebase over time. Every PR review adds to its memory. The longer it runs, the better its reviews get.

## How it works

```
PR #1 (first run)
  -> search_memory("auth")         # nothing yet
  -> reviews the diff
  -> write_memory("auth_patterns", "We use JWT with 15min expiry, RS256")
  -> write_memory("test_conventions", "Always mock external APIs")
  -> report_activity("Reviewed PR #1: password stored in plaintext")

PR #5 (later)
  -> search_memory("auth")         # finds past notes
  -> search_memory("testing")      # finds testing conventions
  -> gives better, context-aware review
```

The agent doesn't start fresh each session — it accumulates a working knowledge of your codebase.

## Setup

### 1. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create `code-reviewer`, attached to a persona (e.g. "my-codebase").

### 2. Add to Claude Desktop

```json
{
  "mcpServers": {
    "code-reviewer": {
      "url": "https://agentid.live/api/mcp/code-reviewer",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Get your key at [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Use it

Select the `code-reviewer` server in Claude Desktop and paste a diff:

> "Review this PR. Save any patterns or conventions you notice."

Next session, the agent searches its memory before reviewing — giving you consistent, project-aware feedback.

## What gets remembered

The agent builds keys like:
- `auth_patterns` — how your project handles authentication
- `test_conventions` — what tests you require and how they're structured
- `naming_conventions` — file, variable, and function naming rules
- `common_mistakes` — issues that keep appearing across PRs
- `architecture_decisions` — why things are built a certain way

You can also seed it manually:

> "Remember that we always validate input at the API boundary, never inside services."

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

The demo includes a sample diff (a login function with a plaintext password bug) and shows memory building up in real time.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to watch every tool call: memory writes, searches, and activity events logged as they happen.
