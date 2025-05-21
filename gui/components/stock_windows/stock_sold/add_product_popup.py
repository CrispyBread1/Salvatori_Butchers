from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QDialog, 
    QHeaderView, QAbstractItemView, QHBoxLayout, QTableWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# Import the DynamicTableWidget component
from PyQt5.QtWidgets import QTableWidget  # Include this for type checking

class AddProductPopup(QDialog):
    # Signal to emit when a product is selected - returns the product ID
    product_selected = pyqtSignal(int)
    
    def __init__(self, products, dynamic_table_widget_class, parent=None):
        """
        Initialize the product selection popup.
        
        Args:
            products: List of product objects
            dynamic_table_widget_class: The DynamicTableWidget class to use
            parent: Parent widget
        """
        super().__init__(parent)
        self.products = products
        self.selected_product_id = None
        self.DynamicTableWidget = dynamic_table_widget_class
        
        self.setWindowTitle("Select Product")
        self.setFixedSize(800, 600)  # Set specific size for the popup
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title label
        title_label = QLabel("Select a product from the list below")
        title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        title_label.setFont(font)
        main_layout.addWidget(title_label)
        
        # Create the dynamic table widget
        self.dynamic_table_widget = self.DynamicTableWidget(self)
        main_layout.addWidget(self.dynamic_table_widget)
        
        # Get reference to the internal table for easy access
        self.table = self.dynamic_table_widget.table
        
        # Configure table behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make table read-only
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)  # Hide vertical headers
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        # Select button
        select_button = QPushButton("Select")
        select_button.clicked.connect(self.select_product)
        select_button.setDefault(True)
        select_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #003d73;
            }
        """)
        
        # Add buttons to the button layout
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(select_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Load product data
        self.load_product_table()
        
        # Connect double-click event
        self.table.cellDoubleClicked.connect(self.handle_double_click)
        
    def load_product_table(self):
        """Load product data into the dynamic table widget."""
        if not self.products:
            label = QLabel("No products found.")
            return
        
        # Set headers - include ID column
        headers = ["ID", "Name", "Stock Cost £", "Stock Count", "Selling Price £", 
                  "Stock Category", "Product Category", "Sage Code", "Supplier", "Sold As"]
        
        # Prepare data for the DynamicTableWidget
        data = []
        for product in self.products:
            row_data = [
                product.id,
                product.name,
                product.cost,
                product.stock_count,
                product.product_value,
                product.stock_category,
                product.product_category,
                product.sage_code,
                product.supplier,
                product.sold_as
            ]
            data.append(row_data)
        
        # Custom format function for cells
        def format_cell(item, row_idx, col_idx, value):
            # Make all cells read-only
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            # Center align all cells
            item.setTextAlignment(Qt.AlignCenter)
            
            # Make Name column clickable with blue underlined text
            if col_idx == 1:  # Name column (second column)
                item.setForeground(QColor(0, 0, 255))  # Blue text
                font = QFont()
                font.setUnderline(True)
                item.setFont(font)
            
            return item
        
        # Populate the dynamic table
        self.dynamic_table_widget.populate(headers, data, format_cell)
    
    def handle_double_click(self, row, column):
        """Handle double-click on a table cell."""
        # Get the product ID from the first column in the clicked row
        product_id = int(self.table.item(row, 0).text())
        self.selected_product_id = product_id
        
        # Emit signal with selected product ID and accept the dialog
        self.product_selected.emit(product_id)
        self.accept()
    
    def select_product(self):
        """Handle Select button click."""
        selected_items = self.table.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            product_id = int(self.table.item(selected_row, 0).text())
            self.selected_product_id = product_id
            
            # Emit signal with selected product ID and accept the dialog
            self.product_selected.emit(product_id)
            self.accept()
        
    def get_selected_product_id(self):
        """Return the selected product ID."""
        return self.selected_product_id


# Example usage:
"""
from gui.components.dynamic_table_widget import DynamicTableWidget
from database.products import fetch_products

def open_product_selection():
    products = fetch_products()
    dialog = ProductSelectionPopup(products, DynamicTableWidget, self)
    
    # Connect to the product_selected signal if you want to handle the selection in a callback
    dialog.product_selected.connect(lambda product_id: print(f"Selected product ID: {product_id}"))
    
    result = dialog.exec_()
    if result == QDialog.Accepted:
        # Get the selected product ID
        selected_id = dialog.get_selected_product_id()
        print(f"Dialog returned product ID: {selected_id}")
        return selected_id
    return None
"""
