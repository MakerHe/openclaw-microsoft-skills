# Contacts

Service: `client.contacts` — Permissions: `Contacts.ReadWrite`

## List / Get / Delete

```python
result = client.contacts.list(top=20, select="displayName,emailAddresses", filter="startswith(displayName,'John')")
result = client.contacts.get(contact_id)
result = client.contacts.delete(contact_id)
```

## Create a Contact

```python
result = client.contacts.create(
    given_name="John",
    surname="Doe",
    email="john.doe@example.com",
    phone="+1-555-0100",
    company="Contoso",
    job_title="Engineer",
)
```

## Update a Contact

```python
result = client.contacts.update(contact_id, updates={"jobTitle": "Senior Engineer"})
```

## Contact Photo

```python
data = client.contacts.get_photo(contact_id)  # -> bytes
```

## Contact Folders

```python
result = client.contacts.list_folders()
result = client.contacts.create_folder("Vendors")
result = client.contacts.list_in_folder(folder_id)
result = client.contacts.create_in_folder(folder_id, contact={
    "givenName": "Jane", "surname": "Smith",
    "emailAddresses": [{"address": "jane@vendor.com"}],
})
result = client.contacts.delete_folder(folder_id)
```
