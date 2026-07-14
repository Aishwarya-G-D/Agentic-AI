---
title: "Challenge 0 — **Hello World**"
sub_title: Your First Agent with Watsonx Orchestrate ADK
author: WxA4Z Workshop
---

What You Will Build
===

A simple agent called **greeter** that responds to "Greeting" by running a Python tool that returns "Hello World".

<!-- pause -->

<!-- new_lines: 2 -->

Three foundational concepts:

<!-- incremental_lists: true -->

* **Agent definition** — a YAML file that describes what the agent does
* **Tool** — a Python function the agent can call
* **ADK CLI** — the commands to import and test your work

<!-- end_slide -->

Prerequisites
===

Before starting, confirm your environment is ready:

<!-- pause -->

```bash +exec
# Check Python version (must be 3.11+)
python3 --version
```

<!-- pause -->

```bash +exec
# Check that uv is installed
uv --version
```

<!-- pause -->

```bash +exec
# Check that the ADK CLI is available
orchestrate --version
```

<!-- pause -->

Make sure you have activated your Watsonx Orchestrate environment:

```bash
orchestrate env activate workshop
```

<!-- end_slide -->

<!-- jump_to_middle -->

Let's Build It
===

<!-- end_slide -->

Step 1: The Agent Definition
===

Open `greeter.yaml` and examine the contents:

```yaml
spec_version: v1
kind: native
name: greeter_<your_id>
description: An agent that greets you using the output from its tool
instructions: Always run the tool "Greeting" when the user types Greeting in the chat.
llm: groq/openai/gpt-oss-120b
style: default
collaborators: []
tools:
  - greeting
```

<!-- end_slide -->

Step 1: Key Fields
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

| Field | Purpose |
|-------|---------|
| `name` | Unique agent identifier |
| `description` | What the agent does |
| `instructions` | Behavioral rules |
| `llm` | Language model to use |
| `tools` | Tools the agent can call |

<!-- column: 1 -->

**Important:**

<!-- incremental_lists: true -->

* Replace `<your_id>` with your Kyndryl ID
* The `description` is read by the LLM
* The `instructions` guide agent behavior
* The `llm` must be a model that currently exists in the environment
* `tools` must match your tool function names

<!-- end_slide -->

Step 2: The Tool
===

Open `tools/greetings.py`:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def <yout_id>_greeting() -> str:
    """
    Greeting for everyone
    """
    greeting = "Hello World"
    return greeting
```

<!-- end_slide -->

Step 2: Key Concepts
===

<!-- incremental_lists: true -->

* The `@tool` decorator registers the function as an agent tool
* The **function name** (`greeting`) must match the agent's `tools:` list
* Replace <your_id> with your ID so the function name doesn't collide
* The **docstring** is what the LLM reads to decide when to call this tool
* The return value is what the agent sends back to the user

<!-- end_slide -->

<!-- jump_to_middle -->

Importing & Testing
===

<!-- end_slide -->

Step 3: Import the Tool
===

From the `00-hello-world/` directory, run:

```bash +exec
orchestrate tools import -k python -f tools/greetings.py
```

<!-- pause -->

<!-- new_lines: 2 -->

You should see a confirmation that the tool was imported.

<!-- pause -->

**Flags explained:**

| Flag | Meaning |
|------|---------|
| `-k python` | Tool kind is Python |
| `-f tools/greetings.py` | Path to the tool file |

<!-- end_slide -->

Step 4: Import the Agent
===

```bash +exec
orchestrate agents import -f greeter.yaml
```

<!-- pause -->

<!-- new_lines: 2 -->

You should see a confirmation that the agent was imported.

<!-- pause -->

<!-- new_lines: 2 -->

**Remember:** Every time you change your agent YAML or tool code, you must re-import!

<!-- end_slide -->

Step 5: Test Your Agent
===

Test the agent on Watsonx Orchestrate.

<!-- pause -->

<!-- new_lines: 2 -->

Try typing:

```
Greeting
```

<!-- pause -->

<!-- new_lines: 2 -->

Expected response: **"Hello World"**

<!-- end_slide -->

<!-- jump_to_middle -->

Experiments
===

<!-- end_slide -->

Experiment 1: Change the Message
===

Edit `tools/greetings.py` to return something different:

```python
@tool
def greeting() -> str:
    """Greeting for everyone"""
    return "Hello from the Watsonx Orchestrate workshop!"
```

<!-- pause -->

Then re-import:

```bash +exec
orchestrate tools import -k python -f tools/greetings.py
```

<!-- end_slide -->

Experiment 2: Add a Parameter
===

Modify the tool to accept a `name` parameter:

```python
@tool
def greeting(name: str) -> str:
    """Greeting for a specific person"""
    return f"Hello, {name}! Welcome to the workshop."
```

<!-- pause -->

<!-- new_lines: 2 -->

Now when you chat with the agent, it can produce **personalized greetings**.

<!-- pause -->

Don't forget to re-import the tool!

<!-- end_slide -->

Experiment 3: Update Instructions
===

Change the agent's `instructions` field to trigger on different phrases:

```yaml
instructions: >
  Run the "Greeting" tool when the user says hello,
  hi, or asks for a greeting. Always be friendly.
```

<!-- pause -->

<!-- new_lines: 2 -->

Then re-import the agent:

```bash +exec
orchestrate agents import -f greeter.yaml
```

<!-- end_slide -->

What You Learned
===

| Concept | What It Means |
|---------|--------------|
| Agent YAML | Declarative definition of an agent |
| `@tool` decorator | Turns a Python function into an agent tool |
| `orchestrate tools import` | Registers a tool in the environment |
| `orchestrate agents import` | Registers an agent in the environment |

<!-- end_slide -->

<!-- jump_to_middle -->

The Import-Test Loop
===

<!-- pause -->

**Change** → **Re-import** → **Test** → **Repeat**

<!-- pause -->

<!-- new_lines: 2 -->

This is the core development workflow for building agents with the ADK.

<!-- end_slide -->

<!-- jump_to_middle -->

Next Up
===

**Challenge 1: SysOps Foundation Prototype**

`../01-sysops-prototype/`
