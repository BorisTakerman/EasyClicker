"""VS Code friendly launcher for EasyClicker."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "requirements.txt"


def _install_requirements() -> bool:
    if not REQUIREMENTS.exists():
        print("[easyclicker] requirements.txt not found; cannot auto-install dependencies.")
        return False

    print("[easyclicker] Installing dependencies from requirements.txt...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        cwd=str(ROOT),
        check=False,
    )
    return result.returncode == 0


def _load_app_main():
    from easyclicker.app import main as app_main

    return app_main


def main() -> int:
    try:
        app_main = _load_app_main()
    except ModuleNotFoundError as exc:
        missing = exc.name or "unknown"
        print(f"[easyclicker] Missing dependency: {missing}")

        if not _install_requirements():
            print("[easyclicker] Auto-install failed. Run: pip install -r requirements.txt")
            return 1

        try:
            app_main = _load_app_main()
        except ModuleNotFoundError as retry_exc:
            print(
                "[easyclicker] Dependencies still unavailable after install attempt: "
                f"{retry_exc.name or 'unknown'}"
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
    exit_code = main()
    if exit_code:
        print(f"[easyclicker] Launcher exited with code {exit_code}.")
