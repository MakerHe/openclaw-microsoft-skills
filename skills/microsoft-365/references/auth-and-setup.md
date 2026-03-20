# Authentication & Setup

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `M365_CLIENT_ID` | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `M365_TENANT_ID` | Tenant ID (use `common` for multi-tenant) | `common` |

## App Registration Prerequisites

Register an application in Microsoft Entra ID (Azure AD):

1. Go to **Azure Portal > Microsoft Entra ID > App registrations > New registration**
2. Set **Supported account types** as appropriate (single tenant or multi-tenant)
3. Under **Authentication > Advanced settings**, set **Allow public client flows** to **Yes**
4. Under **API permissions**, add **Microsoft Graph** delegated permissions as needed (see [Delegated Permissions](#delegated-permissions) below)
5. Note the **Application (client) ID** and **Directory (tenant) ID**

## Device Code Flow

### Step 1: Request Device Code

```bash
TENANT_ID="${M365_TENANT_ID:-common}"

DEVICE_CODE_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/devicecode" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$M365_CLIENT_ID" \
  -d "scope=https://graph.microsoft.com/.default")

echo "$DEVICE_CODE_RESPONSE" | jq -r '.message'
DEVICE_CODE=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.device_code')
INTERVAL=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.interval')
```

This prints a message like:
> To sign in, use a web browser to open https://microsoft.com/devicelogin and enter the code XXXXXXXXX

### Step 2: User Completes Login

The user opens `https://microsoft.com/devicelogin` in any browser, enters the displayed code, and signs in with their Microsoft account.

### Step 3: Poll for Token

```bash
while true; do
  TOKEN_RESPONSE=$(curl -s -X POST \
    "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
    -d "client_id=$M365_CLIENT_ID" \
    -d "device_code=$DEVICE_CODE")

  ERROR=$(echo "$TOKEN_RESPONSE" | jq -r '.error // empty')

  if [ -z "$ERROR" ]; then
    ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
    REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token')
    echo "Authentication successful."
    break
  elif [ "$ERROR" = "authorization_pending" ]; then
    sleep "$INTERVAL"
  elif [ "$ERROR" = "slow_down" ]; then
    INTERVAL=$((INTERVAL + 5))
    sleep "$INTERVAL"
  else
    echo "Error: $ERROR - $(echo "$TOKEN_RESPONSE" | jq -r '.error_description')"
    break
  fi
done
```

### Step 4: Verify Authentication

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me" | jq '{displayName, mail, userPrincipalName}'
```

## Token Refresh

Access tokens expire (typically in 1 hour). Use the refresh token to obtain a new access token:

```bash
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$M365_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token')
```

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
