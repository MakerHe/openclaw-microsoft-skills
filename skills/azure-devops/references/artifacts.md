# Azure Artifacts / Package Management API

Base: `https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG` (organization-scoped) or `https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT` (project-scoped)

**Note**: Artifacts uses the `feeds.dev.azure.com` host.

## Feeds

### List Feeds

```bash
# Organization-scoped
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds?api-version=7.1"

# Project-scoped
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/packaging/feeds?api-version=7.1"
```

### Get a Feed

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}?api-version=7.1"
```

### Create a Feed

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds?api-version=7.1" \
  -d '{
    "name": "my-feed",
    "description": "My package feed",
    "hideDeletedPackageVersions": true,
    "upstreamEnabled": true
  }'
```

### Delete a Feed

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}?api-version=7.1"
```

## Packages

### List Packages in a Feed

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/packages?api-version=7.1"
```

### Get Package Versions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/packages/{packageId}/versions?api-version=7.1"
```

## NuGet

### Get NuGet Package Version

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/nuget/packages/{packageName}/versions/{version}?api-version=7.1"
```

### Delete NuGet Package Version

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/nuget/packages/{packageName}/versions/{version}?api-version=7.1"
```

## npm

### Get npm Package Version

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/npm/{packageName}/versions/{version}?api-version=7.1"
```

### Unpublish npm Package

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/npm/{packageName}/versions/{version}?api-version=7.1"
```

## Maven

### Get Maven Package Version

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/maven/{groupId}/{artifactId}/versions/{version}?api-version=7.1"
```

## Python (PyPI)

### Get Python Package Version

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/pypi/packages/{packageName}/versions/{version}?api-version=7.1"
```

## Universal Packages

### List Versions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/upack/packages/{packageName}/versions?api-version=7.1"
```

## Feed Views (Promote)

```bash
# List views
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/views?api-version=7.1"

# Promote a NuGet package to a view
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/nuget/packages/{packageName}/versions/{version}?api-version=7.1" \
  -d '{"views": {"op": "add", "path": "/views/-", "value": "{viewId}"}}'
```

## Recycle Bin

```bash
# List deleted packages
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://feeds.dev.azure.com/$AZURE_DEVOPS_ORG/_apis/packaging/feeds/{feedId}/recyclebin/packages?api-version=7.1"
```
