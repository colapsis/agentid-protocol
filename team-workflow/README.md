# Team Workflow

Two agents share one persona's memory and identity. When `@alice` writes something, `@bob` reads it — different agents, shared brain.

Demo: `@alice` summarizes a customer call and writes structured notes to memory. `@bob` reads those notes and drafts the follow-up email. No copy-pasting, no Slack messages, no "can you send me those notes."

## How it works

```
@alice (after a customer call)
  -> write_memory("call_2026-05-16_acme", "Company: Acme, Contact: Sarah...")
  -> write_memory("followup_2026-05-16_acme", "Send showcase link, schedule deep-dive")
  -> handoff(to_agent="bob", context="Notes saved: call_2026-05-16_acme")
  -> report_activity("Call with Acme saved, handed off to @bob")

@bob (separate session, could be a different person's machine)
  -> read_mission()                          # sees @alice's handoff
  -> read_memory("call_2026-05-16_acme")     # reads the call notes
  -> read_memory("followup_2026-05-16_acme") # reads what to follow up on
  -> drafts the follow-up email
  -> write_memory("email_draft_2026-05-16_acme", "<full email>")
```

The key: `@alice` and `@bob` are both attached to the **same persona**. They share a memory store. What one writes, the other reads.

## Setup

### 1. Create two agents on one persona

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `alice` — attached to a persona (e.g. "cs-team")
- `bob` — attached to **the same persona**

### 2. Add to Claude Desktop

```json
{
  "mcpServers": {
    "alice": {
      "url": "https://agentid.live/api/mcp/alice",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "bob": {
      "url": "https://agentid.live/api/mcp/bob",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

### 3. Run it

**Session 1** — select `alice`:
> "I just finished a call with Acme Corp. Sarah Chen, Head of Engineering, is evaluating us vs. Competitor X. Timeline: 3 weeks. Save the notes and hand off to @bob."

**Session 2** — open a new window, select `bob`:
> "Check for any handoffs from @alice and draft the follow-up email."

Bob reads Alice's notes from shared memory and writes the email — no context repeated.

## Real-world extensions

This pattern scales to full teams:
- `@intake` receives a support ticket, categorizes it, hands to `@specialist`
- `@planner` breaks down a project, `@engineer` picks up tasks from memory
- `@monitor` writes alerts to memory, `@oncall` reads and responds

Any agent on the shared persona can read anything any other agent wrote.

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

The demo includes a sample customer call about Acme Corp evaluating AgentID.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see both agents' activity in one feed — Alice's memory writes, the handoff, and Bob's email draft.
