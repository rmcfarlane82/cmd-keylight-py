#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

import constants
from keylight_client import KeyLightClient


def _default_config_path() -> Path:
    if sys.platform == "win32":
        return Path("~/AppData/Local/cmd-keylights-py/keylights.json").expanduser()
    return Path("~/.config/cmd-keylights-py/keylights.conf").expanduser()


def _config_template() -> dict:
    return {
        "defaults": {"port": 9123, "timeout": 5},
        "lights": [
            {"alias": "left", "host": "192.168.1.5"},
            {"alias": "right", "host": "192.168.1.6", "port": 9123 },
        ],
    }


def _load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found at {config_path}. Create it with your keylight hosts."
        )

    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def _load_clients(config: dict) -> dict[str, KeyLightClient]:
    defaults = config.get("defaults", {})
    lights = config.get("lights", [])
    if not lights:
        raise ValueError("Config must include a non-empty 'lights' list.")

    clients: dict[str, KeyLightClient] = {}
    for entry in lights:
        alias = entry.get("alias")
        host = entry.get("host")
        if not alias or not host:
            raise ValueError("Each light must include 'alias' and 'host'.")

        if alias in clients:
            raise ValueError(f"Duplicate alias in config: {alias}")

        port = entry.get("port", defaults.get("port", 9123))
        timeout = entry.get(
            "timeout", defaults.get("timeout", constants.HTTP_REQUEST_TIMEOUT)
        )
        clients[alias] = KeyLightClient(host=host, port=port, timeout=timeout)

    return clients


def _parse_args(default_config: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Control Elgato Key Lights.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "alias",
        nargs="?",
        help="Alias of the light to target. Omit to target all lights.",
    )
    parser.add_argument(
        "-t",
        "--temp",
        type=int,
        help="Temperature (2900-7900). in Kelvin. Omit to leave unchanged.",
    )
    parser.add_argument(
        "-b",
        "--brightness",
        type=int,
        help="Brightness (5-100). Omit to leave unchanged.",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print the current config and exit.",
    )
    parser.add_argument(
        "--print-config-template",
        action="store_true",
        help="Print a sample config template and exit.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help=f"Path to config file (default: {default_config}).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args(_default_config_path())
    if args.print_config_template:
        print(json.dumps(_config_template(), indent=2, sort_keys=True))
        return

    config = _load_config(args.config)
    if args.show_config:
        print(json.dumps(config, indent=2, sort_keys=True))
        return

    clients = _load_clients(config)

    if args.alias:
        if args.alias not in clients:
            raise ValueError(f"Alias not found in config: {args.alias}")
        targets = [clients[args.alias]]
    else:
        targets = list(clients.values())

    errors: list[str] = []

    if args.temp is None and args.brightness is None:
        for client in targets:
            try:
                client.toggle_power()
            except Exception as exc:
                errors.append(str(exc))
        if errors:
            print("Some lights failed to toggle:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            raise SystemExit(1)
        return

    for client in targets:
        try:
            if args.temp is not None:
                client.set_temp(args.temp)
            if args.brightness is not None:
                client.set_brightness(args.brightness)
        except Exception as exc:
            errors.append(str(exc))

    if errors:
        print("Some lights failed to update:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
