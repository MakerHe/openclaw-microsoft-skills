"""Device Code Flow (OAuth2) authentication via Microsoft Entra ID."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

import httpx


GRAPH_SCOPE = "https://graph.microsoft.com/.default"
ADO_SCOPE = "499b84ac-1321-427f-aa17-267ca6975798/.default"

_GRAPH_HOST = "graph.microsoft.com"
_ADO_HOST = "dev.azure.com"
_VSSPS_HOST = "vssps.visualstudio.com"

_CREDENTIALS_DIR = Path.home() / ".openclaw" / "credentials"

# Credential file names
_REFRESH_TOKEN_FILE = "refresh_token.json"
_TOKEN_FILES: dict[str, str] = {
    GRAPH_SCOPE: "microsoft365.json",
    ADO_SCOPE:   "azuredevops.json",
}

# Minimum remaining lifetime (seconds) before a token is proactively refreshed.
_REFRESH_THRESHOLD = 30 * 60  # 30 minutes


class RefreshResult(NamedTuple):
    """Return value of :meth:`DeviceCodeAuth.refresh_credentials`."""

    refreshed: bool
    issued_at: datetime | None
    expired: bool


@dataclass
class DeviceCodeAuth(httpx.Auth):
    """httpx-compatible auth that uses Device Code Flow to obtain Bearer tokens.

    Credential files in ``~/.openclaw/credentials/``:
    - ``refresh_token.json``  — shared refresh token (all resources)
    - ``microsoft365.json``   — Graph access token
    - ``azuredevops.json``    — Azure DevOps access token
    """

    client_id: str
    tenant_id: str = "common"
    client_secret: str | None = None
    primary_scope: str = GRAPH_SCOPE
    credentials_dir: Path = field(default=None, repr=False)

    _tokens: dict[str, tuple[str, float]] = field(
        default_factory=dict, init=False, repr=False
    )
    _refresh_token: str | None = field(default=None, init=False, repr=False)
    _issued_at: float | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.credentials_dir is None:
            self.credentials_dir = _CREDENTIALS_DIR
        self._load_tokens()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def _token_url(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

    @property
    def _device_code_url(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/devicecode"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def authenticate(self, scope: str = GRAPH_SCOPE, *, extra_scopes: list[str] | None = None, print_fn=print) -> None:
        """Obtain a Bearer token for *scope*.

        - If a valid access token exists on disk: returns immediately.
        - If a refresh token exists: silently acquires a new access token.
          If the refresh token cannot be used for this resource (cross-resource
          refresh not supported), falls through to interactive login without
          clearing the refresh token or other resources' tokens.
        - Otherwise: runs the interactive Device Code Flow.

        ``extra_scopes`` are acquired silently via refresh token after the
        primary scope is obtained (best-effort; failures are ignored).
        """
        # Check if access token already valid
        key = self._scope_key(scope)
        token_info = self._tokens.get(key)
        if token_info is not None:
            _, expires_at = token_info
            if time.time() < expires_at:
                print_fn("Authentication successful (existing token is still valid).")
                if extra_scopes:
                    self._acquire_extra_scopes(extra_scopes)
                return

        if self._refresh_token:
            try:
                self._refresh_for_scope(scope)
                if extra_scopes:
                    self._acquire_extra_scopes(extra_scopes)
                print_fn("Authentication successful (token refreshed silently).")
                return
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (400, 401):
                    # Refresh token cannot be used for this resource — fall
                    # through to interactive login. Do NOT clear the refresh
                    # token; it may still be valid for other resources.
                    print_fn(
                        "Saved refresh token cannot be used for this resource — "
                        "falling back to interactive login."
                    )
                else:
                    raise

        # Interactive: device code flow
        scope_str = self._build_scope(scope)
        with httpx.Client() as client:
            resp = client.post(
                self._device_code_url,
                data={"client_id": self.client_id, "scope": scope_str},
            )
            resp.raise_for_status()
            data = resp.json()

            print_fn(data["message"])
            device_code = data["device_code"]
            interval = data.get("interval", 5)

            while True:
                time.sleep(interval)
                token_data_req = {
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "client_id": self.client_id,
                    "device_code": device_code,
                }
                token_data_req.update(self._extra_params())
                token_resp = client.post(self._token_url, data=token_data_req)
                token_data = token_resp.json()
                error = token_data.get("error")

                if not error:
                    self._store_tokens(scope, token_data)
                    if extra_scopes:
                        self._acquire_extra_scopes(extra_scopes)
                    return
                if error == "authorization_pending":
                    continue
                if error == "slow_down":
                    interval += 5
                    continue
                raise RuntimeError(
                    f"Device code auth failed: {error} — {token_data.get('error_description', '')}"
                )

    def _acquire_extra_scopes(self, scopes: list[str]) -> None:
        """Silently acquire tokens for extra scopes using the refresh token.

        Per Microsoft identity platform docs, a refresh token issued for one
        resource can be used to obtain access tokens for any resource the app
        has consent for.  Failures are ignored (best-effort).
        """
        for s in scopes:
            key = self._scope_key(s)
            token_info = self._tokens.get(key)
            if token_info is not None:
                _, expires_at = token_info
                if time.time() < expires_at:
                    continue
            try:
                self._refresh_for_scope(s)
            except (httpx.HTTPStatusError, RuntimeError):
                pass

    def acquire_token(self, scope: str) -> None:
        """Silently acquire a token for a resource using the refresh token."""
        if not self._refresh_token:
            raise RuntimeError("No refresh token — call authenticate() first")
        self._refresh_for_scope(scope)

    def refresh_credentials(self) -> RefreshResult:
        """Proactively refresh tokens that are close to expiry (< 30 min remaining)."""
        if not self._tokens:
            return RefreshResult(refreshed=False, issued_at=None, expired=False)

        now = time.time()
        refreshed = False
        any_expired = False

        for scope_key, (_, expires_at) in list(self._tokens.items()):
            remaining = expires_at - now
            if remaining <= 0:
                if not self._refresh_token:
                    any_expired = True
                    continue
                self._refresh_for_scope(scope_key)
                refreshed = True
            elif remaining < _REFRESH_THRESHOLD:
                self._refresh_for_scope(scope_key)
                refreshed = True

        issued_at = (
            datetime.fromtimestamp(self._issued_at, tz=timezone.utc)
            if self._issued_at is not None
            else None
        )
        return RefreshResult(refreshed=refreshed, issued_at=issued_at, expired=any_expired)

    # ------------------------------------------------------------------
    # httpx.Auth protocol
    # ------------------------------------------------------------------

    def auth_flow(self, request: httpx.Request):
        url = str(request.url)
        token = self._get_token_for_url(url)
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_scope(self, scope: str) -> str:
        parts = scope.split()
        if "offline_access" not in parts:
            parts.append("offline_access")
        return " ".join(parts)

    def _extra_params(self) -> dict:
        if self.client_secret:
            return {"client_secret": self.client_secret}
        return {}

    def _scope_key(self, scope: str) -> str:
        parts = [p for p in scope.split() if p != "offline_access"]
        return " ".join(parts)

    def _token_file(self, scope_key: str) -> Path:
        """Return the access token file path for the given scope key."""
        for scope, filename in _TOKEN_FILES.items():
            if self._scope_key(scope) == scope_key:
                return self.credentials_dir / filename
        # fallback: derive from first URL component
        return self.credentials_dir / "tokens.json"

    def _refresh_token_file(self) -> Path:
        return self.credentials_dir / _REFRESH_TOKEN_FILE

    def _refresh_for_scope(self, scope: str) -> None:
        """Use the refresh token to get a new access token for the given scope."""
        if not self._refresh_token:
            raise RuntimeError("No refresh token available — call authenticate() first")
        scope_str = self._build_scope(scope)
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self._refresh_token,
            "scope": scope_str,
        }
        data.update(self._extra_params())
        with httpx.Client() as client:
            resp = client.post(self._token_url, data=data)
            # AADSTS700025: public-client apps must not present client_secret.
            # Retry without it when the server rejects the secret.
            if resp.status_code == 401 and self.client_secret and "700025" in resp.text:
                data.pop("client_secret", None)
                resp = client.post(self._token_url, data=data)
            resp.raise_for_status()
            self._store_tokens(scope, resp.json())

    def _clear_credentials(self, scope: str | None = None) -> None:
        """Remove tokens from memory and disk.

        If *scope* is given, only that resource's access token file is removed.
        The shared refresh_token.json is only removed when scope is None.
        """
        if scope is None:
            self._tokens.clear()
            self._refresh_token = None
            self._issued_at = None
            for filename in list(_TOKEN_FILES.values()) + [_REFRESH_TOKEN_FILE]:
                path = self.credentials_dir / filename
                if path.exists():
                    path.unlink()
        else:
            key = self._scope_key(scope)
            self._tokens.pop(key, None)
            token_file = self._token_file(key)
            if token_file.exists():
                token_file.unlink()
            # Keep _refresh_token and refresh_token.json intact

    def _store_tokens(self, scope: str, data: dict) -> None:
        """Store access token for scope and persist to disk.

        The refresh token is written to its own file; the access token is
        written to the resource-specific file.
        """
        access_token = data["access_token"]
        expires_at = time.time() + data.get("expires_in", 3600) - 60
        key = self._scope_key(scope)
        self._tokens[key] = (access_token, expires_at)
        self._issued_at = time.time()

        if data.get("refresh_token"):
            self._refresh_token = data["refresh_token"]
            self._save_refresh_token()

        self._save_access_token(key, access_token, expires_at)

    def _save_refresh_token(self) -> None:
        """Persist the refresh token to its own file."""
        self.credentials_dir.mkdir(parents=True, exist_ok=True)
        self._refresh_token_file().write_text(
            json.dumps({"refresh_token": self._refresh_token, "issued_at": self._issued_at}, indent=2)
        )

    def _save_access_token(self, scope_key: str, access_token: str, expires_at: float) -> None:
        """Persist a single access token to its resource file."""
        self.credentials_dir.mkdir(parents=True, exist_ok=True)
        path = self._token_file(scope_key)
        payload = {"access_token": access_token, "expires_at": expires_at}
        path.write_text(json.dumps(payload, indent=2))

    def _load_tokens(self) -> None:
        """Load persisted tokens from disk into memory."""
        # Load shared refresh token first
        rt_file = self._refresh_token_file()
        if rt_file.exists():
            try:
                payload = json.loads(rt_file.read_text())
                self._refresh_token = payload.get("refresh_token")
                self._issued_at = payload.get("issued_at")
            except (json.JSONDecodeError, OSError):
                pass

        # Load access tokens from each resource file
        for scope, filename in _TOKEN_FILES.items():
            path = self.credentials_dir / filename
            if not path.exists():
                continue
            try:
                payload = json.loads(path.read_text())
                key = self._scope_key(scope)
                self._tokens[key] = (payload["access_token"], payload["expires_at"])
            except (json.JSONDecodeError, OSError, KeyError):
                continue

    def _get_token_for_url(self, url: str) -> str:
        if _ADO_HOST in url or _VSSPS_HOST in url:
            return self._get_or_refresh(ADO_SCOPE)
        return self._get_or_refresh(GRAPH_SCOPE)

    def _get_or_refresh(self, scope: str) -> str:
        """Return a valid access token for scope, refreshing if needed."""
        key = self._scope_key(scope)
        token_info = self._tokens.get(key)
        if token_info is None:
            if self._refresh_token:
                try:
                    self._refresh_for_scope(scope)
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code in (400, 401):
                        raise RuntimeError(
                            f"Cannot acquire token for scope '{scope}' — "
                            "call authenticate() to log in for this resource."
                        ) from exc
                    raise
                token_info = self._tokens.get(key)
            if token_info is None:
                raise RuntimeError(
                    f"No token for scope '{scope}' — call authenticate() first"
                )
        access_token, expires_at = token_info
        if time.time() >= expires_at:
            try:
                self._refresh_for_scope(scope)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (400, 401):
                    self._clear_credentials(scope)
                    raise RuntimeError(
                        "Access token expired and refresh failed — call authenticate() to log in again."
                    ) from exc
                raise
            access_token, _ = self._tokens[key]
        return access_token
