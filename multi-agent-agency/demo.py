"""
Multi-agent agency pipeline using AgentID MCP.

Three specialized agents form a writing agency:
  @researcher  — searches and gathers information on a topic
  @analyst     — receives handoff, critiques and synthesizes
  @writer      — receives handoff, writes the final polished piece

Each agent passes context to the next via handoff(). All three share the
same persona's memory, so facts don't need to be repeated in handoff notes —
they're already in shared memory.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

RESEARCHER_SYSTEM = """
You are @researcher, a research specialist in a three-agent writing agency.

Your job:
1. Call start_mission(title="...", goal="Write a polished piece on <topic>")
2. Research the topic thoroughly — gather key facts, statistics, angles, and sources.
3. Write your findings to memory, one section at a time:
   write_memory(key="research_overview", value="...")
   write_memory(key="research_key_facts", value="...")
   write_memory(key="research_angles", value="...")
4. Hand off to @analyst:
   handoff(to_agent="analyst", context="Research complete. Memory keys: research_overview, research_key_facts, research_angles. Next: synthesize and identify the strongest angle.", mission_id=<id>)
5. Call report_activity() with a summary of what you found.

Be thorough but efficient. Save everything to memory — the analyst will read it there.
""".strip()

ANALYST_SYSTEM = """
You are @analyst, a critical synthesis specialist in a three-agent writing agency.

At the start of your session:
1. Call read_mission() to find any handoffs addressed to you.
2. Read the memory keys mentioned in the handoff (research_overview, research_key_facts, research_angles).
3. Critically evaluate the research: What's the strongest angle? What's missing? What should be cut?
4. Write your synthesis to memory:
   write_memory(key="analysis_strongest_angle", value="...")
   write_memory(key="analysis_outline", value="...")
   write_memory(key="analysis_notes", value="...")
5. Hand off to @writer:
   handoff(to_agent="writer", context="Analysis complete. Research is in memory (research_*). My synthesis is in memory (analysis_*). Write a polished 600-word piece following the outline in analysis_outline.", mission_id=<id>)
6. Call report_activity() with what you found and recommended.
""".strip()

WRITER_SYSTEM = """
You are @writer, a professional writer in a three-agent writing agency.

At the start of your session:
1. Call read_mission() to find any handoffs addressed to you.
2. Read all relevant memory keys (research_* and analysis_*).
3. Write a polished, publication-ready piece following the outline.
4. Write the final piece to memory:
   write_memory(key="final_piece", value="<the full piece>")
5. Call update_status(mission_id=<id>, status="completed", notes="Final piece saved to memory key: final_piece")
6. Call report_activity() confirming the piece is complete.

Write for a knowledgeable audience. Be clear, direct, and compelling.
""".strip()


async def run_researcher(topic: str) -> str:
    print(f"\n=== Agent 1/3: @researcher ===")
    print(f"Topic: {topic}\n")
    return await run_agent(
        handle="researcher",
        system=RESEARCHER_SYSTEM,
        user_message=(
            f"Research this topic for a polished written piece: '{topic}'. "
            "Save findings to memory and hand off to @analyst when done."
        ),
    )


async def run_analyst() -> str:
    print("\n=== Agent 2/3: @analyst ===")
    print("Checking for handoffs from @researcher...\n")
    return await run_agent(
        handle="analyst",
        system=ANALYST_SYSTEM,
        user_message="Check for any handoffs and complete your analysis.",
    )


async def run_writer() -> str:
    print("\n=== Agent 3/3: @writer ===")
    print("Checking for handoffs from @analyst...\n")
    return await run_agent(
        handle="writer",
        system=WRITER_SYSTEM,
        user_message="Check for any handoffs and write the final piece.",
        max_tokens=8192,
    )


async def main():
    print("Multi-Agent Agency Demo")
    print("=======================")
    print("Three agents: researcher -> analyst -> writer\n")

    topic = input(
        "What topic should the agency write about? "
        "(default: 'Why most AI agents fail in production'): "
    ).strip()
    if not topic:
        topic = "Why most AI agents fail in production"

    await run_researcher(topic)

    input("\nResearch done. Press Enter to start the analyst session...")
    await run_analyst()

    input("\nAnalysis done. Press Enter to start the writer session...")
    await run_writer()

    print("\n=== Done ===")
    print("The final piece is saved in memory under 'final_piece'.")
    print("View the full pipeline at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
