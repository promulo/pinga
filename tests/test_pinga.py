import pytest
from jsonschema import SchemaError, ValidationError, validate
from pinga import check_site
from schema import STATUS_SCHEMA


def test_check_site_happy_path(requests_mock):
    test_site = "http://example.org"
    requests_mock.get(test_site)

    result = check_site(test_site)

    try:
        validate(instance=result, schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))
    assert result["url"] == test_site
    assert result["status"] == "up"
    assert result["httpStatus"] == 200


@pytest.mark.parametrize(
    "sample, expected_msg", [
        ("foo", "Invalid URL"),
        ("", "Invalid URL"),
        ("a", "Invalid URL"),
        ("1", "Invalid URL"),
        ("http://localhost:9999", "Max retries exceeded with url")
    ]
)
def test_check_site_error(sample, expected_msg):
    result = check_site(sample)

    try:
        validate(instance=result, schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))
    assert result["url"] == sample
    assert result["status"] == "error"
    assert expected_msg in result["errorMessage"]
