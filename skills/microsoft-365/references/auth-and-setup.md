# Authentication & Setup

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MICROSOFT_CLIENT_ID` | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `MICROSOFT_TENANT_ID` | Tenant ID (use `common` for multi-tenant) | `common` |

## App Registration Prerequisites

Register an application in Microsoft Entra ID (Azure AD):

1. Go to **Azure Portal > Microsoft Entra ID > App registrations > New registration**
2. Set **Supported account types** as appropriate (single tenant or multi-tenant)
3. Under **Authentication > Advanced settings**, set **Allow public client flows** to **Yes**
4. Under **API permissions**, add **Microsoft Graph** delegated permissions as needed (see [Delegated Permissions](#delegated-permissions) below)
5. Note the **Application (client) ID** and **Directory (tenant) ID**

## Device Code Flow

For the full Device Code Flow steps, see the shared reference: [`../../shared/auth/device-code-flow.md`](../../shared/auth/device-code-flow.md).

### Verify Authentication

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me" | jq '{displayName, mail, userPrincipalName}'
```

## Token Refresh

See the shared reference for token refresh steps: [`../../shared/auth/device-code-flow.md`](../../shared/auth/device-code-flow.md#token-refresh).

## Delegated Permissions

Common Microsoft Graph delegated permissions used by this skill:

| Permission | Description |
|------------|-------------|
| `Mail.Read` | Read user mail |
| `Mail.Send` | Send mail as the user |
| `Mail.ReadWrite` | Read and write user mail |
| `Calendars.ReadWrite` | Read and write user calendars |
| `Files.ReadWrite.All` | Read and write all files the user can access |
| `Team.ReadBasic.All` | Read teams the user is a member of |
| `Channel.ReadBasic.All` | Read channel names and descriptions |
| `ChannelMessage.Send` | Send channel messages |
| `ChatMessage.Send` | Send chat messages |
| `Notes.ReadWrite.All` | Read and write OneNote notebooks |
| `Tasks.ReadWrite` | Read and write To Do tasks |
| `Contacts.ReadWrite` | Read and write user contacts |
| `User.Read` | Read signed-in user profile |
| `User.ReadBasic.All` | Read basic profiles of all users |
| `Group.Read.All` | Read all groups |
| `Sites.ReadWrite.All` | Read and write SharePoint sites |

## Pagination

Many Graph API endpoints return paginated results. The response includes `@odata.nextLink` with the URL for the next page:

```bash
# First request
RESPONSE=$(curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages?\$top=10")

echo "$RESPONSE" | jq '.value'

# Get next page URL
NEXT_LINK=$(echo "$RESPONSE" | jq -r '.["@odata.nextLink"] // empty')

# Follow next page
if [ -n "$NEXT_LINK" ]; then
  curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$NEXT_LINK" | jq '.value'
fi
```

## Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `$top` | Number of results per page | `?$top=25` |
| `$skip` | Number of results to skip | `?$skip=10` |
| `$select` | Fields to return | `?$select=subject,from,receivedDateTime` |
| `$filter` | Filter results | `?$filter=isRead eq false` |
| `$orderby` | Sort results | `?$orderby=receivedDateTime desc` |
| `$search` | Search (KQL) | `?$search="keyword"` |
| `$count` | Include count of results | `?$count=true` |
