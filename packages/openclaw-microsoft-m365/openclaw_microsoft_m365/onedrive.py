"""OneDrive service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me/drive"


class OneDrive(BaseService):
    """Microsoft Graph OneDrive API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    def list_root(self) -> dict:
        return self._get(f"{BASE}/root/children")

    def list_folder(self, folder_path: str) -> dict:
        return self._get(f"{BASE}/root:/{folder_path}:/children")

    def list_folder_by_id(self, item_id: str) -> dict:
        return self._get(f"{BASE}/items/{item_id}/children")

    def get_metadata(self, file_path: str) -> dict:
        return self._get(f"{BASE}/root:/{file_path}:")

    def get_metadata_by_id(self, item_id: str) -> dict:
        return self._get(f"{BASE}/items/{item_id}")

    def download(self, file_path: str) -> bytes:
        resp = self._request("GET", f"{BASE}/root:/{file_path}:/content")
        return resp.content

    def download_by_id(self, item_id: str) -> bytes:
        resp = self._request("GET", f"{BASE}/items/{item_id}/content")
        return resp.content

    def upload(self, file_path: str, data: bytes) -> dict:
        return self._request(
            "PUT",
            f"{BASE}/root:/{file_path}:/content",
            content=data,
            content_type="application/octet-stream",
        ).json()

    def create_upload_session(
        self, file_path: str, *, conflict_behavior: str = "rename"
    ) -> dict:
        return self._post(
            f"{BASE}/root:/{file_path}:/createUploadSession",
            json={"item": {"@microsoft.graph.conflictBehavior": conflict_behavior}},
        )

    def create_folder(
        self, name: str, *, parent_path: str | None = None, conflict_behavior: str = "rename"
    ) -> dict:
        url = f"{BASE}/root/children" if not parent_path else f"{BASE}/root:/{parent_path}:/children"
        return self._post(
            url,
            json={"name": name, "folder": {}, "@microsoft.graph.conflictBehavior": conflict_behavior},
        )

    def delete(self, item_id: str) -> None:
        self._delete(f"{BASE}/items/{item_id}")

    def move_or_rename(
        self, item_id: str, *, name: str | None = None, parent_id: str | None = None
    ) -> dict:
        body: dict[str, Any] = {}
        if name:
            body["name"] = name
        if parent_id:
            body["parentReference"] = {"id": parent_id}
        return self._patch(f"{BASE}/items/{item_id}", json=body)

    def copy(self, item_id: str, *, destination_folder_id: str, name: str | None = None) -> dict:
        body: dict[str, Any] = {"parentReference": {"id": destination_folder_id}}
        if name:
            body["name"] = name
        return self._post(f"{BASE}/items/{item_id}/copy", json=body)

    def create_sharing_link(
        self, item_id: str, *, link_type: str = "view", scope: str = "organization"
    ) -> dict:
        return self._post(
            f"{BASE}/items/{item_id}/createLink",
            json={"type": link_type, "scope": scope},
        )

    def search(self, query: str) -> dict:
        return self._get(f"{BASE}/root/search(q='{query}')")

    def get_drive_info(self) -> dict:
        return self._get(BASE)

    def list_recent(self) -> dict:
        return self._get(f"{BASE}/recent")

    def list_shared_with_me(self) -> dict:
        return self._get(f"{BASE}/sharedWithMe")
