from itertools import chain
import json
import os
import socket
import requests
from datetime import date, datetime
from dotenv import load_dotenv
from collections import defaultdict

from database.butchers_lists import fetch_butchers_list_by_date
from database.products import fetch_products_stock_code_fresh
from models.butchers_list import ButchersList

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
        urls_to_try = [internal_url, external_url]
    else:
        print("Detected external network, prioritizing external connection")
        urls_to_try = [external_url, internal_url]
    
    # Try each URL in priority order
    for url in urls_to_try:
        if not url:
            continue
            
        try:
            print(f"Attempting to connect to {url}...")
            response = requests.get(f"{url}/api/searchInvoice", timeout=3)
            print(f"Successfully connected to {url} (status: {response.status_code})")
            return url
        except requests.RequestException as e:
            print(f"Failed to connect to {url} - {str(e)}")
    
    # If all attempts fail, log error and return the external URL as last resort
    print(f"All connection attempts failed. Defaulting to external URL: {external_url}")
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
        test_response = requests.head(test_endpoint, headers=headers, timeout=5)
        
        print(f"API endpoint test status: {test_response.status_code}")
        if test_response.status_code < 400:
            print("✓ API endpoint is accessible")
        else:
            print("✗ API endpoint returned an error status")
    except requests.RequestException as e:
        print(f"✗ API endpoint test failed: {str(e)}")


API_URL = get_api_url()
API_TOKEN = os.getenv("SAGE_API_TOKEN")


test_connection()

if not API_TOKEN:
    API_TOKEN = os.environ.get("API_TOKEN")

