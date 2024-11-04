import requests


class NodeClient:
    _BASE_URL = "http://192.168.168.150/"
    _DEFAULT_VALUES = {"D2": 0, "D3": 0, "D4": 0, "D5": 0, "D6": 0, "D7": 0, "D8": 0}

    def __init__(self):
        self.values_cache = requests.get(self._BASE_URL + "state").json()
        self.rotate_servo("D1", 0)

    def rotate_servo(self, pin: str, degree: int):
        if self.values_cache[pin] == degree:
            return

        requests.get(self._BASE_URL + f"servo/{pin}/{degree}")
        self.values_cache[pin] = degree

    def update_pin(self, pin: str, state: int):
        if self.values_cache[pin] == state:
            return

        requests.get(self._BASE_URL + f"pin/{pin}/{state}")
        self.values_cache[pin] = state

    def reset_pin(self, pin: str):
        self.update_pin(pin, self._DEFAULT_VALUES[pin])
