"""Azure Artifacts / Package Management service."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_azdo._base import BaseService

API_VERSION = "7.1"


class Artifacts(BaseService):
    """Azure DevOps Artifacts (feeds.dev.azure.com) API."""

    def __init__(self, http, org: str, project: str) -> None:
        super().__init__(http)
        self._org_base = f"https://feeds.dev.azure.com/{org}/_apis/packaging"
        self._proj_base = f"https://feeds.dev.azure.com/{org}/{project}/_apis/packaging"
        self._params = {"api-version": API_VERSION}

    # -- Feeds ------------------------------------------------------------

    def list_feeds(self, *, project_scoped: bool = False) -> dict:
        base = self._proj_base if project_scoped else self._org_base
        return self._get(f"{base}/feeds", params=self._params)

    def get_feed(self, feed_id: str) -> dict:
        return self._get(f"{self._org_base}/feeds/{feed_id}", params=self._params)

    def create_feed(self, name: str, *, description: str = "", upstream_enabled: bool = True) -> dict:
        return self._post(
            f"{self._org_base}/feeds",
            json={
                "name": name,
                "description": description,
                "hideDeletedPackageVersions": True,
                "upstreamEnabled": upstream_enabled,
            },
            params=self._params,
        )

    def delete_feed(self, feed_id: str) -> None:
        self._delete(f"{self._org_base}/feeds/{feed_id}", params=self._params)

    # -- Packages ---------------------------------------------------------

    def list_packages(self, feed_id: str) -> dict:
        return self._get(f"{self._org_base}/feeds/{feed_id}/packages", params=self._params)

    def list_package_versions(self, feed_id: str, package_id: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/packages/{package_id}/versions",
            params=self._params,
        )

    # -- Protocol-specific ------------------------------------------------

    def get_nuget_version(self, feed_id: str, package_name: str, version: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/nuget/packages/{package_name}/versions/{version}",
            params=self._params,
        )

    def delete_nuget_version(self, feed_id: str, package_name: str, version: str) -> None:
        self._delete(
            f"{self._org_base}/feeds/{feed_id}/nuget/packages/{package_name}/versions/{version}",
            params=self._params,
        )

    def get_npm_version(self, feed_id: str, package_name: str, version: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/npm/{package_name}/versions/{version}",
            params=self._params,
        )

    def delete_npm_version(self, feed_id: str, package_name: str, version: str) -> None:
        self._delete(
            f"{self._org_base}/feeds/{feed_id}/npm/{package_name}/versions/{version}",
            params=self._params,
        )

    def get_maven_version(
        self, feed_id: str, group_id: str, artifact_id: str, version: str
    ) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/maven/{group_id}/{artifact_id}/versions/{version}",
            params=self._params,
        )

    def get_pypi_version(self, feed_id: str, package_name: str, version: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/pypi/packages/{package_name}/versions/{version}",
            params=self._params,
        )

    def list_upack_versions(self, feed_id: str, package_name: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/upack/packages/{package_name}/versions",
            params=self._params,
        )

    # -- Views ------------------------------------------------------------

    def list_views(self, feed_id: str) -> dict:
        return self._get(f"{self._org_base}/feeds/{feed_id}/views", params=self._params)

    # -- Recycle Bin -------------------------------------------------------

    def list_recycle_bin(self, feed_id: str) -> dict:
        return self._get(
            f"{self._org_base}/feeds/{feed_id}/recyclebin/packages", params=self._params
        )
