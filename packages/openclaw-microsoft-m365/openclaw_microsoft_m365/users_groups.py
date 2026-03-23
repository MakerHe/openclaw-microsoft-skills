"""Users & Groups service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0"


class UsersGroups(BaseService):
    """Microsoft Graph Users & Groups API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    # -- Users ------------------------------------------------------------

    def get_me(self) -> dict:
        return self._get(f"{BASE}/me")

    def get_my_photo(self) -> bytes:
        return self._request("GET", f"{BASE}/me/photo/$value").content

    def get_user(self, user_id_or_upn: str) -> dict:
        return self._get(f"{BASE}/users/{user_id_or_upn}")

    def list_users(
        self,
        *,
        top: int = 20,
        select: list[str] | None = None,
        filter: str | None = None,
        search: str | None = None,
    ) -> dict:
        params: dict[str, str] = {"$top": str(top)}
        if select:
            params["$select"] = ",".join(select)
        if filter:
            params["$filter"] = filter
        if search:
            params["$search"] = search
        headers = {"ConsistencyLevel": "eventual"} if search else None
        return self._request("GET", f"{BASE}/users", params=params, headers=headers).json()

    def get_manager(self) -> dict:
        return self._get(f"{BASE}/me/manager")

    def get_direct_reports(self) -> dict:
        return self._get(f"{BASE}/me/directReports")

    # -- Groups -----------------------------------------------------------

    def list_groups(
        self, *, top: int = 20, filter: str | None = None
    ) -> dict:
        params: dict[str, str] = {"$top": str(top)}
        if filter:
            params["$filter"] = filter
        return self._get(f"{BASE}/groups", params=params)

    def get_group(self, group_id: str) -> dict:
        return self._get(f"{BASE}/groups/{group_id}")

    def list_group_members(self, group_id: str) -> dict:
        return self._get(f"{BASE}/groups/{group_id}/members")

    def list_my_groups(self) -> dict:
        return self._get(f"{BASE}/me/memberOf")

    def check_member_groups(self, group_ids: list[str]) -> dict:
        return self._post(f"{BASE}/me/checkMemberGroups", json={"groupIds": group_ids})

    def list_group_owners(self, group_id: str) -> dict:
        return self._get(f"{BASE}/groups/{group_id}/owners")

    def get_organization(self) -> dict:
        return self._get(f"{BASE}/organization")
