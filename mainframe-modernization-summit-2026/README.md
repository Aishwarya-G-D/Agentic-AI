# Watsonx Assistant for Z — Workshop Challenges

Hands-on challenge repository for the **Mainframe Modernization Summit 2026 — Specialist Workshop**.

Participants use this repository to complete the Watsonx-related challenges: the Hello World tutorial (Day 1) and the SysOps Foundation prototype (Day 2).

## Repository Structure

```
wxa4z-challenges/
├── README.md                        # You are here
├── 00-hello-world/                  # Day 1: Hello World tutorial
│   └── README.md                    # Step-by-step guide (you create the files)
├── 01-sysops-prototype/             # Day 2: SysOps Foundation challenge
│   ├── README.md                    # Challenge instructions
│   ├── agent.yaml                   # Supervisor agent definition
│   ├── connections/
│   │   ├── zos_connection.yaml      # z/OS connection definition

│   └── tools/
│       ├── zos_console.py           # z/OS console commands (has TODOs)

├── reference/
│   ├── adk-quickref.md              # ADK command reference
│   ├── zosmf-console-api.md         # z/OSMF REST console API reference
│   └── agent-architecture.md        # Agent architecture overview
├── .env.example                     # Environment variable template
├── .gitignore
├── .python-version
└── pyproject.toml
```

## Prerequisites

Before starting the challenges, make sure you have:

1. **Python 3.11+** installed (`python --version`)
2. **uv** package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
3. **Git** (`git --version`)
4. **VS Code** with recommended extensions (Python, Pylance, YAML)
5. **IBM Watsonx Orchestrate ADK** installed and authenticated

## Getting Started

### 1. Clone this repository

```bash
git clone <REPO_URL>
cd wxa4z-challenges
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure your ADK environment

```bash
cp .env.example .env
# Edit .env with your Watsonx Orchestrate credentials
```

### 4. Activate your orchestrate environment

```bash
orchestrate env add <env_name> --url <instance_url> --api-key <api_key>
orchestrate env activate <env_name>
```

### 5. Start with the Hello World tutorial

```bash
cd 00-hello-world
```

Follow the instructions in `00-hello-world/README.md`.

## Challenge Progression

| Challenge | Day | Duration | Focus |
|-----------|-----|----------|-------|
| Hello World | Day 1 | 1.5 hours | ADK basics — create, import, and chat with your first agent |
| SysOps Prototype | Day 2 | 1.5 hours | Build a z/OS operations assistant with real z/OSMF integration |

## Need Help?

- ADK documentation: https://developer.watson-orchestrate.ibm.com
- z/OSMF REST API reference: See `reference/zosmf-console-api.md`
- Ask your facilitator
