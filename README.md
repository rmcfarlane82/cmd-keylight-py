# cmd-keylights-py

Simple CLI for controlling Elgato Key Lights from the terminal.

## Config

Create a config file at:

- Linux: `~/.config/cmd-keylights-py/keylights.conf`
- Windows: `~/AppData/Local/cmd-keylights-py/keylights.json`

```json
{
  "defaults": {
    "port": 9123,
    "timeout": 5
  },
  "lights": [
    { "alias": "left", "host": "192.168.1.5" },
    { "alias": "right", "host": "192.168.1.6", "port": 1234 }
  ]
}
```

Per-light `port` and `timeout` values override defaults.

## Usage

Examples:

```bash
python -m src.main
python -m src.main left -t 3000 -b 10
python -m src.main -t 2000 -b 20
python -m src.main --show-config
python -m src.main --print-config-template
```

Behavior:

- `keylights` with no switches toggles power.
- Provide an alias to target a single light.
- Omit an alias to target all lights.

## Terminal shortcuts

Linux/macOS (zsh/bash):

```bash
lights() {
  python3 ~/Git/cmd-keylights-py/src/main.py --config ~/.config/cmd-keylights-py/keylights.conf "$@"
}
```

There is a shebang (`#!/usr/bin/env python3`) in the `src/main.py`, you can `chmod +x` the main.py, then you can call it directly:

```bash
lights() {
  ~/[YOUR_PATH]/cmd-keylights-py/src/main.py --config ~/.config/cmd-keylights-py/keylights.conf "$@"
}
```

Windows (PowerShell):

```powershell
function lights {
  python "$HOME\[YOUR_PATH]\cmd-keylights-py\src\main.py" --config "$HOME\AppData\Local\cmd-keylights-py\keylights.json" @args
}
```

Once added to your terminal you can run:

```bash
lights 
lights -b 50
lights -t 4500
lights -b 20 -t 5000
lights left -b 10 -t 2500
```

and so on. enjoy
