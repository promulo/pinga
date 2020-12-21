import requests

from log import get_logger


def check_site(site_url: str) -> dict:
    """
    Checks if a given site is up or now by sending and HTTP
    request to the given URL

    :param site_url: the event to be sent. It must UTF-8 encodable.
    :returns: the result of the HTTP request as dict
    """
    logger = get_logger()
    try:
        response = requests.get(site_url)
        status = "up" if response.ok else "down"
        result = {
            "url": site_url,
            "status": status,
            "httpStatus": response.status_code,
            "responseTimeSeconds": response.elapsed.total_seconds()
        }
        logger.info(result)
    except requests.RequestException as exc:
        result = {
            "url": site_url,
            "status": "error",
            "errorMessage": str(exc)
        }
        logger.error(result)

    return result
