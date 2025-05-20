import json
import os
import socket
import requests
import urllib3  # Add this import
from dotenv import load_dotenv

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env
load_dotenv()

def is_internal_network():
    """
    Check if we're likely running on the internal network by testing if we can
    resolve the internal hostname quickly.
    """
    try:
        # Try to resolve the internal server hostname with a short timeout
        socket.getaddrinfo('server69.cw-direct.co.uk', 50027)
        return True
    except (socket.gaierror, socket.timeout):
        return False
    finally:
        # Reset socket timeout to default
        socket.setdefaulttimeout(None)


def get_api_url():
    """
    Function to get the API URL with fallback support.
    Detects whether we're on internal or external network to choose 
    the appropriate connection route.
    """
    # Get configured URLs from environment
    internal_url = os.getenv("SAGE_API_URL_INTERNAL") or os.environ.get("SAGE_API_URL_INTERNAL")
    external_url = os.getenv("SAGE_API_URL") or os.environ.get("SAGE_API_URL")
    
    # Define direct internal server connection as backup option
    # direct_internal = "https://10.0.0.69:50027"  # Direct IP to SERVER69
    
    # If we're likely on the internal network, prioritize internal connections
    if is_internal_network():
        print("Detected internal network, prioritizing direct internal connection")
        return internal_url
    else:
        print("Detected external network, prioritizing external connection")
        return external_url


def test_connection():
    url = get_api_url()
    print(f"\nFinal selected API URL: {url}")
    
    # Optional: Try making a basic API request with the selected URL
    # This helps verify the URL works beyond just being reachable
    try:
        test_endpoint = f"{url}/api/searchInvoice"  # Using an endpoint we know exists
        print(f"\nTesting API endpoint: {test_endpoint}")
        
        # Only send a HEAD request to avoid unnecessary data transfer
        headers = {
            'Content-Type': 'application/json',
            'AuthToken': os.getenv("SAGE_API_TOKEN") or os.environ.get("SAGE_API_TOKEN") or "test-token"
        }
        test_response = requests.head(test_endpoint, headers=headers, timeout=5, verify=False)
        
        print(f"API endpoint test status: {test_response.status_code}")
        if test_response.status_code < 400:
            print("✓ API endpoint is accessible")
        else:
            print("✗ API endpoint returned an error status")
    except requests.RequestException as e:
        print(f"✗ API endpoint test failed: {str(e)}")


API_URL = get_api_url()
API_TOKEN = os.getenv("SAGE_API_TOKEN")


if not API_TOKEN:
    API_TOKEN = os.environ.get("API_TOKEN")


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
        return invoice_items

    except requests.RequestException as e:
        print(f"Error fetching invoice items: {e}")
        return None

