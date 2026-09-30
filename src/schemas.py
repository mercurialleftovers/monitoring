from enum import Enum

from pydantic import BaseModel


class DeviceType(Enum):
    MOTOR = "MOTOR"
    AGITATOR = "AGITATOR"
    SURPRESSOR = "SURPRESSOR"
    COMPRESSOR = "COMPRESSOR"


class SensorType(Enum):
    THERMAL = "THERMAL"
    VIBRATION = "VIBRATION"


class SensorData(BaseModel):
    sensor: SensorType
    value: float


class Sample(BaseModel):
    deviceId: int
    sensorReadings: list[SensorData]
    # for benchmarking:
    # timeSampled: float


class Device(BaseModel):
    # id: int  # given by the database
    name: str  # unique ?
    deviceType: DeviceType
