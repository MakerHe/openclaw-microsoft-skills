# Graph & Identity

Service: `client.graph_identity`

## Users

```python
result = client.graph_identity.list_users()
result = client.graph_identity.get_user(user_descriptor)
result = client.graph_identity.create_user("user@example.com", origin_id="aad-object-id")
client.graph_identity.delete_user(user_descriptor)
```

## Groups

```python
result = client.graph_identity.list_groups()
result = client.graph_identity.get_group(group_descriptor)
result = client.graph_identity.create_group(display_name="My Group", description="Group description")
client.graph_identity.delete_group(group_descriptor)
```

## Memberships

```python
result = client.graph_identity.list_memberships(subject_descriptor, direction="Down")
result = client.graph_identity.add_membership(subject_descriptor, container_descriptor)
client.graph_identity.remove_membership(subject_descriptor, container_descriptor)
```

## Descriptors / Lookup

```python
result = client.graph_identity.get_descriptor(storage_key)
result = client.graph_identity.get_scope_descriptor(project_id)
result = client.graph_identity.lookup_subjects(descriptors=["desc1", "desc2"])
result = client.graph_identity.search_identity("user@example.com", search_filter="General")
```
