"""PyTautulliHostConfiguration."""
from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import PyTautulliException


@dataclass
class PyTautulliHostConfiguration:
    """PyTautulliHostConfiguration."""

    api_token: str
    hostname: str | None = None
    ipaddress: str | None = None
    port: int | None = 8181
    ssl: bool = False
    verify_ssl: bool = True
    base_api_path: str | None = None
    url: str | None = None

    def __post_init__(self):
        """post init."""
        if self.api_token is None:
            raise PyTautulliException(
                message="No api token to the tautulli server was provided"
            )
        if self.hostname is None and self.ipaddress is None and self.url is None:
            raise PyTautulliException(
                message="No url, hostname or ipaddress to the tautulli server was provided"
            )

    def api_url(self, command: str) -> str:
        """Return the generated base URL based on host configuration."""
        return f"{self.base_url}/api/v2?apikey={self.api_token}&cmd={command}"

    @property
    def base_url(self) -> str:
        """Return the base URL for the configured service."""
        if self.url is not None:
            return self.url
        protocol = f"http{'s' if self.ssl else ''}"
        host = self.hostname or self.ipaddress
        if self.port:
            host = f"{host}:{str(self.port)}"
        return f"{protocol}://{host}{self.base_api_path or ''}"
