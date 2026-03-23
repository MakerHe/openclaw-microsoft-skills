"""Unit tests for DeviceCodeAuth."""

from __future__ import annotations

import json
import time
from pathlib import Path

import httpx
import pytest
import respx


from openclaw_microsoft_azdo.auth.device_code import (
    DeviceCodeAuth,
    GRAPH_SCOPE,
    ADO_SCOPE,
)


TENANT = "test-tenant"
CLIENT_ID = "test-client-id"
CLIENT_SECRET = "test-secret"

DEVICE_CODE_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/devicecode"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"


def _device_code_response():
    return {
        "device_code": "device-code-abc",
        "user_code": "ABC123",
        "verification_uri": "https://microsoft.com/devicelogin",
        "message": "Go to https://microsoft.com/devicelogin and enter ABC123",
        "interval": 1,
        "expires_in": 900,
    }


def _token_response(access_token="at-graph", refresh_token="rt-1", expires_in=3600):
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "scope": GRAPH_SCOPE,
    }


def _write_refresh_token(tmp_path: Path, refresh_token: str, issued_at: float | None = None) -> None:
    """Write refresh_token.json."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "refresh_token.json").write_text(json.dumps({
        "refresh_token": refresh_token,
        "issued_at": issued_at or time.time(),
    }))


def _write_access_token(tmp_path: Path, filename: str, access_token: str, expires_at: float) -> None:
    """Write a resource access token file."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / filename).write_text(json.dumps({
        "access_token": access_token,
        "expires_at": expires_at,
    }))


def _make_auth(tmp_path: Path, **kwargs) -> DeviceCodeAuth:
    return DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT, credentials_dir=tmp_path, **kwargs)


