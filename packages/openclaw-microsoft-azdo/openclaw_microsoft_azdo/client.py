"""Azure DevOps client — main entry point."""

from __future__ import annotations

import os
from pathlib import Path

import httpx

from openclaw_microsoft_azdo._base import load_env_file
from openclaw_microsoft_azdo.auth.device_code import DeviceCodeAuth, ADO_SCOPE, GRAPH_SCOPE
from openclaw_microsoft_azdo.auth.pat import PATAuth
from openclaw_microsoft_azdo.artifacts import Artifacts
from openclaw_microsoft_azdo.audit import Audit
from openclaw_microsoft_azdo.boards_backlogs import BoardsBacklogs
from openclaw_microsoft_azdo.builds import Builds
from openclaw_microsoft_azdo.dashboards import Dashboards
from openclaw_microsoft_azdo.extensions import Extensions
from openclaw_microsoft_azdo.git_repos import GitRepos
from openclaw_microsoft_azdo.graph_identity import GraphIdentity
from openclaw_microsoft_azdo.notifications import Notifications
from openclaw_microsoft_azdo.pipelines import Pipelines
from openclaw_microsoft_azdo.policy import Policy
from openclaw_microsoft_azdo.projects_teams import ProjectsTeams
from openclaw_microsoft_azdo.releases import Releases
from openclaw_microsoft_azdo.search import Search
from openclaw_microsoft_azdo.security import Security
from openclaw_microsoft_azdo.service_endpoints import ServiceEndpoints
from openclaw_microsoft_azdo.service_hooks import ServiceHooks
from openclaw_microsoft_azdo.test_plans import TestPlans
from openclaw_microsoft_azdo.wiki import Wiki
from openclaw_microsoft_azdo.work_items import WorkItems

_ENV_FILE = Path.home() / ".openclaw" / ".env"


class AzureDevOpsClient:
    """High-level client for Azure DevOps REST APIs.

    Supports two authentication modes:

    * **PAT** — pass ``pat`` to the constructor.
    * **Device Code Flow** — pass ``client_id`` (and optionally ``tenant_id``),
      then call :meth:`authenticate`.
    """

    def __init__(
        self,
        org: str,
        project: str,
        *,
        pat: str | None = None,
        client_id: str | None = None,
        tenant_id: str = "common",
        client_secret: str | None = None,
        team: str | None = None,
        device_auth: DeviceCodeAuth | None = None,
    ) -> None:
        self.org = org
        self.project = project
        self.team = team or project

        base_url = f"https://dev.azure.com/{org}"

        if pat:
            auth: httpx.Auth = PATAuth(pat)
        elif device_auth:
            self._device_auth = device_auth
            auth = self._device_auth
        elif client_id:
            self._device_auth = DeviceCodeAuth(
                client_id=client_id,
                tenant_id=tenant_id,
                client_secret=client_secret,
                primary_scope=ADO_SCOPE,
            )
            auth = self._device_auth
        else:
            raise ValueError("Provide either 'pat', 'client_id', or 'device_auth' for authentication")

        self._http = httpx.Client(auth=auth, timeout=30.0)

        # Core services
        self.work_items = WorkItems(self._http, base_url, project)
        self.git_repos = GitRepos(self._http, base_url, project)
        self.pipelines = Pipelines(self._http, base_url, project)
        self.builds = Builds(self._http, base_url, project)
        self.releases = Releases(self._http, org, project)
        self.test_plans = TestPlans(self._http, base_url, project)
        self.artifacts = Artifacts(self._http, org, project)
        self.wiki = Wiki(self._http, base_url, project)
        self.projects_teams = ProjectsTeams(self._http, base_url, project)
        self.boards_backlogs = BoardsBacklogs(self._http, base_url, project, self.team)
        self.service_hooks = ServiceHooks(self._http, base_url)
        self.security = Security(self._http, base_url)
        self.graph_identity = GraphIdentity(self._http, org)
        self.dashboards = Dashboards(self._http, base_url, project, self.team)
        self.search = Search(self._http, org, project)
        self.notifications = Notifications(self._http, base_url)
        self.audit = Audit(self._http, org)
        self.extensions = Extensions(self._http, org)
        self.service_endpoints = ServiceEndpoints(self._http, base_url, project)
        self.policy = Policy(self._http, base_url, project)

    def authenticate(self, *, print_fn=print, **kwargs) -> None:
        """Run Device Code Flow (only needed when using client_id auth)."""
        if not hasattr(self, "_device_auth"):
            raise RuntimeError("authenticate() is only for Device Code Flow auth")
        self._device_auth.authenticate(
            scope=ADO_SCOPE,
            extra_scopes=[GRAPH_SCOPE],
            print_fn=print_fn,
            **kwargs,
        )
        resp = self._http.get(
            "https://app.vssps.visualstudio.com/_apis/profile/profiles/me",
            params={"api-version": "7.1"},
        )
        if resp.status_code == 200:
            me = resp.json()
            name = me.get("displayName", "")
            email = me.get("emailAddress", "")
            print_fn(f"Signed in as: {name} <{email}>")
        projects = self.projects_teams.list_projects()
        count = projects.get("count", len(projects.get("value", [])))
        print_fn(f"Organization: {self.org}  |  Projects: {count}  |  Default project: {self.project}")

    @classmethod
    def from_env(cls, env_file: Path | None = None, *, device_auth: DeviceCodeAuth | None = None) -> "AzureDevOpsClient":
        """Construct a client from ``~/.openclaw/.env`` (or a custom path)."""
        env = load_env_file(env_file or _ENV_FILE)

        def _get(key: str) -> str | None:
            return env.get(key) or os.environ.get(key)

        org = _get("AZURE_DEVOPS_ORG")
        if not org:
            raise ValueError(
                "AZURE_DEVOPS_ORG not found in ~/.openclaw/.env "
                "or environment variables"
            )
        project = _get("AZURE_DEVOPS_PROJECT")
        if not project:
            raise ValueError(
                "AZURE_DEVOPS_PROJECT not found in ~/.openclaw/.env "
                "or environment variables"
            )
        team = _get("AZURE_DEVOPS_TEAM")
        pat = _get("AZURE_DEVOPS_PAT")
        client_id = _get("MICROSOFT_CLIENT_ID")
        tenant_id = _get("MICROSOFT_TENANT_ID") or "common"
        client_secret = _get("MICROSOFT_CLIENT_SECRET")

        if not pat and not client_id and not device_auth:
            raise ValueError(
                "Provide AZURE_DEVOPS_PAT or MICROSOFT_CLIENT_ID in "
                "~/.openclaw/.env or environment variables"
            )
        return cls(
            org=org,
            project=project,
            pat=pat,
            client_id=client_id,
            tenant_id=tenant_id,
            client_secret=client_secret,
            team=team,
            device_auth=device_auth,
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
