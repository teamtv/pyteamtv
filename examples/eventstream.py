from os import environ

from dotenv import load_dotenv

from pyteamtv import TeamTVUser
import sseclient


def main():
    team_name = "KoensTest1337 1"
    sporting_event_id = "7d38416d-6689-4a90-957b-f25ce5bd517e"

    load_dotenv()

    api = TeamTVUser(jwt_token=environ["TEAMTV_API_TOKEN"])
    team = api.get_team(team_name)

    sporting_event = team.get_sporting_event(sporting_event_id)

    # 1. Check if there is already an existing EventStream
    event_streams = sporting_event.get_event_streams()
    if not event_streams:
        # This may take a some time.
        event_stream = sporting_event.create_event_stream()
    else:
        event_stream = event_streams[0]

    sse_url = event_stream.endpoint_urls['sse']

    # Listen for all new events. Now start live tagging in TeamTV
    messages = sseclient.SSEClient(sse_url)
    for message in messages:
        if message.event == 'message':
            # Keep-Alive event
            continue

        print(f"Receive new event {message.event}: {message.data}")

    """
    Example output:
    
    Receive new event SportingEventCreated: {"eventAttributes": {"homeTeam": {"teamId": "48688688-cba3-4bdb-b1b9-84484b4d631e", "appearance": {"primaryColor": null, "logoUrl": null, "secondaryColor": null}, "shortCode": null, "name": "Away Team"}, "awayTeam": {"teamId": "faf133da-5ae0-4580-9bee-dbd61969c1ed", "appearance": {"primaryColor": null, "logoUrl": null, "secondaryColor": null}, "shortCode": null, "name": "Home Team"}, "scheduledAt": "2022-11-24T21:30:58.000000Z", "name": "Away Team - Home Team"}, "occurredOn": "2022-11-24T21:09:17.733469Z"}
    Receive new event StartPeriod: {"eventAttributes": {"time": "1669325088.49300003", "period": "1"}, "occurredOn": "2022-11-24T21:24:49.275530Z"}
    Receive new event StartPossession: {"eventAttributes": {"time": 1669325088.498, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.1.5b15", "startPossessionAttributes": {"teamId": "48688688-cba3-4bdb-b1b9-84484b4d631e", "team": {"name": "Away Team"}, "position": "ATTACK"}, "description": "Start balbezit: 1st attack Away Team"}, "occurredOn": "2022-11-24T21:24:49.570236Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325093.597, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.2.4530", "description": "long : hit", "shotAttributes": {"angle": -37.5, "result": "HIT", "type": "LONG", "distance": 10.8}}, "occurredOn": "2022-11-24T21:24:55.944364Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325098.554, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.3.1359", "description": "short : hit", "shotAttributes": {"angle": 32.7, "result": "HIT", "type": "SHORT", "distance": 10.3}}, "occurredOn": "2022-11-24T21:25:01.915764Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325104.015, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.4.8627", "description": "long : goal", "shotAttributes": {"angle": -9.4, "result": "GOAL", "type": "LONG", "distance": 9.8}}, "occurredOn": "2022-11-24T21:25:06.592732Z"}
    Receive new event StartPossession: {"eventAttributes": {"time": 1669325106.494, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.6.66ea", "startPossessionAttributes": {"teamId": "faf133da-5ae0-4580-9bee-dbd61969c1ed", "team": {"name": "Home Team"}, "position": "ATTACK"}, "description": "Start balbezit: 1st attack Home Team"}, "occurredOn": "2022-11-24T21:25:07.838933Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325110.737, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.7.7df8", "description": "long : hit", "shotAttributes": {"angle": 30.1, "result": "HIT", "type": "LONG", "distance": 7}}, "occurredOn": "2022-11-24T21:25:12.554782Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325115.547, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.8.2f77", "description": "long : goal", "shotAttributes": {"angle": -35.2, "result": "GOAL", "type": "LONG", "distance": 8.1}}, "occurredOn": "2022-11-24T21:25:17.672290Z"}
    Receive new event StartPossession: {"eventAttributes": {"time": 1669325117.533, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.10.b75f", "startPossessionAttributes": {"teamId": "48688688-cba3-4bdb-b1b9-84484b4d631e", "team": {"name": "Away Team"}, "position": "DEFENCE"}, "description": "Start balbezit: 1st defence Away Team"}, "occurredOn": "2022-11-24T21:25:18.734420Z"}
    Receive new event Shot: {"eventAttributes": {"time": 1669325122.861, "id": "0ea6b631-5a2d-40e1-8b47-97b4f9fb69d7.11.b4f3", "description": "short : miss", "shotAttributes": {"angle": -17.3, "result": "MISS", "type": "SHORT", "distance": 10.1}}, "occurredOn": "2022-11-24T21:25:26.110798Z"}
    Receive new event EndPeriod: {"eventAttributes": {"time": "1669325129.17400002", "period": "1"}, "occurredOn": "2022-11-24T21:25:30.072036Z"}
    """


if __name__ == "__main__":
    main()
