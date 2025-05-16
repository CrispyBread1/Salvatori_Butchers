import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QTableWidgetItem, QPushButton, QLabel, QTableWidget, QVBoxLayout,
    QMainWindow, QMessageBox, QHBoxLayout, QFileDialog
)
from database.products import fetch_products, update_product
from gui.components.reusable.animations.loading_component import LoadingManager
from gui.product_detail_window import ProductDetailWindow
from datetime import datetime
from resources.update_supplier_excel import process_file, save_output_file

class EditProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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


        # Product Table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Load Data
        self.load_product_table()

        # self.table_button = QPushButton("Save", self)
        # self.table_button.clicked.connect(self.reload_list)
        # self.layout.addWidget(self.table_button)

    def load_product_table(self):
        """Load product data into the table (Hardcoded Columns)."""
        self.products = fetch_products()
        self.products.sort(key=lambda product: (product.stock_category, product.name))  

        if not self.products:
            self.label.setText("No data found.")
            return

        # Clear existing table contents before reloading data
        self.table.clearContents()
        
        try:
          self.table.cellDoubleClicked.disconnect()
        except:
            pass

        self.table.setRowCount(len(self.products))

        # Set headers manually (matching database fields)
        headers = ["Name", "Stock Cost £", "Stock Count", "Selling Price £", "Stock Category", "Product Category", "Sage Code", "Supplier", "Sold As"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setUpdatesEnabled(False)  
        # Populate Table (No Looping for Field Mapping)
        for row_idx, product in enumerate(self.products):
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

        self.table.setUpdatesEnabled(True)
        self.table.itemChanged.connect(self.cell_edited)
         
        self.table.cellDoubleClicked.connect(self.open_product_detail)
        self.table.resizeColumnsToContents()

    def reload_product_list(self):
        self.reloading = True  # Set the flag to True before reloading.
        self.load_product_table()  # Reload the table data.
        self.reloading = False 

    def cell_edited(self, item):
      """Show Save button at the bottom after editing a cell."""
      if self.reloading:  # Skip the logic if a reload is in progress.
        return

      row_idx = item.row()
      col_idx = item.column()

      if col_idx == 2:  # Stock Count should not be editable
          return

      # Remove previous Save button if it exists
      if hasattr(self, 'save_button'):
          self.save_button.deleteLater()

      # Create and show Save button at the bottom of the layout
      self.save_button = QPushButton("Save", self)
      self.save_button.clicked.connect(lambda: self.save_product(row_idx))

      # Add the Save button at the bottom of the layout (below the current widgets)
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

        update_product(product.id, name=product.name, cost=product.cost, 
                       product_value=product.product_value, stock_category=product.stock_category, product_category=product.product_category, 
                       sage_code=product.sage_code, supplier=product.supplier, sold_as=product.sold_as)  # Save changes to DB

        QMessageBox.information(self, "Success", "Product updated successfully!")
        self.save_button.deleteLater()
        del self.save_button

    def open_product_detail(self, row_idx, col_idx):
        """Open detailed product edit window when clicking on Name."""
        if col_idx == 0:
            self.product_detail_window = ProductDetailWindow(self.products, row_idx, self)
            self.product_detail_window.show()

    # def sort_products(self, fetched_products):
    #     """Sort products by category & name."""
    #     return sorted(fetched_products, key=lambda product: (product.stock_category, product.name))

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
