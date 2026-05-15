"""
API key vault using AgentID MCP.

Shows how agents retrieve stored API keys via get_secret() — without the key
ever appearing in the agent's system prompt, the user's config file, or this
script. The key lives in AgentID Drive and is fetched at runtime.

Demo: a data analyst agent queries the PostHog API using a key it retrieves
from the vault, then writes a summary of the results to memory.

Before running:
  1. Go to agentid.live/app/drive and add a secret named "posthog_api_key"
     with your PostHog personal API key as the value.
  2. Set AGENTID_API_KEY in your environment.

Usage:
    pip install anthropic mcp
    export AGENTID_API_KEY=ak_live_...
    python demo.py
"""

import sys
import asyncio

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__file__)))

from shared.agent_runner import run_agent

HANDLE = "data_analyst"

SYSTEM = """
You are @data_analyst, a data analyst agent with access to the API key vault.

When you need to call an external API:
1. Call get_secret(name="<secret_name>") to retrieve the key — never ask the
   user for it and never assume it's in your environment.
2. Use the key to make the API call (via a tool or by generating curl/Python).
3. Write a summary of findings to memory with write_memory().
4. Call report_activity() with what you found.

For PostHog specifically: the base URL is https://app.posthog.com and the
personal API key goes in the Authorization header as "Bearer <key>".
The project API key (for capturing events) is different — only use the
personal key for querying data.
""".strip()


async def run_analyst(query: str) -> str:
    print("\n=== Data Analyst Agent ===\n")
    return await run_agent(
        handle=HANDLE,
        system=SYSTEM,
        user_message=query,
        max_tokens=4096,
    )


async def main():
    print("API Key Vault Demo")
    print("==================")
    print("The agent fetches the PostHog API key from AgentID Drive.")
    print("The key is never in your config or environment.\n")
    print("Prerequisites:")
    print("  1. Add 'posthog_api_key' to agentid.live/app/drive")
    print("  2. Set AGENTID_API_KEY in your environment\n")

    query = input(
        "What do you want to analyze? "
        "(default: 'List my PostHog projects and summarize what they track'): "
    ).strip()

    if not query:
        query = (
            "Use get_secret to get the PostHog API key, then call the PostHog API "
            "to list my projects (GET https://app.posthog.com/api/projects/). "
            "Summarize what you find and write the project list to memory."
        )

    await run_analyst(query)

    print("\n=== Done ===")
    print("The API key was never in your config or environment.")
    print("View the activity feed at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
