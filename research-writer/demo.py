"""
Research → Writer pipeline using AgentID MCP.

Two agents share one identity. Researcher gathers info and hands off.
Writer picks up from the handoff note automatically.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import os
import asyncio
import anthropic
from mcp import ClientSession
from mcp.client.sse import sse_client

API_KEY = os.environ["AGENTID_API_KEY"]
BASE_URL = "https://agentid.live/api/mcp"

client = anthropic.Anthropic()


async def run_agent(handle: str, system: str, user_message: str, max_tokens: int = 4096) -> str:
    """Run one agent session: connects to MCP, runs agentic loop until done."""
    url = f"{BASE_URL}/{handle}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with sse_client(url, headers=headers) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            tools = [
                {
                    "name": t.name,
                    "description": t.description or "",
                    "input_schema": t.inputSchema,
                }
                for t in tools_result.tools
            ]

            messages = [{"role": "user", "content": user_message}]
            final_text = ""

            while True:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=max_tokens,
                    system=system,
                    tools=tools,
                    messages=messages,
                )

                for block in response.content:
                    if hasattr(block, "text"):
                        final_text = block.text
                        print(block.text)

                if response.stop_reason == "end_turn":
                    break

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"  → {block.name}({list(block.input.keys())})")
                        result = await session.call_tool(block.name, block.input)
                        content = result.content[0].text if result.content else ""
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": content,
                        })

                if not tool_results:
                    break

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            return final_text


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
    print(f"\n=== Session 2: @writer_agent ===")
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
    topic = input("What should the researcher investigate? (e.g. 'MCP server patterns in 2025'): ").strip()
    if not topic:
        topic = "MCP server patterns developers are using in 2025"

    await run_researcher(topic)

    input("\nResearch done. Press Enter to start the writer session...")

    await run_writer()

    print("\n=== Done ===")
    print("View the full activity feed at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
