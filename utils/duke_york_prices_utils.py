import calendar
import json
from controllers.sage_controllers.invoice_items import get_invoice_items_id
from controllers.sage_controllers.invoices import get_customer_invoices_by_month
from database.duke_york_prices import fetch_duke_york_prices_by_date_range
from database.reports import fetch_report_by_id

def get_duke_york_prices_complete(date):
    start_month = date.replace(day=1).strftime("%Y-%m-%d %H:%M:%S")
    last_day = calendar.monthrange(date.year, date.month)[1]
    end_month = date.replace(day=last_day).strftime("%Y-%m-%d %H:%M:%S")
    return fetch_duke_york_prices_by_date_range(start_month, end_month)

def get_duke_york_prices(date, report, on_pause=None):
  duke_york_customer_sage_code = report.customers

  start_month = date.replace(day=1).strftime("%Y-%m-%d")
  last_day = calendar.monthrange(date.year, date.month)[1]
  end_month = date.replace(day=last_day).strftime("%Y-%m-%d %H:%M:%S")

  invoice_list = get_customer_invoices_by_month(duke_york_customer_sage_code, start_month, end_month)['results']

  invoices_ids = []

  
  if invoice_list:
    for invoice in invoice_list:
        if 'invoiceNumber' in invoice:
            invoices_ids.append(invoice['invoiceNumber'])
          
    invoice_items = get_invoice_items_id(invoices_ids)

    processed_data = process_duke_york_prices(invoice_list, invoice_items, report)
    
    # Validate and clean the processed data
    validated_data = validate_invoice_totals(processed_data, invoice_list)

    return validated_data
  

def process_duke_york_prices(invoice_list, invoice_items, report):
  # [{invoice_number: '', invoice_date: '', product_description: '', product_sage_code: '', cost_price: '', exact_price: ''},],

  processed_data = []

  for invoice in invoice_list:
    invoice_number = invoice.get("invoiceNumber")
    
    
    for invoice_item in invoice_items:
      invoice_item_number = invoice_item.get("invoiceNumber")
      invoice_item_sage_code = invoice_item.get("stockCode")

      # Skip items with sage code 'M'
      if invoice_item_sage_code == 'M':
        continue

      if (str(invoice_number) == str(invoice_item_number)):
        invoice_item_cost = invoice_item.get("netAmount")

        processed_invoice_item_data = {
          'invoice_number': invoice_item_number, 
          'invoice_date': invoice.get("invoiceDate"), 
          'product_description': invoice_item.get("description"), 
          'product_sage_code': invoice_item_sage_code, 
          'cost_price': invoice_item_cost, 
          'exact_price': get_exact_item_price(invoice_item_sage_code, invoice_item_cost, report)
         }
        
        processed_data.append(processed_invoice_item_data)

      # elif (str(invoice_number) == str(invoice_item_number)) and (len(invoice_number) == 7 ):

  return processed_data

def get_exact_item_price(invoice_item_sage_code, invoice_item_cost, report):
  duke_york_product_sage_codes = report.products
  percentages = json.loads(report.description)
  duke_york_column1_percentage = percentages["column1"]
  duke_york_column2_percentage = percentages["column2"]

  if invoice_item_sage_code in duke_york_product_sage_codes:
    difference = (duke_york_column1_percentage / 100) * invoice_item_cost
    return invoice_item_cost - difference
  
  else:
    difference = (duke_york_column2_percentage / 100) * invoice_item_cost
    return invoice_item_cost - difference

# ============================================================================
# NEW VALIDATION FUNCTIONS
# ============================================================================

