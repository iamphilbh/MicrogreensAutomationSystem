from typing import List, Dict
import httpx

from microgreensautomationsystem.core.logger import SharedLogger
from microgreensautomationsystem.core.common import Common

class DBClientWrapper(Common):
    def __init__(self):
        self.logger = SharedLogger.get_logger()
        self._config = self.open_config_file(self.config_file_path, "db_client_config", "yml")
        self._host = self.mqtt_config["db"]["host"]
        self._port = self.mqtt_config["db"]["port"]
        self._api_endpoints = self.mqtt_config["db"]["api_endpoints"]

    @property
    def config_file_path(self) -> List[str]:
        return ["microgreensautomationsystem", "backend", "app", "server", "api", "device", "config"]
            
    @property
    def config(self) -> Dict:
        if not self._config:
            raise ValueError("Database config is not set")

        if "db" not in self._config:
            raise ValueError("Key 'db' is not set in database config")

        required_keys = ["host", "port", "api_endpoints"]
        for key in required_keys:
            if key not in self._config["db"].keys():
                raise ValueError(f"{key} is not set in database config")

        return self._config

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
    def api_endpoints(self) -> List[str]:
        if not self._api_endpoints:
            raise ValueError("API endpoints are not set")
        api_endpoints = [endpoint for endpoint in self._api_endpoints]
        return api_endpoints
    
    async def write_system_event(self, system_event: Dict) -> None:
        system_type = system_event.get("system_type")
        system_state = system_event.get("system_state")
        SharedLogger.get_logger().info(f"Saving {system_type} state ({system_state}) to database...")

        url = f"http://{self.host}:{self.port}/{self.api_endpoints[0]}"
        headers = {"Content-Type": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=system_event)

        if response.status_code != 200:
            SharedLogger.get_logger().error(f"Failed to save system state to database: {response.text}")
        else:
            SharedLogger.get_logger().info(f"Successfully saved {system_type} state ({system_state}) to database")