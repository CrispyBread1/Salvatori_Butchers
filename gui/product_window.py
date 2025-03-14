import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem

class ProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Window')

        # Layout for product window
        layout = QVBoxLayout()

        # Label for product window
        label = QLabel("Product List", self)
        layout.addWidget(label)

        # Create Table Widget
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Load Data from Database
        self.load_data()

        # Set up layout for product window
        self.setLayout(layout)


    def load_data(self):
        """Fetches product data from the database and fills the table."""
        connection = sqlite3.connect("salvatori_butchers.db")  # Ensure this is the correct database path
        cursor = connection.cursor()

        # Get all products
        cursor.execute("SELECT name, cost, stock_count, product_value, stock_category, sold_as FROM products")
        rows = cursor.fetchall()
        connection.close()

        # Define column headers
        headers = ["Name", "Stock", "Price Per K/C/B", "Total Cost", "Stock Category", "Total Profit"]

        # Set table row & column count
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers))

        # Set column headers
        self.table.setHorizontalHeaderLabels(headers)

        # Populate table
        for row_idx, row in enumerate(rows):
            for col_idx in range(len(headers)):
                stock_cost = row[1] 
                stock_count = row[2] 
                product_value = row[3]  
                if col_idx == 3:
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(stock_cost * stock_count)))
                elif col_idx == 5:  # "Total Profit" column (calculated value)
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(stock_count * product_value)))
                else:
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(row[col_idx])))



        self.table.resizeColumnsToContents()  # Auto resize columns
