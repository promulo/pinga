from kafka import KafkaProducer
from pinga.config import get_kafka_config
from pinga.log import get_logger


class Producer:
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
        Sends a message (event) to the respective Kafka topic

        :param event: the message to be sent. It must be UTF-8 encodable.
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

    def shutdown(self):
        """
        Shuts down producer by closing the Kafka producer
        """
        self._logger.info("Closing Kafka producer")
        self._kafka_producer.flush()
        self._kafka_producer.close()


class ProducerException(Exception):
    pass
