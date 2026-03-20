# Wiki API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki`

## Wikis

### List Wikis

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis?api-version=7.1"
```

### Get a Wiki

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}?api-version=7.1"
```

### Create a Project Wiki

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis?api-version=7.1" \
  -d '{
    "name": "my-wiki",
    "type": "projectWiki"
  }'
```

### Create a Code Wiki (from repo)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis?api-version=7.1" \
  -d '{
    "name": "code-wiki",
    "type": "codeWiki",
    "version": {"version": "main"},
    "repositoryId": "{repoId}",
    "mappedPath": "/docs"
  }'
```

## Pages

### Get a Page

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/pages?path=/Home&includeContent=true&api-version=7.1"
```

### Create or Update a Page

```bash
# Create (use If-Match: * for create-or-update, omit for create-only)
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT \
  -H "Content-Type: application/json" \
  -H "If-Match: *" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/pages?path=/NewPage&api-version=7.1" \
  -d '{"content": "# My Page\n\nPage content in markdown."}'
```

For updates, use the ETag from the GET response in the `If-Match` header.

### Delete a Page

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/pages?path=/OldPage&api-version=7.1"
```

### List Pages (Page Stats)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/pagesstats?api-version=7.1-preview.1"
```

## Page Moves

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/pagemoves?api-version=7.1" \
  -d '{
    "path": "/OldPath",
    "newPath": "/NewPath",
    "newOrder": 0
  }'
```

## Attachments

```bash
# Upload attachment
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT \
  -H "Content-Type: application/octet-stream" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/wiki/wikis/{wikiIdentifier}/attachments?name=image.png&api-version=7.1" \
  --data-binary @image.png
```
