"""Zimbra MCP server configuration."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class ZimbraConfig:
    """Configuration for Zimbra connection."""

    url: str
    user: str
    password: str
    timeout: int = 30
    enable_send: bool = False
    # A ready-made auth token, used instead of signing in with the password (for example one issued by a
    # local Zimbra Desktop backend, or a delegated token from an administrator).
    auth_token: str | None = None

    @classmethod
    def from_env(cls) -> "ZimbraConfig":
        """Load configuration from environment variables."""
        load_dotenv()

        url = os.getenv("ZIMBRA_URL")
        user = os.getenv("ZIMBRA_USER")
        password = os.getenv("ZIMBRA_PASSWORD")
        auth_token = os.getenv("ZIMBRA_AUTH_TOKEN") or None
        timeout = int(os.getenv("ZIMBRA_TIMEOUT", "30"))
        enable_send = os.getenv("ZIMBRA_ENABLE_SEND", "").lower() in ("true", "1", "yes")

        if not url:
            raise ValueError("ZIMBRA_URL not defined")
        if not user:
            raise ValueError("ZIMBRA_USER not defined")
        if not password and not auth_token:
            raise ValueError("ZIMBRA_PASSWORD not defined (or set ZIMBRA_AUTH_TOKEN)")

        return cls(
            url=url,
            user=user,
            password=password or "",
            timeout=timeout,
            enable_send=enable_send,
            auth_token=auth_token,
        )
