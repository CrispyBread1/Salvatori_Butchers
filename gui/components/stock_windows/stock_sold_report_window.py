from datetime import date
import json
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMessageBox, QDialog
)

from database.products import fetch_products
from database.reports import fetch_report_by_id, update_report
from gui.components.reusable.date_input_dialog import DateInputDialog
from gui.components.reusable.table import DynamicTableWidget
from gui.components.stock_windows.stock_sold.add_product_popup import AddProductPopup


class StockSoldReportWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.main_layout = QVBoxLayout()
    self.title_label = QLabel()
    self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
    self.main_layout.addWidget(self.title_label)
    self.setup_ui()
        
  def setup_ui(self):
      self.report = fetch_report_by_id(1)  
      print(self.report)   
      self.date = date.today().strftime('%Y-%m-%d')
      self.title_label.setText(f"Report for: {self.date}")

      
      # Title
      # title = QLabel("Stock Sold Report")
      # title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
      # layout.addWidget(title)

      self.change_date_button = QPushButton("Change Date", self)
      self.change_date_button.clicked.connect(self.change_date)
      self.create_report_button = QPushButton("Create Report", self)
      self.create_report_button.clicked.connect(self.create_report)
      self.add_product_button = QPushButton("Add product", self)
      self.add_product_button.clicked.connect(self.add_product)
      self.remove_product_button = QPushButton("Remove product", self)
      self.remove_product_button.clicked.connect(self.remove_product)
      
      self.button_layout = QHBoxLayout()
      self.button_layout.addWidget(self.change_date_button)
      self.button_layout.addWidget(self.create_report_button)
      self.button_layout.addWidget(self.add_product_button)
      self.button_layout.addWidget(self.remove_product_button)


      self.main_layout.addLayout(self.button_layout)
    
      self.setLayout(self.main_layout)


  def change_date(self):
      # Open date input dialog
      dialog = DateInputDialog(self)
      if dialog.exec_():  # If user clicks OK
          self.date = dialog.get_just_date()
          # self.butchers_lists = fetch_all_butchers_lists_by_date(self.date)
          # Update the UI with the new date
          self.update_ui()

  def add_product(self):
      product_id = self.open_product_selection()
      

      if product_id is not None:
        # Get the current report's product IDs
        report = self.report  # Assuming self.report holds the current report object
        
        # Check if report has products already
        if report.products:
            try:
                # Try to parse existing product_ids as JSON if it's a string
                if isinstance(report.products, str):
                    
                    current_product_ids = json.loads(report.products)
                else:
                    # Otherwise, assume it's already a list
                    current_product_ids = report.products
                
                # Make sure current_product_ids is a list
                if not isinstance(current_product_ids, list):
                    current_product_ids = [current_product_ids]
                
                # Add the new product ID if it's not already in the list
                if product_id not in current_product_ids:
                    current_product_ids.append(product_id)
                else:
                    QMessageBox.critical(self, "Add failed", "Error: Product already added")
            except Exception as e:
                # If there was a problem parsing the existing product_ids
                print(f"Error processing existing product IDs: {e}")
                current_product_ids = [product_id]  # Start fresh with just the new ID
        else:
            # No existing products, create a new array with the selected product ID
            current_product_ids = [product_id]
        
        # Update the report with the new product_ids array
        
        update_report(current_product_ids, report.id)
        
        # Update the UI to reflect the changes
        self.update_ui()
        

  def open_product_selection(self):
      products = fetch_products()
      dialog = AddProductPopup(products, DynamicTableWidget)
      
      result = dialog.exec_()
      if result == QDialog.Accepted:
          # Get the selected product ID
          selected_id = dialog.get_selected_product_id()
          return selected_id
      
      return None
  
  def remove_product(self):
      pass
  
  def create_report(self):
      pass
  
  def update_ui(self):
      pass

