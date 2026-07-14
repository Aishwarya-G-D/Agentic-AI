# Challenge 2 — SysOps Foundation Prototype

**Total working time: 1 hour 10 minutes** plus 30-minute walkthrough.

---

## Narrative Context

The readiness assessment is complete. SkyBridge is cleared for a proof of concept on the test LPAR. Sarah (CTO) has greenlit a prototype. James (VP Infra) has one condition: *"Show me something that works on our test LPAR first."*

The Kyndryl team (workshop participants) must now build a working prototype of the z/OS SysOps Foundation assistant using IBM Watsonx Orchestrate ADK. This prototype is the evidence that Kyndryl can run operations better than SkyBridge's internal team. It's the pitch to win the delivery contract.

---

## Naming Convention — Read This First

!!! info "Shared Environment"
    We are working in a **shared environment**. If everyone creates agents, tools, and connections with the same name, you will overwrite each other's work.

To avoid this, **prefix every agent name, tool name, and connection name with your user ID** (the part before `@` in your Kyndryl email).

| Your email | Prefix | Supervisor agent | Sub-agent | Connection |
|---|---|---|---|---|
| `gcartier@kyndryl.com` | `gcartier` | `gcartier_sysops_supervisor` | `gcartier_zos_commands` | `gcartier_zos_connection` |
| `jsmith@kyndryl.com` | `jsmith` | `jsmith_sysops_supervisor` | `jsmith_zos_commands` | `jsmith_zos_connection` |

Use this prefix consistently throughout the entire challenge — in YAML files, Python tool functions, and CLI commands.

---

## Objective

Build a **simplified but functional** SysOps Foundation assistant that connects to SkyBridge's test LPAR and demonstrates core z/OS operational capabilities.

**Expected Skill Level**: Level 2 — Demonstrates GitHub, VS Code, and development tool proficiency. Applies foundational Python code reading skills. Understands existing agent code structure, configuration, and dependencies.

**Activity Type**: Guided hands-on development using IBM Watsonx Orchestrate ADK.

---

## Scope Reduction: From Full SysOps to Workshop-Ready

The full SysOps Foundation includes 6+ agents and collaborators. That is too much for 1.5 hours. The workshop prototype targets a **simplified two-agent architecture**.

### Simplified Agent Architecture

```
<userid>_sysops_supervisor
├── <userid>_zos_commands (JES/Console display commands)
└── global_servicenow (create and search incidents — pre-built)
```

### Included Capabilities (must-have)

| Capability | Agent | What It Does |
|-----------|-------|-------------|
| Display active address spaces | System Commands Agent | Runs `D A,L` or equivalent display command via z/OSMF |
| Check address space info | System Commands Agent | Runs `D A,jobname` to show address space information |
| Display spool usage | System Commands Agent | Runs JES2 `$D SPOOL` to show spool utilization |
| Create a ServiceNow incident | ServiceNow Agent | Opens a new incident with system-generated data |

### Excluded from Workshop Scope (for time reasons)

| Capability | Why Excluded |
|-----------|-------------|
| z/OSMF Jobs API integration | Requires additional REST API configuration and auth setup |
| Health Check collaborator | Complex multi-step analysis; too much for 1.5 hours |
| Routine Checks collaborator | Requires OMVS, VTAM, TCP/IP checks; scope too broad |
| zRAG agent | Requires knowledge base configuration |
| Job purge capability | Write operation; safety concerns in workshop environment |

### Stretch Goals (for fast teams)

Teams that finish the core prototype early can attempt:

1. Add a basic health check function (spool utilization threshold alert)
2. Add z/OSMF Jobs API listing (read-only)
3. Integrate system data into ServiceNow incident descriptions automatically

---

## What You Will Build

The challenge uses standard ADK artifacts — plain YAML and Python files. You edit the files directly, then import them into Watsonx Orchestrate with CLI commands.

### Key Files

All files are in the `01-sysops-prototype/` directory:

| File | Purpose |
|------|---------|
| `agent.yaml` | Supervisor agent definition — name it `<userid>_sysops_supervisor` |
| `zos_commands_agent.yaml` | z/OS System Commands sub-agent — name it `<userid>_zos_commands` |
| `tools/zos_console.py` | z/OS console command tools — prefix all function names with `<userid>_` |
| `connections/zos_connection.yaml` | z/OSMF connection — name it `<userid>_zos_connection` |

!!! info "ServiceNow Agent"
    The ServiceNow agent is **pre-built** and already deployed in the workshop environment. Agent name: `global_servicenow`. You do not need to build or import it — just reference it as a collaborator.

---

## Step-by-Step Instructions

### Step 1: Understand the Agent Architecture (10 minutes)

Read through the files to understand how the pieces connect:

1. **`agent.yaml`** — The supervisor agent definition. Look at:
      - The `collaborators` list — this tells the supervisor who it can delegate to
      - The `instructions` field — this tells the LLM how to behave
      - Notice: the supervisor has **no tools of its own** — it delegates to collaborators

2. **`zos_commands_agent.yaml`** — The z/OS sub-agent. Look at:
      - The `tools` list — these are the tools this agent can call
      - The `instructions` — display-only, no modify operations

3. **`tools/zos_console.py`** — The z/OS console tools. Look at:
      - The `@tool` decorator and `expected_credentials` — how tools authenticate
      - The function signature and docstring — the LLM reads these
      - The z/OSMF REST API call pattern — `requests.put()` to the console endpoint

