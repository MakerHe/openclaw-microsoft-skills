"""Wiki service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Wiki(BaseService):
    """Azure DevOps Wiki API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/wiki"
        self._params = {"api-version": API_VERSION}

    def list_wikis(self) -> dict:
        return self._get(f"{self._base}/wikis", params=self._params)

    def get_wiki(self, wiki_id: str) -> dict:
        return self._get(f"{self._base}/wikis/{wiki_id}", params=self._params)

    def create_project_wiki(self, name: str) -> dict:
        return self._post(
            f"{self._base}/wikis",
            json={"name": name, "type": "projectWiki"},
            params=self._params,
        )

    def create_code_wiki(
        self, name: str, *, repo_id: str, branch: str = "main", mapped_path: str = "/docs"
    ) -> dict:
        return self._post(
            f"{self._base}/wikis",
            json={
                "name": name,
                "type": "codeWiki",
                "version": {"version": branch},
                "repositoryId": repo_id,
                "mappedPath": mapped_path,
            },
            params=self._params,
        )

    def get_page(self, wiki_id: str, path: str, *, include_content: bool = True) -> dict:
        params = {**self._params, "path": path}
        if include_content:
            params["includeContent"] = "true"
        return self._get(f"{self._base}/wikis/{wiki_id}/pages", params=params)

    def create_or_update_page(
        self, wiki_id: str, path: str, content: str, *, etag: str = "*"
    ) -> dict:
        return self._request(
            "PUT",
            f"{self._base}/wikis/{wiki_id}/pages",
            json={"content": content},
            params={**self._params, "path": path},
            headers={"If-Match": etag},
        ).json()

    def delete_page(self, wiki_id: str, path: str) -> None:
        self._delete(
            f"{self._base}/wikis/{wiki_id}/pages",
            params={**self._params, "path": path},
        )

    def list_page_stats(self, wiki_id: str) -> dict:
        return self._get(
            f"{self._base}/wikis/{wiki_id}/pagesstats",
            params={"api-version": "7.1-preview.1"},
        )

    def move_page(
        self, wiki_id: str, old_path: str, new_path: str, *, new_order: int = 0
    ) -> dict:
        return self._post(
            f"{self._base}/wikis/{wiki_id}/pagemoves",
            json={"path": old_path, "newPath": new_path, "newOrder": new_order},
            params=self._params,
        )

    def upload_attachment(
        self, wiki_id: str, name: str, data: bytes
    ) -> dict:
        return self._request(
            "PUT",
            f"{self._base}/wikis/{wiki_id}/attachments",
            content=data,
            params={**self._params, "name": name},
            content_type="application/octet-stream",
        ).json()
