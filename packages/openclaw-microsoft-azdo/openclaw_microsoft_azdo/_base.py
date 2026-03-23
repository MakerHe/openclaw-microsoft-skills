"""Shared base client with HTTP helpers, pagination, and error handling."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx


def load_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE env file, ignoring comments and blank lines."""
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result


class APIError(Exception):
    """Raised when the API returns a non-2xx status."""

    def __init__(self, response: httpx.Response) -> None:
        self.status_code = response.status_code
        self.response = response
        try:
            body = response.json()
        except Exception:
            body = response.text
        super().__init__(f"HTTP {self.status_code}: {body}")


class BaseService:
    """Mixin for service classes that need HTTP helpers."""

    def __init__(self, http: httpx.Client) -> None:
        self._http = http

    # -- low-level helpers ------------------------------------------------

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
        content: bytes | None = None,
        content_type: str | None = None,
    ) -> httpx.Response:
        kw: dict[str, Any] = {}
        if params:
            kw["params"] = params
        if json is not None:
            kw["json"] = json
        if content is not None:
            kw["content"] = content
        if headers or content_type:
            h = dict(headers or {})
            if content_type:
                h["Content-Type"] = content_type
            kw["headers"] = h
        resp = self._http.request(method, url, **kw)
        if not resp.is_success:
            raise APIError(resp)
        return resp

    def _get(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", url, params=params).json()

    def _post(
        self,
        url: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        content_type: str | None = None,
    ) -> Any:
        resp = self._request("POST", url, json=json, params=params, content_type=content_type)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _patch(
        self,
        url: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
        content_type: str | None = None,
    ) -> Any:
        resp = self._request("PATCH", url, json=json, params=params, content_type=content_type)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _put(self, url: str, *, json: Any = None, params: dict[str, Any] | None = None) -> Any:
        resp = self._request("PUT", url, json=json, params=params)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    def _delete(self, url: str, *, params: dict[str, Any] | None = None) -> None:
        self._request("DELETE", url, params=params)
