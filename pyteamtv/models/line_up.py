from typing import Literal, NewType, Dict, TYPE_CHECKING

from .teamtv_object import TeamTVObject

if TYPE_CHECKING:
    from .person import Person
    from .team import Team

Position = NewType("Position", Literal["ATTACK", "DEFENCE"])


class LineUp(TeamTVObject):
    @property
    def line_up_id(self):
        return self._line_up_id

    @property
    def sporting_event(self):
        return self._sporting_event

    def sync_players(self, team: 'Team', positions: Dict['Person', Position]):
        self._requester.request(
            "POST",
            f"/lineUps/{self.line_up_id}/resetTeamLineUp",
            {
                'teamId': team.team_id
            }
        )
        for person, position in positions.items():
            self._requester.request(
                "POST",
                f"/lineUps/{self.line_up_id}/addPlayer",
                {
                    'teamId': team.team_id,
                    'personId': person.person_id,
                    'position': position
                }
            )

    def _use_attributes(self, attributes: dict):
        self._sporting_event = attributes['sportingEvent']
        self._line_up_id = attributes["lineUpId"]
        self._roles_per_team = attributes["rolesPerTeam"]

    def __repr__(self):
        return f"<LineUp sportingEvent={self.sporting_event}>"
