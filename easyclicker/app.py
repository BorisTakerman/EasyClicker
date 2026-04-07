"""Application entrypoint and hotkey orchestration."""

from __future__ import annotations

import argparse
import signal
import sys
from dataclasses import dataclass
from threading import Event

from pynput import keyboard, mouse
import pyautogui

from .engine import ClickEngine
from .interval import parse_interval


@dataclass
class Position:
    x: int
    y: int


class EasyClickerApp:
    def __init__(self, interval_seconds: float, start_stop_hotkey: str, set_position_hotkey: str) -> None:
        self._current_position: Position | None = None
        self._mouse_controller = mouse.Controller()
        self._engine = ClickEngine(click_fn=self._click, interval_seconds=interval_seconds)
        self._exit_event = Event()

        self._hotkeys = keyboard.GlobalHotKeys(
            {
                start_stop_hotkey: self._handle_toggle,
                set_position_hotkey: self._handle_set_position,
            }
        )

    def run(self) -> int:
        self._print_help()

        def _signal_handler(_sig, _frame):
            self.stop()

        signal.signal(signal.SIGINT, _signal_handler)
        self._hotkeys.start()
        self._exit_event.wait()
        return 0

    def stop(self) -> None:
        self._engine.shutdown()
        self._hotkeys.stop()
        self._exit_event.set()

    def _handle_set_position(self) -> None:
        x, y = self._mouse_controller.position
        self._current_position = Position(x=x, y=y)
        print(f"[easyclicker] Click target set to ({x}, {y})")

    def _handle_toggle(self) -> None:
        if self._current_position is None:
            print("[easyclicker] Set a target position first using the set-position hotkey.")
            return

        active = self._engine.toggle()
        print("[easyclicker] Autoclicker started." if active else "[easyclicker] Autoclicker stopped.")

    def _click(self) -> None:
        if self._current_position is None:
            return

        pyautogui.click(x=self._current_position.x, y=self._current_position.y)

    @staticmethod
    def _print_help() -> None:
        print("[easyclicker] Running. Use your configured hotkeys to set position and toggle.")
        print("[easyclicker] Press Ctrl+C to exit.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EasyClicker core autoclicker")
    parser.add_argument("--interval", type=float, default=1.0, help="Click interval numeric value")
    parser.add_argument(
        "--unit",
        default="seconds",
        choices=["microseconds", "milliseconds", "seconds", "minutes", "hours"],
        help="Interval unit",
    )
    parser.add_argument(
        "--start-stop-hotkey",
        default="<ctrl>+<alt>+s",
        help="Global hotkey to start/stop clicking",
    )
    parser.add_argument(
        "--set-position-hotkey",
        default="<ctrl>+<alt>+p",
        help="Global hotkey to capture click target position",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    interval = parse_interval(args.interval, args.unit)
    app = EasyClickerApp(
        interval_seconds=interval.seconds,
        start_stop_hotkey=args.start_stop_hotkey,
        set_position_hotkey=args.set_position_hotkey,
    )
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
