# Code Reviewer Agent

A single agent that builds up knowledge of your codebase over time. Every PR review adds to its memory — patterns, decisions, context. The longer it runs, the better its reviews get.

## How it works

```
Session 1 (first PR)
  → start_mission("review PR #42")
  → write_memory("auth_patterns", "We use JWT with 15min expiry...")
  → write_memory("testing_conventions", "Always mock external APIs...")
  → report_activity("Reviewed PR #42: 3 issues found")

Session N (later PR)
  → search_memory("auth")       ← finds past notes on auth patterns
  → search_memory("testing")    ← finds testing conventions
  → leaves better review because it remembers context
```

The key: memory persists across sessions. The agent doesn't start fresh every time — it builds a working knowledge of your codebase.

## Setup

### 1. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `code-reviewer` — attach it to a persona (e.g. "my-codebase")

### 2. Add to Claude Desktop

Copy `claude_desktop_config.json` into your Claude Desktop config:

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

Replace `YOUR_API_KEY` with your key from [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Use it

**In Claude Desktop, select the `code-reviewer` MCP server and say:**

> "Review this PR. Remember any patterns or conventions you notice for future reviews."

Paste your diff or link your PR. The agent will:
1. Review the code
2. Save notable patterns to memory (auth patterns, naming conventions, common mistakes)
3. Log the review to its activity feed

Next session:

> "Review this PR."

The agent will search its memory for relevant context before reviewing — and give you a better, more consistent review.

## What gets remembered

The agent builds up memory in categories like:

- `auth_patterns` — how your project handles auth
- `testing_conventions` — what tests you require
- `naming_conventions` — file/variable/function naming rules
- `common_mistakes` — issues that keep appearing
- `architecture_decisions` — why things are built a certain way

You can seed it manually too:

> "Remember that we always validate input at the API boundary, never inside services."

## Python demo

See `demo.py` for a Python version.

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see the memory building up over time — every write, every search, every review logged.
