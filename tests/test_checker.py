import pytest
from jsonschema import SchemaError, ValidationError, validate
from pinga.checker import check_site
from pinga.schema import STATUS_SCHEMA


@pytest.mark.parametrize(
    "url, status, http_status", [
        ("http://example.org", "up", 200),
        ("http://example.org/404", "down", 404),
        ("http://example.org/500", "down", 500)
    ]
)
def test_check_site_happy_path(url, status, http_status, requests_mock):
    requests_mock.get(url, status_code=http_status)

    result = check_site(url)

    try:
        validate(instance=result, schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))
    assert result["url"] == url
    assert result["status"] == status
    assert result["httpStatus"] == http_status


@pytest.mark.parametrize(
    "url, expected_msg", [
        ("foo", "Invalid URL"),
        ("", "Invalid URL"),
        ("a", "Invalid URL"),
        ("1", "Invalid URL"),
        ("http://localhost:9999", "Max retries exceeded with url")
    ]
)
def test_check_site_error(url, expected_msg):
    result = check_site(url)

    try:
        validate(instance=result, schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))
    assert result["url"] == url
    assert result["status"] == "error"
    assert expected_msg in result["errorMessage"]
