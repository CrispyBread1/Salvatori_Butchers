from datetime import date
import json
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMessageBox, QDialog
)

from database.products import fetch_products, fetch_products_by_ids
from database.reports import fetch_report_by_id, update_report
from database.stock_sold_reports import fetch_stock_sold_report_by_date, insert_stock_sold_report, update_stock_sold_report
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.components.reusable.date_input_dialog import DateInputDialog
from gui.components.reusable.table import DynamicTableWidget
from gui.components.reusable.product_popup import AddProductPopup
from utils.stock_sold_report_utils import add_product_stock_sold_report, fetch_chosen_dates_invoice_items, fetch_chosen_dates_invoice_items, remove_product_stock_sold_report


class StockSoldReportWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.main_layout = QVBoxLayout()
    self.title_label = QLabel()
    self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
    self.main_layout.addWidget(self.title_label)
    self.loading_manager = LoadingManager(self)
    self.table_widget = DynamicTableWidget(self)
    self.main_layout.addWidget(self.table_widget)
    self.status_label = QLabel("", self)
    self.main_layout.addWidget(self.status_label)
    self.setup_ui()
        
  def setup_ui(self):
      self.date = date.today().strftime('%Y-%m-%d')
      self.report = fetch_report_by_id(1)  
      self.report_products = fetch_products_by_ids(self.report.products)
      self.stock_sold_report = fetch_stock_sold_report_by_date(self.date)
      
      self.title_label.setText(f"Report for: {self.date}")


      self.change_date_button = QPushButton("Change Date", self)
      self.change_date_button.clicked.connect(self.change_date)
      self.create_report_button = QPushButton("Create Report", self)
      self.create_report_button.clicked.connect(self.create_report)
      self.update_report_button = QPushButton("Update Report", self)
      self.update_report_button.clicked.connect(self.create_report)
      self.add_product_button = QPushButton("Add product", self)
      self.add_product_button.clicked.connect(self.add_product)
      self.remove_product_button = QPushButton("Remove product", self)
      self.remove_product_button.clicked.connect(self.remove_product)
      
      self.button_layout = QHBoxLayout()
      self.button_layout.addWidget(self.change_date_button)
      self.button_layout.addWidget(self.create_report_button)
      self.button_layout.addWidget(self.update_report_button)
      self.button_layout.addWidget(self.add_product_button)
      self.button_layout.addWidget(self.remove_product_button)

      if self.stock_sold_report:
          self.create_report_button.hide()
          self.update_report_button.show()
          self.populate_table(self.stock_sold_report.data)
      else:
          self.table_widget.setEnabled(False)

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

      state, message = add_product_stock_sold_report(self.report, product_id)
      QMessageBox.information(
                self, 
                f"{state}", 
                f"{message}!"
            )
        # Update the UI to reflect the changes
      self.update_ui()
        
  def remove_product(self):
      product_id = self.open_product_selection(True)

      state, message = remove_product_stock_sold_report(self.report, product_id)
      QMessageBox.information(
                self, 
                f"{state}", 
                f"{message}!"
            )
        # Update the UI to reflect the changes
      self.update_ui()
      

  def open_product_selection(self, remove=None):
      if remove:
          dialog = AddProductPopup(self.report_products, DynamicTableWidget)
      else:
          products = fetch_products()
          dialog = AddProductPopup(products, DynamicTableWidget)
      
      result = dialog.exec_()
      if result == QDialog.Accepted:
          # Get the selected product ID
          selected_id = dialog.get_selected_product_id()
          return selected_id
      
      return None
  
  
  def create_report(self):
      # products_sage_codes = create_sage_codes_array(self.report_products)
      # Disable the button to prevent multiple clicks
      self.create_report_button.setEnabled(False)  # Fixed: was using general_settings_button
      # Use the loading manager to run the get_invoice_products function with a loading animation
      self.loading_manager.run_with_loading(
          task_function=fetch_chosen_dates_invoice_items,  # Direct call to your function
          on_complete=self.on_fetch_complete,
          on_error=self.on_fetch_error,
          on_pause=self.handle_pause,
          loading_text="Fetching invoice data...",
          title="Loading Invoices",
          task_args=(self.date, self.report_products,)
      )
    
  def on_fetch_complete(self, product_sold_data, updated_at, original_id=None):
      # Re-enable button
      self.create_report_button.setEnabled(True)  # Fixed: was using general_settings_button
      # Update status with results
      if product_sold_data:
          self.status_label.setText(f"Successfully created {self.date} product report.")
          if self.stock_sold_report:
              update_stock_sold_report(self.stock_sold_report.id, product_sold_data, updated_at)
          else:
              insert_stock_sold_report(self.date, product_sold_data)
              
          self.update_ui()
      else:
          self.status_label.setText("No invoices found for the selected date.")

      # self.date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
  
  def on_fetch_error(self, error_message):
      # Re-enable button
      self.create_report_button.setEnabled(True)  # Fixed: was using general_settings_button
      
      # Show error message
      print(error_message)
      self.status_label.setText(f"Error fetching invoices: {error_message}")

  def handle_pause(self):
      pass
  
  def populate_table(self, product_sold_data=None):
      if product_sold_data:
          headers = ["Name", "Quantity Sold"]
          data = []

          for key, value in product_sold_data.items():
              row_data = [key, value]
              data.append(row_data)
          self.table_widget.setEnabled(True)
          self.table_widget.populate(headers, data)
      else:
        # Clear and hide the table if no data
        self.table_widget.table.clear()
        self.table_widget.setEnabled(False)
        self.table_widget.table.setRowCount(0)
        self.table_widget.table.setColumnCount(0)

  def update_ui(self):
      self.report = fetch_report_by_id(1)
      self.report_products = fetch_products_by_ids(self.report.products)
      self.stock_sold_report = fetch_stock_sold_report_by_date(self.date)
      self.title_label.setText(f"Report for: {self.date}")
      if self.stock_sold_report:
          self.create_report_button.hide()
          self.update_report_button.show()
          self.populate_table(self.stock_sold_report.data)
      else:
          self.create_report_button.show()
          self.update_report_button.hide()    
          self.populate_table()

