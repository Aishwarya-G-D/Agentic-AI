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


def _preferred_console_name(user: str) -> str:
    """Build a stable 8-char console name from user ID to encourage reuse."""
    cleaned = ''.join(ch for ch in user.upper() if ch.isalnum())
    if not cleaned:
        cleaned = "USER"
    if not cleaned[0].isalpha():
        cleaned = f"U{cleaned}"
    return (cleaned[:8]).ljust(2, "U")


def _run_console_command(command: str, max_retries: int = 10) -> dict:
    """Send a console command to z/OS via the z/OSMF REST Console API.

    Uses dynamic console allocation and attempts cleanup after each call
    to reduce the chance of exhausting available consoles.
    """
    host = connections.key_value("shivamsanjay_mainframe_connection")["host"]
    port = connections.key_value("shivamsanjay_mainframe_connection")["port"]
    credentials = {
        "user": connections.key_value("shivamsanjay_mainframe_connection")["username"],
        "password": connections.key_value("shivamsanjay_mainframe_connection")["password"],
    }
    payload = {"cmd": command, "sol-key": None}
    headers = {
        "Content-Type": "application/json",
        "X-CSRF-ZOSMF-HEADER": "",
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()

    last_error = None
    console_names = [_preferred_console_name(credentials["user"])]
    console_names.extend(_generate_console_name() for _ in range(max_retries - 1))

    for console_name in console_names:
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
            status_code = e.response.status_code if e.response is not None else "unknown"
            response_text = ""
            if e.response is not None and e.response.text:
                response_text = e.response.text.strip().replace("\n", " ")[:300]
            last_error = RuntimeError(
                f"HTTP {status_code} for console {console_name}. Response: {response_text}"
            )
        except requests.exceptions.RequestException as e:
            last_error = e
        finally:
            # Best-effort cleanup to avoid accumulating dynamic consoles.
            try:
                session.request(
                    method="DELETE",
                    url=url,
                    auth=(credentials["user"], credentials["password"]),
                    verify=False,
                    timeout=30,
                    headers=headers,
                )
            except requests.exceptions.RequestException:
                pass

    raise RuntimeError(
        f"Unable to find an available console after {max_retries} attempts: {last_error}"
    )


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",  
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_active_jobs() -> dict:  
    """Display all active address spaces on the z/OS system.

    Runs the z/OS command D A,L to show all active address spaces,
    including started tasks, batch jobs, and system tasks.
    Use this when the user asks about active jobs, running tasks,
    or wants a general system status overview.

    Returns:
        dict: The z/OSMF response with active address spaces.
    """
    return _run_console_command("D A,L")


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_address_space(jobname: str) -> dict:
    """Display details for a specific address space on the z/OS system.

    Runs the z/OS command D A,jobname for a single address space.
    Use this when the user asks for details about a specific
    job, started task, or address space.

    Args:
        jobname: The target job or address space name.

    Returns:
        dict: The z/OSMF response for the requested address space.
    """
    normalized_jobname = jobname.strip().upper()
    if not normalized_jobname:
        raise ValueError("jobname must not be empty")

    return _run_console_command(f"D A,{normalized_jobname}")


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_spool_utilization() -> dict:
    """Display JES2 spool utilization on the z/OS system.

    Runs the JES2 command $D SPOOL to show spool usage and status.
    Use this when the user asks about JES2 spool capacity,
    utilization, or spool health.

    Returns:
        dict: The z/OSMF response with JES2 spool details.
    """
    return _run_console_command("$D SPOOL")


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_wtor_messages() -> dict:
    """Display outstanding WTOR messages on the z/OS system.

    Runs the z/OS command D R,L to list outstanding WTORs
    and reply-required messages.

    Returns:
        dict: The z/OSMF response with WTOR details.
    """
    return _run_console_command("D R,L")


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_iplinfo() -> dict:
    """Display IPL information for the z/OS system.

    Runs the z/OS command D IPLINFO to show system IPL details,
    including when the system was last booted, IPL volume, and
    z/OS release information.

    Returns:
        dict: The z/OSMF response with IPL information.
    """
    return _run_console_command("D IPLINFO")


@tool(
    expected_credentials=[
        ExpectedCredentials(
            app_id="shivamsanjay_mainframe_connection",
            type=ConnectionType.KEY_VALUE,
        )
    ]
)
def shivamsanjay_display_online_dasd() -> dict:
    """Display online DASD device status on the z/OS system.

    Runs the z/OS command D U,DASD,ONLINE to list online DASD
    units and their status.

    Returns:
        dict: The z/OSMF response with online DASD details.
    """
    return _run_console_command("D U,DASD,ONLINE")