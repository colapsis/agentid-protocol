"""
Daily standup agent using AgentID MCP.

Log work as you go. Generate your standup in the morning.
The agent remembers everything across sessions.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import os
import asyncio
from datetime import date
import anthropic
from mcp import ClientSession
from mcp.client.sse import sse_client

API_KEY = os.environ["AGENTID_API_KEY"]
BASE_URL = "https://agentid.live/api/mcp"
TODAY = date.today().isoformat()

client = anthropic.Anthropic()


async def run_agent(handle: str, system: str, user_message: str, max_tokens: int = 2048) -> str:
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


async def log_work(update: str) -> str:
    print(f"\n=== Logging work update ===\n")
    return await run_agent(
        handle="standup_bot",
        system=(
            "You are @standup_bot. Your job is to remember what the user is working on. "
            f"Today is {TODAY}. When the user tells you what they did or are doing, "
            f"save it to memory using today's date in the key (e.g. '{TODAY}_work', "
            f"'{TODAY}_blockers'). Confirm what you saved. Be brief."
        ),
        user_message=update,
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
        print("Logging a sample update and generating a standup...\n")
        await log_work("Finished the auth refactor, opened PR #42. Reviewed Alice's migration. Still waiting on design review from Bob.")
        await generate_standup()

    print("\n=== Done ===")
    print("View the full activity feed at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
