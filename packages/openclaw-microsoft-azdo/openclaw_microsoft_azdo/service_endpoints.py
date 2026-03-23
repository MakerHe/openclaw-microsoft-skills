"""Service Connections (Endpoints) service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class ServiceEndpoints(BaseService):
    """Azure DevOps Service Endpoints API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/serviceendpoint"
        self._org_base = f"{base_url}/_apis/serviceendpoint"
        self._params = {"api-version": API_VERSION}

    def list(self, *, endpoint_type: str | None = None) -> dict:
        params = dict(self._params)
        if endpoint_type:
            params["type"] = endpoint_type
        return self._get(f"{self._base}/endpoints", params=params)

    def get(self, endpoint_id: str) -> dict:
        return self._get(f"{self._base}/endpoints/{endpoint_id}", params=self._params)

    def create(self, endpoint: dict[str, Any]) -> dict:
        return self._post(f"{self._base}/endpoints", json=endpoint, params=self._params)

    def update(self, endpoint_id: str, endpoint: dict[str, Any]) -> dict:
        return self._put(
            f"{self._base}/endpoints/{endpoint_id}", json=endpoint, params=self._params
        )

    def delete(self, endpoint_id: str, *, project_ids: str, deep: bool = True) -> None:
        self._delete(
            f"{self._base}/endpoints/{endpoint_id}",
            params={**self._params, "projectIds": project_ids, "deep": str(deep).lower()},
        )

    def share(self, endpoint_id: str, references: list[dict[str, Any]]) -> dict:
        return self._patch(
            f"{self._org_base}/endpoints/{endpoint_id}",
            json=references,
            params=self._params,
        )

    def execution_history(self, endpoint_id: str) -> dict:
        return self._get(
            f"{self._base}/endpoints/{endpoint_id}/executionhistory",
            params=self._params,
        )
