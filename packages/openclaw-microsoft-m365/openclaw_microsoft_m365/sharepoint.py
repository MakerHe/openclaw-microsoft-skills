"""SharePoint service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0"


class SharePoint(BaseService):
    """Microsoft Graph SharePoint API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    # -- Sites ------------------------------------------------------------

    def search_sites(self, keyword: str) -> dict:
        return self._get(f"{BASE}/sites", params={"search": keyword})

    def get_root_site(self) -> dict:
        return self._get(f"{BASE}/sites/root")

    def get_site_by_path(self, hostname: str, site_path: str) -> dict:
        return self._get(f"{BASE}/sites/{hostname}:/{site_path}")

    def get_site(self, site_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}")

    def list_subsites(self, site_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/sites")

    def list_followed_sites(self) -> dict:
        return self._get(f"{BASE}/me/followedSites")

    # -- Lists ------------------------------------------------------------

    def list_lists(self, site_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/lists")

    def get_list(self, site_id: str, list_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/lists/{list_id}")

    def create_list(self, site_id: str, list_def: dict[str, Any]) -> dict:
        return self._post(f"{BASE}/sites/{site_id}/lists", json=list_def)

    def delete_list(self, site_id: str, list_id: str) -> None:
        self._delete(f"{BASE}/sites/{site_id}/lists/{list_id}")

    def list_columns(self, site_id: str, list_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/lists/{list_id}/columns")

    # -- List Items -------------------------------------------------------

    def list_items(
        self,
        site_id: str,
        list_id: str,
        *,
        top: int = 20,
        expand_fields: bool = True,
        field_select: list[str] | None = None,
    ) -> dict:
        params: dict[str, str] = {"$top": str(top)}
        if expand_fields:
            if field_select:
                params["$expand"] = f"fields($select={','.join(field_select)})"
            else:
                params["$expand"] = "fields"
        return self._get(f"{BASE}/sites/{site_id}/lists/{list_id}/items", params=params)

    def get_item(self, site_id: str, list_id: str, item_id: str) -> dict:
        return self._get(
            f"{BASE}/sites/{site_id}/lists/{list_id}/items/{item_id}",
            params={"$expand": "fields"},
        )

    def create_item(self, site_id: str, list_id: str, fields: dict[str, Any]) -> dict:
        return self._post(
            f"{BASE}/sites/{site_id}/lists/{list_id}/items", json={"fields": fields}
        )

    def update_item(
        self, site_id: str, list_id: str, item_id: str, fields: dict[str, Any]
    ) -> dict:
        return self._patch(
            f"{BASE}/sites/{site_id}/lists/{list_id}/items/{item_id}/fields",
            json=fields,
        )

    def delete_item(self, site_id: str, list_id: str, item_id: str) -> None:
        self._delete(f"{BASE}/sites/{site_id}/lists/{list_id}/items/{item_id}")

    # -- Site Drive -------------------------------------------------------

    def get_drive(self, site_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/drive")

    def list_drive_root(self, site_id: str) -> dict:
        return self._get(f"{BASE}/sites/{site_id}/drive/root/children")
