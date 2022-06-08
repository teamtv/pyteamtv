from ..teamtv_object import TeamTVObject
from .capabilities import _HasStorage


class _ResourceGroup(TeamTVObject, _HasStorage):
    def _use_attributes(self, attributes: dict):
        super()._use_attributes(attributes)

        self._name = attributes["targetResourceName"]
        self._tenant_id = attributes["tenantId"]
        self._resource_group_id = attributes["resourceGroupId"]

    @property
    def resource_group_id(self):
        return self._resource_group_id

    @property
    def name(self):
        return self._name

    @property
    def tenant_id(self):
        return self._tenant_id

    def __repr__(self):
        return f"<ResourceGroup name='{self.name}'>"

    def __eq__(self, other):
        if not isinstance(other, _ResourceGroup):
            return False

        return other.resource_group_id == self.resource_group_id
