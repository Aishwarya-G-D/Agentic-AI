# ADK Quick Reference

Common commands for the IBM Watsonx Orchestrate ADK (Agent Development Kit).

---

## Environment Management

```bash
# Add a new environment
orchestrate env add <name> --url <instance_url> --api-key <api_key>

# List environments
orchestrate env list

# Activate an environment
orchestrate env activate <name>

# Check active environment
orchestrate env active
```

---

## Connections

```bash
# Import a connection definition
orchestrate connections import -f <connection.yml>

# List connections
orchestrate connections list
```

After importing a connection, configure its credentials in the Watsonx Orchestrate UI (Settings → Connections).

---

## Tools

```bash
# Import a Python tool (no connection)
orchestrate tools import -k python -f <tool.py>

# Import a Python tool that uses a connection
orchestrate tools import -k python -f <tool.py> --app-id <connection_app_id>

# List tools
orchestrate tools list
```

---

## Agents

```bash
# Import an agent definition
orchestrate agents import -f <agent.yml>

# List agents
orchestrate agents list
```

---

## Chat

```bash
# Start an interactive chat session
orchestrate chat start

# Start chat with a specific agent
orchestrate chat start --agent <agent_name>
```

---

## Deployment Order

Always import in dependency order:

1. **Connections** — tools need these to authenticate
2. **Tools** — agents need these to do work
3. **Agents** — wire everything together

---

## Agent YAML Structure

```yaml
spec_version: v1
kind: native
name: my_agent                    # Unique name (must be valid Python identifier)
description: |                    # What the agent does
  Description text here.
instructions: >                  # Behavioral rules for the LLM
  Instructions text here.
llm: watsonx/meta-llama/llama-3-3-70b-instruct   # Model to use
style: react                     # Reasoning style
collaborators:                   # Other agents this agent can delegate to
  - other_agent_name
tools:                           # Tools this agent can call
  - my_tool_name
```

---

## Tool Python Structure

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.run import connections

@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="my_connection",           # Must match a connection app_id
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def my_tool(param1: str) -> str:
    """Tool description — the LLM reads this to decide when to call it.

    Args:
        param1: Description of the parameter.

    Returns:
        A string result.
    """
    username = connections.key_value("username")
    password = connections.key_value("password")
    # ... implementation ...
    return "result"
```

---

## Connection YAML Structure

```yaml
spec_version: v1
kind: connection
app_id: my_connection             # Referenced by tools via expected_credentials
environments:
    draft:
        kind: key_value
        type: team
        sso: false
    live:
        kind: key_value
        type: team
        sso: false
```

---

## Useful Links

- ADK Documentation: https://developer.watson-orchestrate.ibm.com
- Tutorials: https://developer.watson-orchestrate.ibm.com/tutorials/tutorial_1_hello_world
- Installing the ADK: https://developer.watson-orchestrate.ibm.com/getting_started/installing
