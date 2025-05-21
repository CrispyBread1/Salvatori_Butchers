from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)


class DashboardWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.setup_ui()
        
  def setup_ui(self):
      layout = QVBoxLayout()
      
      # Title
      title = QLabel("Stock Menu")
      title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
      layout.addWidget(title)
    
      self.setLayout(layout)
