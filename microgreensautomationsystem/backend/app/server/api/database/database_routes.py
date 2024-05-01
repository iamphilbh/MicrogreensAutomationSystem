import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from microgreensautomationsystem.backend.app.server.models.database.sqlalchemy_models import SessionLocal, Base, engine, SystemEvents, SystemTypes, SystemStates
from microgreensautomationsystem.backend.app.server.models.database.pydantic_models import SystemEventRead, SystemEventCreate
from microgreensautomationsystem.core.enums import SystemType

app = FastAPI()

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@app.get("/")
def root() -> Dict:
    return {"message": "Hello, World! This is the database API."}

@app.post("/api/system_events/create")
def create_system_event(system_event:SystemEventCreate, db:Session=Depends(get_db)) -> SystemEventRead:
    """
    Create a new system event in the database
    """
    # Insert record in SystemTypes table
    db_system_type = SystemTypes(system_type=system_event.system_type)
    db.add(db_system_type)
    db.commit()
    # Insert record in SystemStates table
    db_system_state = SystemStates(system_state=system_event.system_state)
    db.add(db_system_state)
    db.commit()
    # Insert record in SystemEvents table
    db_system_event = SystemEvents(
        system_type_id=db_system_type.id,   # Get the id of the record inserted in SystemTypes table
        system_state_id=db_system_state.id, # Get the id of the record inserted in SystemStates table
        system_event_timestamp=system_event.system_event_timestamp,
        record_created_timestamp=datetime.datetime.now()
    )
    db.add(db_system_event)
    db.commit()
    db.refresh(db_system_event)

    return SystemEventRead(
        id=db_system_event.id,
        system_type=db_system_type.system_type,
        system_state=db_system_state.system_state,
        system_event_timestamp=db_system_event.system_event_timestamp,
        record_created_timestamp=db_system_event.record_created_timestamp
    )

@app.get("/api/system_events/{system_type}/last")
def read_last_system_event(system_type:SystemType, db:Session=Depends(get_db)) -> SystemEventRead:
    """
    Get the last system event for the specified system type
    """
    db_system_event = (
        db.query(SystemEvents, SystemTypes, SystemStates)
        .filter(SystemEvents.system_type_id == SystemTypes.id)
        .filter(SystemEvents.system_state_id == SystemStates.id)
        .filter(SystemTypes.system_type == system_type)
        .order_by(desc(SystemEvents.system_event_timestamp))
        .first()
    )
    if db_system_event is None:
        raise HTTPException(status_code=404, detail="System event not found!")
    
    return SystemEventRead(
        id=db_system_event.SystemEvents.id,
        system_type=db_system_event.SystemTypes.system_type,
        system_state=db_system_event.SystemStates.system_state,
        system_event_timestamp=db_system_event.SystemEvents.system_event_timestamp,
        record_created_timestamp=db_system_event.SystemEvents.record_created_timestamp
    )

@app.get("/api/system_events/{system_type}/all")
def read_all_system_events(system_type:SystemType, db:Session=Depends(get_db)) -> List[SystemEventRead]:
    """
    Query all system events for the specified system type
    """
    db_system_events = (
        db.query(SystemEvents, SystemTypes, SystemStates)
        .filter(SystemEvents.system_type_id == SystemTypes.id)
        .filter(SystemEvents.system_state_id == SystemStates.id)
        .filter(SystemTypes.system_type == system_type)
        .order_by(desc(SystemEvents.system_event_timestamp))
        .all()
    )
    if db_system_events is None:
        raise HTTPException(status_code=404, detail="System events not found!")
    
    return [
        SystemEventRead(
            id=db_system_event.SystemEvents.id,
            system_type=db_system_event.SystemTypes.system_type,
            system_state=db_system_event.SystemStates.system_state,
            system_event_timestamp=db_system_event.SystemEvents.system_event_timestamp,
            record_created_timestamp=db_system_event.SystemEvents.record_created_timestamp
        )
        for db_system_event in db_system_events
    ]