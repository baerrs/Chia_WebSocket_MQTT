import os
from pathlib import Path

CONFIGURATION_PATH = Path(os.path.expanduser(os.getenv("CHIA_ROOT", "~/.Chia_WebSocket_MQTT"))).resolve()
print("CONFIGURATION_PATH:", CONFIGURATION_PATH)
