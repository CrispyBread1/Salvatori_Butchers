from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models.product import Product
from database.products import fetch_products_stock_take

class StockTakeWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Stock Take Window')
    self.load_data()

  def load_data(self):
    data = fetch_products_stock_take(['fresh', 'dry', 'frozen'])
    print(data)
