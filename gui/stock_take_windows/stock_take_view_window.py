from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QLabel, QTableWidgetItem, QMainWindow,
    QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta

from database.products import fetch_products
from database.stock_takes import fetch_stock_takes_in_date_range, fetch_stock_takes_in_date_range_with_category


class StockTakeViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Stock Take View")

        # Main container widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navigation buttons for previous and next week
        

        # Title for date range
        self.header_label = QLabel("", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        self.main_layout.addWidget(self.header_label)

        self.create_navigation_buttons()

        # Category filter buttons
        self.create_filter_buttons()

        # Create table
        self.table = QTableWidget()
        self.setup_table()

        # Add table to layout and ensure it expands
        self.main_layout.addWidget(self.table)

        # Apply layout to the central widget
        self.central_widget.setLayout(self.main_layout)

        # Initialize default week (current week)
        self.current_monday = self.get_current_monday()
        self.update_week_dates()

        # Load default data (All products)
        self.load_data("all")

    def create_navigation_buttons(self):
        """Create buttons to navigate between weeks."""
        self.nav_layout = QHBoxLayout()
        self.main_layout.addLayout(self.nav_layout)

        self.previous_week_button = QPushButton("Previous Week")
        self.next_week_button = QPushButton("Next Week")

        self.previous_week_button.clicked.connect(self.go_to_previous_week)
        self.next_week_button.clicked.connect(self.go_to_next_week)

        self.nav_layout.addWidget(self.previous_week_button)
        self.nav_layout.addWidget(self.next_week_button)

    def get_current_monday(self):
        """Get the Monday of the current week."""
        today = datetime.today()
        return today - timedelta(days=today.weekday())  # Start of the week (Monday)

    def update_week_dates(self):
        """Update the displayed week range and fetch data."""
        monday = self.current_monday
        friday = monday + timedelta(days=4)

        # Update header title
        self.header_label.setText(f"{monday.strftime('%A %d %b')} - {friday.strftime('%A %d %b')}")

        # Store the updated start and end dates
        self.start_date = monday
        self.end_date = friday

        # Reload the table data with the new date range
        self.load_data("all")

    def go_to_previous_week(self):
        """Move the date range one week back."""
        self.current_monday -= timedelta(weeks=1)
        self.update_week_dates()

    def go_to_next_week(self):
        """Move the date range one week forward."""
        self.current_monday += timedelta(weeks=1)
        self.update_week_dates()

    def create_filter_buttons(self):
        """Create category filter buttons (Fresh, Dry, Frozen, All)."""
        self.button_layout = QHBoxLayout()

        self.fresh_button = QPushButton("Fresh")
        self.dry_button = QPushButton("Dry")
        self.frozen_button = QPushButton("Frozen")
        self.all_button = QPushButton("All")

        # Connect buttons to filter function
        self.fresh_button.clicked.connect(lambda: self.load_data("fresh"))
        self.dry_button.clicked.connect(lambda: self.load_data("dry"))
        self.frozen_button.clicked.connect(lambda: self.load_data("frozen"))
        self.all_button.clicked.connect(lambda: self.load_data("all"))

        # Add buttons to layout
        self.button_layout.addWidget(self.fresh_button)
        self.button_layout.addWidget(self.dry_button)
        self.button_layout.addWidget(self.frozen_button)
        self.button_layout.addWidget(self.all_button)

        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)

    def setup_table(self):
        """Initialize table with weekdays as headers (excluding weekends)."""
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Set table dimensions
        self.table.setColumnCount(len(weekdays))
        self.table.setHorizontalHeaderLabels(weekdays)

        # Allow the table to stretch fully within the window
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        # Resize table to fit contents properly
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1)  # Stretch columns

    def load_data(self, category):
        """Load stock take data into the table based on selected category."""
        self.data = {}

        products_results = fetch_products()
        self.products = []

        if category == 'all':
          stock_take_results = fetch_stock_takes_in_date_range(self.start_date, self.end_date)
          self.data = products_results
          self.products = products_results
        else:
          stock_take_results = fetch_stock_takes_in_date_range_with_category(category, self.start_date, self.end_date)
          for product in products_results:
            if product.stock_category not in self.data:
                self.data[product.stock_category] = []
            self.data[product.stock_category].append(product)
          self.products = self.data.get(category, [])

        

        # Clear existing table rows
        self.table.setRowCount(0)

        # Load new data
       
        self.table.setRowCount(len(self.products))

        for row_idx, product in enumerate(self.products):
            stock_values = [""] * 5  # Empty values for each day of the week

            # If stock take data exists, fill in values
            if category in stock_take_results:
                for stock_take in stock_take_results[category]:
                    # Assume stock_take.take contains a dictionary of stock values per date
                    for i, day_offset in enumerate(range(5)):  # Monday-Friday
                        date_str = (self.start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
                        stock_values[i] = stock_take.take.get(date_str, "")

            # Populate table cells
            for col_idx, stock_value in enumerate(stock_values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(stock_value))
