from unittest.mock import call, patch

from pinga.persistence import QUERY_INSERT_ERROR_EVENT, QUERY_INSERT_EVENT, save_event


@patch("pinga.persistence.psycopg2.connect")
def test_save_event(mock_db):
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

    save_event(event_1)
    save_event(event_2)

    mock_db().cursor().execute.assert_has_calls([
        call(QUERY_INSERT_EVENT, ("http://example.org/404", "down", 404, 0.160735)),
        call(QUERY_INSERT_ERROR_EVENT, ("a.a", "error", "some error"))
    ])
