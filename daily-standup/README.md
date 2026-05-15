# Daily Standup Agent

An agent that tracks what you're working on and generates your standup each morning. Tell it what you did. Ask it what to report. It remembers everything.

## How it works

```
End of day (or throughout the day)
  → write_memory("2025-01-15_work", "Finished auth refactor, opened PR #42...")
  → write_memory("2025-01-15_blockers", "Waiting on design review for settings page")

Next morning
  → search_memory("2025-01-15")   ← finds yesterday's notes
  → generates standup: yesterday / today / blockers
```

One agent, persistent across every session. Your standup is always based on what you actually did — not what you can remember at 9am.

## Setup

### 1. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `standup-bot` — attach it to a persona (e.g. "my-work")

### 2. Add to Claude Desktop

Copy `claude_desktop_config.json` into your Claude Desktop config:

```json
{
  "mcpServers": {
    "standup": {
      "url": "https://agentid.live/api/mcp/standup-bot",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Replace `YOUR_API_KEY` with your key from [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Log work as you go

**In Claude Desktop, select the `standup` MCP server and say:**

> "I just finished the auth refactor and opened PR #42. Still waiting on design review for the settings page."

The agent saves this to memory with today's date.

Do this whenever you finish something, hit a blocker, or switch context.

### 4. Generate your standup

Next morning:

> "Generate my standup for today."

The agent searches memory for recent activity, formats a standup, and optionally copies it to your clipboard or Slack.

## Standup format

```
Yesterday:
- Finished auth refactor, opened PR #42
- Reviewed @alice's database migration

Today:
- Start on the settings page redesign
- Unblock the CI pipeline issue

Blockers:
- Waiting on design review from @bob
```

## Python demo

See `demo.py` for a Python version that logs work and generates standups programmatically.

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see the full activity log — every note saved, every standup generated.
