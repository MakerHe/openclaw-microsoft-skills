# Device Code Flow Authentication (Azure DevOps)

For the full Device Code Flow steps, see the shared authentication reference: [`../../shared/auth/device-code-flow.md`](../../shared/auth/device-code-flow.md).

## Azure DevOps–Specific Notes

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MICROSOFT_CLIENT_ID` | Application (client) ID from Microsoft Entra ID app registration | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `MICROSOFT_TENANT_ID` | Tenant ID (default: `common`) | `common` |
| `AZURE_DEVOPS_ORG` | Organization name | `myorg` |
| `AZURE_DEVOPS_PROJECT` | Default project name | `MyProject` |

### Scope

The Azure DevOps resource application ID is `499b84ac-1321-427f-aa17-267ca6975798`. When requesting only Azure DevOps access, use:

```
499b84ac-1321-427f-aa17-267ca6975798/.default
```

When the app registration also has Microsoft Graph permissions, use the merged scope from the shared auth file to authenticate once for both services.

### Bearer Token vs PAT Authentication

| Aspect | PAT (`-u ":$PAT"`) | Bearer (`-H "Authorization: Bearer $TOKEN"`) |
|--------|---------------------|-----------------------------------------------|
| Auth header | `Authorization: Basic <base64>` | `Authorization: Bearer <token>` |
| Token lifetime | Up to 1 year (configurable) | ~1 hour (auto-refreshable) |
| MFA support | No | Yes |
| Management | Manual creation in portal | Automatic via OAuth flow |
