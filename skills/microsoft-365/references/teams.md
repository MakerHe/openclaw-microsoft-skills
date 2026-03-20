# Teams API

Base path: `https://graph.microsoft.com/v1.0`

Permissions: `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Send`, `ChatMessage.Send`

## List Joined Teams

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/joinedTeams" | jq '.value[] | {id, displayName, description}'
```

## Get a Team

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}" | jq '{displayName, description, isArchived}'
```

## List Channels

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels" | jq '.value[] | {id, displayName, membershipType}'
```

## Get a Channel

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}"
```

## Create a Channel

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels" \
  -d '{
    "displayName": "New Channel",
    "description": "Channel description",
    "membershipType": "standard"
  }'
```

Membership types: `standard`, `private`, `shared`.

## Send a Channel Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages" \
  -d '{
    "body": {
      "content": "Hello from Graph API!"
    }
  }'
```

With HTML content:

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages" \
  -d '{
    "body": {
      "contentType": "html",
      "content": "<h1>Title</h1><p>Rich content here</p>"
    }
  }'
```

## Reply to a Channel Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages/{message-id}/replies" \
  -d '{
    "body": {
      "content": "This is a reply"
    }
  }'
```

## List Channel Messages

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages?\$top=20" | jq '.value[] | {id, from: .from.user.displayName, body: .body.content, createdDateTime}'
```

## List Team Members

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/members" | jq '.value[] | {displayName, roles, email: .email}'
```

## Add a Team Member

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/teams/{team-id}/members" \
  -d '{
    "@odata.type": "#microsoft.graph.aadUserConversationMember",
    "roles": ["member"],
    "user@odata.bind": "https://graph.microsoft.com/v1.0/users/{user-id}"
  }'
```

## List Chats

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/chats" | jq '.value[] | {id, topic, chatType}'
```

## Send a Chat Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/chats/{chat-id}/messages" \
  -d '{
    "body": {
      "content": "Hello in chat!"
    }
  }'
```

## List Chat Messages

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/chats/{chat-id}/messages?\$top=20" | jq '.value[] | {from: .from.user.displayName, body: .body.content, createdDateTime}'
```
