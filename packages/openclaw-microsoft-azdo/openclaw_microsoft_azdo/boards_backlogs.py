"""Boards, Backlogs & Sprints service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class BoardsBacklogs(BaseService):
    """Azure DevOps Boards, Backlogs & Sprints API (team-scoped)."""

    def __init__(self, http, base_url: str, project: str, team: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/{team}/_apis/work"
        self._params = {"api-version": API_VERSION}

    # -- Boards -----------------------------------------------------------

    def list_boards(self) -> dict:
        return self._get(f"{self._base}/boards", params=self._params)

    def get_board(self, board_id: str) -> dict:
        return self._get(f"{self._base}/boards/{board_id}", params=self._params)

    def get_columns(self, board_id: str) -> dict:
        return self._get(f"{self._base}/boards/{board_id}/columns", params=self._params)

    def update_columns(self, board_id: str, columns: list[dict[str, Any]]) -> dict:
        return self._put(
            f"{self._base}/boards/{board_id}/columns", json=columns, params=self._params
        )

    def get_rows(self, board_id: str) -> dict:
        return self._get(f"{self._base}/boards/{board_id}/rows", params=self._params)

    # -- Backlogs ---------------------------------------------------------

    def list_backlogs(self) -> dict:
        return self._get(f"{self._base}/backlogs", params=self._params)

    def get_backlog_items(self, backlog_id: str) -> dict:
        return self._get(
            f"{self._base}/backlogs/{backlog_id}/workItems", params=self._params
        )

    # -- Iterations -------------------------------------------------------

    def list_iterations(self) -> dict:
        return self._get(f"{self._base}/teamsettings/iterations", params=self._params)

    def get_current_iteration(self) -> dict:
        return self._get(
            f"{self._base}/teamsettings/iterations",
            params={**self._params, "$timeframe": "current"},
        )

    def get_iteration_work_items(self, iteration_id: str) -> dict:
        return self._get(
            f"{self._base}/teamsettings/iterations/{iteration_id}/workitems",
            params=self._params,
        )

    def get_iteration_capacity(self, iteration_id: str) -> dict:
        return self._get(
            f"{self._base}/teamsettings/iterations/{iteration_id}/capacities",
            params=self._params,
        )

    def add_iteration(self, iteration_id: str) -> dict:
        return self._post(
            f"{self._base}/teamsettings/iterations",
            json={"id": iteration_id},
            params=self._params,
        )

    # -- Team Settings ----------------------------------------------------

    def get_settings(self) -> dict:
        return self._get(f"{self._base}/teamsettings", params=self._params)

    def update_settings(self, settings: dict[str, Any]) -> dict:
        return self._patch(f"{self._base}/teamsettings", json=settings, params=self._params)

    def get_team_field_values(self) -> dict:
        return self._get(f"{self._base}/teamsettings/teamfieldvalues", params=self._params)
