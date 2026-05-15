# AgentID Examples

Real-world agent patterns using the [AgentID MCP server](https://agentid.live).

AgentID gives your AI agent a persistent identity, memory, and coordination primitives — all through one MCP URL. No backend required.

## Examples

| Example | What it shows |
|---|---|
| [research-writer](./research-writer/) | Two agents handing off work through shared memory |
| [code-reviewer](./code-reviewer/) | Single agent that builds knowledge of your codebase over time |
| [daily-standup](./daily-standup/) | Agent that tracks your todos and generates daily summaries |

## Prerequisites

1. Create a free account at [agentid.live](https://agentid.live)
2. Create an agent and grab your API key from [/app/developers](https://agentid.live/app/developers)
3. Clone this repo

## Setup

Each example has:
- `README.md` — walkthrough and expected output
- `claude_desktop_config.json` — copy into your Claude Desktop config
- `demo.py` — Python script to run the same workflow programmatically

```bash
pip install anthropic mcp
```

## How AgentID MCP works

Every agent gets a URL: `https://agentid.live/api/mcp/YOUR_HANDLE`

Add it to Claude Desktop, Cursor, or any MCP client:

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

The agent then has access to: `write_memory`, `read_memory`, `search_memory`, `report_activity`, `start_mission`, `update_status`, `handoff`, `read_mission`, and an API key vault.

---

[Documentation](https://agentid.live/app/developers) · [Live showcase](https://agentid.live/showcase/multi-agent) · [Sign up free](https://agentid.live/register)
