"""Graph & Identity service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_PREVIEW = "7.1-preview.1"


class GraphIdentity(BaseService):
    """Azure DevOps Graph & Identity API (vssps.dev.azure.com)."""

    def __init__(self, http, org: str) -> None:
        super().__init__(http)
        self._base = f"https://vssps.dev.azure.com/{org}/_apis"
        self._params = {"api-version": API_PREVIEW}

    # -- Users ------------------------------------------------------------

    def list_users(self) -> dict:
        return self._get(f"{self._base}/graph/users", params=self._params)

    def get_user(self, user_descriptor: str) -> dict:
        return self._get(f"{self._base}/graph/users/{user_descriptor}", params=self._params)

    def create_user(self, principal_name: str, *, origin_id: str = "") -> dict:
        return self._post(
            f"{self._base}/graph/users",
            json={"principalName": principal_name, "storageKey": "", "originId": origin_id},
            params=self._params,
        )

    def delete_user(self, user_descriptor: str) -> None:
        self._delete(f"{self._base}/graph/users/{user_descriptor}", params=self._params)

    # -- Groups -----------------------------------------------------------

    def list_groups(self) -> dict:
        return self._get(f"{self._base}/graph/groups", params=self._params)

    def get_group(self, group_descriptor: str) -> dict:
        return self._get(
            f"{self._base}/graph/groups/{group_descriptor}", params=self._params
        )

    def create_group(
        self, display_name: str, *, scope_descriptor: str, description: str = ""
    ) -> dict:
        return self._post(
            f"{self._base}/graph/groups",
            json={"displayName": display_name, "description": description},
            params={**self._params, "scopeDescriptor": scope_descriptor},
        )

    def delete_group(self, group_descriptor: str) -> None:
        self._delete(
            f"{self._base}/graph/groups/{group_descriptor}", params=self._params
        )

    # -- Memberships ------------------------------------------------------

    def list_memberships(self, subject_descriptor: str, *, direction: str = "Down") -> dict:
        return self._get(
            f"{self._base}/graph/memberships/{subject_descriptor}",
            params={**self._params, "direction": direction},
        )

    def add_membership(self, subject_descriptor: str, container_descriptor: str) -> dict:
        return self._put(
            f"{self._base}/graph/memberships/{subject_descriptor}/{container_descriptor}",
            params=self._params,
        )

    def remove_membership(self, subject_descriptor: str, container_descriptor: str) -> None:
        self._delete(
            f"{self._base}/graph/memberships/{subject_descriptor}/{container_descriptor}",
            params=self._params,
        )

    # -- Descriptors ------------------------------------------------------

    def get_descriptor(self, storage_key: str) -> dict:
        return self._get(f"{self._base}/graph/descriptors/{storage_key}", params=self._params)

    def get_scope_descriptor(self, project_id: str) -> dict:
        return self._get(f"{self._base}/graph/descriptors/{project_id}", params=self._params)

    # -- Subject Lookup ---------------------------------------------------

    def lookup_subjects(self, descriptors: list[str]) -> dict:
        return self._post(
            f"{self._base}/graph/subjectlookup",
            json={"lookupKeys": [{"descriptor": d} for d in descriptors]},
            params=self._params,
        )

    # -- Identities (Legacy) ----------------------------------------------

    def search_identity(self, filter_value: str, *, search_filter: str = "General") -> dict:
        return self._get(
            f"{self._base}/identities",
            params={"api-version": "7.1", "searchFilter": search_filter, "filterValue": filter_value},
        )
