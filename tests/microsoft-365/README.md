# Microsoft 365 Smoke Tests

Automated smoke tests for the Microsoft 365 skill, verifying Graph API connectivity across key services.

## Prerequisites

1. A valid Microsoft Graph access token (via Device Code Flow)
2. `jq` installed
3. `curl` installed

## Usage

```bash
# Set your access token
export ACCESS_TOKEN="eyJ0..."

# Run all tests
bash tests/microsoft-365/smoke-test.sh

# Run a single test
bash tests/microsoft-365/smoke-test.sh outlook_read
bash tests/microsoft-365/smoke-test.sh teams_1on1_chat
```

## Test Coverage

| Test | Service | Operation | Type |
|------|---------|-----------|------|
| `outlook_read` | Outlook | List inbox messages | Read |
| `outlook_send` | Outlook | Send email to self | Write |
| `onenote_list` | OneNote | List notebooks | Read |
| `onenote_create` | OneNote | Create a notebook | Write |
| `sharepoint_root` | SharePoint | Get root site | Read |
| `sharepoint_search` | SharePoint | Search sites | Read |
| `teams_list` | Teams | List joined teams | Read |
| `teams_channel_message` | Teams | Send message to channel | Write |
| `teams_1on1_chat` | Teams | Create 1-1 chat & send message | Write |

## Notes

- Write tests create real resources (emails, notebooks, messages). Run in a test tenant if possible.
- Tests that depend on tenant data (e.g., Teams channels, other users) will **SKIP** gracefully if prerequisites are not met.
- Exit code is `1` if any test fails, `0` otherwise.
