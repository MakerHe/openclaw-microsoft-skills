# Device Code Flow Authentication

Device Code Flow (OAuth2) allows authentication without directly entering credentials in the CLI. The user completes login in a browser on any device, and the CLI automatically receives tokens.

## When to Use

- No PAT available or PAT management is undesirable
- Organization requires OAuth/MFA-based authentication
- Interactive CLI usage where a browser is accessible on any device

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_DEVOPS_CLIENT_ID` | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_DEVOPS_TENANT_ID` | Tenant ID (use `organizations` for multi-tenant) | `organizations` |
| `AZURE_DEVOPS_ORG` | Organization name | `myorg` |
| `AZURE_DEVOPS_PROJECT` | Default project name | `MyProject` |

## App Registration Prerequisites

Register an application in Microsoft Entra ID (Azure AD):

1. Go to **Azure Portal > Microsoft Entra ID > App registrations > New registration**
2. Set **Supported account types** to match your org (single tenant or multi-tenant)
3. Under **Authentication > Advanced settings**, set **Allow public client flows** to **Yes**
4. Under **API permissions**, add:
   - `Azure DevOps` > `user_impersonation` (delegated)
5. Note the **Application (client) ID** and **Directory (tenant) ID**

## Device Code Flow Steps

### Step 1: Request Device Code

```bash
TENANT_ID="${AZURE_DEVOPS_TENANT_ID:-organizations}"

DEVICE_CODE_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/devicecode" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$AZURE_DEVOPS_CLIENT_ID" \
  -d "scope=499b84ac-1321-427f-aa17-267ca6975798/.default")

echo "$DEVICE_CODE_RESPONSE" | jq -r '.message'
DEVICE_CODE=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.device_code')
INTERVAL=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.interval')
```

This prints a message like:
> To sign in, use a web browser to open https://microsoft.com/devicelogin and enter the code XXXXXXXXX

### Step 2: User Completes Login

The user opens `https://microsoft.com/devicelogin` in any browser, enters the displayed code, and signs in with their Azure AD account.

### Step 3: Poll for Token

While the user completes login, poll the token endpoint:

```bash
while true; do
  TOKEN_RESPONSE=$(curl -s -X POST \
    "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
    -d "client_id=$AZURE_DEVOPS_CLIENT_ID" \
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

### Step 4: Call Azure DevOps API with Bearer Token

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1" | jq '.value[].name'
```

### Step 5: Refresh Token

Access tokens expire (typically in 1 hour). Use the refresh token to get a new access token:

```bash
TOKEN_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=$AZURE_DEVOPS_CLIENT_ID" \
  -d "refresh_token=$REFRESH_TOKEN")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.refresh_token')
```

## Scope

The scope for Azure DevOps is the Azure DevOps resource application ID with `/.default`:

```
499b84ac-1321-427f-aa17-267ca6975798/.default
```

This requests all permissions granted to the app registration.

## Bearer Token vs PAT Authentication

| Aspect | PAT (`-u ":$PAT"`) | Bearer (`-H "Authorization: Bearer $TOKEN"`) |
|--------|---------------------|-----------------------------------------------|
| Auth header | `Authorization: Basic <base64>` | `Authorization: Bearer <token>` |
| Token lifetime | Up to 1 year (configurable) | ~1 hour (auto-refreshable) |
| MFA support | No | Yes |
| Management | Manual creation in portal | Automatic via OAuth flow |

## Complete Example: List Projects

```bash
# Full flow: authenticate and list projects
TENANT_ID="${AZURE_DEVOPS_TENANT_ID:-organizations}"

# Request device code
DEVICE_CODE_RESPONSE=$(curl -s -X POST \
  "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/devicecode" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$AZURE_DEVOPS_CLIENT_ID" \
  -d "scope=499b84ac-1321-427f-aa17-267ca6975798/.default")

echo "$DEVICE_CODE_RESPONSE" | jq -r '.message'
DEVICE_CODE=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.device_code')
INTERVAL=$(echo "$DEVICE_CODE_RESPONSE" | jq -r '.interval')

# Poll for token
while true; do
  TOKEN_RESPONSE=$(curl -s -X POST \
    "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
    -d "client_id=$AZURE_DEVOPS_CLIENT_ID" \
    -d "device_code=$DEVICE_CODE")

  ERROR=$(echo "$TOKEN_RESPONSE" | jq -r '.error // empty')
  if [ -z "$ERROR" ]; then
    ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
    break
  elif [ "$ERROR" = "authorization_pending" ]; then
    sleep "$INTERVAL"
  elif [ "$ERROR" = "slow_down" ]; then
    INTERVAL=$((INTERVAL + 5))
    sleep "$INTERVAL"
  else
    echo "Error: $ERROR"; break
  fi
done

# List projects
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/projects?api-version=7.1" | jq '.value[].name'
```
