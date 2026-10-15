import os
import random
import time
from typing import Any

import requests

deviceStringIdentifier: str = "pompe_doseuse_coagulation_1"  # hardcoded in each device, when setting it up, the MC (arduino), should have a kbd + LCD to do so
HandshakeURL: str = "http://127.0.0.1:8000/device/handshake/"
SAMPLE_URL: str = "http://127.0.0.1:8000/sample/submit/"
DELTA_TIME: float = 2.0
TIMEOUT = 5

# getting a numeric identifier:
req = requests.get(HandshakeURL + deviceStringIdentifier, timeout=TIMEOUT)
# print(req.json())
numericId: int = req.json()


def takeSample():
    data: dict[str, Any] = {}

    thermalSensor = {"sensor": "THERMAL", "value": random.random()}
    vibrationSensor = {"sensor": "VIBRATION", "value": random.random()}

    data["deviceId"] = numericId
    data["sensorReadings"] = [thermalSensor, vibrationSensor]

    print(data)

    return data


beginTime = time.perf_counter()

while True:
    data = takeSample()
    # send the data:
    response = requests.post(url=SAMPLE_URL, json=data, timeout=TIMEOUT)
    # print(response.json())
    currentTime = time.perf_counter()
    print(currentTime - beginTime)  # dt
    beginTime = currentTime
    time.sleep(DELTA_TIME)
    os.system("cls")
