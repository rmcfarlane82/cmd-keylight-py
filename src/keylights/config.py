from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast


@dataclass(frozen=True)
class Keylight:
    host: str
    port: int = 9123
    alias: str | None = None

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Keylight":
        host = value.get("host")
        if not isinstance(host, str) or not host:
            raise RuntimeError("Each light needs a non-empty 'host' field")

        alias = value.get("alias")
        if alias is not None and not isinstance(alias, str):
            raise RuntimeError("Alias must be a string if provided")

        port = value.get("port", 9123)
        if not isinstance(port, int):
            raise RuntimeError("Port must be an integer if provided")

        return cls(host=host, port=port, alias=alias)


def load_config(path: str) -> list[Keylight]:
    config_path = Path(path)
    try:
        raw = config_path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except OSError as exc:
        raise RuntimeError(f"Failed to read config file: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in config file: {config_path}") from exc

    return _parse_config(payload, config_path)


def _parse_config(payload: object, config_path: Path) -> list[Keylight]:
    if not isinstance(payload, dict):
        raise RuntimeError(f"Config file must be a JSON object: {config_path}")

    payload_dict = cast(dict[str, Any], payload)
    lights = payload_dict.get("lights")
    if not isinstance(lights, list) or not lights:
        raise RuntimeError(f"Config file must include a non-empty 'lights' list: {config_path}")

    keylights: list[Keylight] = []
    for item in cast(list[object], lights):
        if not isinstance(item, dict):
            raise RuntimeError("Each light entry must be an object")
        keylights.append(Keylight.from_dict(cast(dict[str, Any], item)))

    return keylights
