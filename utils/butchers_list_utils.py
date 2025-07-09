from itertools import chain
from collections import defaultdict
import json

from controllers.sage_controllers.invoice_products import get_invoice_items_id
from controllers.sage_controllers.invoices import get_todays_invoices, get_todays_new_invoices, refresh_get_todays_invoices
from database.butchers_lists import fetch_all_butchers_lists_by_date, fetch_butchers_list_by_date
from database.products import fetch_products_stock_code_fresh

def get_invoice_products(date):
    """
    Main function to retrieve and process invoice products for a specific date.
    Creates a new butchers list row in the database instead of updating a JSON blob.
    """
    invoices_ids = []
    
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
                invoices_ids.append(invoice['invoiceNumber'])
        
        # Process invoices and create new butchers list
        invoice_items = get_invoice_items_id(invoices_ids)

        processed_data = process_invoices_products(invoice_items, fresh_products_codes, invoice_list['results'])

    return processed_data, "Not sure what to put here"

def refresh_get_invoice_products(date, list_number):
    """
    Main function to refresh and process invoice products for a specific date.
    Creates a new butchers list row in the database instead of updating a JSON blob.
    """
    invoices_ids = []
    
    invoice_list = []
    fresh_products_codes = fetch_products_stock_code_fresh()
    existing_butchers_lists = fetch_all_butchers_lists_by_date(date)
    processed_data = []
    
    original_fetch = existing_butchers_lists[list_number].updated_at.strftime("%Y-%m-%d %H:%M:%S")

    if list_number == 0:
        previous_fetch = ""
    else:
        previous_fetch = existing_butchers_lists[(list_number - 1)].updated_at.strftime("%Y-%m-%d %H:%M:%S")

    invoice_list = refresh_get_todays_invoices(date, original_fetch, previous_fetch)    

    if invoice_list and 'results' in invoice_list and invoice_list['results']:
        for invoice in invoice_list['results']:
            if 'invoiceNumber' in invoice:
                invoices_ids.append(invoice['invoiceNumber'])
        
        invoice_items = get_invoice_items_id(invoices_ids)
        processed_data = process_invoices_products(invoice_items, fresh_products_codes, invoice_list['results'])
    return processed_data, existing_butchers_lists[list_number].id

def check_product_is_fresh(stock_code, fresh_products_codes):
    """
    Check if a product is considered fresh based on its stock code.
    """
    
    for fresh_code in fresh_products_codes:
        try:
            # Try to parse as JSON first
            parsed_codes = json.loads(fresh_code)
            if isinstance(parsed_codes, str):
                # JSON string value
                if parsed_codes == stock_code:

                    return True
            elif isinstance(parsed_codes, list):
                # JSON array
                if stock_code in parsed_codes:
                    return True
                    
        except (json.JSONDecodeError, TypeError):
            # If JSON parsing fails, treat as plain string
            if isinstance(fresh_code, str) and fresh_code == stock_code:
                return True
    
    return False

def create_customer_lookup(butchers_list):
    """
    Build a lookup dictionary for existing customers based on customer name only.
    """
    customer_lookup = {}
    
    for customer in butchers_list:
        customer_key = customer.get("customer_name", "").strip()
        customer_lookup[customer_key] = customer

        # Create a quick-access product map for merging
        customer["product_dict"] = {
            (prod["sage_code"], prod["product_name"]): float(prod["quantity"])
            for prod in customer.get("products", [])
        }
    
    return customer_lookup

def get_or_create_customer(customer_name, customer_lookup, invoice_id, new_customers):
    """
    Get an existing customer or create a new one if it doesn't exist, using only customer name.
    """
    customer_key = customer_name.strip()
    
    if customer_key in customer_lookup:
        customer_entry = customer_lookup[customer_key]
        # Avoid duplicate invoice IDs
        if str(invoice_id) not in customer_entry["invoice_ids"]:
            customer_entry["invoice_ids"].append(str(invoice_id))
    else:
        customer_entry = {
            "customer_name": customer_name,
            "invoice_ids": [str(invoice_id)],
            "products": [],
            "product_dict": defaultdict(float)
        }
        customer_lookup[customer_key] = customer_entry
        new_customers.append(customer_entry)
    
    return customer_entry

def process_invoice_items(invoice_products, customer_entry, fresh_products_codes):
    """
    Process items in an invoice and update customer's products.
    All products are aggregated by their stock code and name.
    """
    has_fresh_products = False
    
    if not invoice_products:
        return has_fresh_products
    
    # Convert invoice_ids to strings for comparison
    invoice_ids_as_strings = [str(inv_id) for inv_id in customer_entry["invoice_ids"]]
    
    # Process each item once, checking if it belongs to any of this customer's invoices
    for item in invoice_products:
        product_invoice_number = item.get("invoiceNumber")
        if product_invoice_number is not None:
            product_invoice_number = str(product_invoice_number)
        else:
            product_invoice_number = ""
        
        # Check if this item belongs to any of this customer's invoices
        if product_invoice_number in invoice_ids_as_strings:
            code = item.get("stockCode", "")
            if code is not None:
                code = str(code).strip()
            else:
                code = ""
                
            if check_product_is_fresh(code, fresh_products_codes):
                has_fresh_products = True
                
                name = item.get("description", "")
                if name is not None:
                    name = str(name).strip()
                else:
                    name = ""
                    
                qty = float(item.get("quantity", 0))
                
                # Aggregate quantities
                product_key = (code, name)
                customer_entry["product_dict"][product_key] += qty
    
    return has_fresh_products

def finalize_customer_products(butchers_list):
    """
    Finalize customer products by converting product_dict back to products list.
    """
    for customer in butchers_list:
        customer["products"] = [
            {
                "sage_code": code,
                "product_name": name,
                "quantity": qty
            }
            for (code, name), qty in customer.get("product_dict", {}).items()
        ]
        
        # Clean up the temporary product_dict
        customer.pop("product_dict", None)

def process_invoices_products(invoices_items, fresh_products_codes=[], invoice_list=[]):
    """
    Process invoices and update the butchers list with products from invoices,
    identifying customers by name only.
    """
    butchers_list = []
    
    # Step 1: Build customer lookup
    customer_lookup = create_customer_lookup(butchers_list)
    
    # Step 2: Process new invoices
    customers_with_fresh_products = set()
    new_customers = []
    
    for invoice in invoice_list:
        # Get company name from the invoice
        company_name = invoice.get("name", "").strip()
        contact_name = invoice.get("contactName", "").strip()
        invoice_id = invoice.get("invoiceNumber")
        
        # Use company name as customer name if available, otherwise use contact name
        customer_name = company_name or contact_name or "Unknown Customer"
        
        # Get or create customer entry based only on name
        customer_entry = get_or_create_customer(
            customer_name, customer_lookup, invoice_id, new_customers
        )
        
        # Process invoice items
        has_fresh_products = process_invoice_items(invoices_items, customer_entry, fresh_products_codes)
        
        # Track customers who have fresh products
        if has_fresh_products:
            customers_with_fresh_products.add(customer_name.strip())

    # Only add new customers who have fresh products
    for customer in new_customers:
        customer_key = customer.get("customer_name", "").strip()
        
        if customer_key in customers_with_fresh_products:
            butchers_list.append(customer)

    # Step 3: Finalize products for all customers
    finalize_customer_products(butchers_list)

    return butchers_list
