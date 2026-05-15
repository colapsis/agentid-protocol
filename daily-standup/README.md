# Daily Standup

Log work as you go. Generate your standup in the morning. The agent remembers everything across sessions.

## How it works

```
Throughout the day
  -> write_memory("2026-05-16_work", "Finished auth refactor, opened PR #42")
  -> write_memory("2026-05-16_blockers", "Waiting on design review from Bob")

Next morning
  -> search_memory("2026-05-16")   # finds yesterday's notes
  -> formats standup: yesterday / today / blockers
```

One agent, persistent. Your standup is based on what you actually did — not what you can remember at 9am.

## Setup

### 1. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create `standup-bot`, attached to a persona (e.g. "my-work").

### 2. Add to Claude Desktop

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

Get your key at [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Log work as you go

Select the `standup` server in Claude Desktop and tell it what you did:

> "I just finished the auth refactor and opened PR #42. Still waiting on design review for the settings page."

Do this whenever you finish something, hit a blocker, or switch context.

### 4. Generate your standup

Next morning:

> "Generate my standup for today."

Output:

```
Yesterday:
- Finished auth refactor, opened PR #42
- Reviewed @alice's database migration

Today:
- Start on the settings page redesign

Blockers:
- Waiting on design review from @bob
```

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

Choose option 1 to log work, option 2 to generate a standup, or press Enter to run the full demo with a sample update.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see the full activity log — every note saved, every standup generated.
