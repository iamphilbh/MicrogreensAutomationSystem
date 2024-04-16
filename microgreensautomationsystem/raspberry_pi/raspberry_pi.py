import logging
from datetime import datetime
import json
import asyncio
import os

from dotenv import load_dotenv
from gmqtt import Client as MQTTClient, Subscription
import RPi.GPIO as GPIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

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

async def on_message(client:MQTTClient, topic, payload, qos, properties) -> None:
    """
    Callback function that is called when a message is received from the broker.
    """
    payload = payload.decode("utf-8")
    logger.info(f"Topic: {topic}, payload: {payload}")
    
    # Dispatch message based on topic
    if topic.startswith("light"):
        asyncio.create_task(handle_system(client, payload, "light/state", "light", 8))
    elif topic.startswith("water"):
        asyncio.create_task(handle_system(client, payload, "water/state", "water", 10))
    elif topic.startswith("fan"):
        asyncio.create_task(handle_system(client, payload, "fan/state", "fan", 12))
    else:
        logger.error(f"Unhandled topic: {topic}")

async def handle_system(client:MQTTClient, payload, pub_topic:str, system_type:str, gpio_pin:int):
    # Handle system control logic
    if payload.upper() == "ON":
        logger.info(f"Turning {system_type} on...")
        GPIO.output(gpio_pin, GPIO.HIGH)
        state_info = {"state": "ON", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        client.publish(pub_topic, json.dumps(state_info))
    elif payload.upper() == "OFF":    
        logger.info(f"Turning {system_type} off...")
        GPIO.output(gpio_pin, GPIO.LOW)
        state_info = {"state": "OFF", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        client.publish(pub_topic, json.dumps(state_info))
    else:
        logger.error("Invalid payload received")

async def main():
    client = MQTTClient(client_id="raspberry_pi")
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
        GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(main())