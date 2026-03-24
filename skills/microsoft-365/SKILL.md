---
name: microsoft-365
description: Interact with Microsoft 365 via Microsoft Graph API using the openclaw-microsoft-m365 Python SDK — mail, calendar, OneDrive, Teams, OneNote, To Do, contacts, users, groups, and SharePoint
---

# Microsoft 365 Skill

Interact with Microsoft 365 services using the `openclaw-microsoft-m365` Python SDK.

## Package

```bash
pip install openclaw-microsoft-m365
```

## Authentication

Environment variables are stored in `~/.openclaw/.env` (read automatically by `from_env()`). Login tokens are persisted in `~/.openclaw/credentials/`.

| Variable | Required | Description |
|----------|----------|-------------|
| `MICROSOFT_CLIENT_ID` | Yes | Application (client) ID from Entra ID |
| `MICROSOFT_TENANT_ID` | Yes | Tenant ID (use `common` for multi-tenant) |
| `MICROSOFT_CLIENT_SECRET` | No | Client secret for confidential-client flows |

### Construct and authenticate

```python
from openclaw_microsoft_m365 import Microsoft365Client

client = Microsoft365Client.from_env()
client.authenticate()
```

`from_env()` raises `ValueError` if `MICROSOFT_CLIENT_ID` is missing.

`authenticate()` behaviour:
- **First run** — prints a device-code URL + code; blocks until login completes.
- **Token valid** — prints `"Authentication successful (existing token is still valid)."`.
- **Silent refresh** — acquires a new token silently from the saved refresh token.
- **Expired** — clears stale credentials and falls back to device-code flow.

After `authenticate()` the client attaches the Bearer token to every request automatically.

## Routing

| Topic | Reference |
|-------|-----------|
| Auth setup, permissions, pagination, query params | `references/auth-and-setup.md` |
| Outlook mail (list, read, send, reply, forward, delete, folders, attachments) | `references/mail.md` |
| Calendar events (list, create, update, delete, free/busy) | `references/calendar.md` |
| OneDrive files (list, upload, download, delete, share, search) | `references/onedrive.md` |
| Teams (teams, channels, messages, members) | `references/teams.md` |
| OneNote (notebooks, sections, pages) | `references/onenote.md` |
| Microsoft To Do (task lists, tasks) | `references/todo.md` |
| Contacts (contacts, contact folders) | `references/contacts.md` |
| Users and groups (profile, list users, groups, members) | `references/users-groups.md` |
| SharePoint (sites, lists, list items) | `references/sharepoint.md` |

## Instructions

1. **Authenticate** — `Microsoft365Client.from_env()` then `client.authenticate()`. If `from_env()` raises `ValueError`, tell the user `MICROSOFT_CLIENT_ID` is missing from `~/.openclaw/.env` and stop.
2. **Route** — read the appropriate reference file for the user's request.
3. **Execute** — call methods on the client's service attributes (`client.mail`, `client.calendar`, etc.).
4. **Parse** — extract and present relevant fields from the returned data.
5. **Paginate** — if a response includes `@odata.nextLink`, fetch the next page until all results are collected.
6. **Cleanup** — call `client.close()` or use `with Microsoft365Client.from_env() as client:`.
