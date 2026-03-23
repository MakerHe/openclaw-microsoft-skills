"""Release Management service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Releases(BaseService):
    """Azure DevOps Release Management API (vsrm.dev.azure.com)."""

    def __init__(self, http, org: str, project: str) -> None:
        super().__init__(http)
        self._base = f"https://vsrm.dev.azure.com/{org}/{project}/_apis/release"
        self._params = {"api-version": API_VERSION}

    def list_definitions(self) -> dict:
        return self._get(f"{self._base}/definitions", params=self._params)

    def get_definition(self, definition_id: int) -> dict:
        return self._get(f"{self._base}/definitions/{definition_id}", params=self._params)

    def create(
        self,
        definition_id: int,
        *,
        description: str = "",
        artifacts: list[dict[str, Any]] | None = None,
    ) -> dict:
        body: dict[str, Any] = {"definitionId": definition_id, "description": description}
        if artifacts:
            body["artifacts"] = artifacts
        return self._post(f"{self._base}/releases", json=body, params=self._params)

    def list(
        self,
        *,
        definition_id: int | None = None,
        top: int | None = None,
    ) -> dict:
        params = dict(self._params)
        if definition_id:
            params["definitionId"] = str(definition_id)
        if top:
            params["$top"] = str(top)
        return self._get(f"{self._base}/releases", params=params)

    def get(self, release_id: int) -> dict:
        return self._get(f"{self._base}/releases/{release_id}", params=self._params)

    def deploy(
        self,
        release_id: int,
        environment_id: int,
        *,
        status: str = "inProgress",
        comment: str = "",
    ) -> dict:
        return self._patch(
            f"{self._base}/releases/{release_id}/environments/{environment_id}",
            json={"status": status, "comment": comment},
            params=self._params,
        )

    def list_approvals(self, *, status_filter: str = "pending") -> dict:
        return self._get(
            f"{self._base}/approvals",
            params={**self._params, "statusFilter": status_filter},
        )

    def approve(self, approval_id: str, *, comments: str = "") -> dict:
        return self._patch(
            f"{self._base}/approvals/{approval_id}",
            json={"status": "approved", "comments": comments},
            params=self._params,
        )

    def get_tasks(
        self, release_id: int, environment_id: int, attempt_id: int
    ) -> dict:
        return self._get(
            f"{self._base}/releases/{release_id}/environments/{environment_id}/attempts/{attempt_id}/tasks",
            params=self._params,
        )

    def delete(self, release_id: int) -> None:
        self._delete(f"{self._base}/releases/{release_id}", params=self._params)

    def list_gates(self, release_id: int, environment_id: int) -> dict:
        return self._get(
            f"{self._base}/releases/{release_id}/environments/{environment_id}/gates",
            params={"api-version": "7.1-preview.1"},
        )
