# OneNote

Service: `client.onenote` — Permissions: `Notes.ReadWrite.All`

## Notebooks

```python
result = client.onenote.list_notebooks()
result = client.onenote.get_notebook(notebook_id)
result = client.onenote.create_notebook("My Notebook")
```

## Sections

```python
result = client.onenote.list_sections(notebook_id)
result = client.onenote.list_all_sections()
result = client.onenote.create_section(notebook_id, "New Section")
```

## Pages

```python
result = client.onenote.list_pages(section_id)
result = client.onenote.list_all_pages(top=20)
html = client.onenote.get_page_content(page_id)  # -> str (HTML)
```

## Create a Page

```python
result = client.onenote.create_page(section_id, html_content="""
<!DOCTYPE html>
<html><head><title>Page Title</title></head>
<body><p>Content here.</p></body></html>
""")
```

## Update / Delete / Copy

```python
result = client.onenote.update_page(page_id, commands=[
    {"target": "body", "action": "append", "content": "<p>Appended</p>"}
])
result = client.onenote.delete_page(page_id)
result = client.onenote.copy_page_to_section(page_id, destination_section_id)
```

Actions for `update_page`: `append`, `insert`, `prepend`, `replace`.

## Section Groups

```python
result = client.onenote.list_section_groups(notebook_id)
```
