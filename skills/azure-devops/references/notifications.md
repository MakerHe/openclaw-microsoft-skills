# Notifications

Service: `client.notifications`

## Subscriptions

```python
result = client.notifications.list_subscriptions()
result = client.notifications.get_subscription(subscription_id)
result = client.notifications.create_subscription(body={...})
result = client.notifications.update_subscription(subscription_id, body={...})
client.notifications.delete_subscription(subscription_id)
```

## Event Types / Diagnostics

```python
result = client.notifications.list_event_types()
result = client.notifications.get_diagnostics(subscription_id)
```

## Settings / Subscribers

```python
result = client.notifications.get_settings()
result = client.notifications.get_subscriber(subscriber_id)
result = client.notifications.update_subscriber(subscriber_id, updates={...})
```
