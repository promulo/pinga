from kafka import KafkaProducer
from pinga.config import get_kafka_config
from pinga.log import get_logger


class Producer():
    """
    A Producer object abstracts the handling
    of sending Kafka events to a given cluster
    """
    def __init__(self):
        self._logger = get_logger()

        kafka_config = get_kafka_config()
        self._kafka_producer = KafkaProducer(
            bootstrap_servers=kafka_config["service_uri"],
            security_protocol="SSL",
            ssl_cafile=kafka_config["ssl_cafile"],
            ssl_certfile=kafka_config["ssl_certfile"],
            ssl_keyfile=kafka_config["ssl_keyfile"],
        )

    def emit(self, event):
        """
        emit sends a given event to the Kafka cluster

        :param event: the event to be sent. It must UTF-8 encodable.
        :raises ProducerException: event provided is invalid
        """
        try:
            message = event.encode("utf-8")
        except AttributeError:
            raise ProducerException(f"emit: event parameter {event} is invalid")

        if event:
            self._logger.info("Emitting event: {}".format(event))
            self._kafka_producer.send("pinga-events", message)
            self._kafka_producer.flush()
        else:
            self._logger.warning("Ignoring attempt of emitting empty string event")


class ProducerException(Exception):
    pass
