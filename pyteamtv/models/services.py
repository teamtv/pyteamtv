from dataclasses import dataclass
from typing import Optional


@dataclass
class ServiceEndpoint:
    url: str
    token: Optional[str] = None


class Services:
    def __init__(self, attributes: dict):
        self._attributes = attributes
        self._endpoints: dict[str, ServiceEndpoint] = {}

        for name, config in attributes.items():
            self._endpoints[name] = ServiceEndpoint(
                url=config.get("url", ""),
                token=config.get("token"),
            )

    @property
    def notifications(self) -> Optional[ServiceEndpoint]:
        return self._endpoints.get("notifications")

    @property
    def data(self) -> Optional[ServiceEndpoint]:
        return self._endpoints.get("data")

    def get(self, name: str) -> Optional[ServiceEndpoint]:
        return self._endpoints.get(name)

    def __contains__(self, name: str) -> bool:
        return name in self._endpoints
