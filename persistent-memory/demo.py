"""
Persistent memory — hello world for AgentID.

A personal assistant that remembers your name, timezone, and project focus
across sessions. On first run it asks who you are. On every subsequent run
it greets you by name and already knows your context.

This demo shows all three memory primitives:
  write_memory  — store a fact under a named key
  read_memory   — retrieve by exact key
  search_memory — find relevant facts by meaning

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

HANDLE = "personal_assistant"

SYSTEM = """
You are @personal_assistant, a personal AI assistant with persistent memory.

At the start of every session:
1. Call read_memory(key="user_profile") to check if you know the user.
2. If you know them, greet them by name and briefly mention what you remember
   (timezone, current project, etc.).
3. If you don't know them yet, ask for their name, timezone, and what they're
   working on. Then save it with write_memory(key="user_profile", value=...).

During the conversation:
- Use search_memory(query=...) to recall relevant facts before answering.
- Use write_memory to save any new important facts the user tells you.
- Always report_activity() at the end of each session with a short summary.

Be warm, concise, and useful.
""".strip()


async def chat(user_message: str) -> str:
    return await run_agent(
        handle=HANDLE,
        system=SYSTEM,
        user_message=user_message,
        max_tokens=2048,
    )


async def main():
    print("Personal Assistant Demo")
    print("=======================")
    print("This agent remembers you across sessions.\n")
    print("Run it twice to see the difference.\n")

    message = input("You: ").strip()
    if not message:
        message = "Hi! Who are you and what can you do?"

    await chat(message)

    print("\n=== Done ===")
    print("Run this script again — the agent will remember you.")
    print("View memory at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