def validate_invoice_totals(processed_data, invoice_list):
    """
    Validate that invoice items match the actual invoice totals.
    Removes deleted items that don't belong to the invoice anymore.
    
    Args:
        processed_data: List of processed invoice items
        invoice_list: List of actual invoices from Sage
        
    Returns:
        List of validated invoice items with deleted items removed
    """
    # Create a lookup for invoice totals using invoiceNet field
    invoice_totals = {}
    for invoice in invoice_list:
        invoice_number = str(invoice.get("invoiceNumber"))
        invoice_totals[invoice_number] = invoice.get("invoiceNet", 0)
    
    # Group processed items by invoice number
    items_by_invoice = {}
    for item in processed_data:
        invoice_num = str(item.get("invoice_number"))
        if invoice_num not in items_by_invoice:
            items_by_invoice[invoice_num] = []
        items_by_invoice[invoice_num].append(item)
    
    # Validate each invoice
    validated_data = []
    for invoice_num, items in items_by_invoice.items():
        expected_total = invoice_totals.get(invoice_num, 0)
        corrected_items = correct_invoice_items(items, expected_total, invoice_num)
        validated_data.extend(corrected_items)
    
    return validated_data


def correct_invoice_items(items, expected_total, invoice_number):
    """
    Remove deleted items from an invoice to match the expected total.
    
    Args:
        items: List of items for a single invoice
        expected_total: The actual total from Sage
        invoice_number: The invoice number for logging
        
    Returns:
        List of corrected items that match the expected total
    """
    # Calculate current total
    current_total = sum(item.get("cost_price", 0) for item in items)
    
    # Allow small rounding difference (0.01)
    if abs(current_total - expected_total) < 0.01:
        return items  # Totals match, return all items
    
    difference = current_total - expected_total
    
    print(f"Invoice {invoice_number}: Mismatch detected. Current: £{current_total:.2f}, Expected: £{expected_total:.2f}, Difference: £{difference:.2f}")
    
    # Try to find and remove deleted items
    corrected_items = remove_deleted_items(items, difference, expected_total)
    
    return corrected_items


def remove_deleted_items(items, difference, expected_total):
    """
    Identify and remove deleted items by finding combinations that match the difference.
    
    Args:
        items: List of invoice items
        difference: The amount difference to reconcile
        expected_total: The target total
        
    Returns:
        List of items with deleted items removed
    """
    # Sort items by cost (largest first) for better matching
    sorted_items = sorted(items, key=lambda x: abs(x.get("cost_price", 0)), reverse=True)
    
    # Try to find single item that matches the difference
    for i, item in enumerate(sorted_items):
        if abs(item.get("cost_price", 0) - difference) < 0.01:
            print(f"  Removing deleted item: {item.get('product_description')} (£{item.get('cost_price', 0):.2f})")
            return sorted_items[:i] + sorted_items[i+1:]
    
    # Try combinations of 2 items
    for i in range(len(sorted_items)):
        for j in range(i + 1, len(sorted_items)):
            combined_cost = sorted_items[i].get("cost_price", 0) + sorted_items[j].get("cost_price", 0)
            if abs(combined_cost - difference) < 0.01:
                print(f"  Removing deleted items:")
                print(f"    - {sorted_items[i].get('product_description')} (£{sorted_items[i].get('cost_price', 0):.2f})")
                print(f"    - {sorted_items[j].get('product_description')} (£{sorted_items[j].get('cost_price', 0):.2f})")
                return [item for idx, item in enumerate(sorted_items) if idx not in [i, j]]
    
    # Try combinations of 3 items
    for i in range(len(sorted_items)):
        for j in range(i + 1, len(sorted_items)):
            for k in range(j + 1, len(sorted_items)):
                combined_cost = (sorted_items[i].get("cost_price", 0) + 
                               sorted_items[j].get("cost_price", 0) + 
                               sorted_items[k].get("cost_price", 0))
                if abs(combined_cost - difference) < 0.01:
                    print(f"  Removing deleted items:")
                    print(f"    - {sorted_items[i].get('product_description')} (£{sorted_items[i].get('cost_price', 0):.2f})")
                    print(f"    - {sorted_items[j].get('product_description')} (£{sorted_items[j].get('cost_price', 0):.2f})")
                    print(f"    - {sorted_items[k].get('product_description')} (£{sorted_items[k].get('cost_price', 0):.2f})")
                    return [item for idx, item in enumerate(sorted_items) if idx not in [i, j, k]]
    
    # If no exact match found, log warning and return original items
    print(f"  WARNING: Could not find exact matching items to remove. Keeping all items.")
    return items
