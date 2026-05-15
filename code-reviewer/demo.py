"""
Code reviewer agent using AgentID MCP.

One agent that builds up knowledge of your codebase over time.
Run it against multiple PRs and watch the reviews get better.

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

SAMPLE_DIFF = """
diff --git a/src/auth/login.py b/src/auth/login.py
index a3b4c5d..e6f7g8h 100644
--- a/src/auth/login.py
+++ b/src/auth/login.py
@@ -12,6 +12,18 @@ from .models import User
+def login(username: str, password: str):
+    user = User.query.filter_by(username=username).first()
+    if user and user.password == password:
+        token = jwt.encode({"user_id": user.id}, SECRET_KEY)
+        return {"token": token}
+    return None
"""


async def run_agent(handle: str, system: str, user_message: str, max_tokens: int = 4096) -> str:
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


async def review_pr(diff: str, pr_title: str) -> str:
    print(f"\n=== Reviewing: {pr_title} ===\n")
    return await run_agent(
        handle="code_reviewer",
        system=(
            "You are @code_reviewer, a persistent code review agent. "
            "At the start of each review: search_memory() for relevant patterns "
            "(auth, testing, naming, etc). After reviewing: write_memory() to save "
            "any new patterns or conventions you notice. Always report_activity() "
            "with a summary of findings. Be direct and specific."
        ),
        user_message=(
            f"Review this PR: '{pr_title}'\n\n"
            f"```diff\n{diff}\n```\n\n"
            "Search your memory for relevant patterns first. "
            "Then review. Then save anything worth remembering."
        ),
    )


async def show_memory() -> str:
    print(f"\n=== Codebase knowledge ===\n")
    return await run_agent(
        handle="code_reviewer",
        system="You are @code_reviewer. Summarize what you know about this codebase.",
        user_message="What do you know about this codebase so far? Search your memory and summarize.",
        max_tokens=2048,
    )


async def main():
    print("Code Reviewer Demo")
    print("==================")
    print("This agent builds up codebase knowledge over time.\n")

    use_sample = input("Use sample diff? (y/n, default y): ").strip().lower()

    if use_sample != "n":
        diff = SAMPLE_DIFF
        title = "Add login endpoint"
    else:
        title = input("PR title: ").strip()
        print("Paste your diff (end with a line containing just '---'):")
        lines = []
        while True:
            line = input()
            if line == "---":
                break
            lines.append(line)
        diff = "\n".join(lines)

    await review_pr(diff, title)

    show = input("\nShow what the agent has learned? (y/n, default y): ").strip().lower()
    if show != "n":
        await show_memory()

    print("\n=== Done ===")
    print("View the full activity feed at https://agentid.live/app/studio")
    print("Run again with a new diff to see the agent apply what it learned.")


if __name__ == "__main__":
    asyncio.run(main())
