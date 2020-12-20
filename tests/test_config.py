import os

import pytest
from config import BadConfigException, load_config


@pytest.mark.parametrize(
    "env_var, error_msg", [
        ("", "Required environment variable SITES_FILE is not set"),
        ("notexists.json", "Configured file notexists.json file does not exist"),
        ("tests/config/sites-test-bad.json",
            "Required configuration is missing or malformed: 'sites' is a required property"),
        ("tests/config/sites-test-bad2.json",
            "Configured file tests/config/sites-test-bad2.json is not a valid JSON")
    ]
)
def test_load_config_errors(env_var, error_msg):
    os.environ["SITES_FILE"] = env_var

    with pytest.raises(BadConfigException) as exc:
        load_config()

    assert str(exc.value) == error_msg


def test_load_config_happy_path():
    config = load_config()
    assert config is not None
    assert "sites" in config
    assert "example.org" in config["sites"]
