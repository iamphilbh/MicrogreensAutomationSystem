from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from microgreensautomationsystem.backend.app.server.models.database_models import SessionLocal, Base, engine, FactSystemEvents
from microgreensautomationsystem.backend.app.server.models.pydantic_models import SystemEvent, SystemEventCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Connect to MQTT broker
    await Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@app.get("/")
async def root() -> Dict:
    return {"message": "Hello, World!"}

@app.post("/system_events/")
def create_system_event(system_event:SystemEvent, db:Session=Depends(get_db)) -> SystemEvent:
    db_system_event = SystemEvent(**system_event.model_dump())
    db.add(db_system_event)
    db.commit()
    db.refresh(db_system_event)
    return SystemEvent(**db_system_event.__dict__)


@app.get("/system_events/{system_type}")
def read_system_state(system_type:str, db:Session=Depends(get_db)) -> SystemEvent:
    db_system = db.query(FactSystemEvents).filter(FactSystemEvents.system_type == system_type).first()
    if db_system is None:
        raise HTTPException(status_code=404, detail="System not found")
    return SystemEvent(**db_system.__dict__)