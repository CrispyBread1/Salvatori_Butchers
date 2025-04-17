from datetime import date, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from database.butchers_lists import fetch_butchers_list_by_date, insert_butchers_list
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.components.reusable.date_input_dialog import DateInputDialog
from controllers.sage_controllers.invoices import *
from resources.excel_exporter import ExcelExporter


class ButchersListWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.loading_manager = LoadingManager(self)
        self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.butchers_list = fetch_butchers_list_by_date(self.date)
        # Create main layout once
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Create title label that we'll update
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        self.pull_orders_button = QPushButton("Pull Orders", self)
        self.pull_orders_button.clicked.connect(self.pull_butcher_data)
        
        self.change_date_button = QPushButton("Change Date", self)
        self.change_date_button.clicked.connect(self.change_date)

        self.export_xl_button = QPushButton("Export to XL", self)
        self.export_xl_button.clicked.connect(self.export_to_xl)
        
        self.invoice_pull_test_button = QPushButton("invoice_pull_test_button", self)
        self.invoice_pull_test_button.clicked.connect(self.invoice_pull_test)
        
        button_layout.addWidget(self.pull_orders_button)
        button_layout.addWidget(self.change_date_button)
        button_layout.addWidget(self.invoice_pull_test_button)
        button_layout.addWidget(self.export_xl_button)
        self.main_layout.addLayout(button_layout)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        self.main_layout.addWidget(self.status_label)
        
        # Update UI with current date
        self.update_ui()
          
    def update_ui(self):
        """Update UI elements without recreating the layout"""
        self.title_label.setText(f"Butchers List - {self.date}")
        self.status_label.setText("")  # Clear previous status

    def pull_butcher_data(self):
        # Disable the button to prevent multiple clicks
        self.pull_orders_button.setEnabled(False)  # Fixed: was using general_settings_button
        
        # Use the loading manager to run the get_invoice_products function with a loading animation
        self.loading_manager.run_with_loading(
            task_function=get_invoice_products,  # Direct call to your function
            on_complete=self.on_fetch_complete,
            on_error=self.on_fetch_error,
            loading_text="Fetching invoice data...",
            title="Loading Invoices",
            task_args=(self.date,)
        )
    
    def on_fetch_complete(self, invoices):
        # Re-enable button
        self.pull_orders_button.setEnabled(True)  # Fixed: was using general_settings_button
        
        # Update status with results
        if invoices:
            self.status_label.setText(f"Successfully created {self.date} butchers list.")
            # Process invoices further as needed
            insert_butchers_list(self.date, invoices)
        else:
            self.status_label.setText("No invoices found for the selected date.")
    
    def on_fetch_error(self, error_message):
        # Re-enable button
        self.pull_orders_button.setEnabled(True)  # Fixed: was using general_settings_button
        
        # Show error message
        print(error_message)
        self.status_label.setText(f"Error fetching invoices: {error_message}")
    
    def change_date(self):
        # Open date input dialog
        dialog = DateInputDialog(self)
        if dialog.exec_():  # If user clicks OK
            self.date = dialog.get_just_date()
            self.butchers_list = fetch_butchers_list_by_date(self.date)
            # Update the UI with the new date
            self.update_ui()

    def invoice_pull_test(self):
        invoice = get_todays_invoices(self.date)
        print(invoice)

    def export_to_xl(self):
        if self.butchers_list:
            # print(self.butchers_list)
            flattened_data = self.flatten_order_data(self.butchers_list)

            exporter = ExcelExporter(parent=self)  # `self` = your PyQt window/widget
            exporter.export(
                data=flattened_data,
                group_by="customer_name",       # groups rows under customer headings
                sheet_name="Customer Orders",   # name of the sheet
                headers=["product_name", "quantity"]  # order of columns
            )

    def flatten_order_data(self, fetched_data):
        """
        Takes the fetched tuple and returns flattened data for Excel export.
        """
        raw_data = fetched_data[-1]  # This is the list of customer dicts
        flattened = []

        for customer in raw_data:
            for product in customer.get("products", []):
                flattened.append({
                    "customer_name": customer["customer_name"],
                    "product_name": product["product_name"],
                    "quantity": product["quantity"]
                })
        
        return flattened
 
