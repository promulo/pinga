from unittest.mock import call, patch

from pinga.persistence import (QUERY_INSERT_ERROR_EVENT, QUERY_INSERT_EVENT,
                               get_db_conn, save_event)


@patch("pinga.persistence.psycopg2.connect")
def test_get_db_conn(mock_db):
    get_db_conn()

    mock_db.assert_called_once_with("postgresl://foo:bar@localhost/test")


@patch("pinga.persistence.psycopg2.connect")
def test_save_event(mock_db_conn):
    event_1 = {
        "url": "http://example.org/404",
        "status": "down",
        "httpStatus": 404,
        "responseTimeSeconds": 0.160735
    }
    event_2 = {
        "url": "a.a",
        "status": "error",
        "errorMessage": "some error"
    }

    save_event(mock_db_conn(), event_1)
    save_event(mock_db_conn(), event_2)

    mock_db_conn().cursor().execute.assert_has_calls([
        call(QUERY_INSERT_EVENT, ("http://example.org/404", "down", 404, 0.160735)),
        call(QUERY_INSERT_ERROR_EVENT, ("a.a", "error", "some error"))
    ])
