"""
Mission tracker using AgentID MCP.

Three agents coordinate a feature build via structured missions:
  @pm_agent       — breaks a feature request into tasks, creates missions
  @engineer_agent — picks up a task, marks it in-progress, completes it
  @summary_agent  — reads all missions and writes a status report

Shows: start_mission, update_status, read_mission

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

PM_SYSTEM = """
You are @pm_agent, a product manager responsible for breaking down feature requests
into trackable engineering tasks.

When given a feature request:
1. Break it into 3-5 concrete engineering tasks.
2. For each task, call start_mission(title="<task>", goal="<specific deliverable>").
3. Write a summary to memory:
   write_memory(key="feature_tasks", value="<list of task titles and their mission IDs>")
4. Call report_activity() confirming the tasks are created.
5. Print the mission IDs so the engineer knows which ones to pick up.

Tasks should be specific and independently completable (e.g., "Add database migration",
not "Do the backend work"). Include the mission ID in your output.
""".strip()

ENGINEER_SYSTEM = """
You are @engineer_agent, an engineer who picks up tasks from the mission tracker.

At the start of your session:
1. Call read_mission() with no arguments to list all active missions.
2. Pick the first one with status "pending" or "not_started".
3. Call update_status(mission_id=<id>, status="in_progress", notes="Starting work")
4. Simulate completing the work (describe what you'd do in a real implementation).
5. Call update_status(mission_id=<id>, status="completed", notes="<what was done>")
6. Call report_activity() with a summary of what was completed.

Be specific in your status notes — the summary agent will read them.
""".strip()

SUMMARY_SYSTEM = """
You are @summary_agent, responsible for generating project status reports.

To generate a report:
1. Call read_memory(key="feature_tasks") to get the list of mission IDs.
2. Call read_mission(mission_id=<id>) for each mission to get its current status.
3. Write a clear status report covering:
   - Overall completion percentage
   - Which tasks are done, in-progress, and pending
   - Any notes from completed tasks
4. Write the report to memory:
   write_memory(key="status_report", value="<full report>")
5. Call report_activity() confirming the report is ready.
""".strip()

SAMPLE_FEATURE = (
    "Add user authentication: login/logout endpoints, JWT tokens, "
    "password hashing, session management, and logout-on-password-change."
)


async def run_pm(feature_request: str) -> str:
    print("\n=== @pm_agent — creating tasks ===\n")
    return await run_agent(
        handle="pm_agent",
        system=PM_SYSTEM,
        user_message=(
            f"Break this feature request into engineering tasks and create missions:\n\n"
            f"{feature_request}"
        ),
    )


async def run_engineer() -> str:
    print("\n=== @engineer_agent — picking up a task ===\n")
    return await run_agent(
        handle="engineer_agent",
        system=ENGINEER_SYSTEM,
        user_message="Check the mission tracker for pending tasks and pick one up.",
    )


async def run_summary() -> str:
    print("\n=== @summary_agent — generating status report ===\n")
    return await run_agent(
        handle="summary_agent",
        system=SUMMARY_SYSTEM,
        user_message="Generate a status report for the current feature build.",
        max_tokens=4096,
    )


async def main():
    print("Mission Tracker Demo")
    print("====================")
    print("PM creates tasks -> Engineer picks one up -> Summary agent reports status\n")

    use_sample = input("Use sample feature request? (y/n, default y): ").strip().lower()

    if use_sample != "n":
        feature = SAMPLE_FEATURE
    else:
        feature = input("\nDescribe the feature: ").strip()
        if not feature:
            feature = SAMPLE_FEATURE

    await run_pm(feature)

    input("\nTasks created. Press Enter to start the engineer session...")
    await run_engineer()

    input("\nTask completed. Press Enter to generate the status report...")
    await run_summary()

    print("\n=== Done ===")
    print("Status report saved in memory under 'status_report'.")
    print("View all missions at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
