from unittest.mock import MagicMock, call, patch

from pinga.events.consumer import Consumer


@patch("pinga.events.consumer.get_logger")
@patch(
    "pinga.events.consumer.KafkaConsumer",
    return_value=[
        MagicMock(value=b"hello"),
        MagicMock(value=b"world")
    ]
)
def test_producer_emit_happy_path(mock_kafka, mock_logger):
    consumer = Consumer()
    consumer.consume()

    mock_logger().info.assert_has_calls([call("Received: hello"), call("Received: world")])
