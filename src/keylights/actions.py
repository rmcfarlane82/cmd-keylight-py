from __future__ import annotations

from typing import Literal

from .config import Keylight
from .device import get_power_state, set_power

Action = Literal["on", "off", "toggle"]


def apply_action(light: Keylight, action: Action) -> None:
    if action == "toggle":
        current = get_power_state(light.host, light.port)
        set_power(light.host, light.port, 0 if current else 1)
    elif action == "on":
        set_power(light.host, light.port, 1)
    else:
        set_power(light.host, light.port, 0)
