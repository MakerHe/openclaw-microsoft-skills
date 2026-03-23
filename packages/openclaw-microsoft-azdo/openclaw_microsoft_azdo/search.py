"""Search service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Search(BaseService):
    """Azure DevOps Search API (almsearch.dev.azure.com)."""

    def __init__(self, http, org: str, project: str) -> None:
        super().__init__(http)
        self._base = f"https://almsearch.dev.azure.com/{org}/{project}/_apis/search"
        self._params = {"api-version": API_VERSION}

    def code(
        self,
        search_text: str,
        *,
        top: int = 25,
        skip: int = 0,
        filters: dict[str, list[str]] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "searchText": search_text,
            "$skip": skip,
            "$top": top,
            "includeFacets": True,
        }
        if filters:
            body["filters"] = filters
        if order_by:
            body["$orderBy"] = order_by
        return self._post(f"{self._base}/codesearchresults", json=body, params=self._params)

    def work_items(
        self,
        search_text: str,
        *,
        top: int = 25,
        skip: int = 0,
        filters: dict[str, list[str]] | None = None,
        order_by: list[dict[str, str]] | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "searchText": search_text,
            "$skip": skip,
            "$top": top,
            "includeFacets": True,
        }
        if filters:
            body["filters"] = filters
        if order_by:
            body["$orderBy"] = order_by
        return self._post(
            f"{self._base}/workitemsearchresults", json=body, params=self._params
        )

    def wiki(
        self,
        search_text: str,
        *,
        top: int = 25,
        skip: int = 0,
        filters: dict[str, list[str]] | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "searchText": search_text,
            "$skip": skip,
            "$top": top,
            "includeFacets": True,
        }
        if filters:
            body["filters"] = filters
        return self._post(f"{self._base}/wikisearchresults", json=body, params=self._params)
