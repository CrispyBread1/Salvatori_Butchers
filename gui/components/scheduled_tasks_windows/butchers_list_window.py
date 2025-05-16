from datetime import date, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from auth.userAuthentication import AuthService
from database.butchers_lists import combine_butchers_lists, fetch_all_butchers_lists_by_date, insert_butchers_list
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.components.reusable.date_input_dialog import DateInputDialog
from gui.components.scheduled_tasks_windows.butchers_list.butcher_list_picker_dialogue import ButcherListPicker
from controllers.sage_controllers.invoices import *
from gui.components.scheduled_tasks_windows.butchers_list.butchers_list_table import ButchersListTable
from resources.excel_exporter import ExcelExporter


class ButchersListWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()
        self.user = self.auth_service.current_user

        self.loading_manager = LoadingManager(self)
        self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.butchers_lists = fetch_all_butchers_lists_by_date(self.date)
        # Create main layout once
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Create title label that we'll update
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.main_layout.addWidget(self.title_label)
        
        # Create button layout
        self.button_layout = QHBoxLayout()
        
        self.pull_orders_button = QPushButton("Pull Orders", self)
        self.pull_orders_button.clicked.connect(self.pull_butcher_data)
        
        self.change_date_button = QPushButton("Change Date", self)
        self.change_date_button.clicked.connect(self.change_date)

        self.export_xl_button = QPushButton("Export to XL", self)
        self.export_xl_button.clicked.connect(self.export_to_xl)
        
        
        self.button_layout.addWidget(self.change_date_button)
        self.button_layout.addWidget(self.pull_orders_button)



        self.button_layout.addWidget(self.export_xl_button)
        self.main_layout.addLayout(self.button_layout)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        self.main_layout.addWidget(self.status_label)

        self.butchers_table = ButchersListTable(self)
        self.main_layout.addWidget(self.butchers_table)
        
        # Update UI with current date
        self.update_ui()
          
    def update_ui(self):
        """Update UI elements without recreating the layout"""
        self.title_label.setText(f"Butchers List - {self.date}")
        self.status_label.setText("")  # Clear previous status
        self.butchers_table.load_butchers_lists(self.butchers_lists)

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
    
    def on_fetch_complete(self, invoices, updated_at):
        # Re-enable button
        self.pull_orders_button.setEnabled(True)  # Fixed: was using general_settings_button
        # Update status with results
        if invoices:
            self.status_label.setText(f"Successfully created {self.date} butchers list.")
            # Process invoices further as needed            
            insert_butchers_list(self.date, invoices, updated_at)
            self.butchers_lists = fetch_all_butchers_lists_by_date(self.date)
            self.update_ui()
        else:
            self.status_label.setText("No invoices found for the selected date.")

        self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
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
            self.butchers_lists = fetch_all_butchers_lists_by_date(self.date)
            # Update the UI with the new date
            self.update_ui()

    def invoice_pull_test(self):
        butchers_lists = fetch_all_butchers_lists_by_date(self.date)
        print(self.butchers_lists)

    def export_to_xl(self):
        butchers_list_count = len(self.butchers_lists)
        selected_butchers_list = 0
        list_number = ""
        todays_date = date.today().strftime('%Y-%m-%d')

        # if butchers_list_count > 1:
        dialog = ButcherListPicker(max_number=len(self.butchers_lists))
        if dialog.exec_():
            selected_butchers_list = dialog.get_selected_number()                
            print(f"User selected number: {selected_butchers_list}")
        
        flattened_data = []
        # print(self.butchers_lists)
        if selected_butchers_list == -1:
            combined_data = combine_butchers_lists(self.butchers_lists)
            flattened_data = self.flatten_order_data(combined_data)
            list_number += "List: All"
        else:
            flattened_data = self.flatten_order_data(self.butchers_lists[selected_butchers_list].data)
            list_number += f"List: {(selected_butchers_list + 1)}"



        exporter = ExcelExporter(parent=self)  # `self` = your PyQt window/widget
        exporter.export(
            data=flattened_data,
            group_by="customer_name",       # groups rows under customer headings
            sheet_name="Customer Orders",   # name of the sheet
            title= f"Date: {todays_date}, {list_number}",
            headers=["Product", "Quantity"],  # order of columns
            butchers_list=True
        )

    def flatten_order_data(self, fetched_data):
        """
        Takes the fetched tuple and returns flattened data for Excel export.
        """
        
         # This is the list of customer dicts
        flattened = []

        for customer in fetched_data:
            for product in customer.get("products", []):
                flattened.append({
                    "customer_name": customer["customer_name"],
                    "product": product["product_name"],
                    "quantity": product["quantity"]
                })
        
        return flattened
    
    def create_table(self):
        headers = ["Customer", "Age", "City"]
        data = []
        self.table.populate(headers, data)
 
