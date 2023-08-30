import pytest

from pyteamtv.infra.requester import Requester
from pyteamtv.models.resource_group.factory import factory
from pyteamtv.models.resource_group.team import TeamResourceGroup


@pytest.fixture
def test_mp4():
    return os.path.dirname(__file__) + "/test.mp4"


@pytest.fixture
def requester():
    return Requester(
        base_url="https://fake-url",
        jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    )


@pytest.fixture
def current_team(requester) -> TeamResourceGroup:
    return factory(
        requester,
        dict(
            tenantId="nl_soccer_test",
            resourceGroupId="1234-1234-1234",
            targetResourceId="team:soccer-team-1",
            targetResourceName="Soccer Team 1",
        ),
    )
