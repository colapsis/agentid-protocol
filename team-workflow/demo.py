"""
Team workflow using AgentID MCP.

Two agents (@alice and @bob) share one persona's memory and identity.
When @alice writes to memory, @bob reads it — they're two agents, one brain.

Demo:
  @alice summarizes a customer call and writes notes to memory.
  @bob (the follow-up agent) reads those notes and drafts the follow-up email.

This pattern lets you split a workflow across agents (or team members) without
any manual copy-pasting. The shared persona is the connective tissue.

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

ALICE_SYSTEM = """
You are @alice, a customer success manager. After each customer call, you write
structured notes to shared memory so your teammates can follow up without asking you.

After a call:
1. Write a structured summary to memory:
   write_memory(key="call_{date}_{company}", value="<summary>")
   Fields to include: company, contact, key discussion points, commitments made,
   follow-up required (yes/no), urgency (low/medium/high).
2. If follow-up is required, also write:
   write_memory(key="followup_{date}_{company}", value="<what bob needs to do>")
3. Call handoff(to_agent="bob", context="Call notes saved. Check memory key: call_{date}_{company}")
4. Call report_activity() with a one-line summary.

Be factual and specific. Bob will use your notes to write the follow-up email.
""".strip()

BOB_SYSTEM = """
You are @bob, a customer success agent responsible for follow-ups. You work with
@alice — when she finishes a call, you draft the follow-up email.

At the start of your session:
1. Call read_mission() to check for handoffs from @alice.
2. Read the memory keys she mentioned (call_*, followup_*).
3. Draft a professional follow-up email based on what you read.
4. Write the draft to memory:
   write_memory(key="email_draft_{date}_{company}", value="<full email>")
5. Call report_activity() confirming the draft is ready for review.

The email should be warm but professional. Reference specific things from the call.
""".strip()


SAMPLE_CALL_NOTES = """
Just got off a call with Acme Corp (contact: Sarah Chen, Head of Engineering).

Key points:
- They're evaluating us vs. Competitor X for their agent infrastructure
- Main concern: multi-agent coordination — they're building a 5-agent pipeline
- Sarah was impressed by the handoff demo, wants to see a live POC
- Timeline: decision in 3 weeks, board presentation in 4 weeks
- They have a $50k budget approved

Commitments I made:
- Send them a link to the multi-agent showcase by EOD
- Schedule a technical deep-dive with their team next week
- Prepare a POC using their actual use case (document processing pipeline)

Follow-up urgency: high
"""


async def run_alice(call_notes: str) -> str:
    print("\n=== @alice — saving call notes ===\n")
    return await run_agent(
        handle="alice",
        system=ALICE_SYSTEM,
        user_message=(
            f"I just finished a customer call. Here are my notes:\n\n{call_notes}\n\n"
            f"Today's date is {TODAY}. Save the notes to memory and hand off to @bob."
        ),
    )


async def run_bob() -> str:
    print("\n=== @bob — drafting follow-up email ===\n")
    return await run_agent(
        handle="bob",
        system=BOB_SYSTEM,
        user_message="Check for any handoffs from @alice and draft the follow-up email.",
        max_tokens=4096,
    )


async def main():
    print("Team Workflow Demo")
    print("==================")
    print("@alice writes call notes. @bob drafts the follow-up.\n")
    print("Both connect to the same persona — memory is shared.\n")

    use_sample = input("Use sample call notes? (y/n, default y): ").strip().lower()

    if use_sample != "n":
        call_notes = SAMPLE_CALL_NOTES
    else:
        print("\nPaste your call notes (end with a line containing just '---'):")
        lines = []
        while True:
            line = input()
            if line == "---":
                break
            lines.append(line)
        call_notes = "\n".join(lines)

    await run_alice(call_notes)

    input("\n@alice done. Press Enter to start @bob's session...")
    await run_bob()

    print("\n=== Done ===")
    print("The email draft is saved in memory under 'email_draft_*'.")
    print("View both agents' activity at https://agentid.live/app/studio")


if __name__ == "__main__":
    asyncio.run(main())
