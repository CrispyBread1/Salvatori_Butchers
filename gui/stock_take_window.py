from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from models.product import Product
from database.products import fetch_products

class StockTakeWindow(QWidget):
   def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Take Window')
