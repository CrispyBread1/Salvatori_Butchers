import calendar
from controllers.sage_controllers.invoices import get_customer_invoices_by_month

duke_york_product_sage_codes = ['BE2', 'CHR93', 'CHR941', 'CHR31', 'CHR92', 'CHR921', 'CHR9201', 'SS111', 'BAC2', 'LA11', 'PO4', 'SSD2', 'PO5', 'BAC81', 'BAC3', 'BE4']
duke_york_customer_sage_code = 'TFDUKEY'

def get_duke_york_prices(date,  on_pause=None):
  start_month = date.replace(day=1).strftime("%Y-%m-%d")
  last_day = calendar.monthrange(date.year, date.month)[1]
  end_month = date.replace(day=last_day).strftime("%Y-%m-%d %H:%M:%S")

  invoice_list = get_customer_invoices_by_month(duke_york_customer_sage_code, start_month, end_month)
  print(invoice_list)
  
