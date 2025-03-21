from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QMainWindow, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from database.products import update_product

class ProductDetailWindow(QMainWindow):
    def __init__(self, products, current_index, parent=None):
        super().__init__(parent)
        self.products = products
        self.current_index = current_index

        self.setWindowTitle("Product Details")
        self.resize(500, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        # Editable fields (QLineEdits) with labels
        self.name_label = QLabel("Product Name:")
        self.layout.addWidget(self.name_label)
        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self.products[self.current_index].name)
        self.layout.addWidget(self.name_edit)

        self.cost_label = QLabel("Stock Cost (£):")
        self.layout.addWidget(self.cost_label)
        self.cost_edit = QLineEdit(self)
        self.cost_edit.setText(str(self.products[self.current_index].cost))
        self.layout.addWidget(self.cost_edit)

        self.product_value_label = QLabel("Selling Price (£):")
        self.layout.addWidget(self.product_value_label)
        self.product_value_edit = QLineEdit(self)
        self.product_value_edit.setText(str(self.products[self.current_index].product_value))
        self.layout.addWidget(self.product_value_edit)

        self.stock_category_label = QLabel("Stock Category:")
        self.layout.addWidget(self.stock_category_label)
        self.stock_category_edit = QLineEdit(self)
        self.stock_category_edit.setText(self.products[self.current_index].stock_category)
        self.layout.addWidget(self.stock_category_edit)

        self.product_category_label = QLabel("Product Category:")
        self.layout.addWidget(self.product_category_label)
        self.product_category_edit = QLineEdit(self)
        self.product_category_edit.setText(self.products[self.current_index].product_category)
        self.layout.addWidget(self.product_category_edit)

        self.sage_code_label = QLabel("Sage Code:")
        self.layout.addWidget(self.sage_code_label)
        self.sage_code_edit = QLineEdit(self)
        self.sage_code_edit.setText(self.products[self.current_index].sage_code)
        self.layout.addWidget(self.sage_code_edit)

        self.supplier_label = QLabel("Supplier:")
        self.layout.addWidget(self.supplier_label)
        self.supplier_edit = QLineEdit(self)
        self.supplier_edit.setText(self.products[self.current_index].supplier)
        self.layout.addWidget(self.supplier_edit)

        self.sold_as_label = QLabel("Sold As:")
        self.layout.addWidget(self.sold_as_label)
        self.sold_as_edit = QLineEdit(self)
        self.sold_as_edit.setText(self.products[self.current_index].sold_as)
        self.layout.addWidget(self.sold_as_edit)

        # Navigation Buttons
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_product)
        self.layout.addWidget(self.next_button)

        self.prev_button = QPushButton("Previous", self)
        if self.current_index < 1:
          self.prev_button.setEnabled(False)
        else:
           self.prev_button.setEnabled(True)
        self.prev_button.clicked.connect(self.prev_product)
        self.layout.addWidget(self.prev_button)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.setStyleSheet("""
          QPushButton {
            background-color: #007BFF;  /* Blue background */
            color: white;               /* White text */
            border: 1px solid #0056b3;  /* Darker blue border */
            padding: 5px 10px;          /* Padding for better appearance */
            border-radius: 4px;         /* Rounded corners */
          }

          QPushButton:hover {
            background-color: #0056b3;  /* Darker blue when hovered */
          }

          QPushButton:pressed {
            background-color: #003d73;  /* Even darker blue when pressed */
          }
        """)
        self.save_button.clicked.connect(self.save_product)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_edit)
        self.layout.addWidget(self.cancel_button)

    def prev_product(self):
        """Navigate to the previous product."""
        print(self.current_index)
        if self.current_index > 1:
            self.current_index -= 1
            self.load_product()
            self.prev_button.setEnabled(True)
        else:
          self.prev_button.setEnabled(False)

    def next_product(self):
        """Navigate to the next product."""
        if self.current_index < len(self.products) - 1:
          self.current_index += 1
          self.load_product()
          self.prev_button.setEnabled(True)
        else:
          self.prev_button.setEnabled(False)

    def save_product(self):
        """Save edited product back to the database."""
        product = self.products[self.current_index]
        product.name = self.name_edit.text()
        product.cost = float(self.cost_edit.text())
        product.product_value = float(self.product_value_edit.text())
        product.stock_category = self.stock_category_edit.text()
        product.product_category = self.product_category_edit.text()
        product.sage_code = self.sage_code_edit.text()
        product.supplier = self.supplier_edit.text()
        product.sold_as = self.sold_as_edit.text()

        update_product(product)
        QMessageBox.information(self, "Success", "Product updated successfully!")

    def cancel_edit(self):
        """Cancel the editing of the product."""
        self.load_product()

    def load_product(self):
        """Load the selected product details into editable fields."""
        product = self.products[self.current_index]
        self.name_edit.setText(product.name)
        self.cost_edit.setText(str(product.cost))
        self.product_value_edit.setText(str(product.product_value))
        self.stock_category_edit.setText(product.stock_category)
        self.product_category_edit.setText(product.product_category)
        self.sage_code_edit.setText(product.sage_code)
        self.supplier_edit.setText(product.supplier)
        self.sold_as_edit.setText(product.sold_as)
