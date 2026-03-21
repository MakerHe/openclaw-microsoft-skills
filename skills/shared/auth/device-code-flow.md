# Shared Device Code Flow Authentication

Device Code Flow (OAuth2) via Microsoft Entra ID. A single login can cover both Microsoft Graph and Azure DevOps APIs when the app registration has permissions for both.

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MICROSOFT_CLIENT_ID` | Yes | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `MICROSOFT_TENANT_ID` | No | Tenant ID (default: `common`) | `common` |
| `MICROSOFT_CLIENT_SECRET` | No | Client secret — include if the app is a confidential client; omit for public clients | `Cvp8Q~...` |

## App Registration Prerequisites

Register an application in Microsoft Entra ID:

1. Go to **Azure Portal > Microsoft Entra ID > App registrations > New registration**
2. Set **Supported account types** as appropriate (single tenant or multi-tenant)
3. Choose one of:
   - **Public client**: Under **Authentication > Advanced settings**, set **Allow public client flows** to **Yes**. No client secret needed.
   - **Confidential client**: Under **Certificates & secrets**, create a client secret. Set `MICROSOFT_CLIENT_SECRET`.
4. Under **API permissions**, add delegated permissions as needed:
   - **Microsoft Graph** — e.g., `Mail.Read`, `Calendars.ReadWrite`, `Files.ReadWrite.All`, `User.Read`, etc.
   - **Azure DevOps** — `user_impersonation` (resource ID: `499b84ac-1321-427f-aa17-267ca6975798`)
5. Note the **Application (client) ID** and **Directory (tenant) ID**

> If you only need one service, you can omit the other's permissions.

## Important: One Resource Per Token

OAuth2 v2.0 does **not** support requesting `.default` scopes for multiple resources in a single token request. Each access token has exactly one audience (resource).

To access both Microsoft Graph and Azure DevOps with a **single user login**:

1. Authenticate with one resource's scope (e.g., `https://graph.microsoft.com/.default`)
2. Obtain a refresh token
3. Use the refresh token to silently acquire a token for the other resource (e.g., `499b84ac-1321-427f-aa17-267ca6975798/.default`)

> **Do NOT combine scopes** like `https://graph.microsoft.com/.default 499b84ac-1321-427f-aa17-267ca6975798/.default` — this will fail with `invalid_scope`.

## Device Code Flow Steps

### Step 1: Request Device Code

Pick the scope for the resource you want the initial token for. Use `offline_access` to ensure a refresh token is returned.

```bash
TENANT_ID="${MICROSOFT_TENANT_ID:-common}"

# Choose your initial scope (Graph or Azure DevOps):
SCOPE="https://graph.microsoft.com/.default offline_access"
# Or for Azure DevOps only:
# SCOPE="499b84ac-1321-427f-aa17-267ca6975798/.default offline_access"

DEVICE_CODE_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/devicecode" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "scope=$SCOPE")

echo "$DEVICE_CODE_RESPONSE" | jq -r '.message'
DEVICE_CODE=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.device_code')
INTERVAL=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.interval')
```

This prints a message like:
> To sign in, use a web browser to open https://microsoft.com/devicelogin and enter the code XXXXXXXXX

### Step 2: User Completes Login

The user opens `https://microsoft.com/devicelogin` in any browser, enters the displayed code, and signs in with their Microsoft account.

### Step 3: Poll for Token

Include `client_secret` if set (confidential client). The `offline_access` scope ensures a refresh token is returned.

```bash
# Build optional client_secret parameter
CLIENT_SECRET_PARAM=""
if [ -n "$MICROSOFT_CLIENT_SECRET" ]; then
  CLIENT_SECRET_PARAM="-d client_secret=$MICROSOFT_CLIENT_SECRET"
fi

while true; do
  TOKEN_RESPONSE=$(curl -s -X POST \
    "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
    -d "client_id=$MICROSOFT_CLIENT_ID" \
    -d "device_code=$DEVICE_CODE" \
    $CLIENT_SECRET_PARAM)

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

### Step 4: Use the Token

```bash
# Microsoft Graph (if initial scope was graph)
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me"
```

### Step 5: Exchange Refresh Token for Another Resource (Optional)

If you need tokens for both Microsoft Graph and Azure DevOps, use the refresh token to silently acquire a token for the other resource — **no second user login required**.

```bash
# Example: exchange refresh token for an Azure DevOps token
AZDO_TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "scope=499b84ac-1321-427f-aa17-267ca6975798/.default offline_access" \
  ${MICROSOFT_CLIENT_SECRET:+-d client_secret=$MICROSOFT_CLIENT_SECRET})

AZDO_ACCESS_TOKEN=$(echo "$AZDO_TOKEN_RESPONSE" | jq -r '.access_token')
# Also capture the new refresh token (rotation)
REFRESH_TOKEN=$(echo "$AZDO_TOKEN_RESPONSE" | jq -r '.refresh_token // empty')

# Use it
curl -s -H "Authorization: Bearer $AZDO_ACCESS_TOKEN" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

> **Tip**: The refresh token may rotate on each use. Always save the latest `refresh_token` from the response.

## Token Refresh

Access tokens expire (typically in 1 hour). Use the refresh token to obtain a new access token for any resource:

```bash
# Refresh for Microsoft Graph
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "scope=https://graph.microsoft.com/.default offline_access" \
  ${MICROSOFT_CLIENT_SECRET:+-d client_secret=$MICROSOFT_CLIENT_SECRET})

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token // empty')

# Refresh for Azure DevOps
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "scope=499b84ac-1321-427f-aa17-267ca6975798/.default offline_access" \
  ${MICROSOFT_CLIENT_SECRET:+-d client_secret=$MICROSOFT_CLIENT_SECRET})

AZDO_ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token // empty')
```
