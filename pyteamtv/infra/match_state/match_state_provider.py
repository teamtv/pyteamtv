import json
from datetime import datetime
import signal
import os
from multiprocessing import Queue, Process
from typing import List, Dict

from .event_store import EventStore, QueueEventStore, StaticEventStore
from .match_event_fetcher import match_event_fetcher
from .match_state_calculator import MatchStateCalculator


class MatchStateProvider:
    def __init__(self, event_stream_url):
        self._match_event_queue = Queue(1000)
        event_store = QueueEventStore(self._match_event_queue)
        self._match_state_calculator = MatchStateCalculator(event_store)
        self._process = Process(
            target=match_event_fetcher, args=(event_stream_url, self._match_event_queue)
        )
        self._process.start()

    def stop(self):
        if self._process and self._process.is_alive():
            os.kill(self._process.pid, signal.SIGKILL)
            self._process.join(1)
            if self._process.is_alive():
                os.kill(self._process.pid, signal.SIGKILL)
                self._process.join()

            self._process = None

    def __del__(self):
        self.stop()

    def get_data(self, snapshot_timestamp):
        return self._match_state_calculator.get_state(snapshot_timestamp)
