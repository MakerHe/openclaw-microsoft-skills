# Service Endpoints

Service: `client.service_endpoints`

## List / Get

```python
result = client.service_endpoints.list()
result = client.service_endpoints.list(endpoint_type="azurerm")
result = client.service_endpoints.get(endpoint_id)
```

## Create / Update / Delete

```python
result = client.service_endpoints.create(endpoint={
    "name": "My Azure Connection",
    "type": "azurerm",
    "url": "https://management.azure.com/",
    "authorization": {...},
})
result = client.service_endpoints.update(endpoint_id, endpoint={...})
client.service_endpoints.delete(endpoint_id, project_ids="project-guid", deep=True)
```

## Share / History

```python
result = client.service_endpoints.share(endpoint_id, references=[{"projectReference": {"id": "project-guid"}, "name": "My Connection"}])
result = client.service_endpoints.execution_history(endpoint_id)
```
