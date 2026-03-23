"""Pipelines (YAML) service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Pipelines(BaseService):
    """Azure DevOps Pipelines (YAML) API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/pipelines"
        self._project_base = f"{base_url}/{project}/_apis"
        self._params = {"api-version": API_VERSION}

    def list(self) -> dict:
        return self._get(self._base, params=self._params)

    def get(self, pipeline_id: int) -> dict:
        return self._get(f"{self._base}/{pipeline_id}", params=self._params)

    def create(
        self,
        name: str,
        *,
        repo_id: str,
        yaml_path: str = "/azure-pipelines.yml",
        folder: str = "/",
    ) -> dict:
        return self._post(
            self._base,
            json={
                "name": name,
                "folder": folder,
                "configuration": {
                    "type": "yaml",
                    "path": yaml_path,
                    "repository": {"id": repo_id, "type": "azureReposGit"},
                },
            },
            params=self._params,
        )

    def run(
        self,
        pipeline_id: int,
        *,
        branch: str = "main",
        template_parameters: dict[str, str] | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "resources": {"repositories": {"self": {"refName": f"refs/heads/{branch}"}}}
        }
        if template_parameters:
            body["templateParameters"] = template_parameters
        return self._post(
            f"{self._base}/{pipeline_id}/runs", json=body, params=self._params
        )

    def list_runs(self, pipeline_id: int) -> dict:
        return self._get(f"{self._base}/{pipeline_id}/runs", params=self._params)

    def get_run(self, pipeline_id: int, run_id: int) -> dict:
        return self._get(
            f"{self._base}/{pipeline_id}/runs/{run_id}", params=self._params
        )

    def list_run_logs(self, pipeline_id: int, run_id: int) -> dict:
        return self._get(
            f"{self._base}/{pipeline_id}/runs/{run_id}/logs", params=self._params
        )

    def get_run_log(self, pipeline_id: int, run_id: int, log_id: int) -> dict:
        return self._get(
            f"{self._base}/{pipeline_id}/runs/{run_id}/logs/{log_id}",
            params=self._params,
        )

    def list_approvals(self) -> dict:
        return self._get(
            f"{self._project_base}/pipelines/approvals",
            params={"api-version": "7.1-preview.1"},
        )

    def approve(self, approval_id: str, *, comment: str = "") -> dict:
        return self._patch(
            f"{self._project_base}/pipelines/approvals",
            json=[{"approvalId": approval_id, "status": "approved", "comment": comment}],
            params={"api-version": "7.1-preview.1"},
        )

    def list_environments(self) -> dict:
        return self._get(
            f"{self._project_base}/pipelines/environments",
            params={"api-version": "7.1-preview.1"},
        )

    def get_environment(self, environment_id: int) -> dict:
        return self._get(
            f"{self._project_base}/pipelines/environments/{environment_id}",
            params={"api-version": "7.1-preview.1"},
        )

    def create_environment(self, name: str, *, description: str = "") -> dict:
        return self._post(
            f"{self._project_base}/pipelines/environments",
            json={"name": name, "description": description},
            params={"api-version": "7.1-preview.1"},
        )

    def preview(self, pipeline_id: int, *, branch: str = "main") -> dict:
        return self._post(
            f"{self._base}/{pipeline_id}/preview",
            json={
                "previewRun": True,
                "resources": {
                    "repositories": {"self": {"refName": f"refs/heads/{branch}"}}
                },
            },
            params={"api-version": "7.1-preview.1"},
        )
