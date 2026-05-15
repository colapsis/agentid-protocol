<div align="center">

# agentid-live/examples

**Real-world patterns for AI agents with persistent identity, memory, and coordination.**

[agentid.live](https://agentid.live) · [Documentation](https://agentid.live/app/developers) · [Sign up free](https://agentid.live/register) · [Live showcase](https://agentid.live/showcase/multi-agent)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

AgentID gives your AI agents a persistent URL, shared memory, and coordination primitives via a single MCP server. No backend required.

```
Your agent code
     │
     ▼
AgentID MCP  ──────────────────────────────────────────────────
     │              write_memory   read_memory   search_memory
     │              start_mission  update_status  read_mission
     │              handoff        report_activity  get_secret
     ▼
Persistent store (memory, missions, activity feed, secret vault)
     │
     ▼
Any other agent connected to the same persona reads it too
```

---

## Examples

| Example | Primitives used | What it shows |
|---|---|---|
| [persistent-memory](./persistent-memory/) | `write_memory` `read_memory` `search_memory` | Hello world — agents that remember across sessions |
| [code-reviewer](./code-reviewer/) | `write_memory` `search_memory` `report_activity` | Single agent that builds codebase knowledge over time |
| [daily-standup](./daily-standup/) | `write_memory` `search_memory` | Log work all day, generate standup in the morning |
| [research-writer](./research-writer/) | `write_memory` `handoff` `start_mission` | Two agents hand off work through shared memory |
| [multi-agent-agency](./multi-agent-agency/) | `handoff` `write_memory` `read_mission` | Three-agent pipeline: researcher → analyst → writer |
| [mission-tracker](./mission-tracker/) | `start_mission` `update_status` `read_mission` | PM + engineer agents coordinate via structured missions |
| [api-key-vault](./api-key-vault/) | `get_secret` | Agents use stored API keys without ever seeing them in config |
| [team-workflow](./team-workflow/) | `write_memory` `read_memory` `handoff` | Two agents share one persona — one writes, one reads |

---

## Quick start

**Prerequisites:** Python 3.10+, an [AgentID account](https://agentid.live/register) (free).

```bash
# 1. Clone
git clone https://github.com/agentid-live/examples
cd examples

# 2. Install dependencies
pip install anthropic mcp

# 3. Set your API key (get it from agentid.live/app/developers)
export AGENTID_API_KEY=ak_live_...

# 4. Run any example
python persistent-memory/demo.py
```

Each example also works with Claude Desktop — copy the `claude_desktop_config.json` into your config and talk to the agent directly.

---

## MCP primitives

Every agent gets these tools via its MCP URL (`https://agentid.live/api/mcp/{handle}`).

### Memory

```python
# Persist anything under a named key
write_memory(key="user_prefs", value="timezone: UTC, language: Python")

# Retrieve by exact key
read_memory(key="user_prefs")

# Semantic search across all stored memory
search_memory(query="what timezone is the user in?")
```

### Missions

```python
# Create a structured task
mission_id = start_mission(title="Analyze Q4 data", goal="Identify top 3 trends")

# Update progress
update_status(mission_id=mission_id, status="in_progress", notes="Processing CSV files")

# Read current state (any agent on the same persona sees this)
read_mission(mission_id=mission_id)
```

### Handoffs

```python
# Pass work to another agent — it sees this on next read_mission() call
handoff(
    to_agent="writer_agent",
    context="Research complete. Memory keys: blog_outline, section_1, section_2.",
    mission_id=mission_id,
)
```

### Activity & secrets

```python
# Log an event to the activity feed (visible in the studio)
report_activity(summary="Reviewed PR #42: found 3 security issues", type="review")

# Retrieve an API key stored in AgentID Drive — never in your config
api_key = get_secret(name="posthog_api_key")
```

---

## Shared utility

All demos import from [`shared/agent_runner.py`](./shared/agent_runner.py), which handles the MCP connection and Anthropic tool-use loop:

```python
from shared.agent_runner import run_agent

result = await run_agent(
    handle="my_agent",
    system="You are @my_agent. ...",
    user_message="Do something useful.",
)
```

---

## Connect to Claude Desktop

Add any agent to Claude Desktop in one step:

```json
{
  "mcpServers": {
    "my-agent": {
      "url": "https://agentid.live/api/mcp/my-agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Works the same in Cursor, Windsurf, or any MCP-compatible client.

---

## Community

- [agentid.live/showcase](https://agentid.live/showcase/multi-agent) — see agents in action
- [agentid.live/app/studio](https://agentid.live/app/studio) — inspect memory, missions, and activity feed
- [Contributing](./CONTRIBUTING.md) — add your own example
- [agentid.live/register](https://agentid.live/register) — free account, no credit card

---

<div align="center">
MIT License · Built with <a href="https://agentid.live">AgentID</a> and <a href="https://github.com/anthropics/anthropic-sdk-python">Anthropic Python SDK</a>
</div>
