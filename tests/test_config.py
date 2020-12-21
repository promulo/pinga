from unittest.mock import patch

import pytest
from pinga.config import BadConfigException, get_kafka_config, get_sites_list


@pytest.mark.parametrize(
    "sites_file, error_msg", [
        ("", "Configured sites_list file '' does not exist"),
        ("notexists.json", "Configured sites_list file 'notexists.json' does not exist"),
        ("tests/config/sites-test-bad.json",
            "Required configuration is missing or malformed: 'sites' is a required property"),
        ("tests/config/sites-test-bad2.json",
            "Configured file tests/config/sites-test-bad2.json is not a valid JSON")
    ]
)
@patch("pinga.config.ConfigParser.get")
def test_get_sites_list_errors(mock_parser, sites_file, error_msg):
    mock_parser.return_value = sites_file

    with pytest.raises(BadConfigException) as exc:
        get_sites_list()

    assert str(exc.value) == error_msg


def test_get_sites_list_missing(monkeypatch):
    monkeypatch.setenv("PINGA_CFG", "tests/config/bad.cfg")

    with pytest.raises(BadConfigException) as exc:
        get_sites_list()

    assert str(exc.value) == "No section: 'checker'"


def test_get_sites_list_happy_path():
    sites_list = get_sites_list()

    assert sites_list is not None
    assert "sites" in sites_list
    assert "http://test.example.org" in sites_list["sites"]


def test_get_kafka_config_happy_path():
    kafka_config = get_kafka_config()

    assert kafka_config["service_uri"] == "example.org:123456"
    assert kafka_config["ssl_cafile"] == "ca.pem"
    assert kafka_config["ssl_certfile"] == "service.cert"
    assert kafka_config["ssl_keyfile"] == "service.key"


def test_get_kafka_config_missing(monkeypatch):
    monkeypatch.setenv("PINGA_CFG", "tests/config/bad.cfg")

    with pytest.raises(BadConfigException) as exc:
        get_kafka_config()

    assert str(exc.value) == "Required section 'kafka' not found in .cfg file"
