# Service Connections (Endpoints) API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint`

## List Service Endpoints

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints?api-version=7.1"
```

### Filter by Type

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints?type=azurerm&api-version=7.1"
```

Common types: `azurerm`, `github`, `dockerregistry`, `kubernetes`, `ssh`, `generic`, `externalnugetfeed`, `externalnpmregistry`.

## Get a Service Endpoint

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints/{endpointId}?api-version=7.1"
```

## Create a Service Endpoint

### Azure Resource Manager (Service Principal)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints?api-version=7.1" \
  -d '{
    "name": "Azure Production",
    "type": "azurerm",
    "url": "https://management.azure.com/",
    "authorization": {
      "scheme": "ServicePrincipal",
      "parameters": {
        "tenantid": "{tenantId}",
        "serviceprincipalid": "{clientId}",
        "authenticationType": "spnKey",
        "serviceprincipalkey": "{clientSecret}"
      }
    },
    "data": {
      "subscriptionId": "{subscriptionId}",
      "subscriptionName": "My Subscription",
      "environment": "AzureCloud",
      "scopeLevel": "Subscription",
      "creationMode": "Manual"
    },
    "isShared": false,
    "serviceEndpointProjectReferences": [{
      "projectReference": {"id": "{projectId}", "name": "'"$AZURE_DEVOPS_PROJECT"'"},
      "name": "Azure Production"
    }]
  }'
```

### GitHub

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints?api-version=7.1" \
  -d '{
    "name": "GitHub Connection",
    "type": "github",
    "url": "https://github.com",
    "authorization": {
      "scheme": "PersonalAccessToken",
      "parameters": {
        "accessToken": "{githubPat}"
      }
    },
    "serviceEndpointProjectReferences": [{
      "projectReference": {"id": "{projectId}", "name": "'"$AZURE_DEVOPS_PROJECT"'"},
      "name": "GitHub Connection"
    }]
  }'
```

### Generic (Username/Password)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints?api-version=7.1" \
  -d '{
    "name": "My Service",
    "type": "generic",
    "url": "https://my-service.example.com",
    "authorization": {
      "scheme": "UsernamePassword",
      "parameters": {
        "username": "user",
        "password": "pass"
      }
    },
    "serviceEndpointProjectReferences": [{
      "projectReference": {"id": "{projectId}", "name": "'"$AZURE_DEVOPS_PROJECT"'"},
      "name": "My Service"
    }]
  }'
```

## Update a Service Endpoint

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints/{endpointId}?api-version=7.1" \
  -d '{
    "id": "{endpointId}",
    "name": "Updated Name",
    "type": "generic",
    "url": "https://new-url.example.com",
    "authorization": {
      "scheme": "UsernamePassword",
      "parameters": {"username": "newuser", "password": "newpass"}
    },
    "serviceEndpointProjectReferences": [{
      "projectReference": {"id": "{projectId}", "name": "'"$AZURE_DEVOPS_PROJECT"'"},
      "name": "Updated Name"
    }]
  }'
```

## Delete a Service Endpoint

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints/{endpointId}?projectIds={projectId}&deep=true&api-version=7.1"
```

## Share an Endpoint with Another Project

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/serviceendpoint/endpoints/{endpointId}?api-version=7.1" \
  -d '[{
    "name": "Shared Connection",
    "projectReference": {"id": "{otherProjectId}", "name": "OtherProject"}
  }]'
```

## Execution History

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/serviceendpoint/endpoints/{endpointId}/executionhistory?api-version=7.1"
```
