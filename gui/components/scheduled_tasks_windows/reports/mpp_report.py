from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from auth.userAuthentication import AuthService
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
        self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
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

        self.create_report_button = QPushButton("Add Customer To Report", self)
        self.create_report_button.clicked.connect(self.add_customer)

        self.create_report_button = QPushButton("Remove Customer From Report", self)
        self.create_report_button.clicked.connect(self.remove_customer)

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
        pass
    
    def add_customer(self):
        customer_id = self.open_product_selection()

        state, message = add_customer_mpp_report(self.report, customer_id)
        QMessageBox.information(
                  self, 
                  f"{state}", 
                  f"{message}!"
              )
          # Update the UI to reflect the changes
        self.update_ui()
          
    def remove_customer(self):
        customer_id = self.open_product_selection(True)

        state, message = remove_customer_mpp_report(self.report, customer_id)
        QMessageBox.information(
                  self, 
                  f"{state}", 
                  f"{message}!"
              )
          # Update the UI to reflect the changes
        self.update_ui()
    
    def export_to_xl(self):
        pass

