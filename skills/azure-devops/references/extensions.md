# Extensions

Service: `client.extensions`

## Installed Extensions

```python
result = client.extensions.list_installed()
result = client.extensions.get(publisher_name, extension_name)
```

## Install / Uninstall / Enable

```python
result = client.extensions.install(publisher_name, extension_name, version)
client.extensions.uninstall(publisher_name, extension_name)
result = client.extensions.set_enabled(publisher_name, extension_name, enabled=True)
```

## Extension Data

```python
result = client.extensions.get_data_document(publisher_name, extension_name, scope_type, scope_value, collection)
result = client.extensions.set_data_document(publisher_name, extension_name, scope_type, scope_value, collection, document)
```

## Extension Requests

```python
result = client.extensions.list_requests()
```
