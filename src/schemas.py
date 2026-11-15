from pydantic import BaseModel

from enums import *


class SensorData(BaseModel):
    sensor: SensorType
    value: float


class Sample(BaseModel):
    deviceId: int
    sensorReadings: list[SensorData]
    # for benchmarking:
    # timeSampled: float


class DeviceInfo(BaseModel):
    tag: str  # unique
    name: str  # human readable
    deviceType: DeviceType
    department: Department


class User(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    role: Role
