# Research → Writer Pipeline

Two agents share one identity. The researcher gathers information and hands off to the writer. The writer picks up exactly where research ended — no context lost, no copy-pasting.

**Live demo:** [agentid.live/showcase/multi-agent](https://agentid.live/showcase/multi-agent)

## How it works

```
Session 1 (@researcher_agent, in Claude Desktop)
  → write_memory("blog_outline", ...)
  → write_memory("section_1", ...)
  → handoff(summary="research done", next_steps=[...], to="writer_agent")

Session 2 (@writer_agent, in Cursor or a new Claude window)
  → read_mission()        ← automatically sees the handoff
  → read_memory(...)      ← reads what researcher saved
  → writes the blog post  ← no repeated research
```

The key: both agents are connected to the **same persona**. They share memory, share mission state, and can hand off work through a structured note that persists until the next agent picks it up.

## Setup

### 1. Create two agents

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `researcher_agent` — attach it to a persona (e.g. "dev-blog")
- `writer_agent` — attach it to the **same persona**

Both agents will now share memory and mission state.

### 2. Add to Claude Desktop

Copy `claude_desktop_config.json` into your Claude Desktop config (usually `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "researcher": {
      "url": "https://agentid.live/api/mcp/researcher_agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "writer": {
      "url": "https://agentid.live/api/mcp/writer_agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Replace `YOUR_API_KEY` with your key from [agentid.live/app/developers](https://agentid.live/app/developers).

### 3. Run it

**Session 1 — open Claude Desktop, select the `researcher` MCP server, and say:**

> "Research [your topic]. Write your findings to memory section by section. When done, hand off to @writer_agent with a summary and the memory keys you used."

**Session 2 — open a new Claude window (or Cursor), select the `writer` MCP server, and say:**

> "Check for any handoffs and complete the task."

The writer will automatically see the handoff and pick up from the researcher's notes.

## Python demo

See `demo.py` for a Python version that drives both agents programmatically.

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

## What you'll see

After running both sessions, open [agentid.live/app/studio](https://agentid.live/app/studio) to see the full activity feed — both agents' tool calls, the handoff event, and the completed output.
