"""Security & Permissions service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Security(BaseService):
    """Azure DevOps Security & Permissions API."""

    def __init__(self, http, base_url: str) -> None:
        super().__init__(http)
        self._base = base_url
        self._params = {"api-version": API_VERSION}

    def list_namespaces(self) -> dict:
        return self._get(f"{self._base}/_apis/security/securitynamespaces", params=self._params)

    def get_namespace(self, namespace_id: str) -> dict:
        return self._get(
            f"{self._base}/_apis/security/securitynamespaces/{namespace_id}",
            params=self._params,
        )

    def query_acls(self, namespace_id: str, token: str) -> dict:
        return self._get(
            f"{self._base}/_apis/accesscontrollists/{namespace_id}",
            params={**self._params, "token": token},
        )

    def set_acl(self, namespace_id: str, acl: dict[str, Any]) -> dict:
        return self._post(
            f"{self._base}/_apis/accesscontrollists/{namespace_id}",
            json=acl,
            params=self._params,
        )

    def set_ace(self, namespace_id: str, body: dict[str, Any]) -> dict:
        return self._post(
            f"{self._base}/_apis/accesscontrolentries/{namespace_id}",
            json=body,
            params=self._params,
        )

    def remove_ace(self, namespace_id: str, token: str, descriptors: str) -> None:
        self._delete(
            f"{self._base}/_apis/accesscontrolentries/{namespace_id}",
            params={**self._params, "token": token, "descriptors": descriptors},
        )

    def evaluate_permissions(self, evaluations: list[dict[str, Any]]) -> dict:
        return self._post(
            f"{self._base}/_apis/security/permissionevaluationbatch",
            json={"alwaysAllowAdministrators": False, "evaluations": evaluations},
            params=self._params,
        )

    def search_identity(self, filter_value: str, *, search_filter: str = "General") -> dict:
        return self._get(
            f"https://vssps.dev.azure.com/{self._base.split('/')[3]}/_apis/identities",
            params={**self._params, "searchFilter": search_filter, "filterValue": filter_value},
        )
