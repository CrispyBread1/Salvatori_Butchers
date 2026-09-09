import os

from datetime import datetime

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QFileDialog
)

from database.products import fetch_products, update_product

from gui.components.reusable.animations.loading_component import LoadingManager

from gui.components.reusable.table import DynamicTableWidget

from gui.components.edit_product_windows.product_detail_window import (
    ProductDetailWindow
)

from resources.update_supplier_excel import process_file, save_output_file

from resources.excel_exporter import ExcelExporter


class EditProductWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self, user=None):

        self.products = []

        self.reloading = False

        self.setWindowTitle("Product Window")

        # Central Widget

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        self.loading_manager = LoadingManager(self)

        # Main Layout

        self.layout = QVBoxLayout(central_widget)

        self.resize(1200, 800)

        self.nav_dashboard_layout = QHBoxLayout()

        # Add Dashboard buttons

        self.update_supplier_sheet_button = QPushButton(
            "Update Prices On Supplier Sheet",
            self
        )

        self.update_supplier_sheet_button.clicked.connect(
            self.update_supplier_sheet
        )

        self.update_supplier_sheet_button.hide()

        if user and user.admin:

            self.update_supplier_sheet_button.show()

        self.export_products_button = QPushButton(
            "Export All Products To Excel",
            self
        )

        self.export_products_button.clicked.connect(
            self.export_products_to_excel
        )

        # Add buttons to navigation Dashboard

        self.nav_dashboard_layout.addWidget(
            self.update_supplier_sheet_button
        )

        self.nav_dashboard_layout.addWidget(
            self.export_products_button
        )

        # Add stretch to push buttons to the left

        self.nav_dashboard_layout.addStretch(1)

        self.layout.addLayout(self.nav_dashboard_layout)

        # Title Label

        self.label = QLabel("Products", self)

        self.layout.addWidget(self.label)

        # Reload Button (Above the Table)

        self.table_button = QPushButton("Reload Products", self)

        self.table_button.clicked.connect(
            lambda: self.reload_product_list()
        )

        self.layout.addWidget(self.table_button)

        # Initialize DynamicTableWidget from the imported component

        self.dynamic_table_widget = DynamicTableWidget(self)

        self.layout.addWidget(self.dynamic_table_widget)

        # Load Data

        self.load_product_table()

    def load_product_table(self):

        """Load product data into the table (Hardcoded Columns)."""

        self.products = fetch_products()

        if not self.products:

            self.label.setText("No data found.")

            return

        self.label.setText("Products")

        # Set headers manually (matching database fields)

        headers = [
            "Name",
            "Stock Cost £",
            "Stock Count",
            "Selling Price £",
            "Stock Category",
            "Product Category",
            "Sage Code",
            "Supplier",
            "Sold As"
        ]

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

        self.dynamic_table_widget.populate(
            headers,
            data,
            format_cell
        )

        # Store reference to the table for easy access in other methods

        self.table = self.dynamic_table_widget.table

        # Connect signals

        try:

            self.table.cellDoubleClicked.disconnect()

        except:

            pass

        self.table.cellDoubleClicked.connect(
            self.open_product_detail
        )

    def reload_product_list(self):

        self.setup_ui()

    def open_product_detail(self, row_idx, col_idx):

        """Open detailed product edit window when clicking on Name."""

        if col_idx == 0:

            filtered_rows = (
                self.dynamic_table_widget.return_row()
            )

            filtered_products = self.get_product_by_name(
                filtered_rows
            )

            self.product_detail_window = ProductDetailWindow(
                filtered_products,
                row_idx,
                self
            )

            self.product_detail_window.show()

    def get_product_by_name(self, filtered_rows):

        # Need to send the whole product object to the display.
        # This uses the name to get the filtered list, but there
        # may be duplicate product names.

        pop_array_products = self.products.copy()

        products_found = []

        for filtered_row in filtered_rows:

            index = 0

            while index < len(pop_array_products):

                product = pop_array_products[index]

                if product.name == filtered_row[0]:

                    products_found.append(product)

                    pop_array_products.pop(index)

                else:

                    index += 1

        return products_found

    def export_products_to_excel(self):

        """Export all products from the database to an Excel file."""

        try:

            products = fetch_products()

            if not products:

                QMessageBox.information(
                    self,
                    "No Products",
                    "There are no products to export."
                )

                return

            current_date = datetime.now().strftime("%Y-%m-%d")

            default_filename = (
                f"all_products_{current_date}.xlsx"
            )

            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Export All Products",
                default_filename,
                "Excel Files (*.xlsx);;All Files (*)"
            )

            if not output_file:

                return

            if not output_file.lower().endswith(".xlsx"):

                output_file += ".xlsx"

            headers = [
                "ID",
                "Name",
                "Cost",
                "Stock Count",
                "Product Value",
                "Stock Category",
                "Product Category",
                "Sage Code",
                "Supplier",
                "Sold As"
            ]

            data = []

            for product in products:

                product_data = {
                    "ID": product.id,
                    "Name": product.name,
                    "Cost": product.cost,
                    "Stock Count": product.stock_count,
                    "Product Value": product.product_value,
                    "Stock Category": product.stock_category,
                    "Product Category": product.product_category,
                    "Sage Code": product.sage_code,
                    "Supplier": product.supplier,
                    "Sold As": product.sold_as
                }

                data.append(product_data)

            excel_exporter = ExcelExporter(parent=self)

            excel_exporter.export(
                data=data,
                sheet_name="Products",
                title="All Products",
                filename=output_file,
                headers=headers
            )

            QMessageBox.information(
                self,
                "Export Complete",
                (
                    "All products were exported successfully to:\n"
                    f"{output_file}"
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Failed",
                (
                    "An error occurred while exporting the products:\n"
                    f"{str(error)}"
                )
            )

    def update_supplier_sheet(self):

        """
        Update price columns on the supplier Excel or CSV sheet
        from Sage data.
        """

        # Ask user to select input file

        input_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Supplier Sheet",
            "",
            (
                "Spreadsheet Files (*.xlsx *.xls *.csv);;"
                "Excel Files (*.xlsx *.xls);;"
                "CSV Files (*.csv);;"
                "All Files (*)"
            )
        )

        if not input_file:

            return

        self.loading_manager.run_with_loading(
            task_function=process_file,
            on_complete=self.on_update_complete,
            on_error=self.on_update_error,
            on_pause=self.handle_pause,
            loading_text="Updating product data...",
            title="Loading Prices",
            task_args=(input_file,)
        )

    def on_update_complete(self, result, updated_at):

        """Handle completion of the price update operation."""

        # Extract just the DataFrame from the tuple result

        if isinstance(result, tuple) and len(result) == 2:

            updated_df = result[0]

            input_file = result[1]

        else:

            updated_df = result

            input_file = None

        if updated_df is not None and not updated_df.empty:

            # Get the base and extension from the original input file

            if input_file:

                base, ext = os.path.splitext(input_file)

            else:

                base = "updated_data"

                ext = ".xlsx"

            default_output = f"{base}_updated{ext}"

            if ext.lower() in [".xlsx", ".xls"]:

                file_type = "Excel Files (*.xlsx)"

            else:

                file_type = "CSV Files (*.csv)"

            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Save Updated File",
                default_output,
                f"{file_type};;All Files (*)"
            )

            if output_file:

                save_output_file(updated_df, output_file)

                QMessageBox.information(
                    self,
                    "Success",
                    (
                        "File updated successfully and saved to:\n"
                        f"{output_file}"
                    )
                )

        else:

            QMessageBox.information(
                self,
                "No Data",
                "No invoices were found for the selected date."
            )

    def on_update_error(self, error_message):

        QMessageBox.critical(
            self,
            "Error",
            (
                "An error occurred while processing the file:\n"
                f"{str(error_message)}"
            )
        )

    def handle_pause(self):

        pass
