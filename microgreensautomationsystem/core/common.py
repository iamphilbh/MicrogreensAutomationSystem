import os
import json
from typing import List, Dict

import yaml

from .logger import SharedLogger


class Common:

    def __init__(self):
        self.logger = SharedLogger.get_logger()

    def open_config_file(self, file_path: List[str], file_name:str, file_type:str) -> Dict:
        try:
            with open(os.path.join(*file_path, file_name, ".", file_type)) as stream:
                if file_type == "yaml":
                    return yaml.safe_load(stream)
                elif file_type == "json":
                    return json.load(stream)
        except Exception as e:
            self.logger.error(f"Error loading configuration file: {e}")