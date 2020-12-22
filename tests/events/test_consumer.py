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
def test_producer_emit_invalid_events(mock_kafka, mock_logger, mock_insert, mock_insert_err):
    consumer = Consumer()
    consumer.consume()

    mock_logger().error.assert_has_calls([
        call("Received invalid message: 'hello'"),
        call("Received invalid message: 'world'"),
        call("Received invalid message: ''")
    ])
    mock_insert.assert_not_called()
    mock_insert_err.assert_not_called()
