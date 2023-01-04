import os.path

import pytest
import requests_mock

from pyteamtv.exceptions import InputError
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


class TestVideoUpload:
    def test_new_video(self, current_team, test_mp4):
        """
        Test upload of a new video
        """
        sporting_event_id = "sporting-event-id-123"
        video_id = "video-id-123"

        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://fake-url/sportingEvents/{sporting_event_id}",
                json={
                    "type": "training",
                    "name": "Test Training",
                    "sportingEventId": sporting_event_id,
                    "clocks": {},
                    "scheduledAt": "2022-01-01T10:00:00.000Z",
                },
            )

            sporting_event = current_team.get_sporting_event(
                sporting_event_id=sporting_event_id
            )

            file_size = os.path.getsize(test_mp4)

            adapter = mock.post(
                f"https://fake-url/sportingEvents/{sporting_event_id}/initVideoUpload",
                json=video_id,
            )
            mock.get(
                f"https://fake-url/videos/{video_id}",
                json={
                    "videoId": video_id,
                    "state": "new",
                    "parts": [
                        {
                            "fileSize": file_size,
                            "tusUploadUrl": "https://upload-url/random-url",
                        }
                    ],
                },
            )
            mock.head(
                "https://upload-url/random-url",
                headers={
                    "Upload-Offset": "0",
                    "Upload-Length": str(file_size),
                    "Tus-Resumable": "1.0.0",
                },
            )
            patch_adapter = mock.patch(
                "https://upload-url/random-url",
                headers={
                    "upload-offset": str(file_size),
                    "Upload-Length": str(file_size),
                    "Tus-Resumable": "1.0.0",
                },
            )

            sporting_event.upload_video(test_mp4, description="Test Training")

            assert adapter.last_request.json() == {
                "description": "Test Training",
                "files": [{"name": "test.mp4", "size": 991017}],
                "skipTranscoding": False,
                "tags": {},
            }

            assert len(patch_adapter.last_request.body) == file_size

    def test_resume_video(self, current_team, test_mp4):
        """
        Test resume of upload of an existing video.

        This test includes:
        1. Test tags are set when resume_if_exists is set
        2. Remote and local files match size
        3. File upload is resumed at based on Upload-Offset header
        """
        sporting_event_id = "sporting-event-id-123"
        tags = {"output_key": "main"}
        video_id = "video-id-123"

        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://fake-url/sportingEvents/{sporting_event_id}",
                json={
                    "type": "training",
                    "name": "Test Training",
                    "sportingEventId": sporting_event_id,
                    "clocks": {},
                    "videoIds": [video_id],
                    "scheduledAt": "2022-01-01T10:00:00.000Z",
                },
            )

            sporting_event = current_team.get_sporting_event(
                sporting_event_id=sporting_event_id
            )

            file_size = os.path.getsize(test_mp4)
            upload_offset = file_size - 100  # Fake the upload offset

            mock.get(
                f"https://fake-url/videos",
                json=[
                    {
                        "videoId": video_id,
                        "state": "new",
                        "tags": tags,
                        "parts": [
                            {
                                "fileSize": file_size
                                - 1,  # Return an incorrect filesize. The resume code MUST check
                                # if the local and remote filesizes match.
                                "state": "new",
                                "tusUploadUrl": "https://upload-url/random-url",
                            }
                        ],
                    }
                ],
            )
            mock.head(
                "https://upload-url/random-url",
                headers={
                    "Upload-Offset": str(upload_offset),
                    "Upload-Length": str(file_size),
                    "Tus-Resumable": "1.0.0",
                },
            )
            adapter = mock.patch(
                "https://upload-url/random-url",
                headers={
                    "Upload-Offset": str(file_size),
                    "Upload-Length": str(file_size),
                    "Tus-Resumable": "1.0.0",
                },
            )

            with pytest.raises(
                InputError,
                match="When `resume_if_exists` is specified you must pass `tags`",
            ):
                sporting_event.upload_video(
                    test_mp4,
                    description="Test Training",
                    resume_if_exists=True,
                )

            mock.get(
                f"https://fake-url/videos/{video_id}",
                json={
                    "videoId": video_id,
                    "state": "new",
                    "tags": tags,
                    "parts": [
                        {
                            "fileSize": file_size,
                            "state": "new",
                            "tusUploadUrl": "https://upload-url/random-url",
                        }
                    ],
                },
            )

            with pytest.raises(
                InputError,
                match=r"File size of '.*test\.mp4' doesn't match existing video",
            ):
                sporting_event.upload_video(
                    test_mp4,
                    description="Test Training",
                    resume_if_exists=True,
                    tags=tags,
                )

            mock.get(
                f"https://fake-url/videos",
                json=[
                    {
                        "videoId": video_id,
                        "state": "new",
                        "tags": tags,
                        "parts": [
                            {
                                "fileSize": file_size,
                                "state": "new",
                                "tusUploadUrl": "https://upload-url/random-url",
                            }
                        ],
                    }
                ],
            )
            sporting_event.upload_video(
                test_mp4,
                description="Test Training",
                resume_if_exists=True,
                tags=tags,
            )

            assert len(adapter.last_request.body) == 100

    def test_resume_completed_video(self, current_team, test_mp4):
        """
        Test calling upload to finished video.
        """
        sporting_event_id = "sporting-event-id-123"
        tags = {"output_key": "main"}
        video_id = "video-id-123"

        with requests_mock.Mocker() as mock:
            mock.get(
                f"https://fake-url/sportingEvents/{sporting_event_id}",
                json={
                    "type": "training",
                    "name": "Test Training",
                    "sportingEventId": sporting_event_id,
                    "clocks": {},
                    "videoIds": [video_id],
                    "scheduledAt": "2022-01-01T10:00:00.000Z",
                },
            )

            sporting_event = current_team.get_sporting_event(
                sporting_event_id=sporting_event_id
            )

            file_size = os.path.getsize(test_mp4)

            mock.get(
                f"https://fake-url/videos",
                json=[
                    {
                        "videoId": video_id,
                        "state": "new",
                        "tags": tags,
                        "parts": [
                            {
                                "fileSize": file_size,
                                "state": "upload-success",
                                "tusUploadUrl": "https://upload-url/random-url",
                            }
                        ],
                    }
                ],
            )

            video = sporting_event.upload_video(
                test_mp4,
                description="Test Training",
                resume_if_exists=True,
                tags=tags,
            )

            assert video.video_id == video_id
