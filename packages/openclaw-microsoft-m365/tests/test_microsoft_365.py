"""Unit tests for Microsoft365Client."""

from __future__ import annotations

import httpx
import pytest
import respx

from openclaw_microsoft_m365.auth.device_code import DeviceCodeAuth, GRAPH_SCOPE
from openclaw_microsoft_m365.client import Microsoft365Client
from openclaw_microsoft_m365._base import APIError


GRAPH_BASE = "https://graph.microsoft.com/v1.0"
ME = f"{GRAPH_BASE}/me"


# ---- helpers ----------------------------------------------------------------


def _inject_token(auth: DeviceCodeAuth, token: str = "graph-access-token") -> None:
    """Manually inject a token into the auth object, bypassing device code flow."""
    key = auth._scope_key(GRAPH_SCOPE)
    auth._tokens[key] = (token, float("inf"))
    auth._refresh_token = "rt-dummy"


def _make_client() -> Microsoft365Client:
    client = Microsoft365Client(client_id="test-client-id", tenant_id="test-tenant")
    _inject_token(client._device_auth)
    return client


# ---- auth header tests -------------------------------------------------------


class TestAuthHeaders:
    @respx.mock
    def test_bearer_header_sent(self):
        """Requests include Bearer Authorization header."""
        respx.get(f"{ME}/messages").mock(
            return_value=httpx.Response(200, json={"value": []})
        )
        with _make_client() as client:
            client.mail.list_messages(top=1)
        request = respx.calls.last.request
        assert request.headers["authorization"] == "Bearer graph-access-token"


# ---- mail -------------------------------------------------------------------


class TestMail:
    @respx.mock
    def test_list_messages(self):
        """list_messages() calls correct endpoint and returns results."""
        expected = {"value": [{"id": "msg1", "subject": "Hello"}]}
        respx.get(f"{ME}/messages").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.mail.list_messages()
        assert result == expected

    @respx.mock
    def test_get_message(self):
        """get_message() fetches a specific message by ID."""
        expected = {"id": "msg1", "subject": "Test"}
        respx.get(f"{ME}/messages/msg1").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.mail.get_message("msg1")
        assert result == expected

    @respx.mock
    def test_send_mail(self):
        """send() posts to sendMail endpoint and succeeds on 202."""
        respx.post(f"{ME}/sendMail").mock(
            return_value=httpx.Response(202)
        )
        with _make_client() as client:
            # Should not raise
            client.mail.send("user@example.com", subject="Hi", body="Hello")

    @respx.mock
    def test_list_folders(self):
        """list_folders() calls mailFolders endpoint."""
        expected = {"value": [{"id": "inbox", "displayName": "Inbox"}]}
        respx.get(f"{ME}/mailFolders").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.mail.list_folders()
        assert result == expected


# ---- calendar ---------------------------------------------------------------


class TestCalendar:
    @respx.mock
    def test_list_events(self):
        """list_events() calls correct Graph calendar endpoint."""
        expected = {"value": [{"id": "ev1", "subject": "Meeting"}]}
        respx.get(f"{ME}/events").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.calendar.list_events()
        assert result == expected


# ---- onedrive ---------------------------------------------------------------


class TestOneDrive:
    @respx.mock
    def test_list_drive_items(self):
        """list_root() calls OneDrive root children endpoint."""
        expected = {"value": [{"id": "file1", "name": "doc.txt"}]}
        respx.get(f"{GRAPH_BASE}/me/drive/root/children").mock(
            return_value=httpx.Response(200, json=expected)
        )
        with _make_client() as client:
            result = client.onedrive.list_root()
        assert result == expected


# ---- error handling ---------------------------------------------------------


class TestErrorHandling:
    @respx.mock
    def test_404_raises_api_error(self):
        """APIError is raised on 404 response."""
        respx.get(f"{ME}/messages/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": {"message": "Not found"}})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.mail.get_message("nonexistent")
        assert exc_info.value.status_code == 404

    @respx.mock
    def test_401_raises_api_error(self):
        """APIError is raised on 401 Unauthorized."""
        respx.get(f"{ME}/messages").mock(
            return_value=httpx.Response(401, json={"error": {"message": "Unauthorized"}})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.mail.list_messages()
        assert exc_info.value.status_code == 401

    @respx.mock
    def test_500_raises_api_error(self):
        """APIError is raised on 500 Server Error."""
        respx.get(f"{ME}/messages").mock(
            return_value=httpx.Response(500, json={"error": {"message": "Server Error"}})
        )
        with _make_client() as client:
            with pytest.raises(APIError) as exc_info:
                client.mail.list_messages()
        assert exc_info.value.status_code == 500
