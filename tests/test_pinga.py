import pytest
from jsonschema import SchemaError, ValidationError, validate
from pinga import check_site
from requests.exceptions import RequestException
from schema import STATUS_SCHEMA


def test_check_site():
    try:
        validate(instance=check_site('https://example.org'), schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))


@pytest.mark.parametrize(
    "sample, expected_msg", [
        ("foo", "Invalid URL"),
        ("", "Invalid URL"),
        ("a", "Invalid URL"),
        (None, "Invalid URL"),
        (1, "Invalid URL"),
        ("http://localhost:9999", "Max retries exceeded with url")
    ]
)
def test_check_site_error(sample, expected_msg):
    with pytest.raises(RequestException) as exc:
        validate(instance=check_site(sample), schema=STATUS_SCHEMA)

    assert expected_msg in str(exc.value)
