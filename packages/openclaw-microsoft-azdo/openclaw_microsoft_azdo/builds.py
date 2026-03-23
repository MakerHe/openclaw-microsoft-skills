"""Classic Build service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Builds(BaseService):
    """Azure DevOps Classic Build API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/build"
        self._params = {"api-version": API_VERSION}

    def list_definitions(self) -> dict:
        return self._get(f"{self._base}/definitions", params=self._params)

    def get_definition(self, definition_id: int) -> dict:
        return self._get(f"{self._base}/definitions/{definition_id}", params=self._params)

    def queue(
        self,
        definition_id: int,
        *,
        source_branch: str = "refs/heads/main",
        parameters: dict[str, str] | None = None,
    ) -> dict:
        import json as _json

        body: dict[str, Any] = {
            "definition": {"id": definition_id},
            "sourceBranch": source_branch,
        }
        if parameters:
            body["parameters"] = _json.dumps(parameters)
        return self._post(f"{self._base}/builds", json=body, params=self._params)

    def list(
        self,
        *,
        definition_id: int | None = None,
        status_filter: str | None = None,
        result_filter: str | None = None,
        top: int | None = None,
    ) -> dict:
        params = dict(self._params)
        if definition_id:
            params["definitions"] = str(definition_id)
        if status_filter:
            params["statusFilter"] = status_filter
        if result_filter:
            params["resultFilter"] = result_filter
        if top:
            params["$top"] = str(top)
        return self._get(f"{self._base}/builds", params=params)

    def get(self, build_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}", params=self._params)

    def cancel(self, build_id: int) -> dict:
        return self._patch(
            f"{self._base}/builds/{build_id}",
            json={"status": "cancelling"},
            params=self._params,
        )

    def list_logs(self, build_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}/logs", params=self._params)

    def get_log(self, build_id: int, log_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}/logs/{log_id}", params=self._params)

    def get_timeline(self, build_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}/timeline", params=self._params)

    def list_artifacts(self, build_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}/artifacts", params=self._params)

    def get_artifact(self, build_id: int, artifact_name: str) -> dict:
        return self._get(
            f"{self._base}/builds/{build_id}/artifacts",
            params={**self._params, "artifactName": artifact_name},
        )

    def list_tags(self, build_id: int) -> dict:
        return self._get(f"{self._base}/builds/{build_id}/tags", params=self._params)

    def add_tag(self, build_id: int, tag: str) -> dict:
        return self._put(f"{self._base}/builds/{build_id}/tags/{tag}", params=self._params)

    def delete(self, build_id: int) -> None:
        self._delete(f"{self._base}/builds/{build_id}", params=self._params)

    def retain(self, build_id: int, *, keep_forever: bool = True) -> dict:
        return self._patch(
            f"{self._base}/builds/{build_id}",
            json={"keepForever": keep_forever},
            params=self._params,
        )
