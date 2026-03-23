"""Authentication helpers for OpenClaw Skills."""

from openclaw_microsoft_azdo.auth.device_code import DeviceCodeAuth
from openclaw_microsoft_azdo.auth.pat import PATAuth

__all__ = ["DeviceCodeAuth", "PATAuth"]
