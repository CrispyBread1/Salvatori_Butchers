from itertools import chain
from collections import defaultdict

from controllers.sage_controllers.invoices import get_invoice_items_id, get_todays_invoices, get_todays_new_invoices
from database.butchers_lists import fetch_butchers_list_by_date
from database.products import fetch_products_stock_code_fresh

def get_invoice_products(date):
    """
    Main function to retrieve and process invoice products for a specific date.
    Creates a new butchers list row in the database instead of updating a JSON blob.
    """
    invoices = []
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
                # current_invoice = get_invoice_by_id(invoice['invoiceNumber'])
                # invoices.append(current_invoice)
        
        # Process invoices and create new butchers list
        # print(invoices_ids)
        invoice_items = get_invoice_items_id(invoices_ids)

        # print(invoice_items)
        processed_data = process_invoices_products(invoice_items['results'], fresh_products_codes, invoice_list['results'])

    return processed_data

def get_company_name_from_invoice_list(customer_act_ref, invoice_list):
    """
    Find the company name for a customer account reference in the invoice list.
    Returns the company name if found, otherwise an empty string.
    """
    for invoice in invoice_list:
        # Debug output to see what's happening
        # print(f"Comparing {invoice.get('accountRef', '')} with {customer_act_ref}")
        
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

def process_invoice_items(invoice_products, customer_entry, fresh_products_codes):
    """
    Process items in an invoice and update customer's products.
    Special handling for CASH accounts: products are added individually rather than summed.
    """
    has_fresh_products = False
    customer_act_ref = customer_entry["customer_act_ref"]
    
    # Safety check - ensure invoice_products is iterable
    if not invoice_products:
        return has_fresh_products
    
    # Convert invoice_ids to strings for comparison
    invoice_ids_as_strings = [str(inv_id) for inv_id in customer_entry["invoice_ids"]]
    
    for item in invoice_products:
        # Get invoice number to match with our invoice list
        # Handle the case where invoiceNumber might be an integer
        invoice_number = item.get("invoiceNumber")
        if invoice_number is not None:
            invoice_number = str(invoice_number)  # Convert to string to ensure comparison works
        else:
            invoice_number = ""
        
        # Check if this item belongs to one of our target invoices
        if invoice_number in invoice_ids_as_strings:
            code = item.get("stockCode", "")
            # Handle case where stockCode might be None or an integer
            if code is not None:
                code = str(code).strip()
            else:
                code = ""
                
            if check_product_is_fresh(code, fresh_products_codes):
                has_fresh_products = True
                
                # Handle case where description might be None or an integer
                name = item.get("description", "")
                if name is not None:
                    name = str(name).strip()
                else:
                    name = ""
                    
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

def process_invoices_products(invoices_items, fresh_products_codes=[], invoice_list=[]):
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
    
    for invoice in invoice_list:
        # Make sure we're getting the right field for customer_act_ref
        customer_act_ref = invoice.get("accountRef", "").strip()  # Changed from customerAccountRef to accountRef
        contact_name = invoice.get("contactName", "").strip()
        invoice_id = invoice.get("invoiceNumber")
        
        # Get company name from the invoice_list if available
        company_name = invoice.get("name", "").strip()  # Get name directly from current invoice
        # print(f"For customer {customer_act_ref}, found company name: {company_name}")
        
        # Use company name as customer name if available, otherwise use contact name
        customer_name = company_name or contact_name or "Unknown Customer"

        key = customer_act_ref or customer_name
        
        # Get or create customer entry
        customer_entry = get_or_create_customer(
            key, customer_lookup, customer_name, customer_act_ref, invoice_id, new_customers
        )
        
        # Process invoice items
        has_fresh_products = process_invoice_items(invoices_items, customer_entry, fresh_products_codes)
        
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
