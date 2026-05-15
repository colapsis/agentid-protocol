# Persistent Memory

The "hello world" of AgentID. A personal assistant that remembers your name, timezone, and project focus across sessions. On first run it asks who you are. On every run after that, it greets you by name.

This example shows all three memory primitives.

## How it works

```
First run
  -> read_memory("user_profile")    # returns empty
  -> "Hi! What's your name and what are you working on?"
  -> user: "I'm Alex, UTC+1, working on a Rust compiler"
  -> write_memory("user_profile", "name: Alex, tz: UTC+1, project: Rust compiler")
  -> report_activity("New user profile saved")

Second run (new session, new process)
  -> read_memory("user_profile")    # returns the profile
  -> "Hey Alex! Still working on the Rust compiler?"

Any time during conversation
  -> search_memory("what timezone")  # semantic search, finds the profile
```

Memory persists indefinitely. There's no session state — everything lives in AgentID.

## The three memory primitives

| Tool | When to use |
|---|---|
| `write_memory(key, value)` | Store a specific fact under a known key |
| `read_memory(key)` | Retrieve by exact key — fast, deterministic |
| `search_memory(query)` | Find relevant memory by meaning — good for open-ended recall |

## Setup

### 1. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create `personal-assistant`, attached to any persona.

### 2. Add to Claude Desktop

```json
{
  "mcpServers": {
    "assistant": {
      "url": "https://agentid.live/api/mcp/personal-assistant",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Get your key at [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Use it

Select the `assistant` server in Claude Desktop and say anything. The first time, it will ask who you are. Every time after, it will already know.

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

Run it twice. The second run greets you by name with no prompting.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to inspect the stored memory keys, browse the activity feed, and watch memory accumulate across sessions.
