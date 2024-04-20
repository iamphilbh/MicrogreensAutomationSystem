from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SystemEvent(BaseModel):
    id: int
    system_type: str
    system_state: str
    system_event_timestamp: datetime
    record_created_timestamp: datetime

class SystemEventCreate(BaseModel):
    system_type: str
    system_state: str
    system_event_timestamp: datetime
    record_created_timestamp: Optional[datetime] = None