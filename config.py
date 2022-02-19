# -- First you import Dynaconf
from dynaconf import Dynaconf, Validator
from os.path import exists
from pathlib import Path

if exists("../.Chia_WebSocket_MQTT") and Path("../.Chia_WebSocket_MQTT/settings.toml").is_file():
    print("Loading settings from ../.Chia_WebSocket_MQTT/settings.toml & .env")
    settings = Dynaconf(
        # settings_files=["../.Chia_WebSocket_MQTT/settings.toml"],
        environments=True,
        load_dotenv=True,
        envvar_prefix="DYNACONF",
        env_switcher="ENV_FOR_DYNACONF",
        dotenv_path="../.Chia_WebSocket_MQTT/.env",
        settings_files=["../.Chia_WebSocket_MQTT/settings.toml"]
    )
else:
    # -- Then you create your `settings` instance
    print("using default settings")
    settings = Dynaconf(
        settings_files=["configs/settings.toml"],
        environments=True,
        load_dotenv=True,
        envvar_prefix="DYNACONF",
        env_switcher="ENV_FOR_DYNACONF",
        dotenv_path="configs/.env"
    )

