"""Microsoft To Do service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me/todo"


class ToDo(BaseService):
    """Microsoft Graph To Do API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    # -- Task Lists -------------------------------------------------------

    def list_task_lists(self) -> dict:
        return self._get(f"{BASE}/lists")

    def get_task_list(self, list_id: str) -> dict:
        return self._get(f"{BASE}/lists/{list_id}")

    def create_task_list(self, display_name: str) -> dict:
        return self._post(f"{BASE}/lists", json={"displayName": display_name})

    def update_task_list(self, list_id: str, display_name: str) -> dict:
        return self._patch(f"{BASE}/lists/{list_id}", json={"displayName": display_name})

    def delete_task_list(self, list_id: str) -> None:
        self._delete(f"{BASE}/lists/{list_id}")

    # -- Tasks ------------------------------------------------------------

    def list_tasks(self, list_id: str, *, filter: str | None = None) -> dict:
        params: dict[str, str] = {}
        if filter:
            params["$filter"] = filter
        return self._get(f"{BASE}/lists/{list_id}/tasks", params=params or None)

    def get_task(self, list_id: str, task_id: str) -> dict:
        return self._get(f"{BASE}/lists/{list_id}/tasks/{task_id}")

    def create_task(
        self,
        list_id: str,
        title: str,
        *,
        importance: str | None = None,
        body: str | None = None,
        body_type: str = "text",
        due_date: str | None = None,
        time_zone: str = "UTC",
    ) -> dict:
        task: dict[str, Any] = {"title": title}
        if importance:
            task["importance"] = importance
        if body:
            task["body"] = {"content": body, "contentType": body_type}
        if due_date:
            task["dueDateTime"] = {"dateTime": due_date, "timeZone": time_zone}
        return self._post(f"{BASE}/lists/{list_id}/tasks", json=task)

    def update_task(self, list_id: str, task_id: str, updates: dict[str, Any]) -> dict:
        return self._patch(f"{BASE}/lists/{list_id}/tasks/{task_id}", json=updates)

    def delete_task(self, list_id: str, task_id: str) -> None:
        self._delete(f"{BASE}/lists/{list_id}/tasks/{task_id}")

    # -- Checklist Items --------------------------------------------------

    def list_checklist_items(self, list_id: str, task_id: str) -> dict:
        return self._get(f"{BASE}/lists/{list_id}/tasks/{task_id}/checklistItems")

    def add_checklist_item(self, list_id: str, task_id: str, display_name: str) -> dict:
        return self._post(
            f"{BASE}/lists/{list_id}/tasks/{task_id}/checklistItems",
            json={"displayName": display_name},
        )

    def update_checklist_item(
        self, list_id: str, task_id: str, item_id: str, *, is_checked: bool
    ) -> dict:
        return self._patch(
            f"{BASE}/lists/{list_id}/tasks/{task_id}/checklistItems/{item_id}",
            json={"isChecked": is_checked},
        )

    # -- Linked Resources -------------------------------------------------

    def add_linked_resource(
        self,
        list_id: str,
        task_id: str,
        *,
        web_url: str,
        application_name: str,
        display_name: str,
    ) -> dict:
        return self._post(
            f"{BASE}/lists/{list_id}/tasks/{task_id}/linkedResources",
            json={
                "webUrl": web_url,
                "applicationName": application_name,
                "displayName": display_name,
            },
        )
