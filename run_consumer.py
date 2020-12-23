from pinga.events.consumer import Consumer
from pinga.log import get_logger


if __name__ == "__main__":
    logger = get_logger()

    consumer = Consumer()
    try:
        logger.info("Starting Pinga consumer...")
        consumer.consume()
    except KeyboardInterrupt:
        logger.info("Pinga consumer interrupted. Goodbye.")
        consumer.shutdown()
