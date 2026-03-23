# SharePoint

Service: `client.sharepoint` — Permissions: `Sites.ReadWrite.All`

## Sites

```python
result = client.sharepoint.search_sites("keyword")
result = client.sharepoint.get_root_site()
result = client.sharepoint.get_site_by_path("contoso.sharepoint.com", "sites/team-site")
result = client.sharepoint.get_site(site_id)
result = client.sharepoint.list_subsites(site_id)
result = client.sharepoint.list_followed_sites()
```

## Lists

```python
result = client.sharepoint.list_lists(site_id)
result = client.sharepoint.get_list(site_id, list_id)
result = client.sharepoint.create_list(site_id, list_def={
    "displayName": "Project Tasks",
    "list": {"template": "genericList"},
    "columns": [
        {"name": "Status", "choice": {"choices": ["Not Started", "In Progress", "Done"]}},
    ],
})
result = client.sharepoint.delete_list(site_id, list_id)
result = client.sharepoint.list_columns(site_id, list_id)
```

## List Items

```python
result = client.sharepoint.list_items(
    site_id, list_id, top=50,
    select="Title,Status", filter="fields/Status eq 'In Progress'",
    expand="fields", order_by="fields/Title",
)
result = client.sharepoint.get_item(site_id, list_id, item_id)
result = client.sharepoint.create_item(site_id, list_id, fields={"Title": "New Task", "Status": "Not Started"})
result = client.sharepoint.update_item(site_id, list_id, item_id, fields={"Status": "Done"})
result = client.sharepoint.delete_item(site_id, list_id, item_id)
```

## Site Drive (Document Library)

```python
result = client.sharepoint.get_drive(site_id)
result = client.sharepoint.list_drive_root(site_id)
```
