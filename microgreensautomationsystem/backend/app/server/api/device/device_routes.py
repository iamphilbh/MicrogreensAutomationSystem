from typing import Dict

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .mqtt_client import MQTTClientWrapper
from .pydantic_models import System

mqtt_client = MQTTClientWrapper()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Connect to MQTT broker
    await mqtt_client.connect()
    yield
    # Shutdown
    # Disconnect from MQTT broker
    await mqtt_client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root() -> Dict:
    return {"message": "Hello, World! This is the device API."}

@app.post("/api/device/system_events/activate")
async def activate_switch(system: System) -> Dict:
    topic = f"{system.system_type.value}/switch"
    await mqtt_client.publish(topic=topic, message=system.system_state.value)
    return {"system_type": system.system_type.value, "system_state": system.system_state.value, "request_status": "sent"}