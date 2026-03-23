# Users & Groups

Service: `client.users_groups` — Permissions: `User.Read`, `User.ReadBasic.All`, `Group.Read.All`

## Current User

```python
result = client.users_groups.get_me()
data = client.users_groups.get_my_photo()  # -> bytes
```

## Users

```python
result = client.users_groups.get_user(user_id_or_upn)
result = client.users_groups.list_users(top=20, select="displayName,mail", filter="startswith(displayName,'John')", search="displayName:John")
```

## Org Hierarchy

```python
result = client.users_groups.get_manager()
result = client.users_groups.get_direct_reports()
```

## Groups

```python
result = client.users_groups.list_groups(top=20, filter="startswith(displayName,'Engineering')")
result = client.users_groups.get_group(group_id)
result = client.users_groups.list_group_members(group_id)
result = client.users_groups.list_group_owners(group_id)
```

## My Groups / Membership Check

```python
result = client.users_groups.list_my_groups()
result = client.users_groups.check_member_groups(group_ids=["group-id-1", "group-id-2"])
```

## Organization

```python
result = client.users_groups.get_organization()
```
