import json
import os
import socket
import requests

def get_invoice_items_id(invoices_ids):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")
    
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
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoice_items = response.json()
        print(f"Fetch in controller completed successfully: {len(invoice_items['results'])}")
        return invoice_items['results']

    except requests.RequestException as e:
        print(f"Error fetching invoice items: {e}")
        return None


def get_invoice_items_date_sage_code(date, product_sage_codes):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")
    
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
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoice_items = response.json()
        print(f"Fetch in controller completed successfully: {len(invoice_items['results'])}")
        return invoice_items['results']

    except requests.RequestException as e:
        print(f"Error fetching invoice items: {e}")
        return None

def get_invoice_items_between_time_frame(date, previous_week_date):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")
    
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
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoice_items = response.json()
        print(f"Fetch in controller completed successfully: {len(invoice_items['results'])}")
        return invoice_items['results']

    except requests.RequestException as e:
        print(f"Error fetching invoice items: {e}")
        return None
