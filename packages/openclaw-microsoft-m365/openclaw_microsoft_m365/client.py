"""Microsoft 365 client — main entry point."""

from __future__ import annotations

import os
from pathlib import Path

import httpx

from openclaw_microsoft_m365._base import load_env_file
from openclaw_microsoft_m365.auth.device_code import DeviceCodeAuth, GRAPH_SCOPE, ADO_SCOPE
from openclaw_microsoft_m365.calendar import Calendar
from openclaw_microsoft_m365.contacts import Contacts
from openclaw_microsoft_m365.mail import Mail
from openclaw_microsoft_m365.onedrive import OneDrive
from openclaw_microsoft_m365.onenote import OneNote
from openclaw_microsoft_m365.sharepoint import SharePoint
from openclaw_microsoft_m365.teams import Teams
from openclaw_microsoft_m365.todo import ToDo
from openclaw_microsoft_m365.users_groups import UsersGroups

_ENV_FILE = Path.home() / ".openclaw" / ".env"


class Microsoft365Client:
    """High-level client for Microsoft 365 via Microsoft Graph API.

    Uses Device Code Flow (OAuth2) for authentication.  After constructing,
    call :meth:`authenticate` to trigger the interactive login.

    Environment variables can be stored in ``~/.openclaw/.env``:

    .. code-block:: ini

        MICROSOFT_CLIENT_ID=<app-id>
        MICROSOFT_TENANT_ID=<tenant-id>
        MICROSOFT_CLIENT_SECRET=<secret>  # optional
    """

    def __init__(
        self,
        client_id: str,
        *,
        tenant_id: str = "common",
        client_secret: str | None = None,
        device_auth: DeviceCodeAuth | None = None,
    ) -> None:
        self._device_auth = device_auth or DeviceCodeAuth(
            client_id=client_id,
            tenant_id=tenant_id,
            client_secret=client_secret,
            primary_scope=GRAPH_SCOPE,
        )
        self._initial_scope = GRAPH_SCOPE
        self._http = httpx.Client(auth=self._device_auth, timeout=30.0)

        self.mail = Mail(self._http)
        self.calendar = Calendar(self._http)
        self.onedrive = OneDrive(self._http)
        self.teams = Teams(self._http)
        self.onenote = OneNote(self._http)
        self.todo = ToDo(self._http)
        self.contacts = Contacts(self._http)
        self.users_groups = UsersGroups(self._http)
        self.sharepoint = SharePoint(self._http)

    @classmethod
    def from_env(cls, env_file: Path | None = None, *, device_auth: DeviceCodeAuth | None = None) -> "Microsoft365Client":
        """Construct a client from ``~/.openclaw/.env`` (or a custom path).

        Falls back to ``MICROSOFT_CLIENT_ID`` / ``MICROSOFT_TENANT_ID`` /
        ``MICROSOFT_CLIENT_SECRET`` environment variables if the file is absent.

        Raises :exc:`ValueError` if ``MICROSOFT_CLIENT_ID`` cannot be resolved
        and no ``device_auth`` is provided.
        """
        env = load_env_file(env_file or _ENV_FILE)
        client_id = env.get("MICROSOFT_CLIENT_ID") or os.environ.get("MICROSOFT_CLIENT_ID")
        if not client_id and not device_auth:
            raise ValueError(
                "MICROSOFT_CLIENT_ID not found in ~/.openclaw/.env "
                "or environment variables"
            )
        tenant_id = (
            env.get("MICROSOFT_TENANT_ID")
            or os.environ.get("MICROSOFT_TENANT_ID")
            or "common"
        )
        client_secret = env.get("MICROSOFT_CLIENT_SECRET") or os.environ.get(
            "MICROSOFT_CLIENT_SECRET"
        )
        return cls(client_id=client_id or "", tenant_id=tenant_id, client_secret=client_secret, device_auth=device_auth)

    def authenticate(self, *, print_fn=print, **kwargs) -> None:
        """Run Device Code Flow — prints a URL and code for the user to enter.

        After successful authentication, prints the signed-in user's basic info.
        """
        self._device_auth.authenticate(extra_scopes=[ADO_SCOPE], print_fn=print_fn, **kwargs)
        me = self.users_groups.get_me()
        name = me.get("displayName", "")
        email = me.get("mail") or me.get("userPrincipalName", "")
        print_fn(f"Signed in as: {name} <{email}>")

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
