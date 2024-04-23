from enum import Enum

class SystemType(str, Enum):
    light = "light"
    fan = "fan"
    pump = "pump"

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError(f"{value} is not a valid SystemType")

class SystemState(str, Enum):
    ON = "ON"
    OFF = "OFF"

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.upper():
                return member
        raise ValueError(f"{value} is not a valid SystemState")