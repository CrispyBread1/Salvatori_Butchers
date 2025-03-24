from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from gui.stock_take_windows.stock_take_new_window import StockTakeNewWindow
from gui.stock_take_windows.stock_take_view_window import StockTakeViewWindow


class StockTakeWindow(QMainWindow):

  def __init__(self):
    super().__init__()

    # Set up the central widget layout
    self.central_widget = QWidget(self)
    self.setCentralWidget(self.central_widget)

    # Create stacked widget to switch between views
    self.stacked_widget = QStackedWidget(self.central_widget)

    # Main content layout
    self.content_layout = QVBoxLayout()
    self.label = QLabel("Welcome to the Main Window!", self)
    self.content_layout.addWidget(self.label)
    

    # Set up the main window content inside the stacked widget
    main_content = QWidget()
    main_content.setLayout(self.content_layout)
    self.stacked_widget.addWidget(main_content)

    # Create the product window as a component
    self.stock_take_new_window = StockTakeNewWindow()
    self.stock_take_view_window = StockTakeViewWindow()
    self.stacked_widget.addWidget(self.stock_take_new_window)
    self.stacked_widget.addWidget(self.stock_take_view_window)

    # Side navigation layout (the nav bar remains static)

    self.stock_take_menu_button1 = QPushButton("New", self)
    self.stock_take_menu_button1.clicked.connect(lambda: self.open_stock_take_new_window())
    

    # Use QHBoxLayout for a horizontal menu
    self.stock_menu_layout = QHBoxLayout()
    self.stock_menu_layout.addWidget(self.stock_take_menu_button1)

    # Create a frame to hold the button layout
    top_menu = QFrame(self.central_widget)


    # Set up the main layout (main window and sidebar)
    main_layout = QHBoxLayout(self.central_widget)
    main_layout.addWidget(self.stacked_widget)

    # Set window geometry
    self.setGeometry(100, 100, 1400, 800)
        

  def open_stock_take_new_window(self):
      self.stacked_widget.setCurrentWidget(self.stock_take_new_window)

  def open_stock_take_window(self):
      # self.stacked_widget.setCurrentWidget(self.stock_take_window)
      return


