# Service Hooks

Service: `client.service_hooks`

## Subscriptions

```python
result = client.service_hooks.list_subscriptions()
result = client.service_hooks.get_subscription(subscription_id)
result = client.service_hooks.create_subscription(
    publisher_id="tfs", event_type="workitem.created",
    consumer_id="webHooks", consumer_action_id="httpRequest",
    consumer_inputs={"url": "https://example.com/webhook"},
    publisher_inputs={"projectId": project_id},
)
result = client.service_hooks.update_subscription(subscription_id, body={...})
client.service_hooks.delete_subscription(subscription_id)
```

## Publishers / Consumers

```python
result = client.service_hooks.list_publishers()
result = client.service_hooks.list_consumers()
```

## Test / Notifications

```python
result = client.service_hooks.test_notification(subscription_id)
result = client.service_hooks.list_notifications(subscription_id)
```