4. **`connections/zos_connection.yaml`** — Defines how the tool gets z/OSMF credentials

See `reference/agent-architecture.md` for a visual overview.

---

### Step 2: Configure the Supervisor Agent (15 minutes)

Open `agent.yaml`. This is your supervisor agent definition. Review and understand the structure:

- **Name**: `<userid>_sysops_supervisor` (e.g. `gcartier_sysops_supervisor`)
- **Description**: A z/OS system operator assistant for the SkyBridge Rewards test environment
- **Collaborators**: References to the two sub-agents (using your prefixed names)
- **Collaborator goals**: Define what each sub-agent is responsible for
- **Guardrails**: Display-only commands. No modify operations. No production LPAR access.

The supervisor YAML structure:

```yaml
name: <userid>_sysops_supervisor          # e.g. gcartier_sysops_supervisor
description: >
  SysOps Foundation assistant for SkyBridge Rewards.
  Monitors z/OS system health, runs display commands,
  and manages ServiceNow incidents for the SKBTEST1 LPAR.
collaborators:
  - agent: <userid>_zos_commands           # e.g. gcartier_zos_commands
    goal: Run JES and console display commands to show live system status
  - agent: global_servicenow
    goal: Search, create, and update ServiceNow incidents
```

!!! tip "Key Concept: Supervisor Pattern"
    The supervisor agent does not call tools directly. It receives user messages and decides which collaborator should handle the request. Each collaborator has its own tools and instructions.

---

### Step 3: Build the z/OS System Commands Agent (30 minutes)

This is the core development task. Open `tools/zos_console.py`. The file contains a working implementation for `<userid>_display_active_address_spaces` and scaffolding for the remaining tools.

**Your task**: 

1. **Prefix all function names** with your user ID (e.g. `gcartier_display_active_address_spaces`)
2. **Update the connection `app_id`** references to use your prefixed connection name (e.g. `gcartier_zos_connection`)
3. **Complete the remaining tool functions** by replacing the `pass` with the correct `_run_console_command()` call. Each tool follows the same pattern as the first one.

#### Tools to Complete

| Function | Command | What to Look For in Response |
|----------|---------|------------------------------|
| `<userid>_display_address_space_info` | `D A,{jobname}` | Address space name, status, ASID |
| `<userid>_display_spool` | `$D SPOOL` | Spool percent full, track counts |

!!! tip "Hint"
    All three tools use the same z/OSMF REST API endpoint and the same call pattern. The only differences are the command string and how you describe the tool in the docstring.

Each tool follows this pattern:

1. Authenticate to z/OSMF using provided credentials (RACF user ID)
2. Submit a console command via the z/OSMF REST console API
3. Parse the response
4. Return structured output to the supervisor

See `reference/zosmf-console-api.md` for the API details.

---

### Step 4: Import and Deploy (15 minutes)

#### Import the Connection

!!! tip "Reuse your existing connection"
    If you completed the [Connect to z/OS tutorial](../tutorials/connect-to-zos.md), you already have a working connection called `<userid>_mainframe_connection`. You can **reuse it** instead of creating a new one — just update the `app_id` references in `connections/zos_connection.yaml` and `tools/zos_console.py` to match your existing connection name (e.g. `gcartier_mainframe_connection`). If you do this, skip the import and credential steps below.

If you need a new connection, import it:

```bash
orchestrate connections import -f connections/zos_connection.yaml
```

Then configure the connection credentials:

```bash
orchestrate connections set-credentials -a <userid>_zos_connection --env draft -e "host=<host>" -e "port=<port>" -e "username=<user>" -e "password=<password>"
```

!!! warning "Replace the placeholders"
    - Replace `<userid>_zos_connection` with your actual connection `app_id` (e.g. `gcartier_zos_connection`).
    - Replace `<host>`, `<port>`, `<user>`, and `<password>` with the values provided by your facilitator.

#### Import Tools

```bash
orchestrate tools import -k python -f tools/zos_console.py --app-id <userid>_zos_connection
```

!!! warning "The `--app-id` flag is required"
    When a tool uses a connection (via `expected_credentials`), you **must** pass `--app-id` with the connection's `app_id` during import. Without it, the platform won't link the tool to its credentials and API calls will fail at runtime.

#### Import the Agents

```bash
orchestrate agents import -f zos_commands_agent.yaml
orchestrate agents import -f agent.yaml
```

!!! warning "Import Order Matters"
    Import the z/OS commands agent **before** the supervisor. The supervisor references `<userid>_zos_commands` as a collaborator — it must exist first.

---

## Deliverable

A **working SysOps Foundation prototype** that can:

- [ ] Connect to SkyBridge's test LPAR via z/OSMF REST API
- [ ] Execute at least 3 display commands and return results
- [ ] Create a ServiceNow incident from the assistant interface
- [ ] Demonstrate supervisor-to-collaborator delegation

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| z/OSMF returns 401 | Check username/password in the connection credentials |
| z/OSMF returns 403 | User ID may lack RACF authorization for console commands |
| Agent can't find collaborator | Import the collaborator agent before the supervisor |
| Supervisor doesn't delegate | Check that collaborator names in `agent.yaml` match exactly |
