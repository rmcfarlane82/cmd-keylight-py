from __future__ import annotations

import argparse
import sys

from .actions import Action, apply_action
from .config import Keylight, load_config


class _Args(argparse.Namespace):
    target: str
    action_pos: Action | None
    action_opt: Action | None
    config: str


def _resolve_targets(lights: list[Keylight], target: str) -> list[Keylight]:
    if target == "all":
        return lights

    matched = [light for light in lights if light.alias == target]
    if not matched:
        raise RuntimeError(f"No light with alias '{target}' found in config")
    return matched


def main(argv: list[str]) -> int:
    actions: tuple[Action, Action, Action] = ("on", "off", "toggle")
    parser = argparse.ArgumentParser(description="Control an Elgato Key Light")
    parser.add_argument("target", nargs="?", default="all", help="Light alias or 'all'")
    parser.add_argument(
        "action_pos",
        nargs="?",
        choices=actions,
        help="Power action to apply",
    )
    parser.add_argument(
        "-a",
        "--action",
        dest="action_opt",
        choices=actions,
        help="Power action to apply",
    )
    parser.add_argument(
        "--config",
        default="keylights.conf",
        help="Path to Key Light config JSON",
    )
    args = parser.parse_args(argv, namespace=_Args())

    action = args.action_opt or args.action_pos
    if action is None and args.target in actions:
        action = args.target
        args.target = "all"
    if action is None:
        action = "toggle"

    try:
        lights = load_config(args.config)
        targets = _resolve_targets(lights, args.target)
        for light in targets:
            apply_action(light, action)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Key Light action applied: {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
