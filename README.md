# AgentID Protocol

**Portable AI agent identity, persistent memory, and real-time activity reporting.**

AgentID gives every AI agent a persistent identity that travels with it across tools and sessions. Agents connect via MCP or HTTP, report what they're doing, and read/write shared memory tied to their identity.

→ **Dashboard & setup:** [agentid.live](https://agentid.live)

---

## How It Works

```
Your Agent ──MCP──► AgentID MCP Server ──► Identity + Memory + Activity Log
           ──HTTP──► /api/studio/ingest ──► Activity Log (public endpoint)
```

Each agent has:
- A **handle** (`@myagent`) — unique identifier
- An **identity** — persona, role, values, communication style
- A **memory store** — shared key/value facts that persist across sessions
- An **activity log** — structured events streamed to the Studio dashboard

---

## Integration Paths

| Method | Best for |
|---|---|
| [MCP Server](#mcp-server) | Claude Code, Cursor, Windsurf, any MCP-compatible host |
| [HTTP Ingest API](#http-ingest-api) | Any language, custom agents, LangChain, OpenAI Agents SDK |
| [Prompt Export](#prompt-export) | Paste-based integration, any LLM without code changes |

---

## MCP Server

**Endpoint:** `https://agentid.live/api/mcp/{handle}`  
**Transport:** SSE (Server-Sent Events)  
**Auth:** `Authorization: Bearer <mcp_secret>`

### Add to Claude Code

```json
// ~/.claude/mcp.json
{
  "mcpServers": {
    "agentid-myagent": {
      "type": "sse",
      "url": "https://agentid.live/api/mcp/myagent",
      "headers": { "Authorization": "Bearer YOUR_MCP_SECRET" }
    }
  }
}
```

### Tools

The MCP server exposes four tools:

#### `report_activity`

Report a task event to the Studio activity log.

```typescript
report_activity({
  type: "task.started" | "task.progress" | "task.completed" | "task.failed",
  title: string,          // short headline, e.g. "Refactoring auth module"
  state: "thinking" | "working" | "idle" | "done" | "error",
  detail?: string,        // what specifically happened (required for progress/completed)
  tokens_used?: number,   // approximate token count for this step
  platform?: string,      // e.g. "claude-code", "cursor", "api"
  tool_name?: string,     // tool being invoked
  tool_input?: string,    // brief summary (≤200 chars)
  tool_output?: string,   // brief summary of result (≤200 chars)
  progress?: number,      // 0–100
  model?: string,
  duration_ms?: number,
})
```

#### `write_memory`

Persist a key/value fact to the agent's shared identity memory.

```typescript
write_memory({ key: string, value: string })
// e.g. write_memory({ key: "user_timezone", value: "Europe/Berlin" })
```

#### `read_memory`

Read all memory entries for this agent's identity.

```typescript
read_memory()
// Returns: "key: value\nkey2: value2\n..."
```

#### `search_memory`

Semantic search over the agent's memory.

```typescript
search_memory({ query: string })
// Returns matching memory entries
```

### Resources

The MCP server exposes the agent's full identity as a resource:

```
agentid://identity/{handle}   — full persona: name, role, values, style, memory
agentid://skill/{handle}      — operational protocol and usage examples
agentid://memory/{handle}     — live memory entries
```

---

## HTTP Ingest API

For agents that can't use MCP, activity events can be posted directly over HTTP. **No auth required** — the agent handle is the identifier.

**Endpoint:** `POST https://agentid.live/api/studio/ingest`  
**Content-Type:** `application/json`

### Request Body

```typescript
{
  agent_handle: string,     // required — your agent's handle
  type: string,             // required — event type (see below)
  title: string,            // required — short headline

  // Optional fields
  run_id?: string,          // group events into a logical run; auto-generated if omitted
  state?: "thinking" | "working" | "idle" | "done" | "error",
  detail?: string,          // what specifically happened
  platform?: string,        // integration platform
  action?: string,          // e.g. "post.publish", "search.web"
  target?: string,          // e.g. "@username", "https://...", "file.txt"
  tool_name?: string,
  tool_input?: string,      // ≤200 chars
  tool_output?: string,     // ≤200 chars
  progress?: number,        // 0–100
  tokens_used?: number,
  model?: string,
  duration_ms?: number,
  session_id?: string,
  metadata?: Record<string, unknown>,
}
```

### Event Types

| Type | When to use |
|---|---|
| `task.started` | Beginning a new task or sub-task |
| `task.progress` | Meaningful step completed within a task |
| `task.completed` | Task finished successfully |
| `task.failed` | Task failed with an error |
| `memory.update` | Persisting a fact to memory (requires `metadata.key` + `metadata.value`) |

### Example

```bash
curl -X POST https://agentid.live/api/studio/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "agent_handle": "myagent",
    "type": "task.completed",
    "title": "Summarised weekly report",
    "state": "done",
    "detail": "Processed 47 items, generated 3-paragraph summary",
    "tokens_used": 1840,
    "platform": "custom"
  }'
```

### Response

```json
{ "ok": true, "event_id": "evt_abc123", "run_id": "run_xyz" }
```

---

## Prompt Export

For LLMs without code changes. From the dashboard, export your agent's identity as a system prompt and paste it directly.

Available formats: `generic`, `claude`, `openai`, `molebook`

**Export URL:** `GET https://agentid.live/api/agents/{handle}/export?format=generic-prompt`  
Auth: `Authorization: Bearer <mcp_secret>`

---

## Identity Format

Identities are defined as **CanonicalPersona** objects:

```typescript
interface CanonicalPersona {
  name: string,
  tagline?: string,
  role?: string,
  mission?: string,
  values?: string[],
  communication_style?: {
    tone?: string,
    format?: string,
    length?: string,
  },
  expertise?: string[],
  behaviors?: { always?: string[], never?: string[] },
  goals?: string[],
  context?: string,
}
```

---

## Agent Session Protocol

When using MCP, agents should follow this protocol:

```
SESSION START:
  1. call report_activity(type="task.started", title="Session started", detail="<what user asked>")
  2. read agentid://identity/{handle}  — load persona + memory

EVERY TASK:
  • report_activity(type="task.started")    — before starting
  • report_activity(type="task.progress")   — at each meaningful step
  • report_activity(type="task.completed" or "task.failed")  — always end

MEMORY:
  • call read_memory at session start
  • call write_memory whenever you learn a persistent fact
  • one key per fact — never one large blob
```

---

## Authentication

| Credential | Where it's used |
|---|---|
| `mcp_secret` | MCP server Bearer token; also used for export API and `/api/sdk/` endpoints |
| None | Studio ingest (`/api/studio/ingest`) — public endpoint, handle is the identifier |

Get your credentials from the [AgentID dashboard](https://agentid.live/app/agents).

---

## SDK (coming soon)

`@agentid/sdk` — TypeScript/JavaScript client for all protocol operations.  
`@agentid/cli` — `npx @agentid/cli setup` to auto-configure Claude Code and Codex.

---

## License

Protocol specification: [MIT](LICENSE)

---

*Built by [@colapsis](https://github.com/colapsis) · [agentid.live](https://agentid.live)*
