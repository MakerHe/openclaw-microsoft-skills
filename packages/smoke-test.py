#!/usr/bin/env python3
"""
Smoke Test — Authentication & Core Functionality
Covers: Microsoft 365 and Azure DevOps

Usage:
    python packages/smoke-test.py           # run all
    python packages/smoke-test.py m365      # M365 only
    python packages/smoke-test.py ado       # Azure DevOps only
"""

from __future__ import annotations

import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

PASS = "✅"
FAIL = "❌"
results: list[tuple[str, str, str]] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    icon = PASS if ok else FAIL
    print(f"{icon} [{status}] {name}" + (f" — {detail}" if detail else ""))
    results.append((name, status, detail))


def section(title: str) -> None:
    print(f"\n── {title} ──")


# ---------------------------------------------------------------------------
# Shared auth helper
# ---------------------------------------------------------------------------

def _build_shared_auth():
    """Create a single DeviceCodeAuth used by both M365 and AzDO clients."""
    from openclaw_microsoft_m365.auth.device_code import DeviceCodeAuth
    from openclaw_microsoft_m365._base import load_env_file

    env_file = Path.home() / ".openclaw" / ".env"
    env = load_env_file(env_file)
    client_id = env.get("MICROSOFT_CLIENT_ID") or os.environ.get("MICROSOFT_CLIENT_ID")
    tenant_id = env.get("MICROSOFT_TENANT_ID") or os.environ.get("MICROSOFT_TENANT_ID") or "common"
    client_secret = env.get("MICROSOFT_CLIENT_SECRET") or os.environ.get("MICROSOFT_CLIENT_SECRET")

    if not client_id:
        raise ValueError("MICROSOFT_CLIENT_ID not found in ~/.openclaw/.env or environment variables")

    auth = DeviceCodeAuth(
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
    )
    return auth


# ---------------------------------------------------------------------------
# Microsoft 365
# ---------------------------------------------------------------------------

def smoke_m365(shared_auth=None) -> None:
    from openclaw_microsoft_m365.client import Microsoft365Client

    section("Microsoft 365: Authenticate")
    try:
        client = Microsoft365Client.from_env(device_auth=shared_auth)
        client.authenticate()
        report("m365_authenticate", True)
    except Exception as exc:
        report("m365_authenticate", False, str(exc))
        traceback.print_exc()
        return

    section("Microsoft 365: Get current user (/me)")
    try:
        me = client.users_groups.get_me()
        name = me.get("displayName", "")
        email = me.get("mail") or me.get("userPrincipalName", "")
        report("m365_get_me", bool(name or email), f"{name} <{email}>")
    except Exception as exc:
        report("m365_get_me", False, str(exc))
        traceback.print_exc()
    finally:
        client.close()


# ---------------------------------------------------------------------------
# Azure DevOps
# ---------------------------------------------------------------------------

def smoke_ado(shared_auth=None) -> None:
    from openclaw_microsoft_azdo.client import AzureDevOpsClient

    section("Azure DevOps: Authenticate")
    try:
        client = AzureDevOpsClient.from_env(device_auth=shared_auth)
        client.authenticate()
        report("ado_authenticate", True)
    except Exception as exc:
        report("ado_authenticate", False, str(exc))
        traceback.print_exc()
        return

    section("Azure DevOps: List projects")
    try:
        data = client.projects_teams.list_projects()
        projects = data.get("value", [])
        count = data.get("count", len(projects))
        for p in projects[:5]:
            print(f"  • {p['name']}")
        report("ado_list_projects", count >= 0, f"{count} projects")
    except Exception as exc:
        report("ado_list_projects", False, str(exc))
        traceback.print_exc()
    finally:
        client.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SUITES = {"m365": smoke_m365, "ado": smoke_ado}


def main() -> None:
    print("=" * 50)
    print(f" Smoke Test — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 50)

    requested = sys.argv[1].lower() if len(sys.argv) > 1 else None
    shared_auth = _build_shared_auth()

    if requested:
        fn = SUITES.get(requested)
        if not fn:
            print(f"Unknown suite '{requested}'. Available: {', '.join(SUITES)}")
            sys.exit(1)
        fn(shared_auth)
    else:
        for fn in SUITES.values():
            fn(shared_auth)

    passed = sum(1 for _, s, _ in results if s == "PASS")
    failed = sum(1 for _, s, _ in results if s == "FAIL")

    print("\n" + "=" * 50)
    print(f" SUMMARY: {passed} passed, {failed} failed")
    print("=" * 50)
    for name, status, detail in results:
        icon = PASS if status == "PASS" else FAIL
        print(f"  {icon} {name}" + (f" — {detail}" if detail else ""))

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
