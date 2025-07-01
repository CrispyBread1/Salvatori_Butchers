from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from auth.userAuthentication import AuthService
from controllers.sage_controllers.invoice_products import get_invoice_items_between_time_frame, get_invoice_items_id
from database.products import fetch_products
from database.reports import fetch_report_by_id
from gui.components.reusable.animations.loading_component import LoadingManager
from controllers.sage_controllers.invoices import *
from gui.components.scheduled_tasks_windows.butchers_list.butchers_list_table import ButchersListTable
from utils.butchers_list_utils import get_invoice_products, refresh_get_invoice_products
from resources.excel_exporter import ExcelExporter
from utils.mpp_report_utils import add_customer_mpp_report, remove_customer_mpp_report

class MPPReport(QWidget):

    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()
        self.user = self.auth_service.current_user

        self.loading_manager = LoadingManager(self)
        self.excel_exporter = ExcelExporter(self)  # Initialize Excel exporter
        self.customer_invoice_data = None  # Store data for export
        
        self.date = date.today().strftime('%Y-%m-%d')
        self.previous_week = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
        
        # Create main layout once
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Create title label that we'll update
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        self.create_report_button = QPushButton("Create report", self)
        self.create_report_button.clicked.connect(self.create_mpp_report)

        self.button_layout.addWidget(self.create_report_button)

        self.main_layout.addLayout(self.button_layout)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        self.main_layout.addWidget(self.status_label)

        self.report = fetch_report_by_id(2)
        
        # Update UI with current date
        self.update_ui()
          
    def update_ui(self):
        """Update UI elements without recreating the layout"""
        self.title_label.setText(f"MPP Report - {self.date}")
        self.status_label.setText("")  # Clear previous status

    def create_mpp_report(self):
        # Disable the button to prevent multiple clicks
        self.create_report_button.setEnabled(False)
        # Use the loading manager to run the get_invoice_products function with a loading animation
        self.loading_manager.run_with_loading(
            task_function=self.create_report,  # Direct call to your function
            on_complete=self.on_fetch_complete,
            on_error=self.on_fetch_error,
            loading_text="Fetching invoice data...",
            title="Loading Invoices",
            task_args=(self.date, self.previous_week, self.report)
        )

    def create_report(self, date, previous_week, report):
        invoices = get_the_last_weeks_invoices(date, previous_week)
        invoice_ids = self.get_customer_invoice_ids(invoices, report.customers)
        invoice_items_for_week = get_invoice_items_id(invoice_ids)
        customer_invoices = self.get_customer_invoices(invoices, report.customers)
        customer_invoice_items = self.get_customer_invoice_items(invoice_items_for_week, customer_invoices, report.customers)
        return customer_invoice_items, None

    def on_fetch_complete(self, customer_invoice_data, updated_at, original_id=None):
        # Re-enable button
        self.create_report_button.setEnabled(True)
        
        # Update status with results
        if customer_invoice_data:
            self.customer_invoice_data = customer_invoice_data  # Store data for export
            self.status_label.setText(f"Successfully created {self.date} product report.")
            self.export_detailed_report()
            
            # print(customer_invoice_data)
            self.update_ui()
        else:
            self.status_label.setText("No invoices found for the selected date.")

    def on_fetch_error(self, error_message):
        # Re-enable button
        self.create_report_button.setEnabled(True) 
        
        # Show error message
        print(error_message)
        self.status_label.setText(f"Error fetching invoices: {error_message}")

    def export_detailed_report(self):
        """Export detailed report with all invoice items"""
        # Flatten the data for detailed export
        flattened_data = self.flatten_invoice_data(self.customer_invoice_data)
        # print(flattened_data)
        # Define headers for detailed report (using display names)
        headers = [
              'location_name', 'city', 'county', 'address_1', 'address_2', 'post_code',
              'sage_code', 'account_name', 'distributor_location',
              'invoice_number', 'invoice_date',
              'product_code', 'product_description', 'unit_price', 'quantity', 'total_price', 'unit_of_measurement'
        ]
            
        # Generate filename
        filename = f"MPP_Detailed_Report_{self.date}"
            
            # Export using the Excel exporter
        exporter = ExcelExporter(parent=self)

        exporter.export(
            data=flattened_data,    
            sheet_name="MPP Data",   # name of the sheet
            title= f"MPP Detailed Report - {self.date}",
            headers=headers,  # order of columns
            butchers_list=False
        )
            
        QMessageBox.information(self, "Success", f"Report exported successfully!")
            
        

    def flatten_invoice_data(self, customer_data):
        """Convert nested invoice data to flat structure for Excel export"""
        flattened = []
        
        for customer in customer_data:
            # Skip locations with no data
            if not customer.get('data'):
                continue
                
            location_info = {
                'location_name': customer.get('location_name', ''),
                'city': customer.get('city', ''),
                'county': customer.get('county', ''),
                'address_1': customer.get('address_1', ''),
                'address_2': customer.get('address_2', ''),
                'post_code': customer.get('post_code', ''),
                'sage_code': customer.get('sage_code', ''),
                'account_name': customer.get('account_name', ''),
                'distributor_location': customer.get('distributor_location', '')
            }
            
            for invoice in customer.get('data', []):
                invoice_info = {
                    'invoice_number': invoice.get('invoice_number', ''),
                    'invoice_date': invoice.get('invoice_date', ''),
                }
                
                # Only add rows for invoices that have items
                if invoice.get('invoice_items'):
                    for item in invoice.get('invoice_items', []):
                        row = {**location_info, **invoice_info}
                        row.update({
                            'product_code': item.get('product_code', ''),
                            'product_description': item.get('product_description', ''),
                            'unit_price': item.get('product_unit_price', 0),
                            'quantity': item.get('amount', 0),
                            'total_price': item.get('total_price', 0),
                            'unit_of_measurement': item.get('unit_of_measurement', 0)
                        })
                        flattened.append(row)
        
        return flattened

    def get_customer_invoices(self, invoices, customers):
        customer_invoices = {}
        for customer in customers:
            # Use consistent dictionary access
            customer_invoices[customer["sage_code"]] = []
            for invoice in invoices:
                if customer["sage_code"] == invoice["accountRef"]:
                    customer_invoices[customer["sage_code"]].append(invoice)
        return customer_invoices
    
    def get_customer_invoice_ids(self, invoices, customers):
        customer_invoices = {}
        for customer in customers:
            # Use consistent dictionary access
            customer_invoices[customer["sage_code"]] = []
            for invoice in invoices:
                if customer["sage_code"] == invoice["accountRef"]:
                    customer_invoices[customer["sage_code"]].append(invoice["invoiceNumber"])
        return customer_invoices
        
    def get_customer_invoice_items(self, invoice_items_for_week, customer_invoices, customers):
        for customer in customers:
            customer["data"] = []  # Initialize as empty list instead of dict
            for customer_invoice in customer_invoices[customer["sage_code"]]:
                invoice_data = {
                    "invoice_number": customer_invoice["invoiceNumber"],
                    "invoice_date": customer_invoice["invoiceDate"],
                    "invoice_items": self.filter_invoice_items(invoice_items_for_week, customer_invoice["invoiceNumber"])
                }
                customer["data"].append(invoice_data)  # Append each invoice as an object to the list
        return customers

    def filter_invoice_items(self, invoice_items_for_week, customer_invoice_number):    
        supabase_items =  fetch_products()
        items = []
        for invoice_item in invoice_items_for_week:
            invoice_item_number = invoice_item["invoiceNumber"]
            if int(invoice_item_number) == int(customer_invoice_number):
                item_data = {
                    "product_code": invoice_item["stockCode"],
                    "product_description": invoice_item["description"],
                    "product_unit_price": invoice_item["unitPrice"],
                    "amount": invoice_item["quantity"],
                    "total_price": invoice_item["netAmount"],
                    "unit_of_measurement": self.get_unit_of_measurement(supabase_items, invoice_item["stockCode"])
                }
                items.append(item_data)
        return items
    
    def get_unit_of_measurement(self, supabase_items, stockCode):
        for supabase_item in supabase_items:
            sage_code = supabase_item.sage_code
            
            try:
                # Try to parse as JSON first
                parsed_sage_codes = json.loads(sage_code)
                
                if isinstance(parsed_sage_codes, str):
                    # JSON string value
                    if parsed_sage_codes == stockCode:
                        return supabase_item.sold_as
                elif isinstance(parsed_sage_codes, list):
                    # JSON array
                    if stockCode in parsed_sage_codes:
                        return supabase_item.sold_as
                        
            except (json.JSONDecodeError, TypeError):
                # If JSON parsing fails, treat as plain string
                if isinstance(sage_code, str) and sage_code == stockCode:
                    return supabase_item.sold_as
        
        return None
