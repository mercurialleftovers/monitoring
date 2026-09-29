import random
import time
from typing import Any

import requests

deviceStringIdentifier: str = "deviceId1322AssaD"  # hardcoded in each device, when setting it up, the MC (arduino), should have a kbd + LCD to do so
HandshakeURL: str = "http://localhost:8000/device/handshake/"
SAMPLE_URL: str = "http://localhost:8000/sample/submit/"
DELTA_TIME: float = 0.2

# getting a numeric identifier:
req = requests.get(HandshakeURL + deviceStringIdentifier)
numericId: int = req.json()["id"]


def takeSample():
    data: dict[str, Any] = {}

    thermalSensor = {"sensor": "THERMAL", "value": random.random()}
    vibrationSensor = {"sensor": "VIBRATION", "value": random.random()}

    data["deviceId"] = numericId
    data["sensorReadings"] = [thermalSensor, vibrationSensor]
    # for benchmarking:
    data["timeSampled"] = time.perf_counter()

    return data


beginTime = time.perf_counter()
while True:
    data = takeSample()
    # send the data:
    response = requests.post(url=SAMPLE_URL, json=data)
    print(response.json())
    currentTime = time.perf_counter()
    print(currentTime - beginTime)  # dt
    beginTime = currentTime
