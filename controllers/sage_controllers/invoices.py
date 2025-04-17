from itertools import chain
import json
import os
import requests
from datetime import date
from dotenv import load_dotenv
from collections import defaultdict

from database.butchers_lists import fetch_butchers_list_by_date
from database.products import fetch_products_stock_code_fresh

# Load environment variables from .env
load_dotenv()

API_URL = os.getenv("SAGE_API_URL")
API_TOKEN = os.getenv("SAGE_API_TOKEN")

def get_invoice_products(date):
    invoices = []
    fresh_products_codes = fetch_products_stock_code_fresh()
    invoice_list = get_todays_invoices(date)
    # print(f"Invoice fetch: {invoice_list}")
    butchers_list = fetch_butchers_list_by_date(date)
    
    for invoice in invoice_list['results']:
        # print(invoice)
        if 'invoiceNumber' in invoice:
            current_invoice = get_invoice_by_id(invoice['invoiceNumber'])
            invoices.append(current_invoice)

    # print(f"Invoices: {invoices}")
    processed_invoices = process_invoices_products(invoices, butchers_list, fresh_products_codes)
    
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



def process_invoices_products(invoices, butchers_list=None, fresh_products_codes=[]):
    if butchers_list is None:
        butchers_list = []
    
    # Step 1: Build a lookup for existing customers
    customer_lookup = {}
    for customer in butchers_list:
        customer_key = customer.get("customer_act_ref") or customer.get("customer_name")
        customer_lookup[customer_key.strip()] = customer

        # Create a quick-access product map for merging
        customer["product_dict"] = {
            (prod["sage_code"], prod["product_name"]): float(prod["quantity"])
            for prod in customer.get("products", [])
        }

    # Step 2: Process new invoices with tracking of customers with fresh products
    customers_with_fresh_products = set()
    new_customers = []
    
    for invoice_data in invoices:
        invoice = invoice_data.get("response", {})
        customer_act_ref = invoice.get("customerAccountRef", "").strip()
        customer_name = invoice.get("contactName", "").strip()
        invoice_id = invoice.get("invoiceNumber")

        key = customer_act_ref or customer_name or "Unknown Customer"
        has_fresh_products = False

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

        # Add/update products
        for item in invoice.get("invoiceItems", []):
            code = item.get("stockCode", "").strip()
            if check_product_is_fresh(code, fresh_products_codes):
                has_fresh_products = True
                name = item.get("description", "").strip()
                qty = float(item.get("quantity", 0))

                product_key = (code, name)
                customer_entry["product_dict"][product_key] += qty
        
        # Track customers who have fresh products
        if has_fresh_products:
            customers_with_fresh_products.add(key)

    # Only add new customers who have fresh products
    for customer in new_customers:
        customer_key = customer.get("customer_act_ref") or customer.get("customer_name")
        key = customer_key.strip()
        
        if key in customers_with_fresh_products:
            butchers_list.append(customer)

    # Step 3: Reconstruct the product list
    for customer in butchers_list:
        customer["products"] = [
            {
                "sage_code": code,
                "product_name": name,
                "quantity": round(qty, 2)
            }
            for (code, name), qty in customer.get("product_dict", {}).items()
        ]
        customer.pop("product_dict", None)

    return butchers_list

def check_product_is_fresh(stock_code, fresh_products_codes):
    # print(f'Check product code:{stock_code}')
    # print(f'Check product is fresh: {stock_code in fresh_products_codes}')
    flat_codes = list(chain.from_iterable(
        [item] if not isinstance(item, list) else item for item in fresh_products_codes
    ))
    return stock_code in flat_codes
