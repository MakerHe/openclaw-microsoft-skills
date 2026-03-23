"""Test Plans & Test Management service for Azure DevOps."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class TestPlans(BaseService):
    """Azure DevOps Test Plans & Test Management API."""

    def __init__(self, http, base_url: str, project: str) -> None:
        super().__init__(http)
        self._plan_base = f"{base_url}/{project}/_apis/testplan"
        self._test_base = f"{base_url}/{project}/_apis/test"
        self._params = {"api-version": API_VERSION}

    # -- Test Plans -------------------------------------------------------

    def list_plans(self) -> dict:
        return self._get(f"{self._plan_base}/plans", params=self._params)

    def get_plan(self, plan_id: int) -> dict:
        return self._get(f"{self._plan_base}/plans/{plan_id}", params=self._params)

    def create_plan(
        self, name: str, *, area_path: str | None = None, iteration: str | None = None
    ) -> dict:
        body: dict[str, Any] = {"name": name}
        if area_path:
            body["areaPath"] = area_path
        if iteration:
            body["iteration"] = iteration
        return self._post(f"{self._plan_base}/plans", json=body, params=self._params)

    # -- Test Suites ------------------------------------------------------

    def list_suites(self, plan_id: int) -> dict:
        return self._get(f"{self._plan_base}/plans/{plan_id}/suites", params=self._params)

    def create_suite(
        self,
        plan_id: int,
        name: str,
        *,
        parent_suite_id: int | None = None,
        suite_type: str = "staticTestSuite",
    ) -> dict:
        body: dict[str, Any] = {"suiteType": suite_type, "name": name}
        if parent_suite_id:
            body["parentSuite"] = {"id": parent_suite_id}
        return self._post(
            f"{self._plan_base}/plans/{plan_id}/suites", json=body, params=self._params
        )

    # -- Test Cases -------------------------------------------------------

    def list_test_cases(self, plan_id: int, suite_id: int) -> dict:
        return self._get(
            f"{self._plan_base}/plans/{plan_id}/suites/{suite_id}/testcase",
            params=self._params,
        )

    def add_test_cases(self, plan_id: int, suite_id: int, work_item_ids: list[int]) -> dict:
        body = [{"workItem": {"id": wid}} for wid in work_item_ids]
        return self._post(
            f"{self._plan_base}/plans/{plan_id}/suites/{suite_id}/testcase",
            json=body,
            params=self._params,
        )

    # -- Test Runs --------------------------------------------------------

    def list_runs(self) -> dict:
        return self._get(f"{self._test_base}/runs", params=self._params)

    def create_run(
        self,
        name: str,
        *,
        plan_id: int,
        point_ids: list[int] | None = None,
        automated: bool = False,
    ) -> dict:
        body: dict[str, Any] = {
            "name": name,
            "plan": {"id": plan_id},
            "automated": automated,
        }
        if point_ids:
            body["pointIds"] = point_ids
        return self._post(f"{self._test_base}/runs", json=body, params=self._params)

    def get_run(self, run_id: int) -> dict:
        return self._get(f"{self._test_base}/runs/{run_id}", params=self._params)

    def complete_run(self, run_id: int) -> dict:
        return self._patch(
            f"{self._test_base}/runs/{run_id}",
            json={"state": "Completed"},
            params=self._params,
        )

    # -- Test Results -----------------------------------------------------

    def list_results(self, run_id: int) -> dict:
        return self._get(f"{self._test_base}/runs/{run_id}/results", params=self._params)

    def add_results(self, run_id: int, results: list[dict[str, Any]]) -> dict:
        return self._post(
            f"{self._test_base}/runs/{run_id}/results", json=results, params=self._params
        )

    # -- Test Points ------------------------------------------------------

    def list_points(self, plan_id: int, suite_id: int) -> dict:
        return self._get(
            f"{self._plan_base}/plans/{plan_id}/suites/{suite_id}/testpoint",
            params=self._params,
        )

    # -- Test Configurations ----------------------------------------------

    def list_configurations(self) -> dict:
        return self._get(f"{self._plan_base}/configurations", params=self._params)
