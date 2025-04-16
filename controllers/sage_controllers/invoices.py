import json
import os
import requests
from datetime import date
from dotenv import load_dotenv

from database.butchers_lists import fetch_butchers_list_by_date

# Load environment variables from .env
load_dotenv()

API_URL = os.getenv("SAGE_API_URL")
API_TOKEN = os.getenv("SAGE_API_TOKEN")

def get_invoice_products(date):
    invoices = []
    invoice_list = get_todays_invoices(date)
    butchers_list = fetch_butchers_list_by_date(date)

    for invoice in invoice_list['results']:
        if 'invoiceNumber' in invoice:
            current_invoice = get_invoice_by_id(invoice['invoiceNumber'])
            invoices.append(current_invoice)

    processed_invoices = process_invoices_products(invoice_list, butchers_list)
    
    return processed_invoices



def get_todays_invoices(date):
    # Load API credentials from environment

    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")

    # Get today's date in ISO format (YYYY-MM-DD)
   

    # Set up request headers and URL

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
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None



def get_invoice_by_id(invoice_id):
    if not API_URL or not API_TOKEN:
        raise ValueError("Missing SAGE_API_URL or SAGE_API_TOKEN in environment variables.")
    
    url = f"{API_URL}/api/salesInvoice/{invoice_id}"

    payload = ""
    headers = {
      'Content-Type': 'application/json',
      'AuthToken': API_TOKEN
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for non-2xx responses

        invoice = response.json()
        return invoice

    except requests.RequestException as e:
        print(f"Error fetching invoice: {e}")
        return None

def process_invoices_products(invoices, butchers_list):
    pass
