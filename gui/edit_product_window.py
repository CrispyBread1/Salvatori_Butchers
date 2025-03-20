from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QDoubleSpinBox, QPushButton, QLabel, QScrollArea, QDateEdit,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QGridLayout, QMessageBox
)
from database.products import fetch_products_stock_take, update_product, fetch_products
from database.stock_takes import insert_stock_take, fetch_most_recent_stock_take
from datetime import datetime

class EditProductWindow(QMainWindow):
  data = {}
  form_loaded = False
  categories = ['fresh', 'dry', 'frozen']

  def __init__(self):
    super().__init__()
