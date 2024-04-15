import logging
from datetime import datetime
import json
import asyncio
import os

from dotenv import load_dotenv
from gmqtt import Client as MQTTClient, Subscription

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
# Accessing variables
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_port = int(os.getenv("MQTT_PORT", 1883))  # Providing a default value if not set

def on_connect(client: MQTTClient, flags, rc, properties) -> None:
    """
    Callback function that is called when the MQTT client successfully connects to the broker.
    """
    logger.info(f"Connected with result code: {rc}")
    client.subscribe(
        [
            Subscription("light/state", qos=0),
            Subscription("water/state", qos=0),
            Subscription("fan/state", qos=0)
        ]
    )

def on_message(client:MQTTClient, topic, payload, qos, properties) -> None:
    """
    Callback function that is called when a message is received from the broker.
    """
    payload = json.loads(payload.decode("utf-8"))
    logger.info(f"Topic: {topic}, payload: {payload}")
    
    # Dispatch message based on topic
    if topic.startswith("light"):
        asyncio.create_task(handle_system(client, payload, "light"))
    elif topic.startswith("water"):
        asyncio.create_task(handle_system(client, payload, "water"))
    elif topic.startswith("fan"):
        asyncio.create_task(handle_system(client, payload, "fan"))
    else:
        logger.error(f"Unhandled topic: {topic}")

async def handle_system(client:MQTTClient, payload, system_type:str,):
    # Handle system control logic
    if payload.get("state") in ("ON", "OFF"):
        logger.info(f"Processing {system_type}, state: {payload.get('state')}")
    else:
        logger.error("Invalid payload received")

async def main():
    client = MQTTClient(client_id="backend_client")
    client.on_connect = on_connect
    client.on_message = on_message

    await client.connect(mqtt_broker, mqtt_port)
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())