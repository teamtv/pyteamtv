from threading import Event

import requests
import time
from queue import Queue

import dateutil.parser


def match_event_fetcher(
    event_stream_url: str, match_event_queue: Queue, should_stop: Event
) -> None:
    last_event_id = None

    while not should_stop.is_set():
        url = event_stream_url
        if last_event_id:
            url += "?last-event-id={}".format(last_event_id)

        response = requests.get(url, timeout=2)

        events = response.json()
        for event in events:
            match_event_queue.put(
                dict(
                    eventType=event["event_name"],
                    eventAttributes=event["event_attributes"],
                    occurredOn=dateutil.parser.parse(event["occurred_on"]),
                )
            )
            last_event_id = event["event_id"]

        time.sleep(1)
    # print("hi")
    #         url = 'https://ttv-live.herokuapp.com/streams/{}/subscribe/sse'.format(event_stream_id)
    # print(url)
    #
    # response = with_urllib3(url)  # or with_requests(url)
    # client = sseclient.SSEClient(response)
    # for event in client.events():
    #                 dict(
    #                 eventType=event.event,
    #                 eventAttributes=json.loads(event.data)['eventAttributes']
    #     match_event_queue.put(event)
