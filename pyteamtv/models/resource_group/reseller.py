from . import _ResourceGroup

from .capabilities import _HasTeamsMixin, _HasSportingEventsMixin, _HasVideosMixin


class ResellerResourceGroup(
    _ResourceGroup, _HasTeamsMixin, _HasSportingEventsMixin, _HasVideosMixin
):
    pass
