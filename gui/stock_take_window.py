from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QDoubleSpinBox, QPushButton, QLabel, QScrollArea,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QGridLayout, QMessageBox
)
from database.products import fetch_products_stock_take, update_product, fetch_products
from resources.pdf_exporter import export_to_pdf 
from database.stock_takes import insert_stock_take, fetch_most_recent_stock_take
import json
import datetime

class StockTakeWindow(QMainWindow):
  data = {}
  form_loaded = False
  spin_boxes = {}
  category = []
  categories = ['fresh', 'dry', 'frozen']
  most_recent_stock_take = {}

  def __init__(self):
    super().__init__()

    self.setWindowTitle('Stock Take Window')
    self.setGeometry(100, 100, 1000, 600)  # Set initial window size

    # Central widget
    self.central_widget = QWidget(self)
    self.setCentralWidget(self.central_widget)

    # Create buttons
    self.stock_button1 = QPushButton("Fresh", self)
    self.stock_button1.clicked.connect(lambda: self.load_specific_data('fresh'))
    self.stock_button2 = QPushButton("Dry", self)
    self.stock_button2.clicked.connect(lambda: self.load_specific_data('dry'))
    self.stock_button3 = QPushButton("Frozen", self)
    self.stock_button3.clicked.connect(lambda: self.load_specific_data('frozen'))
    self.stock_button4 = QPushButton("All", self)
    self.stock_button4.clicked.connect(lambda: self.load_all_data())

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

    # Add Scroll Area
    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)
    self.main_layout.addWidget(self.scroll_area)  # Add scroll area to main layout

    # Create form container inside scroll area
    self.form_container = QWidget()
    self.scroll_layout = QVBoxLayout(self.form_container)  # Main scrollable layout
    self.scroll_area.setWidget(self.form_container)  # Set form container inside scroll area

    
    # Create Label for Error Messages
    self.label = QLabel("")
    self.main_layout.addWidget(self.label)  # Add label below form

    self.back_button = QPushButton("Back", self)
    self.back_button.clicked.connect(self.reset_ui)
    self.export_button = QPushButton("Export to PDF", self)
    self.export_button.clicked.connect(lambda: export_to_pdf(self, self.data))
    self.save_button = QPushButton("Save", self)
    self.save_button.clicked.connect(self.confirm_save)

    self.main_layout.addWidget(self.back_button)
    self.main_layout.addWidget(self.export_button)
    self.main_layout.addWidget(self.save_button)

    # Hide buttons initially (until data loads)
    self.back_button.hide()
    self.export_button.hide()
    self.save_button.hide()

    self.load_most_recent_stock_take()
    self.render_last_stock_take()


  def load_specific_data(self, stock_category):
    self.category = stock_category
    self.data = fetch_products_stock_take(stock_category)
    self.render_stock_form()

  def load_all_data(self):
    self.category = 'all'
    results = fetch_products() 
    self.data = {}  # Ensure it's a clean dictionary before populating

    for product in results:
        if product.stock_category not in self.data:
            self.data[product.stock_category] = []  
        self.data[product.stock_category].append(product)  # Append product to list

    self.render_stock_form()


  def render_stock_form(self):
    """Render stock take form dynamically."""

    # Clear previous spin boxes dictionary to avoid referencing deleted widgets
    self.spin_boxes = {}

    # Remove old form content
    self.form_container.deleteLater()
    
    self.form_container = QWidget()
    self.scroll_layout = QVBoxLayout(self.form_container)
    self.scroll_area.setWidget(self.form_container)

    if not self.data:
        self.label.setText("Data has not been found")
        return

    self.label.setText("")  # Clear error message

    category_groups = {}
    for key in self.data:
        for product in self.data[key]:
            category = product.product_category
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(product)

    column_layout = QGridLayout()
    col = 0

    for category, products in category_groups.items():
        category_label = QLabel(f"<b>{category.title()}</b>")
        category_label.setAlignment(Qt.AlignCenter)
        column_layout.addWidget(category_label, 0, col)

        row = 1
        for product in products:
            product_spin_box = QDoubleSpinBox()
            product_spin_box.setMaximum(100000)
            product_spin_box.setDecimals(2) 
            form_label = QLabel(product.name)
            
            column_layout.addWidget(form_label, row, col)
            column_layout.addWidget(product_spin_box, row + 1, col)
            self.spin_boxes[product.id] = product_spin_box

            row += 2

        col += 1

    self.scroll_layout.addLayout(column_layout)

    # Show buttons since form is now loaded
    self.back_button.show()
    self.export_button.show()
    self.save_button.show()


  def confirm_save(self):
    # Create a confirmation message box
    msg_box = QMessageBox(self)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowTitle('Confirm Save')
    msg_box.setText('Are you sure you want to save this data?')
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.Yes)

    # Show the message box and get user response
    response = msg_box.exec_()

    # Check the response (Yes or No)
    if response == QMessageBox.Yes:
      self.save_form_data()  # Call the function to save data
    else:
      print("Save canceled.")  # Optionally handle cancellation


  def save_form_data(self):
    """Save stock take data and reset the UI."""
    updated_data = {}
    
    for product_id, spin_box in self.spin_boxes.items():
      updated_data[product_id] = spin_box.value()
      update_product(product_id, stock_count=spin_box.value())

    json_data = json.dumps(updated_data)
    insert_stock_take(json_data, str(self.category))

    QMessageBox.information(self, "Success", "Stock take saved successfully!")

    # Reset the form after saving
    self.reset_ui()

  def reset_ui(self):
    """Clears the form and resets UI back to the menu."""
    self.spin_boxes = {}
    self.data = {}
    self.form_loaded = False

    # Remove form container
    self.form_container.deleteLater()
    self.form_container = QWidget()
    self.scroll_layout = QVBoxLayout(self.form_container)
    self.scroll_area.setWidget(self.form_container)

    self.label.setText("Stock take saved. Select a category to continue.")

    # Hide buttons since no form is displayed
    self.back_button.hide()
    self.export_button.hide()
    self.save_button.hide()
    self.load_most_recent_stock_take()
    self.render_last_stock_take()

  def render_last_stock_take(self):
    self.last_stock_take_layout = QVBoxLayout()
    self.categories.append('all')
    for category in self.categories:
      time_stamp = self.most_recent_stock_take[category].date
      last_stock_take_label = QLabel(f"<b>Last stock take for {category.title()}: </b>" + time_stamp.strftime('%d-%m-%y, %H:%M:%S'))
      # last_stock_take_label.setAlignment(Qt.AlignCenter)
      self.last_stock_take_layout.addWidget(last_stock_take_label)
    self.scroll_layout.addLayout(self.last_stock_take_layout)
    self.categories.pop()

  def load_most_recent_stock_take(self):
     self.categories.append('all')
     self.most_recent_stock_take = fetch_most_recent_stock_take(self.categories)
     self.categories.pop()


