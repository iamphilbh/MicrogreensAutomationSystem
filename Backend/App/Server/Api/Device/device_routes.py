from fastapi import FastAPI
from paho.mqtt.client import Client as MQTTClient
from pydantic import BaseModel

app = FastAPI()

# Create an MQTT client
client = MQTTClient()

# Connect to the MQTT broker
client.connect("192.168.0.68", 1883, 60)  # Replace with your broker's hostname/IP and port

class LightState(BaseModel):
    state: str

@app.get("/")
async def read_root() -> dict:
    return {"message": "Hello, World!"}

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> dict:
    # Publish a message to the "light/switch" topic
    client.publish("light/switch", light_state.state)
    return {"light_state": light_state.state, "status": "sent"}

@app.get("/light_state")
async def get_light_state() -> dict:
    # Subscribe to the "light/state" topic
    result = client.subscribe("light/state")
    return {"state": result.get("state", "unknown")}