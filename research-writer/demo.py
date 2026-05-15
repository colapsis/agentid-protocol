"""
Research -> Writer pipeline using AgentID MCP.

Two agents share one identity. Researcher gathers info and hands off.
Writer picks up from the handoff note automatically — no context lost,
no copy-pasting, no repeated work.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent


async def run_researcher(topic: str) -> str:
    print(f"\n=== Session 1: @researcher_agent ===")
    print(f"Topic: {topic}\n")

    return await run_agent(
        handle="researcher_agent",
        system=(
            "You are @researcher_agent. Your job is to research a topic, "
            "save structured notes to memory, then hand off to @writer_agent. "
            "Always: (1) start_mission, (2) write findings to memory key by key, "
            "(3) handoff() with a clear summary and the memory keys you used."
        ),
        user_message=(
            f"Research '{topic}' for a developer blog post. "
            "Write your findings section by section into memory. "
            "When done, hand off to @writer_agent with the memory keys and clear next steps."
        ),
    )


async def run_writer() -> str:
    print("\n=== Session 2: @writer_agent ===")
    print("Starting session, checking for handoffs...\n")

    return await run_agent(
        handle="writer_agent",
        system=(
            "You are @writer_agent. At the start of every session, call read_mission() "
            "to check for active missions and handoffs addressed to you. "
            "If a handoff is waiting, pick it up immediately — read the memory keys "
            "mentioned and complete the task. Write thoroughly and well."
        ),
        user_message="Check for any handoffs and complete the assigned task.",
        max_tokens=8192,
    )


async def main():
    topic = input(
        "What should the researcher investigate? "
        "(e.g. 'MCP server patterns in 2025'): "
    ).strip()
    if not topic:
        topic = "MCP server patterns developers are using in 2025"

    await run_researcher(topic)

    input("\nResearch done. Press Enter to start the writer session...")

    await run_writer()

    print("\n=== Done ===")
    print("View the full activity feed at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
