# OneDrive

Service: `client.onedrive` — Permissions: `Files.ReadWrite.All`

## List Files

```python
result = client.onedrive.list_root()
result = client.onedrive.list_folder("Documents/Reports")
result = client.onedrive.list_folder_by_id(item_id)
```

## Get Metadata

```python
result = client.onedrive.get_metadata("Documents/report.docx")
result = client.onedrive.get_metadata_by_id(item_id)
```

## Download

```python
data = client.onedrive.download("Documents/report.docx")  # -> bytes
data = client.onedrive.download_by_id(item_id)             # -> bytes
```

## Upload

```python
result = client.onedrive.upload("Documents/report.docx", data=file_bytes)

# Large files (> 4 MB) — create an upload session
session = client.onedrive.create_upload_session("Documents/large-file.zip")
```

## Create a Folder

```python
result = client.onedrive.create_folder(parent_path="Documents", name="New Folder")
```

## Delete

```python
result = client.onedrive.delete(item_id)
```

## Move / Rename / Copy

```python
result = client.onedrive.move_or_rename(item_id, new_name="renamed.txt", parent_id=dest_folder_id)
result = client.onedrive.copy(item_id, destination_folder_id=dest_folder_id, name="copy.txt")
```

## Sharing Link

```python
result = client.onedrive.create_sharing_link(item_id, link_type="view", scope="anonymous")
```

Link types: `view`, `edit`, `embed`. Scopes: `anonymous`, `organization`.

## Search / Recent / Shared

```python
result = client.onedrive.search("keyword")
result = client.onedrive.list_recent()
result = client.onedrive.list_shared_with_me()
```

## Drive Info

```python
result = client.onedrive.get_drive_info()
```
