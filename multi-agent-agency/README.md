# Multi-Agent Agency

Three specialized agents form a writing pipeline: researcher gathers information, analyst synthesizes and finds the best angle, writer produces the final polished piece. Each agent hands off to the next via `handoff()`.

## How it works

```
@researcher
  -> start_mission("Write piece on AI agents in production")
  -> write_memory("research_overview", ...)
  -> write_memory("research_key_facts", ...)
  -> write_memory("research_angles", ...)
  -> handoff(to_agent="analyst", context="Keys: research_*")

@analyst
  -> read_mission()           # sees the handoff
  -> read_memory("research_overview")
  -> read_memory("research_key_facts")
  -> write_memory("analysis_outline", ...)
  -> handoff(to_agent="writer", context="Outline in analysis_outline")

@writer
  -> read_mission()           # sees the handoff
  -> read_memory("analysis_outline")
  -> read_memory("research_*")
  -> write_memory("final_piece", "...")
  -> update_status(mission_id, "completed")
```

All three agents share one persona's memory. Handoff notes don't need to repeat the research — they just name the memory keys. The next agent reads them directly.

## Setup

### 1. Create three agents

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `researcher` — attached to a shared persona (e.g. "writing-agency")
- `analyst` — attached to **the same persona**
- `writer` — attached to **the same persona**

All three will share memory and mission state.

### 2. Add to Claude Desktop

```json
{
  "mcpServers": {
    "researcher": {
      "url": "https://agentid.live/api/mcp/researcher",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "analyst": {
      "url": "https://agentid.live/api/mcp/analyst",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "writer": {
      "url": "https://agentid.live/api/mcp/writer",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

### 3. Run it

**Session 1** — select `researcher`:
> "Research [topic]. Save to memory and hand off to @analyst when done."

**Session 2** — open new window, select `analyst`:
> "Check for handoffs and complete your analysis."

**Session 3** — open new window, select `writer`:
> "Check for handoffs and write the final piece."

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

The demo runs all three sessions sequentially. Press Enter between sessions to step through the pipeline.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see all three agents' activity in one timeline — memory writes, handoffs, and the completed piece.
