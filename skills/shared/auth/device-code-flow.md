# Shared Device Code Flow Authentication

Device Code Flow (OAuth2) via Microsoft Entra ID. A single login can cover both Microsoft Graph and Azure DevOps APIs when the app registration has permissions for both.

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MICROSOFT_CLIENT_ID` | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `MICROSOFT_TENANT_ID` | Tenant ID (default: `common`) | `common` |

## App Registration Prerequisites

Register an application in Microsoft Entra ID:

1. Go to **Azure Portal > Microsoft Entra ID > App registrations > New registration**
2. Set **Supported account types** as appropriate (single tenant or multi-tenant)
3. Under **Authentication > Advanced settings**, set **Allow public client flows** to **Yes**
4. Under **API permissions**, add delegated permissions as needed:
   - **Microsoft Graph** — e.g., `Mail.Read`, `Calendars.ReadWrite`, `Files.ReadWrite.All`, `User.Read`, etc.
   - **Azure DevOps** — `user_impersonation`
5. Note the **Application (client) ID** and **Directory (tenant) ID**

> If you only need one service, you can omit the other's permissions. The merged scope below will simply request whatever permissions have been granted.

## Merged Scope

The scope combines Microsoft Graph and Azure DevOps resource IDs, space-separated:

```
https://graph.microsoft.com/.default 499b84ac-1321-427f-aa17-267ca6975798/.default
```

This requests all delegated permissions granted to the app for both resources in a single login.

> **Note**: If the app registration only has permissions for one resource, include only that resource's scope. The merged scope is for apps that need both.

## Device Code Flow Steps

### Step 1: Request Device Code

```bash
TENANT_ID="${MICROSOFT_TENANT_ID:-common}"

DEVICE_CODE_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/devicecode" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "scope=https://graph.microsoft.com/.default 499b84ac-1321-427f-aa17-267ca6975798/.default")

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
    -d "client_id=$MICROSOFT_CLIENT_ID" \
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

### Step 4: Use the Token

The `$ACCESS_TOKEN` is valid for both APIs:

```bash
# Microsoft Graph
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me"

# Azure DevOps
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1"
```

## Token Refresh

Access tokens expire (typically in 1 hour). Use the refresh token to obtain a new access token:

```bash
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$MICROSOFT_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token')
```
