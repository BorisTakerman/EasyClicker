"""Click scheduling engine."""

from __future__ import annotations

from threading import Event, Thread
from time import sleep
from typing import Callable


class ClickEngine:
    """Background click loop that can be started/stopped safely."""

    def __init__(self, click_fn: Callable[[], None], interval_seconds: float) -> None:
        self._click_fn = click_fn
        self._interval_seconds = interval_seconds
        self._active = Event()
        self._shutdown = Event()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    @property
    def is_active(self) -> bool:
        return self._active.is_set()

    def set_interval(self, interval_seconds: float) -> None:
        if interval_seconds <= 0:
            raise ValueError("Interval must be > 0")
        self._interval_seconds = interval_seconds

    def start(self) -> None:
        self._active.set()

    def stop(self) -> None:
        self._active.clear()

    def toggle(self) -> bool:
        if self.is_active:
            self.stop()
            return False
        self.start()
        return True

    def shutdown(self) -> None:
        self._active.clear()
        self._shutdown.set()
        self._thread.join(timeout=1.0)

    def _run(self) -> None:
        while not self._shutdown.is_set():
            if self._active.is_set():
                self._click_fn()
                sleep(self._interval_seconds)
            else:
                sleep(0.01)
