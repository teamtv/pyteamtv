from . import _ResourceGroup

from .capabilities import (
    _HasTeamsMixin,
    _HasSportingEventsMixin,
    _HasVideosMixin,
    _HasPersonsMixin,
    _HasPlaylistsMixin,
    _HasCustomTagsMixin,
    _HasIcebergCatalogMixin,
)


class TeamResourceGroup(
    _ResourceGroup,
    _HasTeamsMixin,
    _HasSportingEventsMixin,
    _HasVideosMixin,
    _HasPersonsMixin,
    _HasPlaylistsMixin,
    _HasCustomTagsMixin,
    _HasIcebergCatalogMixin,
):
    pass
