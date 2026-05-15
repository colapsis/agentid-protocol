"""
shared/agent_runner.py — reusable async agent loop for AgentID examples.

Every demo in this repo uses this helper. It handles:
- Connecting to the AgentID MCP server for a given agent handle
- Running the Anthropic agentic loop until stop_reason == "end_turn"
- Printing text output and tool calls as they happen

Usage:
    from shared.agent_runner import run_agent

    result = await run_agent(
        handle="my_agent",
        system="You are @my_agent. ...",
        user_message="Do something useful.",
    )
"""

import os
import sys
import anthropic
from mcp import ClientSession
from mcp.client.sse import sse_client

BASE_URL = "https://agentid.live/api/mcp"
MODEL = "claude-sonnet-4-6"

_anthropic_client = anthropic.Anthropic()


def _get_api_key() -> str:
    key = os.environ.get("AGENTID_API_KEY", "")
    if not key:
        print("Error: AGENTID_API_KEY environment variable is not set.", file=sys.stderr)
        print("Get your key at https://agentid.live/app/developers", file=sys.stderr)
        sys.exit(1)
    return key


async def run_agent(
    handle: str,
    system: str,
    user_message: str,
    *,
    verbose: bool = True,
    max_tokens: int = 4096,
) -> str:
    """
    Run one agent session against the AgentID MCP server.

    Connects to https://agentid.live/api/mcp/{handle}, authenticates with
    AGENTID_API_KEY, and drives the Anthropic tool-use loop until the agent
    finishes. Returns the final text response.

    Args:
        handle:       Agent handle (the part after /api/mcp/).
        system:       System prompt for this agent.
        user_message: The user turn that kicks off the session.
        verbose:      If True, print text output and tool calls as they happen.
        max_tokens:   Max tokens for each Anthropic API call.

    Returns:
        The agent's final text response as a string.
    """
    api_key = _get_api_key()
    url = f"{BASE_URL}/{handle}"
    headers = {"Authorization": f"Bearer {api_key}"}

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
                response = _anthropic_client.messages.create(
                    model=MODEL,
                    max_tokens=max_tokens,
                    system=system,
                    tools=tools,
                    messages=messages,
                )

                for block in response.content:
                    if hasattr(block, "text"):
                        final_text = block.text
                        if verbose:
                            print(block.text)

                if response.stop_reason == "end_turn":
                    break

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        if verbose:
                            print(f"  -> {block.name}({list(block.input.keys())})")
                        result = await session.call_tool(block.name, block.input)
                        content = result.content[0].text if result.content else ""
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": content,
                            }
                        )

                if not tool_results:
                    break

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

    return final_text
