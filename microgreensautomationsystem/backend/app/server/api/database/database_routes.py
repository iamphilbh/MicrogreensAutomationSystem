import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from microgreensautomationsystem.backend.app.server.models.database.sqlalchemy_models import SessionLocal, Base, engine, FactSystemEvents
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
    db_system_event = FactSystemEvents(**system_event.model_dump(), record_created_timestamp=datetime.datetime.now())
    db.add(db_system_event)
    db.commit()
    db.refresh(db_system_event)
    return SystemEventRead(**db_system_event.__dict__)

@app.get("/api/system_events/{system_type}/last")
def read_last_system_event(system_type:SystemType, db:Session=Depends(get_db)) -> SystemEventRead:
    db_system_event = (
        db.query(FactSystemEvents)
        .filter(FactSystemEvents.system_type == system_type)
        .order_by(desc(FactSystemEvents.system_event_timestamp))
        .first()
    )
    if db_system_event is None:
        raise HTTPException(status_code=404, detail="System event not found!")
    return SystemEventRead(**db_system_event.__dict__)

@app.get("/api/system_events/{system_type}/all")
def read_all_system_events(system_type:SystemType, db:Session=Depends(get_db)) -> List[SystemEventRead]:
    db_system_events = (
        db.query(FactSystemEvents)
        .filter(FactSystemEvents.system_type == system_type)
        .order_by(desc(FactSystemEvents.system_event_timestamp))
        .all()
    )
    if not db_system_events:
        raise HTTPException(status_code=404, detail="System events not found!")
    return [SystemEventRead(**db_system_event.__dict__) for db_system_event in db_system_events]