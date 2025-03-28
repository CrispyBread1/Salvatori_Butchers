from collections import defaultdict
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QLabel, QTableWidgetItem, QMainWindow,
    QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
import json
from database.products import fetch_products
from database.stock_takes import fetch_stock_takes_in_date_range, fetch_stock_takes_in_date_range_with_category


class StockTakeViewWindow(QMainWindow):
    category = ''
    current_week_monday = ''

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
        self.current_week_monday = self.get_current_monday()
        self.update_week_dates()

        # Load default data (All products)

    def create_navigation_buttons(self):
        """Create buttons to navigate between weeks."""
        self.nav_layout = QHBoxLayout()
        self.main_layout.addLayout(self.nav_layout)

        self.previous_week_button = QPushButton("Previous Week")
        self.current_week_button = QPushButton("Current Week")
        self.next_week_button = QPushButton("Next Week")

        self.previous_week_button.clicked.connect(self.go_to_previous_week)
        self.current_week_button.clicked.connect(self.go_to_current_week)
        self.next_week_button.clicked.connect(self.go_to_next_week)

        self.current_week_button.hide()

        self.nav_layout.addWidget(self.previous_week_button)
        self.nav_layout.addWidget(self.current_week_button)
        self.nav_layout.addWidget(self.next_week_button)

    def get_current_monday(self):
        """Get the Monday of the current week."""
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        return today - timedelta(days=today.weekday())  # Start of the week (Monday)

    def update_week_dates(self):
        """Update the displayed week range and fetch data."""
        monday = self.current_monday
        friday = monday.replace(hour=23, minute=59, second=59, microsecond=9999) + timedelta(days=4)

        # Update header title
        self.header_label.setText(f"{monday.strftime('%A %d %b')} - {friday.strftime('%A %d %b')}")

        # Store the updated start and end dates
        self.start_date = monday
        self.end_date = friday

        # Reload the table data with the new date range
        self.load_data(self.category)

    def go_to_previous_week(self):
        """Move the date range one week back."""
        self.current_week_button.show()
        self.current_monday -= timedelta(weeks=1)
        self.update_week_dates()

    def go_to_next_week(self):
        """Move the date range one week forward."""
        self.current_week_button.show()
        self.current_monday += timedelta(weeks=1)
        self.update_week_dates()

    def go_to_current_week(self):
        self.current_week_button.hide()
        self.current_monday = self.current_week_monday
        self.update_week_dates()

    def create_filter_buttons(self):
        """Create category filter buttons (Fresh, Dry, Frozen, All)."""
        self.button_layout = QHBoxLayout()

        self.fresh_button = QPushButton("Fresh")
        self.dry_button = QPushButton("Dry")
        self.frozen_button = QPushButton("Frozen")


        # Connect buttons to filter function
        self.fresh_button.clicked.connect(lambda: self.load_data("fresh"))
        self.dry_button.clicked.connect(lambda: self.load_data("dry"))
        self.frozen_button.clicked.connect(lambda: self.load_data("frozen"))

        # Add buttons to layout
        self.button_layout.addWidget(self.fresh_button)
        self.button_layout.addWidget(self.dry_button)
        self.button_layout.addWidget(self.frozen_button)

        # Add button layout to main layout
        self.main_layout.addLayout(self.button_layout)

    def setup_table(self):
      """Initialize table with weekdays as headers (excluding weekends)."""
      headers = ["Product", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

      # Set table dimensions
      self.table.setColumnCount(len(headers))
      self.table.setHorizontalHeaderLabels(headers)

      # Allow the table to stretch fully within the window
      self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

      # Resize table to fit contents properly
      self.table.horizontalHeader().setStretchLastSection(True)
      self.table.horizontalHeader().setSectionResizeMode(1)  # Stretch columns

    def load_data(self, category):
        """Load stock take data into the table based on selected category."""
        self.category = category
        products_results = fetch_products()

        stock_take_results = self.process_stock_takes(fetch_stock_takes_in_date_range_with_category(category, self.start_date, self.end_date))
        self.render_table_category(products_results, category, stock_take_results)

    def render_table_all(self, products, stock_takes):
      """Populate the table with stock take data for all categories."""
      
      # Clear existing table rows
      self.table.setRowCount(0)
      
      # Define weekdays mapping for table columns
      weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      date_to_column = {
          (self.start_date + timedelta(days=i)).strftime('%Y-%m-%d'): i + 1  # Offset by 1 because column 0 is 'Product'
          for i in range(6)
      }
      
      # Set number of rows based on product count
      self.table.setRowCount(len(products))
      # Populate table with stock values
      for row_idx, product in enumerate(products):
          stock_values = [""] * 6  # Initialize empty values for Monday-Friday

          # Find stock take data for this product
          product_id = str(product.id)  # Convert product ID to string (since stock_take uses string keys)
          
          for stock_date, stock_take in stock_takes.items():  # Convert datetime to string
              
              if stock_date in date_to_column:
                  col_idx = date_to_column[stock_date]  # Get corresponding column index
                  
                  # ✅ Ensure JSON Decoding is only done if needed
                  stock_data = stock_take.take if isinstance(stock_take.take, dict) else json.loads(stock_take.take)

                  # ✅ Get stock value using product ID
                  stock_values[col_idx - 1] = str(stock_data.get(product_id, ""))

          # Set product name in first column
          self.table.setItem(row_idx, 0, QTableWidgetItem(product.name))

          # Populate table row with stock values
          for col_idx, stock_value in enumerate(stock_values, start=1):  # Start from column 1
              self.table.setItem(row_idx, col_idx, QTableWidgetItem(stock_value))


    def render_table_category(self, products, category, stock_takes):
        """Render table for a specific product category."""
        filtered_products = [p for p in products if p.stock_category == category]
        self.render_table_all(filtered_products, stock_takes)

    def process_stock_takes(self, stock_takes):
        """Process stock takes: group by date and select the most recent entries."""

        if not stock_takes:
            return {}

        grouped_stock_takes = defaultdict(list)

        # Group by date
        for stock_take in stock_takes:
            stock_date_str = stock_take.date.strftime('%Y-%m-%d')  # Convert datetime to string
            grouped_stock_takes[stock_date_str].append(stock_take)

        # Sort by date_added (newest first) and pick the latest entry
        newest_stock_takes = {
            stock_date: sorted(takes, key=lambda x: x.created_at, reverse=True)[0]
            for stock_date, takes in grouped_stock_takes.items()
        }

        return newest_stock_takes
