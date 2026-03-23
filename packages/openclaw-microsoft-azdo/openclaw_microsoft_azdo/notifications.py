"""Notifications service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Notifications(BaseService):
    """Azure DevOps Notifications API."""

    def __init__(self, http, base_url: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/_apis/notification"
        self._params = {"api-version": API_VERSION}

    def list_subscriptions(self) -> dict:
        return self._get(f"{self._base}/subscriptions", params=self._params)

    def get_subscription(self, subscription_id: str) -> dict:
        return self._get(
            f"{self._base}/subscriptions/{subscription_id}", params=self._params
        )

    def create_subscription(self, body: dict[str, Any]) -> dict:
        return self._post(f"{self._base}/subscriptions", json=body, params=self._params)

    def update_subscription(self, subscription_id: str, body: dict[str, Any]) -> dict:
        return self._put(
            f"{self._base}/subscriptions/{subscription_id}",
            json=body,
            params=self._params,
        )

    def delete_subscription(self, subscription_id: str) -> None:
        self._delete(
            f"{self._base}/subscriptions/{subscription_id}", params=self._params
        )

    def list_event_types(self) -> dict:
        return self._get(f"{self._base}/eventtypes", params=self._params)

    def get_diagnostics(self, subscription_id: str) -> dict:
        return self._get(
            f"{self._base}/subscriptions/{subscription_id}/diagnostics",
            params={"api-version": "7.1-preview.1"},
        )

    def get_settings(self) -> dict:
        return self._get(
            f"{self._base}/settings", params={"api-version": "7.1-preview.1"}
        )

    def get_subscriber(self, subscriber_id: str) -> dict:
        return self._get(
            f"{self._base}/subscribers/{subscriber_id}",
            params={"api-version": "7.1-preview.1"},
        )

    def update_subscriber(self, subscriber_id: str, updates: dict[str, Any]) -> dict:
        return self._patch(
            f"{self._base}/subscribers/{subscriber_id}",
            json=updates,
            params={"api-version": "7.1-preview.1"},
        )
