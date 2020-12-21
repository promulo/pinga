from unittest.mock import patch

import pytest
from pinga.events.producer import Producer, ProducerException


@patch("pinga.events.producer.KafkaProducer")
def test_producer_emit_happy_path(mock_kafka):
    event = "hello world"

    producer = Producer()
    producer.emit(event)

    mock_kafka().send.assert_called_with("pinga-events", event.encode("utf-8"))
    mock_kafka().flush.assert_called_once()


@patch("pinga.events.producer.KafkaProducer")
def test_producer_emit_empty_event_ignored(mock_kafka):
    event = ""

    producer = Producer()
    producer.emit(event)

    mock_kafka().send.assert_not_called()
    mock_kafka().flush.assert_not_called()


@pytest.mark.parametrize(
    "event", [
        (-1,),
        (lambda x: x)
        (None)
    ]
)
@patch("pinga.events.producer.KafkaProducer")
def test_producer_emit_invalid_event(mock_kafka, event):
    producer = Producer()

    with pytest.raises(ProducerException) as exc_info:
        producer.emit(event)

    assert str(exc_info.value) == f"emit: event parameter {event} is invalid"
