"""Teams service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0"


class Teams(BaseService):
    """Microsoft Graph Teams API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    def list_joined_teams(self) -> dict:
        return self._get(f"{BASE}/me/joinedTeams")

    def get_team(self, team_id: str) -> dict:
        return self._get(f"{BASE}/teams/{team_id}")

    def list_channels(self, team_id: str) -> dict:
        return self._get(f"{BASE}/teams/{team_id}/channels")

    def get_channel(self, team_id: str, channel_id: str) -> dict:
        return self._get(f"{BASE}/teams/{team_id}/channels/{channel_id}")

    def create_channel(
        self,
        team_id: str,
        display_name: str,
        *,
        description: str = "",
        membership_type: str = "standard",
    ) -> dict:
        return self._post(
            f"{BASE}/teams/{team_id}/channels",
            json={
                "displayName": display_name,
                "description": description,
                "membershipType": membership_type,
            },
        )

    def send_channel_message(
        self,
        team_id: str,
        channel_id: str,
        content: str,
        *,
        content_type: str = "text",
    ) -> dict:
        return self._post(
            f"{BASE}/teams/{team_id}/channels/{channel_id}/messages",
            json={"body": {"contentType": content_type, "content": content}},
        )

    def reply_to_channel_message(
        self, team_id: str, channel_id: str, message_id: str, content: str
    ) -> dict:
        return self._post(
            f"{BASE}/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies",
            json={"body": {"content": content}},
        )

    def list_channel_messages(self, team_id: str, channel_id: str, *, top: int = 20) -> dict:
        return self._get(
            f"{BASE}/teams/{team_id}/channels/{channel_id}/messages",
            params={"$top": str(top)},
        )

    def list_members(self, team_id: str) -> dict:
        return self._get(f"{BASE}/teams/{team_id}/members")

    def add_member(self, team_id: str, user_id: str, *, roles: list[str] | None = None) -> dict:
        return self._post(
            f"{BASE}/teams/{team_id}/members",
            json={
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": roles or ["member"],
                "user@odata.bind": f"{BASE}/users/{user_id}",
            },
        )

    # -- Chats ------------------------------------------------------------

    def list_chats(self) -> dict:
        return self._get(f"{BASE}/me/chats")

    def send_chat_message(self, chat_id: str, content: str) -> dict:
        return self._post(
            f"{BASE}/me/chats/{chat_id}/messages",
            json={"body": {"content": content}},
        )

    def list_chat_messages(self, chat_id: str, *, top: int = 20) -> dict:
        return self._get(
            f"{BASE}/me/chats/{chat_id}/messages", params={"$top": str(top)}
        )
