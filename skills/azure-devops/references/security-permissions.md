# Security & Permissions

Service: `client.security`

## Namespaces

```python
result = client.security.list_namespaces()
result = client.security.get_namespace(namespace_id)
```

## ACLs / ACEs

```python
result = client.security.query_acls(namespace_id, token="security-token")
result = client.security.set_acl(namespace_id, acl={...})
result = client.security.set_ace(namespace_id, body={...})
client.security.remove_ace(namespace_id, token="security-token", descriptors="descriptor-string")
```

## Evaluate Permissions

```python
result = client.security.evaluate_permissions(evaluations=[
    {"securityNamespaceId": ns_id, "token": token, "permissions": 4},
])
```

## Identity Search

```python
result = client.security.search_identity("user@example.com", search_filter="General")
```
