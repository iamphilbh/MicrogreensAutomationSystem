from typing import Dict

from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from .mqtt_client import MQTTClientWrapper

mqtt_client = MQTTClientWrapper()

class LightState(BaseModel):
    state: str

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
    return {"message": "Hello, World!"}

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> Dict:
    # Publish a message to the "light/switch" topic
    await mqtt_client.publish(topic="light/switch", message=light_state.state)
    return {"light_state": light_state.state, "status": "sent"}