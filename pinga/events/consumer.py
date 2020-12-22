import json
from uuid import uuid4

from jsonschema import SchemaError, ValidationError, validate
from kafka import KafkaConsumer
from pinga.config import get_kafka_config
from pinga.log import get_logger
from pinga.persistence import insert_error_event, insert_event
from pinga.schema import STATUS_SCHEMA


class Consumer:
    """
    A Consumer object abstracts the handling
    of consuming events from a Kafka cluster
    """
    POLL_TIMEOUT = 1000

    def __init__(self):
        self._logger = get_logger()

        kafka_config = get_kafka_config()
        self._kafka_consumer = KafkaConsumer(
            "pinga-events",
            bootstrap_servers=kafka_config["service_uri"],
            client_id=f"pinga-consumer-{uuid4()}",
            group_id="pinga-consumer-group",
            auto_offset_reset='earliest',
            security_protocol="SSL",
            ssl_cafile=kafka_config["ssl_cafile"],
            ssl_certfile=kafka_config["ssl_certfile"],
            ssl_keyfile=kafka_config["ssl_keyfile"],
        )

    def consume(self):
        """
        Listens for and processes incoming messages
        sent to the respective Kafka topic
        """
        for received in self._kafka_consumer:
            message = received.value.decode("utf-8")
            try:
                event = json.loads(message)
                validate(instance=event, schema=STATUS_SCHEMA)
            except (json.decoder.JSONDecodeError, SchemaError, ValidationError):
                self._logger.error(f"Received invalid message: '{message}'")
                continue

            self._logger.info(f"Received message: '{message}'")
            if event["status"] == "error":
                insert_error_event(event)
            else:
                insert_event(event)
