# Extensions Management API

Base: `https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement`

**Note**: Extension Management uses the `extmgmt.dev.azure.com` host.

## List Installed Extensions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensions?api-version=7.1-preview.1"
```

## Get an Installed Extension

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensionsbyname/{publisherName}/{extensionName}?api-version=7.1-preview.1"
```

## Install an Extension

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensionsbyname/{publisherName}/{extensionName}/{version}?api-version=7.1-preview.1"
```

## Uninstall an Extension

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensionsbyname/{publisherName}/{extensionName}?api-version=7.1-preview.1"
```

## Enable/Disable an Extension

```bash
# Disable
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensionsbyname/{publisherName}/{extensionName}?api-version=7.1-preview.1" \
  -d '{"installState": {"flags": "disabled"}}'

# Enable
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/installedextensionsbyname/{publisherName}/{extensionName}?api-version=7.1-preview.1" \
  -d '{"installState": {"flags": "none"}}'
```

## Extension Data (Storage)

Extensions can store data in the organization:

```bash
# Get document
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/ExtensionManagement/InstalledExtensions/{publisherName}/{extensionName}/Data/Scopes/Default/Current/Collections/{collectionName}/Documents/{documentId}?api-version=7.1-preview.1"

# Create/update document
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/ExtensionManagement/InstalledExtensions/{publisherName}/{extensionName}/Data/Scopes/Default/Current/Collections/{collectionName}/Documents?api-version=7.1-preview.1" \
  -d '{"id": "doc1", "key": "value"}'
```

## Requests (Pending Installs)

```bash
# List extension requests
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://extmgmt.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/extensionmanagement/requests?api-version=7.1-preview.1"
```
