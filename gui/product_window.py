from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models.product import Product
from database.products import fetch_products

class ProductWindow(QWidget):
    rows = []
    changed_data = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Window')

        # Layout for product window
        layout = QVBoxLayout()
        self.resize(1200, 800)

        # Label for product window
        label = QLabel("Product List", self)
        layout.addWidget(label)

        # Create Table Widget
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Load Data from Database
        self.load_data()

        self.table_button = QPushButton("Reload List", self)
        self.table_button.clicked.connect(self.reload_list)

        self.table.itemChanged.connect(self.collect_changes)

        # Set up layout for product window
        self.setLayout(layout)


    def load_data(self):
        if not self.rows:
          # Get all products
          data = fetch_products()
          self.rows = [Product(*product) for product in data]         

        headers = ["Name", "Stock", "Stock Cost Per K/C/B £", "Total Cost £", "Stock Category", "Selling Price Per K/C/B £",  "Total Profit £"]
        # Set table row & column count
      
        self.table.setRowCount(len(self.rows))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Populate table
        for row_idx, product in enumerate(self.rows):
            for col_idx in range(len(headers)):
                if col_idx == 0:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.name)))
                elif col_idx == 1:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_count)))
                elif col_idx == 2:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.cost)))
                elif col_idx == 3:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_product_cost())))
                elif col_idx == 4:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_category)))
                elif col_idx == 5:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.product_value)))
                else:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_profit())))


        # self.table.itemChanged.connect(self.collect_changes)
        self.table.resizeColumnsToContents()  # Auto resize columns

    def reload_list(self):
      self.load_data()

    def collect_changes(self, item):
      row_idx = item.row()  
      col_idx = item.column() 

      # Retrieve the product object associated with this row
      product = self.rows[row_idx]

      # Check if you're updating the correct field in the Product object
      if col_idx == 1:  
          product.stock_count = float(item.text())
      elif col_idx == 2:  
          product.cost = float(item.text())
      elif col_idx == 4:
          product.stock_category = item.text()
      elif col_idx == 5: 
          product.product_value = float(item.text())

