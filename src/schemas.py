from pydantic import BaseModel
from fastapi import UploadFile

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
    role: Role
    lastname: str


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str
    phone: str
    firstname: str
    lastname: str
    role: Role
    profile_picture: UploadFile | None = None


class UserCreateResponse(BaseModel):
    username: str
    email: str
    firstname: str
    role: Role
    lastname: str
    has_profile_pic: bool = False
