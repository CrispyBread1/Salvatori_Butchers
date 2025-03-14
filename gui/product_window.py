import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models.product import Product

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
        # if self.table.itemChanged in self.table.__dict__.get('signals', {}).get('itemChanged', []):
        #   self.table.itemChanged.disconnect(self.collect_changes)

        """Fetches product data from the database and fills the table."""
        if not self.rows:
          connection = sqlite3.connect("salvatori_butchers.db")  # Ensure this is the correct database path
          cursor = connection.cursor()

          # Get all products
          cursor.execute("SELECT id, name, cost, stock_count, product_value, product_category, sold_as FROM products")
          self.rows = [Product(*product) for product in cursor.fetchall()]
          connection.close()

          # Define column headers
          

        headers = ["Name", "Stock", "Price Per K/C/B £", "Total Cost £", "Stock Category", "Total Profit £"]
        # Set table row & column count
      
        self.table.setRowCount(len(self.rows))
        self.table.setColumnCount(len(headers))
        self.table.clearContents()
        # Set column headers
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
                else:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_product_cost())))


        # self.table.itemChanged.connect(self.collect_changes)
        self.table.resizeColumnsToContents()  # Auto resize columns

    def reload_list(self):
      self.load_data()

    def collect_changes(self, item):
      row_idx = item.row()  
      col_idx = item.column() 

      # Retrieve the product object associated with this row
      product = self.rows[row_idx]
      print("item: " + str(item) + " col_idx: " + str(col_idx))
      # Check if you're updating the correct field in the Product object
      if col_idx == 1:  # Example: Update stock count
          print("col_idx 1:" + str(item.text()))
          product.stock_count = float(item.text())
      elif col_idx == 2:  # Example: Update product value
          print("col_idx 2:" + str(item.text()))
          product.cost = float(item.text())
      elif col_idx == 4:  # Example: Update stock category
          print("col_idx 4:" + str(item.text()))
          product.stock_category = item.text()

      print("Product: " + product.name + "Product stock: " + str(product.stock_count) + "Total Product cost: " + str(product.total_product_cost()) + "Product price: " + str(product.cost) + " Total Product Price: " + str(product.total_product_cost()))

