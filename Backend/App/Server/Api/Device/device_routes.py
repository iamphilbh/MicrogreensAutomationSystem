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

@app.post("/change_light_state")
async def change_light_state(light_state: LightState) -> dict:
    # Publish a message to the "test" topic
    client.publish("light/switch", light_state.state)
    return {"light_state": light_state.state, "status": "sent"}