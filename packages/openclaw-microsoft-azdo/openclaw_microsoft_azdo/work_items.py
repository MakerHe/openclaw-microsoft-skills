"""Work Item Tracking service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class WorkItems(BaseService):
    """Azure DevOps Work Item Tracking API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._base = f"{base_url}/{project}/_apis/wit"
        self._params = {"api-version": API_VERSION}

    def get(
        self,
        work_item_id: int,
        *,
        fields: list[str] | None = None,
        expand: str | None = None,
    ) -> dict:
        params = dict(self._params)
        if fields:
            params["$fields"] = ",".join(fields)
        if expand:
            params["$expand"] = expand
        return self._get(f"{self._base}/workitems/{work_item_id}", params=params)

    def get_batch(
        self,
        ids: list[int],
        *,
        fields: list[str] | None = None,
    ) -> dict:
        params = dict(self._params)
        if not fields:
            return self._get(
                f"{self._base}/workitems",
                params={**params, "ids": ",".join(str(i) for i in ids)},
            )
        body: dict[str, Any] = {"ids": ids}
        if fields:
            body["fields"] = fields
        return self._post(f"{self._base}/workitemsbatch", json=body, params=params)

    def create(
        self,
        work_item_type: str,
        *,
        title: str,
        description: str | None = None,
        assigned_to: str | None = None,
        priority: int | None = None,
        extra_fields: dict[str, Any] | None = None,
    ) -> dict:
        ops: list[dict] = [{"op": "add", "path": "/fields/System.Title", "value": title}]
        if description:
            ops.append({"op": "add", "path": "/fields/System.Description", "value": description})
        if assigned_to:
            ops.append({"op": "add", "path": "/fields/System.AssignedTo", "value": assigned_to})
        if priority is not None:
            ops.append(
                {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority}
            )
        for k, v in (extra_fields or {}).items():
            ops.append({"op": "add", "path": f"/fields/{k}", "value": v})
        return self._request(
            "POST",
            f"{self._base}/workitems/${work_item_type}",
            json=ops,
            params=self._params,
            content_type="application/json-patch+json",
        ).json()

    def update(self, work_item_id: int, fields: dict[str, Any]) -> dict:
        ops = [{"op": "replace", "path": f"/fields/{k}", "value": v} for k, v in fields.items()]
        return self._request(
            "PATCH",
            f"{self._base}/workitems/{work_item_id}",
            json=ops,
            params=self._params,
            content_type="application/json-patch+json",
        ).json()

    def delete(self, work_item_id: int, *, destroy: bool = False) -> None:
        params = dict(self._params)
        if destroy:
            params["destroy"] = "true"
        self._delete(f"{self._base}/workitems/{work_item_id}", params=params)

    def query(self, wiql: str) -> dict:
        return self._post(f"{self._base}/wiql", json={"query": wiql}, params=self._params)

    def add_comment(self, work_item_id: int, text: str) -> dict:
        return self._post(
            f"{self._base}/workitems/{work_item_id}/comments",
            json={"text": text},
            params={"api-version": "7.1-preview.4"},
        )

    def list_comments(self, work_item_id: int) -> dict:
        return self._get(
            f"{self._base}/workitems/{work_item_id}/comments",
            params={"api-version": "7.1-preview.4"},
        )

    def add_relation(
        self,
        work_item_id: int,
        target_id: int,
        relation_type: str = "System.LinkTypes.Hierarchy-Forward",
    ) -> dict:
        target_url = f"{self._base}/workitems/{target_id}"
        ops = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {"rel": relation_type, "url": target_url},
            }
        ]
        return self._request(
            "PATCH",
            f"{self._base}/workitems/{work_item_id}",
            json=ops,
            params=self._params,
            content_type="application/json-patch+json",
        ).json()

    def list_types(self) -> dict:
        return self._get(f"{self._base}/workitemtypes", params=self._params)

    def list_revisions(self, work_item_id: int) -> dict:
        return self._get(f"{self._base}/workitems/{work_item_id}/revisions", params=self._params)

    def list_recycle_bin(self) -> dict:
        return self._get(f"{self._base}/recyclebin", params=self._params)

    def restore(self, work_item_id: int) -> dict:
        return self._request(
            "PATCH",
            f"{self._base}/recyclebin/{work_item_id}",
            json={"IsDeleted": False},
            params=self._params,
            content_type="application/json-patch+json",
        ).json()
