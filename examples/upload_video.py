import logging
import sys
from os import environ

from dotenv import load_dotenv
from pyteamtv import TeamTVUser


def main():
    team_name = "Rust Roest 1"
    sporting_event_id = "c1a29d76-6e7f-11ed-ac56-51ebda3b25a3"

    load_dotenv()

    api = TeamTVUser(jwt_token=environ["TEAMTV_API_TOKEN"])

    team = api.get_team(team_name)
    sporting_event = team.get_sporting_event(sporting_event_id)

    original = sporting_event.original
    if original:
        # This means the SportingEvent is a copy of some other SportingEvent,
        # probably because from an exchange.
        print(f"SportingEvent: {sporting_event} - {sporting_event.sporting_event_id}")
        print(f"Original: {original} - {original.sporting_event_id}")
        print(f"Can upload to original: {original.has_privilege('init-upload')}")

        # video = original.upload_video(
        #    "video.mp4",
        # )


if __name__ == "__main__":
    main()
