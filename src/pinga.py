import requests


def check_site(site: str) -> dict:
    response = requests.get(site)
    result = {
        "httpStatus": response.status_code,
        "responseTimeSeconds": response.elapsed.total_seconds()
    }
    return result
