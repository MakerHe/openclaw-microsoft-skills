# Search

Service: `client.search`

## Code Search

```python
result = client.search.code(
    search_text="def authenticate",
    top=25, skip=0,
    filters={"Repository": ["my-repo"], "Path": ["/src"]},
)
```

## Work Item Search

```python
result = client.search.work_items(
    search_text="login bug",
    top=25, skip=0,
    filters={"Work Item Type": ["Bug"], "State": ["Active"]},
)
```

## Wiki Search

```python
result = client.search.wiki(
    search_text="deployment guide",
    top=25, skip=0,
)
```
