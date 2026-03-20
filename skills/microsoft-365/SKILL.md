---
name: microsoft-365
description: Interact with Microsoft 365 via Microsoft Graph API - mail, calendar, OneDrive, Teams, OneNote, To Do, contacts, users, groups, and SharePoint
---

# Microsoft 365 Skill

Interact with Microsoft 365 services via the Microsoft Graph API using curl commands with delegated user permissions.

## Authentication Setup

This skill uses Device Code Flow (OAuth2) for authentication. The user completes login in a browser, and the CLI receives tokens automatically.

Required environment variables:

- `M365_CLIENT_ID` — Application (client) ID from Microsoft Entra ID app registration
- `M365_TENANT_ID` — Tenant ID (default: `common` for multi-tenant)

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me"
```

## API Base URL

All endpoints use:

```
https://graph.microsoft.com/v1.0
```

## Routing

Route the user's request to the appropriate reference file:

| Topic | Reference |
|-------|-----------|
| Auth (Device Code Flow), setup, permissions, pagination | `references/auth-and-setup.md` |
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

1. **Check authentication**: Verify `M365_CLIENT_ID` is set. If not, inform the user and stop.
2. **Authenticate**: Execute Device Code Flow to obtain an access token (see `references/auth-and-setup.md`).
3. **Route**: Read the appropriate reference file based on the user's request.
4. **Execute**: Use `curl` with `-H "Authorization: Bearer $ACCESS_TOKEN"` to call Graph API endpoints.
5. **Parse**: Use `jq` to extract specific fields from JSON responses.
6. **Paginate**: If the response contains `@odata.nextLink`, follow it to retrieve additional pages.
7. **Content-Type**: For POST/PUT/PATCH requests, set `-H "Content-Type: application/json"`.
