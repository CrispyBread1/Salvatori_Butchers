from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
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
        for invoice in invoices:
            row = [
                invoice.get("invoice_number", ""),
                self._format_date(invoice.get("invoice_date", "")),
                invoice.get("product_description", ""),
                invoice.get("product_sage_code", ""),
                f"£{invoice.get('cost_price', 0):.2f}",
                f"£{invoice.get('exact_price', 0):.2f}"
            ]
            data.append(row)
        
        # Add totals row
        total_cost = sum(item.get("cost_price", 0) for item in invoices)
        total_exact = sum(item.get("exact_price", 0) for item in invoices)
        
        data.append([
            "",
            "",
            "TOTAL",
            "",
            f"£{total_cost:.2f}",
            f"£{total_exact:.2f}"
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
        
        return item
