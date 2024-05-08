import json
import asyncio
from typing import List, Dict
from gmqtt import Client as MQTTClient, Subscription

from microgreensautomationsystem.core.logger import SharedLogger
from microgreensautomationsystem.core.common import Common
from .db_client import DBClientWrapper

class MQTTClientWrapper(Common):
    def __init__(self):
        self.last_message = None
        self.logger = SharedLogger.get_logger()
        self.db_client = DBClientWrapper()

        self._config = self.open_config_file(self.config_file_path, "mqtt_client_config", "yml")
        self._client_id = self.config["mqtt"]["client_id"]
        self._host = self.config["mqtt"]["host"]
        self._port = self.config["mqtt"]["port"]
        self._subscribe_topics = self.config["mqtt"]["subscribe_topics"]
        self._client = MQTTClient(self.client_id)

    @property
    def config_file_path(self) -> List[str]:
        return ["microgreensautomationsystem", "backend", "app", "server", "api", "device", "config"]
    
    @property
    def config(self) -> Dict:
        if not self._config:
            raise ValueError("MQTT config is not set")

        if "mqtt" not in self._config:
            raise ValueError("Key 'mqtt' is not set in MQTT config")

        required_keys = ["client_id", "host", "port", "subscribe_topics"]
        for key in required_keys:
            if key not in self._config["mqtt"].keys():
                raise ValueError(f"{key} is not set in MQTT config")
        return self._config

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
        asyncio.create_task(self.db_client.write_system_event(self.last_message))

    async def publish(self, topic, message):
        self.client.publish(topic, message, qos=0)