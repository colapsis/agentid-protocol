# Mission Tracker

Project management via agents. A PM agent breaks a feature request into tasks, an engineer agent picks up a task and marks it done, and a summary agent reads all missions and writes a status report.

Shows `start_mission`, `update_status`, and `read_mission` working together as a lightweight project tracker.

## How it works

```
@pm_agent (receives feature request)
  -> start_mission(title="Add database migration", goal="Create users table")
     # returns mission_id: abc123
  -> start_mission(title="Add password hashing", goal="Bcrypt with cost factor 12")
     # returns mission_id: def456
  -> start_mission(title="Build login endpoint", goal="POST /auth/login -> JWT")
     # returns mission_id: ghi789
  -> write_memory("feature_tasks", "abc123, def456, ghi789")

@engineer_agent
  -> read_mission()             # lists all missions, finds abc123 is pending
  -> update_status("abc123", "in_progress", "Starting migration")
  -> update_status("abc123", "completed", "Created users table with indexes")

@summary_agent
  -> read_memory("feature_tasks")   # gets the IDs
  -> read_mission("abc123")         # status: completed
  -> read_mission("def456")         # status: pending
  -> read_mission("ghi789")         # status: pending
  -> writes: "1/3 complete (33%). abc123: done. def456, ghi789: pending."
```

## Setup

### 1. Create three agents on one persona

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create:
- `pm-agent` — attached to a shared persona (e.g. "engineering-team")
- `engineer-agent` — attached to **the same persona**
- `summary-agent` — attached to **the same persona**

### 2. Add to Claude Desktop

```json
{
  "mcpServers": {
    "pm": {
      "url": "https://agentid.live/api/mcp/pm-agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "engineer": {
      "url": "https://agentid.live/api/mcp/engineer-agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    },
    "summary": {
      "url": "https://agentid.live/api/mcp/summary-agent",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

### 3. Run it

**Session 1** — select `pm`:
> "Break this feature request into tasks: [your feature]. Create a mission for each one."

**Session 2** — select `engineer`:
> "Check the mission tracker for pending tasks and pick one up."

**Session 3** — select `summary`:
> "Generate a status report for the current feature build."

## Mission states

Missions track status through their lifecycle:

| Status | Meaning |
|---|---|
| `pending` | Created, not yet picked up |
| `in_progress` | An agent is actively working it |
| `completed` | Done — notes describe what was delivered |
| `blocked` | Waiting on something |

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

The demo uses a sample feature request (user authentication system) and runs all three agent sessions sequentially.

## What you'll see

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see the mission list, status transitions, and the final status report — all in one place.
