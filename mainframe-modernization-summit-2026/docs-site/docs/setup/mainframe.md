# Environment Connection Details

This page lists the connection details for all external systems used during the workshop.

---

## Mainframe (zD&T)

During the workshop we will be using a **zD&T** (IBM Z Development and Test Environment) instance.

| Resource | Value |
|----------|-------|
| Host | `20.110.90.209` |
| z/OSMF port | `10443` |
| 3270 port | `992` |

### Credentials

The user ID and password for each participant will be shared by the workshop staff.

!!! warning "Reset Your Password"
    You **must** reset your initial mainframe password before proceeding. The first time you log on via 3270, the system will prompt you to change it. Complete this step before attempting any z/OSMF or agent operations.

---

## ServiceNow (Dev Instance)

The workshop uses a shared **ServiceNow Developer instance** for incident management exercises.

| Resource | Value |
|----------|-------|
| Instance URL | `https://dev231463.service-now.com` |
| Username | `admin` |
| Password | `5Op5Q%jzNwN-` |

[:fontawesome-solid-arrow-right-to-bracket: **Click here to log in automatically**](https://dev231463.service-now.com/login.do?user_name=admin&sys_action=sysverb_login&user_password=5Op5Q%25jzNwN-){ .md-button .md-button--primary target="_blank" }

!!! info "Shared Instance"
    This is a shared dev instance. All participants use the same admin account. Be mindful of other participants' data when creating or modifying incidents.
