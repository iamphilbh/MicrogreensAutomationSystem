from datetime import datetime
from pydantic import BaseModel

from microgreensautomationsystem.core.enums import SystemState, SystemType

class SystemBase(BaseModel):
    system_type: SystemType
    system_state: SystemState
    
class SystemEvent(SystemBase):
    id: int
    system_event_timestamp: datetime
    record_created_timestamp: datetime

class SystemEventCreate(SystemBase):
    system_event_timestamp: datetime