from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QDialog, 
    QHeaderView, QAbstractItemView, QHBoxLayout, QTableWidgetItem,
    QLineEdit, QComboBox, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QDoubleValidator

class EditProductsListPopup(QDialog):
    # Signal to emit when changes are saved - returns (column1_value, column2_value, products_list)
    data_updated = pyqtSignal(float, float, list)
    
    def __init__(self, column1_value, column2_value, current_products, available_products, dynamic_table_widget_class, parent=None):
        """
        Initialize the product list editor popup.
        
        Args:
            column1_value: Initial value for column 1 (e.g., 18)
            column2_value: Initial value for column 2 (e.g., 28.5)
            current_products: List of current product objects
            available_products: List of all available product objects to choose from
            dynamic_table_widget_class: The DynamicTableWidget class to use
            parent: Parent widget
        """
        super().__init__(parent)
        self.column1_value = column1_value
        self.column2_value = column2_value
        self.current_products = current_products.copy() if current_products else []
        self.available_products = available_products
        self.DynamicTableWidget = dynamic_table_widget_class
        
        self.setWindowTitle("Edit Products List")
        self.setFixedSize(1000, 700)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title label
        title_label = QLabel("Edit Product List")
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title_label.setFont(font)
        main_layout.addWidget(title_label)
        
        # Column values section
        column_layout = QFormLayout()
        
        # Column 1 input
        self.column1_input = QLineEdit()
        self.column1_input.setText(str(self.column1_value))
        self.column1_input.setValidator(QDoubleValidator())
        column_layout.addRow("Column 1:", self.column1_input)
        
        # Column 2 input
        self.column2_input = QLineEdit()
        self.column2_input.setText(str(self.column2_value))
        self.column2_input.setValidator(QDoubleValidator())
        column_layout.addRow("Column 2:", self.column2_input)
        
        main_layout.addLayout(column_layout)
        
        # Separator
        separator = QLabel()
        separator.setStyleSheet("background-color: #ccc; max-height: 2px;")
        main_layout.addWidget(separator)
        
        # Products section label
        products_label = QLabel("Products in List:")
        products_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(products_label)
        
        # Search and Add section
        add_section = QHBoxLayout()
        
        search_label = QLabel("Add Product:")
        self.search_combo = QComboBox()
        self.search_combo.setEditable(True)
        self.search_combo.setInsertPolicy(QComboBox.NoInsert)
        
        # Populate combo with available products
        self.search_combo.addItem("-- Select Product --", None)
        for product in self.available_products:
            self.search_combo.addItem(f"{product.name} ({product.sage_code})", product)
        
        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_product)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: 1px solid #0056b3;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        add_section.addWidget(search_label)
        add_section.addWidget(self.search_combo, stretch=1)
        add_section.addWidget(add_button)
        
        main_layout.addLayout(add_section)
        
        # Create the dynamic table widget
        self.dynamic_table_widget = self.DynamicTableWidget(self)
        main_layout.addWidget(self.dynamic_table_widget)
        
        # Get reference to the internal table
        self.table = self.dynamic_table_widget.table
        
        # Configure table behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Remove button
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_product)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: 1px solid #BD2130;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #BD2130;
            }
        """)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        save_button.setDefault(True)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: 1px solid #218838;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        button_layout.addWidget(remove_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        
        main_layout.addLayout(button_layout)
        
        # Load current products
        self.load_product_table()
        
    def load_product_table(self):
        """Load product data into the table."""
        headers = ["ID", "Product Name", "Sage Code", "Supplier", "Category"]
        
        data = []
        for product in self.current_products:
            row_data = [
                product.id,
                product.name,
                product.sage_code,
                product.supplier if hasattr(product, 'supplier') else '',
                product.product_category if hasattr(product, 'product_category') else ''
            ]
            data.append(row_data)
        
        def format_cell(item, row_idx, col_idx, value):
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            return item
        
        self.dynamic_table_widget.populate(headers, data, format_cell)
    
    def add_product(self):
        """Add a new product to the list."""
        current_index = self.search_combo.currentIndex()
        if current_index <= 0:
            QMessageBox.warning(self, "No Product Selected", "Please select a product to add.")
            return
        
        product = self.search_combo.currentData()
        
        # Check if product already exists in the list
        for existing_product in self.current_products:
            if existing_product.id == product.id:
                QMessageBox.warning(self, "Duplicate Product", "This product is already in the list.")
                return
        
        # Add product
        self.current_products.append(product)
        
        # Reload table
        self.load_product_table()
        
        # Reset combo box
        self.search_combo.setCurrentIndex(0)
    
    def remove_product(self):
        """Remove the selected product from the list."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a product to remove.")
            return
        
        selected_row = selected_items[0].row()
        product_id = int(self.table.item(selected_row, 0).text())
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            "Are you sure you want to remove this product?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from current_products list
            self.current_products = [
                product for product in self.current_products 
                if product.id != product_id
            ]
            
            # Reload table
            self.load_product_table()
    
    def save_changes(self):
        """Save changes and close the dialog."""
        # Validate column inputs
        try:
            col1 = float(self.column1_input.text())
            col2 = float(self.column2_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for Column 1 and Column 2.")
            return
        
        # Update values
        self.column1_value = col1
        self.column2_value = col2
        
        # Emit signal with updated data
        self.data_updated.emit(self.column1_value, self.column2_value, self.current_products)
        self.accept()
    
    def get_data(self):
        """Return the updated data as a tuple (column1, column2, products_list)."""
        return (self.column1_value, self.column2_value, self.current_products)


# Example usage:
"""
from gui.components.dynamic_table_widget import DynamicTableWidget
from database.products import fetch_all_products

def open_edit_products_dialog():
    # Initial values
    column1 = 18
    column2 = 28.5
    current_products = [product_obj1, product_obj2]  # List of product objects
    
    # All available products
    available_products = fetch_all_products()
    
    dialog = EditProductsListPopup(
        column1_value=column1,
        column2_value=column2,
        current_products=current_products,
        available_products=available_products,
        dynamic_table_widget_class=DynamicTableWidget,
        parent=self
    )
    
    # Option 1: Using signal
    dialog.data_updated.connect(lambda col1, col2, products: 
        print(f"Column 1: {col1}, Column 2: {col2}, Products: {len(products)}"))
    
    # Option 2: Using return value
    result = dialog.exec_()
    if result == QDialog.Accepted:
        col1, col2, products = dialog.get_data()
        print(f"Updated - Column 1: {col1}, Column 2: {col2}")
        print(f"Products in list: {[p.name for p in products]}")
        return col1, col2, products
    return None
"""
