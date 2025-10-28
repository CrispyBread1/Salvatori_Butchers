from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QLineEdit, 
    QDialogButtonBox, QFormLayout, QMessageBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from database.products import insert_product
from utils.butchers_list_utils import add_product_supabase


class AddProductDialog(QDialog):
    def __init__(self, sage_code=None, product_description=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Missing Product")
        self.sage_code = sage_code
        self.product_description = product_description
        self.product_data = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Fields
        self.sage_code_input = QLineEdit(self)
        self.sage_code_input.setText(self.sage_code or "")

        self.product_name_input = QLineEdit(self)
        self.product_name_input.setText(self.product_description or "")

        self.stock_category_input = QComboBox(self)
        self.stock_category_input.addItems(["fresh", "frozen", "dry"])

        self.sold_as_input = QComboBox(self)
        self.sold_as_input.addItems(["bag", "kilo", "case"])

        self.price_input = QLineEdit(self)

        form.addRow("Sage Code:", self.sage_code_input)
        form.addRow("Product Name:", self.product_name_input)
        form.addRow("Category:", self.stock_category_input)
        form.addRow("Sold As:", self.sold_as_input)
        form.addRow("Price:", self.price_input)

        layout.addLayout(form)

        # Buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.handle_submit)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def handle_submit(self):
        """Handles saving to DB internally and closes with result."""
        sage_code = self.sage_code_input.text().strip()
        name = self.product_name_input.text().strip()
        category = self.stock_category_input.currentText().strip()
        sold_as = self.sold_as_input.currentText().strip()
        price_text = self.price_input.text().strip()

        # Validation
        if not sage_code or not name:
            QMessageBox.warning(self, "Missing Info", "Please fill in Sage Code and Product Name.")
            return

        # Convert price safely
        try:
            price = float(price_text) if price_text else 0
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid price.")
            return

        # Insert into DB
        try:
            add_product_supabase(name, price, 0, 0, category, None, sage_code, None, sold_as)
            self.accept()  # Closes the dialog with success

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add product:\n{e}")
            self.reject()
