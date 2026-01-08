import calendar
from controllers.sage_controllers.invoice_products import get_invoice_items_id
from controllers.sage_controllers.invoices import get_customer_invoices_by_month

duke_york_product_sage_codes = ['BE2', 'CHR93', 'CHR941', 'CHR31', 'CHR92', 'CHR921', 'CHR9201', 'SS111', 'BAC2', 'LA11', 'PO4', 'SSD2', 'PO5', 'BAC81', 'BAC3', 'BE4']
duke_york_customer_sage_code = 'TFDUKEY'

def get_duke_york_prices(date,  on_pause=None):
  start_month = date.replace(day=1).strftime("%Y-%m-%d")
  last_day = calendar.monthrange(date.year, date.month)[1]
  end_month = date.replace(day=last_day).strftime("%Y-%m-%d %H:%M:%S")

  invoice_list = get_customer_invoices_by_month(duke_york_customer_sage_code, start_month, end_month)['results']
  invoices_ids = []


  if invoice_list:
    if invoice_list and 'results' in invoice_list and invoice_list['results']:
          for invoice in invoice_list['results']:
              if 'invoiceNumber' in invoice:
                  invoices_ids.append(invoice['invoiceNumber'])
          
    invoice_items = get_invoice_items_id(invoices_ids)

    processed_data = process_duke_york_prices(invoice_list, invoice_items)

    return
  

def process_duke_york_prices(invoice_list, invoice_items):
  # [{invoice_number: '', invoice_date: '', product_description: '', product_sage_code: '', cost_price: '', exact_price: ''},],

  processed_data = []

  for invoice in invoice_list:
    invoice_number = invoice.get("invoiceNumber")
    
    
    for invoice_item in invoice_items:
      invoice_item_number = invoice_item.get("invoiceNumber")

      if invoice_number == invoice_item_number:
        invoice_item_cost = invoice_item.get("netAmount")
        invoice_item_sage_code = invoice_item.get("stockCode")

        processed_invoice_item_data = {
          'invoice_number': invoice_item_number, 
          'invoice_date': invoice.get("invoiceDate"), 
          'product_description': invoice_item.get("description"), 
          'product_sage_code': invoice_item_sage_code, 
          'cost_price': invoice_item_cost, 
          'exact_price': get_exact_item_price(invoice_item_sage_code, invoice_item_cost)
         }
        
        processed_data.append(processed_invoice_item_data)

def get_exact_item_price(invoice_item_sage_code, invoice_item_cost):
  pass   
