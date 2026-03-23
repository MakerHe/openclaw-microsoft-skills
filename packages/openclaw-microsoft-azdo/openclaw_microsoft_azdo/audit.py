"""Audit Log service for Azure DevOps."""

from __future__ import annotations

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Audit(BaseService):
    """Azure DevOps Audit Log API (auditservice.dev.azure.com)."""

    def __init__(self, http, org: str) -> None:
        super().__init__(http)
        self._base = f"https://auditservice.dev.azure.com/{org}/_apis/audit"
        self._params = {"api-version": API_VERSION}

    def query(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        continuation_token: str | None = None,
    ) -> dict:
        params = dict(self._params)
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if continuation_token:
            params["continuationToken"] = continuation_token
        return self._get(f"{self._base}/auditlog", params=params)

    def download(
        self,
        *,
        start_time: str,
        end_time: str,
        fmt: str = "json",
    ) -> bytes:
        resp = self._request(
            "GET",
            f"{self._base}/downloadlog",
            params={**self._params, "format": fmt, "startTime": start_time, "endTime": end_time},
        )
        return resp.content

    def list_actions(self) -> dict:
        return self._get(f"{self._base}/actions", params=self._params)
