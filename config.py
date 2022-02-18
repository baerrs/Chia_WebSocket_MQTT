# -- First you import Dynaconf
from dynaconf import Dynaconf, Validator

# -- Then you create your `settings` instance
settings = Dynaconf(
    settings_files=["configs/settings.toml"],
    environments=True,
    load_dotenv=True,
    envvar_prefix="DYNACONF",
    env_switcher="ENV_FOR_DYNACONF",
    dotenv_path="configs/.env"
)

