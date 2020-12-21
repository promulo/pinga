import json
import os
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from jsonschema import SchemaError, ValidationError, validate

from pinga.schema import SITES_SCHEMA


def get_sites_list() -> dict:
    config = _load_cfg_file()

    try:
        sites_list = config.get('checker', 'sites_list')
    except (NoSectionError, NoOptionError) as err:
        raise BadConfigException(str(err))

    conf_file = Path(sites_list)
    if not conf_file.exists() or not conf_file.is_file():
        raise BadConfigException(f"Configured sites_list file '{sites_list}' does not exist")

    with conf_file.open("r") as f:
        try:
            sites = json.load(f)
            validate(instance=sites, schema=SITES_SCHEMA)
        except json.decoder.JSONDecodeError:
            raise BadConfigException(f"Configured file {sites_list} is not a valid JSON")
        except (SchemaError, ValidationError) as err:
            raise BadConfigException(
                "Required configuration is missing or malformed: {}".format(err.message)
            )

    return sites


def _load_cfg_file() -> ConfigParser:
    config = ConfigParser()
    config.read(os.getenv("PINGA_CFG", default="pinga.cfg"))
    return config


class BadConfigException(Exception):
    """
    Raised when the config YAML is malformed
    """
    pass