def get_invoice_products(date):
    """
    Main function to retrieve and process invoice products for a specific date.
    Creates a new butchers list row in the database instead of updating a JSON blob.
    """
    invoices = []
    invoice_list = []
    fresh_products_codes = fetch_products_stock_code_fresh()
    existing_butchers_list = fetch_butchers_list_by_date(date)
    processed_data = []
    
    # Get appropriate invoices based on whether we have an existing list
    if existing_butchers_list:
        previous_fetch = existing_butchers_list.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        invoice_list = get_todays_new_invoices(date, previous_fetch)
    else:
        invoice_list = get_todays_invoices(date)
    
    if invoice_list and 'results' in invoice_list and invoice_list['results']:
        for invoice in invoice_list['results']:
            if 'invoiceNumber' in invoice:
                current_invoice = get_invoice_by_id(invoice['invoiceNumber'])
                invoices.append(current_invoice)
        
        # Process invoices and create new butchers list
        processed_data = process_invoices_products(invoices, fresh_products_codes, invoice_list['results'])

    return processed_data

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
        response = requests.request(
            "POST", 
            url, 
            headers=headers, 
            data=payload,
            timeout=(30, 90)  # (connection timeout, read timeout)
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
        response = requests.request(
            "POST", 
            url, 
            headers=headers, 
            data=payload,
            timeout=(30, 90)  # (connection timeout, read timeout)
        )
        response.raise_for_status()  # Raise an error for non-2xx responses

        response.raise_for_status()  # Raise an error for non-2xx responses

        invoices = response.json()
        print(f"Fetch in controller completed successfully: {len(invoices['results'])}")
        return invoices

    except requests.RequestException as e:
        print(f"Error fetching invoices: {e}")
        return None

def get_invoice_by_id(invoice_id):
    """
    Fetch a specific invoice by its ID from the Sage API.
    """
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

def get_company_name_from_invoice_list(customer_act_ref, invoice_list):
    """
    Find the company name for a customer account reference in the invoice list.
    Returns the company name if found, otherwise an empty string.
    """
    for invoice in invoice_list:
        if invoice.get("accountRef", "").strip() == customer_act_ref:
            return invoice.get("name", "").strip()
    return ""

def check_product_is_fresh(stock_code, fresh_products_codes):
    """
    Check if a product is considered fresh based on its stock code.
    """
    flat_codes = list(chain.from_iterable(
        [item] if not isinstance(item, list) else item for item in fresh_products_codes
    ))
    return stock_code in flat_codes

def create_customer_lookup(butchers_list):
    """
    Build a lookup dictionary for existing customers.
    """
    customer_lookup = {}
    
    for customer in butchers_list:
        customer_key = customer.get("customer_act_ref") or customer.get("customer_name")
        customer_lookup[customer_key.strip()] = customer

        # Create a quick-access product map for merging
        customer["product_dict"] = {
            (prod["sage_code"], prod["product_name"]): float(prod["quantity"])
            for prod in customer.get("products", [])
        }
    
    return customer_lookup

def get_or_create_customer(key, customer_lookup, customer_name, customer_act_ref, invoice_id, new_customers):
    """
    Get an existing customer or create a new one if it doesn't exist.
    """
    if key in customer_lookup:
        customer_entry = customer_lookup[key]
        customer_entry["invoice_ids"].append(str(invoice_id))
    else:
        customer_entry = {
            "customer_name": customer_name,
            "customer_act_ref": customer_act_ref,
            "invoice_ids": [str(invoice_id)],
            "products": [],
            "product_dict": defaultdict(float)
        }
        customer_lookup[key] = customer_entry
        new_customers.append(customer_entry)
    
    return customer_entry

def process_invoice_items(invoice, customer_entry, fresh_products_codes):
    """
    Process items in an invoice and update customer's products.
    Special handling for CASH accounts: products are added individually rather than summed.
    """
    has_fresh_products = False
    customer_act_ref = customer_entry["customer_act_ref"]
    
    for item in invoice.get("invoiceItems", []):
        code = item.get("stockCode", "").strip()
        if check_product_is_fresh(code, fresh_products_codes):
            has_fresh_products = True
            name = item.get("description", "").strip()
            qty = float(item.get("quantity", 0))
            
            # Special handling for CASH accounts
            if customer_act_ref == "CASH":
                # For CASH accounts, add as a new product instead of summing quantities
                customer_entry["products"].append({
                    "sage_code": code,
                    "product_name": name,
                    "quantity": qty  # No rounding applied
                })
            else:
                # For regular accounts, aggregate quantities of the same product
                product_key = (code, name)
                customer_entry["product_dict"][product_key] += qty
    
    return has_fresh_products

def finalize_customer_products(butchers_list):
    """
    Finalize customer products by converting product_dict back to products list.
    Skip CASH accounts as their products are already directly added.
    """
    for customer in butchers_list:
        # Only process non-CASH accounts
        if customer.get("customer_act_ref") != "CASH":
            customer["products"] = [
                {
                    "sage_code": code,
                    "product_name": name,
                    "quantity": qty  # No rounding applied
                }
                for (code, name), qty in customer.get("product_dict", {}).items()
            ]
        
        # Clean up the temporary product_dict
        customer.pop("product_dict", None)

def process_invoices_products(invoices, fresh_products_codes=[], invoice_list=[]):
    """
    Process invoices and update the butchers list with products from invoices.
    Special handling for CASH accounts: products are added individually rather than summed.
    """

    butchers_list = []
    
    # Step 1: Build customer lookup
    customer_lookup = create_customer_lookup(butchers_list)
    
    # Step 2: Process new invoices
    customers_with_fresh_products = set()
    new_customers = []
    
    for invoice_data in invoices:
        invoice = invoice_data.get("response", {})
        customer_act_ref = invoice.get("customerAccountRef", "").strip()
        contact_name = invoice.get("contactName", "").strip()
        invoice_id = invoice.get("invoiceNumber")
        
        # Get company name from the invoice_list if available
        company_name = get_company_name_from_invoice_list(customer_act_ref, invoice_list)
        # Use company name as customer name if available, otherwise use contact name
        customer_name = company_name if company_name else contact_name

        key = customer_act_ref or customer_name or "Unknown Customer"
        
        # Get or create customer entry
        customer_entry = get_or_create_customer(
            key, customer_lookup, customer_name, customer_act_ref, invoice_id, new_customers
        )
        
        # Process invoice items
        has_fresh_products = process_invoice_items(invoice, customer_entry, fresh_products_codes)
        
        # Track customers who have fresh products
        if has_fresh_products:
            customers_with_fresh_products.add(key)

    # Only add new customers who have fresh products
    for customer in new_customers:
        customer_key = customer.get("customer_act_ref") or customer.get("customer_name")
        key = customer_key.strip()
        
        if key in customers_with_fresh_products:
            butchers_list.append(customer)

    # Step 3: Finalize products for all customers
    finalize_customer_products(butchers_list)

    return butchers_list
