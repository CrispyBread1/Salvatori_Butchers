import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QPushButton, QLabel, QTableWidget, QVBoxLayout,
    QMainWindow, QMessageBox, QHBoxLayout, QFileDialog
)
from database.products import fetch_products, update_product
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.components.reusable.table import DynamicTableWidget
from gui.components.edit_product_windows.product_detail_window import ProductDetailWindow
from datetime import datetime
from resources.update_supplier_excel import process_file, save_output_file

class EditProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self, user=None):
        self.products = []
        self.reloading = False

        self.setWindowTitle('Product Window')

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.loading_manager = LoadingManager(self)

        # Main Layout
        self.layout = QVBoxLayout(central_widget)
        self.resize(1200, 800)

        self.nav_dashboard_layout = QHBoxLayout()
        
        # Add Dashboard buttons
        self.update_supplier_sheet_button = QPushButton("Update Prices On Supplier Sheet", self)
        self.update_supplier_sheet_button.clicked.connect(self.update_supplier_sheet)
        self.update_supplier_sheet_button.hide() 

        if user and user.admin:
            self.update_supplier_sheet_button.show() 
        
        # Add buttons to navigation Dashboard
        self.nav_dashboard_layout.addWidget(self.update_supplier_sheet_button)            

        self.nav_dashboard_layout.addStretch(1)  # Add stretch to push buttons to the left
        self.layout.addLayout(self.nav_dashboard_layout)
        
        # Title Label
        self.label = QLabel("Products", self)
        self.layout.addWidget(self.label)

        # Reload Button (Above the Table)
        self.table_button = QPushButton("Reload Products", self)
        self.table_button.clicked.connect(lambda: self.reload_product_list())
        self.layout.addWidget(self.table_button)

        # Initialize DynamicTableWidget from the imported component
        self.dynamic_table_widget = DynamicTableWidget(self)
        self.layout.addWidget(self.dynamic_table_widget)

        # Load Data
        self.load_product_table()

    def load_product_table(self):
        """Load product data into the table (Hardcoded Columns)."""
        self.products = fetch_products()
        self.products.sort(key=lambda product: (product.stock_category, product.name))  

        if not self.products:
            self.label.setText("No data found.")
            return

        # Set headers manually (matching database fields)
        headers = ["Name", "Stock Cost £", "Stock Count", "Selling Price £", "Stock Category", "Product Category", "Sage Code", "Supplier", "Sold As"]
        
        # Prepare data for the DynamicTableWidget
        data = []
        for product in self.products:
            row_data = [
                product.name,
                str(product.cost),
                str(product.stock_count),
                str(product.product_value),
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
            
            # Make Name column clickable with blue underlined text
            if col_idx == 0:
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(Qt.blue)
                font = QFont()
                font.setUnderline(True)
                item.setFont(font)
            
            return item

        # Populate the dynamic table
        self.dynamic_table_widget.populate(headers, data, format_cell)
        
        # Store reference to the table for easy access in other methods
        self.table = self.dynamic_table_widget.table
        
        # Connect signals
        try:
            self.table.cellDoubleClicked.disconnect()
        except:
            pass
        
        self.table.cellDoubleClicked.connect(self.open_product_detail)

    def reload_product_list(self):
        self.setup_ui()  # Reload the table data.

    def open_product_detail(self, row_idx, col_idx):
        """Open detailed product edit window when clicking on Name."""
        if col_idx == 0:
            filtered_rows = self.dynamic_table_widget.return_row()
            filtered_products = self.get_product_by_name(filtered_rows)
            self.product_detail_window = ProductDetailWindow(filtered_products, row_idx, self)
            self.product_detail_window.show()
    
    def get_product_by_name(self, filtered_rows):
        products_found = []
        for product in self.products:
            for filtered_row in filtered_rows:
              if product.name == filtered_row[0]:
                  products_found.append(product)
        return products_found
                  

    def update_supplier_sheet(self):
        """
        Update price columns on the supplier Excel or CSV sheet from Sage data.
        Simple implementation without any worker threads or progress tracking.
        """
        # Ask user to select input file
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Select Supplier Sheet", "", 
            "Spreadsheet Files (*.xlsx *.xls *.csv);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)"
        )
        
        if not input_file:  # User cancelled file selection
            return
        
        self.loading_manager.run_with_loading(
            task_function=process_file,  # Direct call to your function
            on_complete=self.on_update_complete,
            on_error=self.on_update_error,
            loading_text="Updating product data...",
            title="Loading Prices",
            task_args=(input_file,)
        )

    def on_update_complete(self, result, updated_at):
        """
        Handle completion of the price update operation
        """
        # Extract just the DataFrame from the tuple result
        if isinstance(result, tuple) and len(result) == 2:
            updated_df = result[0]  # Get just the DataFrame from the tuple
            input_file = result[1]  # Get the original file path
        else:
            updated_df = result
            input_file = None
        
        # Continue with the original function logic
        if updated_df is not None and not updated_df.empty:
            # Get the base and extension from the original input file
            if input_file:
                base, ext = os.path.splitext(input_file)
            else:
                # Fallback if no input file is available
                base = "updated_data"
                ext = ".xlsx"
                
            default_output = f"{base}_updated{ext}"
            file_type = "Excel Files (*.xlsx)" if ext.lower() in ['.xlsx', '.xls'] else "CSV Files (*.csv)"
            
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Save Updated File", default_output, 
                f"{file_type};;All Files (*)"
            )

            if output_file:
                # Save to the selected location
                save_output_file(updated_df, output_file)
                QMessageBox.information(self, "Success", f"File updated successfully and saved to:\n{output_file}")
        else:
            self.status_label.setText("No invoices found for the selected date.")

    
    def on_update_error(self, error_message):
        QMessageBox.critical(self, "Error", f"An error occurred while processing the file:\n{str(error_message)}")
