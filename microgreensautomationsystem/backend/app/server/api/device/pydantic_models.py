from pydantic import BaseModel
from microgreensautomationsystem.core.enums import SystemState, SystemType

class System(BaseModel):
    system_type: SystemType
    system_state: SystemState