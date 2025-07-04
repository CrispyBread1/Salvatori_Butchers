from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from datetime import date, datetime
from database.deliveries import fetch_deliveries_by_week
from gui.components.reusable.table import DynamicTableWidget


class GoodsInWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.chosen_date = datetime.now()
    self.setup_ui()
        
  def setup_ui(self):
      layout = QVBoxLayout()
      
      # Title
      title = QLabel("Goods In")
      title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
      layout.addWidget(title)
    
      self.dynamic_table_widget = DynamicTableWidget(self)
      layout.addWidget(self.dynamic_table_widget)


      self.setLayout(layout)
      
      self.load_product_table(self.chosen_date)

  def load_product_table(self, chose_date):
      """Load product data into the table (Hardcoded Columns)."""
      deliveries = fetch_deliveries_by_week(chose_date)

      print(deliveries)
      # if not self.products:
      #     self.label.setText("No data found.")
      #     return


      # # Set headers manually (matching database fields)
      # headers = ["Name", "Stock Cost £", "Stock Count", "Selling Price £", "Stock Category", "Product Category", "Sage Code", "Supplier", "Sold As"]
      
      # # Prepare data for the DynamicTableWidget
      # data = []
      # for product in self.products:
      #     row_data = [
      #         product.name,
      #         str(product.cost),
      #         str(product.stock_count),
      #         str(product.product_value),
      #         product.stock_category,
      #         product.product_category,
      #         product.sage_code,
      #         product.supplier,
      #         product.sold_as
      #     ]
      #     data.append(row_data)

      # # Custom format function for cells
      # def format_cell(item, row_idx, col_idx, value):
      #     # Make all cells read-only
      #     item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
          
      #     # Make Name column clickable with blue underlined text
      #     if col_idx == 0:
      #         item.setTextAlignment(Qt.AlignCenter)
      #         item.setForeground(Qt.blue)
      #         font = QFont()
      #         font.setUnderline(True)
      #         item.setFont(font)
          
      #     return item

      # # Populate the dynamic table
      # self.dynamic_table_widget.populate(headers, data, format_cell)
      
      # # Store reference to the table for easy access in other methods
      # self.table = self.dynamic_table_widget.table
      
      # # Connect signals
      # try:
      #     self.table.cellDoubleClicked.disconnect()
      # except:
      #     pass
      
      # self.table.cellDoubleClicked.connect(self.open_product_detail)
