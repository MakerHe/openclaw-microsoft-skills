# Dashboards

Service: `client.dashboards`

## Dashboards

```python
result = client.dashboards.list()
result = client.dashboards.get(dashboard_id)
result = client.dashboards.create("Sprint Dashboard", description="Sprint metrics")
result = client.dashboards.update(dashboard_id, updates={...})
client.dashboards.delete(dashboard_id)
```

## Widgets

```python
result = client.dashboards.list_widgets(dashboard_id)
result = client.dashboards.get_widget(dashboard_id, widget_id)
result = client.dashboards.create_widget(dashboard_id, widget={
    "name": "Burndown", "contributionId": "ms.vss-dashboards-web.burndownWidget",
})
result = client.dashboards.update_widget(dashboard_id, widget_id, widget={...})
client.dashboards.delete_widget(dashboard_id, widget_id)
```
