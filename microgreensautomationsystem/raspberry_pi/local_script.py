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
            Subscription("light/switch", qos=0),
            Subscription("water/switch", qos=0),
            Subscription("fan/switch", qos=0)
        ]
    )

def on_message(client:MQTTClient, topic, payload, qos, properties) -> None:
    """
    Callback function that is called when a message is received from the broker.
    """
    payload = payload.decode("utf-8")
    logger.info(f"Topic: {topic}, payload: {payload}")
    
    # Dispatch message based on topic
    if topic.startswith("light"):
        asyncio.create_task(handle_system(client, payload, "light", 8))
    elif topic.startswith("water"):
        asyncio.create_task(handle_system(client, payload, "water", 10))
    elif topic.startswith("fan"):
        asyncio.create_task(handle_system(client, payload, "fan", 12))
    else:
        logger.error(f"Unhandled topic: {topic}")

async def handle_system(client:MQTTClient, payload, system_type:str, gpio_pin:int):
    # Handle system control logic
    if payload.upper() in ("ON", "OFF"):
        try:
            logger.info(f"Turning {system_type} {payload.upper()}...")
            # TODO: Implement GPIO control logic here
            state_info = {"system_type": system_type, "system_state": payload.upper(), "system_event_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            client.publish(f"{system_type}/state", json.dumps(state_info))
        except Exception as e:
            logger.error(f"Error turning {system_type} {payload.upper()}: {e}")
    else:
        logger.error("Invalid payload received")

async def main():
    client = MQTTClient(client_id="raspberry_pi_v2")
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