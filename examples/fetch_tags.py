from os import environ

from dotenv import load_dotenv

from pyteamtv import TeamTVUser
from pyteamtv.dataframe_builder import DataframeBuilder


def main():
    team_name = "Team A"
    sporting_event_id = "123456-abcd-abcd-abcd-123456789"

    load_dotenv()

    api = TeamTVUser(jwt_token=environ["TEAMTV_API_TOKEN"])
    team = api.get_team(team_name)

    builder = DataframeBuilder(team)

    sporting_event = team.get_sporting_event(sporting_event_id)
    video = sporting_event.get_videos_by_tags(output_key="switched")[0]
    df = builder.build_df([sporting_event.get_observation_log(video_id=video.video_id)])

    print(df)


if __name__ == "__main__":
    main()
