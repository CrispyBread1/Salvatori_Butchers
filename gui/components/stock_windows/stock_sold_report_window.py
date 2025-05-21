from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QDialog
)

from database.products import fetch_products
from gui.components.reusable.date_input_dialog import DateInputDialog
from gui.components.reusable.table import DynamicTableWidget
from gui.components.stock_windows.stock_sold.add_product_popup import AddProductPopup


class StockSoldReportWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.setup_ui()
        
  def setup_ui(self):
      layout = QVBoxLayout()
      
      # Title
      # title = QLabel("Stock Sold Report")
      # title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
      # layout.addWidget(title)

      self.change_date_button = QPushButton("Change Date", self)
      self.change_date_button.clicked.connect(self.change_date)
      self.add_product_button = QPushButton("Add product", self)
      self.add_product_button.clicked.connect(self.open_product_selection)
      self.remove_product_button = QPushButton("Remove product", self)
      self.remove_product_button.clicked.connect(self.remove_product)
      
      self.button_layout = QHBoxLayout()
      self.button_layout.addWidget(self.change_date_button)
      self.button_layout.addWidget(self.add_product_button)
      self.button_layout.addWidget(self.remove_product_button)


      layout.addLayout(self.button_layout)
    
      self.setLayout(layout)


  def change_date(self):
      # Open date input dialog
      dialog = DateInputDialog(self)
      if dialog.exec_():  # If user clicks OK
          self.date = dialog.get_just_date()
          # self.butchers_lists = fetch_all_butchers_lists_by_date(self.date)
          # Update the UI with the new date
          self.update_ui()

  def open_product_selection(self):
      products = fetch_products()
      dialog = AddProductPopup(products, DynamicTableWidget)
      
      # Connect to the product_selected signal if you want to handle the selection in a callback
      dialog.product_selected.connect(lambda product_id: print(f"Selected product ID: {product_id}"))
      
      result = dialog.exec_()
      if result == QDialog.Accepted:
          # Get the selected product ID
          selected_id = dialog.get_selected_product_id()
          print(f"Dialog returned product ID: {selected_id}")
          return selected_id
      return None
  
  def remove_product(self):
     pass
