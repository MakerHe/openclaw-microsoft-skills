"""Outlook Mail service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me"


class Mail(BaseService):
    """Microsoft Graph Mail API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    def list_messages(
        self,
        *,
        top: int = 10,
        filter: str | None = None,
        select: list[str] | None = None,
        search: str | None = None,
        order_by: str = "receivedDateTime desc",
    ) -> dict:
        params: dict[str, str] = {"$top": str(top), "$orderby": order_by}
        if filter:
            params["$filter"] = filter
        if select:
            params["$select"] = ",".join(select)
        if search:
            params["$search"] = f'"{search}"'
        return self._get(f"{BASE}/messages", params=params)

    def get_message(self, message_id: str) -> dict:
        return self._get(f"{BASE}/messages/{message_id}")

    def send(
        self,
        to: str | list[str],
        *,
        subject: str,
        body: str,
        body_type: str = "Text",
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        save_to_sent: bool = True,
    ) -> None:
        recipients = [to] if isinstance(to, str) else to
        msg: dict[str, Any] = {
            "subject": subject,
            "body": {"contentType": body_type, "content": body},
            "toRecipients": [{"emailAddress": {"address": r}} for r in recipients],
        }
        if cc:
            msg["ccRecipients"] = [{"emailAddress": {"address": r}} for r in cc]
        if bcc:
            msg["bccRecipients"] = [{"emailAddress": {"address": r}} for r in bcc]
        self._post(f"{BASE}/sendMail", json={"message": msg, "saveToSentItems": save_to_sent})

    def create_draft(
        self,
        to: str | list[str],
        *,
        subject: str,
        body: str,
        body_type: str = "Text",
    ) -> dict:
        recipients = [to] if isinstance(to, str) else to
        return self._post(
            f"{BASE}/messages",
            json={
                "subject": subject,
                "body": {"contentType": body_type, "content": body},
                "toRecipients": [{"emailAddress": {"address": r}} for r in recipients],
            },
        )

    def send_draft(self, message_id: str) -> None:
        self._post(f"{BASE}/messages/{message_id}/send")

    def reply(self, message_id: str, comment: str) -> None:
        self._post(f"{BASE}/messages/{message_id}/reply", json={"comment": comment})

    def reply_all(self, message_id: str, comment: str) -> None:
        self._post(f"{BASE}/messages/{message_id}/replyAll", json={"comment": comment})

    def forward(self, message_id: str, to: str | list[str], *, comment: str = "") -> None:
        recipients = [to] if isinstance(to, str) else to
        self._post(
            f"{BASE}/messages/{message_id}/forward",
            json={
                "comment": comment,
                "toRecipients": [{"emailAddress": {"address": r}} for r in recipients],
            },
        )

    def delete(self, message_id: str) -> None:
        self._delete(f"{BASE}/messages/{message_id}")

    def mark_read(self, message_id: str, *, is_read: bool = True) -> dict:
        return self._patch(f"{BASE}/messages/{message_id}", json={"isRead": is_read})

    def move(self, message_id: str, destination: str) -> dict:
        return self._post(
            f"{BASE}/messages/{message_id}/move", json={"destinationId": destination}
        )

    def list_folders(self) -> dict:
        return self._get(f"{BASE}/mailFolders")

    def get_folder_messages(self, folder_id: str, *, top: int = 10) -> dict:
        return self._get(f"{BASE}/mailFolders/{folder_id}/messages", params={"$top": str(top)})

    def create_folder(self, display_name: str) -> dict:
        return self._post(f"{BASE}/mailFolders", json={"displayName": display_name})

    def list_attachments(self, message_id: str) -> dict:
        return self._get(f"{BASE}/messages/{message_id}/attachments")

    def get_attachment(self, message_id: str, attachment_id: str) -> dict:
        return self._get(f"{BASE}/messages/{message_id}/attachments/{attachment_id}")

    def add_attachment(
        self, message_id: str, name: str, content_bytes: str
    ) -> dict:
        return self._post(
            f"{BASE}/messages/{message_id}/attachments",
            json={
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": name,
                "contentBytes": content_bytes,
            },
        )
