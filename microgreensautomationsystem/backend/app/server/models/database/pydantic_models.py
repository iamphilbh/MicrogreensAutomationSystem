from datetime import datetime
from pydantic import (
    BaseModel,
    field_validator
)

from microgreensautomationsystem.core.enums import SystemState, SystemType

class Base(BaseModel):
    system_type: str
    system_state: str

    @field_validator("system_type")
    @classmethod
    def validate_system_type(cls, v:str) -> str:
        if v.lower() not in (e.value for e in SystemType):
            raise ValueError(f"The value provided for the system type is wrong. Got '{v}'.")
        return v.lower()
    
    @field_validator("system_state")
    @classmethod
    def validate_system_state(cls, v:str) -> str:
        if v.upper() not in (e.value for e in SystemState):
            raise ValueError(f"The value provided for the system state is wrong. Got '{v}'.")
        return v.upper()
    
class SystemEvent(Base):
    id: int
    system_event_timestamp: datetime
    record_created_timestamp: datetime

class SystemEventCreate(Base):
    system_event_timestamp: datetime