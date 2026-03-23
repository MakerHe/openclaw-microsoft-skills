"""Contacts service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me"


class Contacts(BaseService):
    """Microsoft Graph Contacts API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    def list(self, *, top: int = 20, select: list[str] | None = None, filter: str | None = None) -> dict:
        params: dict[str, str] = {"$top": str(top)}
        if select:
            params["$select"] = ",".join(select)
        if filter:
            params["$filter"] = filter
        return self._get(f"{BASE}/contacts", params=params)

    def get(self, contact_id: str) -> dict:
        return self._get(f"{BASE}/contacts/{contact_id}")

    def create(
        self,
        *,
        given_name: str,
        surname: str | None = None,
        email: str | None = None,
        mobile_phone: str | None = None,
        business_phones: list[str] | None = None,
        company_name: str | None = None,
        job_title: str | None = None,
    ) -> dict:
        body: dict[str, Any] = {"givenName": given_name}
        if surname:
            body["surname"] = surname
        if email:
            body["emailAddresses"] = [{"address": email, "name": f"{given_name} {surname or ''}".strip()}]
        if mobile_phone:
            body["mobilePhone"] = mobile_phone
        if business_phones:
            body["businessPhones"] = business_phones
        if company_name:
            body["companyName"] = company_name
        if job_title:
            body["jobTitle"] = job_title
        return self._post(f"{BASE}/contacts", json=body)

    def update(self, contact_id: str, updates: dict[str, Any]) -> dict:
        return self._patch(f"{BASE}/contacts/{contact_id}", json=updates)

    def delete(self, contact_id: str) -> None:
        self._delete(f"{BASE}/contacts/{contact_id}")

    def get_photo(self, contact_id: str) -> bytes:
        return self._request("GET", f"{BASE}/contacts/{contact_id}/photo/$value").content

    # -- Folders ----------------------------------------------------------

    def list_folders(self) -> dict:
        return self._get(f"{BASE}/contactFolders")

    def create_folder(self, display_name: str) -> dict:
        return self._post(f"{BASE}/contactFolders", json={"displayName": display_name})

    def list_in_folder(self, folder_id: str) -> dict:
        return self._get(f"{BASE}/contactFolders/{folder_id}/contacts")

    def create_in_folder(self, folder_id: str, contact: dict[str, Any]) -> dict:
        return self._post(f"{BASE}/contactFolders/{folder_id}/contacts", json=contact)

    def delete_folder(self, folder_id: str) -> None:
        self._delete(f"{BASE}/contactFolders/{folder_id}")
