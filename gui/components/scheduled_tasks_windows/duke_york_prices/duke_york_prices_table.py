from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from gui.components.reusable.table import DynamicTableWidget

class DukeYorkPricesTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Create single table widget
        self.table = DynamicTableWidget()
        
        # Add table to layout
        self.layout.addWidget(self.table)
        
    def load_invoices(self, invoices):
        """
        Load and display invoice data.
        
        Args:
            invoices (list): List of invoice dictionaries
        """
        headers = ["Invoice #", "Date", "Product", "Sage Code", "Cost Price", "Exact Price"]
        
        if not invoices:
            # Display empty table
            self.table.populate(headers, [])
            return
        
        # Prepare data rows
        data = []
        total_cost = 0
        total_exact = 0
        
        for invoice in invoices:
            invoice_number = str(invoice.get("invoice_number", ""))
            cost_price = invoice.get('cost_price', 0)
            exact_price = invoice.get('exact_price', 0)
            
            # Check if it's a credit invoice (7 digits)
            is_credit = len(invoice_number) == 7
            
            # If credit invoice, make values negative
            if is_credit:
                cost_price = -cost_price
                exact_price = -exact_price
            
            # Add to totals
            total_cost += cost_price
            total_exact += exact_price
            
            row = [
                invoice_number,
                self._format_date(invoice.get("invoice_date", "")),
                invoice.get("product_description", ""),
                invoice.get("product_sage_code", ""),
                f"£{cost_price:.2f}",
                f"£{exact_price:.2f}",
                is_credit  # Store credit flag for formatting
            ]
            data.append(row)
        
        # Add totals row
        data.append([
            "",
            "",
            "TOTAL",
            "",
            f"£{total_cost:.2f}",
            f"£{total_exact:.2f}",
            False  # Not a credit row
        ])
        
        # Populate table
        self.table.populate(headers, data, self._format_cell)
    
    def _format_date(self, date_str):
        """
        Format date string to a more readable format.
        
        Args:
            date_str (str): Date string in format "DD/MM/YYYY HH:MM:SS"
            
        Returns:
            str: Formatted date string
        """
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            return date_obj.strftime("%d/%m/%Y")
        except:
            return date_str
    
    def _format_cell(self, item, row_idx, col_idx, value):
        """
        Custom formatting callback for table cells.
        
        Args:
            item: The QTableWidgetItem
            row_idx: Row index
            col_idx: Column index
            value: Cell value
            
        Returns:
            The formatted QTableWidgetItem
        """
        # Right-align currency columns (Cost Price and Exact Price)
        if col_idx in [4, 5]:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Make total row bold
        if isinstance(value, str) and value == "TOTAL":
            font = item.font()
            font.setBold(True)
            item.setFont(font)
        
        # Color credit invoices red (check if last column is True)
        if col_idx < 6:  # Don't check the flag column itself
            try:
                # Get the credit flag from the last column
                row_data = []
                for col in range(self.table.table.columnCount()):
                    cell_item = self.table.table.item(row_idx, col)
                    if cell_item:
                        row_data.append(cell_item.text())
                
                # Check if invoice number is 7 digits (credit)
                invoice_num = self.table.table.item(row_idx, 0)
                if invoice_num and len(invoice_num.text()) == 7:
                    item.setForeground(QColor(200, 0, 0))  # Red color for credits
            except:
                pass
        
        return item
