import requests

import constants


class KeyLightClient:
    def __init__(
        self,
        host: str,
        port: int = 9123,
        timeout: int = constants.HTTP_REQUEST_TIMEOUT,
    ):
        self._base_url = f"http://{host}:{port}/elgato/lights"
        self._timeout = timeout
        self._session = requests.Session()

    def _get(self) -> dict:
        response = self._session.get(self._base_url, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def _put(self, payload: dict) -> None:
        response = self._session.put(
            self._base_url, json=payload, timeout=self._timeout
        )
        response.raise_for_status()

    def get_state(self) -> dict:
        try:
            return self._get()
        except Exception as exc:
            raise RuntimeError(f"Failed to get state for {self._base_url}") from exc

    def get_power_state(self) -> int:
        state = self.get_state()
        return state["lights"][0]["on"]

    def set_power(self, state: bool) -> None:
        try:
            self._put({"lights": [{"on": int(state)}]})
        except Exception as exc:
            raise RuntimeError(f"Failed to set power for {self._base_url}") from exc

    def toggle_power(self) -> None:
        new_state = not self.get_power_state()
        self.set_power(new_state)

    def set_brightness(self, brightness: int) -> None:
        brightness = max(constants.MIN_BRIGHTNESS, min(constants.MAX_BRIGHTNESS, brightness))
        try:
            payload = {"numberOfLights": 1, "lights": [{"brightness": brightness}]}
            self._put(payload)
        except Exception as exc:
            raise RuntimeError(f"Failed to change brightness for {self._base_url}") from exc

    def set_temp(self, temperature: int) -> None:
        temperature = max(constants.MIN_TEMP, min(constants.MAX_TEMP, temperature))
        converted_temp = round(1_000_000 / temperature)
        try:
            payload = {"numberOfLights": 1, "lights": [{"temperature": converted_temp}]}
            self._put(payload)
        except Exception as exc:
            raise RuntimeError(f"Failed to change temperature for {self._base_url}") from exc
