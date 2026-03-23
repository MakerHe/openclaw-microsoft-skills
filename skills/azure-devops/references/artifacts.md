# Artifacts

Service: `client.artifacts`

## Feeds

```python
result = client.artifacts.list_feeds()
result = client.artifacts.list_feeds(project_scoped=True)
result = client.artifacts.get_feed(feed_id)
result = client.artifacts.create_feed("my-feed", description="Internal packages", upstream_enabled=True)
client.artifacts.delete_feed(feed_id)
```

## Packages

```python
result = client.artifacts.list_packages(feed_id)
result = client.artifacts.list_package_versions(feed_id, package_id)
```

## Protocol-Specific

```python
# NuGet
result = client.artifacts.get_nuget_version(feed_id, "Newtonsoft.Json", "13.0.1")
client.artifacts.delete_nuget_version(feed_id, "Newtonsoft.Json", "13.0.1")

# npm
result = client.artifacts.get_npm_version(feed_id, "@scope/package", "1.0.0")
client.artifacts.delete_npm_version(feed_id, "@scope/package", "1.0.0")

# Maven
result = client.artifacts.get_maven_version(feed_id, "com.example", "my-lib", "1.0.0")

# PyPI
result = client.artifacts.get_pypi_version(feed_id, "my-package", "1.0.0")

# Universal Packages
result = client.artifacts.list_upack_versions(feed_id, "my-upack")
```

## Views / Recycle Bin

```python
result = client.artifacts.list_views(feed_id)
result = client.artifacts.list_recycle_bin(feed_id)
```
