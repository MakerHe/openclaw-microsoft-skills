# OneDrive API

Base path: `https://graph.microsoft.com/v1.0/me/drive`

Permissions: `Files.ReadWrite.All`

## List Files in Root

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/root/children" | jq '.value[] | {name, size, folder: .folder.childCount, lastModifiedDateTime}'
```

## List Files in a Folder

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/root:/{folder-path}:/children" | jq '.value[] | {name, size}'
```

By item ID:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/children"
```

## Get File Metadata

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/root:/{file-path}:" | jq '{name, size, webUrl, lastModifiedDateTime}'
```

By item ID:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}"
```

## Download a File

```bash
curl -s -L -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/root:/{file-path}:/content" -o output-file
```

By item ID:

```bash
curl -s -L -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/content" -o output-file
```

## Upload a Small File (< 4 MB)

```bash
curl -s -X PUT -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  "https://graph.microsoft.com/v1.0/me/drive/root:/{file-path}:/content" \
  --data-binary @local-file
```

## Upload a Large File (> 4 MB) — Create Upload Session

```bash
# Step 1: Create upload session
UPLOAD_URL=$(curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/drive/root:/{file-path}:/createUploadSession" \
  -d '{"item": {"@microsoft.graph.conflictBehavior": "rename"}}' | jq -r '.uploadUrl')

# Step 2: Upload bytes in chunks (e.g., 10 MB chunks)
FILE_SIZE=$(stat -f%z local-file)
curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Range: bytes 0-$((FILE_SIZE-1))/$FILE_SIZE" \
  --data-binary @local-file
```

## Create a Folder

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/drive/root/children" \
  -d '{
    "name": "New Folder",
    "folder": {},
    "@microsoft.graph.conflictBehavior": "rename"
  }'
```

## Delete a File or Folder

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}"
```

## Move/Rename a File

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}" \
  -d '{
    "name": "new-name.txt",
    "parentReference": {"id": "{destination-folder-id}"}
  }'
```

## Copy a File

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/copy" \
  -d '{
    "parentReference": {"id": "{destination-folder-id}"},
    "name": "copy-of-file.txt"
  }'
```

## Create a Sharing Link

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/createLink" \
  -d '{
    "type": "view",
    "scope": "organization"
  }' | jq '.link.webUrl'
```

Link types: `view`, `edit`, `embed`. Scopes: `anonymous`, `organization`.

## Search Files

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/root/search(q='keyword')" | jq '.value[] | {name, webUrl}'
```

## Get Drive Info

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive" | jq '{driveType, quota: {used: .quota.used, total: .quota.total, remaining: .quota.remaining}}'
```

## List Recent Files

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/recent" | jq '.value[] | {name, lastModifiedDateTime}'
```

## List Shared with Me

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/drive/sharedWithMe" | jq '.value[] | {name, remoteItem: .remoteItem.webUrl}'
```
