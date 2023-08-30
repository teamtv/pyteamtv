from datetime import datetime, timezone
import time
from queue import Queue
from typing import Iterator

from threading import Thread, Event

from .teamtv_object import TeamTVObject
from ..infra.match_state.event_store import QueueEventStore
from ..infra.match_state.match_event_fetcher import match_event_fetcher


def utcnow() -> datetime:
    return datetime.fromtimestamp(time.time(), timezone.utc)


class EventStreamReader(Iterator):
    def __next__(self):
        while True:
            events = self.event_store.get_events()

            if len(events) > self.cursor:
                item = events[self.cursor]
                self.cursor += 1
                if self.start_timestamp and item.occurred_on < self.start_timestamp:
                    continue

                return None, item

            time.sleep(0.1)

    def __init__(self, poll_url: str, seek_to_start: bool = False):
        self.queue = Queue()
        self.start_timestamp = None if seek_to_start else utcnow()
        self.event_store = QueueEventStore(self.queue)
        self.should_stop = Event()
        self.cursor = 0
        self.poll_url = poll_url

        self.thread = Thread(target=self._read_to_queue, daemon=True)
        self.thread.start()

    def _read_to_queue(self):
        match_event_fetcher(self.poll_url, self.queue, self.should_stop)

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.should_stop.set()
        self.thread.join()


class EventStream(TeamTVObject):
    @property
    def event_stream_id(self):
        return self._event_stream_id

    @property
    def endpoint_urls(self):
        return self._endpoint_urls

    def __repr__(self):
        return f"<EventStream event_stream_id={self.event_stream_id}>"

    def _use_attributes(self, attributes: dict):
        self._event_stream_id = attributes["eventStreamId"]
        self._endpoint_urls = attributes["endpointUrls"]

        super()._use_attributes(attributes)

    def open(self, seek_to_start: bool = False):
        return EventStreamReader(
            self.endpoint_urls["polling"], seek_to_start=seek_to_start
        )
