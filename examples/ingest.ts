/**
 * AgentID Protocol — TypeScript example
 * POST activity events to /api/studio/ingest
 */

const AGENT_HANDLE = "myagent";
const BASE_URL = "https://agentid.live";

async function report(type: string, title: string, extra: Record<string, unknown> = {}) {
  const res = await fetch(`${BASE_URL}/api/studio/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_handle: AGENT_HANDLE, type, title, ...extra }),
  });
  if (!res.ok) throw new Error(`AgentID ingest failed: ${res.status}`);
  return res.json();
}

// Example usage
await report("task.started", "Drafting email", { state: "working", platform: "custom" });
// ... do work ...
await report("task.completed", "Email drafted", {
  state: "done",
  detail: "450-word reply, 3 action items",
  tokens_used: 890,
});
