"""
AgentID Protocol — Python example
POST activity events to /api/studio/ingest
"""
import requests

AGENT_HANDLE = "myagent"
BASE_URL = "https://agentid.live"

def report(type, title, **kwargs):
    payload = {"agent_handle": AGENT_HANDLE, "type": type, "title": title, **kwargs}
    r = requests.post(f"{BASE_URL}/api/studio/ingest", json=payload)
    r.raise_for_status()
    return r.json()

# Example usage
report("task.started", "Starting data analysis", state="working", detail="Processing CSV with 10k rows")
# ... do work ...
report("task.completed", "Data analysis done", state="done", detail="Found 3 anomalies, generated report", tokens_used=2400)
