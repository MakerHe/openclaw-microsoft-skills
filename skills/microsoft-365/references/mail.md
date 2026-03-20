# Outlook Mail API

Base path: `https://graph.microsoft.com/v1.0/me`

Permissions: `Mail.Read`, `Mail.Send`, `Mail.ReadWrite`

## List Messages

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages?\$top=10&\$orderby=receivedDateTime%20desc" | jq '.value[] | {subject, from: .from.emailAddress.address, receivedDateTime}'
```

With filter (unread only):

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages?\$filter=isRead%20eq%20false&\$top=10" | jq '.value[] | {subject, from: .from.emailAddress.address}'
```

With select (specific fields):

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages?\$select=subject,from,receivedDateTime,isRead&\$top=10"
```

With search:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages?\$search=%22keyword%22&\$top=10"
```

## Get a Message

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}" | jq '{subject, from: .from.emailAddress, body: .body.content}'
```

## Send a Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/sendMail" \
  -d '{
    "message": {
      "subject": "Hello",
      "body": {
        "contentType": "Text",
        "content": "Hello from Microsoft Graph API"
      },
      "toRecipients": [
        {"emailAddress": {"address": "recipient@example.com"}}
      ]
    },
    "saveToSentItems": true
  }'
```

With CC and BCC:

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/sendMail" \
  -d '{
    "message": {
      "subject": "Hello",
      "body": {"contentType": "HTML", "content": "<h1>Hello</h1><p>HTML content</p>"},
      "toRecipients": [{"emailAddress": {"address": "to@example.com"}}],
      "ccRecipients": [{"emailAddress": {"address": "cc@example.com"}}],
      "bccRecipients": [{"emailAddress": {"address": "bcc@example.com"}}]
    }
  }'
```

## Create Draft Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages" \
  -d '{
    "subject": "Draft subject",
    "body": {"contentType": "Text", "content": "Draft body"},
    "toRecipients": [{"emailAddress": {"address": "recipient@example.com"}}]
  }' | jq '{id, subject}'
```

## Send a Draft

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/send"
```

## Reply to a Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/reply" \
  -d '{
    "comment": "Thanks for your message!"
  }'
```

## Reply All

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/replyAll" \
  -d '{
    "comment": "Reply to all recipients"
  }'
```

## Forward a Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/forward" \
  -d '{
    "comment": "FYI",
    "toRecipients": [{"emailAddress": {"address": "forward-to@example.com"}}]
  }'
```

## Delete a Message

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}"
```

## Mark as Read/Unread

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}" \
  -d '{"isRead": true}'
```

## Move a Message

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/move" \
  -d '{"destinationId": "archive"}'
```

Well-known folder names: `inbox`, `drafts`, `sentitems`, `deleteditems`, `archive`, `junkemail`.

## List Mail Folders

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/mailFolders" | jq '.value[] | {id, displayName, totalItemCount, unreadItemCount}'
```

## Get Messages in a Folder

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/mailFolders/{folder-id}/messages?\$top=10"
```

## Create a Mail Folder

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/mailFolders" \
  -d '{"displayName": "My Custom Folder"}'
```

## List Attachments

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/attachments" | jq '.value[] | {name, contentType, size}'
```

## Get an Attachment

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/attachments/{attachment-id}"
```

## Add an Attachment to a Draft

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/messages/{message-id}/attachments" \
  -d '{
    "@odata.type": "#microsoft.graph.fileAttachment",
    "name": "file.txt",
    "contentBytes": "'$(base64 < file.txt)'"
  }'
```
