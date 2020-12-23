from unittest.mock import patch

from pinga.persistence import (QUERY_INSERT_ERROR_EVENT, QUERY_INSERT_EVENT,
                               insert_error_event, insert_event)


@patch("pinga.persistence.psycopg2.connect")
def test_insert_event(mock_db):
    event = {
        "url": "http://example.org/404",
        "status": "down",
        "httpStatus": 404,
        "responseTimeSeconds": 0.160735
    }

    insert_event(event)

    mock_db().cursor().execute.assert_called_once_with(
        QUERY_INSERT_EVENT,
        ("http://example.org/404", "down", 404, 0.160735)
    )


@patch("pinga.persistence.psycopg2.connect")
def test_insert_error_event(mock_db):
    event = {
        "url": "a.a",
        "status": "error",
        "errorMessage": "some error"
    }

    insert_error_event(event)

    mock_db().cursor().execute.assert_called_once_with(
        QUERY_INSERT_ERROR_EVENT,
        ("a.a", "error", "some error")
    )
