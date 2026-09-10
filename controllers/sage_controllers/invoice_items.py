import json

import requests

from controllers.sage_controllers.resources.sage_connection import (
    get_sage_config,
    is_internal_network,
    use_dummy_sage,
)

from controllers.sage_controllers.dummy_data.invoice_items import DUMMY_INVOICE_ITEMS


def get_invoice_items_id(invoices_ids):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """

    if use_dummy_sage():
        return DUMMY_INVOICE_ITEMS['results']

    API_URL, API_TOKEN = get_sage_config()

    url = f"{API_URL}/api/searchInvoiceItem/"

    payload = json.dumps([
        {
            "field": "INVOICE_NUMBER",
            "type": "in",
            "value": invoices_ids
        }
    ])

    headers = {
        'Content-Type': 'application/json',
        'AuthToken': API_TOKEN
    }

    try:

        if is_internal_network():

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                verify=False
            )

        else:

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload
            )

        response.raise_for_status()

        invoice_items = response.json()

        print(
            f"Fetch in controller completed successfully: "
            f"{len(invoice_items['results'])}"
        )

        return invoice_items['results']

    except requests.RequestException as e:

        print(f"Error fetching invoice items: {e}")

        return None


def get_invoice_items_date_sage_code(date, product_sage_codes):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """

    if use_dummy_sage():
        return DUMMY_INVOICE_ITEMS['results']

    API_URL, API_TOKEN = get_sage_config()

    url = f"{API_URL}/api/searchInvoiceItem/"

    payload = json.dumps([
        {
            "field": "RECORD_CREATE_DATE",
            "type": "eq",
            "value": date
        },
        {
            "field": "STOCK_CODE",
            "type": "in",
            "value": product_sage_codes
        }
    ])

    headers = {
        'Content-Type': 'application/json',
        'AuthToken': API_TOKEN
    }

    try:

        if is_internal_network():

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                verify=False
            )

        else:

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload
            )

        response.raise_for_status()

        invoice_items = response.json()

        print(
            f"Fetch in controller completed successfully: "
            f"{len(invoice_items['results'])}"
        )

        return invoice_items['results']

    except requests.RequestException as e:

        print(f"Error fetching invoice items: {e}")

        return None


def get_invoice_items_between_time_frame(date, previous_week_date):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """

    if use_dummy_sage():
        return DUMMY_INVOICE_ITEMS['results']

    API_URL, API_TOKEN = get_sage_config()

    url = f"{API_URL}/api/searchInvoiceItem/"

    payload = json.dumps([
        {
            "field": "RECORD_CREATE_DATE",
            "type": "lte",
            "value": date
        },
        {
            "field": "STOCK_CODE",
            "type": "gte",
            "value": previous_week_date
        }
    ])

    headers = {
        'Content-Type': 'application/json',
        'AuthToken': API_TOKEN
    }

    try:

        if is_internal_network():

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                verify=False
            )

        else:

            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload
            )

        response.raise_for_status()

        invoice_items = response.json()

        print(
            f"Fetch in controller completed successfully: "
            f"{len(invoice_items['results'])}"
        )

        return invoice_items['results']

    except requests.RequestException as e:

        print(f"Error fetching invoice items: {e}")

        return None
