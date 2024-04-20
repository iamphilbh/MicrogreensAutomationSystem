import json
import yaml
import os
import asyncio
from typing import List, Dict
from gmqtt import Client as MQTTClient, Subscription
import httpx

from microgreensautomationsystem.core.logger import SharedLogger

class MQTTClientWrapper:
    def __init__(self):
        self.last_message = None
        self.logger = SharedLogger.get_logger()
        # TODO: Trnasfer this to a common/base python file
        # This is the full path since uvicorn runs from the root directory
        with open(os.path.join("microgreensautomationsystem", "backend", "app", "server", "api", "device", "Config", "mqtt_client_config.yml")) as stream:
            try:
                config = yaml.safe_load(stream)
                self._client_id = config["mqtt"]["client_id"]
                self._host = config["mqtt"]["host"]
                self._port = config["mqtt"]["port"]
                self._subscribe_topics = config["mqtt"]["subscribe_topics"]
            except yaml.YAMLError as exc:
                print(exc)

        self._client = MQTTClient(self.client_id)

    @property
    def client(self) -> MQTTClient:
        if not self._client:
            raise ValueError("Client is not set")
        return self._client
    
    @property
    def client_id(self) -> str:
        if not self._client_id:
            raise ValueError("Client ID is not set")
        return self._client_id
    
    @property
    def host(self) -> str:
        if not self._host:
            raise ValueError("Host is not set")
        return self._host

    @property
    def port(self) -> int:
        if not self._port:
            raise ValueError("Port is not set")
        return self._port
    
    @property
    def subscribe_topics(self) -> List[Subscription]:
        if not self._subscribe_topics:
            raise ValueError("Subscribe topic is not set")
        subscribe_topics = [Subscription(topic, qos=0) for topic in self._subscribe_topics]
        return subscribe_topics

    async def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        await self.client.connect(self.host, self.port)

    async def disconnect(self):
        await self.client.disconnect()

    def on_connect(self, client, flags, rc, properties):
        self.client.subscribe(self.subscribe_topics)

    def on_message(self, client, topic, payload, qos, properties):
        self.last_message = json.loads(payload.decode("utf-8"))
        SharedLogger.get_logger().info(f"Received message: {self.last_message}")
        asyncio.create_task(self.save_system_event_to_db(self.last_message))

    async def save_system_event_to_db(self, system_event: Dict) -> None:
        system_type = system_event.get("system_type")
        system_state = system_event.get("system_state")
        SharedLogger.get_logger().info(f"Saving {system_type} state ({system_state}) to database...")

        url = "http://localhost:8000/system_events/"
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=system_event)

        if response.status_code != 200:
            SharedLogger.get_logger().error(f"Failed to save system state to database: {response.text}")

    async def publish(self, topic, message):
        self.client.publish(topic, message, qos=0)