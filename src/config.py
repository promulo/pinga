import json
import os
from pathlib import Path

from jsonschema import SchemaError, ValidationError, validate

from schema import CONFIG_SCHEMA


def get_configured_sites() -> list:
    config = load_config()
    return config["sites"]


def load_config():
    sites_file = os.getenv("SITES_FILE", default="sites.json")
    if not sites_file:
        raise BadConfigException("Required environment variable SITES_FILE is not set")

    conf_file = Path(sites_file)
    if not conf_file.exists():
        raise BadConfigException(f"Configured file {sites_file} file does not exist")

    with conf_file.open("r") as f:
        try:
            config = json.load(f)
            validate(instance=config, schema=CONFIG_SCHEMA)
        except json.decoder.JSONDecodeError:
            raise BadConfigException(f"Configured file {sites_file} is not a valid JSON")
        except (SchemaError, ValidationError) as err:
            raise BadConfigException(
                "Required configuration is missing or malformed: {}".format(err.message)
            )

    return config


class BadConfigException(Exception):
    """
    Raised when the config YAML is malformed
    """
    pass
