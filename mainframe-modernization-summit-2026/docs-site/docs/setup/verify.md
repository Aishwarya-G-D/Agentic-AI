# Verify your install

!!! info "This guide is updated continuously. Make sure to refresh the page often."

Run through this checklist while connected to **GlobalProtect → Brazil South**.

| # | Check | How to verify | Expected |
|---|-------|---------------|----------|
| 1 | GitHub Desktop signed in | Open it, look top-left | Your Kyndryl username appears |
| 2 | VS Code installed | Launch it | Opens without errors |
| 3 | VS Code extensions | Extensions panel → Installed | All required extensions listed |
| 4 | Copilot active | Bottom-right icon | No slash through icon |
| 5 | Copilot Chat works | Cmd/Ctrl+Shift+I → "Hello" | Chat responds |
| 6 | Python | `python --version` (Win) or `python3 --version` (mac) | `>= 3.11` |
| 7 | uv | `uv --version` | Version number |
| 8 | ADK | `orchestrate --version` | First line shows ADK version |
| 9 | ADK env | `orchestrate agents list` | No errors |
| 10 | CPD login | Open [CPD_URL](https://cpd-cpd-instance-2.apps.ocp-prod-2-usa.agenthub.kyndryl.net/) | Home page loads |
| 11 | Challenges repo | Open in VS Code | `00-hello-world/`, `01-sysops-prototype/` visible |
| 12 | Agentic Workspace repo | Open folder in VS Code | `INDEX.md` and structure visible |

If anything fails, jump to the matching [troubleshooting page](../troubleshooting/index.md) — every error in this guide has a seeded entry there.

---

## VPN reminder: Brazil South only

The workshop's Watsonx Orchestrate instance is only reachable through the **Brazil South** GlobalProtect gateway. Any other gateway → CPD URL and ADK calls will fail.

1. Open **GlobalProtect**.
2. Confirm gateway = **Brazil South**.
3. If wrong, disconnect and reconnect with Brazil South selected.
