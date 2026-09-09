import os
import socket

import urllib3

def get_app_environment():
    return os.getenv("APP_ENV", "production").strip().lower()


def is_development():
    return get_app_environment() == "development"


def is_test():
    return get_app_environment() == "test"


def is_production():
    return get_app_environment() == "production"


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def use_dummy_sage():
    return is_development() or is_test()


def is_internal_network():
    if use_dummy_sage():
        return False

    try:
        socket.getaddrinfo(
            "server69.cw-direct.co.uk",
            50027
        )

        return True

    except (socket.gaierror, socket.timeout):
        return False

    finally:
        socket.setdefaulttimeout(None)


def get_api_url():
    if use_dummy_sage():
        return None

    internal_url = os.getenv("SAGE_API_URL_INTERNAL")
    external_url = os.getenv("SAGE_API_URL")

    if is_internal_network():
        print(
            "Detected internal network, "
            "prioritizing direct internal connection"
        )

        return internal_url

    print(
        "Detected external network, "
        "prioritizing external connection"
    )

    return external_url


def get_api_token():
    if use_dummy_sage():
        return None

    return (
        os.getenv("SAGE_API_TOKEN")
        or os.getenv("API_TOKEN")
    )


def get_sage_config():
    api_url = get_api_url()
    api_token = get_api_token()

    if not api_url or not api_token:
        raise ValueError(
            "Missing SAGE_API_URL or SAGE_API_TOKEN "
            "in environment variables."
        )

    return api_url, api_token
