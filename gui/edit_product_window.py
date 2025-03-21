from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QPushButton, QLabel, QTableWidget, QDateEdit,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QGridLayout, QMessageBox
)
from database.products import fetch_products_stock_take, update_product, fetch_products
from database.stock_takes import insert_stock_take, fetch_most_recent_stock_take
from datetime import datetime

class EditProductWindow(QMainWindow):
  products = {}
  form_loaded = False
  categories = ['fresh', 'dry', 'frozen']

  def __init__(self):
    super().__init__()
    self.products = self.sort_products(fetch_products())
    print(self.products)

    self.setWindowTitle('Product Window')

    central_widget = QWidget()
    self.setCentralWidget(central_widget)  

    layout = QVBoxLayout(central_widget)

    self.resize(1200, 800)

    # Label for product window
    self.label = QLabel("Products", self)
    layout.addWidget(self.label)

    self.table_button = QPushButton("Reload List", self)
    self.table_button.clicked.connect(self.reload_list)
    layout.addWidget(self.table_button)

    # Create Table Widget
    self.table = QTableWidget()
    layout.addWidget(self.table)

    self.label = QLabel("")
    layout.addWidget(self.label) 

    # self.table.itemChanged.connect(self.collect_changes)
    self.load_product_table()

  def load_product_table(self):    
    if self.products:
      headers = ["Name", "Stock Cost Per K/C/B £", "Stock Count", "Selling Price Per K/C/B £", "Stock Category",  "Product Category", "Sage Code(s)", "Supplier", "Sold As"]
    
      self.table.setRowCount(len(self.products))
      self.table.setColumnCount(len(headers))
      self.table.setHorizontalHeaderLabels(headers)

      # Populate table
      for row_idx, product in enumerate(self.products):
          for col_idx in range(len(headers)):
              if col_idx == 0:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.name)))
              elif col_idx == 1:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.cost)))
              elif col_idx == 2:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_count)))
              elif col_idx == 3:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.product_value)))
              elif col_idx == 4:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_category)))
              elif col_idx == 5:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.product_category)))
              elif col_idx == 6:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.sage_code)))
              elif col_idx == 7:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.supplier)))
              else:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.sold_as)))
      # self.table.itemChanged.connect(self.collect_changes)
      self.table.resizeColumnsToContents()  # Auto resize columns
    else:
      self.label.setText("Data has not been found")

  def reload_list(self):
    self.products = self.sort_products(fetch_products())
    self.load_product_table()

  def collect_changes(self, item):
    row_idx = item.row()  
    col_idx = item.column() 

    # Retrieve the product object associated with this row
    product = self.products[row_idx]

    # Check if you're updating the correct field in the Product object
    if col_idx == 1:  
        product.stock_count = float(item.text())
    elif col_idx == 2:  
        product.cost = float(item.text())
    elif col_idx == 4:
        product.stock_category = item.text()
    elif col_idx == 5: 
        product.product_value = float(item.text())

  def new_product(self):
    return
  
  def sort_products(self, fetched_products):
     print(sorted(fetched_products, key=lambda product: (product.stock_category, product.name)))
     return sorted(fetched_products, key=lambda product: (product.stock_category, product.name))
  
  # json.dumps(updated_data)/
