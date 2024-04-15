import logging
from datetime import datetime
import json
import asyncio
import os

from dotenv import load_dotenv
from gmqtt import Client as MQTTClient, Subscription

class MQTTClientWrapper:
    def __init__(self, client_id):
        self.client = MQTTClient(client_id)
        self.last_message = None
        # TODO: Load YAML config file (host, port, topics)

    async def connect(self, host, port):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        await self.client.connect(host, port)

    async def disconnect(self):
        await self.client.disconnect()

    def on_connect(self, client, flags, rc, properties):
        self.client.subscribe("light/state", qos=0)

    def on_message(self, client, topic, payload, qos, properties):
        self.last_message = json.loads(payload.decode("utf-8"))

    async def publish(self, topic, message):
        self.client.publish(topic, message, qos=1)

    async def subscribe(self, topic):
        self.client.subscribe(topic, qos=1)
        return self.last_message