"""Service Hooks service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class ServiceHooks(BaseService):
    """Azure DevOps Service Hooks API."""

    def __init__(self, http, base_url: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/_apis/hooks"
        self._params = {"api-version": API_VERSION}

    def list_subscriptions(self) -> dict:
        return self._get(f"{self._base}/subscriptions", params=self._params)

    def get_subscription(self, subscription_id: str) -> dict:
        return self._get(
            f"{self._base}/subscriptions/{subscription_id}", params=self._params
        )

    def create_subscription(
        self,
        *,
        event_type: str,
        webhook_url: str,
        publisher_id: str = "tfs",
        publisher_inputs: dict[str, str] | None = None,
        consumer_id: str = "webHooks",
        consumer_action_id: str = "httpRequest",
    ) -> dict:
        body: dict[str, Any] = {
            "publisherId": publisher_id,
            "eventType": event_type,
            "resourceVersion": "1.0",
            "consumerId": consumer_id,
            "consumerActionId": consumer_action_id,
            "consumerInputs": {"url": webhook_url},
        }
        if publisher_inputs:
            body["publisherInputs"] = publisher_inputs
        return self._post(f"{self._base}/subscriptions", json=body, params=self._params)

    def update_subscription(self, subscription_id: str, body: dict[str, Any]) -> dict:
        return self._put(
            f"{self._base}/subscriptions/{subscription_id}", json=body, params=self._params
        )

    def delete_subscription(self, subscription_id: str) -> None:
        self._delete(
            f"{self._base}/subscriptions/{subscription_id}", params=self._params
        )

    def list_publishers(self) -> dict:
        return self._get(f"{self._base}/publishers", params=self._params)

    def list_consumers(self) -> dict:
        return self._get(f"{self._base}/consumers", params=self._params)

    def test_notification(self, subscription_id: str) -> dict:
        return self._post(
            f"{self._base}/testnotifications",
            json={"subscriptionId": subscription_id},
            params=self._params,
        )

    def list_notifications(self, subscription_id: str) -> dict:
        return self._get(
            f"{self._base}/subscriptions/{subscription_id}/notifications",
            params=self._params,
        )
