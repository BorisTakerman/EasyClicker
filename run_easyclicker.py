"""VS Code friendly launcher for EasyClicker."""

from __future__ import annotations

import sys


def main() -> int:
    try:
        from easyclicker.app import main as app_main
    except ModuleNotFoundError as exc:
        missing = exc.name or "unknown"
        print(
            "[easyclicker] Missing dependency: "
            f"{missing}.\n"
            "Install dependencies first with: pip install -r requirements.txt"
        )
        return 1

    return app_main(
        [
            "--interval",
            "1",
            "--unit",
            "seconds",
            "--start-stop-hotkey",
            "<ctrl>+<alt>+s",
            "--set-position-hotkey",
            "<ctrl>+<alt>+p",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
