import json
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow, QLineEdit, QMessageBox, QHBoxLayout, QComboBox
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

        # self.stock_category_label = QLabel("Stock Category:")
        # self.layout.addWidget(self.stock_category_label)
        # self.stock_category_edit = QComboBox(self)
        # self.stock_category_edit.setText(self.products[self.current_index].stock_category)
        # self.layout.addWidget(self.stock_category_edit)
        self.stock_category_label = QLabel("Stock Category:")
        self.layout.addWidget(self.stock_category_label)
        self.stock_category_combo = QComboBox(self)
        stock_categories = ["dry", "fresh", "frozen"]
        self.stock_category_combo.addItems(stock_categories)

        # Set the current index based on the product's stock category
        current_category = self.products[self.current_index].stock_category
        self.stock_category_combo.setCurrentText(current_category)
        self.layout.addWidget(self.stock_category_combo)

        self.product_category_label = QLabel("Product Category:")
        self.layout.addWidget(self.product_category_label)
        self.product_category_edit = QLineEdit(self)
        self.product_category_edit.setText(self.products[self.current_index].product_category)
        self.layout.addWidget(self.product_category_edit)

        # Sage Code
        self.sage_code_label = QLabel("Sage Code(s):")
        self.layout.addWidget(self.sage_code_label)

        # Create a layout specifically for the Sage Code inputs
        self.sage_code_layout = QVBoxLayout()
        
        # Original Sage Code field

        sage_code = self.products[self.current_index].sage_code
        sage_codes = []

        if sage_code and not isinstance(sage_code, str):
            sage_codes = json.loads(sage_code)
        elif sage_code and isinstance(sage_code, str):
            sage_codes.append(sage_code)
   
        
        self.sage_code_inputs = []  # List to hold the QLineEdit inputs
        self.delete_buttons = []  # List to hold the delete buttons

        for sage_code in sage_codes:
            self.add_sage_code_input(sage_code)

        # Add the Sage Code layout to the main layout
        self.layout.addLayout(self.sage_code_layout)

        # Add Another Code Button
        self.add_code_button = QPushButton("Add Another Code", self)
        self.add_code_button.clicked.connect(self.add_sage_code_input)
        self.layout.addWidget(self.add_code_button)

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

    def add_sage_code_input(self, sage_code=""):
        """Dynamically adds another Sage Code input and delete button under the first one"""
        # Ensure sage_code is a string
        if not isinstance(sage_code, str):
            sage_code = ""  # If not a string, default to an empty string

        # Create a new QLineEdit for another Sage Code
        new_sage_code_edit = QLineEdit(self)
        new_sage_code_edit.setText(sage_code)  # Set the text to the valid string
        self.sage_code_layout.addWidget(new_sage_code_edit)

        # Create the delete button for this QLineEdit
        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(lambda: self.delete_sage_code_input(new_sage_code_edit, delete_button))

        # Layout to keep the QLineEdit and delete button in the same row
        h_layout = QHBoxLayout()
        h_layout.addWidget(new_sage_code_edit)
        h_layout.addWidget(delete_button)

        # Add the row (QHBoxLayout) to the Sage Code layout
        self.sage_code_layout.addLayout(h_layout)

        # Add the new QLineEdit and delete button to the lists
        self.sage_code_inputs.append(new_sage_code_edit)
        self.delete_buttons.append(delete_button)

    def delete_sage_code_input(self, line_edit, delete_button):
        """Deletes the given line edit and delete button"""
        self.sage_code_layout.removeWidget(line_edit)
        self.sage_code_layout.removeWidget(delete_button)
        line_edit.deleteLater()
        delete_button.deleteLater()

        # Remove the line edit and delete button from the lists
        self.sage_code_inputs.remove(line_edit)
        self.delete_buttons.remove(delete_button)

    def prev_product(self):
        """Navigate to the previous product."""
        if self.current_index > 0:
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

        # Save all the Sage Codes from the dynamic fields
        sage_codes = [sage_code.text() for sage_code in self.sage_code_inputs]
        product.sage_code = json.dumps(sage_codes)

        product.supplier = self.supplier_edit.text()
        product.sold_as = self.sold_as_edit.text()

        update_product(product.id, name=product.name, cost=product.cost, 
                       product_value=product.product_value, stock_category=product.stock_category, product_category=product.product_category, 
                       sage_code=product.sage_code, supplier=product.supplier, sold_as=product.sold_as)
        QMessageBox.information(self, "Success", "Product updated successfully!")


    def load_product(self):
        """Load the selected product details into editable fields."""
        product = self.products[self.current_index]
        self.name_edit.setText(product.name)
        self.cost_edit.setText(str(product.cost))
        self.product_value_edit.setText(str(product.product_value))
        self.stock_category_combo.setCurrentText(product.stock_category)
        self.product_category_edit.setText(product.product_category)

        # Clear existing sage code inputs and delete buttons
        for sage_code_input, delete_button in zip(self.sage_code_inputs[:], self.delete_buttons[:]):
            self.delete_sage_code_input(sage_code_input, delete_button)
        
        self.sage_code_inputs.clear()
        self.delete_buttons.clear()

        # Populate the Sage Code fields
        sage_code = self.products[self.current_index].sage_code
        sage_codes = []
        
        if sage_code:
            try:
                if isinstance(sage_code, str):
                    # Try to parse as JSON first
                    try:
                        sage_codes = json.loads(sage_code)
                        if not isinstance(sage_codes, list):
                            sage_codes = [str(sage_codes)]
                    except json.JSONDecodeError:
                        # If not valid JSON, treat as a single string
                        sage_codes = [sage_code]
                else:
                    # If not a string, convert to string
                    sage_codes = [str(sage_code)]
                    
                # Add each sage code to the UI
                for code in sage_codes:
                    self.add_sage_code_input(code)
                    
            except Exception as e:
                print(f"Error processing sage_code: {e}")
                # Add a blank input if there was an error
                self.add_sage_code_input("")
        else:
            # Add a blank input if there's no sage code
            self.add_sage_code_input("")

        self.supplier_edit.setText(product.supplier)
        self.sold_as_edit.setText(product.sold_as)
