"""OneNote service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me/onenote"


class OneNote(BaseService):
    """Microsoft Graph OneNote API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    # -- Notebooks --------------------------------------------------------

    def list_notebooks(self) -> dict:
        return self._get(f"{BASE}/notebooks")

    def get_notebook(self, notebook_id: str) -> dict:
        return self._get(f"{BASE}/notebooks/{notebook_id}")

    def create_notebook(self, display_name: str) -> dict:
        return self._post(f"{BASE}/notebooks", json={"displayName": display_name})

    # -- Sections ---------------------------------------------------------

    def list_sections(self, notebook_id: str) -> dict:
        return self._get(f"{BASE}/notebooks/{notebook_id}/sections")

    def list_all_sections(self) -> dict:
        return self._get(f"{BASE}/sections")

    def create_section(self, notebook_id: str, display_name: str) -> dict:
        return self._post(
            f"{BASE}/notebooks/{notebook_id}/sections",
            json={"displayName": display_name},
        )

    # -- Pages ------------------------------------------------------------

    def list_pages(self, section_id: str) -> dict:
        return self._get(f"{BASE}/sections/{section_id}/pages")

    def list_all_pages(self, *, top: int = 20) -> dict:
        return self._get(
            f"{BASE}/pages",
            params={"$top": str(top), "$orderby": "lastModifiedDateTime desc"},
        )

    def get_page_content(self, page_id: str) -> str:
        resp = self._request("GET", f"{BASE}/pages/{page_id}/content")
        return resp.text

    def create_page(self, section_id: str, html_content: str) -> dict:
        return self._request(
            "POST",
            f"{BASE}/sections/{section_id}/pages",
            content=html_content.encode(),
            content_type="text/html",
        ).json()

    def update_page(self, page_id: str, commands: list[dict[str, Any]]) -> None:
        self._patch(f"{BASE}/pages/{page_id}/content", json=commands)

    def delete_page(self, page_id: str) -> None:
        self._delete(f"{BASE}/pages/{page_id}")

    def copy_page_to_section(self, page_id: str, destination_section_id: str) -> dict:
        return self._post(
            f"{BASE}/pages/{page_id}/copyToSection",
            json={"id": destination_section_id},
        )

    # -- Section Groups ---------------------------------------------------

    def list_section_groups(self, notebook_id: str) -> dict:
        return self._get(f"{BASE}/notebooks/{notebook_id}/sectionGroups")
