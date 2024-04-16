from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

from .mqtt_client import MQTTClientWrapper

app = FastAPI()

mqtt_client = MQTTClientWrapper()

class LightState(BaseModel):
    state: str

@app.get("/")
def read_root() -> Dict:
    return {"message": "Hello, World!"}

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> Dict:
    # Publish a message to the "light/switch" topic
    await MQTTClientWrapper.publish("light/switch", light_state.state)
    return {"light_state": light_state.state, "status": "sent"}

@app.get("/get_light_state")
async def get_light_state() -> Dict:
    # Subscribe to the "light/state" topic
    # Retrieve from Database
    result = "Retrieving from database..."
    return {"state": result}