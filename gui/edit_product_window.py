from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QPushButton, QLabel, QTableWidget, QVBoxLayout,
    QMainWindow, QMessageBox
)
from database.products import fetch_products, update_product
from gui.product_detail_window import ProductDetailWindow
from datetime import datetime

class EditProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.products = self.sort_products(fetch_products())
        self.setWindowTitle('Product Window')

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        self.layout = QVBoxLayout(central_widget)
        self.resize(1200, 800)

        # Title Label
        self.label = QLabel("Products", self)
        self.layout.addWidget(self.label)

        # Reload Button (Above the Table)
        self.table_button = QPushButton("Reload List", self)
        self.table_button.clicked.connect(self.reload_list)
        self.layout.addWidget(self.table_button)

        # Product Table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Load Data
        self.load_product_table()

    def load_product_table(self):
        """Load product data into the table (Hardcoded Columns)."""
        if not self.products:
            self.label.setText("No data found.")
            return

        # Set headers manually (matching database fields)
        headers = ["Name", "Stock Cost £", "Stock Count", "Selling Price £", "Stock Category", "Product Category", "Sage Code", "Supplier", "Sold As"]

        self.table.setRowCount(len(self.products))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # self.table.setStyleSheet("""
        #   QTableWidget::item:hover {
        #     background-color: #B0C4DE;  # Lighter Blue color for hover
        #   }
        # """)

        # Populate Table (No Looping for Field Mapping)
        for row_idx, product in enumerate(self.products):
          # Product Name: Styled to look like a button (Blue and Underlined)
          name_item = QTableWidgetItem(str(product.name))
          name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
          name_item.setTextAlignment(Qt.AlignCenter)
          name_item.setForeground(Qt.blue)  # Blue text
          font = QFont()
          font.setUnderline(True)  # Underline the text
          name_item.setFont(font)
          self.table.setItem(row_idx, 0, name_item)
          
          self.table.setItem(row_idx, 1, QTableWidgetItem(str(product.cost)))
          
          # Stock Count should be read-only
          stock_count_item = QTableWidgetItem(str(product.stock_count))
          stock_count_item.setFlags(stock_count_item.flags() & ~Qt.ItemIsEditable)
          self.table.setItem(row_idx, 2, stock_count_item)
          
          self.table.setItem(row_idx, 3, QTableWidgetItem(str(product.product_value)))
          self.table.setItem(row_idx, 4, QTableWidgetItem(str(product.stock_category)))
          self.table.setItem(row_idx, 5, QTableWidgetItem(str(product.product_category)))
          self.table.setItem(row_idx, 6, QTableWidgetItem(str(product.sage_code)))
          self.table.setItem(row_idx, 7, QTableWidgetItem(str(product.supplier)))
          self.table.setItem(row_idx, 8, QTableWidgetItem(str(product.sold_as)))

          # Make the product name clickable (opens detailed edit)
          self.table.item(row_idx, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.table.itemChanged.connect(self.cell_edited)
        self.table.cellDoubleClicked.connect(self.open_product_detail)
        self.table.resizeColumnsToContents()

    def reload_list(self):
        """Reload the product list from the database."""
        self.products = self.sort_products(fetch_products())
        self.load_product_table()

    def cell_edited(self, item):
        """Show Save button next to the changed cell."""
        row_idx = item.row()
        col_idx = item.column()

        if col_idx == 2:  # Stock Count should not be editable
            return

        # Remove previous Save button if it exists
        if hasattr(self, 'save_button'):
            self.save_button.deleteLater()

        # Create and show Save button next to the cell that was edited
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(lambda: self.save_product(row_idx))
        self.layout.addWidget(self.save_button)
        self.save_button.show()

    def save_product(self, row_idx):
        """Save changes of a specific row to the database."""
        product = self.products[row_idx]

        # Manually assign values (hardcoded mapping)
        product.name = self.table.item(row_idx, 0).text()
        product.cost = float(self.table.item(row_idx, 1).text())
        product.product_value = float(self.table.item(row_idx, 3).text())
        product.stock_category = self.table.item(row_idx, 4).text()
        product.product_category = self.table.item(row_idx, 5).text()
        product.sage_code = self.table.item(row_idx, 6).text()
        product.supplier = self.table.item(row_idx, 7).text()
        product.sold_as = self.table.item(row_idx, 8).text()

        update_product(product)  # Save changes to DB

        QMessageBox.information(self, "Success", "Product updated successfully!")
        self.save_button.deleteLater()
        del self.save_button

    def open_product_detail(self, row_idx, col_idx):
        """Open detailed product edit window when clicking on Name."""
        if col_idx == 0:
            self.product_detail_window = ProductDetailWindow(self.products, row_idx, self)
            self.product_detail_window.show()

    def sort_products(self, fetched_products):
        """Sort products by category & name."""
        return sorted(fetched_products, key=lambda product: (product.stock_category, product.name))
