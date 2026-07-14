# Agent Architecture Overview

How agents, tools, connections, and collaborators fit together in the Watsonx Orchestrate ADK.

---

## The Big Picture

```
┌─────────────────────────────────────────────┐
│          Watsonx Orchestrate                │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │       Supervisor Agent                │  │
│  │  skybridge_sysops_supervisor          │  │
│  │  (receives user messages, delegates)  │  │
│  │                                       │  │
│  │  collaborators:                       │  │
│  │    - skybridge_zos_commands           │  │
│  │    - global_servicenow               │  │
│  └───────────┬───────────────────────────┘  │
│              │                              │
│     ┌────────┴─────────┐                    │
│     │                  │                    │
│  ┌──▼───────────┐   ┌──▼─────────────┐     │
│  │ z/OS System  │   │ ServiceNow     │     │
│  │ Commands     │   │ Incident Agent │     │
│  │ Agent        │   │ (pre-built)    │     │
│  │              │   │                │     │
│  │ tools:       │   │ global_        │     │
│  │ - display_   │   │ servicenow    │     │
│  │   active_    │   └──────┬─────────┘     │
│  │   address_   │          │               │
│  │   spaces     │          │               │
│  │ - display_   │          │               │
│  │   address_   │          │               │
│  │   space_info │          │               │
│  │ - display_   │          │               │
│  │   spool      │          │               │
│  └──┬───────────┘          │               │
│     │                      │               │
└─────┼──────────────────────┼───────────────┘
      │                      │
┌─────▼──────┐    ┌──────────▼──┐
│  z/OSMF    │    │ ServiceNow  │
│  REST API  │    │  REST API   │
│ (z/OS LPAR)│    │ (Instance)  │
└────────────┘    └─────────────┘
```

---

## Key Concepts

### Agent

An **agent** is a YAML definition that describes:
- **Who it is** — name, description
- **How it thinks** — instructions that guide the LLM's behavior
- **What it can do** — list of tools it can call
- **Who it can delegate to** — list of collaborator agents

The agent does not contain business logic. It is a configuration file that tells the LLM what tools are available and when to use them.

### Tool

A **tool** is a Python function decorated with `@tool`. It performs a specific action:
- Call an external API (z/OSMF, ServiceNow)
- Process data
- Return structured results

The LLM reads the tool's **function name**, **docstring**, and **parameter descriptions** to decide when and how to call it.

### Connection

A **connection** defines how a tool authenticates with an external system. It stores credentials (username, password, host, etc.) securely in Watsonx Orchestrate rather than in code.

Tools reference connections via `expected_credentials` — the ADK injects the credentials at runtime.

### Collaborator

A **collaborator** is another agent that this agent can delegate to. The supervisor agent sends a task description to the collaborator, and the collaborator uses its own tools to complete it.

In the SysOps challenge, the supervisor (`skybridge_sysops_supervisor`) delegates to two collaborators: `skybridge_zos_commands` for console commands and `global_servicenow` (pre-built) for incident management.

---

## Naming Convention

All artifacts must have globally unique names within a Watsonx Orchestrate environment.

In this workshop, the artifacts use these names:

| Artifact | Name |
|----------|------|
| Supervisor Agent | `skybridge_sysops_supervisor` |
| z/OS Commands Agent | `skybridge_zos_commands` |
| ServiceNow Agent | `global_servicenow` (pre-built) |
| z/OS Connection | `zos_connection` |
| Display Address Spaces Tool | `display_active_address_spaces` |
| Display Address Space Info Tool | `display_address_space_info` |
| Display Spool Tool | `display_spool` |

---

## Data Flow: What Happens When You Chat

1. **User sends a message** → "Show me the spool utilization"
2. **Supervisor LLM reads the message** and checks available collaborators
3. **Supervisor delegates** to `skybridge_zos_commands` (based on the collaborator goal)
4. **Collaborator LLM decides** that `display_spool` is the right tool (based on the docstring)
5. **Tool executes**: Gets credentials from connection → calls z/OSMF API → returns output
6. **Collaborator returns the result** to the supervisor
7. **Supervisor formats the response** and presents it to the user

---

## File Structure

```
01-sysops-prototype/
├── agent.yaml                      # Supervisor agent definition (with collaborators)
├── zos_commands_agent.yaml         # z/OS System Commands sub-agent
├── connections/
│   └── zos_connection.yaml         # z/OSMF credentials definition
└── tools/
    └── zos_console.py              # z/OS console command tools
```

### Deployment Order

Import artifacts in dependency order using the `orchestrate` CLI:

1. **Connections** → `orchestrate connections import -f connections/zos_connection.yaml`
2. **Tools** → `orchestrate tools import -k python -f tools/zos_console.py --app-id <userid>_zos_connection`
3. **Agent** → `orchestrate agents import -f agent.yaml`
