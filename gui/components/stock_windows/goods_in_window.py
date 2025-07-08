from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import date, datetime, timedelta
from database.deliveries import fetch_deliveries_by_week
from database.products import fetch_products
from gui.components.reusable.table import DynamicTableWidget
from gui.components.stock_windows.goods_in.delivery_detail_window import DeliveryDetailWindow



class GoodsInWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.chosen_date = datetime.now()
        self.deliveries = []  # Store deliveries for detail window
        # Create product lookup dictionary once for O(1) access
        self.product_lookup = {product.id: product.name for product in fetch_products()}
        self.layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.title = QLabel(f"Goods In - {self.chosen_date.strftime('%Y-%m-%d')}")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.layout.addWidget(self.title)
        
        previous_week_button = QPushButton("Previous Week")
        previous_week_button.clicked.connect(self.move_previous_week)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_table)
        
        next_week_button = QPushButton("Next Week")
        next_week_button.clicked.connect(self.move_next_week)
        
        button_layout.addWidget(previous_week_button)
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(next_week_button)
        
        self.layout.addLayout(button_layout)
        
        self.dynamic_table_widget = DynamicTableWidget(self)
        self.layout.addWidget(self.dynamic_table_widget)
        
        self.label = QLabel("")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        self.title.setText(f"Goods In - {self.chosen_date.strftime('%Y-%m-%d')}")
        
        self.load_product_table()

    def load_product_table(self):
        """Load product data into the table."""
        self.deliveries = fetch_deliveries_by_week(self.chosen_date)

        if not self.deliveries:
            self.label.setText("No data found.")
            # Clear the table when no deliveries are found
            self.dynamic_table_widget.populate([], [], None)
            return
        
        # Clear previous message
        self.label.setText("")
        
        # Update title with current date
        self.title.setText(f"Goods In - {self.chosen_date.strftime('%Y-%m-%d')}")
        
        # Headers
        headers = ["Product", "Cases", "Batch Code", "Supplier", "Date"]
        
        # Build data list more efficiently
        data = []
        for delivery in self.deliveries:
            row_data = [
                self.product_lookup.get(delivery.product, "Unknown Product"),  # O(1) lookup
                str(delivery.quantity),
                str(delivery.batch_code),
                delivery.supplier,  # Fixed order - supplier was in wrong position
                delivery.date,
            ]
            data.append(row_data)

        # Simplified format function
        def format_cell(item, row_idx, col_idx, value):
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            # Format first column (Product) with blue underlined text
            if col_idx == 0:
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(Qt.blue)
                font = QFont()
                font.setUnderline(True)
                item.setFont(font)
            
            return item

        # Populate table
        self.dynamic_table_widget.populate(headers, data, format_cell)
        self.table = self.dynamic_table_widget.table
        
        # Connect table double-click event to open detail window (matching EditProductWindow pattern)
        try:
            self.table.cellDoubleClicked.disconnect()
        except:
            pass
        
        self.table.cellDoubleClicked.connect(self.open_delivery_detail)

    def open_delivery_detail(self, row_idx, col_idx):
        """Open the delivery detail window when double-clicking on Product column (similar to EditProductWindow)."""
        if col_idx == 0 and row_idx < len(self.deliveries):  # Only open on Product column (first column)
            # Import here to avoid circular imports
            
            
            self.delivery_detail_window = DeliveryDetailWindow(self.deliveries, row_idx, self)
            self.delivery_detail_window.show()

    def move_previous_week(self):
        self.chosen_date -= timedelta(weeks=1)
        self.setup_ui()
        self.repaint()  # Force UI refresh
    
    def move_next_week(self):
        self.chosen_date += timedelta(weeks=1)
        self.setup_ui()
        self.repaint()  # Force UI refresh
    
    def refresh_table(self):
        self.setup_ui()
        self.repaint()  # Force UI refresh
