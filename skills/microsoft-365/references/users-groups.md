# Users & Groups API

Base path: `https://graph.microsoft.com/v1.0`

Permissions: `User.Read`, `User.ReadBasic.All`, `Group.Read.All`

## Get My Profile

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me" | jq '{displayName, mail, userPrincipalName, jobTitle, department, officeLocation}'
```

## Get My Photo

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/photo/\$value" -o my-photo.jpg
```

## Get a User by ID or UPN

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/users/{user-id-or-upn}" | jq '{displayName, mail, jobTitle, department}'
```

## List Users

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/users?\$top=20&\$select=displayName,mail,userPrincipalName,jobTitle" | jq '.value[] | {displayName, mail}'
```

With filter:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/users?\$filter=startswith(displayName,'John')&\$select=displayName,mail"
```

Search by name:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "ConsistencyLevel: eventual" \
  "https://graph.microsoft.com/v1.0/users?\$search=%22displayName:John%22&\$count=true&\$select=displayName,mail"
```

## Get User's Manager

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/manager" | jq '{displayName, mail, jobTitle}'
```

## Get User's Direct Reports

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/directReports" | jq '.value[] | {displayName, mail, jobTitle}'
```

## List Groups

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/groups?\$top=20&\$select=displayName,description,groupTypes,mail" | jq '.value[] | {displayName, description, mail}'
```

With filter:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/groups?\$filter=startswith(displayName,'Engineering')"
```

## Get a Group

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/groups/{group-id}" | jq '{displayName, description, mail, groupTypes}'
```

## List Group Members

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/groups/{group-id}/members" | jq '.value[] | {displayName, mail, "@odata.type"}'
```

## List My Groups

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/memberOf" | jq '.value[] | {displayName, "@odata.type"}'
```

## Check Member Of

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/checkMemberGroups" \
  -d '{"groupIds": ["{group-id-1}", "{group-id-2}"]}'
```

## List Group Owners

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/groups/{group-id}/owners" | jq '.value[] | {displayName, mail}'
```

## Get Organization Info

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/organization" | jq '.value[] | {displayName, verifiedDomains}'
```
