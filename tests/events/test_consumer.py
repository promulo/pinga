import json
from unittest.mock import MagicMock, call, patch

from pinga.events.consumer import Consumer


@patch("pinga.events.consumer.insert_error_event")
@patch("pinga.events.consumer.insert_event")
@patch("pinga.events.consumer.get_logger")
@patch(
    "pinga.events.consumer.KafkaConsumer",
    return_value=[
        MagicMock(value=b"hello"),
        MagicMock(value=b"world"),
        MagicMock(value=b"")
    ]
)
def test_consumer_consume_invalid_events(mock_kafka, mock_logger, mock_insert, mock_insert_err):
    consumer = Consumer()
    consumer.consume()

    mock_logger().error.assert_has_calls([
        call("Received invalid message: 'hello'"),
        call("Received invalid message: 'world'"),
        call("Received invalid message: ''")
    ])
    mock_insert.assert_not_called()
    mock_insert_err.assert_not_called()


@patch("pinga.events.consumer.insert_error_event")
@patch("pinga.events.consumer.insert_event")
@patch("pinga.events.consumer.KafkaConsumer")
def test_consumer_consume_happy_path(mock_kafka, mock_insert, mock_insert_err):
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
    mock_kafka.return_value = [
        MagicMock(value=json.dumps(event_1).encode("utf-8")),
        MagicMock(value=json.dumps(event_2).encode("utf-8"))
    ]

    consumer = Consumer()
    consumer.consume()

    mock_insert.assert_called_once_with(event_1)
    mock_insert_err.assert_called_once_with(event_2)
