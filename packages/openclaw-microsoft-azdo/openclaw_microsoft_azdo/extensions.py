"""Extensions Management service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_PREVIEW = "7.1-preview.1"


class Extensions(BaseService):
    """Azure DevOps Extension Management API (extmgmt.dev.azure.com)."""

    def __init__(self, http, org: str) -> None:
        super().__init__(http)
        self._base = f"https://extmgmt.dev.azure.com/{org}/_apis/extensionmanagement"
        self._params = {"api-version": API_PREVIEW}

    def list_installed(self) -> dict:
        return self._get(f"{self._base}/installedextensions", params=self._params)

    def get(self, publisher_name: str, extension_name: str) -> dict:
        return self._get(
            f"{self._base}/installedextensionsbyname/{publisher_name}/{extension_name}",
            params=self._params,
        )

    def install(self, publisher_name: str, extension_name: str, version: str) -> dict:
        return self._post(
            f"{self._base}/installedextensionsbyname/{publisher_name}/{extension_name}/{version}",
            params=self._params,
        )

    def uninstall(self, publisher_name: str, extension_name: str) -> None:
        self._delete(
            f"{self._base}/installedextensionsbyname/{publisher_name}/{extension_name}",
            params=self._params,
        )

    def set_enabled(self, publisher_name: str, extension_name: str, *, enabled: bool) -> dict:
        flags = "none" if enabled else "disabled"
        return self._patch(
            f"{self._base}/installedextensionsbyname/{publisher_name}/{extension_name}",
            json={"installState": {"flags": flags}},
            params=self._params,
        )

    def get_data_document(
        self,
        publisher_name: str,
        extension_name: str,
        collection_name: str,
        document_id: str,
    ) -> dict:
        return self._get(
            f"{self._base}/InstalledExtensions/{publisher_name}/{extension_name}"
            f"/Data/Scopes/Default/Current/Collections/{collection_name}/Documents/{document_id}",
            params=self._params,
        )

    def set_data_document(
        self,
        publisher_name: str,
        extension_name: str,
        collection_name: str,
        document: dict[str, Any],
    ) -> dict:
        return self._put(
            f"{self._base}/InstalledExtensions/{publisher_name}/{extension_name}"
            f"/Data/Scopes/Default/Current/Collections/{collection_name}/Documents",
            json=document,
            params=self._params,
        )

    def list_requests(self) -> dict:
        return self._get(f"{self._base}/requests", params=self._params)
