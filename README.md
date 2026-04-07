# EasyClicker

A foundation-focused autoclicker prototype with:

- Position capture (set where simulated clicks should happen).
- Adjustable interval with units from microseconds through hours.
- Custom hotkeys for:
  - Capturing click position
  - Start/stop toggling the clicker
- Background click loop that does not block your normal workflow.

> Important platform note: truly independent dual-cursor mouse control is not generally available from user-space apps on standard desktop OSes. This app keeps your real mouse usable, but simulated clicks are still sent through the OS input pipeline (not a second physical cursor).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m easyclicker
```

## CLI options

```bash
python -m easyclicker \
  --interval 250 \
  --unit milliseconds \
  --start-stop-hotkey '<ctrl>+<alt>+s' \
  --set-position-hotkey '<ctrl>+<alt>+p'
```

Units supported:

- `microseconds`
- `milliseconds`
- `seconds`
- `minutes`
- `hours`

## Controls

- Press the **set-position hotkey** to save your current mouse position.
- Press the **start/stop hotkey** to toggle autoclicking at that saved position.
- Press `Ctrl+C` in terminal to quit.

## Foundation-first architecture

The app is split into small testable pieces:

- `interval.py` parses and validates click intervals.
- `engine.py` contains the click scheduling loop.
- `app.py` wires hotkeys, position capture, and click behavior.

## Tests

```bash
python -m unittest
```

## Visual Studio Code quick test

If you just want to press **Run** in VS Code:

1. Open this folder in VS Code.
2. Create/activate a Python environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Open **Run and Debug** and select **EasyClicker: Run app**.
5. Press **F5**.

This runs `run_easyclicker.py`, which launches the app with sane defaults for fast manual testing. If dependencies are missing, the launcher will try to run `pip install -r requirements.txt` automatically once.
