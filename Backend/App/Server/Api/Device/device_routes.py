from fastapi import FastAPI
from gmqtt import Client as MQTTClient, Subscription
from pydantic import BaseModel

from client import publish, subscribe, setup_mqtt

app = FastAPI()

class LightState(BaseModel):
    state: str

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, World!"}

@app.on_event("startup")
async def startup_event():
    await setup_mqtt()

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> dict:
    # Publish a message to the "light/switch" topic
    await publish("light/switch", light_state.state)
    return {"light_state": light_state.state, "status": "sent"}

@app.get("/get_light_state")
async def get_light_state() -> dict:
    # Subscribe to the "light/state" topic
    result = await subscribe("light/state")
    return {"state": result}