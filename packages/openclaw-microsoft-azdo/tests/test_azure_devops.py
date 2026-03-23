"""Unit tests for AzureDevOpsClient."""

from __future__ import annotations

import httpx
import pytest
import respx

from openclaw_microsoft_azdo.auth.device_code import DeviceCodeAuth, ADO_SCOPE
from openclaw_microsoft_azdo.client import AzureDevOpsClient
from openclaw_microsoft_azdo._base import APIError


ORG = "myorg"
PROJECT = "myproject"
BASE = f"https://dev.azure.com/{ORG}"

# ---- helpers ----------------------------------------------------------------


def _inject_token(auth: DeviceCodeAuth, token: str = "ado-access-token") -> None:
    """Manually inject a token into the auth object, bypassing device code flow."""
    key = auth._scope_key(ADO_SCOPE)
    auth._tokens[key] = (token, float("inf"))
    auth._refresh_token = "rt-dummy"


def _make_client(pat: str | None = None) -> AzureDevOpsClient:
    if pat:
        return AzureDevOpsClient(ORG, PROJECT, pat=pat)
    client = AzureDevOpsClient(ORG, PROJECT, client_id="test-client-id", tenant_id="test-tenant")
    _inject_token(client._device_auth)
    return client


# ---- auth header tests -------------------------------------------------------


class TestAuthHeaders:
    @respx.mock
    def test_pat_auth_sends_basic_header(self):
        """PAT auth sends Basic Authorization header."""
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/1").mock(
            return_value=httpx.Response(200, json={"id": 1, "fields": {}})
        )
        with _make_client(pat="my-pat") as client:
            client.work_items.get(1)
        request = respx.calls.last.request
        assert request.headers["authorization"].startswith("Basic ")

    @respx.mock
    def test_device_auth_sends_bearer_header(self):
        """Device Code auth sends Bearer Authorization header."""
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/1").mock(
            return_value=httpx.Response(200, json={"id": 1, "fields": {}})
        )
        with _make_client() as client:
            client.work_items.get(1)
        request = respx.calls.last.request
        assert request.headers["authorization"] == "Bearer ado-access-token"

    def test_no_auth_raises(self):
        """Constructor without pat or client_id raises ValueError."""
        with pytest.raises(ValueError, match="pat.*client_id"):
            AzureDevOpsClient(ORG, PROJECT)


# ---- work items -------------------------------------------------------------


class TestWorkItems:
    @respx.mock
    def test_get_work_item(self):
        """get() calls correct URL and returns parsed JSON."""
        expected = {"id": 42, "fields": {"System.Title": "Hello"}}
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/42").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.work_items.get(42)
        assert result == expected

    @respx.mock
    def test_query_work_items(self):
        """query() posts WIQL and returns results."""
        wiql = "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project"
        expected = {"queryType": "flat", "workItems": [{"id": 1}]}
        respx.post(f"{BASE}/{PROJECT}/_apis/wit/wiql").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.work_items.query(wiql)
        assert result == expected

    @respx.mock
    def test_api_error_raised_on_4xx(self):
        """APIError is raised when server returns 404."""
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/999").mock(
            return_value=httpx.Response(404, json={"message": "Not found"})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.work_items.get(999)
        assert exc_info.value.status_code == 404


# ---- git repos --------------------------------------------------------------


class TestGitRepos:
    @respx.mock
    def test_list_repos(self):
        """list() calls correct Git repos endpoint."""
        expected = {"value": [{"id": "abc", "name": "myrepo"}]}
        respx.get(f"{BASE}/{PROJECT}/_apis/git/repositories").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.git_repos.list_repos()
        assert result == expected


# ---- pipelines --------------------------------------------------------------


class TestPipelines:
    @respx.mock
    def test_list_pipelines(self):
        """list() calls correct pipelines endpoint."""
        expected = {"value": [{"id": 1, "name": "Build"}]}
        respx.get(f"{BASE}/{PROJECT}/_apis/pipelines").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.pipelines.list()
        assert result == expected


# ---- error handling ---------------------------------------------------------


class TestErrorHandling:
    @respx.mock
    def test_500_raises_api_error(self):
        """Server 500 raises APIError."""
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/1").mock(
            return_value=httpx.Response(500, json={"message": "Internal Server Error"})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.work_items.get(1)
        assert exc_info.value.status_code == 500

    @respx.mock
    def test_401_raises_api_error(self):
        """Unauthorized 401 raises APIError."""
        respx.get(f"{BASE}/{PROJECT}/_apis/wit/workitems/1").mock(
            return_value=httpx.Response(401, json={"message": "Unauthorized"})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.work_items.get(1)
        assert exc_info.value.status_code == 401
