import json
from unittest.mock import ANY, MagicMock, call, patch

from pinga.events.consumer import Consumer


@patch("pinga.events.consumer.get_db_conn")
@patch("pinga.events.consumer.save_event")
@patch("pinga.events.consumer.get_logger")
@patch(
    "pinga.events.consumer.KafkaConsumer",
    return_value=[
        MagicMock(value=b"hello"),
        MagicMock(value=b"world"),
        MagicMock(value=b"")
    ]
)
def test_consumer_consume_invalid_events(mock_kafka, mock_logger, mock_save, mock_db_conn):
    consumer = Consumer()
    consumer.consume()

    mock_logger().error.assert_has_calls([
        call("Received invalid message: 'hello', skipping"),
        call("Received invalid message: 'world', skipping"),
        call("Received invalid message: '', skipping")
    ])
    mock_save.assert_not_called()


@patch("pinga.events.consumer.get_db_conn")
@patch("pinga.events.consumer.save_event")
@patch("pinga.events.consumer.KafkaConsumer")
def test_consumer_consume_happy_path(mock_kafka, mock_save, mock_db_conn):
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

    mock_save.assert_has_calls([call(ANY, event_1), call(ANY, event_2)])


@patch("pinga.events.consumer.get_db_conn")
@patch("pinga.events.consumer.create_events_table")
@patch("pinga.events.consumer.KafkaConsumer")
def test_consumer_table_created(mock_kafka, mock_create_table, mock_db_conn):
    _ = Consumer()

    mock_create_table.assert_called_once_with(mock_db_conn())
