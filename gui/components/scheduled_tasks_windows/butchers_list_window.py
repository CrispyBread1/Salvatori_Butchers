from datetime import timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from database.butchers_lists import fetch_butchers_list_by_date
from gui.components.reusable.animations.loading_component import LoadingManager
from sage_controllers.invoices import *



class ButchersListWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.loading_manager = LoadingManager(self)
        self.setup_ui()
        self.date = (date.today() + timedelta(days=1)).isoformat()
          
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Butchers List")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
      
        self.settings_menu_layout = QHBoxLayout()

        self.general_settings_button = QPushButton("Pull Orders", self)
        self.general_settings_button.clicked.connect(self.pull_butcher_data)
        
        self.settings_menu_layout.addWidget(self.general_settings_button)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        layout.addLayout(self.settings_menu_layout)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def pull_butcher_data(self):
        # Disable the button to prevent multiple clicks
        self.general_settings_button.setEnabled(False)
        
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
        self.general_settings_button.setEnabled(True)
        
        # Update status with results
        if invoices:
            print(invoices)
            self.status_label.setText(f"Successfully fetched {len(invoices)} invoices.")
            # Process invoices further as needed
            self.process_invoices(invoices)
        else:
            self.status_label.setText("No invoices found for today.")
    
    def on_fetch_error(self, error_message):
        # Re-enable button
        self.general_settings_button.setEnabled(True)
        
        # Show error message
        self.status_label.setText(f"Error fetching invoices: {error_message}")
    
    def process_invoices(self, invoices):
        butchers_list = fetch_butchers_list_by_date()
        
        pass

