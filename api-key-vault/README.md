# API Key Vault

Shows how agents retrieve API keys at runtime via `get_secret()` — without the key ever appearing in the agent's system prompt, the user's config file, or any environment variable on the agent's machine.

Keys are stored in AgentID Drive and fetched only when needed.

## How it works

```
Traditional approach (insecure)
  POSTHOG_API_KEY=sk_live_... python agent.py   # key in shell history
  system="...your key is sk_live_..."            # key in prompt logs

AgentID approach
  -> get_secret(name="posthog_api_key")   # fetched from vault at runtime
  -> uses key to call PostHog API
  -> key never touches your config, logs, or this repo
```

The agent knows the **name** of the secret. The value lives in AgentID Drive, accessible only to agents connected to that persona.

## Setup

### 1. Store the secret

Go to [agentid.live/app/drive](https://agentid.live/app/drive) and add a secret:
- Name: `posthog_api_key`
- Value: your PostHog personal API key

Any secret name works — the agent references it by name in `get_secret()`.

### 2. Create the agent

Go to [agentid.live/app/agents](https://agentid.live/app/agents) and create `data-analyst`, attached to the same persona where you stored the secret.

### 3. Add to Claude Desktop

```json
{
  "mcpServers": {
    "analyst": {
      "url": "https://agentid.live/api/mcp/data-analyst",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

### 4. Use it

Select the `analyst` server in Claude Desktop and say:

> "Use get_secret to get the PostHog API key, then list my projects."

The agent fetches the key, calls the API, and writes a summary to memory — all without you ever seeing the key.

## Python demo

```bash
pip install anthropic mcp
export AGENTID_API_KEY=ak_live_...
python demo.py
```

Before running: add `posthog_api_key` to [agentid.live/app/drive](https://agentid.live/app/drive).

## What you'll see

The agent calls `get_secret("posthog_api_key")`, uses the returned value to call the PostHog API, and writes results to memory. The secret value appears only inside the agent's tool call — never in your terminal, logs, or config.

Open [agentid.live/app/studio](https://agentid.live/app/studio) to see the full trace.

## Using other APIs

The pattern works for any API key:

```python
# In your system prompt:
"Use get_secret(name='stripe_api_key') to authenticate with Stripe."
"Use get_secret(name='github_token') for GitHub API calls."
"Use get_secret(name='openai_key') if you need to call OpenAI."
```

Store the secret in AgentID Drive once. All agents on that persona can use it.
