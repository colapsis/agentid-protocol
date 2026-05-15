# Research → Writer Pipeline

Two agents share one identity. The researcher gathers information and hands off to the writer. The writer picks up exactly where research ended — no context lost, no copy-pasting.

**Live demo:** [agentid.live/showcase/multi-agent](https://agentid.live/showcase/multi-agent)

## How it works

```
Session 1: @researcher_agent
  -> start_mission("Write blog post on MCP patterns")
  -> write_memory("blog_outline", "Introduction, Pattern 1, Pattern 2...")
  -> write_memory("section_1", "MCP tools are...")
  -> handoff(to="writer_agent", context="Keys: blog_outline, section_1, ...")

Session 2: @writer_agent (separate window or tool)
  -> read_mission()       # sees the handoff automatically
  -> read_memory(...)     # reads each key the researcher saved
  -> writes the final post without re-doing any research
```

Both agents connect to the **same persona**. They share memory, mission state, and handoff notes. When one writes, the other reads.

## Setup

### 1. Create two agents

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `researcher_agent` — attached to a persona (e.g. "dev-blog")
- `writer_agent` — attached to **the same persona**

### 2. Add to Claude Desktop

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

### 3. Run it

**Session 1** — select `researcher`, then:

> "Research [your topic]. Write findings to memory section by section. When done, hand off to @writer_agent."

**Session 2** — open a new Claude window, select `writer`, then:

> "Check for any handoffs and complete the task."

The writer sees the handoff and takes it from there.

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

The demo runs both sessions sequentially in one script. You'll see the researcher save memory keys, then the writer read them and produce the final output.

## What you'll see

After both sessions, open [agentid.live/app/studio](https://agentid.live/app/studio) to see the full activity feed — both agents' tool calls, the handoff event, and the completed output in one timeline.
