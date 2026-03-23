"""Branch Policy service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Policy(BaseService):
    """Azure DevOps Branch Policy API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/policy"
        self._params = {"api-version": API_VERSION}

    def list_configurations(self) -> dict:
        return self._get(f"{self._base}/configurations", params=self._params)

    def get_configuration(self, config_id: int) -> dict:
        return self._get(f"{self._base}/configurations/{config_id}", params=self._params)

    def list_types(self) -> dict:
        return self._get(f"{self._base}/types", params=self._params)

    def create(self, configuration: dict[str, Any]) -> dict:
        return self._post(
            f"{self._base}/configurations", json=configuration, params=self._params
        )

    def update(self, config_id: int, configuration: dict[str, Any]) -> dict:
        return self._put(
            f"{self._base}/configurations/{config_id}",
            json=configuration,
            params=self._params,
        )

    def delete(self, config_id: int) -> None:
        self._delete(f"{self._base}/configurations/{config_id}", params=self._params)

    def list_evaluations(self, project_id: str, pr_id: int) -> dict:
        artifact_id = f"vstfs:///CodeReview/CodeReviewId/{project_id}/{pr_id}"
        return self._get(
            f"{self._base}/evaluations",
            params={**self._params, "artifactId": artifact_id},
        )
