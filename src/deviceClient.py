import sys
import re
import os
import random
import time
from threading import Thread
from typing import Any
from enums import *

import requests

# deviceStringIdentifier: str = "string1"  # hardcoded in each device, when setting it up, the MC (arduino), should have a kbd + LCD to do so
HandshakeURL: str = "http://127.0.0.1:8000/device/handshake/"
SAMPLE_URL: str = "http://127.0.0.1:8000/sample/submit/"
DELTA_TIME: float = 2.0
TIMEOUT = 5


def takeSample(numericId):
    data: dict[str, Any] = {}

    thermalSensor = {"sensor": "THERMAL", "value": random.random()}
    vibrationSensor = {"sensor": "VIBRATION", "value": random.random()}

    data["deviceId"] = numericId
    data["sensorReadings"] = [thermalSensor, vibrationSensor]

    # print(data)

    return data


def monitoringRoutine(deviceStringIdentifier: str):
    req = requests.get(HandshakeURL + deviceStringIdentifier, timeout=TIMEOUT)
    # print(req.json())
    numericId: int = req.json()
    while True:
        data = takeSample(numericId)
        requests.post(url=SAMPLE_URL, json=data, timeout=TIMEOUT)
        time.sleep(DELTA_TIME)
        # os.system("cls")


def registerDevice(
    deviceName: str, identifier: str, category: DeviceType, department: Department
):
    deviceData = {
        "name": deviceName,
        "deviceType": category.value,
        "identifier": identifier,
        "department": department.value,
    }

    res = requests.post("http://127.0.0.1:8000/device/register/", json=deviceData)
    print(res.text)


# registering sample devices:
registerDevice(
    "agitateur suflate 01",
    "ag_sulf_react_01",
    DeviceType.AGITATOR,
    Department.REACTIF,
)

registerDevice(
    "pompe doseuse suflate 01",
    "pump_sulf_react_01",
    DeviceType.PUMP,
    Department.REACTIF,
)


registerDevice(
    "compresseur lavage 01",
    "surpr_01",
    DeviceType.PUMP,
    Department.SURPRESSEURS,
)

spawnWorkers: bool = True
identifiers: list[str] = ["ag_sulf_react_01", "pump_sulf_react_01", "surpr_01"]

if spawnWorkers:
    # num_workers: int = int(input("enter the name of workers (virtual devices): "))
    num_workers: int = len(identifiers)
    threads: list[Thread] = []

    for i in range(num_workers):
        t = Thread(target=monitoringRoutine, args=(identifiers[i],))
        threads.append(t)

    for thread in threads:
        thread.start()

while True:
    cmd: str = input(">>> ")
    if cmd == "kill":
        sys.exit(0)
    cmd: str = "kill t1"
    cmd = cmd.strip()

    pattern = r"kill t\d"
    match = re.search(pattern, cmd)
    # print(dir(match))
    # print(match.group(0))
    # print(match.group(1))
    # if match:
    #     print(match.group())
    #     print(type(match.group()))
    #     thread_idx = int(match.group(1)) - 1
    # TODO(bader): stop thread thread_idx
