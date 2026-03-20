# Contacts API

Base path: `https://graph.microsoft.com/v1.0/me`

Permissions: `Contacts.ReadWrite`

## List Contacts

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts?\$top=20" | jq '.value[] | {id, displayName, emailAddresses: [.emailAddresses[].address], mobilePhone}'
```

With select:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts?\$select=displayName,emailAddresses,businessPhones,companyName&\$top=20"
```

With search:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts?\$filter=startswith(displayName,'John')"
```

## Get a Contact

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts/{contact-id}"
```

## Create a Contact

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/contacts" \
  -d '{
    "givenName": "John",
    "surname": "Doe",
    "emailAddresses": [
      {"address": "john.doe@example.com", "name": "John Doe"}
    ],
    "businessPhones": ["+1-555-0100"],
    "mobilePhone": "+1-555-0101",
    "companyName": "Contoso",
    "jobTitle": "Engineer"
  }'
```

## Update a Contact

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/contacts/{contact-id}" \
  -d '{
    "jobTitle": "Senior Engineer",
    "companyName": "Contoso Ltd"
  }'
```

## Delete a Contact

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts/{contact-id}"
```

## Get Contact Photo

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contacts/{contact-id}/photo/\$value" -o contact-photo.jpg
```

## List Contact Folders

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contactFolders" | jq '.value[] | {id, displayName}'
```

## Create a Contact Folder

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/contactFolders" \
  -d '{"displayName": "Vendors"}'
```

## List Contacts in a Folder

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contactFolders/{folder-id}/contacts" | jq '.value[] | {displayName, emailAddresses}'
```

## Create a Contact in a Folder

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/contactFolders/{folder-id}/contacts" \
  -d '{
    "givenName": "Jane",
    "surname": "Smith",
    "emailAddresses": [{"address": "jane@vendor.com"}]
  }'
```

## Delete a Contact Folder

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/contactFolders/{folder-id}"
```
