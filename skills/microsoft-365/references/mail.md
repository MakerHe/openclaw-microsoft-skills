# Outlook Mail

Service: `client.mail` — Permissions: `Mail.Read`, `Mail.Send`, `Mail.ReadWrite`

## List Messages

```python
result = client.mail.list_messages(top=10, order_by="receivedDateTime desc")
result = client.mail.list_messages(filter="isRead eq false", top=10)
result = client.mail.list_messages(select="subject,from,receivedDateTime", top=10)
result = client.mail.list_messages(search="keyword", top=10)
```

## Get a Message

```python
result = client.mail.get_message(message_id)
```

## Send a Message

```python
result = client.mail.send(
    to="recipient@example.com",
    subject="Hello",
    body="Hello from the SDK",
    body_type="Text",
    save_to_sent=True,
)

# With CC and BCC
result = client.mail.send(
    to="to@example.com",
    subject="Hello",
    body="<h1>Hello</h1>",
    body_type="HTML",
    cc="cc@example.com",
    bcc="bcc@example.com",
)
```

## Drafts

```python
result = client.mail.create_draft(to="recipient@example.com", subject="Draft", body="Draft body")
result = client.mail.send_draft(message_id)
```

## Reply / Reply All / Forward

```python
result = client.mail.reply(message_id, comment="Thanks!")
result = client.mail.reply_all(message_id, comment="Reply to all")
result = client.mail.forward(message_id, to="forward-to@example.com", comment="FYI")
```

## Delete / Mark Read / Move

```python
result = client.mail.delete(message_id)
result = client.mail.mark_read(message_id, is_read=True)
result = client.mail.move(message_id, destination="archive")
```

Well-known destinations: `inbox`, `drafts`, `sentitems`, `deleteditems`, `archive`, `junkemail`.

## Folders

```python
result = client.mail.list_folders()
result = client.mail.get_folder_messages(folder_id, top=10)
result = client.mail.create_folder("My Custom Folder")
```

## Attachments

```python
result = client.mail.list_attachments(message_id)
result = client.mail.get_attachment(message_id, attachment_id)
result = client.mail.add_attachment(message_id, name="file.txt", content_bytes=b"...")
```
