import calendar
import json
from controllers.sage_controllers.invoice_products import get_invoice_items_id
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

    return processed_data
  

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
