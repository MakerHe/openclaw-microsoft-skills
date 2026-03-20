# OneNote API

Base path: `https://graph.microsoft.com/v1.0/me/onenote`

Permissions: `Notes.ReadWrite.All`

## List Notebooks

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks" | jq '.value[] | {id, displayName, createdDateTime, lastModifiedDateTime}'
```

## Get a Notebook

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook-id}"
```

## Create a Notebook

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks" \
  -d '{"displayName": "My New Notebook"}'
```

## List Sections

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook-id}/sections" | jq '.value[] | {id, displayName}'
```

List all sections across notebooks:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/sections" | jq '.value[] | {id, displayName, parentNotebook: .parentNotebook.displayName}'
```

## Create a Section

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook-id}/sections" \
  -d '{"displayName": "New Section"}'
```

## List Pages in a Section

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/sections/{section-id}/pages" | jq '.value[] | {id, title, createdDateTime}'
```

List all pages:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/pages?\$top=20&\$orderby=lastModifiedDateTime%20desc" | jq '.value[] | {id, title}'
```

## Get Page Content

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/pages/{page-id}/content"
```

This returns HTML content of the page.

## Create a Page

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: text/html" \
  "https://graph.microsoft.com/v1.0/me/onenote/sections/{section-id}/pages" \
  -d '<!DOCTYPE html>
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <p>Page content goes here.</p>
  </body>
</html>'
```

## Update Page Content

OneNote pages are updated with PATCH using JSON commands:

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/onenote/pages/{page-id}/content" \
  -d '[
    {
      "target": "body",
      "action": "append",
      "content": "<p>Appended content</p>"
    }
  ]'
```

Actions: `append`, `insert`, `prepend`, `replace`.

## Delete a Page

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/pages/{page-id}"
```

## Copy a Page to a Section

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/onenote/pages/{page-id}/copyToSection" \
  -d '{"id": "{destination-section-id}"}'
```

## List Section Groups

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook-id}/sectionGroups" | jq '.value[] | {id, displayName}'
```
