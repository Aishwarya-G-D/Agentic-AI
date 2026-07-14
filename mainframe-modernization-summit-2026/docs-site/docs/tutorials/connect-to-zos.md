# Connecting to z/OS: Your First Mainframe Tool

In this tutorial you will connect your agent to a real z/OS system running on zD&T, create a tool that executes a console command, and chat with the agent to see live mainframe output.

**Duration**: ~30 minutes

**Prerequisites**: You must have completed the [Hello World](hello-world.md) tutorial and have a working `<userid>_greeter` agent.

---

## What You Will Build

You will extend your greeter agent with a new tool that:

1. Connects to the workshop zD&T system using a **Key-Value connection**
2. Sends the `D A,L` console command to z/OS via the **z/OSMF REST API**
3. Returns the list of active address spaces to the agent

This teaches three new concepts:

1. **Connections** — how agents securely store and retrieve credentials
2. **z/OSMF REST API** — the HTTP interface to z/OS operations
3. **`expected_credentials`** — how a tool declares the connection it needs

!!! info "Reference"
    The ADK connections documentation is available at [Connections Overview](https://developer.watson-orchestrate.ibm.com/connections/overview).

---

## Before You Begin

!!! warning "VPN Required"
    Make sure you are connected to the **GlobalProtect VPN on Brazil South**.

1. Activate your Watsonx Orchestrate environment:

    ```bash
    orchestrate env activate workshop
    ```

2. Confirm you have your zD&T credentials. If not, see [Setup → Mainframe Environment](../setup/mainframe.md).

---

## Step 1: Create the Connection File

A **connection** tells Watsonx Orchestrate how to store and pass credentials to your tools. For z/OS we use a **Key-Value** connection — a simple dictionary of keys and values.

Create a file called `zos_connection.yaml` inside `00-hello-world/`:

```yaml
spec_version: v1
kind: connection
app_id: <userid>_mainframe_connection   # e.g. gcartier_mainframe_connection
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

!!! tip "Replace `<userid>` with your own prefix"
    Use the same prefix from the Hello World tutorial (the part before `@` in your Kyndryl email).

Key fields:

| Field | Purpose |
|-------|---------|
| `app_id` | Unique identifier for this connection |
| `kind: key_value` | Stores arbitrary key-value pairs (host, port, user, password) |
| `type: team` | Shared across the team — anyone with access can use it |
| `sso: false` | No single sign-on; credentials are provided manually |

---

## Step 2: Import the Connection

From the **root of the repository**, run:

```bash
orchestrate connections import -f 00-hello-world/zos_connection.yaml
```

You should see a confirmation that the connection was imported.

---

## Step 3: Set the Connection Credentials

Now populate the connection with the zD&T host details and your personal credentials.

```bash
orchestrate connections set-credentials -a <userid>_mainframe_connection --env draft -e "host=20.110.90.209" -e "port=10443" -e "username=<user>" -e "password=<password>"
```

!!! warning "Replace the placeholders"
    - Replace `<userid>_mainframe_connection` with your actual connection `app_id` (e.g. `gcartier_mainframe_connection`).
    - Replace `<user>` and `<password>` with the zD&T credentials provided by the workshop staff. See [Setup → Mainframe Environment](../setup/mainframe.md).
    - Make sure you have already **reset your initial mainframe password** before using it here.

---

## Step 4: Create the z/OS Console Tool

Create the file `00-hello-world/tools/zos_console.py` with the following content:

```python
"""z/OS Console Command Tool.

Sends a display command to z/OS via the z/OSMF REST Console API
and returns the system output.

Uses dynamic console names to avoid conflicts when multiple
participants share the same z/OSMF instance.
"""

import random
import string

import requests
import urllib3
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run import connections

# Suppress SSL warnings for self-signed certificates (common in z/OSMF)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _generate_console_name() -> str:
    """Generate a random console name (max 8 chars, starting with a letter)."""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"CN{suffix}"


def _run_console_command(command: str, max_retries: int = 5) -> dict:
    """Send a console command to z/OS via the z/OSMF REST Console API."""
    host = connections.key_value("<userid>_mainframe_connection")["host"]
    port = connections.key_value("<userid>_mainframe_connection")["port"]
    credentials = {
        "user": connections.key_value("<userid>_mainframe_connection")["username"],
        "password": connections.key_value("<userid>_mainframe_connection")["password"],
    }
    payload = {"cmd": command, "sol-key": None}
    headers = {
        "Content-Type": "application/json",
        "X-CSRF-ZOSMF-HEADER": "",
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()

    last_error = None
    for _ in range(max_retries):
        console_name = _generate_console_name()
        url = f"https://{host}:{port}/zosmf/restconsoles/consoles/{console_name}"
        try:
            response = session.request(
                method="PUT",
                url=url,
                json=payload,
                auth=(credentials["user"], credentials["password"]),
                verify=False,
                timeout=90,
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            last_error = e
            continue

    raise RuntimeError(
        f"Unable to find an available console after {max_retries} attempts: {last_error}"
    )


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="<userid>_mainframe_connection",  # (1)!
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def <userid>_display_active_jobs() -> dict:  # (2)!
    """Display all active address spaces on the z/OS system.

    Runs the z/OS command D A,L to show all active address spaces,
    including started tasks, batch jobs, and system tasks.
    Use this when the user asks about active jobs, running tasks,
    or wants a general system status overview.

    Returns:
        dict: The z/OSMF response with active address spaces.
    """
    return _run_console_command("D A,L")
```

1. Replace `<userid>_mainframe_connection` with your actual connection `app_id`.
2. Replace `<userid>_display_active_jobs` with your prefixed function name (e.g. `gcartier_display_active_jobs`).

!!! tip "Replace `<userid>` in both places"
    The `app_id` in `expected_credentials` must match the `app_id` in your connection YAML. The function name must use your prefix.

Key concepts:

| Concept | What It Does |
|---------|-------------|
| `expected_credentials` | Declares which connection this tool needs — Orchestrate injects the credentials at runtime |
| `ConnectionType.KEY_VALUE` | Tells Orchestrate this is a key-value connection |
| `connections.key_value("<userid>_mainframe_connection")["host"]` | Retrieves a specific value from the connected credential store |
| `requests.Session()` | Creates a reusable HTTP session for the z/OSMF API call |
| `response.json()` | Returns the raw z/OSMF response as a dictionary |

---

## Step 5: Import the Tool

From the **root of the repository**, run:

```bash
orchestrate tools import -k python -f 00-hello-world/tools/zos_console.py --app-id <userid>_mainframe_connection
```

!!! tip "Replace `<userid>` with your own prefix"
    For example: `--app-id gcartier_mainframe_connection`

!!! note
    All `orchestrate` commands must be run from the root of the repo.

---

## Step 6: Update Your Agent

Edit your `00-hello-world/greeter.yaml` to add the new tool and update the instructions:

```yaml
spec_version: v1
kind: native
name: <userid>_greeter
description: An agent that can greet you and check z/OS system status.
instructions: |
  When the user types "Greeting", run the greeting tool.
  When the user asks about active jobs or system status, run the display active jobs tool.
llm: virtual-model/openai/ibm-granite/granite-4.1-8b
style: default
collaborators: []
tools:
  - <userid>_greeting
  - <userid>_display_active_jobs
```

!!! tip "Replace `<userid>` with your own prefix"

Then re-import the agent:

```bash
orchestrate agents import -f 00-hello-world/greeter.yaml
```

!!! failure "Getting a 500 Internal Server Error?"
    If the import fails with `ClientAPIException(status_code=500)`, see [Troubleshooting → 500 Internal Server Error](../troubleshooting/index.md#500-internal-server-error-clientapiexceptionstatus_code500).

---

## Step 7: Test It

Open the Watsonx Orchestrate chat and try:

- **"Show me all active address spaces"** — the agent should call your `display_active_jobs` tool and return live z/OS output.
- **"Greeting"** — should still work as before.

If the tool returns an error, double-check:

1. Your connection credentials are correct (`orchestrate connections set-credentials ...`)
2. You have reset your mainframe password (see [Mainframe Environment](../setup/mainframe.md))
3. You are connected to the **Brazil South** VPN

---

## What You Learned

| Concept | What It Means |
|---------|--------------|
| Connection YAML | Declares an external dependency with its authentication type |
| `set-credentials` | Populates a connection with actual credentials |
| `expected_credentials` | Links a tool to a connection so credentials are injected at runtime |
| z/OSMF REST Console API | The HTTP interface for sending operator commands to z/OS |

---

## Reference

- [ADK Connections Overview](https://developer.watson-orchestrate.ibm.com/connections/overview)
- [ADK Creating Connections](https://developer.watson-orchestrate.ibm.com/connections/build_connections)
- [z/OSMF Console API Reference](../reference/zosmf-console-api.md)

---

## Next Step

You now have an agent that can talk to a live mainframe. In the next challenge, move on to **Challenge 1: SysOps Foundation Prototype** in `01-sysops-prototype/` to build a full operational agent with multiple tools and ServiceNow integration.
