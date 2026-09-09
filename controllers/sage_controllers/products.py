from itertools import chain

import json

import requests

from datetime import date, datetime

from collections import defaultdict

from database.butchers_lists import fetch_butchers_list_by_date

from database.products import fetch_products_stock_code_fresh

from models.butchers_list import ButchersList

from resources.sage_connection import (
    get_sage_config,
    is_internal_network,
    use_dummy_sage,
)

from sage_controllers.dummy_data.products import DUMMY_PRODUCTS


def get_product_by_code(sage_code):
    """
    Fetch a specific product from Sage.

    Development/test:
        Returns dummy Sage product data.

    Production:
        Calls the real Sage API.
    """

    if use_dummy_sage():

        for product in DUMMY_PRODUCTS:

            if product["STOCK_CODE"] == sage_code:

                return product

        return None

    api_url, api_token = get_sage_config()

    url = f"{api_url}/api/product/{sage_code}"

    headers = {
        "Content-Type": "application/json",
        "AuthToken": api_token,
    }

    try:

        if is_internal_network():

            response = requests.get(
                url,
                headers=headers,
                verify=False,
                timeout=10,
            )

        else:

            response = requests.get(
                url,
                headers=headers,
                timeout=10,
            )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:

        print(f"Error fetching Sage product: {e}")

        return None


def get_products_by_codes(sage_codes):
    """
    Fetch multiple products from Sage using Sage stock codes.

    Development/test:
        Returns matching dummy Sage products.

    Production:
        Calls the real Sage API.
    """

    if use_dummy_sage():

        return [
            product
            for product in DUMMY_PRODUCTS
            if product["STOCK_CODE"] in sage_codes
        ]

    api_url, api_token = get_sage_config()

    url = f"{api_url}/api/searchProduct"

    payload = json.dumps([
        {
            "field": "STOCK_CODE",
            "type": "in",
            "value": sage_codes,
        }
    ])

    headers = {
        "Content-Type": "application/json",
        "AuthToken": api_token,
    }

    try:

        if is_internal_network():

            response = requests.post(
                url,
                headers=headers,
                data=payload,
                verify=False,
                timeout=10,
            )

        else:

            response = requests.post(
                url,
                headers=headers,
                data=payload,
                timeout=10,
            )

        response.raise_for_status()

        products = response.json()

        return products["results"]

    except requests.RequestException as e:

        print(f"Error fetching Sage products: {e}")

        return None
