import sys
import re
import os
import random
import time
import threading
from typing import Any
from enums import *
from urllib3 import encode_multipart_formdata

import requests

HandshakeURL: str = "http://127.0.0.1:8000/device/handshake/"
SAMPLE_URL: str = "http://127.0.0.1:8000/sample/submit/"
DELTA_TIME: float = 0.5
TIMEOUT = 5
MAX_TEMP: int = 120
MIN_TEMP: int = 50


def takeSample(numericId):
    data: dict[str, Any] = {}

    thermalSensor = {
        "sensor": "THERMAL",
        "value": random.random() * (MAX_TEMP / 2) + MIN_TEMP,
    }
    vibrationSensor = {"sensor": "VIBRATION", "value": random.random()}

    data["deviceId"] = numericId
    data["sensorReadings"] = [thermalSensor, vibrationSensor]

    return data


def monitoringRoutine(tag: str):
    req = requests.get(HandshakeURL + tag, timeout=TIMEOUT)
    numericId: int = req.json()
    while True:
        begin_time = time.perf_counter()
        data = takeSample(numericId)
        # encoding data as multipart-encode_multipart_formdata
        data, header = encode_multipart_formdata(data)

        print(data)
        print(header)

        # requests.post(url=SAMPLE_URL, json=data, timeout=TIMEOUT)
        requests.post(url=SAMPLE_URL, data=data, timeout=TIMEOUT)

        time_to_sleep: float = DELTA_TIME - (time.perf_counter() - begin_time)
        if time_to_sleep > 0:
            time.sleep(DELTA_TIME)


name_prefixes = ["pompe", "agitateur", "moteur"]


class FakeDevice:
    i: int = 0

    def __init__(self):
        return {}


def registerDevice(
    deviceName: str,
    tag: str,
    category: DeviceType,
    department: Department,
):
    tags.append(tag)
    deviceData = {
        "name": deviceName,
        "tag": tag,
        "deviceType": category.value,
        "department": department.value,
    }

    res = requests.post("http://127.0.0.1:8000/device/register/", json=deviceData)
    print(res.text)


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


registerDevice(
    "compresseur lavage 02",
    "surpr_02",
    DeviceType.COMPRESSOR,
    Department.REACTIF,
)


registerDevice(
    "pompe lavage 02",
    "pump_lav_02",
    DeviceType.PUMP,
    Department.BIOFOR,
)

spawnWorkers: bool = True

if spawnWorkers:
    num_workers: int = len(tags)
    threads: list[threading.Thread] = []

    for i in range(num_workers):
        t = threading.Thread(target=monitoringRoutine, args=(tags[i],))
        threads.append(t)

    for thread in threads:
        thread.start()
