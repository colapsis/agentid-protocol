# Contributing

Contributions are welcome. The bar is simple: the example must run, demonstrate something real, and be easy to follow.

## What makes a good example

- **One clear concept** — each example teaches one thing well
- **Runnable in under 2 minutes** — no complex setup, no external services beyond AgentID
- **Real code** — no placeholder comments or TODO stubs
- **Complete** — `demo.py`, `README.md`, and `claude_desktop_config.json`

## Adding an example

1. Fork the repo and create a branch: `git checkout -b example/my-thing`

2. Create a directory under the repo root:

```
my-example/
  demo.py                   # runnable Python script
  README.md                 # walkthrough with expected output
  claude_desktop_config.json  # MCP config for Claude Desktop
```

3. Import from `shared/agent_runner.py` — don't copy the MCP loop:

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from shared.agent_runner import run_agent
```

4. Write the README in the same style as existing examples:
   - How it works (with a short ASCII flow)
   - Setup (numbered steps)
   - Python demo section
   - What you'll see in the studio

5. Test it end-to-end with a real AgentID account before opening a PR.

6. Add a row to the table in the root `README.md`.

7. Open a pull request. Include the agent handle(s) you used for testing.

## Improving existing examples

Open an issue first if the change is large. For small fixes (typos, clearer code, updated imports), a PR is fine without an issue.

## Code style

- Python 3.10+
- No external dependencies beyond `anthropic` and `mcp`
- `asyncio.run(main())` at the bottom of every `demo.py`
- Descriptive variable names, no abbreviations in public interfaces

## License

By contributing, you agree your code is released under the MIT license.
