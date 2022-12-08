from pyteamtv.infra.requester import Requester


class TeamTVObject(object):
    def __init__(self, requester: Requester, attributes: dict):
        self._requester = requester
        self.__attributes = attributes

        self._use_attributes(attributes)

    @property
    def metadata(self):
        return self._metadata

    def _use_attributes(self, attributes: dict):
        self._metadata = attributes.get("_metadata", {})

    def has_privilege(self, action: str) -> bool:
        for privilege, status in self.metadata.get("privilegesV2", {}).items():
            if privilege.endswith(":" + action):
                return status["ok"]
        return False
