import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models.product import Product

class ProductWindow(QWidget):
    rows = []

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

        # Set up layout for product window
        self.setLayout(layout)


    def load_data(self):
        """Fetches product data from the database and fills the table."""
        if not self.rows:
          connection = sqlite3.connect("salvatori_butchers.db")  # Ensure this is the correct database path
          cursor = connection.cursor()

          # Get all products
          cursor.execute("SELECT name, cost, stock_count, product_value, product_category, sold_as FROM products")
          self.rows = [Product(*product) for product in cursor.fetchall()]
          connection.close()

          # Define column headers
          headers = ["Name", "Stock", "Price Per K/C/B", "Total Cost", "Stock Category", "Total Profit"]


        # Set table row & column count
        self.table.setRowCount(len(self.rows))
        self.table.setColumnCount(len(headers))

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
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.product_value)))
                elif col_idx == 3:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_product_cost())))
                elif col_idx == 4:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_category)))
                else:
                  self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_product_cost())))



        self.table.resizeColumnsToContents()  # Auto resize columns

    def reload_list(self):
      self.load_data()
