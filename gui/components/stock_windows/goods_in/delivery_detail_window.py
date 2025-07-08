from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow, QLineEdit, 
    QMessageBox, QHBoxLayout, QComboBox, QDateEdit, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from database.products import fetch_products

class DeliveryDetailWindow(QMainWindow):
    def __init__(self, deliveries, current_index, parent=None):
        super().__init__(parent)
        self.deliveries = deliveries
        self.current_index = current_index
        self.products = fetch_products()
        
        # Create product lookup dictionaries
        self.product_lookup = {product.id: product.name for product in self.products}
        self.product_name_to_id = {product.name: product.id for product in self.products}

        self.setWindowTitle("Delivery Details")
        self.resize(800, 500)  # Wider but shorter

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Title label
        self.title_label = QLabel("Delivery Details")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        self.layout.addWidget(self.title_label)

        # Create grid layout for fields
        grid_layout = QGridLayout()
        
        # Common style for display fields
        field_style = "background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc; min-height: 20px;"
        
        # Row 0: Product and Cases
        grid_layout.addWidget(QLabel("Product:"), 0, 0)
        self.product_display = QLabel(self)
        self.product_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.product_display, 0, 1)
        
        grid_layout.addWidget(QLabel("Cases:"), 0, 2)
        self.quantity_display = QLabel(self)
        self.quantity_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.quantity_display, 0, 3)

        # Row 1: Batch Code and Vehicle Temperature
        grid_layout.addWidget(QLabel("Batch Code:"), 1, 0)
        self.batch_code_display = QLabel(self)
        self.batch_code_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.batch_code_display, 1, 1)
        
        grid_layout.addWidget(QLabel("Vehicle Temperature:"), 1, 2)
        self.vehicle_temp_display = QLabel(self)
        self.vehicle_temp_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.vehicle_temp_display, 1, 3)

        # Row 2: Product Temperature and Driver Name
        grid_layout.addWidget(QLabel("Product Temperature:"), 2, 0)
        self.product_temp_display = QLabel(self)
        self.product_temp_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.product_temp_display, 2, 1)
        
        grid_layout.addWidget(QLabel("Driver Name:"), 2, 2)
        self.driver_name_display = QLabel(self)
        self.driver_name_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.driver_name_display, 2, 3)

        # Row 3: License Plate and Origin
        grid_layout.addWidget(QLabel("License Plate:"), 3, 0)
        self.license_plate_display = QLabel(self)
        self.license_plate_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.license_plate_display, 3, 1)
        
        grid_layout.addWidget(QLabel("Origin:"), 3, 2)
        self.origin_display = QLabel(self)
        self.origin_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.origin_display, 3, 3)

        # Row 4: Kill Date and Use By Date
        grid_layout.addWidget(QLabel("Kill Date:"), 4, 0)
        self.kill_date_display = QLabel(self)
        self.kill_date_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.kill_date_display, 4, 1)
        
        grid_layout.addWidget(QLabel("Use By Date:"), 4, 2)
        self.use_by_display = QLabel(self)
        self.use_by_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.use_by_display, 4, 3)

        # Row 5: Supplier and Slaughter Number
        grid_layout.addWidget(QLabel("Supplier:"), 5, 0)
        self.supplier_display = QLabel(self)
        self.supplier_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.supplier_display, 5, 1)
        
        grid_layout.addWidget(QLabel("Slaughter Number:"), 5, 2)
        self.slaughter_number_display = QLabel(self)
        self.slaughter_number_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.slaughter_number_display, 5, 3)

        # Row 6: Cut Number (spans 2 columns)
        grid_layout.addWidget(QLabel("Cut Number:"), 6, 0)
        self.cut_number_display = QLabel(self)
        self.cut_number_display.setStyleSheet(field_style)
        grid_layout.addWidget(self.cut_number_display, 6, 1)

        # Add grid layout to main layout
        self.layout.addLayout(grid_layout)

        # Certifications section
        certifications_layout = QHBoxLayout()
        
        # Certifications label
        self.certifications_label = QLabel("Certifications:")
        self.certifications_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        certifications_layout.addWidget(self.certifications_label)

        # Certification displays in horizontal layout
        self.red_tractor_display = QLabel(self)
        self.red_tractor_display.setStyleSheet(field_style)
        certifications_layout.addWidget(self.red_tractor_display)

        self.rspca_display = QLabel(self)
        self.rspca_display.setStyleSheet(field_style)
        certifications_layout.addWidget(self.rspca_display)

        self.organic_assured_display = QLabel(self)
        self.organic_assured_display.setStyleSheet(field_style)
        certifications_layout.addWidget(self.organic_assured_display)

        certifications_layout.addStretch()  # Push certifications to the left
        
        self.layout.addLayout(certifications_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Previous", self)
        self.prev_button.clicked.connect(self.prev_delivery)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_delivery)
        nav_layout.addWidget(self.next_button)

        nav_layout.addStretch()  # Push navigation buttons to the left

        # Close Button
        self.close_button = QPushButton("Close", self)
        self.close_button.setStyleSheet("""
          QPushButton {
            background-color: #6c757d;
            color: white;
            border: 1px solid #545b62;
            padding: 10px 20px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
          }
          QPushButton:hover {
            background-color: #545b62;
          }
          QPushButton:pressed {
            background-color: #3e444a;
          }
        """)
        self.close_button.clicked.connect(self.close)
        nav_layout.addWidget(self.close_button)

        self.layout.addLayout(nav_layout)

        self.load_delivery()

    def prev_delivery(self):
        """Navigate to the previous delivery."""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_delivery()
            self.update_navigation_buttons()

    def next_delivery(self):
        """Navigate to the next delivery."""
        if self.current_index < len(self.deliveries) - 1:
            self.current_index += 1
            self.load_delivery()
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Update the state of navigation buttons."""
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.deliveries) - 1)

    def load_delivery(self):
        """Load the selected delivery details into display fields."""
        delivery = self.deliveries[self.current_index]
        
        # Set product display
        product_name = self.product_lookup.get(delivery.product, "Unknown Product")
        self.product_display.setText(product_name)
        
        # Set all other fields
        self.quantity_display.setText(str(delivery.quantity))
        self.batch_code_display.setText(str(delivery.batch_code))
        self.vehicle_temp_display.setText(delivery.vehicle_temperature or "")
        self.product_temp_display.setText(delivery.product_temperature or "")
        self.driver_name_display.setText(delivery.driver_name or "")
        self.license_plate_display.setText(delivery.license_plate or "")
        self.origin_display.setText(delivery.origin or "")
        
        # Set dates
        if delivery.kill_date:
            self.kill_date_display.setText(delivery.kill_date.strftime('%Y-%m-%d'))
        else:
            self.kill_date_display.setText("")
            
        if delivery.use_by:
            self.use_by_display.setText(delivery.use_by.strftime('%Y-%m-%d'))
        else:
            self.use_by_display.setText("")
        
        self.supplier_display.setText(delivery.supplier or "")
        self.slaughter_number_display.setText(delivery.slaughter_number or "")
        self.cut_number_display.setText(delivery.cut_number or "")
        
        # Set certification displays
        self.red_tractor_display.setText("✓ Red Tractor" if delivery.red_tractor else "✗ Red Tractor")
        self.rspca_display.setText("✓ RSPCA" if delivery.rspca else "✗ RSPCA")
        self.organic_assured_display.setText("✓ Organic Assured" if delivery.organic_assured else "✗ Organic Assured")
        
        # Update navigation buttons
        self.update_navigation_buttons()
        
        # Update window title with current delivery info
        self.setWindowTitle(f"Delivery Details - {product_name} ({self.current_index + 1}/{len(self.deliveries)})")
