from fastapi import FastAPI
from gmqtt import Client as MQTTClient, Subscription
from pydantic import BaseModel

from app.mqtt.client import publish, subscribe

app = FastAPI()

class LightState(BaseModel):
    state: str

@app.get("/")
async def read_root() -> dict:
    return {"message": "Hello, World!"}

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> dict:
    # Publish a message to the "light/switch" topic
    publish("light/switch", light_state.state)
    return {"light_state": light_state.state, "status": "sent"}

@app.get("/light_state")
async def get_light_state() -> dict:
    # Subscribe to the "light/state" topic
    result = subscribe("light/state")
    return {"state": result.get("state", "unknown")}