class TestDeviceCodeFlow:
    @pytest.fixture(autouse=True)
    def isolated_creds(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "openclaw_microsoft_azdo.auth.device_code._CREDENTIALS_DIR", tmp_path
        )

    @respx.mock
    def test_authenticate_basic(self):
        """Device code flow completes and stores tokens."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        messages = []
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=messages.append)

        assert auth._refresh_token == "rt-1"
        key = auth._scope_key(GRAPH_SCOPE)
        assert key in auth._tokens
        assert auth._tokens[key][0] == "at-graph"
        assert "Go to" in messages[0]

    @respx.mock
    def test_authenticate_includes_offline_access(self):
        """Scope sent to devicecode endpoint always includes offline_access."""
        captured = {}

        def capture_request(request):
            captured["scope"] = request.content.decode()
            return httpx.Response(200, json=_device_code_response())

        respx.post(DEVICE_CODE_URL).mock(side_effect=capture_request)
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        assert "offline_access" in captured["scope"]
        assert "graph.microsoft.com" in captured["scope"]

    @respx.mock
    def test_authenticate_authorization_pending_then_success(self):
        """Polls through authorization_pending before getting token."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        responses = [
            httpx.Response(200, json={"error": "authorization_pending"}),
            httpx.Response(200, json={"error": "authorization_pending"}),
            httpx.Response(200, json=_token_response()),
        ]
        respx.post(TOKEN_URL).mock(side_effect=responses)

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        assert auth._refresh_token == "rt-1"

    @respx.mock
    def test_authenticate_slow_down(self):
        """slow_down error increases interval and retries."""
        dc = _device_code_response()
        dc["interval"] = 1
        respx.post(DEVICE_CODE_URL).mock(return_value=httpx.Response(200, json=dc))
        responses = [
            httpx.Response(200, json={"error": "slow_down"}),
            httpx.Response(200, json=_token_response()),
        ]
        respx.post(TOKEN_URL).mock(side_effect=responses)

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        assert auth._refresh_token == "rt-1"

    @respx.mock
    def test_authenticate_error_raises(self):
        """Non-recoverable error raises RuntimeError."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(
                200,
                json={"error": "expired_token", "error_description": "Token expired"},
            )
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        with pytest.raises(RuntimeError, match="expired_token"):
            auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

    @respx.mock
    def test_client_secret_included_in_token_request(self):
        """client_secret is sent in token request when set."""
        captured = {}

        def capture_token_req(request):
            captured["body"] = request.content.decode()
            return httpx.Response(200, json=_token_response())

        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(side_effect=capture_token_req)

        auth = DeviceCodeAuth(
            client_id=CLIENT_ID, tenant_id=TENANT, client_secret=CLIENT_SECRET
        )
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        assert "client_secret=test-secret" in captured["body"]

    @respx.mock
    def test_no_client_secret_when_not_set(self):
        """client_secret is NOT sent when not configured."""
        captured = {}

        def capture_token_req(request):
            captured["body"] = request.content.decode()
            return httpx.Response(200, json=_token_response())

        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(side_effect=capture_token_req)

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        assert "client_secret" not in captured["body"]


class TestMultiResourceTokens:
    @pytest.fixture(autouse=True)
    def isolated_creds(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "openclaw_microsoft_azdo.auth.device_code._CREDENTIALS_DIR", tmp_path
        )

    @respx.mock
    def test_acquire_token_for_ado_via_refresh(self):
        """acquire_token uses refresh token to get ADO token silently."""
        ado_token_resp = {
            "access_token": "at-ado",
            "refresh_token": "rt-2",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=_token_response()),
                httpx.Response(200, json=ado_token_resp),
            ]
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        auth.acquire_token(scope=ADO_SCOPE)

        graph_key = auth._scope_key(GRAPH_SCOPE)
        ado_key = auth._scope_key(ADO_SCOPE)
        assert auth._tokens[graph_key][0] == "at-graph"
        assert auth._tokens[ado_key][0] == "at-ado"
        assert auth._refresh_token == "rt-2"

    @respx.mock
    def test_acquire_token_without_authenticate_raises(self, tmp_path):
        """acquire_token without prior authenticate raises RuntimeError."""
        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT, credentials_dir=tmp_path)
        with pytest.raises(RuntimeError, match="authenticate"):
            auth.acquire_token(scope=ADO_SCOPE)

    @respx.mock
    def test_acquire_token_sends_offline_access(self):
        """Refresh token exchange includes offline_access."""
        captured = {}

        def capture(request):
            captured["body"] = request.content.decode()
            return httpx.Response(200, json=_token_response(access_token="at-ado"))

        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=_token_response()),
                capture,
            ]
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        auth.acquire_token(scope=ADO_SCOPE)

        assert "offline_access" in captured["body"]

    @respx.mock
    def test_client_secret_in_refresh_request(self):
        """client_secret is included in refresh token exchange."""
        captured = {}

        def capture(request):
            captured["body"] = request.content.decode()
            return httpx.Response(200, json=_token_response(access_token="at-ado"))

        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=_token_response()),
                capture,
            ]
        )

        auth = DeviceCodeAuth(
            client_id=CLIENT_ID, tenant_id=TENANT, client_secret=CLIENT_SECRET
        )
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        auth.acquire_token(scope=ADO_SCOPE)

        assert "client_secret=test-secret" in captured["body"]


class TestTokenExpiry:
    @pytest.fixture(autouse=True)
    def isolated_creds(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "openclaw_microsoft_azdo.auth.device_code._CREDENTIALS_DIR", tmp_path
        )

    @respx.mock
    def test_auto_refresh_on_expiry(self):
        """auth_flow auto-refreshes token when expired."""
        initial_resp = _token_response(access_token="at-old", expires_in=3600)
        refreshed_resp = _token_response(access_token="at-new", refresh_token="rt-2")

        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=initial_resp),
                httpx.Response(200, json=refreshed_resp),
            ]
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        key = auth._scope_key(GRAPH_SCOPE)
        auth._tokens[key] = ("at-old", 0.0)

        request = httpx.Request("GET", "https://graph.microsoft.com/v1.0/me")
        list(auth.auth_flow(request))

        assert request.headers["Authorization"] == "Bearer at-new"

    def test_auth_flow_no_token_raises(self, tmp_path):
        """auth_flow raises if no token for the resource."""
        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT, credentials_dir=tmp_path)
        request = httpx.Request("GET", "https://graph.microsoft.com/v1.0/me")
        with pytest.raises(RuntimeError, match="authenticate"):
            list(auth.auth_flow(request))


class TestAuthFlow:
    @pytest.fixture(autouse=True)
    def isolated_creds(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "openclaw_microsoft_azdo.auth.device_code._CREDENTIALS_DIR", tmp_path
        )

    @respx.mock
    def test_auth_flow_picks_graph_token_for_graph_url(self):
        """auth_flow uses Graph token for graph.microsoft.com URLs."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response(access_token="at-graph"))
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        request = httpx.Request("GET", "https://graph.microsoft.com/v1.0/me")
        list(auth.auth_flow(request))
        assert request.headers["Authorization"] == "Bearer at-graph"

    @respx.mock
    def test_auth_flow_picks_ado_token_for_ado_url(self):
        """auth_flow uses ADO token for dev.azure.com URLs."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=_token_response()),
                httpx.Response(200, json=_token_response(access_token="at-ado")),
            ]
        )

        auth = DeviceCodeAuth(client_id=CLIENT_ID, tenant_id=TENANT)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        auth.acquire_token(scope=ADO_SCOPE)

        request = httpx.Request("GET", "https://dev.azure.com/myorg/_apis/projects")
        list(auth.auth_flow(request))
        assert request.headers["Authorization"] == "Bearer at-ado"


class TestTokenPersistence:
    @respx.mock
    def test_tokens_saved_after_authenticate(self, tmp_path):
        """authenticate() persists access token to microsoft365.json and refresh to refresh_token.json."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )

        auth = _make_auth(tmp_path)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)

        # Access token in resource file
        m365_file = tmp_path / "microsoft365.json"
        assert m365_file.exists()
        payload = json.loads(m365_file.read_text())
        assert payload["access_token"] == "at-graph"

        # Refresh token in its own file
        rt_file = tmp_path / "refresh_token.json"
        assert rt_file.exists()
        rt_payload = json.loads(rt_file.read_text())
        assert rt_payload["refresh_token"] == "rt-1"

    @respx.mock
    def test_ado_tokens_saved_to_azuredevops_json(self, tmp_path):
        """Azure DevOps access token is persisted to azuredevops.json."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            side_effect=[
                httpx.Response(200, json=_token_response()),
                httpx.Response(200, json=_token_response(access_token="at-ado", refresh_token="rt-2")),
            ]
        )

        auth = _make_auth(tmp_path)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        auth.acquire_token(scope=ADO_SCOPE)

        ado_file = tmp_path / "azuredevops.json"
        assert ado_file.exists()
        payload = json.loads(ado_file.read_text())
        assert payload["access_token"] == "at-ado"

    def test_tokens_loaded_on_construction(self, tmp_path):
        """Tokens written to disk are loaded into a new DeviceCodeAuth instance."""
        _write_refresh_token(tmp_path, "saved-rt")
        _write_access_token(tmp_path, "microsoft365.json", "saved-token", time.time() + 3600)

        auth = _make_auth(tmp_path)

        assert auth._refresh_token == "saved-rt"
        graph_key = auth._scope_key(GRAPH_SCOPE)
        assert auth._tokens[graph_key][0] == "saved-token"

    def test_load_skips_corrupt_file(self, tmp_path):
        """Corrupt credentials file is silently skipped."""
        (tmp_path / "microsoft365.json").write_text("not json {{{")
        auth = _make_auth(tmp_path)
        assert auth._tokens == {}
        assert auth._refresh_token is None

    def test_no_reauthentication_needed_with_valid_saved_token(self, tmp_path):
        """auth_flow uses saved token without calling authenticate."""
        _write_refresh_token(tmp_path, "cached-rt")
        _write_access_token(tmp_path, "microsoft365.json", "cached-token", time.time() + 3600)

        auth = _make_auth(tmp_path)
        request = httpx.Request("GET", "https://graph.microsoft.com/v1.0/me")
        list(auth.auth_flow(request))
        assert request.headers["Authorization"] == "Bearer cached-token"


class TestSilentAuthenticate:
    @respx.mock
    def test_authenticate_silent_when_refresh_token_present(self, tmp_path):
        """authenticate() uses refresh token silently — no device-code prompt."""
        _write_refresh_token(tmp_path, "saved-rt")

        refreshed = _token_response(access_token="at-silent", refresh_token="rt-2")
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=refreshed))

        messages = []
        auth = _make_auth(tmp_path)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=messages.append)

        assert not any("Go to" in m or "sign in" in m.lower() for m in messages)
        graph_key = auth._scope_key(GRAPH_SCOPE)
        assert auth._tokens[graph_key][0] == "at-silent"
        assert auth._refresh_token == "rt-2"

    @respx.mock
    def test_authenticate_falls_back_to_device_code_without_refresh_token(self, tmp_path):
        """authenticate() runs device-code flow when no refresh token exists."""
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )

        messages = []
        auth = _make_auth(tmp_path)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=messages.append)

        assert "Go to" in messages[0]
        assert auth._refresh_token == "rt-1"

    @respx.mock
    def test_authenticate_silent_uses_ado_fallback_refresh_token(self, tmp_path):
        """M365 authenticate() can use a refresh token saved from a prior ADO login."""
        _write_refresh_token(tmp_path, "ado-saved-rt")
        _write_access_token(tmp_path, "azuredevops.json", "at-ado-old", time.time() + 3600)

        refreshed = _token_response(access_token="at-graph-new", refresh_token="rt-rotated")
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=refreshed))

        messages = []
        auth = DeviceCodeAuth(
            client_id=CLIENT_ID, tenant_id=TENANT,
            primary_scope=GRAPH_SCOPE, credentials_dir=tmp_path,
        )
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=messages.append)

        assert not any("Go to" in m or "sign in" in m.lower() for m in messages)
        graph_key = auth._scope_key(GRAPH_SCOPE)
        assert auth._tokens[graph_key][0] == "at-graph-new"


class TestPrimaryScopeLoadOrder:
    def test_refresh_token_shared_across_resources(self, tmp_path):
        """refresh_token.json is shared — both M365 and ADO clients read the same token."""
        _write_refresh_token(tmp_path, "shared-rt")

        auth_m365 = DeviceCodeAuth(
            client_id=CLIENT_ID, tenant_id=TENANT,
            primary_scope=GRAPH_SCOPE, credentials_dir=tmp_path,
        )
        auth_ado = DeviceCodeAuth(
            client_id=CLIENT_ID, tenant_id=TENANT,
            primary_scope=ADO_SCOPE, credentials_dir=tmp_path,
        )
        assert auth_m365._refresh_token == "shared-rt"
        assert auth_ado._refresh_token == "shared-rt"

    def test_access_tokens_loaded_independently(self, tmp_path):
        """Each resource's access token is loaded from its own file."""
        _write_refresh_token(tmp_path, "rt")
        _write_access_token(tmp_path, "microsoft365.json", "at-m365", time.time() + 3600)
        _write_access_token(tmp_path, "azuredevops.json", "at-ado", time.time() + 3600)

        auth = _make_auth(tmp_path)
        graph_key = auth._scope_key(GRAPH_SCOPE)
        ado_key = auth._scope_key(ADO_SCOPE)
        assert auth._tokens[graph_key][0] == "at-m365"
        assert auth._tokens[ado_key][0] == "at-ado"


