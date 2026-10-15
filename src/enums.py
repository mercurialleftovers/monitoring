from enum import Enum


class DeviceType(Enum):
    MOTOR = "MOTOR"
    AGITATOR = "AGITATOR"
    SURPRESSOR = "SURPRESSOR"
    COMPRESSOR = "COMPRESSOR"


class Department(Enum):
    REACTIF = "REACTIF"
    COAGULATION = "COAGULATION"
    BIOFOR = "BIOFOR"
    CHARBON_ACTIF = "CHARBON_ACTIF"
    OZONATION = "OZONATION"


class SensorType(Enum):
    THERMAL = "THERMAL"
    VIBRATION = "VIBRATION"
