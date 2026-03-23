"""Personal Access Token (PAT) authentication for Azure DevOps."""

from __future__ import annotations

import base64

import httpx


class PATAuth(httpx.Auth):
    """httpx-compatible auth that injects Basic auth with an Azure DevOps PAT."""

    def __init__(self, pat: str) -> None:
        self._header = "Basic " + base64.b64encode(f":{pat}".encode()).decode()

    def auth_flow(self, request: httpx.Request):
        request.headers["Authorization"] = self._header
        yield request
