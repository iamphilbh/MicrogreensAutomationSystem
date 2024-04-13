from gmqtt import Client as MQTTClient

# Set up the MQTT client
client = MQTTClient("fastapi-mqtt-client")

# Variable to store the last received message
last_message = None

def on_message(client, message):
    
    print("in on_message")
    last_message = message.payload.decode("utf-8")

async def setup_mqtt():
    # Connect to the broker
    await client.connect("localhost", 1883)

async def publish(topic, message):
    # Publish a message to a topic
    client.publish(topic, message, qos=1)

async def subscribe(topic):
    # Subscribe to a topic and return the last message received
    client.on_message = on_message
    client.subscribe(topic, qos=1)
    print("in subscribe")
    print(last_message)
    return last_message





# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def on_connect(client: MQTTClient, flags, rc, properties) -> None:
#     logger.info(f"Connected with result code: {rc}")
#     client.subscribe(
#         [
#             Subscription("light/switch", qos=0),
#             Subscription("light/state", qos=0),
#             Subscription("water/switch", qos=0),
#             Subscription("water/state", qos=0),
#             Subscription("fan/switch", qos=0),
#             Subscription("fan/state", qos=0)
#         ]
#     )

# def on_message(client, topic, payload, qos, properties):
#     payload = payload.decode("utf-8")
#     logger.info(f"Topic: {topic}, payload: {payload}")

# def on_publish(client, topic, payload, qos, properties):
#     logger.info('MESSAGE PUBLISHED')

# def publish(client, topic, message):
#     client.publish(topic, message)

# def subscribe(client, topic):
#     return client.subscribe(topic)