class TestRefreshCredentials:
    @pytest.fixture(autouse=True)
    def isolated_creds(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "openclaw_microsoft_azdo.auth.device_code._CREDENTIALS_DIR", tmp_path
        )

    def _write_creds(self, tmp_path: Path, expires_in: float) -> None:
        _write_refresh_token(tmp_path, "rt-existing")
        _write_access_token(tmp_path, "microsoft365.json", "at-existing", time.time() + expires_in)

    def test_no_credentials_returns_no_issued_at(self, tmp_path):
        auth = _make_auth(tmp_path)
        result = auth.refresh_credentials()
        assert result.refreshed is False
        assert result.issued_at is None
        assert result.expired is False

    @respx.mock
    def test_skips_refresh_when_more_than_30_minutes_remain(self, tmp_path):
        self._write_creds(tmp_path, expires_in=3600)
        auth = _make_auth(tmp_path)
        result = auth.refresh_credentials()
        assert result.refreshed is False
        assert result.expired is False
        assert not respx.calls

    @respx.mock
    def test_refreshes_when_less_than_30_minutes_remain(self, tmp_path):
        self._write_creds(tmp_path, expires_in=1000)
        refreshed_resp = _token_response(access_token="at-refreshed", refresh_token="rt-new")
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=refreshed_resp))

        auth = _make_auth(tmp_path)
        result = auth.refresh_credentials()

        assert result.refreshed is True
        assert result.expired is False
        graph_key = auth._scope_key(GRAPH_SCOPE)
        assert auth._tokens[graph_key][0] == "at-refreshed"

    @respx.mock
    def test_refreshes_fully_expired_token(self, tmp_path):
        self._write_creds(tmp_path, expires_in=-60)
        refreshed_resp = _token_response(access_token="at-renewed", refresh_token="rt-new2")
        respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=refreshed_resp))

        auth = _make_auth(tmp_path)
        result = auth.refresh_credentials()
        assert result.refreshed is True
        assert result.expired is False

    def test_expired_without_refresh_token(self, tmp_path):
        _write_access_token(tmp_path, "microsoft365.json", "at-dead", time.time() - 60)
        # No refresh_token.json

        auth = _make_auth(tmp_path)
        result = auth.refresh_credentials()
        assert result.expired is True
        assert result.refreshed is False

    @respx.mock
    def test_issued_at_saved_and_loaded(self, tmp_path):
        respx.post(DEVICE_CODE_URL).mock(
            return_value=httpx.Response(200, json=_device_code_response())
        )
        respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json=_token_response())
        )
        before = time.time()
        auth = _make_auth(tmp_path)
        auth.authenticate(scope=GRAPH_SCOPE, print_fn=lambda _: None)
        after = time.time()

        rt_payload = json.loads((tmp_path / "refresh_token.json").read_text())
        assert before <= rt_payload["issued_at"] <= after

        auth2 = _make_auth(tmp_path)
        assert auth2._issued_at is not None
        assert before <= auth2._issued_at <= after
