import logging
from datetime import datetime
import json

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

def on_connect(client:mqtt.Client, userdata, flags, rc:int) -> None:
    """
    Callback function that is called when the MQTT client successfully connects to the broker.
    
    Parameters
    ----------
        client (mqtt.Client): The client instance for this callback
        userdata: The private user data as set in Client()
        flags: Response flags sent by the broker
        rc (int): The connection result

    Returns
    -------
        None
    """
    logger.info("Connected with result code "+str(rc))
    client.subscribe("light/switch")

def on_message(client:mqtt.Client, userdata, msg:mqtt.MQTTMessage) -> None:
    """
    Callback function that is called when a message is received from the broker.
    
    Parameters
    ----------
        client (mqtt.Client): The client instance for this callback
        userdata: The private user data as set in Client()
        msg (mqtt.MQTTMessage): An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.

    Returns
    -------
        None
    """
    logger.info("Topic: "+msg.topic+", payload: "+str(msg.payload))

    payload = msg.payload.decode('utf-8')
    light_status_topic = "light/state"

    if payload.upper() == "ON":
        logger.info("Turning LED on...")
        GPIO.output(8, GPIO.HIGH)
        status_info = {"state": "ON", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        client.publish(light_status_topic, json.dumps(status_info))
    elif payload.upper() == "OFF":    
        logger.info("Turning LED off...")
        GPIO.output(8, GPIO.LOW)
        status_info = {"state": "OFF", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        client.publish(light_status_topic, json.dumps(status_info))
    else:
        logger.error("Invalid payload received")

if __name__ == "__main__":
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Exiting...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")