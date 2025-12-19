from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def build_url(host: str, port: int) -> str:
    return f"http://{host}:{port}/elgato/lights"


def request_json(req: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Unexpected status {resp.status} from {req.full_url}")
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} from {req.full_url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error connecting to {req.full_url}: {exc.reason}") from exc


def get_power_state(host: str, port: int) -> int:
    url = build_url(host, port)
    req = urllib.request.Request(url, method="GET")
    payload = request_json(req)
    try:
        return int(payload["lights"][0]["on"])
    except (KeyError, IndexError, ValueError, TypeError) as exc:
        raise RuntimeError(f"Unexpected response format from {url}") from exc


def set_power(host: str, port: int, on: int) -> None:
    url = build_url(host, port)
    payload = {"lights": [{"on": on}]}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="PUT",
    )

    request_json(req)
