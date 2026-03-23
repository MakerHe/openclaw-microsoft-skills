"""Authentication helpers for OpenClaw Skills."""

from openclaw_microsoft_m365.auth.device_code import DeviceCodeAuth
from openclaw_microsoft_m365.auth.pat import PATAuth

__all__ = ["DeviceCodeAuth", "PATAuth"]
