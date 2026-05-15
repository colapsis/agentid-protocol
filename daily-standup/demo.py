"""
Daily standup agent using AgentID MCP.

Log work as you go. Generate your standup in the morning.
The agent remembers everything across sessions.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio
from datetime import date

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

TODAY = date.today().isoformat()


async def log_work(update: str) -> str:
    print("\n=== Logging work update ===\n")
    return await run_agent(
        handle="standup_bot",
        system=(
            "You are @standup_bot. Your job is to remember what the user is working on. "
            f"Today is {TODAY}. When the user tells you what they did or are doing, "
            f"save it to memory using today's date in the key (e.g. '{TODAY}_work', "
            f"'{TODAY}_blockers'). Confirm what you saved. Be brief."
        ),
        user_message=update,
        max_tokens=1024,
    )


async def generate_standup(for_date: str = None) -> str:
    target = for_date or TODAY
    print(f"\n=== Generating standup for {target} ===\n")
    return await run_agent(
        handle="standup_bot",
        system=(
            "You are @standup_bot. Generate a concise standup report. "
            "Search memory for recent work logs. Format as:\n\n"
            "Yesterday:\n- ...\n\nToday:\n- ...\n\nBlockers:\n- ..."
        ),
        user_message=f"Generate my standup for {target}. Search memory for recent activity.",
        max_tokens=1024,
    )


async def main():
    print("Daily Standup Bot")
    print("=================")
    print("Log work as you go. Generate your standup in the morning.\n")

    action = input("What do you want to do?\n  1. Log work\n  2. Generate standup\n> ").strip()

    if action == "1":
        update = input("\nWhat did you work on? ").strip()
        if update:
            await log_work(update)
            print("\nLogged. Run again to log more, or choose option 2 to generate your standup.")
    elif action == "2":
        await generate_standup()
    else:
        print("Running demo: logging a sample update then generating a standup...\n")
        await log_work(
            "Finished the auth refactor, opened PR #42. "
            "Reviewed Alice's migration. Still waiting on design review from Bob."
        )
        await generate_standup()

    print("\n=== Done ===")
    print("View the full activity feed at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
