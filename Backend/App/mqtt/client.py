from gmqtt import Client as MQTTClient

# Create an MQTT client
client = MQTTClient(client_id="fastapi-mqtt")

# Connect to the MQTT broker
client.connect("localhost", 1883, 60)  # Replace with your broker's hostname/IP and port

async def on_message(client, topic, payload, qos, properties):
    print('RECEIVED MESSAGE:', payload.decode())

async def on_publish(client, topic, payload, qos, properties):
    print('MESSAGE PUBLISHED')

client.on_message = on_message
client.on_publish = on_publish

def publish(topic, message):
    client.publish(topic, message)

def subscribe(topic):
    return client.subscribe(topic)