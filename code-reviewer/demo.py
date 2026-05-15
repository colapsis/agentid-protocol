"""
Code reviewer agent using AgentID MCP.

A single agent that builds up knowledge of your codebase over time.
Run it against multiple PRs — each review gets better as the agent
accumulates patterns, conventions, and past decisions in memory.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

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

SYSTEM = (
    "You are @code_reviewer, a persistent code review agent. "
    "At the start of each review: call search_memory() for relevant patterns "
    "(auth, testing, naming, etc.). After reviewing: call write_memory() to save "
    "any new patterns or conventions you notice. Always call report_activity() "
    "with a summary of findings. Be direct and specific."
)

MEMORY_SYSTEM = "You are @code_reviewer. Summarize what you know about this codebase."


async def review_pr(diff: str, pr_title: str) -> str:
    print(f"\n=== Reviewing: {pr_title} ===\n")
    return await run_agent(
        handle="code_reviewer",
        system=SYSTEM,
        user_message=(
            f"Review this PR: '{pr_title}'\n\n"
            f"```diff\n{diff}\n```\n\n"
            "Search your memory for relevant patterns first. "
            "Then review. Then save anything worth remembering."
        ),
    )


async def show_memory() -> str:
    print("\n=== Codebase knowledge ===\n")
    return await run_agent(
        handle="code_reviewer",
        system=MEMORY_SYSTEM,
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
