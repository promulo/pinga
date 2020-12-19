import pytest
from jsonschema import SchemaError, ValidationError, validate
from pinga import check_site
from schema import STATUS_SCHEMA


def test_check_site():
    try:
        validate(instance=check_site('http://google.com'), schema=STATUS_SCHEMA)
    except (SchemaError, ValidationError) as err:
        pytest.fail("Unexpected validation error: {}".format(err))
