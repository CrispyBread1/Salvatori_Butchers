import os
import socket

import requests
import urllib3


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def is_development():
    return os.getenv(
        "APP_ENV",
        "production"
    ).lower() in (
        "development",
        "test",
    )


def is_internal_network():
    if is_development():
        return False

    try:
        socket.getaddrinfo(
            "server69.cw-direct.co.uk",
            50027,
        )
        return True

    except (socket.gaierror, socket.timeout):
        return False


def get_api_url():
    if is_development():
        return None

    internal_url = os.getenv(
        "SAGE_API_URL_INTERNAL"
    )

    external_url = os.getenv(
        "SAGE_API_URL"
    )

    if is_internal_network():
        print(
            "Detected internal network, "
            "prioritizing internal connection"
        )
        return internal_url

    print(
        "Detected external network, "
        "prioritizing external connection"
    )

    return external_url


def get_api_token():
    if is_development():
        return None

    return (
        os.getenv("SAGE_API_TOKEN")
        or os.getenv("API_TOKEN")
    )
