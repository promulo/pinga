import pytest


@pytest.fixture(autouse=True)
def load_test_env(monkeypatch):
    monkeypatch.setenv("PINGA_CFG", "tests/config/pinga-test.cfg")
