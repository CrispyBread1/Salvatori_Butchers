from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QSpinBox, QPushButton, QLabel, QScrollArea,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QGridLayout
)
from database.products import fetch_products_stock_take

class StockTakeWindow(QMainWindow):
    data = {}

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Stock Take Window')
        self.setGeometry(100, 100, 1000, 600)  # Set initial window size

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create buttons
        self.stock_button1 = QPushButton("Fresh", self)
        self.stock_button1.clicked.connect(lambda: self.load_data(['fresh']))
        self.stock_button2 = QPushButton("Dry", self)
        self.stock_button2.clicked.connect(lambda: self.load_data(['dry']))
        self.stock_button3 = QPushButton("Frozen", self)
        self.stock_button3.clicked.connect(lambda: self.load_data(['frozen']))
        self.stock_button4 = QPushButton("All", self)
        self.stock_button4.clicked.connect(lambda: self.load_data(['fresh', 'dry', 'frozen']))

        # Use QHBoxLayout for a horizontal menu
        self.stock_menu_layout = QHBoxLayout()
        self.stock_menu_layout.addWidget(self.stock_button1)
        self.stock_menu_layout.addWidget(self.stock_button2)
        self.stock_menu_layout.addWidget(self.stock_button3)
        self.stock_menu_layout.addWidget(self.stock_button4)

        # Create a frame to hold the button layout
        top_menu = QFrame(self.central_widget)
        top_menu.setLayout(self.stock_menu_layout)

        # Use QVBoxLayout for main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(top_menu)  # Add the top menu first

        # ✅ Add Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)  # Add scroll area to main layout

        # ✅ Create form container inside scroll area
        self.form_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.form_container)  # Main scrollable layout
        self.scroll_area.setWidget(self.form_container)  # Set form container inside scroll area

        # ✅ Create Label for Error Messages
        self.label = QLabel("")
        self.main_layout.addWidget(self.label)  # Add label below form

    def load_data(self, stock_category):
        self.data = fetch_products_stock_take(stock_category)
        self.render_stock_form()

    def render_stock_form(self):
    
      # ✅ Remove old form content
      self.form_container.deleteLater()
      self.form_container = QWidget()  # Create a new form container
      self.scroll_layout = QVBoxLayout(self.form_container)
      self.scroll_area.setWidget(self.form_container)  # Reassign it to the scroll area

      if not self.data:
          self.label.setText("Data has not been found")
          return

      self.label.setText("")  # ✅ Clear error message
      
      # ✅ Group products by category
      category_groups = {}
      for key in self.data:
          for product in self.data[key]:
              category = product.product_category
              if category not in category_groups:
                  category_groups[category] = []
              category_groups[category].append(product)

      num_categories = len(category_groups)  # Number of unique categories
      column_layout = QGridLayout()  # Grid layout to support dynamic columns
      
      # ✅ Create dynamic columns based on categories
      col = 0
      
      # Add Category Headings to the Top
      for category, products in category_groups.items():
          category_label = QLabel(f"<b>{category}</b>")
          category_label.setAlignment(Qt.AlignCenter)  # Align heading to the center
          column_layout.addWidget(category_label, 0, col)  # Add category heading at the top
          
          # Add Product Names and Spinboxes Below the Heading
          row = 1  # Start placing product info in the next row (below the heading)
          for product in products:
              product_spin_box = QSpinBox()
              form_label = QLabel(product.name)  # Product name label
              column_layout.addWidget(form_label, row, col)  # Place product name in grid
              column_layout.addWidget(product_spin_box, row + 1, col)  # Place spinbox below the product
              row += 2  # Move to the next row

          col += 1  # Move to the next column for the next category
      
      self.scroll_layout.addLayout(column_layout)  # ✅ Add columns to the scrollable layout
  # ✅ Add columns to the scrollable layout
