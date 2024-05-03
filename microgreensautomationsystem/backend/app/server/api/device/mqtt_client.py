import json
import asyncio
from typing import List, Dict
from gmqtt import Client as MQTTClient, Subscription
import httpx

from microgreensautomationsystem.core.logger import SharedLogger
from microgreensautomationsystem.core.common import Common

class MQTTClientWrapper(Common):
    def __init__(self):
        self.last_message = None
        self.logger = SharedLogger.get_logger()
        self._mqtt_config = self.open_config_file(self.config_file_path, "mqtt_client_config", "yml")
        self._client_id = self.mqtt_config["mqtt"]["client_id"]
        self._host = self.mqtt_config["mqtt"]["host"]
        self._port = self.mqtt_config["mqtt"]["port"]
        self._subscribe_topics = self.mqtt_config["mqtt"]["subscribe_topics"]
        self._client = MQTTClient(self.client_id)

    @property
    def config_file_path(self) -> List[str]:
        return ["microgreensautomationsystem", "backend", "app", "server", "api", "device", "config"]
    
    @property
    def mqtt_config(self) -> Dict:
        if not self._mqtt_config:
            raise ValueError("MQTT config is not set")

        if "mqtt" not in self._mqtt_config:
            raise ValueError("MQTT config is not set")

        required_keys = ["client_id", "host", "port", "subscribe_topics"]
        for key in required_keys:
            if key not in self._mqtt_config["mqtt"].keys():
                raise ValueError(f"{key} is not set in MQTT config")

        return self._mqtt_config

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

        url = "http://localhost:8080/api/database/system_events/create" # TODO: Move to config
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=system_event)

        if response.status_code != 200:
            SharedLogger.get_logger().error(f"Failed to save system state to database: {response.text}")
        else:
            SharedLogger.get_logger().info(f"Successfully saved {system_type} state ({system_state}) to database")

    async def publish(self, topic, message):
        self.client.publish(topic, message, qos=0)