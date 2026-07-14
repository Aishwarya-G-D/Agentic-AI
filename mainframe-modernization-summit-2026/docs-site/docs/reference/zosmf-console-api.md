# z/OSMF REST Console API Reference

The z/OSMF REST Console API allows you to issue z/OS operator commands and retrieve responses programmatically. This is the API used by the z/OS console tools in the SysOps challenge.

---

## API Endpoint

```
PUT https://<host>:<port>/zosmf/restconsoles/consoles/<console-name>
```

- `<host>` — z/OSMF host IP address or hostname
- `<port>` — z/OSMF port (typically 443 or a custom port)
- `<console-name>` — Console name to use. Must be unique per concurrent user (max 8 characters, must start with a letter). Use a dynamically generated name to avoid conflicts in shared environments.

---

## Authentication

z/OSMF uses HTTP Basic Authentication with a RACF user ID and password.

```
Authorization: Basic <base64(username:password)>
```

In Python with `requests`:

```python
response = requests.put(url, auth=(username, password), ...)
```

---

## Request Headers

```
Content-Type: application/json
X-CSRF-ZOSMF-HEADER: ""
```

The `X-CSRF-ZOSMF-HEADER` is required by z/OSMF for CSRF protection. The value can be an empty string.

---

## Request Body

```json
{
    "cmd": "D A,L",
    "sol-key": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cmd` | string | Yes | The z/OS operator command to execute |
| `sol-key` | string | No | Key to wait for a specific solicited message (set to `null` for immediate response) |

---

## Response

```json
{
    "cmd-response-key": "C0000001",
    "cmd-response-url": "/zosmf/restconsoles/consoles/defcn/solmsgs/C0000001",
    "cmd-response": "IEE114I 14.30.00 2026.112 ACTIVITY 831...\n JOBS     M/S   TS USERS    SYSAS    INITS   ACTIVE/MAX\n   0002   0042   0000       0030    0001    0001/00010"
}
```

| Field | Description |
|-------|-------------|
| `cmd-response-key` | Identifier for this command response |
| `cmd-response-url` | URL to retrieve solicited messages (if any) |
| `cmd-response` | The text output from the command |

---

## Common Display Commands

These are the commands used in the SysOps challenge. All are read-only.

| Command | What It Shows |
|---------|--------------|
| `D A,L` | Active address spaces (jobs, started tasks, system tasks) |
| `D J,jobname` | Status of a specific job or STC |
| `$D SPOOL` | JES2 spool utilization (percent full, tracks used) |
| `D R,L` | Outstanding operator messages (WTO/WTOR waiting for reply) |
| `D ASM` | Auxiliary storage (page dataset) status |
| `D IPLINFO` | IPL information (system name, IPL volume, IPL time) |

---

## Python Example

```python
import random
import string

import requests
import urllib3

# Suppress SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generate_console_name():
    """Generate a random console name (max 8 chars, starting with a letter)."""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"CN{suffix}"


def run_console_command(host, port, username, password, command, max_retries=5):
    """Send a console command to z/OS via z/OSMF.

    Uses dynamic console names with retry to avoid conflicts
    when multiple participants share the same z/OSMF instance.
    """
    session = requests.Session()

    last_error = None
    for _ in range(max_retries):
        console_name = generate_console_name()
        url = f"https://{host}:{port}/zosmf/restconsoles/consoles/{console_name}"
        try:
            response = session.put(
                url,
                json={"cmd": command, "sol-key": None},
                auth=(username, password),
                headers={
                    "Content-Type": "application/json",
                    "X-CSRF-ZOSMF-HEADER": "",
                },
                verify=False,   # Self-signed certificates
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("cmd-response", "No output returned.")
        except requests.exceptions.HTTPError as e:
            last_error = e
            continue

    raise RuntimeError(
        f"Unable to find an available console after {max_retries} attempts: {last_error}"
    )


# Example usage
output = run_console_command(
    host="10.1.2.3",
    port="10443",
    username="IBMUSER",
    password="password",
    command="D A,L",
)
print(output)
```

---

## Error Codes

| HTTP Status | Meaning | Likely Cause |
|------------|---------|--------------|
| 400 | Bad Request | Console name already in use by another session — use dynamic console names with retry |
| 401 | Unauthorized | Wrong username/password or expired password |
| 403 | Forbidden | User ID lacks RACF authorization for z/OSMF or console commands |
| 404 | Not Found | Wrong console name or z/OSMF REST services not configured |
| 500 | Internal Server Error | z/OSMF server issue; check z/OSMF logs |
| Connection Error | Cannot reach host | Wrong IP/port, firewall block, or z/OSMF not running |

---

## Troubleshooting

1. **Test connectivity first**: `curl -k https://<host>:<port>/zosmf/info`
2. **Check RACF authorization**: User needs access to IZUDFLT profile in the ZMFAPLA class
3. **Console name**: Do **not** use `defcn` in a shared environment — it causes 400 errors when multiple users compete for the same console. Generate a random console name (max 8 chars, starting with a letter) and retry on failure.
4. **SSL certificates**: Use `verify=False` for self-signed z/OSMF certificates in development/workshop environments
