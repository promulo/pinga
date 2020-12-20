import pytest


@pytest.fixture(autouse=True)
def load_test_env(monkeypatch):
    monkeypatch.setenv("SITES_FILE", "tests/config/sites-test.json")
