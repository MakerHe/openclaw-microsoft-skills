# Teams

Service: `client.teams` — Permissions: `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Send`, `ChatMessage.Send`

## Teams

```python
result = client.teams.list_joined_teams()
result = client.teams.get_team(team_id)
```

## Channels

```python
result = client.teams.list_channels(team_id)
result = client.teams.get_channel(team_id, channel_id)
result = client.teams.create_channel(
    team_id, display_name="New Channel",
    description="Channel description", membership_type="standard",
)
```

Membership types: `standard`, `private`, `shared`.

## Channel Messages

```python
result = client.teams.send_channel_message(team_id, channel_id, content="Hello!", content_type="html")
result = client.teams.reply_to_channel_message(team_id, channel_id, message_id, content="Reply")
result = client.teams.list_channel_messages(team_id, channel_id, top=20)
```

## Members

```python
result = client.teams.list_members(team_id)
result = client.teams.add_member(team_id, user_id, roles=["member"])
```

## Chats

```python
result = client.teams.list_chats()
result = client.teams.send_chat_message(chat_id, content="Hello in chat!")
result = client.teams.list_chat_messages(chat_id, top=20)
```
