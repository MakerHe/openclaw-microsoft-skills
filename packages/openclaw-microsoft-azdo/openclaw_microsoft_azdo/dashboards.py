"""Dashboards & Widgets service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

DASH_API = "7.1-preview.3"
WIDGET_API = "7.1-preview.2"


class Dashboards(BaseService):
    """Azure DevOps Dashboards & Widgets API (team-scoped)."""

    def __init__(self, http, base_url: str, project: str, team: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/{team}/_apis/dashboard"

    # -- Dashboards -------------------------------------------------------

    def list(self) -> dict:
        return self._get(f"{self._base}/dashboards", params={"api-version": DASH_API})

    def get(self, dashboard_id: str) -> dict:
        return self._get(
            f"{self._base}/dashboards/{dashboard_id}", params={"api-version": DASH_API}
        )

    def create(self, name: str, *, description: str = "") -> dict:
        return self._post(
            f"{self._base}/dashboards",
            json={"name": name, "description": description},
            params={"api-version": DASH_API},
        )

    def update(self, dashboard_id: str, updates: dict[str, Any]) -> dict:
        return self._put(
            f"{self._base}/dashboards/{dashboard_id}",
            json=updates,
            params={"api-version": DASH_API},
        )

    def delete(self, dashboard_id: str) -> None:
        self._delete(
            f"{self._base}/dashboards/{dashboard_id}", params={"api-version": DASH_API}
        )

    # -- Widgets ----------------------------------------------------------

    def list_widgets(self, dashboard_id: str) -> dict:
        return self._get(
            f"{self._base}/dashboards/{dashboard_id}/widgets",
            params={"api-version": WIDGET_API},
        )

    def get_widget(self, dashboard_id: str, widget_id: str) -> dict:
        return self._get(
            f"{self._base}/dashboards/{dashboard_id}/widgets/{widget_id}",
            params={"api-version": WIDGET_API},
        )

    def create_widget(self, dashboard_id: str, widget: dict[str, Any]) -> dict:
        return self._post(
            f"{self._base}/dashboards/{dashboard_id}/widgets",
            json=widget,
            params={"api-version": WIDGET_API},
        )

    def update_widget(
        self, dashboard_id: str, widget_id: str, updates: dict[str, Any]
    ) -> dict:
        return self._put(
            f"{self._base}/dashboards/{dashboard_id}/widgets/{widget_id}",
            json=updates,
            params={"api-version": WIDGET_API},
        )

    def delete_widget(self, dashboard_id: str, widget_id: str) -> None:
        self._delete(
            f"{self._base}/dashboards/{dashboard_id}/widgets/{widget_id}",
            params={"api-version": WIDGET_API},
        )
