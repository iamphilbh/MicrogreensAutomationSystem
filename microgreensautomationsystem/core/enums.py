from enum import Enum

class SystemType(Enum):
    light = "light"
    fan = "fan"
    pump = "pump"

class SystemState(Enum):
    on = "ON"
    off = "OFF"