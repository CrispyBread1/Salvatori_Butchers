from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox, QComboBox,
    QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QDialog, QDialogButtonBox
)
from database.duke_york_prices import deactivate_duke_york_prices, insert_duke_york_prices
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.components.reusable.month_input_dialog import MonthInputDialog
from controllers.sage_controllers.invoices import *
from gui.components.scheduled_tasks_windows.duke_york_prices.duke_york_prices_table import DukeYorkPricesTable
from resources.excel_exporter import ExcelExporter
from utils.duke_york_prices_utils import *


class DukeYorkPricesWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.loading_manager = LoadingManager(self)
        self.excel_exporter = ExcelExporter(self)
        self.date = (date.today() + timedelta(days=1))

        self.current_duke_york_prices = get_duke_york_prices_complete(self.date)
        self.report = fetch_report_by_id(3)

        # Create main layout once
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Create title label that we'll update
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        self.pull_prices_button = QPushButton("Pull Prices", self)
        self.pull_prices_button.clicked.connect(self.pull_duke_york_data)
        
        self.change_date_button = QPushButton("Change Date", self)
        self.change_date_button.clicked.connect(self.change_date)

        # self.update_prices_products_button = QPushButton("Update Prices/Products", self)
        # self.update_prices_products_button.clicked.connect(self.update_prices_products)

        self.archive_duke_york_price_list_button = QPushButton("Delete Record", self)
        self.archive_duke_york_price_list_button.clicked.connect(self.archive_duke_york_price_list)

        self.export_xl_button = QPushButton("Export to Excel", self)
        self.export_xl_button.clicked.connect(self.export_to_excel)
        
        self.button_layout.addWidget(self.change_date_button)
        # self.button_layout.addWidget(self.update_prices_products_button)
        self.button_layout.addWidget(self.pull_prices_button)
        self.button_layout.addWidget(self.archive_duke_york_price_list_button)
        self.button_layout.addWidget(self.export_xl_button)

        self.main_layout.addLayout(self.button_layout)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        self.main_layout.addWidget(self.status_label)

        self.duke_york_prices_table = DukeYorkPricesTable(self)
        self.main_layout.addWidget(self.duke_york_prices_table)
        
        # Update UI with current date
        self.update_ui()
          
    def update_ui(self):
        """Update UI elements without recreating the layout"""
        self.title_label.setText(f"Duke York Prices - {self.date}")
        self.status_label.setText("")  # Clear previous status
        
        if self.current_duke_york_prices and hasattr(self.current_duke_york_prices, 'data'):
            self.duke_york_prices_table.load_invoices(self.current_duke_york_prices.data)
            self.archive_duke_york_price_list_button.show()
            self.export_xl_button.show()
            self.pull_prices_button.setEnabled(False)
        else:
            # Load empty table if no data
            self.duke_york_prices_table.load_invoices([])
            self.pull_prices_button.setEnabled(True)
            self.archive_duke_york_price_list_button.hide()
            self.export_xl_button.hide()
        
        

    def pull_duke_york_data(self):
        # Disable the button to prevent multiple clicks
        self.pull_prices_button.setEnabled(False)
        
        # Use the loading manager to run the get_invoice_products function with a loading animation
        self.loading_manager.run_with_loading(
            task_function=get_duke_york_prices,
            on_complete=self.on_fetch_complete,
            on_error=self.on_fetch_error,
            on_pause=self.handle_pause,
            loading_text="Fetching invoice data...",
            title="Loading Invoices",
            task_args=(self.date, self.report)
        )

    def handle_pause(self, data):
        pass

    
    def on_fetch_complete(self, invoices_data, updated_at, original_id=None):
        # Re-enable button
        self.pull_prices_button.setEnabled(True)
        # Update status with results
        if invoices_data:
            self.status_label.setText(f"Successfully created {self.date} Duke York prices.")
            # Process invoices further as needed            
            insert_duke_york_prices(self.date, invoices_data)
            self.current_duke_york_prices = get_duke_york_prices_complete(self.date)
            self.update_ui()
        else:
            self.status_label.setText("No invoices found for the selected date.")
    
    def on_fetch_error(self, error_message):
        # Re-enable button
        self.pull_prices_button.setEnabled(True)
        
        # Show error message
        print(error_message)
        self.status_label.setText(f"Error fetching invoices: {error_message}")
    
    def change_date(self):
        # Open date input dialog
        dialog = MonthInputDialog(self)
        if dialog.exec_():
            date_string = dialog.get_just_date()
            # Convert string to date object if it's a string
            if isinstance(date_string, str):
                self.date = datetime.strptime(date_string, "%Y-%m-%d").date()
            else:
                self.date = date_string
            
            self.current_duke_york_prices = get_duke_york_prices_complete(self.date)
            # Update the UI with the new date
            self.update_ui()

    def export_to_excel(self):
        """Export Duke York prices to Excel"""
        if not self.current_duke_york_prices or not hasattr(self.current_duke_york_prices, 'data'):
            QMessageBox.warning(self, "No Data", "No data available to export.")
            return
        
        try:
            # Prepare data for export
            invoices_data = self.current_duke_york_prices.data
            
            # Format the data for Excel (convert to list of dicts with proper keys)
            export_data = []
            for invoice in invoices_data:
                invoice_number = str(invoice.get("invoice_number", ""))
                cost_price = invoice.get('cost_price', 0)
                exact_price = invoice.get('exact_price', 0)
                
                # Check if it's a credit invoice (7 digits) and make negative
                if len(invoice_number) == 7:
                    cost_price = -cost_price
                    exact_price = -exact_price
                
                export_data.append({
                    'Invoice #': invoice_number,
                    'Date': self._format_date(invoice.get("invoice_date", "")),
                    'Product': invoice.get("product_description", ""),
                    'Sage Code': invoice.get("product_sage_code", ""),
                    'Cost Price': f"£{cost_price:.2f}",
                    'Exact Price': f"£{exact_price:.2f}"
                })
            
            # Add totals row
            total_cost = sum(
                (-inv.get('cost_price', 0) if len(str(inv.get("invoice_number", ""))) == 7 else inv.get('cost_price', 0))
                for inv in invoices_data
            )
            total_exact = sum(
                (-inv.get('exact_price', 0) if len(str(inv.get("invoice_number", ""))) == 7 else inv.get('exact_price', 0))
                for inv in invoices_data
            )
            
            export_data.append({
                'Invoice #': '',
                'Date': '',
                'Product': 'TOTAL',
                'Sage Code': '',
                'Cost Price': f"£{total_cost:.2f}",
                'Exact Price': f"£{total_exact:.2f}"
            })
            
            # Set headers
            headers = ['Invoice #', 'Date', 'Product', 'Sage Code', 'Cost Price', 'Exact Price']
            
            # Generate filename
            date_str = self.date.strftime("%Y-%m-%d")
            default_filename = f"Duke_York_Prices_{date_str}.xlsx"
            
            # Export using ExcelExporter
            self.excel_exporter.export(
                data=export_data,
                headers=headers,
                title=f"Duke York Prices - {date_str}",
                sheet_name="Duke York Prices",
                filename=None  # Will trigger file dialog
            )
            
            self.status_label.setText("Excel file exported successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export to Excel: {str(e)}")
            print(f"Export error: {e}")
    
    def _format_date(self, date_str):
        """Format date string to readable format"""
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str

    def update_prices_products(self):
        pass
    
    def archive_duke_york_price_list(self):
        deactivate_duke_york_prices(self.current_duke_york_prices.id)
        self.current_duke_york_prices = get_duke_york_prices_complete(self.date)
        self.update_ui()
