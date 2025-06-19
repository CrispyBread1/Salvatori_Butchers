from datetime import date, datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from auth.userAuthentication import AuthService
from gui.components.reusable.animations.loading_component import LoadingManager
from controllers.sage_controllers.invoices import *
from gui.components.scheduled_tasks_windows.butchers_list.butchers_list_table import ButchersListTable
from utils.butchers_list_utils import get_invoice_products, refresh_get_invoice_products
from resources.excel_exporter import ExcelExporter

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

        self.refresh_report_button = QPushButton("Refresh Report", self)
        self.refresh_report_button.clicked.connect(self.refresh_mpp_report)
        self.refresh_report_button.hide()


        self.export_xl_button = QPushButton("Export to XL", self)
        self.export_xl_button.clicked.connect(self.export_to_xl)
        
        
        self.button_layout.addWidget(self.create_report_button)
        self.button_layout.addWidget(self.refresh_report_button)

        self.button_layout.addWidget(self.export_xl_button)
        self.main_layout.addLayout(self.button_layout)
        
        # Status label to show results
        self.status_label = QLabel("", self)
        self.main_layout.addWidget(self.status_label)


        
        # Update UI with current date
        self.update_ui()
          
    def update_ui(self):
        """Update UI elements without recreating the layout"""
        self.title_label.setText(f"MPP Report - {self.date}")
        self.status_label.setText("")  # Clear previous status

    def create_mpp_report(self):
        pass
    
    def refresh_mpp_report(self):
        pass
    
    def export_to_xl(self):
        pass

