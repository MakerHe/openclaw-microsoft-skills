# Wiki

Service: `client.wiki`

## Wikis

```python
result = client.wiki.list_wikis()
result = client.wiki.get_wiki(wiki_id)
result = client.wiki.create_project_wiki("Project Wiki")
result = client.wiki.create_code_wiki(name="Code Wiki", repo_id="repo-guid", branch="main", mapped_path="/docs")
```

## Pages

```python
result = client.wiki.get_page(wiki_id, path="/Home", include_content=True)
result = client.wiki.create_or_update_page(wiki_id, path="/New Page", content="# Hello\nPage content here.")
client.wiki.delete_page(wiki_id, path="/Old Page")
```

## Move / Stats / Attachments

```python
result = client.wiki.move_page(wiki_id, path="/Old Path", new_path="/New Path")
result = client.wiki.list_page_stats(wiki_id)
result = client.wiki.upload_attachment(wiki_id, name="image.png", content=image_bytes)
```
