from datetime import datetime
from pydantic import BaseModel

from microgreensautomationsystem.core.enums import SystemState, SystemType

class SystemBase(BaseModel):
    """
    Base class. All system events need at least these two fields.
    """
    system_type: SystemType
    system_state: SystemState
    
class SystemEventRead(SystemBase):
    """
    System event read class. This class is used to represent a system event in the database.
    """
    id: int
    system_event_timestamp: datetime
    record_created_timestamp: datetime

class SystemEventCreate(SystemBase):
    """
    System event create class. This class is used to represent a system event creation in the database.
    """
    system_event_timestamp: datetime