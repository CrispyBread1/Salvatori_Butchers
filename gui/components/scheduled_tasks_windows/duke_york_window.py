from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox, QComboBox,
    QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QDialog, QDialogButtonBox
)
from auth.userAuthentication import AuthService
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

        self.auth_service = AuthService()
        self.user = self.auth_service.current_user

        self.loading_manager = LoadingManager(self)
        self.date = (date.today() + timedelta(days=1))

        self.current_duke_york_prices = get_duke_york_prices_complete(self.date)

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

        self.archive_duke_york_price_list_button = QPushButton("Delete Record", self)
        self.archive_duke_york_price_list_button.clicked.connect(self.archive_duke_york_price_list)

        # self.export_xl_button = QPushButton("Export to XL", self)
        # self.export_xl_button.clicked.connect(self.export_to_xl)
        
        self.button_layout.addWidget(self.change_date_button)
        self.button_layout.addWidget(self.pull_prices_button)
        self.button_layout.addWidget(self.archive_duke_york_price_list_button)

        # self.button_layout.addWidget(self.export_xl_button)
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
            self.pull_prices_button.setEnabled(False)
        else:
            # Load empty table if no data
            self.duke_york_prices_table.load_invoices([])
            self.pull_prices_button.setEnabled(True)
            self.archive_duke_york_price_list_button.hide()
        
        

    def pull_duke_york_data(self):
        # Disable the button to prevent multiple clicks
        self.pull_prices_button.setEnabled(False)  # Fixed: was using general_settings_button
        
        # Use the loading manager to run the get_invoice_products function with a loading animation
        self.loading_manager.run_with_loading(
            task_function=get_duke_york_prices,  # Direct call to your function
            on_complete=self.on_fetch_complete,
            on_error=self.on_fetch_error,
            on_pause=self.handle_pause,
            loading_text="Fetching invoice data...",
            title="Loading Invoices",
            task_args=(self.date,)
        )

    def handle_pause(self, data):
        pass

    
    def on_fetch_complete(self, invoices_data, updated_at, original_id=None):
        # Re-enable button
        self.pull_prices_button.setEnabled(True)  # Fixed: was using general_settings_button
        # Update status with results
        print(f"on_fetch_complete: {invoices_data}")
        if invoices_data:
            self.status_label.setText(f"Successfully created {self.date} kings head rye prices.")
            # Process invoices further as needed            
            insert_duke_york_prices(self.date, invoices_data)
            self.current_duke_york_prices = get_duke_york_prices_complete(self.date)
            self.update_ui()
        else:
            self.status_label.setText("No invoices found for the selected date.")

        # self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    def on_fetch_error(self, error_message):
        # Re-enable button
        self.pull_prices_button.setEnabled(True)  # Fixed: was using general_settings_button
        
        # Show error message
        print(error_message)
        self.status_label.setText(f"Error fetching invoices: {error_message}")
    

    
    def change_date(self):
      # Open date input dialog
      dialog = MonthInputDialog(self)
      if dialog.exec_():  # If user clicks OK
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
      pass
    
    def archive_duke_york_price_list(self):
      deactivate_duke_york_prices(self.current_duke_york_prices.id)
      self.update_ui()
   
