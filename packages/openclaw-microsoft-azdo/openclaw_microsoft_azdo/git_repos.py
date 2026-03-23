"""Git Repositories & Pull Requests service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class GitRepos(BaseService):
    """Azure DevOps Git Repositories & Pull Requests API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/git"
        self._params = {"api-version": API_VERSION}

    # -- Repositories -----------------------------------------------------

    def list_repos(self) -> dict:
        return self._get(f"{self._base}/repositories", params=self._params)

    def get_repo(self, repo_id: str) -> dict:
        return self._get(f"{self._base}/repositories/{repo_id}", params=self._params)

    def create_repo(self, name: str) -> dict:
        return self._post(
            f"{self._base}/repositories", json={"name": name}, params=self._params
        )

    def delete_repo(self, repo_id: str) -> None:
        self._delete(f"{self._base}/repositories/{repo_id}", params=self._params)

    # -- Branches / Refs --------------------------------------------------

    def list_branches(self, repo_id: str) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/refs",
            params={**self._params, "filter": "heads/"},
        )

    def list_tags(self, repo_id: str) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/refs",
            params={**self._params, "filter": "tags/"},
        )

    def create_branch(
        self, repo_id: str, branch_name: str, source_commit_id: str
    ) -> dict:
        return self._post(
            f"{self._base}/repositories/{repo_id}/refs",
            json=[
                {
                    "name": f"refs/heads/{branch_name}",
                    "oldObjectId": "0" * 40,
                    "newObjectId": source_commit_id,
                }
            ],
            params=self._params,
        )

    def delete_branch(
        self, repo_id: str, branch_name: str, current_commit_id: str
    ) -> dict:
        return self._post(
            f"{self._base}/repositories/{repo_id}/refs",
            json=[
                {
                    "name": f"refs/heads/{branch_name}",
                    "oldObjectId": current_commit_id,
                    "newObjectId": "0" * 40,
                }
            ],
            params=self._params,
        )

    # -- Commits ----------------------------------------------------------

    def list_commits(self, repo_id: str, *, branch: str = "main") -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/commits",
            params={**self._params, "searchCriteria.itemVersion.version": branch},
        )

    def get_commit(self, repo_id: str, commit_id: str) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/commits/{commit_id}",
            params=self._params,
        )

    def get_commit_diffs(
        self, repo_id: str, base_version: str, target_version: str
    ) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/diffs/commits",
            params={
                **self._params,
                "baseVersion": base_version,
                "targetVersion": target_version,
            },
        )

    # -- Items (files) ----------------------------------------------------

    def get_file(
        self, repo_id: str, path: str, *, include_content: bool = False
    ) -> Any:
        params = {**self._params, "path": path}
        if include_content:
            params["includeContent"] = "true"
        return self._get(f"{self._base}/repositories/{repo_id}/items", params=params)

    def list_directory(
        self, repo_id: str, scope_path: str, *, recursion: str = "OneLevel"
    ) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/items",
            params={
                **self._params,
                "scopePath": scope_path,
                "recursionLevel": recursion,
            },
        )

    # -- Pull Requests ----------------------------------------------------

    def list_pull_requests(
        self,
        repo_id: str,
        *,
        status: str = "active",
        creator_id: str | None = None,
    ) -> dict:
        params = {**self._params, "searchCriteria.status": status}
        if creator_id:
            params["searchCriteria.creatorId"] = creator_id
        return self._get(
            f"{self._base}/repositories/{repo_id}/pullrequests", params=params
        )

    def get_pull_request(self, repo_id: str, pr_id: int) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}",
            params=self._params,
        )

    def create_pull_request(
        self,
        repo_id: str,
        *,
        source_branch: str,
        target_branch: str = "main",
        title: str,
        description: str = "",
        reviewer_ids: list[str] | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "sourceRefName": f"refs/heads/{source_branch}",
            "targetRefName": f"refs/heads/{target_branch}",
            "title": title,
            "description": description,
        }
        if reviewer_ids:
            body["reviewers"] = [{"id": rid} for rid in reviewer_ids]
        return self._post(
            f"{self._base}/repositories/{repo_id}/pullrequests",
            json=body,
            params=self._params,
        )

    def update_pull_request(
        self, repo_id: str, pr_id: int, updates: dict[str, Any]
    ) -> dict:
        return self._patch(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}",
            json=updates,
            params=self._params,
        )

    def add_reviewer(
        self, repo_id: str, pr_id: int, reviewer_id: str, *, vote: int = 0
    ) -> dict:
        return self._put(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}/reviewers/{reviewer_id}",
            json={"vote": vote},
            params=self._params,
        )

    # -- PR Threads -------------------------------------------------------

    def list_pr_threads(self, repo_id: str, pr_id: int) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}/threads",
            params=self._params,
        )

    def create_pr_thread(
        self, repo_id: str, pr_id: int, content: str, *, status: int = 1
    ) -> dict:
        return self._post(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}/threads",
            json={
                "comments": [
                    {"parentCommentId": 0, "content": content, "commentType": 1}
                ],
                "status": status,
            },
            params=self._params,
        )

    def list_pr_work_items(self, repo_id: str, pr_id: int) -> dict:
        return self._get(
            f"{self._base}/repositories/{repo_id}/pullrequests/{pr_id}/workitems",
            params=self._params,
        )

    # -- Push (file operations) -------------------------------------------

    def push(
        self,
        repo_id: str,
        *,
        branch: str,
        current_commit_id: str,
        commit_comment: str,
        changes: list[dict[str, Any]],
    ) -> dict:
        return self._post(
            f"{self._base}/repositories/{repo_id}/pushes",
            json={
                "refUpdates": [
                    {"name": f"refs/heads/{branch}", "oldObjectId": current_commit_id}
                ],
                "commits": [{"comment": commit_comment, "changes": changes}],
            },
            params=self._params,
        )
