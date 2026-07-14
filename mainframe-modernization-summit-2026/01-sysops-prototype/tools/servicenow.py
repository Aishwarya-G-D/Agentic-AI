"""ServiceNow Tools — Group 2 SysOps Foundation.

Creates and searches incidents in ServiceNow via the Table API.
"""

import requests
import urllib3
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.run import connections

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_CONNECTION_ID = "group_2_servicenow"


def _normalize_instance(instance: str) -> str:
    """Normalize instance input to a bare hostname."""
    value = instance.strip()
    value = value.removeprefix("https://").removeprefix("http://")
    return value.rstrip("/")


def _get_session() -> tuple[requests.Session, str, str]:
    """Build an authenticated requests session and return (session, base_url, instance)."""
    raw_instance = connections.key_value(_CONNECTION_ID)["instance"]
    instance = _normalize_instance(raw_instance)
    username = connections.key_value(_CONNECTION_ID)["username"]
    password = connections.key_value(_CONNECTION_ID)["password"]

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    base_url = f"https://{instance}/api/now/table"
    return session, base_url, instance


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id=_CONNECTION_ID,
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def group_2_create_incident(
    short_description: str,
    description: str,
    urgency: int = 2,
    impact: int = 2,
) -> dict:
    """Create a new incident in ServiceNow.

    Opens a new incident ticket and returns the sys_id, number, and state.
    Use this when the user asks to create, open, or log an incident.

    Args:
        short_description: One-line summary of the issue.
        description: Detailed description of the incident.
        urgency: Urgency level — 1 (High), 2 (Medium), 3 (Low). Defaults to 2.
        impact: Impact level — 1 (High), 2 (Medium), 3 (Low). Defaults to 2.

    Returns:
        dict: Created incident including sys_id, number, and state.
    """
    session, base_url, instance = _get_session()
    payload = {
        "short_description": short_description,
        "description": description,
        "urgency": str(urgency),
        "impact": str(impact),
        "caller_id": "admin",
    }
    response = session.post(
        f"{base_url}/incident",
        json=payload,
        verify=False,
        timeout=30,
    )
    response.raise_for_status()
    record = response.json().get("result", {})
    sys_id = record.get("sys_id")
    number = record.get("number")
    if not sys_id or not number:
        raise RuntimeError("Incident creation response did not include sys_id and number")

    verify_response = session.get(
        f"{base_url}/incident/{sys_id}",
        params={"sysparm_fields": "sys_id,number,state,short_description,sys_created_on"},
        verify=False,
        timeout=30,
    )
    verify_response.raise_for_status()
    verified_record = verify_response.json().get("result", {})
    verified_number = verified_record.get("number")
    if verified_number != number:
        raise RuntimeError("Incident verification failed: created record could not be confirmed")

    return {
        "verified": True,
        "instance": instance,
        "sys_id": sys_id,
        "number": number,
        "state": verified_record.get("state"),
        "short_description": verified_record.get("short_description"),
        "created_on": verified_record.get("sys_created_on"),
        "portal_url": f"https://{instance}/nav_to.do?uri=incident.do?sys_id={sys_id}",
    }


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id=_CONNECTION_ID,
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def group_2_search_incidents(
    query: str,
    limit: int = 10,
) -> dict:
    """Search for existing incidents in ServiceNow.

    Queries incidents whose short_description or description contains the
    given keyword. Use this when the user asks to find, list, or check incidents.

    Args:
        query: Keyword or phrase to search for in incident records.
        limit: Maximum number of results to return. Defaults to 10.

    Returns:
        dict: List of matching incidents with number, state, and description.
    """
    if not query.strip():
        raise ValueError("query must not be empty")

    session, base_url, instance = _get_session()
    params = {
        "sysparm_query": f"short_descriptionLIKE{query}^ORdescriptionLIKE{query}",
        "sysparm_limit": str(limit),
        "sysparm_fields": "number,state,short_description,description,sys_created_on,urgency,impact",
    }
    response = session.get(
        f"{base_url}/incident",
        params=params,
        verify=False,
        timeout=30,
    )
    response.raise_for_status()
    records = response.json().get("result", [])
    return {
        "instance": instance,
        "count": len(records),
        "incidents": [
            {
                "number": r.get("number"),
                "state": r.get("state"),
                "short_description": r.get("short_description"),
                "urgency": r.get("urgency"),
                "impact": r.get("impact"),
                "created_on": r.get("sys_created_on"),
            }
            for r in records
        ],
    }
