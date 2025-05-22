import json
from controllers.sage_controllers.invoice_products import get_invoice_items_id
from controllers.sage_controllers.invoices import get_todays_invoices
from database.reports import update_report


def add_product_stock_sold_report(report, product_id): 
      if product_id is not None:
          # Check if report has products already
          if report.products:
              try:
                  # Try to parse existing product_ids as JSON if it's a string
                  if isinstance(report.products, str):
                      
                      current_product_ids = json.loads(report.products)
                  else:
                      # Otherwise, assume it's already a list
                      current_product_ids = report.products
                  
                  # Make sure current_product_ids is a list
                  if not isinstance(current_product_ids, list):
                      current_product_ids = [current_product_ids]
                  
                  # Add the new product ID if it's not already in the list
                  if product_id not in current_product_ids:
                      current_product_ids.append(product_id)
                  else:
                      return "Add failed", "Error: Product already added"
              except Exception as e:
                  # If there was a problem parsing the existing product_ids
                  print(f"Error processing existing product IDs: {e}")
                  current_product_ids = [product_id]  # Start fresh with just the new ID
          else:
              # No existing products, create a new array with the selected product ID
              current_product_ids = [product_id]
          
          # Update the report with the new product_ids array
          
          state = update_report(current_product_ids, report.id)
          if state: 
              return "Added successfully", "Product now in report"
          else:
              return "Error", "Adding product failed"
      else:
        # Add this return statement for when product_id is None (user canceled)
        return "Canceled", "No product selected"
        

def remove_product_stock_sold_report(report, product_id):
    if product_id is not None:
        # Check if report has products already
        if report.products:
            try:
                # Try to parse existing product_ids as JSON if it's a string
                if isinstance(report.products, str):
                    current_product_ids = json.loads(report.products)
                else:
                    # Otherwise, assume it's already a list
                    current_product_ids = report.products
                
                # Make sure current_product_ids is a list
                if not isinstance(current_product_ids, list):
                    current_product_ids = [current_product_ids]
                
                # Remove the product ID if it exists in the list
                if product_id in current_product_ids:
                    current_product_ids.remove(product_id)
                else:
                    return "Remove failed", "Error: Product not found in report"
            except Exception as e:
                # If there was a problem parsing the existing product_ids
                print(f"Error processing existing product IDs: {e}")
                return "Remove failed", "Error: Could not process product list"
        else:
            # No existing products, nothing to remove
            return "Remove failed", "Error: No products in report to remove"
        
        # Update the report with the modified product_ids array
        state = update_report(current_product_ids, report.id)
        if state: 
            return "Removed successfully", "Product removed from report"
        else:
            return "Error", "Removing product failed"
    else:
        # Add this return statement for when product_id is None (user canceled)
        return "Canceled", "No product selected"
    

def create_sage_codes_array(products):
    all_codes = []
    
    for product in products:
        sage_code = product.sage_code
        
        if sage_code:  # Check if sage_code is not None or empty
            if isinstance(sage_code, str):
                try:
                    # Try to parse as JSON array first
                    parsed_codes = json.loads(sage_code)
                    if isinstance(parsed_codes, list):
                        all_codes.extend(parsed_codes)
                    else:
                        # If it's not a list after parsing, treat as single code
                        all_codes.append(str(parsed_codes))
                except json.JSONDecodeError:
                    # If JSON parsing fails, treat as single code
                    all_codes.append(sage_code)
            elif isinstance(sage_code, list):
                # If it's already a list, extend directly
                all_codes.extend(sage_code)
            else:
                # For any other type, convert to string and add
                all_codes.append(str(sage_code))
    
    # Remove duplicates while preserving order
    unique_codes = []
    seen = set()
    for code in all_codes:
        if code not in seen:
            unique_codes.append(code)
            seen.add(code)
    
    return unique_codes

def fetch_chosen_dates_invoice_items(date, report_products):
    invoices_ids = []
    
    invoice_list = []
    processed_data = []
    
    # Get appropriate invoices based on whether we have an existing list
    invoice_list = get_todays_invoices(date)
    
    if invoice_list and 'results' in invoice_list and invoice_list['results']:
        for invoice in invoice_list['results']:
            if 'invoiceNumber' in invoice:
                invoices_ids.append(invoice['invoiceNumber'])
        
        # Process invoices and create new butchers list
        invoice_items = get_invoice_items_id(invoices_ids)

        processed_data = process_invoices_products(invoice_items['results'], report_products, invoices_ids)

    return processed_data, "Not sure what to put here"


def process_invoices_products(invoice_items, report_products, invoices_ids):
    product_sold_count = {}
    selected_dates_invoice_items = process_invoice_items(invoice_items, invoices_ids)
    
    for product in report_products:
        product_sold_count[product.name] = 0
        
        # Parse sage codes for this product
        try:
            sage_codes = json.loads(product.sage_code)
        except json.JSONDecodeError:
            sage_codes = [product.sage_code]
        
        for invoice_item in selected_dates_invoice_items:
            if invoice_item['stockCode'] in sage_codes:
                product_sold_count[product.name] += invoice_item['quantity']

    return product_sold_count


def process_invoice_items(invoice_items, invoices_ids):
    selected_dates_invoice_items = []
    
    # Convert invoices_ids to handle both string and integer types
    try:
        invoices_ids_int = [int(id) for id in invoices_ids]
        invoices_ids_str = [str(id) for id in invoices_ids_int]
    except (ValueError, TypeError):
        invoices_ids_int = invoices_ids
        invoices_ids_str = [str(id) for id in invoices_ids]

    for invoice_item in invoice_items:
        invoice_num = invoice_item['invoiceNumber']
        if invoice_num in invoices_ids_int or invoice_num in invoices_ids_str:
            selected_dates_invoice_items.append(invoice_item)

    return selected_dates_invoice_items
