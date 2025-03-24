from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class StockTakeViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Take View")
        self.setGeometry(100, 100, 800, 600)  # Set window size

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.content_layout = QVBoxLayout(central_widget)

        # Initialize the table
        self.table = QTableWidget()
        self.content_layout.addWidget(self.table)

        # Set up the table structure
        self.setup_table()

    def setup_table(self):
        """Set up the table with weekday headers and empty cells for stock take."""
        
        # Define headers for Monday to Friday
        headers = ["Product Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Placeholder: Replace this with actual product data retrieval
        products = [
            "Product A", 
            "Product B", 
            "Product C"
        ]  # TODO: Fetch product list dynamically

        self.table.setRowCount(len(products))

        # Populate the table with product names and empty cells for stock takes
        for row_idx, product in enumerate(products):
            # Set the product name in the first column
            self.table.setItem(row_idx, 0, QTableWidgetItem(product))

            # Create empty cells for stock take (Monday to Friday)
            for col_idx in range(1, len(headers)):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(""))  # Empty by default


