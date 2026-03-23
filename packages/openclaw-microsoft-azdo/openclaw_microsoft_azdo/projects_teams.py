"""Projects, Teams & Process service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class ProjectsTeams(BaseService):
    """Azure DevOps Projects, Teams & Process API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._org_base = base_url
        self._project = project
        self._params = {"api-version": API_VERSION}

    # -- Projects ---------------------------------------------------------

    def list_projects(self) -> dict:
        return self._get(f"{self._org_base}/_apis/projects", params=self._params)

    def get_project(self, project_id: str) -> dict:
        return self._get(f"{self._org_base}/_apis/projects/{project_id}", params=self._params)

    def create_project(
        self,
        name: str,
        *,
        description: str = "",
        source_control: str = "Git",
        process_template_id: str = "6b724908-ef14-45cf-84f8-768b5384da45",
    ) -> dict:
        return self._post(
            f"{self._org_base}/_apis/projects",
            json={
                "name": name,
                "description": description,
                "capabilities": {
                    "versioncontrol": {"sourceControlType": source_control},
                    "processTemplate": {"templateTypeId": process_template_id},
                },
            },
            params=self._params,
        )

    def update_project(self, project_id: str, updates: dict[str, Any]) -> dict:
        return self._patch(
            f"{self._org_base}/_apis/projects/{project_id}",
            json=updates,
            params=self._params,
        )

    def delete_project(self, project_id: str) -> None:
        self._delete(f"{self._org_base}/_apis/projects/{project_id}", params=self._params)

    # -- Teams ------------------------------------------------------------

    def list_teams(self) -> dict:
        return self._get(
            f"{self._org_base}/_apis/projects/{self._project}/teams",
            params=self._params,
        )

    def get_team(self, team_id: str) -> dict:
        return self._get(
            f"{self._org_base}/_apis/projects/{self._project}/teams/{team_id}",
            params=self._params,
        )

    def create_team(self, name: str, *, description: str = "") -> dict:
        return self._post(
            f"{self._org_base}/_apis/projects/{self._project}/teams",
            json={"name": name, "description": description},
            params=self._params,
        )

    def list_team_members(self, team_id: str) -> dict:
        return self._get(
            f"{self._org_base}/_apis/projects/{self._project}/teams/{team_id}/members",
            params=self._params,
        )

    # -- Process ----------------------------------------------------------

    def list_processes(self) -> dict:
        return self._get(f"{self._org_base}/_apis/process/processes", params=self._params)

    def get_process(self, process_id: str) -> dict:
        return self._get(
            f"{self._org_base}/_apis/process/processes/{process_id}", params=self._params
        )

    # -- Project Properties -----------------------------------------------

    def get_properties(self) -> dict:
        return self._get(
            f"{self._org_base}/_apis/projects/{self._project}/properties",
            params={"api-version": "7.1-preview.1"},
        )

    # -- Areas and Iterations ---------------------------------------------

    def list_areas(self, *, depth: int = 10) -> dict:
        return self._get(
            f"{self._org_base}/{self._project}/_apis/wit/classificationnodes/areas",
            params={**self._params, "$depth": str(depth)},
        )

    def list_iterations(self, *, depth: int = 10) -> dict:
        return self._get(
            f"{self._org_base}/{self._project}/_apis/wit/classificationnodes/iterations",
            params={**self._params, "$depth": str(depth)},
        )

    def create_area(self, name: str) -> dict:
        return self._post(
            f"{self._org_base}/{self._project}/_apis/wit/classificationnodes/areas",
            json={"name": name},
            params=self._params,
        )

    def create_iteration(
        self,
        name: str,
        *,
        start_date: str | None = None,
        finish_date: str | None = None,
    ) -> dict:
        body: dict[str, Any] = {"name": name}
        if start_date or finish_date:
            body["attributes"] = {}
            if start_date:
                body["attributes"]["startDate"] = start_date
            if finish_date:
                body["attributes"]["finishDate"] = finish_date
        return self._post(
            f"{self._org_base}/{self._project}/_apis/wit/classificationnodes/iterations",
            json=body,
            params=self._params,
        )
