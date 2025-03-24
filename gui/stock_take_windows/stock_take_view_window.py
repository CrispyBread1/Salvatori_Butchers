from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QDoubleSpinBox, QPushButton, QLabel, QScrollArea, QDateEdit,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow, QGridLayout, QMessageBox
)


class StockTakeViewWindow(QMainWindow):


  def __init__(self):
    super().__init__()
