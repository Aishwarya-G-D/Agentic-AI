from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def shivamsanjay_greeting(name: str) -> str:
    """Greeting for a specific person"""
    return f"Hello, {name}! Welcome to the workshop."