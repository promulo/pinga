import json

import gevent
from gevent.pool import Group

from pinga.checker import check_site
from pinga.config import get_sites_list
from pinga.events.producer import Producer
from pinga.log import get_logger


def _check_site_thread(producer, site):
    while True:
        result = check_site(site)
        producer.emit(json.dumps(result))
        gevent.sleep(5)


if __name__ == "__main__":
    logger = get_logger()

    group = Group()

    producer = Producer()

    sites_list = get_sites_list()["sites"]
    logger.info(f"List of sites to be checked by Pinga {sites_list}")
    for site in sites_list:
        group.add(gevent.spawn(_check_site_thread, producer, site))

    try:
        logger.info("Starting Pinga producer...")
        group.join()
    except KeyboardInterrupt:
        logger.info("Pinga producer interrupted. Goodbye.")
        group.kill()
