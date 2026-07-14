# Group 2 SysOps Supervisor Implementation Plan

## Purpose
Deliver a production-style workshop prototype centered on `group_2_sysops_supervisor` that can safely monitor z/OS using display-only commands, delegate correctly, and provide consistent incident-oriented operational guidance.

## Target Architecture
- Supervisor agent: `group_2_sysops_supervisor`
- Specialist collaborator: `group_2_zos_commands`
- Shared connection app id: `group_2_mainframe_connection`
- Python tool module: `01-sysops-prototype/tools/zos_console.py`

## Scope
### In Scope
- Standardize all names to `group_2_` prefix.
- Use one shared z/OSMF connection for all Group 2 console tools.
- Implement and import display-only z/OS command tools.
- Configure routing rules in supervisor and specialist agent instructions.
- Validate import and run smoke-test prompts.

### Out of Scope
- Write or modify z/OS state (cancel, purge, start, etc.).
- Non-workshop production hardening (SIEM integration, RBAC redesign, full audit pipeline).
- Automated CI/CD deployment pipeline.

## Implementation Workstreams
### 1. Naming and Configuration Consolidation
- Ensure all tool functions use `group_2_` prefix.
- Ensure YAML `name` fields use `group_2_` prefix.
- Ensure connection app id is exactly `group_2_mainframe_connection` in:
  - `01-sysops-prototype/connections/zos_connection.yaml`
  - `01-sysops-prototype/tools/zos_console.py` (`expected_credentials` and `connections.key_value`)

### 2. Tooling Layer (z/OS Commands)
Implement or confirm these tools in `01-sysops-prototype/tools/zos_console.py`:
- `group_2_display_active_jobs` -> `D A,L`
- `group_2_display_address_space` -> `D A,jobname`
- `group_2_display_spool_utilization` -> `$D SPOOL`
- `group_2_display_wtor_messages` -> `D R,L`
- `group_2_display_iplinfo` -> `D IPLINFO`
- `group_2_display_online_dasd` -> `D U,DASD,ONLINE`

Design requirements:
- All tools must be decorated with `@tool`.
- All tools must use identical connection credential binding.
- `group_2_display_address_space` must validate non-empty `jobname`.
- Helper function must retry on transient API failures and return clear runtime error context.

### 3. Specialist Agent Assembly
File: `01-sysops-prototype/zos_commands_agent.yaml`
- Agent name: `group_2_zos_commands`
- List all six group tools under `tools`.
- Keep constraints display-only.
- Keep collaborators empty (`[]`).

### 4. Supervisor Agent Assembly
File: `01-sysops-prototype/agent.yaml`
- Agent name: `group_2_sysops_supervisor`
- Collaborator list includes `group_2_zos_commands`.
- Routing rules explicitly delegate:
  - System status and active jobs -> `group_2_zos_commands`
  - Specific address space checks -> `group_2_zos_commands`
  - Spool checks -> `group_2_zos_commands`
  - WTOR checks -> `group_2_zos_commands`
  - IPL info -> `group_2_zos_commands`
  - DASD online status -> `group_2_zos_commands`
- Constraint section enforces display-only command policy.

## Import and Deployment Sequence
Run from repository root in this order:
1. `uv run orchestrate connections import -f 01-sysops-prototype/connections/zos_connection.yaml`
2. `uv run orchestrate tools import -k python -f 01-sysops-prototype/tools/zos_console.py --app-id group_2_mainframe_connection`
3. `uv run orchestrate agents import -f 01-sysops-prototype/zos_commands_agent.yaml`
4. `uv run orchestrate agents import -f 01-sysops-prototype/agent.yaml`

## Verification Plan
### A. Import Verification
- Connection import succeeds with draft and live configurations.
- Six tools import successfully with no missing app-id errors.
- `group_2_zos_commands` imports before supervisor.
- `group_2_sysops_supervisor` imports with collaborator resolution success.

### B. Functional Smoke Tests
Run these prompts against `group_2_sysops_supervisor`:
- Show active jobs.
- Show details for address space JES2.
- Show spool utilization.
- Show outstanding WTOR messages.
- Show IPL information.
- Show online DASD devices.

Expected behavior:
- Supervisor delegates to `group_2_zos_commands`.
- Responses include command output context.
- No write operation is suggested or executed.

### C. Failure Handling Checks
- If tool call fails, response should explain likely cause and next action.
- Validate error text is informative for HTTP failures.

## Operational Guardrails
- Never run state-changing z/OS commands.
- Treat all outputs as operational signals; human validation remains required.
- If spool utilization appears high, recommend incident creation workflow.

## Risks and Mitigations
- Tool import fails due to missing app id.
  - Mitigation: Always pass `--app-id group_2_mainframe_connection` for tool import.
- Agent import fails due to unresolved tool names.
  - Mitigation: Ensure exact string match between YAML `tools` names and Python function names.
- z/OSMF API returns 5xx during peak usage.
  - Mitigation: Retry logic in tool helper, stable+fallback console naming, rerun after brief delay.
- Collaborator not found on supervisor import.
  - Mitigation: Import specialist agent before supervisor every time.

## Delivery Checklist
- [ ] Connection YAML finalized with group app id.
- [ ] Tool module finalized with six prefixed tools.
- [ ] Specialist agent YAML finalized.
- [ ] Supervisor agent YAML finalized.
- [ ] Imports completed in correct order.
- [ ] Smoke tests executed and documented.
- [ ] Group demo script prepared.

## Demo Script (5 Minutes)
1. Introduce architecture and safety posture.
2. Ask supervisor for active jobs.
3. Ask for spool utilization and explain threshold interpretation.
4. Ask for WTOR messages and IPL info.
5. Ask for online DASD status.
6. Summarize why this is integration-ready for next iteration.

## Next Iteration Suggestions
- Add a consolidated health-summary tool that calls multiple display commands and returns one structured report.
- Add optional incident payload formatter for downstream ticketing integration.
- Add response templates for operator-facing status summaries.
