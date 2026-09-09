import json
import os
import socket
import requests

def get_todays_invoices(date):
    """
    Fetch all invoices for a specific date from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    url = f"{API_URL}/api/searchInvoice"

    payload = json.dumps([
      {
        "field": "INVOICE_DATE",
        "type": "eq",
        "value": date
      }
    ])
    headers = {
      'Content-Type': 'application/json',
      'AuthToken': API_TOKEN
    }

    try:
        # Increase timeout values (in seconds)
        if is_internal_network():
          response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
              verify=False
          )
        else:
            response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
          )
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None
    

def get_todays_new_invoices(date, previous_fetch):
    """
    Fetch all invoices for a specific date from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    url = f"{API_URL}/api/searchInvoice"

    payload = json.dumps([
      {
        "field": "INVOICE_DATE",
        "type": "eq",
        "value": date
      },
      {
        "field": "RECORD_CREATE_DATE",
        "type": "gt",
        "value": previous_fetch
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
              timeout=(30, 90),  # (connection timeout, read timeout)
              verify=False
          )
        else:
            response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
          )
        response.raise_for_status()  # Raise an error for non-2xx responses

        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None
    
def get_customer_invoices_by_month(customer_code, start_month, end_month):
    """
    Fetch all invoices for a specific date from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    url = f"{API_URL}/api/searchInvoice"

    payload = json.dumps([
      {
        "field": "ACCOUNT_REF",
        "type": "eq",
        "value": customer_code
      },
      {
        "field": "INVOICE_DATE",
        "type": "gte",
        "value": start_month
      },
      {
        "field": "INVOICE_DATE",
        "type": "lt",
        "value": end_month
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
              timeout=(30, 90),  # (connection timeout, read timeout)
              verify=False
          )
        else:
            response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
          )
        response.raise_for_status()  # Raise an error for non-2xx responses

        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None
    
def refresh_get_todays_invoices(date, original_fetch, previous_fetch):
    """
    Fetch all invoices for a specific date from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    url = f"{API_URL}/api/searchInvoice"

    if previous_fetch:
        payload = json.dumps([
          {
            "field": "INVOICE_DATE",
            "type": "eq",
            "value": date
          },
          {
            "field": "RECORD_CREATE_DATE",
            "type": "lte",
            "value": original_fetch
          },
          {
            "field": "RECORD_CREATE_DATE",
            "type": "gte",
            "value": previous_fetch
          }
        ])
    else:
        payload = json.dumps([
          {
            "field": "INVOICE_DATE",
            "type": "eq",
            "value": date
          },
          {
            "field": "RECORD_CREATE_DATE",
            "type": "lte",
            "value": original_fetch
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
              timeout=(30, 90),  # (connection timeout, read timeout)
              verify=False
          )
        else:
            response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
          )
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None
    
def get_the_last_weeks_invoices(date, date_week_ago):
    """
    Fetch all invoices for a specific date from the Sage API.
    """
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    url = f"{API_URL}/api/searchInvoice"

    payload = json.dumps([
      {
        "field": "INVOICE_DATE",
        "type": "lte",
        "value": date
      },
      {
        "field": "INVOICE_DATE",
        "type": "gte",
        "value": date_week_ago
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
              timeout=(30, 90),  # (connection timeout, read timeout)
              verify=False
          )
        else:
            response = requests.request(
              "POST", 
              url, 
              headers=headers, 
              data=payload,
              timeout=(30, 90),  # (connection timeout, read timeout)
          )
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices['results']

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None
    



